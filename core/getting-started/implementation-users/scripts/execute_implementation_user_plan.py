#!/usr/bin/env python3
"""Execute supported REST steps from an HCM implementation-user plan.

This wrapper intentionally calls the FSCR Fusion REST client process instead of
duplicating OAuth/token handling. It defaults to dry-run and records an audit
artifact for every planned or executed step.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def find_fdos_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "core" / "fusion-api" / "rest-api-client" / "scripts" / "fusion_rest_client.py").exists():
            return candidate
    raise RuntimeError(f"Could not locate repository root from {start}")


FDOS_ROOT = find_fdos_root(Path(__file__).resolve())
sys.path.insert(0, str(FDOS_ROOT / "core/auth/fusion-oauth-authentication/scripts"))
from fusion_auth import validate_scim_endpoint, reject_password_fields
REST_CLIENT = FDOS_ROOT / "core" / "fusion-api" / "rest-api-client" / "scripts" / "fusion_rest_client.py"
DEFAULT_TOKEN_CACHE = "auto"
DEFAULT_USERS_ENDPOINT = "/hcmRestApi/scim/Users"
DEFAULT_ROLES_ENDPOINT = "/hcmRestApi/scim/Roles"
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_.@-]+$")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_username(username: str) -> None:
    if not USERNAME_PATTERN.fullmatch(username):
        raise ValueError(
            "Plan user.username is invalid. Regenerate the plan with a username containing only "
            "letters, numbers, dot, underscore, hyphen, or @."
        )
    if username.startswith("-") or "--" in username:
        raise ValueError("Plan user.username looks like a command option. Regenerate the plan.")


def validate_email(email: str) -> None:
    if not EMAIL_PATTERN.fullmatch(email):
        raise ValueError("Plan user.email is invalid. Regenerate the plan with a valid email address.")


def resolve_path(value: str | None, *, must_exist: bool = False) -> Path | None:
    if not value:
        return None
    raw_path = Path(value).expanduser()
    candidates = [raw_path]
    if not raw_path.is_absolute():
        candidates.extend(
            [
                Path.cwd() / raw_path,
                FDOS_ROOT / raw_path,
            ]
        )
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    if must_exist:
        checked = "\n  - ".join(str(candidate) for candidate in candidates)
        raise FileNotFoundError(f"Could not find path: {value}\nChecked:\n  - {checked}")
    return candidates[1 if len(candidates) > 1 else 0]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute supported REST steps from an HCM implementation-user plan."
    )
    parser.add_argument("--plan", help="Path to the implementation-user plan JSON.")
    parser.add_argument("--execute", action="store_true", help="Perform mutating REST calls.")
    parser.add_argument(
        "--live-preflight",
        action="store_true",
        help="Call Fusion for the user lookup only, then stop before any write.",
    )
    parser.add_argument(
        "--confirm-create-user",
        action="store_true",
        help="Required with --execute before user creation and role assignment calls are made.",
    )
    parser.add_argument("--token-cache", default=DEFAULT_TOKEN_CACHE)
    parser.add_argument("--properties", help="Fusion environment properties file for the FSCR REST client.")
    parser.add_argument(
        "--user-accounts-endpoint",
        "--users-endpoint",
        dest="users_endpoint",
        default=DEFAULT_USERS_ENDPOINT,
        help="Fusion user endpoint. Defaults to /hcmRestApi/scim/Users.",
    )
    parser.add_argument("--user-query-field", default="userName")
    parser.add_argument("--user-key-field", default="id")
    parser.add_argument("--roles-endpoint", default=DEFAULT_ROLES_ENDPOINT)
    parser.add_argument("--role-query-field", default="displayName")
    parser.add_argument("--role-key-field", default="id")
    parser.add_argument(
        "--allow-create-after-preflight-error",
        action="store_true",
        help="Removed unsafe option: supplying this flag is rejected.",
    )
    parser.add_argument(
        "--include-roles-in-user-body",
        action="store_true",
        default=False,
        help="Include finalRoleAssignments as SCIM roles in the /hcmRestApi/scim/Users create body.",
    )
    parser.add_argument(
        "--no-include-roles-in-user-body",
        action="store_false",
        dest="include_roles_in_user_body",
        help="Do not include roles in the SCIM user create body.",
    )
    parser.add_argument("--skip-role-assignments", action="store_true")
    parser.add_argument(
        "--assign-roles-to-existing",
        action="store_true",
        help="When the user already exists, assign roles to that existing SCIM user instead of stopping.",
    )
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--audit-output", help="Audit JSON output path.")
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def rest_client_base_args(args: argparse.Namespace) -> list[str]:
    if not REST_CLIENT.exists():
        raise FileNotFoundError(f"FSCR REST client not found: {REST_CLIENT}")
    command = [
        "python3",
        str(REST_CLIENT),
        "--service", "standard", "--scim-only",
        "--token-cache",
        args.token_cache,
        "--timeout",
        str(args.timeout),
    ]
    if args.properties:
        properties_path = resolve_path(args.properties, must_exist=True)
        command.extend(["--properties", str(properties_path)])
    return command


def parse_response(stdout: str) -> Any:
    text = stdout.strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        json_start = text.rfind("\n{")
        if json_start != -1:
            return json.loads(text[json_start + 1 :])
        array_start = text.rfind("\n[")
        if array_start != -1:
            return json.loads(text[array_start + 1 :])
        raise


def call_rest(
    args: argparse.Namespace,
    endpoint: str,
    *,
    method: str = "GET",
    query: list[str] | None = None,
    body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    # Policy failures must escape the lookup/error fallback before any body is staged.
    validate_scim_endpoint(endpoint)
    reject_password_fields(body)
    try:
        command = rest_client_base_args(args)
        command.insert(2, endpoint)
        command.extend(["--method", method])
        for query_param in query or []:
            command.extend(["--query", query_param])
    except Exception as exc:
        return {
            "endpoint": endpoint,
            "method": method,
            "query": query or [],
            "status": "error",
            "returnCode": None,
            "stderr": str(exc),
        }

    temp_body: Path | None = None
    try:
        if body is not None:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
                json.dump(body, handle)
                handle.write("\n")
                temp_body = Path(handle.name)
            command.extend(["--body-file", str(temp_body)])

        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            # The REST client has its own HTTP timeout, but OAuth or a stalled
            # child process can otherwise leave this safety check waiting
            # forever. Allow a small grace period for client cleanup.
            timeout=max(args.timeout + 5, 10),
        )
    except subprocess.TimeoutExpired:
        return {
            "endpoint": endpoint,
            "method": method,
            "query": query or [],
            "status": "error",
            "returnCode": None,
            "stderr": f"REST client exceeded the {max(args.timeout + 5, 10)}-second executor timeout.",
        }
    finally:
        if temp_body is not None:
            temp_body.unlink(missing_ok=True)

    result: dict[str, Any] = {
        "endpoint": endpoint,
        "method": method,
        "query": query or [],
        "status": "success" if completed.returncode == 0 else "error",
        "returnCode": completed.returncode,
        "stderr": "REST client failed; raw diagnostics suppressed" if completed.returncode else "",
    }
    if completed.returncode == 0:
        try:
            response = parse_response(completed.stdout)
            reject_password_fields(response)
            result["response"] = response
        except (json.JSONDecodeError, ValueError):
            result["status"] = "error"
            result["responseText"] = "Unsafe or non-JSON SCIM response suppressed"
    else:
        result["responseText"] = "Failed SCIM response suppressed"
    return result


def extract_items(response: Any) -> list[dict[str, Any]]:
    if isinstance(response, dict):
        resources = response.get("Resources")
        if isinstance(resources, list):
            return [item for item in resources if isinstance(item, dict)]
        items = response.get("items")
        if isinstance(items, list):
            return [item for item in items if isinstance(item, dict)]
        return [response]
    if isinstance(response, list):
        return [item for item in response if isinstance(item, dict)]
    return []


def first_value(data: dict[str, Any], names: list[str]) -> Any:
    lower_map = {key.lower(): value for key, value in data.items()}
    for name in names:
        if name in data:
            return data[name]
        if name.lower() in lower_map:
            return lower_map[name.lower()]
    return None


def nested_values(data: Any, key_names: set[str]) -> list[str]:
    values: list[str] = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key.lower() in key_names and value is not None:
                values.append(str(value))
            values.extend(nested_values(value, key_names))
    elif isinstance(data, list):
        for item in data:
            values.extend(nested_values(item, key_names))
    return values


def ora_role_identifiers(role_resource: dict[str, Any]) -> list[str]:
    candidates = nested_values(
        role_resource,
        {
            "name",
            "rolename",
            "role_name",
            "rolecode",
            "role_code",
            "code",
            "value",
            "id",
        },
    )
    return sorted({value for value in candidates if value.startswith("ORA_")})


def planned_role_identifiers(plan: dict[str, Any]) -> dict[str, list[str]]:
    identifiers: dict[str, set[str]] = {}

    def add(role_name: Any, *values: Any) -> None:
        name = str(role_name or "").strip()
        if not name:
            return
        bucket = identifiers.setdefault(name, set())
        for value in values:
            text = str(value or "").strip()
            if text.startswith("ORA_"):
                bucket.add(text)

    for role in plan.get("baseJobRoles", []):
        if isinstance(role, dict):
            add(role.get("displayName"), role.get("roleCode"), role.get("code"), role.get("name"), role.get("value"))

    for role in plan.get("abstractRoles", []):
        if isinstance(role, dict):
            add(role.get("role") or role.get("displayName"), role.get("roleCode"), role.get("code"), role.get("name"), role.get("value"))

    for role in plan.get("oracleGrounding", {}).get("distinctFunctionalSetupManagerRoles", []):
        if isinstance(role, dict):
            add(role.get("displayName"), role.get("roleCode"), role.get("code"), role.get("name"), role.get("value"))

    for role_name, values in list(identifiers.items()):
        if not values:
            identifiers.pop(role_name, None)

    return {role_name: sorted(values) for role_name, values in identifiers.items()}


def base_job_role_names(plan: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for role in plan.get("baseJobRoles", []):
        if isinstance(role, dict):
            name = str(role.get("displayName") or "").strip()
            if name:
                names.add(name)
    return names


def scim_filter_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def final_role_names(plan: dict[str, Any]) -> list[str]:
    return [str(role).strip() for role in plan.get("finalRoleAssignments", []) if str(role).strip()]


def scim_role_entries(plan: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "value": role_name,
            "type": "default",
            "primary": False,
        }
        for role_name in final_role_names(plan)
    ]


def build_user_payload(plan: dict[str, Any], *, include_roles: bool = True) -> dict[str, Any]:
    user = plan.get("user") or {}
    username = str(user.get("username") or "").strip()
    email = str(user.get("email") or "").strip()
    last_name = str(user.get("lastName") or username).strip()
    if not username:
        raise ValueError("Plan user.username is required")
    validate_username(username)
    if not email:
        raise ValueError("Plan user.email is required")
    validate_email(email)
    payload = {
        "schemas": [
            "urn:scim:schemas:core:2.0:User",
        ],
        "userName": username,
        "name": {
            "formatted": last_name,
            "familyName": last_name,
        },
        "displayName": last_name,
        "active": bool(user.get("active", True)),
        "emails": [
            {
                "value": email,
                "type": "work",
                "primary": True,
            }
        ],
    }
    if include_roles:
        roles = scim_role_entries(plan)
        if roles:
            payload["roles"] = roles
    return payload


def role_assignment_payload(role_name: str, payload_field: str) -> dict[str, Any]:
    return {payload_field: role_name}


def role_lookup_query(args: argparse.Namespace, role_name: str, *, query_field: str | None = None) -> list[str]:
    field = query_field or args.role_query_field
    return [
        f'filter={field} eq "{scim_filter_value(role_name)}"',
        "count=1",
        "attributes=id,displayName,name",
    ]


def resolve_planned_roles_for_preflight(
    args: argparse.Namespace,
    plan: dict[str, Any],
    audit: dict[str, Any],
) -> bool:
    """Resolve every planned final role before a user-creation write.

    ORA role codes are resolved by their SCIM ``name`` and verified in the
    response.  This prevents a same-display-name role from satisfying the
    implementation-user write gate.
    """

    planned_ora_identifiers = planned_role_identifiers(plan)
    all_resolved = True
    for role_name in final_role_names(plan):
        planned_identifiers = planned_ora_identifiers.get(role_name, [])
        lookup_value = planned_identifiers[0] if planned_identifiers else role_name
        lookup_field = "name" if planned_identifiers else args.role_query_field
        lookup = call_rest(
            args,
            args.roles_endpoint,
            query=role_lookup_query(args, lookup_value, query_field=lookup_field),
        )
        step: dict[str, Any] = {
            "name": "preflight_lookup_role",
            "roleName": role_name,
            "lookupField": lookup_field,
            "lookupValue": lookup_value,
            "plannedOraIdentifiers": planned_identifiers,
            **lookup,
        }
        if lookup.get("status") != "success":
            step["preflightStatus"] = "unresolved"
            audit["steps"].append(step)
            audit["manualFollowUp"].append(f"Required role lookup failed for {role_name}.")
            all_resolved = False
            continue

        role_items = extract_items(lookup.get("response"))
        if not role_items:
            step["preflightStatus"] = "unresolved"
            audit["steps"].append(step)
            audit["manualFollowUp"].append(
                f"Required role was not found through SCIM Roles: {role_name} using {lookup_field}={lookup_value}."
            )
            all_resolved = False
            continue

        role = role_items[0]
        role_id = first_value(role, [args.role_key_field, "id", "value"])
        resolved_ora_identifiers = ora_role_identifiers(role)
        step["roleId"] = role_id
        step["resolvedOraIdentifiers"] = resolved_ora_identifiers
        if not role_id or (planned_identifiers and planned_identifiers[0] not in resolved_ora_identifiers):
            step["preflightStatus"] = "unresolved"
            audit["steps"].append(step)
            audit["manualFollowUp"].append(
                f"Required role did not resolve to its planned ORA identifier: {role_name}."
            )
            all_resolved = False
            continue

        step["preflightStatus"] = "resolved"
        audit["steps"].append(step)
    return all_resolved


def role_membership_patch_payload(user_id: str, username: str) -> dict[str, Any]:
    return {
        "schemas": ["urn:oracle:apps:scim:schemas:fa:1.0:Role"],
        "members": [
            {
                "value": user_id,
            }
        ],
    }


def assign_roles_via_scim_roles(
    args: argparse.Namespace,
    plan: dict[str, Any],
    user_id: str,
    username: str,
    audit: dict[str, Any],
) -> None:
    planned_ora_identifiers = planned_role_identifiers(plan)
    base_jobs = base_job_role_names(plan)
    for role_name in final_role_names(plan):
        is_base_job_role = role_name in base_jobs
        planned_identifiers = planned_ora_identifiers.get(role_name, [])
        if is_base_job_role and not planned_identifiers:
            audit["manualFollowUp"].append(
                f"Base job role skipped because the plan has no ORA_ roleCode/name/value for {role_name}."
            )
            audit["steps"].append(
                {
                    "name": "skip_base_job_role_without_planned_ora_identifier",
                    "roleName": role_name,
                    "status": "skipped",
                    "reason": "base job role has no ORA_ roleCode/name/value in the plan",
                }
            )
            continue

        lookup_value = planned_identifiers[0] if planned_identifiers else role_name
        lookup_field = "name" if planned_identifiers else args.role_query_field
        lookup = call_rest(args, args.roles_endpoint, query=role_lookup_query(args, lookup_value, query_field=lookup_field))
        audit["steps"].append(
            {
                "name": "lookup_role",
                "roleName": role_name,
                "lookupField": lookup_field,
                "lookupValue": lookup_value,
                "baseJobRole": is_base_job_role,
                "plannedOraIdentifiers": planned_identifiers,
                **lookup,
            }
        )
        if lookup.get("status") != "success":
            audit["manualFollowUp"].append(f"Role lookup failed for {role_name}; role was not assigned.")
            continue

        role_items = extract_items(lookup.get("response"))
        if not role_items:
            audit["manualFollowUp"].append(
                f"Role not found through SCIM Roles endpoint: {role_name} using {lookup_field}={lookup_value}"
            )
            continue

        resolved_ora_identifiers = ora_role_identifiers(role_items[0])

        role_id = first_value(role_items[0], [args.role_key_field, "id", "value"])
        if not role_id:
            audit["manualFollowUp"].append(f"Role lookup did not expose an id for {role_name}; role was not assigned.")
            continue

        endpoint = f"{args.roles_endpoint.rstrip('/')}/{role_id}"
        body = role_membership_patch_payload(user_id, username)
        assignment = call_rest(args, endpoint, method="PATCH", body=body)
        assignment["requestBody"] = body
        audit["steps"].append(
            {
                "name": "assign_role_via_scim_roles",
                "roleName": role_name,
                "roleId": role_id,
                "baseJobRole": is_base_job_role,
                "plannedOraIdentifiers": planned_identifiers,
                "resolvedOraIdentifiers": resolved_ora_identifiers,
                **assignment,
            }
        )
        if assignment.get("status") != "success":
            audit["manualFollowUp"].append(f"Role assignment failed for {role_name}; review audit step.")


def default_audit_path(plan_path: Path, plan: dict[str, Any]) -> Path:
    user = plan.get("user") or {}
    username = str(user.get("username") or "implementation-user").strip() or "implementation-user"
    return plan_path.parent / f"{username}_implementation_user_execution_audit.json"


def build_preflight_query(args: argparse.Namespace, username: str) -> list[str]:
    if "/scim/" in args.users_endpoint.lower():
        return [
            f'filter={args.user_query_field} eq "{username}"',
            "count=1",
            "attributes=id,userName,active,displayName",
        ]
    return [f"q={args.user_query_field}='{username}'", "limit=1", "onlyData=true"]


def should_assign_roles(args: argparse.Namespace) -> bool:
    return not args.skip_role_assignments


def main() -> int:
    args = parse_args()
    validate_scim_endpoint(args.users_endpoint, collection="Users")
    validate_scim_endpoint(args.roles_endpoint, collection="Roles")
    if args.allow_create_after_preflight_error:
        raise ValueError("Creation after a failed identity preflight is not supported")
    plan_path = resolve_path(args.plan, must_exist=True)
    if plan_path is None:
        raise ValueError("--plan is required")
    plan = read_json(plan_path)
    reject_password_fields(plan)
    user = plan.get("user") or {}
    username = str(user.get("username") or "").strip()
    if not username:
        raise ValueError("Plan user.username is required")
    validate_username(username)
    validate_email(str(user.get("email") or "").strip())

    if args.execute and args.live_preflight:
        raise ValueError("Use either --execute or --live-preflight, not both")
    if args.execute and not args.confirm_create_user:
        raise ValueError("--execute requires --confirm-create-user")
    audit: dict[str, Any] = {
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mode": "execute" if args.execute else "live-preflight" if args.live_preflight else "dry-run",
        "plan": str(plan_path),
        "projectId": plan.get("projectId"),
        "username": username,
        "restClient": str(REST_CLIENT),
        "steps": [],
        "manualFollowUp": [],
    }

    preflight_query = build_preflight_query(args, username)
    if args.execute or args.live_preflight:
        preflight = call_rest(args, args.users_endpoint, query=preflight_query)
    else:
        preflight = {
            "endpoint": args.users_endpoint,
            "method": "GET",
            "query": preflight_query,
            "status": "planned",
        }
    audit["steps"].append({"name": "preflight_user_lookup", **preflight})

    existing_user_id = None
    if preflight.get("status") == "success":
        items = extract_items(preflight.get("response"))
        if items:
            existing_user_id = first_value(items[0], [args.user_key_field, "UserId", "userId", "id"])
            audit["existingUser"] = {
                "found": True,
                "userId": existing_user_id,
            }
    elif args.execute:
        audit["result"] = "stopped_preflight_failed"
        audit["manualFollowUp"].append(
            "Preflight user lookup failed, so the script stopped before attempting user creation. "
            "Fix the lookup endpoint/query or manually confirm the user does not exist."
        )
    role_preflight_resolved = False
    if preflight.get("status") == "success" and not existing_user_id:
        role_preflight_resolved = resolve_planned_roles_for_preflight(args, plan, audit)
        if not role_preflight_resolved:
            audit["result"] = "stopped_required_role_unresolved"
    if args.live_preflight:
        if preflight.get("status") != "success":
            audit["result"] = "stopped_preflight_failed"
        elif existing_user_id:
            audit["result"] = "stopped_existing_user_found"
        elif role_preflight_resolved:
            audit["result"] = "live_preflight_completed"
            audit["existingUser"] = {"found": False}
        audit["manualFollowUp"].append("Live preflight only; no user creation or role assignment was attempted.")
    elif existing_user_id:
        if args.execute and args.assign_roles_to_existing and should_assign_roles(args):
            assign_roles_via_scim_roles(args, plan, str(existing_user_id), username, audit)
            audit["result"] = "completed_existing_user_role_assignment"
        else:
            audit["result"] = "stopped_existing_user_found"
            audit["manualFollowUp"].append(
                "Review whether the existing user should be updated; rerun with --assign-roles-to-existing to assign roles."
            )
    elif audit.get("result") in {"stopped_preflight_failed", "stopped_required_role_unresolved"}:
        pass
    else:
        create_payload = build_user_payload(
            plan,
            include_roles=args.include_roles_in_user_body and not args.skip_role_assignments,
        )
        if args.execute:
            create = call_rest(args, args.users_endpoint, method="POST", body=create_payload)
            create["requestBody"] = create_payload
            if create.get("status") != "success":
                audit["result"] = "stopped_user_create_failed"
                audit["manualFollowUp"].append("User creation failed; review the create_user_account step before retrying.")
        else:
            create = {
                "endpoint": args.users_endpoint,
                "method": "POST",
                "status": "planned",
                "requestBody": create_payload,
            }
        audit["steps"].append({"name": "create_user_account", **create})

        user_id = None
        if create.get("status") == "success":
            response = create.get("response")
            if isinstance(response, dict):
                user_id = first_value(response, [args.user_key_field, "UserId", "userId", "id"])

        role_names = final_role_names(plan)
        if create.get("status") != "success":
            pass
        elif args.skip_role_assignments:
            audit["manualFollowUp"].append("Role assignment was skipped by --skip-role-assignments.")
        elif args.include_roles_in_user_body and "/scim/" in args.users_endpoint.lower():
            audit["manualFollowUp"].append(
                "Role values were submitted in the SCIM /Users create body; verify accepted role memberships in Fusion."
            )
        elif should_assign_roles(args) and user_id:
            assign_roles_via_scim_roles(args, plan, str(user_id), username, audit)
        elif user_id:
            audit["manualFollowUp"].append("Role assignment was not requested.")
        elif role_names:
            audit["manualFollowUp"].append(
                "Role assignment could not run because the user create response did not expose a user key."
            )

    audit["manualFollowUp"].extend(
        [
            "Run or verify Retrieve Latest LDAP Changes and Import Users and Roles into Application Security.",
        ]
    )
    audit.setdefault("result", "completed" if args.execute else "dry_run_planned")

    audit_path = Path(args.audit_output) if args.audit_output else default_audit_path(plan_path, plan)
    write_json(audit_path, audit)
    print(f"Wrote {audit_path}")
    print(f"Result: {audit['result']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

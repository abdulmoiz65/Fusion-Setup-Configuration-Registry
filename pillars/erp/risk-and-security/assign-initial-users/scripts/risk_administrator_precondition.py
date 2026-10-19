#!/usr/bin/env python3
"""Plan and evaluate the Risk Administrator prerequisite from Core results.

This helper never calls Fusion.  It produces deterministic Core request plans
and evaluates only previously returned SCIM results.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SELF_DETAILS = "/hcmRestApi/resources/11.13.18.05/selfDetails"
SCIM_USERS = "/hcmRestApi/scim/Users"
SCIM_ROLES = "/hcmRestApi/scim/Roles"
RISK_ADMINISTRATOR_ROLE = "ORA_GTG_RISK_ADMINISTRATOR_JOB"
IT_SECURITY_MANAGER_ROLE = "ORA_FND_IT_SECURITY_MANAGER_JOB"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def response_body(value: dict[str, Any]) -> dict[str, Any]:
    body = value.get("body", value)
    if not isinstance(body, dict):
        raise ValueError("Core response body must be an object")
    return body


def load_responses(specifications: list[str]) -> dict[str, dict[str, Any]]:
    responses: dict[str, dict[str, Any]] = {}
    for specification in specifications:
        response_id, separator, raw_path = specification.partition("=")
        if not separator or not response_id or not raw_path or response_id in responses:
            raise ValueError("--core-response must be a unique response_id=Core-result.json")
        responses[response_id] = read_json(Path(raw_path))
    return responses


def request(request_id: str, method: str, endpoint: str, query: dict[str, str] | None = None, body: dict[str, Any] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {"id": request_id, "service": "fusion", "method": method, "endpoint": endpoint}
    if query:
        value["query"] = query
    if body is not None:
        value["body"] = body
    return value


def canonical_digest(value: dict[str, str]) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def current_username(payload: dict[str, Any]) -> str:
    items = response_body(payload).get("items")
    if not isinstance(items, list) or len(items) != 1 or not isinstance(items[0], dict):
        raise ValueError("Signed-in user lookup must return exactly one item")
    username = items[0].get("Username")
    if not isinstance(username, str) or not username.strip():
        raise ValueError("Signed-in user lookup did not return Username")
    return username.strip()


def exactly_one_resource(payload: dict[str, Any], response_id: str) -> dict[str, Any]:
    resources = response_body(payload).get("Resources")
    if not isinstance(resources, list) or len(resources) != 1 or not isinstance(resources[0], dict):
        raise ValueError(f"Core response {response_id!r} must return exactly one SCIM resource")
    return resources[0]


def direct_resource(payload: dict[str, Any], response_id: str) -> dict[str, Any]:
    resource = response_body(payload)
    if not isinstance(resource.get("id"), str) or not resource["id"].strip():
        raise ValueError(f"Core response {response_id!r} must return one SCIM resource")
    return resource


def active_exact_user(payload: dict[str, Any], response_id: str, username: str) -> dict[str, Any]:
    user = exactly_one_resource(payload, response_id)
    actual_username = user.get("userName")
    if (
        not isinstance(user.get("id"), str)
        or not user["id"].strip()
        or user.get("active") is not True
        or not isinstance(actual_username, str)
        or actual_username.casefold() != username.casefold()
    ):
        raise ValueError("Authenticated Fusion user did not resolve to one active exact SCIM account")
    return user


def matching_roles(payload: dict[str, Any], response_id: str, expected_code: str) -> list[dict[str, Any]]:
    resources = response_body(payload).get("Resources")
    if not isinstance(resources, list) or not resources or not all(isinstance(role, dict) for role in resources):
        raise ValueError(f"{expected_code} did not resolve to a role record")
    for role in resources:
        if role.get("name") != expected_code or not isinstance(role.get("id"), str) or not role["id"].strip():
            raise ValueError(f"{expected_code} role data is invalid")
        members = role.get("members", [])
        if not isinstance(members, list) or not all(isinstance(member, dict) for member in members):
            raise ValueError(f"{expected_code} membership is invalid")
    return resources


def assignment_role(roles: list[dict[str, Any]]) -> dict[str, Any]:
    if len(roles) != 1:
        raise ValueError("Risk Administrator did not resolve uniquely for assignment")
    return roles[0]


def member_ids(role: dict[str, Any]) -> list[str]:
    return [str(member["value"]) for member in role.get("members", []) if isinstance(member.get("value"), str) and member["value"].strip()]


def member_ids_for_roles(roles: list[dict[str, Any]]) -> list[str]:
    return list(dict.fromkeys(member_id for role in roles for member_id in member_ids(role)))


def membership(roles: list[dict[str, Any]], user_id: str) -> bool:
    return user_id in member_ids_for_roles(roles)


def global_member_request(member_id: str) -> dict[str, Any]:
    return request(f"coverage_member:{member_id}", "GET", f"{SCIM_USERS}/{member_id}")


def discovery_requests(responses: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    if "current_user" not in responses:
        return [request("current_user", "GET", SELF_DETAILS, {"fields": "Username"})]
    username = current_username(responses["current_user"])
    if "authenticated_user" not in responses:
        return [request("authenticated_user", "GET", SCIM_USERS, {"filter": f'userName eq "{username}"', "count": "2"})]
    user = active_exact_user(responses["authenticated_user"], "authenticated_user", username)
    required_roles = (
        ("risk_administrator_role", RISK_ADMINISTRATOR_ROLE),
        ("it_security_manager_role", IT_SECURITY_MANAGER_ROLE),
    )
    missing_roles = [request(response_id, "GET", SCIM_ROLES, {"filter": f'name eq "{role_code}"', "count": "2"}) for response_id, role_code in required_roles if response_id not in responses]
    if missing_roles:
        return missing_roles
    risk_administrator = matching_roles(responses["risk_administrator_role"], "risk_administrator_role", RISK_ADMINISTRATOR_ROLE)
    it_security_manager = matching_roles(responses["it_security_manager_role"], "it_security_manager_role", IT_SECURITY_MANAGER_ROLE)
    user_id = str(user["id"])
    if membership(risk_administrator, user_id) or membership(it_security_manager, user_id):
        return []
    risk_member_ids = member_ids_for_roles(risk_administrator)
    ordered_members = risk_member_ids + [member_id for member_id in member_ids_for_roles(it_security_manager) if member_id not in risk_member_ids]
    for member_id in ordered_members:
        if member_id == user_id:
            continue
        response_id = f"coverage_member:{member_id}"
        if response_id not in responses:
            return [global_member_request(member_id)]
        member = direct_resource(responses[response_id], response_id)
        if member.get("active") is True:
            return []
    return []


def organization_coverage(responses: dict[str, dict[str, Any]], user_id: str, risk_administrator: list[dict[str, Any]], it_security_manager: list[dict[str, Any]]) -> bool:
    if membership(risk_administrator, user_id) or membership(it_security_manager, user_id):
        return True
    risk_member_ids = member_ids_for_roles(risk_administrator)
    for member_id in risk_member_ids + [member_id for member_id in member_ids_for_roles(it_security_manager) if member_id not in risk_member_ids]:
        if member_id == user_id:
            continue
        response_id = f"coverage_member:{member_id}"
        if response_id not in responses:
            raise ValueError("Coverage review is incomplete")
        if direct_resource(responses[response_id], response_id).get("active") is True:
            return True
    return False


def discovery(responses: dict[str, dict[str, Any]], environment: str) -> dict[str, Any]:
    pending = discovery_requests(responses)
    if pending:
        return {"stage": "discovery", "status": "awaiting_core_results", "requests": pending}
    username = current_username(responses["current_user"])
    user = active_exact_user(responses["authenticated_user"], "authenticated_user", username)
    risk_administrator = matching_roles(responses["risk_administrator_role"], "risk_administrator_role", RISK_ADMINISTRATOR_ROLE)
    it_security_manager = matching_roles(responses["it_security_manager_role"], "it_security_manager_role", IT_SECURITY_MANAGER_ROLE)
    user_id = str(user["id"])
    runner_has_access = membership(risk_administrator, user_id) or membership(it_security_manager, user_id)
    coverage = organization_coverage(responses, user_id, risk_administrator, it_security_manager)
    risk_administrator_role_id = None if runner_has_access else str(assignment_role(risk_administrator)["id"])
    approval_scope = {
        "environment": environment,
        "authenticated_username": username,
        "authenticated_user_id": user_id,
        "risk_administrator_role_id": risk_administrator_role_id,
    }
    return {
        "stage": "discovery",
        "status": "completed_runner_ready" if runner_has_access else "awaiting_final_approval",
        "environment": environment,
        "organization_coverage": coverage,
        "authenticated_username": username,
        "authenticated_user_id": user_id,
        "risk_administrator_role_id": risk_administrator_role_id,
        "approval_digest_sha256": canonical_digest(approval_scope),
        "runner_access_ready": runner_has_access,
        "requests": [],
    }


def preflight(source: dict[str, Any], responses: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if source.get("status") != "awaiting_final_approval" or source.get("approved") is not True:
        raise ValueError("Preflight requires the approved discovery result")
    username = source.get("authenticated_username")
    user_id = source.get("authenticated_user_id")
    role_id = source.get("risk_administrator_role_id")
    environment = source.get("environment")
    if not all(isinstance(value, str) and value for value in (username, user_id, role_id, environment)):
        raise ValueError("Approved discovery result is incomplete")
    approval_scope = {
        "environment": environment,
        "authenticated_username": username,
        "authenticated_user_id": user_id,
        "risk_administrator_role_id": role_id,
    }
    if source.get("approval_digest_sha256") != canonical_digest(approval_scope) or source.get("approved_plan_digest_sha256") != source.get("approval_digest_sha256"):
        raise ValueError("Approved discovery result does not match the exact authenticated-user assignment plan")
    pending = []
    if "preflight_user" not in responses:
        pending.append(request("preflight_user", "GET", f"{SCIM_USERS}/{user_id}"))
    if "preflight_risk_administrator_role" not in responses:
        pending.append(request("preflight_risk_administrator_role", "GET", f"{SCIM_ROLES}/{role_id}"))
    if pending:
        return {"stage": "preflight", "status": "awaiting_core_results", "requests": pending}
    user = direct_resource(responses["preflight_user"], "preflight_user")
    if user.get("active") is not True or user.get("id") != user_id or not isinstance(user.get("userName"), str) or user["userName"].casefold() != username.casefold():
        raise ValueError("Authenticated Fusion user is no longer an active exact match")
    role = direct_resource(responses["preflight_risk_administrator_role"], "preflight_risk_administrator_role")
    if role.get("id") != role_id or role.get("name") != RISK_ADMINISTRATOR_ROLE:
        raise ValueError("Risk Administrator role no longer resolves to the approved target")
    members = role.get("members", [])
    if not isinstance(members, list) or not all(isinstance(member, dict) for member in members):
        raise ValueError("Risk Administrator membership is invalid")
    if membership([role], user_id):
        return {"stage": "preflight", "status": "completed_no_change_required", "environment": environment, "runner_access_ready": True, "requests": []}
    assignment = request("assignment", "PATCH", f"{SCIM_ROLES}/{role_id}", body={"members": [{"value": user_id, "operation": "ADD"}]})
    return {
        "stage": "preflight",
        "status": "ready_for_core_assignment",
        "environment": environment,
        "authenticated_username": username,
        "authenticated_user_id": user_id,
        "risk_administrator_role_id": role_id,
        "requests": [assignment],
    }


def verify(source: dict[str, Any], responses: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if source.get("status") != "ready_for_core_assignment":
        raise ValueError("Verification requires a ready-for-assignment preflight result")
    user_id = source.get("authenticated_user_id")
    role_id = source.get("risk_administrator_role_id")
    environment = source.get("environment")
    if not all(isinstance(value, str) and value for value in (user_id, role_id, environment)):
        raise ValueError("Preflight result is incomplete")
    if "assignment" not in responses:
        return {"stage": "verify", "status": "awaiting_core_assignment", "requests": source.get("requests", [])}
    if int(responses["assignment"].get("status", 200)) >= 400:
        return {"stage": "verify", "status": "assignment_failed", "environment": environment, "runner_access_ready": False, "requests": []}
    if "verify_risk_administrator_role" not in responses:
        return {"stage": "verify", "status": "awaiting_core_results", "requests": [request("verify_risk_administrator_role", "GET", f"{SCIM_ROLES}/{role_id}")]}
    role = direct_resource(responses["verify_risk_administrator_role"], "verify_risk_administrator_role")
    if role.get("id") != role_id or role.get("name") != RISK_ADMINISTRATOR_ROLE:
        return {"stage": "verify", "status": "verification_failed", "environment": environment, "runner_access_ready": False, "requests": []}
    verified = membership([role], user_id)
    return {"stage": "verify", "status": "completed_runner_ready" if verified else "verification_failed", "environment": environment, "runner_access_ready": verified, "requests": []}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", required=True, choices=("discovery", "preflight", "verify"))
    parser.add_argument("--environment")
    parser.add_argument("--input", help="Approved discovery or preflight result for later stages.")
    parser.add_argument("--core-response", action="append", default=[], help="Repeat as response_id=Core-result.json.")
    parser.add_argument("--output", required=True)
    parser.add_argument("--request-plan-output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    responses = load_responses(args.core_response)
    source = read_json(Path(args.input)) if args.input else {}
    if args.stage == "discovery":
        if not isinstance(args.environment, str) or not args.environment:
            raise ValueError("--environment is required for discovery")
        result = discovery(responses, args.environment)
    elif args.stage == "preflight":
        result = preflight(source, responses)
    else:
        result = verify(source, responses)
    write_json(Path(args.output), result)
    write_json(Path(args.request_plan_output), {"environment": result.get("environment", source.get("environment")), "requests": result.get("requests", [])})
    if result.get("requests"):
        print("I’m checking the current setup. I’ll return with a complete review or a clear next action.")
    elif result.get("status") == "completed_runner_ready":
        print("The current setup review is complete. Organization coverage and the authenticated user's access are ready.")
    elif result.get("status") == "awaiting_final_approval":
        print("The current setup review is complete. The authenticated user needs Risk Administrator access before the next step.")
    else:
        print("The current setup review could not be completed. No access change was made.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

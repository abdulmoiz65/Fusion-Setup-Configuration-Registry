#!/usr/bin/env python3
"""Build, validate, preview, and verify safe Library Goal creates."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import date
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from goal_business_rules import validate_library_goal_rules


VALID_VARIANTS = {"PERFORMANCE", "DEVELOPMENT"}
VALID_STATUS_CODES = {"I", "A"}
VISIBLE_MEANINGS = {
    "ALL": "HR specialist, manager, and worker",
}
KEY_CREATE_FIELDS = ("GoalName", "TypeCode", "StatusCode", "Visible")


class PayloadValidationError(ValueError):
    """Raised when no safe canonical Library Goal payload can be built."""


def attributes(metadata: dict[str, Any]) -> dict[str, dict[str, Any]]:
    resource = metadata.get("Resources", {}).get("libraryGoals", metadata)
    entries = resource.get("attributes", [])
    if isinstance(entries, dict):
        entries = [{"name": name, **field} for name, field in entries.items() if isinstance(field, dict)]
    return {
        entry["name"]: entry
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }


def external_id_suggestion(value: str, maximum: int) -> str:
    normalized = re.sub(r"[^A-Za-z0-9_-]+", "-", value).strip("-_") or "GOAL"
    if len(normalized) <= maximum:
        return normalized
    suffix = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:7].upper()
    return f"{normalized[: maximum - len(suffix) - 1].rstrip('-_')}-{suffix}"


def has_default_value_expression(field: dict[str, Any]) -> bool:
    return field.get("hasDefaultValueExpression") is True or field.get(
        "hasDefaultValueExpression"
    ) == "true"


def uses_server_external_id_derivation(metadata: dict[str, Any]) -> bool:
    live_attributes = attributes(metadata)
    return has_default_value_expression(
        live_attributes.get("GoalId", {})
    ) and has_default_value_expression(live_attributes.get("GoalExternalId", {}))


def _field_accepts_input(field: dict[str, Any], operation: str = "create") -> bool:
    def is_flag(name, expected):
        value = field.get(name)
        return value is expected or (isinstance(value, str) and value.casefold() == str(expected).casefold())
    return not (
        is_flag("readOnly", True)
        or is_flag("writable", False)
        or any(is_flag(key, False) for key in (
            ("createable", "creatable") if operation == "create" else ("updateable", "updatable")
        ))
    )


def _allowed_codes(field: dict[str, Any]) -> set[str]:
    raw = field.get("allowedValues") or field.get("enum") or []
    codes: set[str] = set()
    if isinstance(raw, dict):
        raw = list(raw.values())
    if not isinstance(raw, list):
        return codes
    for entry in raw:
        if isinstance(entry, str):
            codes.add(entry)
        elif isinstance(entry, dict):
            for name in ("value", "code", "LookupCode"):
                if isinstance(entry.get(name), str):
                    codes.add(entry[name])
                    break
    return codes


def _validate_code(field_name: str, value: str, field: dict[str, Any]) -> None:
    codes = _allowed_codes(field)
    if codes and (not isinstance(value, str) or value not in codes):
        raise PayloadValidationError(
            f"{field_name} value {value!r} is not in the current advertised value set"
        )


def prepare_create_payload(
    payload: dict[str, Any],
    metadata: dict[str, Any],
    *,
    variant: str,
    allow_active_create: bool = False,
) -> dict[str, Any]:
    """Materialize safe defaults into the exact payload that will be approved."""
    variant = str(variant).upper()
    if variant not in VALID_VARIANTS:
        raise PayloadValidationError("variant must be PERFORMANCE or DEVELOPMENT")
    if "AvailableTo" in payload:
        raise PayloadValidationError(
            "AvailableTo is read-only; send the validated Visible code instead"
        )

    prepared = dict(payload)
    supplied_variant = prepared.get("TypeCode")
    if "TypeCode" in prepared and supplied_variant != variant:
        raise PayloadValidationError(f"{variant} Library Goals require TypeCode={variant}")
    prepared["TypeCode"] = variant
    prepared.setdefault("StatusCode", "I")
    prepared.setdefault("Visible", "ALL")
    # Create-only business default; explicit values (including null/blank) are
    # not omission. Metadata/LOV validation below retains its existing policy.
    prepared.setdefault("PriorityCode", "MEDIUM")

    for field_name in KEY_CREATE_FIELDS:
        if prepared.get(field_name) in (None, ""):
            raise PayloadValidationError(f"{field_name} must be non-null for Library Goal create")

    live_attributes = attributes(metadata)
    for field_name in KEY_CREATE_FIELDS:
        field = live_attributes.get(field_name)
        if field is None:
            raise PayloadValidationError(
                f"current Library Goal metadata does not expose key create field {field_name}"
            )
        if not _field_accepts_input(field):
            raise PayloadValidationError(
                f"current Library Goal metadata does not allow create input for {field_name}"
            )

    status = str(prepared["StatusCode"])
    if status not in VALID_STATUS_CODES:
        raise PayloadValidationError("StatusCode must resolve to I or A")
    if status == "A" and not allow_active_create:
        raise PayloadValidationError(
            "active create requires an explicit create-active contract; normal creates default to I"
        )
    visible = str(prepared["Visible"])
    if visible not in VISIBLE_MEANINGS and visible not in _allowed_codes(live_attributes["Visible"]):
        raise PayloadValidationError(
            "Visible must resolve to a supported role-audience code before preview"
        )
    _validate_code("StatusCode", status, live_attributes["StatusCode"])
    _validate_code("Visible", visible, live_attributes["Visible"])
    if "PriorityCode" in live_attributes:
        _validate_code("PriorityCode", prepared["PriorityCode"], live_attributes["PriorityCode"])

    if "StartDate" in prepared:
        try:
            date.fromisoformat(prepared["StartDate"])
        except (ValueError, TypeError) as exc:
            raise PayloadValidationError("StartDate must be ISO YYYY-MM-DD") from exc
    business_unit_id = prepared.get("BusinessUnitId")
    if business_unit_id is not None and (
        isinstance(business_unit_id, bool)
        or not str(business_unit_id).isdigit()
        or int(business_unit_id) < 1
    ):
        raise PayloadValidationError("BusinessUnitId must be one exact positive identifier")

    if "GoalExternalId" not in prepared and uses_server_external_id_derivation(metadata):
        prepared.pop("GoalId", None)
        prepared.pop("GoalExternalId", None)
    errors = validate_create(prepared, metadata, variant=variant,
                             duplicate_risk_acknowledged=True)
    if errors:
        raise PayloadValidationError("; ".join(f"{e['field']}:{e['code']}" for e in errors))
    return prepared


def validate_create(
    payload: dict[str, Any],
    metadata: dict[str, Any],
    *,
    variant: str,
    duplicate_risk_acknowledged: bool = False,
) -> list[dict[str, str]]:
    live_attributes = attributes(metadata)
    errors: list[dict[str, str]] = []
    try:
        validate_library_goal_rules(payload, variant)
    except (ValueError, TypeError) as exc:
        errors.append({"field": "business_rules", "code": "INVALID_BUSINESS_VALUE", "message": str(exc)})
    for name, value in payload.items():
        field = live_attributes.get(name)
        if field is None or not _field_accepts_input(field):
            errors.append({"field": name, "code": "NOT_WRITABLE",
                           "message": "Current create metadata must advertise every supplied field as writable."})
            continue
        try:
            _validate_code(name, value, field)
        except PayloadValidationError as exc:
            errors.append({"field": name, "code": "INVALID_CODE", "message": str(exc)})
        maximum = field.get("maxLength")
        if name != "GoalExternalId" and maximum and isinstance(value, str) and len(value) > int(maximum):
            errors.append({"field": name, "code": "MAX_LENGTH_EXCEEDED", "message": "Value exceeds current metadata length."})
    for name, details in live_attributes.items():
        if details.get("mandatory") and details.get("inputRequired") and payload.get(name) in (None, ""):
            errors.append(
                {
                    "field": name,
                    "code": "MISSING_REQUIRED",
                    "message": "Current metadata requires a value.",
                }
            )
    for name in KEY_CREATE_FIELDS:
        if payload.get(name) is None or not str(payload.get(name, "")).strip():
            errors.append(
                {
                    "field": name,
                    "code": "MISSING_KEY_CREATE_FIELD",
                    "message": "FSCR requires this field to be non-null in the exact create payload.",
                }
            )
    if payload.get("TypeCode") != variant:
        errors.append(
            {
                "field": "TypeCode",
                "code": "VARIANT_MISMATCH",
                "message": f"{variant} Library Goals require TypeCode={variant}.",
            }
        )
    if payload.get("StatusCode") not in VALID_STATUS_CODES:
        errors.append(
            {
                "field": "StatusCode",
                "code": "INVALID_STATUS",
                "message": "StatusCode must resolve to I or A.",
            }
        )
    if payload.get("Visible") not in VISIBLE_MEANINGS and payload.get("Visible") not in _allowed_codes(live_attributes.get("Visible", {})):
        errors.append(
            {
                "field": "Visible",
                "code": "INVALID_VISIBILITY",
                "message": "Visible must resolve to a supported role-audience code.",
            }
        )
    if "AvailableTo" in payload:
        errors.append(
            {
                "field": "AvailableTo",
                "code": "READ_ONLY_FIELD",
                "message": "AvailableTo is verification-only; send Visible instead.",
            }
        )

    if "StartDate" in payload:
        try:
            date.fromisoformat(payload["StartDate"])
        except (TypeError, ValueError):
            errors.append({"field": "StartDate", "code": "INVALID_DATE", "message": "StartDate must be ISO YYYY-MM-DD."})
    if "BusinessUnitId" in payload and (isinstance(payload["BusinessUnitId"], bool)
        or not str(payload["BusinessUnitId"]).isdigit() or int(payload["BusinessUnitId"]) < 1):
        errors.append({"field": "BusinessUnitId", "code": "INVALID_ID", "message": "Resolve one positive Business Unit ID."})
    external_id = payload.get("GoalExternalId")
    field = live_attributes.get("GoalExternalId", {})
    maximum = int(field.get("maxLength") or field.get("precision") or 0)
    if external_id and maximum and len(str(external_id)) > maximum:
        errors.append(
            {
                "field": "GoalExternalId",
                "code": "MAX_LENGTH_EXCEEDED",
                "message": f"External ID has {len(str(external_id))} characters; maximum is {maximum}.",
                "suggestion": external_id_suggestion(str(external_id), maximum),
            }
        )
    if (
        "GoalExternalId" not in payload
        and not uses_server_external_id_derivation(metadata)
        and not duplicate_risk_acknowledged
    ):
        errors.append(
            {
                "field": "GoalExternalId",
                "code": "DUPLICATE_RISK_ACKNOWLEDGEMENT_REQUIRED",
                "message": f"Server External-ID derivation is unavailable; exact GoalName plus TypeCode={variant} duplicate controls require acknowledgement.",
            }
        )
    return errors


def approval_preview(
    payload: dict[str, Any],
    environment: str,
    *,
    variant: str,
    metadata: dict[str, Any],
    duplicate_risk_acknowledged: bool = False,
    request_path: str = "/libraryGoals",
    allow_active_create: bool = False,
) -> dict[str, Any]:
    payload = deepcopy(payload)
    if payload.get("StatusCode") == "A" and not allow_active_create:
        raise PayloadValidationError("active create requires an explicit create-active contract")
    errors = validate_create(
        payload,
        metadata,
        variant=variant,
        duplicate_risk_acknowledged=duplicate_risk_acknowledged,
    )
    if errors:
        raise PayloadValidationError(
            "cannot preview an invalid Library Goal payload: "
            + "; ".join(f"{item['field']}:{item['code']}" for item in errors)
        )
    if not isinstance(environment, str) or not environment.strip():
        raise PayloadValidationError("environment must be non-empty for approval binding")
    operation = f"Create {variant.title()} Library Goal"
    approval_envelope = {
        "environment": environment.strip().casefold(),
        "operation": operation,
        "request_path": request_path,
        "identity": {
            "GoalName": payload["GoalName"],
            "TypeCode": payload["TypeCode"],
        },
        "payload": payload,
    }
    canonical_payload = json.dumps(
        approval_envelope, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    display = [{"field": key, "value": value} for key, value in payload.items()]
    display.extend(
        [
            {"field": "Environment", "value": environment},
            {"field": "Operation", "value": operation},
            {"field": "Request path", "value": request_path},
            {"field": "Initial status", "value": payload["StatusCode"]},
            {
                "field": "Available To",
                "value": VISIBLE_MEANINGS.get(payload["Visible"], payload["Visible"]),
            },
            {
                "field": "Duplicate control",
                "value": f"Exact GoalName plus TypeCode={variant}",
            },
        ]
    )
    if uses_server_external_id_derivation(metadata) and "GoalExternalId" not in payload:
        display.append(
            {
                "field": "GoalExternalId default",
                "value": "Fusion derives GoalExternalId from generated GoalId; post-create equality verification is required.",
            }
        )
    fingerprint = hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()
    return {
        "display": display,
        "environment": environment,
        "operation": operation,
        "request_path": request_path,
        "payload": payload,
        "approval_envelope": approval_envelope,
        "sha256": fingerprint,
        "approval": {
            "required": "Reply Approve, Yes, or Go ahead to continue.",
            "accepted_examples": ["approve", "approved", "yes", "go ahead", "proceed", "submit it"],
            "fingerprint_is_internal": True,
            "payload_change_requires_fresh_approval": True,
        },
    }


def approval_is_current(
    approved_fingerprint: str,
    preview: dict[str, Any],
    *,
    current_state: dict[str, Any] | list[dict[str, Any]] | None = None,
) -> bool:
    try:
        if "operations" in preview:
            envelope = deepcopy(preview["approval_envelope"])
            for key in (
                "operation",
                "approval_mode",
                "execution_mode",
                "transport_atomic",
                "operations",
                "requests",
            ):
                envelope[key] = deepcopy(preview[key])
            envelope["environment"] = preview["environment"].strip().casefold()
            states = current_state if isinstance(current_state, list) else [current_state]
            if len(states) != len(preview["operations"]) or any(not isinstance(state, dict) for state in states):
                return False
            for operation, state in zip(preview["operations"], states):
                if any(state.get(key) != value for key, value in operation["precondition"].items()):
                    return False
            digest = hashlib.sha256(
                json.dumps(envelope, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
            ).hexdigest()
            return approved_fingerprint == preview["sha256"] == digest
        envelope = deepcopy(preview["approval_envelope"])
        for key in ("payload", "request_path", "item_path", "operation", "identity", "precondition"):
            if key in preview:
                envelope[key] = preview[key]
        envelope["environment"] = preview["environment"].strip().casefold()
        if "batch" in preview:
            if current_state is None or any(key not in current_state or current_state[key] != value for key, value in envelope["precondition"].items()):
                return False
            parts = preview["batch"]["parts"]
            if len(parts) != 1 or parts[0]["payload"] != envelope["payload"] or parts[0]["path"] != envelope["item_path"] or parts[0]["operation"] != "update":
                return False
        digest = hashlib.sha256(json.dumps(envelope, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        return approved_fingerprint == preview["sha256"] == digest
    except (KeyError, TypeError, AttributeError):
        return False


def verify_created_goal(expected: dict[str, Any], actual: dict[str, Any], *, metadata: dict[str, Any] | None = None) -> list[dict[str, str]]:
    """Return blocking verification mismatches for one freshly created row."""
    errors: list[dict[str, str]] = []
    for name in KEY_CREATE_FIELDS:
        if actual.get(name) in (None, ""):
            errors.append(
                {
                    "field": name,
                    "code": "INVALID_CREATED_STATE",
                    "message": "Created Library Goal returned a null key configuration value.",
                }
            )
    # Verify every approved caller-supplied scalar, not only lifecycle fields.
    # This catches silent loss of Description, StartDate, and future supported
    # scope/configuration values before a Run Book task can complete.
    for name, expected_value in expected.items():
        if name == "AvailableTo":
            continue
        if actual.get(name) != expected_value:
            errors.append(
                {
                    "field": name,
                    "code": "VERIFICATION_MISMATCH",
                    "message": "Created value does not match the approved payload.",
                }
            )
    visible = expected.get("Visible")
    meanings = VISIBLE_MEANINGS if metadata is None else metadata.get("availableToMeanings", {})
    if visible in meanings and actual.get("AvailableTo") != meanings[visible]:
        errors.append(
            {
                "field": "AvailableTo",
                "code": "VERIFICATION_MISMATCH",
                "message": "Returned Available To meaning does not match the approved Visible code.",
            }
        )
    if metadata is not None and uses_server_external_id_derivation(metadata) and "GoalExternalId" not in expected:
        if actual.get("GoalId") in (None, "") or str(actual.get("GoalId")) != str(actual.get("GoalExternalId")):
            errors.append({"field": "GoalExternalId", "code": "GENERATED_ID_MISMATCH",
                           "message": "Verify the metadata-declared generated GoalId/GoalExternalId relationship."})
    return errors


def _environment_host(environment: str) -> str:
    if not isinstance(environment, str) or not environment.strip():
        raise PayloadValidationError("environment must be non-empty")
    parsed = urlsplit(environment if "://" in environment else "https://" + environment)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise PayloadValidationError("environment must identify one HTTPS Fusion host")
    return parsed.netloc.casefold()


def _validated_path(value: str, *, environment: str, label: str, item: bool) -> str:
    if not isinstance(value, str) or not value.strip() or value.startswith("//"):
        raise PayloadValidationError(f"{label} must be a non-empty same-host path")
    parsed = urlsplit(value)
    if parsed.query or parsed.fragment or parsed.username or parsed.password:
        raise PayloadValidationError(f"{label} must not contain query, fragment, or credentials")
    if parsed.scheme or parsed.netloc:
        if parsed.scheme != "https" or parsed.netloc.casefold() != _environment_host(environment):
            raise PayloadValidationError(f"{label} must belong to the selected HTTPS environment")
    path = parsed.path
    if not path.startswith("/") or any(part in {".", ".."} for part in unquote(path).split("/")):
        raise PayloadValidationError(f"{label} must be a safe absolute resource path")
    if item and not re.fullmatch(r"/(?:[^/?#]+/)*libraryGoals/[^/?#]+", path):
        raise PayloadValidationError("item_path must be a fresh opaque Library Goal item path")
    return value


def _normalize_update_contract(
    contract: dict[str, Any], *, environment: str, item_path: str
) -> dict[str, Any]:
    if not isinstance(contract, dict):
        raise PayloadValidationError("current operation_contract is required")
    method = str(contract.get("method", "")).upper()
    content_type = str(contract.get("content_type") or contract.get("contentType") or "").casefold()
    transport = str(contract.get("transport", "")).casefold()
    request_path = contract.get("request_path") or contract.get("requestPath")
    if method == "PATCH" and "json" in content_type and transport in {"", "item", "item_patch"}:
        request_path = request_path or item_path
        _validated_path(request_path, environment=environment, label="request_path", item=True)
        if urlsplit(request_path).path != urlsplit(item_path).path:
            raise PayloadValidationError("PATCH request_path must be the fresh selected Library Goal item path")
        return {
            "transport": "item_patch",
            "method": "PATCH",
            "content_type": contract.get("content_type") or contract.get("contentType"),
            "request_path": request_path,
            "atomic": contract.get("atomic") is True,
        }
    if (
        method == "POST"
        and content_type == "application/vnd.oracle.adf.batch+json"
        and transport in {"adf_batch", "batch"}
        and contract.get("batch_enabled") is True
    ):
        if not request_path:
            raise PayloadValidationError("metadata-supported ADF batch requires its current request_path")
        _validated_path(request_path, environment=environment, label="ADF batch request_path", item=False)
        return {
            "transport": "adf_batch",
            "method": "POST",
            "content_type": contract.get("content_type") or contract.get("contentType"),
            "request_path": request_path,
            "atomic": contract.get("atomic") is True,
        }
    raise PayloadValidationError(
        "current operation contract supports neither item PATCH nor an explicitly batch-enabled ADF update"
    )


def build_update_execution_preview(
    operations: list[dict[str, Any]],
    *,
    environment: str,
    approval_mode: str = "single_group",
) -> dict[str, Any]:
    """Build one approval plan while resolving transport per operation.

    ``single_group`` controls only approval cardinality.  It never implies an
    ADF batch request.  Each operation must carry a fresh row, current metadata,
    fresh item path, requested scalar changes, and a current operation contract.
    """
    _environment_host(environment)
    if approval_mode not in {"single_group", "per_operation"}:
        raise PayloadValidationError("approval_mode must be single_group or per_operation")
    if not isinstance(operations, list) or not operations:
        raise PayloadValidationError("at least one Library Goal update operation is required")

    resolved: list[dict[str, Any]] = []
    for index, source in enumerate(deepcopy(operations), start=1):
        if not isinstance(source, dict):
            raise PayloadValidationError("every Library Goal update operation must be an object")
        row = source.get("row")
        changes = source.get("changes")
        metadata = source.get("metadata")
        item_path = source.get("item_path")
        if not isinstance(row, dict) or not isinstance(changes, dict) or not changes:
            raise PayloadValidationError("every update requires a fresh row and non-empty changes")
        if not isinstance(metadata, dict):
            raise PayloadValidationError("every update requires current Library Goal metadata")
        _validated_path(item_path, environment=environment, label="item_path", item=True)
        identity = {
            key: row.get(key)
            for key in ("GoalId", "GoalExternalId", "GoalName", "TypeCode")
            if row.get(key) not in (None, "")
        }
        if not identity.get("GoalName") or identity.get("TypeCode") not in VALID_VARIANTS:
            raise PayloadValidationError("fresh Library Goal identity must include GoalName and a valid TypeCode")
        if not any(identity.get(key) for key in ("GoalId", "GoalExternalId")):
            raise PayloadValidationError("fresh target requires an immutable Library Goal identifier")
        live_attributes = attributes(metadata)
        precondition = dict(identity)
        for name, value in changes.items():
            field = live_attributes.get(name)
            if field is None or not _field_accepts_input(field, "update"):
                raise PayloadValidationError(f"current metadata does not allow {name} update")
            if name not in row:
                raise PayloadValidationError(f"fresh current state must include {name} before preview")
            if name == "StatusCode":
                if value not in VALID_STATUS_CODES:
                    raise PayloadValidationError("StatusCode must resolve to I or A")
                _validate_code(name, value, field)
            precondition[name] = row[name]
        contract = _normalize_update_contract(
            source.get("operation_contract"), environment=environment, item_path=item_path
        )
        resolved.append(
            {
                "index": index,
                "identity": identity,
                "precondition": precondition,
                "changes": changes,
                "item_path": item_path,
                "transport": contract["transport"],
                "method": contract["method"],
                "content_type": contract["content_type"],
                "request_path": contract["request_path"],
                "atomic": contract["atomic"],
                "transport_reason": "current_operation_contract",
            }
        )

    all_one_batch = (
        all(item["transport"] == "adf_batch" for item in resolved)
        and len({item["request_path"] for item in resolved}) == 1
        and len({item["content_type"] for item in resolved}) == 1
    )
    requests: list[dict[str, Any]] = []
    if all_one_batch:
        requests.append(
            {
                "method": "POST",
                "path": resolved[0]["request_path"],
                "content_type": resolved[0]["content_type"],
                "body": {
                    "parts": [
                        {
                            "id": f"Update-library-goal-{item['index']}",
                            "path": item["item_path"],
                            "operation": "update",
                            "payload": item["changes"],
                        }
                        for item in resolved
                    ]
                },
                "operation_indexes": [item["index"] for item in resolved],
            }
        )
    else:
        for item in resolved:
            body = item["changes"]
            if item["transport"] == "adf_batch":
                body = {
                    "parts": [
                        {
                            "id": f"Update-library-goal-{item['index']}",
                            "path": item["item_path"],
                            "operation": "update",
                            "payload": item["changes"],
                        }
                    ]
                }
            requests.append(
                {
                    "method": item["method"],
                    "path": item["request_path"],
                    "content_type": item["content_type"],
                    "body": body,
                    "operation_indexes": [item["index"]],
                }
            )

    envelope = {
        "environment": environment.strip().casefold(),
        "operation": "Update Library Goals",
        "approval_mode": approval_mode,
        "execution_mode": "single_request" if len(requests) == 1 else "multiple_requests",
        # One HTTP request, including an ADF batch, is not evidence of an
        # all-or-nothing transaction.  Claim atomicity only when every current
        # operation contract explicitly advertises it.
        "transport_atomic": all_one_batch and all(item["atomic"] for item in resolved),
        "operations": resolved,
        "requests": requests,
    }
    fingerprint = hashlib.sha256(
        json.dumps(envelope, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    preview = {
        **deepcopy(envelope),
        "environment": environment,
        "approval_envelope": envelope,
        "sha256": fingerprint,
        "approval": {
            "required": "Reply Approve, Yes, or Go ahead to continue.",
            "fingerprint_is_internal": True,
            "payload_change_requires_fresh_approval": True,
            "approval_does_not_select_transport": True,
        },
    }
    if len(resolved) == 1:
        preview.update(
            {
                "identity": resolved[0]["identity"],
                "precondition": resolved[0]["precondition"],
                "request_path": resolved[0]["request_path"],
                "item_path": resolved[0]["item_path"],
                "payload": resolved[0]["changes"],
            }
        )
    return preview


def build_status_update_preview(
    row: dict[str, Any],
    *,
    status_code: str,
    environment: str,
    metadata: dict[str, Any],
    item_path: str,
    operation_contract: dict[str, Any],
) -> dict[str, Any]:
    """Build one status preview from the current operation contract."""
    return build_update_execution_preview(
        [
            {
                "row": row,
                "changes": {"StatusCode": status_code},
                "metadata": metadata,
                "item_path": item_path,
                "operation_contract": operation_contract,
            }
        ],
        environment=environment,
    )


def classify_existing_goal(row: dict[str, Any]) -> dict[str, Any]:
    missing = [name for name in ("StatusCode", "Visible") if row.get(name) in (None, "")]
    if missing:
        return {
            "status": "invalid_existing_state",
            "code": "INVALID_EXISTING_LIBRARY_GOAL_STATE",
            "missing_fields": missing,
            "action": "Stop duplicate create and prepare an explicit repair or replacement decision.",
        }
    return {"status": "valid_existing_state", "missing_fields": []}


def verify_existing_goal_for_reuse(expected: dict[str, Any], actual: dict[str, Any], *,
                                  environment: str, expected_environment: str,
                                  item_read_verified: bool) -> dict[str, Any]:
    """A search candidate or a structurally valid row is not proof of usability."""
    required = {"GoalName", "TypeCode", "StatusCode", "Visible"}
    if (not environment or environment != expected_environment or item_read_verified is not True
            or not required.issubset(expected) or actual.get("GoalId") in (None, "")):
        return {"status": "unresolved", "can_skip_create": False}
    mismatches = [field for field, value in expected.items()
                  if value is None or actual.get(field) != value]
    return {"status": "verified_usable" if not mismatches else "verified_existing_not_usable",
            "can_skip_create": not mismatches, "mismatched_fields": mismatches}


def approved_create_body(
    payload: dict[str, Any], preview: dict[str, Any], approved_fingerprint: str,
    environment: str, metadata: dict[str, Any], *, variant: str,
    request_path: str = "/libraryGoals", duplicate_risk_acknowledged: bool = False,
    allow_active_create: bool = False,
) -> dict[str, Any]:
    """Validate the actual outgoing body without repairing it after approval."""
    current = approval_preview(
        payload, environment, variant=variant, metadata=metadata,
        request_path=request_path,
        duplicate_risk_acknowledged=duplicate_risk_acknowledged,
        allow_active_create=allow_active_create,
    )
    if (not approval_is_current(approved_fingerprint, preview)
            or current["sha256"] != approved_fingerprint):
        raise PayloadValidationError("submission differs from the approved create preview")
    return deepcopy(current["payload"])


def write_new_json(path: Path, value: Any) -> None:
    """Never silently replace an approved or caller-owned artifact."""
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + "\n")


def main(*, variant: str | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", required=True, type=Path)
    parser.add_argument("--payload", required=True, type=Path)
    parser.add_argument("--environment", required=True)
    parser.add_argument("--request-path", default="/libraryGoals")
    parser.add_argument("--preview-output", type=Path)
    parser.add_argument("--prepared-output", type=Path)
    parser.add_argument("--approved-preview", type=Path)
    parser.add_argument("--approved-fingerprint")
    parser.add_argument("--submission-output", type=Path)
    parser.add_argument("--variant", choices=sorted(VALID_VARIANTS), default=variant)
    parser.add_argument("--allow-active-create", action="store_true")
    parser.add_argument("--duplicate-risk-acknowledged", action="store_true")
    args = parser.parse_args()
    if not args.variant:
        parser.error("--variant is required")
    if variant and args.variant != variant:
        parser.error("--variant cannot override this task's variant")
    submission = args.approved_preview is not None
    if submission != bool(args.approved_fingerprint) or submission != bool(args.submission_output):
        parser.error("submission requires --approved-preview, --approved-fingerprint and --submission-output together")
    if submission and (args.preview_output or args.prepared_output):
        parser.error("preview and submission handoff are separate steps")
    outputs = [path.resolve() for path in (args.preview_output, args.prepared_output, args.submission_output) if path]
    if len(set(outputs)) != len(outputs) or any(path.exists() for path in outputs):
        parser.error("output paths must be distinct new artifacts; overwrite is not allowed")
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    source = json.loads(args.payload.read_text(encoding="utf-8"))
    try:
        if submission:
            preview = json.loads(args.approved_preview.read_text(encoding="utf-8"))
            body = approved_create_body(
                source, preview, args.approved_fingerprint, args.environment, metadata,
                variant=args.variant, request_path=args.request_path,
                duplicate_risk_acknowledged=args.duplicate_risk_acknowledged,
                allow_active_create=args.allow_active_create,
            )
            write_new_json(args.submission_output, body)
            print(json.dumps({"valid": True, "body_file": str(args.submission_output),
                              "sha256": args.approved_fingerprint}))
            return 0
        prepared = prepare_create_payload(
            source,
            metadata,
            variant=args.variant,
            allow_active_create=args.allow_active_create,
        )
    except (PayloadValidationError, OSError, ValueError) as exc:
        print(json.dumps({"valid": False, "errors": [{"code": "PAYLOAD_INVALID", "message": str(exc)}]}, indent=2))
        return 2
    errors = validate_create(
        prepared,
        metadata,
        variant=args.variant,
        duplicate_risk_acknowledged=args.duplicate_risk_acknowledged,
    )
    preview = approval_preview(
        prepared, args.environment, variant=args.variant, metadata=metadata,
        request_path=args.request_path,
        duplicate_risk_acknowledged=args.duplicate_risk_acknowledged,
        allow_active_create=args.allow_active_create,
    ) if not errors else None
    if preview is not None:
        try:
            if args.preview_output:
                write_new_json(args.preview_output, preview)
            if args.prepared_output:
                write_new_json(args.prepared_output, prepared)
        except OSError as exc:
            print(json.dumps({"valid": False, "errors": [{"code": "ARTIFACT_PERSISTENCE", "message": str(exc)}]}))
            return 2
    print(
        json.dumps(
            {
                "valid": not errors,
                "errors": errors,
                "preview": preview,
            },
            indent=2,
        )
    )
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())

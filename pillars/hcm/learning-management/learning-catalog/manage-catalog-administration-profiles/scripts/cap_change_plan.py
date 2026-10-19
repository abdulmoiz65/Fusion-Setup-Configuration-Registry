"""Deterministic local CAP change planning; never payload validation or approval.

Consume a versioned cap_proposal, an unfiltered routed root-list result and an
explicit operation for each selected row. No HTTP, file writes or authorization
are performed. Missing rows mean no action, never deletion. A complete accessible
baseline establishes neither global absence nor management suitability.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import json
import re
import sys
from urllib.parse import urlsplit

import cap_proposal


ROOT_FIELDS = ("name", "description", "visibility")
OPERATIONS = frozenset(cap_proposal.INTENTS)
EXTRA_OPERATIONS = {"contributors", "content-defaults", "certificates", "delete", "reconcile"}
COMMON_CONTRACTS = ("operation-specific-privileges", "exact-target-and-input-binding",
                    "immutable-artifact-approval", "shared-task-validation",
                    "loader-outcome-and-exact-readback")
OPERATION_CONTRACTS = {
    "create": ("root-post-template", "omission-and-server-defaults", "generated-number-readback",
               "contributor-free-or-parent-child-create-contract"),
    "update": ("root-patch-template", "canonical-composite-key", "date-and-concurrency-contract"),
    "activate": ("status-transition", "canonical-composite-key", "date-and-concurrency-contract",
                 "default-provider-and-usage-restrictions"),
    "deactivate": ("status-transition", "canonical-composite-key", "date-and-concurrency-contract",
                   "default-provider-and-usage-restrictions"),
    "delete": ("delete-semantics", "canonical-composite-key", "destination-and-usage-restrictions"),
    "contributors": ("canonical-person-resolution", "writable-contributor-section", "parent-child-keys",
                     "additive-versus-replacement-semantics", "effective-membership-after-processing"),
    "content-defaults": ("existing-seeded-type-row", "type-specific-template-and-fields",
                         "null-reset-and-inheritance-semantics"),
    "certificates": ("existing-certificate-row", "permitted-template-lookup",
                     "certificate-template-and-fields", "configuration-versus-rendering-verification"),
    "reconcile": ("supported-shared-action-executor", "action-arguments", "correlated-process-monitoring"),
    "reuse": ("management-and-content-suitability", "effective-contributors-and-access"),
}


def _text(value, *, maximum=4000):
    return (isinstance(value, str) and bool(value.strip()) and len(value) <= maximum
            and not any(ord(char) < 32 for char in value))


def _target(environment, confirmed_host):
    if not isinstance(environment, str) or not re.fullmatch(r"[A-Za-z0-9_.-]{1,80}", environment):
        raise ValueError("An explicit environment is required")
    if not isinstance(confirmed_host, str):
        raise ValueError("An explicit HTTPS origin is required")
    parsed = urlsplit(confirmed_host)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password
            or parsed.path or parsed.query or parsed.fragment
            or not re.fullmatch(r"https://[A-Za-z0-9.-]+(?::[0-9]{1,5})?", confirmed_host)):
        raise ValueError("The target must be an HTTPS origin without credentials or paths")
    if parsed.port is not None and not 1 <= parsed.port <= 65535:
        raise ValueError("Invalid target port")
    return {"environment": environment, "host": confirmed_host}


def _proposal_rows(proposal):
    if (not isinstance(proposal, dict) or proposal.get("schema_version") != "1.0"
            or not _text(proposal.get("proposal_id"), maximum=200)
            or type(proposal.get("revision")) is not int or proposal["revision"] < 1
            or not isinstance(proposal.get("rows"), list) or len(proposal["rows"]) > 100):
        raise ValueError("A bounded versioned proposal is required")
    rows = {}
    for row in proposal["rows"]:
        if (not isinstance(row, dict) or not _text(row.get("row_id"), maximum=200)
                or row["row_id"] in rows or not set(cap_proposal.ROW_FIELDS) <= set(row)):
            raise ValueError("Proposal rows need unique stable identities")
        # Reuse the established field contract without generating/replacing text.
        supplied = {key: row[key] for key in cap_proposal.ROW_FIELDS}
        normalized = cap_proposal.normalize_row(supplied, row["row_id"])
        if any(normalized[key] != row[key] for key in cap_proposal.ROW_FIELDS):
            raise ValueError("Proposal rows must already contain their reviewable proposed values")
        rows[row["row_id"]] = row
    return rows


def _request(request, rows):
    allowed = {"row_id", "operation", "selector", "fields", "change_ref", "change_sha256"}
    if not isinstance(request, dict) or set(request) - allowed:
        raise ValueError("Unknown change request field; raw REST payloads are not accepted")
    row_id, operation = request.get("row_id"), request.get("operation")
    if not isinstance(row_id, str) or row_id not in rows or operation not in OPERATIONS:
        raise ValueError("Select a proposal row and an explicit supported planning operation")
    if operation != rows[row_id]["intent"]:
        raise ValueError("Revise the proposal explicitly before changing its operation")
    if operation == "create":
        if "selector" in request:
            raise ValueError("Creation must not select an existing profile")
    else:
        selector = request.get("selector")
        if (not isinstance(selector, dict) or len(selector) != 1
                or not set(selector) <= {"name", "number"}
                or not _text(next(iter(selector.values())), maximum=4000)):
            raise ValueError("An existing profile requires exact name OR number")
    if operation in {"create", "update"}:
        fields = request.get("fields", list(ROOT_FIELDS) if operation == "create" else None)
        if (not isinstance(fields, list) or not fields or len(fields) != len(set(fields))
                or any(field not in ROOT_FIELDS for field in fields)
                or (operation == "create" and "name" not in fields)):
            raise ValueError("Select explicit root fields; create requires name")
    elif "fields" in request:
        raise ValueError("Root fields cannot stand in for lifecycle or child contracts")
    if operation in EXTRA_OPERATIONS:
        if (not _text(request.get("change_ref")) or not isinstance(request.get("change_sha256"), str)
                or not re.fullmatch(r"[a-f0-9]{64}", request["change_sha256"])):
            raise ValueError("Child/destructive/action intent needs a protected change reference and digest")
    elif {"change_ref", "change_sha256"} & set(request):
        raise ValueError("Unexpected opaque change intent for root planning")
    return deepcopy(request)


def _baseline_state(baseline, target):
    if not isinstance(baseline, dict) or not isinstance(baseline.get("items"), list):
        raise ValueError("Use the routed unfiltered root-list result")
    items = baseline["items"]
    if len(items) > 50000 or any(not isinstance(item, dict) for item in items):
        raise ValueError("Invalid or unbounded baseline collection")
    complete = (baseline.get("pagination_completed") is True and baseline.get("status") == "complete"
                and not baseline.get("errors"))
    if baseline.get("environment") != target["environment"] or baseline.get("host") != target["host"]:
        return items, "baseline_target_mismatch"
    if not complete:
        return items, "baseline_incomplete"
    numbers = [item.get("learningCatalogProfileNumber") for item in items]
    if (any(not _text(number) for number in numbers)
            or len(numbers) != len(set(numbers))
            or any(not _text(item.get("name"), maximum=250) for item in items)):
        return items, "baseline_identity_invalid"
    return items, None


def _block(row, code):
    if code not in row["blockers"]:
        row["blockers"].append(code)
    row["status"] = "blocked"


def _plan_row(request, proposal_row, items, baseline_error):
    operation = request["operation"]
    result = {"row_id": request["row_id"], "operation": operation, "status": "proposed",
              "profile_number": None, "changes": {}, "blockers": [],
              "required_contracts": list(OPERATION_CONTRACTS[operation]) +
                  ([] if operation == "reuse" else list(COMMON_CONTRACTS)),
              "write_eligible": False, "executable": False,
              "source": proposal_row["source"], "contributor_counts": {
                  "requested": (proposal_row["contributors"] or {}).get("requested_count"),
                  "resolved": None, "effective": None}}
    if baseline_error:
        _block(result, baseline_error)
        return result
    if operation == "create":
        if any(item["name"] == proposal_row["name"] for item in items):
            _block(result, "existing_profile_requires_explicit_reuse_or_update")
        if proposal_row["broad_general"] and any(item.get("isSystemDefault") == "Y" for item in items):
            _block(result, "seeded_profile_suitability_review_required")
        for field in ("ownership", "contributors"):
            if proposal_row[field] is None:
                _block(result, "missing_" + field)
        for field in request.get("fields", ROOT_FIELDS):
            if proposal_row[field] is None:
                _block(result, "missing_" + field)
            else:
                result["changes"][field] = {"before_known": False, "after": proposal_row[field]}
        result["omitted_root_fields"] = [field for field in ROOT_FIELDS if field not in result["changes"]]
        return result
    selector = request["selector"]
    key = "learningCatalogProfileNumber" if "number" in selector else "name"
    selected = [item for item in items if item.get(key) == next(iter(selector.values()))]
    if len(selected) != 1:
        _block(result, "ambiguous_profile" if selected else "no_accessible_profile")
        return result
    existing = selected[0]
    result["profile_number"] = existing["learningCatalogProfileNumber"]
    result["system_default"] = existing.get("isSystemDefault")
    if operation == "update":
        for field in request["fields"]:
            if proposal_row[field] is None:
                _block(result, "missing_" + field)
            elif field not in existing:
                _block(result, "baseline_field_unavailable_" + field)
            elif existing[field] != proposal_row[field]:
                result["changes"][field] = {"before_known": True, "before": existing[field],
                                            "after": proposal_row[field]}
        if "name" in result["changes"] and any(item["name"] == proposal_row["name"] and item != existing for item in items):
            _block(result, "rename_conflicts_with_accessible_profile")
        if not result["changes"] and not result["blockers"]:
            result["status"] = "noop"
    elif operation in {"activate", "deactivate"}:
        state = existing.get("status")
        desired = "ORA_ACTIVE" if operation == "activate" else "ORA_INACTIVE"
        if state not in {"ORA_ACTIVE", "ORA_INACTIVE"}:
            _block(result, "current_status_unsupported_or_unknown")
        elif state == desired:
            result["status"] = "noop"
        else:
            result["changes"]["status"] = {"before_known": True, "before": state, "after": desired}
    elif operation == "reuse":
        if existing.get("status") == "ORA_INACTIVE":
            _block(result, "explicit_activation_required")
        elif existing.get("status") != "ORA_ACTIVE":
            _block(result, "current_status_unsupported_or_unknown")
        result["root_differences"] = [field for field in ROOT_FIELDS
                                      if proposal_row[field] is not None and existing.get(field) != proposal_row[field]]
    elif operation == "delete":
        if existing.get("isSystemDefault") == "Y":
            _block(result, "system_default_deletion_forbidden")
        elif existing.get("isSystemDefault") != "N":
            _block(result, "system_default_identity_unverified")
    return result


def build_plan(proposal, baseline, requests, *, environment, confirmed_host):
    """Return non-executable per-row change proposals with exact input binding.

    ``fields`` is a list drawn from name/description/visibility; its values come
    exclusively from the immutable proposal revision. Existing operations require
    a selector with exactly one name or number. Child/destructive/action requests
    bind a sanitized change_ref and SHA256, not unverified payload fields.
    """
    target = _target(environment, confirmed_host)
    proposal_rows = _proposal_rows(proposal)
    if not isinstance(requests, list) or not 1 <= len(requests) <= 100:
        raise ValueError("Provide one to 100 explicit operation requests")
    requests = [_request(request, proposal_rows) for request in requests]
    if len({request["row_id"] for request in requests}) != len(requests):
        raise ValueError("Select at most one explicit operation per proposal row")
    items, baseline_error = _baseline_state(baseline, target)
    rows = [_plan_row(request, proposal_rows[request["row_id"]], items, baseline_error) for request in requests]
    # Two aliases for the same number are not independent operations. Never infer
    # order, merge changes, or silently discard an operation in a mixed request.
    counts = Counter(row["profile_number"] for row in rows if row["profile_number"])
    resulting_names = Counter(proposal_rows[row["row_id"]]["name"] for row in rows
                              if row["operation"] == "create" or "name" in row["changes"])
    for row in rows:
        if row["profile_number"] and counts[row["profile_number"]] > 1:
            _block(row, "multiple_operations_for_same_profile")
        if ((row["operation"] == "create" or "name" in row["changes"])
                and resulting_names[proposal_rows[row["row_id"]]["name"]] > 1):
            _block(row, "duplicate_resulting_name")
    status = "blocked" if any(row["blockers"] for row in rows) else "noop" if all(row["status"] == "noop" for row in rows) else "proposed"
    plan = {"schema_version": "1.0", "status": status, "target": target,
            "binding": {"proposal_id": proposal["proposal_id"], "proposal_revision": proposal["revision"],
                        "proposal_sha256": cap_proposal.digest(proposal),
                        "baseline_sha256": cap_proposal.digest(baseline)},
            "requests": requests, "rows": rows, "unselected_rows": [key for key in proposal_rows
                      if key not in {request["row_id"] for request in requests}],
            "batch_contracts": (["multi-row-template-and-ordering", "per-row-identity-correlation",
                                  "non-atomic-partial-outcomes"] if len(rows) > 1 else []),
            "approval": None, "write_eligible": False, "executable": False,
            "limitations": ["Account-visible, effective-date and language-limited baseline only.",
                            "Baseline hash binds a snapshot; it does not establish freshness or write privileges.",
                            "Proposed operations are not validated load payloads or an execution route.",
                            "Ownership, central override and contributor counts do not establish effective access."]}
    plan["plan_sha256"] = cap_proposal.digest(plan)
    return plan


def validate_binding(plan, proposal, baseline, *, environment, confirmed_host):
    """Reject edited plans and stale revisions/targets; never grant write approval."""
    if not isinstance(plan, dict) or not isinstance(plan.get("requests"), list):
        raise ValueError("Invalid plan")
    expected = build_plan(proposal, baseline, plan["requests"], environment=environment,
                          confirmed_host=confirmed_host)
    if plan != expected:
        raise ValueError("Change plan no longer matches its proposal, baseline or target")
    return {"status": "bound", "plan_sha256": expected["plan_sha256"],
            "write_eligible": False, "executable": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("build", "verify"))
    args = parser.parse_args()
    try:
        payload = json.load(sys.stdin)
        options = {"environment": payload["environment"], "confirmed_host": payload["confirmed_host"]}
        if args.action == "build":
            result = build_plan(payload["proposal"], payload["baseline"], payload["requests"], **options)
        else:
            result = validate_binding(payload["plan"], payload["proposal"], payload["baseline"], **options)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 2 if result["status"] == "blocked" else 0
    except (KeyError, TypeError, ValueError):
        print(json.dumps({"status": "invalid_input", "write_eligible": False,
                          "executable": False, "message": "Use the local change-plan contract; no action was executed."}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

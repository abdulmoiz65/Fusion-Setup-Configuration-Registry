"""Check Manage Project Statuses operation boundaries locally, without Fusion I/O.

This is a scope guard, not a validator, package builder or execution approval.
Identity, editability, references, provenance and import approval remain with the
task's declared resolvers, Task Hook and Data Loader.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


SUPPORTED = {"read", "create", "update", "validate", "export", "import", "end_date"}
UNSUPPORTED = {"rename", "clear", "delete", "remove_lifecycle", "replace_lifecycle"}


def result(status, reason, message):
    return {"scope_status": status, "reason": reason, "message": message,
            "task_validation_complete": False, "import_authorized": False}


def targets(value):
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise ValueError("LifecycleTargets must be a list of resolved nonblank code strings")
    if len(set(value)) != len(value):
        raise ValueError("LifecycleTargets contains duplicate codes")
    return set(value)


def check(request, baseline=None):
    if not isinstance(request, dict) or not isinstance(request.get("operation"), str):
        return result("invalid", "missing_operation", "Supply a normalized operation")
    operation = request["operation"]
    if operation in UNSUPPORTED:
        return result("unsupported", "unverified_mutation_contract", "This operation has no verified selected route; retain the business intent and stop before lookups or package creation")
    if operation not in SUPPORTED:
        return result("invalid", "unknown_operation", "Resolve the operation; do not interpret it as create")
    changes = request.get("changes", {})
    clears = request.get("clear_fields", [])
    if not isinstance(changes, dict) or not isinstance(clears, list) or any(not isinstance(f, str) or not f.strip() for f in clears):
        return result("invalid", "invalid_change_shape", "changes must be an object and clear_fields a list of field names")
    if baseline is not None and not isinstance(baseline, dict):
        return result("invalid", "invalid_baseline", "Supply the resolved baseline as an object")
    scope_fields = {"operation", "StatusType", "ProjectStatusName", "changes", "clear_fields", "LifecycleTargets", "lifecycle_intent"}
    if operation != "create" and set(request) - scope_fields:
        return result("invalid", "unnormalized_change_fields", "For existing rows, put explicit scalar changes in changes; pass only the documented scope input fields")
    if set(changes) & {"LifecycleTargets", "lifecycle_intent", "operation", "StatusType"}:
        return result("invalid", "misplaced_scope_fields", "Keep lifecycle intent/targets and source identity outside changes; changing the status object is not an ordinary update")
    if "lifecycle_intent" in request and "LifecycleTargets" not in request:
        return result("invalid", "missing_target_set", "An explicit lifecycle intent requires the requested target set")
    if operation in {"read", "export"} and (changes or clears or "LifecycleTargets" in request):
        return result("invalid", "read_with_changes", "A read/export cannot contain requested changes")
    if clears or (operation != "create" and any(v is None or v == "" for v in changes.values())):
        return result("unsupported", "persisted_clear_unverified", "Explicit clearing is not supported; omit unchanged intake cells before constructing changes")
    if operation != "create" and "ProjectStatusName" in changes:
        original = request.get("ProjectStatusName")
        if original is None and baseline is not None:
            original = baseline.get("ProjectStatusName")
        if original is None:
            return result("needs_baseline", "rename_identity_unresolved", "Resolve the existing name before interpreting a requested name change")
        if changes["ProjectStatusName"] != original:
            return result("unsupported", "rename_unverified", "A changed alternate-key name is a rename, not an ordinary update")
    if baseline is not None:
        for field in ("StatusType", "ProjectStatusName"):
            if field in request and (field not in baseline or request[field] != baseline[field]):
                return result("invalid", "baseline_identity_mismatch", "The supplied baseline does not match the requested object/name")
    if "LifecycleTargets" in request or "NextAllowableStatusFlag" in changes or (operation == "create" and "NextAllowableStatusFlag" in request):
        if operation != "create" and baseline is None:
            return result("needs_baseline", "lifecycle_baseline_required", "Resolve current mode and complete lifecycle targets before checking this change")
        try:
            previous = set() if operation == "create" else targets(baseline["LifecycleTargets"])
            mode = changes.get("NextAllowableStatusFlag", request.get("NextAllowableStatusFlag") if operation == "create" else baseline["NextAllowableStatusFlag"])
            old_mode = None if operation == "create" else baseline["NextAllowableStatusFlag"]
            intent = request.get("lifecycle_intent", "replace")
            if not isinstance(intent, str) or intent not in {"append", "replace"}:
                raise ValueError("lifecycle_intent must be append or replace")
            proposed = targets(request["LifecycleTargets"]) if "LifecycleTargets" in request else previous
            if not isinstance(mode, str) or mode not in {"A", "N", "S", "U"}:
                raise ValueError("Resolve the requested lifecycle mode to A, N, S or U")
            if previous and mode != old_mode:
                return result("unsupported", "lifecycle_reinterpretation", "Changing the mode with existing children requires an unverified removal/rekeying contract")
            if mode in {"A", "N"} and proposed:
                return result("invalid", "targets_with_all_or_none", "All/None cannot be submitted with requested lifecycle targets")
            if intent == "append":
                proposed |= previous
            if previous - proposed:
                return result("unsupported", "lifecycle_removal_unverified", "The requested complete set removes existing targets; dropping CSV rows is not removal")
            if mode in {"S", "U"} and not proposed:
                return result("invalid", "missing_lifecycle_targets", "Status/classification mode requires resolved lifecycle targets")
        except (KeyError, ValueError) as exc:
            return result("invalid", "incomplete_lifecycle_evidence", str(exc))
        output = result("eligible_for_task_validation", "scope_supported", "Continue the normal task checks; this scope result does not authorize import")
        output["proposed_lifecycle_targets"] = sorted(proposed)
        return output
    return result("eligible_for_task_validation", "scope_supported", "Continue the normal task checks; this scope result does not authorize import")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="JSON object with request and optional baseline")
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text())
        if not isinstance(data, dict):
            raise ValueError("Input must be an object")
        output = check(data.get("request"), data.get("baseline"))
    except (OSError, ValueError) as exc:
        output = result("invalid", "input_validation", str(exc))
    print(json.dumps(output, indent=2))
    return {"eligible_for_task_validation": 0, "invalid": 1, "unsupported": 2, "needs_baseline": 3}[output["scope_status"]]


if __name__ == "__main__":
    raise SystemExit(main())

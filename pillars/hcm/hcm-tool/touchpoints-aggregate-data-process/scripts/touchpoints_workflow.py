"""Read-only Touchpoints planning and evidence-shape checks; no external I/O.

Evidence provenance, Run Book synchronization and live approval remain the
invoking skill's responsibility. Output is NOT a core Run Book creation payload.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
from touchpoints_task_plan import enrich_plan


JOB = "JobDefinition://oracle/apps/ess/hcm/touchpoints/core/setup/ProcessPersonAggregationsParentJob"
CONTEXT = ("project_id", "environment", "configuration_revision")
TASKS = {
    "profiles": ("Touchpoints Profile Options", "Touchpoints profile provider"),
    "checkins": ("Check-In Templates", "Performance Management: Check-In Templates"),
    "feedback": ("Request Feedback Template", "Performance Management: Requested Feedback Template"),
    "surveys": ("Pulse Surveys", "User: UI configuration and assignment"),
    "nudges": ("Nudges", "User: UI configuration"),
}
DISPOSITIONS = {"unknown", "configure", "already_configured", "completed", "not_applicable"}
ALL_KEYS = (*TASKS, "readiness", "full", "daily")


def selected_scope(state):
    """Consume the agent's explicit, source-backed scope decision, never keywords.

    A focused follow-up is not a scope amendment. Persist approved_scope before
    resuming; an intentional amendment requires a new source-backed decision.
    """
    if state.get("run_status") == "abandoned":
        raise ValueError("Run abandoned; start a new project from the new user prompt")
    scope = state.get("scope")
    if not isinstance(scope, dict) or not text(scope.get("source_reference")):
        raise ValueError("Explicit scope and source_reference required; no automatic expansion")
    mode = scope.get("mode")
    keys = scope.get("selected_tasks")
    if mode == "implementation":
        if keys not in (None, list(ALL_KEYS)):
            raise ValueError("Implementation scope requires the complete task set")
        keys = list(ALL_KEYS)
    elif mode == "selected_tasks":
        if (not isinstance(keys, list) or not keys
                or any(not isinstance(k, str) or k not in ALL_KEYS or k == "readiness" for k in keys)
                or len(set(keys)) != len(keys)):
            raise ValueError("Select distinct supported tasks; readiness is implementation-only")
        keys = [key for key in ALL_KEYS if key in keys]
    else:
        raise ValueError("Scope mode must be implementation or selected_tasks")
    resolved = {"mode": mode, "selected_tasks": keys}
    previous = state.get("approved_scope")
    if (isinstance(previous, dict) and previous.get("mode") == "selected_tasks"
            and isinstance(previous.get("selected_tasks"), list)
            and all(isinstance(key, str) and key in ALL_KEYS for key in previous["selected_tasks"])
            and len(set(previous["selected_tasks"])) == len(previous["selected_tasks"])):
        previous = {**previous, "selected_tasks": [key for key in ALL_KEYS if key in previous["selected_tasks"]]}
    if previous is not None and previous != resolved:
        raise ValueError("Scope differs from approved_scope; explicitly reconcile the plan before resuming")
    return resolved


def text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def timestamp(value: object) -> bool:
    if not text(value):
        return False
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).utcoffset() is not None
    except ValueError:
        return False


def context_matches(record: dict, state: dict) -> bool:
    return all(record.get(key) == state[key] for key in CONTEXT)


def attested(record: object, state: dict) -> bool:
    return (
        isinstance(record, dict)
        and context_matches(record, state)
        and all(text(record.get(key)) for key in ("actor", "reference"))
        and timestamp(record.get("recorded_at"))
    )


def full_succeeded(record: object, state: dict) -> bool:
    """Require explicit ESS success evidence, not the core CLI's exit code."""
    if not isinstance(record, dict):
        return False
    request_id = record.get("request_id")
    valid_id = (
        type(request_id) is int and request_id > 0
        or isinstance(request_id, str) and request_id.isdecimal() and int(request_id) > 0
    )
    return bool(
        valid_id
        and context_matches(record, state)
        and record.get("job_definition_id") == JOB
        and record.get("run_type") == "ORA_HRE_FULL_RUN"
        and record.get("cause") == "PROCESS_SUCCESS"
        and record.get("errors_present") is not True
        and not any(record.get(key) for key in ("error_type", "error_warning_message", "error_warning_detail"))
        and timestamp(record.get("completed_at"))
        and text(record.get("verification_reference"))
    )


def daily_verified(record: object, state: dict) -> bool:
    """A recurring parent's configured schedule is distinct from future runs."""
    return bool(
        isinstance(record, dict)
        and full_succeeded(state.get("full_run"), state)
        and context_matches(record, state)
        and str(record.get("full_request_id")) == str(state["full_run"]["request_id"])
        and type(record.get("request_id")) is int and record["request_id"] > 0
        and record.get("job_definition_id") == JOB
        and record.get("run_type") == "ORA_HRE_INCREMENTAL_RUN"
        and record.get("request_type") == "RECUR_PARENT"
        and record.get("schedule_verified") is True
        and record.get("errors_present") is False
        and timestamp(record.get("verified_at"))
        and text(record.get("verification_reference"))
        and text(record.get("approval_reference"))
    )


def evaluate(state: dict) -> dict:
    if not isinstance(state, dict) or not all(text(state.get(key)) for key in CONTEXT):
        raise ValueError("project_id, environment and configuration_revision are required")
    scope = selected_scope(state)
    selected = scope["selected_tasks"]
    implementation = scope["mode"] == "implementation"
    dependencies = state.get("dependencies", {})
    if not isinstance(dependencies, dict) or set(dependencies) - TASKS.keys():
        raise ValueError("dependencies must contain only the five documented dependency keys")
    rows = []
    for key, (name, owner) in TASKS.items():
        if key not in selected:
            continue
        item = dependencies.get(key, {})
        if not isinstance(item, dict):
            raise ValueError(f"{key}: dependency must be an object")
        disposition = item.get("disposition", "unknown")
        if not isinstance(disposition, str) or disposition not in DISPOSITIONS:
            raise ValueError(f"{key}: unsupported disposition")
        missing = item.get("missing_inputs", [])
        if not isinstance(missing, list) or any(not text(value) for value in missing):
            raise ValueError(f"{key}: missing_inputs must be an array of business input names")
        evidence = item.get("evidence", {})
        resolved = False
        status = "Awaiting confirmation"
        remote_status = "open"
        if disposition == "configure":
            status = "Blocked — input needed" if missing else "Pending configuration"
        elif disposition in {"already_configured", "completed", "not_applicable"}:
            resolved = attested(evidence, state)
            if disposition == "not_applicable":
                resolved = resolved and key != "profiles" and text(evidence.get("reason"))
                status, remote_status = "Not Applicable — user confirmed", "not-applicable"
            elif disposition == "completed":
                resolved = resolved and key not in {"surveys", "nudges"} and text(evidence.get("verification_reference"))
                status, remote_status = "Completed — verified", "completed"
            else:
                # Profile outcomes require provider readback, not an attestation.
                resolved = resolved and key != "profiles"
                status, remote_status = "Completed — user confirmed", "completed"
            if not resolved:
                status, remote_status = "Blocked — missing or mismatched evidence", "open"
        rows.append({
            "key": key, "name": name, "owner": owner,
            "disposition": disposition, "status": status,
            "proposed_runbook_status": remote_status, "resolved": bool(resolved),
            "missing_inputs": missing if disposition == "configure" else [],
            "delegate_configuration": disposition == "configure" and key in {"checkins", "feedback"} and not missing,
        })
    configuration_ready = all(row["resolved"] for row in rows)
    confirmation = state.get("readiness_confirmation", {})
    confirmed = attested(confirmation, state) and confirmation.get("confirmed") is True
    full_ready = implementation and configuration_ready and confirmed
    success = full_succeeded(state.get("full_run"), state)
    schedule_success = daily_verified(state.get("daily_schedule"), state)
    result = {
        "schema_version": "1.0", "kind": "touchpoints_configuration_plan",
        **{key: state[key] for key in CONTEXT}, "tasks": rows + [
            {"key": "readiness", "name": "Confirm Touchpoints Configuration Readiness",
             "status": "Confirmed" if full_ready else "Awaiting confirmation" if configuration_ready else "Blocked — configuration unresolved"},
            {"key": "full", "name": "Aggregate Oracle Touchpoints Data — Full",
             "status": "Succeeded" if full_ready and success else "Ready for exact preview and approval" if full_ready else "Blocked — readiness not confirmed"},
            {"key": "daily", "name": "Schedule Aggregate Oracle Touchpoints Data — Daily Incremental",
             "status": "Schedule configured and verified" if full_ready and schedule_success else "Ready for exact schedule preview and approval" if full_ready and success else "Blocked — awaiting current configuration readiness and verified Full success"},
        ],
        "configuration_resolved": configuration_ready,
        "full_ready_for_preview": full_ready,
        "daily_ready_for_preview": full_ready and success,
        "execution_authorized": False,
        "remaining_checks": ["Inspect referenced evidence", "Verify Run Book task bindings and synchronization", "Run owning skill preflight", "Obtain exact operation approval"],
    }
    result["scope"] = scope
    result["tasks"] = [row for key in selected for row in result["tasks"] if row["key"] == key]
    result["standalone_ready_for_preview"] = not implementation and "full" in selected
    if not implementation:
        result["daily_ready_for_preview"] = "daily" in selected and success
        for row in result["tasks"]:
            if row["key"] == "full":
                row["name"] = "Aggregate Oracle Touchpoints Data"
                row["status"] = "Succeeded" if success else "Pending owning ESS preflight and exact approval"
            elif row["key"] == "daily":
                row["status"] = "Schedule configured and verified" if schedule_success else "Ready for schedule preflight" if success else "Blocked — verified Full success required"
    session = state.get("session", {})
    if not isinstance(session, dict):
        raise ValueError("session must be an object")
    result["publish_overview"] = implementation and session.get("overview_shown") is not True
    return enrich_plan(result, state, attested)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Sanitized workflow state JSON")
    parser.add_argument("--dry-run", action="store_true", required=True, help="Required: emit plan only; never write or submit")
    args = parser.parse_args()
    try:
        result = evaluate(json.loads(args.input.read_text(encoding="utf-8")))
    except (OSError, ValueError) as error:
        # Never echo input JSON or configuration values in diagnostics.
        message = "Cannot read or parse workflow input" if isinstance(error, (OSError, json.JSONDecodeError)) else str(error)
        print(json.dumps({"status": "blocked", "failure_class": "input_validation", "message": message}))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Deterministic Touchpoints plan/provisioning entry point; no external I/O.

Consumes an allow-listed core.runbook list-tasks snapshot and explicit bindings.
Emits core add-task inputs, never invented catalog codes or an ESS authorization.
The skill dispatches those operations through core.runbook with its approvals.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from touchpoints_workflow import CONTEXT, evaluate, text, timestamp
from touchpoints_task_plan import execution_checkpoints, dependent_tasks
from touchpoints_feedback_profiles import KEY as FEEDBACK_PROFILES


KEYS = ("profiles", "checkins", "feedback", "surveys", "nudges", "readiness", "full", "daily")
STATUS = {"open": {"INI", "INP", "RFR", "DEP"}, "completed": {"COM"}, "not-applicable": {"REJ"}}


def identifier(value):
    return isinstance(value, str) and value.isdecimal() and int(value) > 0


def sequence_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError("Sequence must be a positive integer")
    if isinstance(value, str) and not value.isdecimal():
        raise ValueError("Sequence must be a positive integer")
    number = int(value)
    if number <= 0:
        raise ValueError("Sequence must be a positive integer")
    return number


def propose_sequences(rows, items, bindings):
    """Preserve anchors when gaps permit; otherwise propose bound-task repairs.

    All values are review proposals, never authorization. Unrelated rows retain
    their positions. Repairs precede additions and require a refreshed snapshot.
    """
    # The dependency-ordered plan is authoritative, including owner prerequisites.
    occupied = {sequence_number(item.get("Sequence")) for item in items}
    assigned, previous = {}, 0
    for row in rows:
        key = row["key"]
        if key in bindings:
            value = sequence_number(row["runbook_sequence"])
            if value <= previous:
                break
        else:
            value = previous + 1
            while value in occupied:
                value += 1
        assigned[key] = value
        previous = value
    else:
        return assigned, []

    # No safe gap (or existing order is wrong). Use unused positions after all
    # existing tasks so each proposed PATCH also avoids transient collisions.
    start = max(occupied, default=0)
    assigned = {row["key"]: start + 10 * (i + 1) for i, row in enumerate(rows)}
    repairs = []
    for row in rows:
        key = row["key"]
        if key in bindings:
            binding = bindings[key]
            repairs.append({"key": key, "operation": "update-task",
                            "parent_id": binding["parent_id"], "task_id": binding["task_id"],
                            "name": binding["name"], "current_sequence": row["runbook_sequence"],
                            "input": {"sequence": assigned[key]}})
    return assigned, repairs


def build(state, snapshot=None):
    """Build selected scope and fail closed on incomplete/ambiguous provisioning.

    Missing bindings produce proposals, never writes. An in-flight or uncertain
    operation suppresses all proposals until read-only reconciliation resolves it.
    A bound row missing from a fresh snapshot is NOT automatically recreated.
    """
    plan = evaluate(state)
    requirements = state.get("task_requirements", {})
    allowed = set(KEYS) | set(dependent_tasks(state)) | {FEEDBACK_PROFILES}
    if not isinstance(requirements, dict) or set(requirements) - allowed:
        raise ValueError("task_requirements must use selected baseline or owner prerequisite keys")
    runbook = state.get("runbook", {})
    if not isinstance(runbook, dict):
        raise ValueError("runbook must be an object")
    bindings = runbook.get("bindings", {})
    if not isinstance(bindings, dict) or set(bindings) - allowed:
        raise ValueError("unsupported Run Book bindings")
    blockers, additions, seen = [], [], set()
    journey = runbook.get("journey_id")
    active = runbook.get("status") == "active" and identifier(journey)
    verified = bool(
        active and isinstance(snapshot, dict)
        and all(snapshot.get(k) == state[k] for k in CONTEXT)
        and snapshot.get("journey_id") == journey
        and snapshot.get("complete") is True
        and timestamp(snapshot.get("captured_at"))
    )
    items = snapshot.get("items", []) if verified else []
    if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
        raise ValueError("snapshot items must be objects")
    if not verified:
        blockers.append("A complete current-target core.runbook task snapshot is required")
    pending = state.get("pending_operation")
    if pending:
        blockers.append("Reconcile pending/unknown operation read-only; do not replay writes")
    for row in plan["tasks"]:
        key = row["key"]
        if key == FEEDBACK_PROFILES and key in requirements:
            raise ValueError("Mandatory Feedback profile requirements cannot be overridden")
        row["requirements"] = requirements.get(key, row.get("requirements", {}))
        binding = bindings.get(key)
        row["runbook_binding_status"] = "missing"
        if binding is None:
            if key == "full":
                blockers.append("Bind Full to the canonical mapped ESS task; never add a manual substitute")
            elif verified and any(item.get("Name") == row["name"] for item in items):
                blockers.append(f"{key}: matching name exists; reconcile identity/scope before binding")
            elif verified:
                additions.append({"key": key, "operation": "add-task", "journey_id": journey,
                                  "input": {"name": row["name"]}})
            continue
        if not isinstance(binding, dict):
            raise ValueError("each binding must be an object")
        task_id, parent_id = binding.get("task_id"), binding.get("parent_id")
        if not identifier(task_id) or not identifier(parent_id) or not text(binding.get("name")):
            blockers.append(f"{key}: invalid task binding")
            continue
        if task_id in seen:
            blockers.append(f"{key}: a task cannot satisfy multiple planned rows")
        seen.add(task_id)
        matches = [item for item in items if str(item.get("WorkerJourneyTaskId")) == task_id
                   and str(item.get("ParentWorkerJourneyId")) == parent_id
                   and item.get("Name") == binding["name"]]
        if not verified or len(matches) != 1:
            blockers.append(f"{key}: binding absent, changed or ambiguous in current snapshot")
            continue
        actual = matches[0]
        expected = row.get("proposed_runbook_status", "open")
        # Full and daily terminal evidence is governed by the owning ESS workflow.
        if key in ("full", "daily"):
            allowed = {"INI", "INP", "RFR", "DEP", "COM"}
        elif key == "readiness" and plan["full_ready_for_preview"]:
            allowed = {"COM"}
        else:
            allowed = STATUS[expected]
        if actual.get("Status") not in allowed:
            blockers.append(f"{key}: remote status does not match the recorded disposition")
        row["runbook_binding_status"] = "verified"
        row["runbook_task_name"] = binding["name"]
        row["runbook_sequence"] = actual.get("Sequence")
    repairs = []
    if verified and not blockers and not pending:
        try:
            sequences, repairs = propose_sequences(plan["tasks"], items, bindings)
            for row in plan["tasks"]:
                row["proposed_sequence"] = sequences[row["key"]]
            for addition in additions:
                addition["input"]["sequence"] = sequences[addition["key"]]
            if repairs:
                blockers.append("Approve sequence repairs, apply once, then refresh before additions")
        except ValueError:
            blockers.append("Invalid snapshot sequence; reconcile before proposing writes")
    all_bound = all(row["runbook_binding_status"] == "verified" for row in plan["tasks"])
    if all_bound:
        sequences = {row["key"]: row.get("runbook_sequence") for row in plan["tasks"]}
        try:
            sequences = {key: int(value) for key, value in sequences.items() if not isinstance(value, bool)}
            ordered = len(sequences) == len(plan["tasks"]) and min(sequences.values()) > 0
            positions = [sequences[row["key"]] for row in plan["tasks"]]
            ordered = ordered and all(a < b for a, b in zip(positions, positions[1:]))
        except (ValueError, TypeError):
            ordered = False
        if not ordered:
            blockers.append("Authorize sequence repair: configuration before readiness before Full before daily")
    complete = all_bound and not blockers and not additions
    if pending or blockers:
        additions = []  # Fail closed: do not execute a partial ambiguous batch.
    plan.update({
        "kind": "touchpoints_runbook_configuration_plan", "schema_version": "2.0",
        "runbook": {"journey_id": journey, "bindings": bindings},
        "provisioning_status": "provisioned" if complete else "blocked" if blockers else "additions_pending",
        "provisioning_blockers": blockers, "runbook_complete": complete,
        "manual_additions": additions,
        "sequence_updates": repairs,
        "presentation_status": "Complete provisioning" if complete else "Partial provisioning",
        "full_ready_for_preview": complete and plan["full_ready_for_preview"],
        "daily_ready_for_preview": complete and plan["daily_ready_for_preview"],
        "standalone_ready_for_preview": complete and plan["standalone_ready_for_preview"],
        "execution_authorized": False,
    })
    for row in plan["tasks"]:
        if row["key"] in ("full", "daily") and not complete:
            row["status"] = "Blocked — Run Book provisioning or synchronization incomplete"
    plan["execution"] = execution_checkpoints(plan, state)
    plan["context_sync_required"] = [
        {"key": row["key"], "catalog_identity": row.get("catalog_identity"),
         "sequence": row.get("runbook_sequence"), "binding": bindings.get(row["key"])}
        for row in plan["tasks"] if row["execution_route"] == "data-loader"
        or row["execution_route"] == "ess" and row.get("catalog_identity")
    ]
    return plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--tasks", type=Path, help="Current allow-listed core task snapshot")
    parser.add_argument("--dry-run", required=True, action="store_true")
    parser.add_argument("--require-ready", choices=("full", "daily", "standalone"))
    args = parser.parse_args()
    try:
        result = build(json.loads(args.input.read_text()),
                       json.loads(args.tasks.read_text()) if args.tasks else None)
    except (OSError, ValueError, TypeError, KeyError):
        print(json.dumps({"status": "blocked", "failure_class": "input_validation",
                          "message": "Invalid workflow state or task snapshot; inspect local inputs"}))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if args.require_ready and not result[f"{args.require_ready}_ready_for_preview"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

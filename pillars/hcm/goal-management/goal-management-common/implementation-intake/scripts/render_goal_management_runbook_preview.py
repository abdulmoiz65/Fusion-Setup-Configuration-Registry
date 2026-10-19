#!/usr/bin/env python3
"""Render and validate a deterministic Goal Management local Run Book preview."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


class GoalManagementRunbookPreviewError(ValueError):
    """The local planning input cannot produce a safe Run Book preview."""


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GoalManagementRunbookPreviewError(f"{label} must be non-empty text")
    return " ".join(value.split())


def _items(value: Any, label: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise GoalManagementRunbookPreviewError(f"{label} must be a list")
    return [_text(item, f"{label} item") for item in value]


def _cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br>")


def _operation_activities(value: Any, task_name: str) -> list[str]:
    if value is None:
        return [task_name]
    if not isinstance(value, list):
        raise GoalManagementRunbookPreviewError("task operations must be a list")
    activities = []
    seen = set()
    for index, operation in enumerate(value, start=1):
        if not isinstance(operation, Mapping):
            raise GoalManagementRunbookPreviewError(f"task operation {index} must be an object")
        sequence = operation.get("sequence")
        if type(sequence) is not int or sequence < 1 or sequence in seen:
            raise GoalManagementRunbookPreviewError("operation sequence must be a unique positive integer")
        seen.add(sequence)
        activities.append((sequence, _text(operation.get("activity", operation.get("operation")), f"task operation {index}")))
    return [activity for _, activity in sorted(activities)] or [task_name]


def _canonical_plan(plan: Mapping[str, Any]) -> dict[str, Any]:
    """Return the order-stable review content bound to Run Book approval."""
    delta = plan.get("configuration_delta", {})
    tasks = []
    for task in sorted(plan["tasks"], key=lambda row: row["sequence"]):
        tasks.append(
            {
                "sequence": task["sequence"],
                "task_code": task["task_code"],
                "task_name": task["task_name"],
                "offering": task["offering"],
                "functional_area": task["functional_area"],
                "skill_path": task["skill_path"],
                "operations": _operation_activities(task.get("operations"), task["task_name"]),
                "approval_gate": task.get(
                    "approval_gate",
                    "Complete read-only preflight; obtain approval before every external state change",
                ),
                "exit_criterion": task.get(
                    "exit_criterion", "Terminal result and fresh target-state verification"
                ),
            }
        )
    return {
        "configuration_delta": {
            key: list(delta.get(key) or [])
            for key in ("proposed_objects", "confirmed_decisions", "unresolved_items", "out_of_scope")
        },
        "tasks": tasks,
    }


def planning_fingerprint(plan: Mapping[str, Any]) -> str:
    """Fingerprint the exact normalized plan shown for approval."""
    canonical = json.dumps(
        _canonical_plan(plan), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def render_preview(plan: Mapping[str, Any], *, resolved_context: Mapping[str, Any] | None = None) -> str:
    """Return CommonMark containing one table row per exact catalog task."""

    if not isinstance(plan, Mapping):
        raise GoalManagementRunbookPreviewError("plan must be an object")
    tasks = plan.get("tasks")
    if not isinstance(tasks, Sequence) or isinstance(tasks, (str, bytes)) or not tasks:
        raise GoalManagementRunbookPreviewError("plan must contain one or more tasks")
    # Compare with the separately loaded, persisted shared-resolver handoff.
    # This validator consumes order; it must never invent an implementation order.
    if not isinstance(resolved_context, Mapping) or not resolved_context.get("tasks"):
        raise GoalManagementRunbookPreviewError("persisted resolved task context is required")
    def snapshot(rows):
        result = {}
        for row in rows:
            if not isinstance(row, Mapping):
                raise GoalManagementRunbookPreviewError("each resolved task must be an object")
            identity = tuple(_text(row.get(key), key) for key in
                             ("task_code", "task_name", "offering", "functional_area"))
            if identity in result:
                raise GoalManagementRunbookPreviewError("duplicate stable task identity")
            if row.get("sequence_source") == "LEXICOGRAPHIC_PATH" or row.get("skill_selection", {}).get("selected_by") == "LEXICOGRAPHIC_PATH":
                raise GoalManagementRunbookPreviewError("path-only resolution is not authoritative")
            result[identity] = (row.get("sequence"), _text(row.get("skill_path"), "skill_path"),
                                _operation_activities(row.get("operations"), row["task_name"]))
        return result
    if snapshot(tasks) != snapshot(resolved_context["tasks"]):
        raise GoalManagementRunbookPreviewError("preview differs from persisted resolved task context; regenerate before approval")

    delta = plan.get("configuration_delta", {})
    if not isinstance(delta, Mapping):
        raise GoalManagementRunbookPreviewError("configuration_delta must be an object")

    fingerprint = planning_fingerprint(plan)
    lines = ["## Configuration-plan delta", "", f"- Plan fingerprint: `{fingerprint}`"]
    for key, label in (
        ("proposed_objects", "Proposed objects"),
        ("confirmed_decisions", "Confirmed decisions"),
        ("unresolved_items", "Unresolved items"),
        ("out_of_scope", "Out of scope"),
    ):
        values = _items(delta.get(key), f"configuration_delta.{key}")
        lines.append(f"- {label}: {_cell('; '.join(values) if values else 'None')}")

    lines.extend(
        [
            "",
            "## Local Run Book preview",
            "",
            "| Task | Catalog setup task | Owner route | Planned operations | Preflight / approval gate | Exit criterion |",
            "| ---: | --- | --- | --- | --- | --- |",
        ]
    )

    seen_sequences: set[int] = set()
    seen_identities: set[tuple[str, str, str, str]] = set()
    ordered_tasks = []
    for task in tasks:
        if not isinstance(task, Mapping):
            raise GoalManagementRunbookPreviewError("each task must be an object")
        sequence = task.get("sequence")
        if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 1:
            raise GoalManagementRunbookPreviewError("task sequence must be a positive integer")
        if sequence in seen_sequences:
            raise GoalManagementRunbookPreviewError("task sequence values must be unique")
        seen_sequences.add(sequence)
        task_name = _text(task.get("task_name"), "task_name")
        task_code = _text(task.get("task_code"), "task_code")
        offering = _text(task.get("offering"), "offering")
        functional_area = _text(task.get("functional_area"), "functional_area")
        identity = (task_code.casefold(), task_name.casefold(), offering.casefold(), functional_area.casefold())
        if identity in seen_identities:
            raise GoalManagementRunbookPreviewError("duplicate stable task identity")
        seen_identities.add(identity)
        ordered_tasks.append((sequence, task, task_name, task_code))

    for sequence, task, task_name, task_code in sorted(ordered_tasks):
        route = _text(task.get("skill_path"), "skill_path")
        activities = _operation_activities(task.get("operations"), task_name)
        gate = _text(
            task.get(
                "approval_gate",
                "Complete read-only preflight; obtain approval before every external state change",
            ),
            "approval_gate",
        )
        exit_criterion = _text(
            task.get("exit_criterion", "Terminal result and fresh target-state verification"),
            "exit_criterion",
        )
        activity_text = "<br>".join(f"{index}. {_cell(activity)}" for index, activity in enumerate(activities, start=1))
        lines.append(
            f"| {sequence} | {_cell(task_name)} (`{_cell(task_code)}`) | `{_cell(route)}` | "
            f"{activity_text} | {_cell(gate)} | {_cell(exit_criterion)} |"
        )

    lines.extend(
        [
            "",
            "> This is a local planning preview. It does not authorize Oracle Fusion Run Book creation or any configuration write.",
            "> Approval of Run Book creation must bind this exact plan fingerprint. Any plan change invalidates that approval.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True, help="Goal Management local planning JSON")
    parser.add_argument("--resolved-context", type=Path, required=True, help="Persisted task context reconciled with shared setup_task_sequence")
    parser.add_argument("--output", type=Path, help="Markdown output; stdout when omitted")
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
        context = json.loads(args.resolved_context.read_text(encoding="utf-8"))
        output = render_preview(plan, resolved_context=context)
    except (OSError, json.JSONDecodeError, GoalManagementRunbookPreviewError) as exc:
        parser.error(str(exc))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Plan and guard Goal Management implementation continuation.

The guided recommendation helper is intentionally lightweight.  The controlled
task resolver is the fail-closed boundary for a confirmed source-pack queue: it
uses the supplied resolved task list and never assumes a fixed number of tasks
or hard-coded Goal Management task names.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable, Optional, Sequence


class GuidedPlanError(ValueError):
    """The guided implementation state is invalid."""


_OBJECTS = (
    "performance_library_goal",
    "development_library_goal",
    "review_period",
    "goal_plan",
)

_DEPENDENCY_OPTIONS = (
    "profile_options",
    "lookups",
    "value_sets",
    "descriptive_flexfields",
    "security",
    "career_development_features",
    "performance_document_type",
)

_COMPLETED_STATUSES = {"completed", "complete", "com"}
_NOT_APPLICABLE_STATUSES = {
    "not applicable",
    "not_applicable",
    "not-applicable",
    "n/a",
}


def _nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GuidedPlanError(f"{label} must be a non-empty string")
    return " ".join(value.split())


def _positive_sequence(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise GuidedPlanError("every controlled task sequence must be a positive integer")
    return value


def _task_identity(task: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        _nonempty_string(task.get("task_code"), "task_code"),
        _nonempty_string(task.get("offering"), "offering"),
        _nonempty_string(task.get("functional_area"), "functional_area"),
        _nonempty_string(task.get("skill_path"), "skill_path"),
    )


def _normalized_status(task: dict[str, Any]) -> str:
    value = task.get("status", "not started")
    if not isinstance(value, str) or not value.strip():
        raise GuidedPlanError("every controlled task must have a non-empty status")
    return " ".join(value.casefold().replace("_", " ").split())


def _control_fingerprint(payload: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def resolve_controlled_next_task(
    tasks: Sequence[dict[str, Any]],
    *,
    requested_task: dict[str, Any] | None,
    plan_status: str,
    configuration_plan_fingerprint: str,
    approved_plan_fingerprint: str,
    runbook_created: bool,
    dashboard_presented: bool,
    stop_requested: bool = False,
) -> dict[str, Any]:
    """Return the sole task that a Goal Management workflow may execute.

    ``tasks`` is the resolved task list for the current input.  It may contain
    one, two, or any other positive number of tasks.  Completion and explicit
    Not Applicable evidence are the only conditions that advance the queue.
    User approval of a later payload never changes task order.
    """
    if stop_requested:
        return {
            "status": "stopped",
            "allowed": False,
            "code": "GOAL_MANAGEMENT_RUN_STOPPED",
            "next_task": None,
            "action": "Preserve evidence and require a fresh intake/control check before any resume.",
        }
    if not isinstance(tasks, Sequence) or isinstance(tasks, (str, bytes)) or not tasks:
        raise GuidedPlanError("controlled execution requires at least one resolved task")
    if not isinstance(plan_status, str) or plan_status.casefold().strip() != "approved":
        return {
            "status": "blocked",
            "allowed": False,
            "code": "PLAN_NOT_APPROVED",
            "next_task": None,
            "action": "Refresh, show, and approve the configuration plan and local Run Book preview.",
        }
    if (
        not isinstance(configuration_plan_fingerprint, str)
        or not configuration_plan_fingerprint
        or configuration_plan_fingerprint != approved_plan_fingerprint
    ):
        return {
            "status": "blocked",
            "allowed": False,
            "code": "PLAN_FINGERPRINT_MISMATCH",
            "next_task": None,
            "action": "Regenerate the changed plan and obtain fresh approval.",
        }
    if runbook_created is not True:
        return {
            "status": "blocked",
            "allowed": False,
            "code": "RUNBOOK_NOT_CREATED",
            "next_task": None,
            "action": "Preview and approve creation of the Oracle Fusion Run Book.",
        }
    if dashboard_presented is not True:
        return {
            "status": "blocked",
            "allowed": False,
            "code": "RUNBOOK_DASHBOARD_NOT_PRESENTED",
            "next_task": None,
            "action": "Present the complete sanitized Run Book dashboard before task execution.",
        }

    normalized: list[dict[str, Any]] = []
    sequences: set[int] = set()
    identities: set[tuple[str, str, str, str]] = set()
    for source in tasks:
        if not isinstance(source, dict):
            raise GuidedPlanError("every controlled task must be an object")
        task = dict(source)
        sequence = _positive_sequence(task.get("sequence"))
        identity = _task_identity(task)
        if sequence in sequences:
            raise GuidedPlanError("controlled task sequences must be unique")
        if identity in identities:
            raise GuidedPlanError("controlled task identities must be unique")
        sequences.add(sequence)
        identities.add(identity)
        task["sequence"] = sequence
        task["status"] = _normalized_status(task)
        normalized.append(task)
    normalized.sort(key=lambda task: task["sequence"])

    pending = [
        task
        for task in normalized
        if task["status"] not in _COMPLETED_STATUSES | _NOT_APPLICABLE_STATUSES
    ]
    if not pending:
        return {
            "status": "complete",
            "allowed": False,
            "code": "ALL_APPLICABLE_TASKS_COMPLETE",
            "next_task": None,
        }

    next_task = pending[0]
    if requested_task is None:
        return {
            "status": "ready_for_preview",
            "allowed": False,
            "code": "NEXT_TASK_PREVIEW_REQUIRED",
            "next_task": next_task,
        }
    if not isinstance(requested_task, dict):
        raise GuidedPlanError("requested_task must be an exact task identity object")
    requested_sequence = _positive_sequence(requested_task.get("sequence"))
    requested_identity = _task_identity(requested_task)
    if requested_sequence != next_task["sequence"] or requested_identity != _task_identity(next_task):
        return {
            "status": "blocked",
            "allowed": False,
            "code": "EARLIER_TASK_INCOMPLETE",
            "next_task": next_task,
            "requested_sequence": requested_sequence,
            "action": "Reconcile and complete the earliest applicable Run Book task first.",
        }

    control = {
        "plan_fingerprint": configuration_plan_fingerprint,
        "task": {
            "sequence": next_task["sequence"],
            "task_code": next_task["task_code"],
            "offering": next_task["offering"],
            "functional_area": next_task["functional_area"],
            "skill_path": next_task["skill_path"],
        },
    }
    return {
        "status": "allowed",
        "allowed": True,
        "code": "CURRENT_TASK_AUTHORIZED",
        "next_task": next_task,
        "execution_control": control,
        "execution_control_fingerprint": _control_fingerprint(control),
    }


def _normalize_objects(values: Iterable[str], label: str) -> list[str]:
    if isinstance(values, (str, bytes)):
        raise GuidedPlanError(f"{label} must be a sequence of object identifiers")
    result = []
    for value in values:
        if value not in _OBJECTS:
            raise GuidedPlanError(f"{label} contains unsupported object {value!r}")
        if value in result:
            raise GuidedPlanError(f"{label} contains duplicate object {value!r}")
        result.append(value)
    return result


def plan_guided_next_actions(
    *,
    guided_mode: bool,
    completed: Iterable[str] = (),
    declined: Iterable[str] = (),
    explicit_order: Optional[Sequence[str]] = None,
    requested_object: Optional[str] = None,
    regular_goal_plan: bool = False,
) -> dict[str, Any]:
    """Return optional continuation actions without changing explicit source order.

    Call only for an open or insufficiently specified implementation request.
    A fully scoped source pack owns its own task order and does not enter guided
    mode. A regular Goal Plan still requires a Review Period before its preview.
    """
    if not guided_mode:
        return {"mode": "not_guided", "next_actions": [], "dependency_options": []}
    done = _normalize_objects(completed, "completed")
    skipped = _normalize_objects(declined, "declined")
    if set(done) & set(skipped):
        raise GuidedPlanError("completed and declined objects must not overlap")
    if requested_object is not None and requested_object not in _OBJECTS:
        raise GuidedPlanError("requested_object is unsupported")

    if explicit_order is not None:
        order = _normalize_objects(explicit_order, "explicit_order")
        if set(order) != set(_OBJECTS):
            raise GuidedPlanError("explicit_order must include each supported Goal Management object once")
        basis = "explicit_source_order"
    else:
        order = list(_OBJECTS)
        basis = "recommended_sequence"

    dependency_blockers = []
    if requested_object == "goal_plan" and regular_goal_plan and "review_period" not in done:
        dependency_blockers.append(
            {
                "object": "goal_plan",
                "required_before_preview": "review_period",
                "reason": "A regular Goal Plan requires one active Review Period.",
            }
        )
    next_actions = [item for item in order if item not in done and item not in skipped]
    return {
        "mode": "guided",
        "selection_basis": basis,
        "next_actions": next_actions,
        "dependency_blockers": dependency_blockers,
        "dependency_options": list(_DEPENDENCY_OPTIONS),
        "choices": ["continue", "skip", "not_now"],
    }

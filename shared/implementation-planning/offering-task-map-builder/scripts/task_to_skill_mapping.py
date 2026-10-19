"""Build implementation task-to-skill mappings before Oracle Run Book planning."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from task_context import TaskContextError, build_setup_task_plan


MAPPING_SCHEMA_VERSION = "1.0"


def build_task_to_skill_mapping(
    repository_root: Path, source_plan: dict[str, Any]
) -> dict[str, Any]:
    """Resolve every selected task to its catalog identity and pillar skill."""

    mapping = build_setup_task_plan(repository_root, source_plan)
    return {"schema_version": MAPPING_SCHEMA_VERSION, **mapping}


def build_implementation_project_task_list(
    task_to_skill_mapping: dict[str, Any], task_notes_html: list[Any]
) -> dict[str, Any]:
    """Create a complete project task list, including manual unmatched tasks."""

    if task_to_skill_mapping.get("schema_version") != MAPPING_SCHEMA_VERSION:
        raise TaskContextError("Task-to-skill mapping has an unsupported schema.")
    tasks = task_to_skill_mapping.get("tasks")
    offering = task_to_skill_mapping.get("offering")
    functional_area = task_to_skill_mapping.get("functional_area")
    if not isinstance(tasks, list) or not tasks:
        raise TaskContextError("Task-to-skill mapping must contain a non-empty tasks array.")
    if not isinstance(task_notes_html, list) or len(task_notes_html) != len(tasks):
        raise TaskContextError("Task-to-skill mapping and task Notes must contain the same number of tasks.")
    if not isinstance(offering, str) or not offering.strip() or not isinstance(functional_area, str) or not functional_area.strip():
        raise TaskContextError("Task-to-skill mapping must contain offering and functional area.")

    task_list = []
    for task in tasks:
        if not isinstance(task, dict):
            raise TaskContextError("Task-to-skill mapping contains an invalid task.")
        name, sequence = task.get("task_name"), task.get("sequence")
        if not isinstance(name, str) or not name.strip() or isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 1:
            raise TaskContextError("Task-to-skill mapping contains an invalid task name or sequence.")
        entry = {"name": " ".join(name.split()), "sequence": sequence}
        if task.get("execution_mode") == "manual":
            entry["matchStatus"] = "unmatched"
            entry["executionMode"] = "manual"
            entry["matchReason"] = task.get("match_reason", "No pillar task-level skill was matched.")
        else:
            entry["matchStatus"] = "matched"
            entry["taskCode"] = task.get("task_code")
            entry["skillPath"] = task.get("skill_path")
        task_list.append(entry)
    return {
        "schema_version": MAPPING_SCHEMA_VERSION,
        "offering": offering.strip(),
        "functional_area": functional_area.strip(),
        "tasks": task_list,
        "taskNotesHtml": task_notes_html,
    }

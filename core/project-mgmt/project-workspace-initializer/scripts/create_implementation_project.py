"""Deprecated compatibility helpers; use create_project_runbook.py for new work."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def build_project_runbook_contract(project_task_list: dict[str, Any], metadata: dict[str, Any], *, functional_area: str) -> tuple[dict[str, Any], dict[str, Any]]:
    source = {task["id"]: task for task in project_task_list["task_list"]}
    tasks = []
    for item in sorted(metadata["tasks"], key=lambda entry: entry["sequence"]):
        details = item.get("task_metadata", {})
        if details.get("execution_route") == "runbook-data-loader":
            tasks.append({"sequence": item["sequence"], "task_name": details.get("task_name"), "task_code": details.get("task_code"), "skill_path": details.get("skill_path")})
        else:
            task = source[item["project_task_id"]]["task"]
            tasks.append({"sequence": item["sequence"], "task_name": task, "execution_mode": "manual", "match_reason": "No task-level pillar skill was mapped for this project task."})
    for task in tasks:
        if task.get("execution_mode") != "manual" and not all(isinstance(task.get(key), str) and task[key] for key in ("task_name", "task_code", "skill_path")):
            raise ValueError("incomplete Run Book metadata")
    setup = {"schema_version": "1.0", "offering": "FSCR Implementation", "functional_area": functional_area, "tasks": tasks}
    plan = {"plan": {"offering": "FSCR Implementation", "functional_area": functional_area, "tasks": [{"name": task["task_name"], "sequence": task["sequence"]} for task in tasks]}, "taskNotesHtml": ["<p>Implementation project task.</p>" for _ in tasks]}
    return setup, plan


def runbook_creation_status(project_root: Path) -> str:
    response = project_root / "state" / "runbook" / "current" / "create-runbook-response.json"
    dashboard = project_root / "artifacts" / "shared" / "runbook" / "current" / "runbook-dashboard.html"
    if response.is_file() and dashboard.is_file():
        return "Run Book created. No Run Book tasks have been executed and no Data Loader uploads or Fusion setup changes have occurred."
    return "Run Book plan and task context were persisted; no Run Book has been created."

"""Optional local reference helpers for setup task CSV export support."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fusion_skill_paths import REPO_ROOT


DEFAULT_REFERENCE_PATH = Path("knowledge") / "setup-task-catalog" / "effective" / "setupTasksAll.json"
REFERENCE_CANDIDATES = (
    REPO_ROOT / DEFAULT_REFERENCE_PATH,
    REPO_ROOT / "setupTasksAll.json",
    REPO_ROOT / "references" / "fsmReferences" / "setupTasksAll.json",
)


def csv_export_import_flag(task: dict[str, Any] | None) -> str:
    if not task:
        return ""
    for key in ("CSVExportImportSupportedFlag", "ExportImportSupportedFlag"):
        value = task.get(key)
        if value is not None:
            return str(value)
    return ""


def load_setup_tasks(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in ("items", "tasks", "setupTasks"):
            items = data.get(key)
            if isinstance(items, list):
                return [item for item in items if isinstance(item, dict)]
    raise RuntimeError(f"Could not find setup task entries in {path}")


def find_reference_path() -> Path | None:
    for candidate in REFERENCE_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


def text_value(item: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = item.get(key)
        if value is not None:
            return str(value)
    return ""


def find_task_matches(
    tasks: list[dict[str, Any]],
    *,
    task_code: str | None = None,
    task_name: str | None = None,
    allow_contains: bool = True,
) -> list[dict[str, Any]]:
    task_code_folded = task_code.casefold() if task_code else None
    task_name_folded = task_name.casefold() if task_name else None
    matches: list[dict[str, Any]] = []

    for task in tasks:
        code = text_value(task, "TaskCode", "task_code", "code").casefold()
        name = text_value(task, "TaskName", "task_name", "name").casefold()

        code_matches = task_code_folded is None or (
            code == task_code_folded or (allow_contains and task_code_folded in code)
        )
        name_matches = task_name_folded is None or (
            name == task_name_folded or (allow_contains and task_name_folded in name)
        )
        if code_matches and name_matches:
            matches.append(task)

    return matches

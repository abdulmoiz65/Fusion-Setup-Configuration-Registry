"""Read-only project Run Book eligibility checks for task execution."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
TASK_CONTEXT = Path("artifacts/shared/runbook/current/task-context.json")


def server_identity(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Run Book server binding is missing.")
    parsed = urlsplit(value.strip())
    if (parsed.scheme not in {"http", "https"} or not parsed.hostname
            or parsed.username or parsed.password or parsed.query or parsed.fragment):
        raise ValueError("Run Book server binding is invalid.")
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path.rstrip("/"), "", ""))


def require_project_runbook(project_root: Path) -> dict[str, str]:
    """Return a stable binding only for a locally recorded, eligible Run Book."""
    root = project_root.resolve(strict=True)
    if root.parent != (REPOSITORY_ROOT / "project").resolve() or root.name == "_template":
        raise ValueError("Run Book execution requires a project/<project_id> workspace.")
    try:
        state = json.loads((root / "state/project-state.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise ValueError("Project Run Book state is missing or unreadable.") from error
    control = state.get("runbook_control") if isinstance(state, dict) else None
    if not isinstance(control, dict) or control.get("status") != "active":
        raise ValueError("Task execution requires Run Book status active.")
    reference = control.get("active_runbook_ref")
    if (isinstance(reference, bool) or not isinstance(reference, (int, str))
            or not str(reference).isascii() or not str(reference).isdigit()
            or not 0 < int(reference) <= 9223372036854775807):
        raise ValueError("Project Run Book binding requires a valid active_runbook_ref.")
    return {
        "projectRoot": str(root),
        "workerJourneyId": str(int(reference)),
        "serverUrl": server_identity(control.get("server_url")),
    }


def runbook_from_task_context(path: Path) -> dict[str, str]:
    context = path.resolve(strict=True)
    if len(context.parents) < len(TASK_CONTEXT.parts):
        raise ValueError("Task context must be the project's generated task-context.json.")
    root = context.parents[len(TASK_CONTEXT.parts) - 1]
    if context != root / TASK_CONTEXT:
        raise ValueError("Task context must be the project's generated task-context.json.")
    return require_project_runbook(root)


def require_runbook_binding(binding: Any) -> dict[str, str]:
    if not isinstance(binding, dict) or not isinstance(binding.get("projectRoot"), str):
        raise ValueError("Task preview is missing its Run Book binding; create a fresh preview and approval.")
    current = require_project_runbook(Path(binding["projectRoot"]))
    if binding != current:
        raise ValueError("Project Run Book binding changed; create a fresh preview and approval.")
    return current


def require_approved_runbook(preview: Any, approval: Any) -> dict[str, str]:
    binding = require_runbook_binding(preview.get("runbookBinding") if isinstance(preview, dict) else None)
    if not isinstance(approval, dict) or approval.get("runbookBinding") != binding:
        raise ValueError("Task approval does not match the Run Book binding; approve a fresh preview.")
    return binding

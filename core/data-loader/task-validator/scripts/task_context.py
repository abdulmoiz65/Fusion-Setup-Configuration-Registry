"""Local task context helpers."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any


SCHEMA_VERSION = "1.0"
CATALOG_PATH = Path("knowledge/setup-task-catalog/release/setupTasksAll.json")
POLICY_PATH = Path("core/data-loader/task-validator/references/task-context-policy.json")


class TaskContextError(ValueError):
    """The local task context is invalid or unsafe."""


def _normalized_name(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TaskContextError("Task name must be non-empty text.")
    return " ".join(value.split()).casefold()


def _positive_sequence(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise TaskContextError("Task sequence must be a positive integer.")
    return value


def _read_json_object(path: Path, description: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise TaskContextError(f"{description} could not be read: {path}") from error
    except json.JSONDecodeError as error:
        raise TaskContextError(f"{description} is not valid JSON: {error.msg}.") from error
    if not isinstance(value, dict):
        raise TaskContextError(f"{description} must be a JSON object.")
    return value


def _manifest_value(manifest: Path, field: str) -> str | None:
    match = re.search(rf"^{re.escape(field)}:\s*[\"']?([^\"'#\r\n]+)", manifest.read_text(encoding="utf-8"), re.MULTILINE)
    return match.group(1).strip() if match else None


def _task_context_policy(repository_root: Path) -> dict[str, Any]:
    policy = _read_json_object(repository_root / POLICY_PATH, "Task-context policy")
    if not isinstance(policy.get("include_missing_skill"), bool):
        raise TaskContextError("Task-context policy include_missing_skill must be a boolean.")
    if policy.get("multiple_skill_policy") not in {"SELECT_BY_PRIORITY", "SELECT_LEXICOGRAPHIC_PATH"}:
        raise TaskContextError("Task-context policy has an unsupported multiple_skill_policy.")
    order = policy.get("priority_order")
    allowed = {"EXACT_TASK_CODE_AND_NAME", "PROJECT_OFFERING_OR_PILLAR", "LEXICOGRAPHIC_PATH"}
    if not isinstance(order, list) or not order or any(value not in allowed for value in order):
        raise TaskContextError("Task-context policy has an invalid priority_order.")
    return policy


def _catalog_task_code(repository_root: Path, task_name: str) -> str:
    catalog = _read_json_object(repository_root / CATALOG_PATH, "Setup-task catalog")
    items = catalog.get("items")
    matches = [item for item in items if isinstance(item, dict) and _normalized_name(item.get("TaskName")) == _normalized_name(task_name)] if isinstance(items, list) else []
    if len(matches) != 1:
        raise TaskContextError(f"Task {task_name!r} must match exactly one setup-task catalog entry; found {len(matches)}.")
    task_code = matches[0].get("TaskCode")
    if not isinstance(task_code, str) or not task_code.strip():
        raise TaskContextError(f"Catalog task {task_name!r} has no task code.")
    return task_code.strip()


def _selection_context(repository_root: Path, selected_path: str, *, offering: Any, functional_area: Any, canonical_reuse: bool) -> dict[str, Any]:
    project_context = {
        "offering": offering.strip() if isinstance(offering, str) and offering.strip() else None,
        "functional_area": functional_area.strip() if isinstance(functional_area, str) and functional_area.strip() else None,
    }
    artifact = repository_root / selected_path
    skill_context = {
        "offering": _manifest_value(artifact, "offering"),
        "functional_area": _manifest_value(artifact, "functional_area"),
    }
    comparable = all(project_context.values()) and all(skill_context.values())
    same_context = comparable and all(_normalized_name(project_context[key]) == _normalized_name(skill_context[key]) for key in project_context)
    relation = "same-context" if same_context else "canonical-task-reuse" if canonical_reuse else "cross-context-fallback"
    result = {"context_relation": relation, "project_context": project_context, "skill_context": skill_context}
    if relation == "canonical-task-reuse":
        result["context_note"] = "The unique task-code-and-name skill is canonical and reusable across Oracle offering and functional-area contexts."
    return result


def _skill_path(repository_root: Path, task_code: str, task_name: str, *, policy: dict[str, Any], offering: Any, functional_area: Any) -> tuple[str | None, dict[str, Any]]:
    matches = []
    for manifest in repository_root.glob("pillars/**/SKILL.md"):
        if _manifest_value(manifest, "task_code") != task_code:
            continue
        manifest_name = _manifest_value(manifest, "task_name")
        if manifest_name is None or _normalized_name(manifest_name) == _normalized_name(task_name):
            matches.append(manifest)
    candidates = sorted(manifest.relative_to(repository_root).as_posix() for manifest in matches)
    if not candidates:
        return None, {"status": "missing", "selected_by": "INCLUDE_MISSING_SKILL", "candidates": [], "context_relation": "missing", "project_context": {"offering": offering, "functional_area": functional_area}, "skill_context": None}
    if len(candidates) == 1:
        return candidates[0], {"status": "selected", "selected_by": "EXACT_TASK_CODE_AND_NAME", "candidates": candidates, **_selection_context(repository_root, candidates[0], offering=offering, functional_area=functional_area, canonical_reuse=True)}
    if policy["multiple_skill_policy"] == "SELECT_LEXICOGRAPHIC_PATH":
        return candidates[0], {"status": "selected", "selected_by": "LEXICOGRAPHIC_PATH", "candidates": candidates, **_selection_context(repository_root, candidates[0], offering=offering, functional_area=functional_area, canonical_reuse=False)}
    scope_tokens = {token.casefold() for token in re.split(r"[^a-z0-9]+", str(offering or "")) if token}
    scoped = [candidate for candidate in candidates if any(token in candidate.casefold() for token in scope_tokens)]
    if len(scoped) == 1:
        return scoped[0], {"status": "selected", "selected_by": "PROJECT_OFFERING_OR_PILLAR", "candidates": candidates, **_selection_context(repository_root, scoped[0], offering=offering, functional_area=functional_area, canonical_reuse=False)}
    return candidates[0], {"status": "selected", "selected_by": "LEXICOGRAPHIC_PATH", "candidates": candidates, **_selection_context(repository_root, candidates[0], offering=offering, functional_area=functional_area, canonical_reuse=False)}


def build_setup_task_plan(repository_root: Path, runbook_plan: dict[str, Any]) -> dict[str, Any]:
    root = repository_root.resolve(strict=True)
    plan = runbook_plan.get("plan")
    tasks = plan.get("tasks") if isinstance(plan, dict) else None
    if not isinstance(tasks, list) or not tasks:
        raise TaskContextError("Run-book plan must contain a non-empty tasks array.")
    context_tasks = []
    policy = _task_context_policy(root)
    identifiers = set()
    for task in tasks:
        if not isinstance(task, dict):
            raise TaskContextError("Every run-book task must be an object.")
        task_name = task.get("name")
        sequence = _positive_sequence(task.get("sequence"))
        identifier = (_normalized_name(task_name), sequence)
        if identifier in identifiers:
            raise TaskContextError("Run-book plan contains duplicate task name and sequence values.")
        identifiers.add(identifier)
        if task.get("execution_mode") == "manual":
            context_tasks.append(
                {
                    "sequence": sequence,
                    "task_name": " ".join(task_name.split()),
                    "execution_mode": "manual",
                    "match_status": "unmatched",
                    "match_reason": "User-designated manual task.",
                }
            )
            continue
        try:
            task_code = _catalog_task_code(root, task_name)
            skill_path, skill_selection = _skill_path(root, task_code, task_name, policy=policy, offering=task.get("offering", plan.get("offering")), functional_area=task.get("functional_area", plan.get("functional_area")))
        except TaskContextError as error:
            context_tasks.append({
                "sequence": sequence,
                "task_name": " ".join(task_name.split()),
                "execution_mode": "manual",
                "match_status": "unmatched",
                "match_reason": str(error),
            })
            continue
        if skill_path is None and not policy["include_missing_skill"]:
            context_tasks.append({"sequence": sequence, "task_name": " ".join(task_name.split()), "execution_mode": "manual", "match_status": "unmatched", "match_reason": "No pillar skill manifest was found and task-context policy excludes missing skills."})
            continue
        context_tasks.append({
            "sequence": sequence,
            "task_name": " ".join(task_name.split()),
            "task_code": task_code,
            "skill_path": skill_path,
            "skill_selection": skill_selection,
            "match_status": "matched",
        })
    return {
        "schema_version": SCHEMA_VERSION,
        "offering": plan.get("offering"),
        "functional_area": plan.get("functional_area"),
        "tasks": context_tasks,
    }

def build_task_context_from_setup_task_plan(setup_task_plan: dict[str, Any]) -> dict[str, Any]:
    """Create task metadata only from the resolved planning artifact."""

    if setup_task_plan.get("schema_version") != SCHEMA_VERSION:
        raise TaskContextError("Setup-task plan has an unsupported schema.")
    tasks = setup_task_plan.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise TaskContextError("Setup-task plan must contain a non-empty tasks array.")

    context_tasks = []
    identifiers = set()
    for task in tasks:
        if not isinstance(task, dict):
            raise TaskContextError("Setup-task plan contains an invalid task.")
        task_name = task.get("task_name")
        sequence = _positive_sequence(task.get("sequence"))
        identifier = (_normalized_name(task_name), sequence)
        if identifier in identifiers:
            raise TaskContextError("Setup-task plan contains duplicate task name and sequence values.")
        identifiers.add(identifier)
        context_metadata = {key: task.get(key) for key in ("offering", "functional_area")}
        if not all(isinstance(value, str) and value.strip() for value in context_metadata.values()):
            raise TaskContextError("Setup-task plan task must contain offering and functional_area.")
        if task.get("execution_mode") == "manual":
            context_tasks.append({"sequence": sequence, "task_name": " ".join(task_name.split()), **context_metadata, "execution_mode": "manual", "match_status": "unmatched", "match_reason": task.get("match_reason", "User-designated manual task.")})
            continue
        task_code = task.get("task_code")
        skill_path = task.get("skill_path")
        if not isinstance(task_code, str) or not task_code.strip() or (skill_path is not None and (not isinstance(skill_path, str) or not skill_path.strip())):
            raise TaskContextError("Setup-task plan task must contain task_code and an optional skill_path.")
        context_tasks.append({"sequence": sequence, "task_name": " ".join(task_name.split()), **context_metadata, "task_code": task_code.strip(), "skill_path": skill_path.strip() if isinstance(skill_path, str) else None, "skill_selection": task.get("skill_selection"), "match_status": "matched"})
    return {"schema_version": SCHEMA_VERSION, "tasks": context_tasks}

def build_task_context(repository_root: Path, runbook_plan: dict[str, Any]) -> dict[str, Any]:
    root = repository_root.resolve(strict=True)
    plan = runbook_plan.get("plan")
    tasks = plan.get("tasks") if isinstance(plan, dict) else None
    if not isinstance(tasks, list) or not tasks:
        raise TaskContextError("Run-book plan must contain a non-empty tasks array.")
    context_tasks = []
    identifiers = set()
    for task in tasks:
        if not isinstance(task, dict):
            raise TaskContextError("Every run-book task must be an object.")
        task_name = task.get("name")
        sequence = _positive_sequence(task.get("sequence"))
        identifier = (_normalized_name(task_name), sequence)
        if identifier in identifiers:
            raise TaskContextError("Run-book plan contains duplicate task name and sequence values.")
        identifiers.add(identifier)
        task_code = _catalog_task_code(root, task_name)
        context_tasks.append({"sequence": sequence, "task_name": " ".join(task_name.split()), "task_code": task_code, "skill_path": _skill_path(root, task_code, task_name)})
    return {"schema_version": SCHEMA_VERSION, "tasks": context_tasks}


def resolve_task_context(task_context_path: Path, task_name: str, sequence: int) -> dict[str, str | int | None]:
    payload = _read_json_object(task_context_path, "Task context")
    if payload.get("schema_version") != SCHEMA_VERSION or not isinstance(payload.get("tasks"), list):
        raise TaskContextError("Task context has an unsupported schema.")
    wanted_name, wanted_sequence = _normalized_name(task_name), _positive_sequence(sequence)
    matches = [task for task in payload["tasks"] if isinstance(task, dict) and _normalized_name(task.get("task_name")) == wanted_name and _positive_sequence(task.get("sequence")) == wanted_sequence]
    if len(matches) != 1:
        raise TaskContextError("Task context must contain exactly one matching task name and sequence.")
    task = matches[0]
    if not isinstance(task.get("task_code"), str) or not task["task_code"].strip():
        raise TaskContextError("Task context entry must contain a non-empty task_code.")
    skill_path = task.get("skill_path")
    if skill_path is not None and (not isinstance(skill_path, str) or not skill_path.strip()):
        raise TaskContextError("Task context skill_path must be non-empty text when supplied.")
    metadata = {key: task.get(key) for key in ("offering", "functional_area")}
    if not all(isinstance(value, str) and value.strip() for value in metadata.values()):
        raise TaskContextError("Task context entry must contain offering and functional_area.")
    return {
        "sequence": wanted_sequence,
        "task_name": " ".join(task_name.split()),
        "task_code": task["task_code"].strip(),
        "skill_path": skill_path.strip() if isinstance(skill_path, str) else None,
        **metadata,
    }

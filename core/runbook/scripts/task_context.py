"""Local task context helpers."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any


SCHEMA_VERSION = "1.0"
CATALOG_PATH = Path("knowledge/setup-task-catalog/effective/setupTasksAll.json")
POLICY_PATH = Path("core/runbook/references/task-context-policy.json")
MANUAL_TASKS_SKILL_PATH = "shared/common/manual-tasks/SKILL.md"
MANUAL_TASKS_EXECUTION_ROUTE = "manual-tasks"


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


def _frontmatter_business_objects(artifact: Path) -> list[str]:
    """Return generator-owned REST business objects from a selected task artifact."""

    content = artifact.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\r?\n(?P<content>.*?)\r?\n---(?:\r?\n|\Z)", content, re.DOTALL)
    if not frontmatter:
        return []
    metadata = frontmatter.group("content")
    singular = re.search(r"^businessObject:\s*(?P<value>.+?)\s*$", metadata, re.MULTILINE)
    plural = re.search(
        r"^businessObjects:\s*\r?\n(?P<items>(?:[ \t]+-\s+.+(?:\r?\n|\Z))+)",
        metadata,
        re.MULTILINE,
    )
    values: list[str] = []
    raw_values = (
        [singular.group("value")]
        if singular
        else re.findall(r"^[ \t]+-\s+(.+?)\s*$", plural.group("items"), re.MULTILINE)
        if plural
        else []
    )
    for raw_value in raw_values:
        try:
            value = json.loads(raw_value)
        except json.JSONDecodeError:
            value = raw_value.strip().strip("\"'")
        if isinstance(value, str) and value.strip() and value.strip() not in values:
            values.append(value.strip())
    return values


def _business_objects(repository_root: Path, skill_path: str | None) -> list[str]:
    if skill_path is None:
        return []
    artifact = (repository_root / skill_path).resolve(strict=True)
    pillars_root = (repository_root / "pillars").resolve(strict=True)
    try:
        artifact.relative_to(pillars_root)
    except ValueError as error:
        raise TaskContextError("Task artifact must be located under pillars.") from error
    return _frontmatter_business_objects(artifact)


def _normalized_business_objects(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise TaskContextError("Task business_objects must be a string array.")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise TaskContextError("Task business_objects must contain non-empty strings.")
        normalized = item.strip()
        if normalized not in result:
            result.append(normalized)
    return result


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


def _selection_context(
    repository_root: Path,
    selected_path: str,
    *,
    offering: Any,
    functional_area: Any,
    canonical_reuse: bool,
) -> dict[str, Any]:
    project_context = {
        "offering": offering.strip() if isinstance(offering, str) and offering.strip() else None,
        "functional_area": functional_area.strip()
        if isinstance(functional_area, str) and functional_area.strip()
        else None,
    }
    artifact = repository_root / selected_path
    if artifact.name != "SKILL.md":
        return {
            "context_relation": "unscoped-guidance",
            "project_context": project_context,
            "skill_context": None,
        }
    skill_context = {
        "offering": _manifest_value(artifact, "offering"),
        "functional_area": _manifest_value(artifact, "functional_area"),
    }
    comparable = all(project_context.values()) and all(skill_context.values())
    same_context = comparable and all(
        _normalized_name(project_context[key]) == _normalized_name(skill_context[key])
        for key in project_context
    )
    if same_context:
        relation = "same-context"
    elif canonical_reuse:
        relation = "canonical-task-reuse"
    else:
        relation = "cross-context-fallback"
    result = {
        "context_relation": relation,
        "project_context": project_context,
        "skill_context": skill_context,
    }
    if relation == "canonical-task-reuse":
        result["context_note"] = (
            "The unique task-code-and-name skill is canonical and reusable across "
            "Oracle offering and functional-area contexts."
        )
    return result


def _offering_scoped_candidates(
    repository_root: Path, candidates: list[str], *, offering: Any, offering_code: Any
) -> list[str]:
    """Match complete declared offering identities, never path substrings."""
    def name(value: Any) -> str | None:
        return _normalized_name(value) if isinstance(value, str) and value.strip() else None

    def code(value: Any) -> str | None:
        return value.strip() if isinstance(value, str) and value.strip() else None

    mapping_path = repository_root / "knowledge/setup-task-catalog/effective/pillars-offerings-mapping.json"
    mapping = _read_json_object(mapping_path, "Offering mapping") if mapping_path.exists() else {}
    identities = [(code(item.get("offeringShortName")), name(item.get("offeringName")))
                  for item in mapping.get("items", []) if isinstance(item, dict)]
    source_name = name(offering)
    source_code = code(offering_code)
    # An offering supplied as a full catalog code is also supported.
    source_codes = {source_code} if source_code else {
        item_code for item_code, item_name in identities
        if item_code and (item_name == source_name or item_code == code(offering))
    }
    source_names = {item_name for item_code, item_name in identities
                    if item_name and item_code in source_codes}
    if source_name:
        source_names.add(source_name)
    scoped = []
    for candidate in candidates:
        artifact = repository_root / candidate
        candidate_code = code(_manifest_value(artifact, "offering_code"))
        candidate_name = name(_manifest_value(artifact, "offering"))
        candidate_codes = {candidate_code} if candidate_code else {
            item_code for item_code, item_name in identities
            if item_code and item_name == candidate_name
        }
        if source_codes and candidate_codes:
            matches = bool(source_codes & candidate_codes)
        else:
            matches = candidate_name is not None and candidate_name in source_names
        if matches:
            scoped.append(candidate)
    return scoped


def _skill_path(
    repository_root: Path,
    task_code: str,
    task_name: str,
    *,
    policy: dict[str, Any],
    offering: Any,
    functional_area: Any,
    offering_code: Any = None,
) -> tuple[str | None, dict[str, Any]]:
    matches = []
    for manifest in repository_root.glob("pillars/**/SKILL.md"):
        if _manifest_value(manifest, "task_code") != task_code:
            continue
        manifest_name = _manifest_value(manifest, "task_name")
        if manifest_name is None or _normalized_name(manifest_name) == _normalized_name(task_name):
            matches.append(manifest)
    flat_filename = "-".join(re.findall(r"[a-z0-9]+", _normalized_name(task_name))) + ".md"
    matches.extend(repository_root.glob(f"pillars/**/{flat_filename}"))
    candidates = sorted({match.relative_to(repository_root).as_posix() for match in matches})
    if not candidates:
        return None, {
            "status": "missing",
            "selected_by": "FLAT_TASK_GUIDANCE_MISSING",
            "candidates": [],
            "context_relation": "missing",
            "project_context": {"offering": offering, "functional_area": functional_area},
            "skill_context": None,
        }
    if len(candidates) == 1:
        selected_by = "FLAT_TASK_GUIDANCE_FILE" if candidates[0].endswith(".md") and not candidates[0].endswith("/SKILL.md") else "EXACT_TASK_CODE_AND_NAME"
        return candidates[0], {
            "status": "selected",
            "selected_by": selected_by,
            "candidates": candidates,
            **_selection_context(
                repository_root,
                candidates[0],
                offering=offering,
                functional_area=functional_area,
                canonical_reuse=selected_by == "EXACT_TASK_CODE_AND_NAME",
            ),
        }
    if policy["multiple_skill_policy"] == "SELECT_LEXICOGRAPHIC_PATH":
        return candidates[0], {"status": "selected", "selected_by": "LEXICOGRAPHIC_PATH", "candidates": candidates, **_selection_context(repository_root, candidates[0], offering=offering, functional_area=functional_area, canonical_reuse=False)}
    scoped = _offering_scoped_candidates(repository_root, candidates, offering=offering, offering_code=offering_code)
    if len(scoped) == 1:
        return scoped[0], {"status": "selected", "selected_by": "PROJECT_OFFERING_OR_PILLAR", "candidates": candidates, **_selection_context(repository_root, scoped[0], offering=offering, functional_area=functional_area, canonical_reuse=False)}
    if len(scoped) > 1 and isinstance(functional_area, str) and functional_area.strip():
        area_scoped = []
        for candidate in scoped:
            candidate_area = _manifest_value(repository_root / candidate, "functional_area")
            if isinstance(candidate_area, str) and candidate_area.strip() and _normalized_name(candidate_area) == _normalized_name(functional_area):
                area_scoped.append(candidate)
        if len(area_scoped) == 1:
            return area_scoped[0], {"status": "selected", "selected_by": "PROJECT_OFFERING_AND_FUNCTIONAL_AREA", "candidates": candidates, **_selection_context(repository_root, area_scoped[0], offering=offering, functional_area=functional_area, canonical_reuse=False)}
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
                    "business_objects": [],
                }
            )
            continue
        try:
            task_code = _catalog_task_code(root, task_name)
            skill_path, skill_selection = _skill_path(
                root,
                task_code,
                task_name,
                policy=policy,
                offering=task.get("offering", plan.get("offering")),
                functional_area=task.get("functional_area", plan.get("functional_area")),
                offering_code=task.get("offering_code", plan.get("offering_code")),
            )
        except TaskContextError as error:
            context_tasks.append({
                "sequence": sequence,
                "task_name": " ".join(task_name.split()),
                "execution_mode": "manual",
                "match_status": "unmatched",
                "match_reason": str(error),
                "business_objects": [],
            })
            continue
        if skill_path is None and not policy["include_missing_skill"]:
            context_tasks.append({"sequence": sequence, "task_name": " ".join(task_name.split()), "execution_mode": "manual", "match_status": "unmatched", "match_reason": "No pillar skill manifest was found and task-context policy excludes missing skills.", "business_objects": []})
            continue
        context_task = {
            "sequence": sequence,
            "task_name": " ".join(task_name.split()),
            "task_code": task_code,
            "offering": task.get("offering", plan.get("offering")),
            "functional_area": task.get("functional_area", plan.get("functional_area")),
            "skill_path": skill_path,
            "skill_selection": skill_selection,
            "match_status": "matched",
            "business_objects": _business_objects(root, skill_path),
        }
        if skill_path is None:
            context_task.update(
                {
                    "execution_mode": "manual",
                    "execution_route": MANUAL_TASKS_EXECUTION_ROUTE,
                    "execution_skill_path": MANUAL_TASKS_SKILL_PATH,
                    "match_reason": (
                        "No task skill or flat task guidance exists in FSCR; "
                        "route this catalog task to the shared Manual Tasks skill."
                    ),
                }
            )
        context_tasks.append(context_task)
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
        if task.get("execution_route") == MANUAL_TASKS_EXECUTION_ROUTE:
            task_code = task.get("task_code")
            execution_skill_path = task.get("execution_skill_path")
            if not isinstance(task_code, str) or not task_code.strip():
                raise TaskContextError("Manual-task fallback must contain a non-empty task_code.")
            if execution_skill_path != MANUAL_TASKS_SKILL_PATH:
                raise TaskContextError("Manual-task fallback must target the shared Manual Tasks skill.")
            context_tasks.append(
                {
                    "sequence": sequence,
                    "task_name": " ".join(task_name.split()),
                    **context_metadata,
                    "task_code": task_code.strip(),
                    "skill_path": None,
                    "skill_selection": task.get("skill_selection"),
                    "execution_mode": "manual",
                    "execution_route": MANUAL_TASKS_EXECUTION_ROUTE,
                    "execution_skill_path": MANUAL_TASKS_SKILL_PATH,
                    "match_status": "matched",
                    "match_reason": task.get("match_reason"),
                    "business_objects": _normalized_business_objects(task.get("business_objects", [])),
                }
            )
            continue
        if task.get("execution_mode") == "manual":
            context_tasks.append({"sequence": sequence, "task_name": " ".join(task_name.split()), **context_metadata, "execution_mode": "manual", "match_status": "unmatched", "match_reason": task.get("match_reason", "User-designated manual task."), "business_objects": _normalized_business_objects(task.get("business_objects", []))})
            continue
        task_code = task.get("task_code")
        skill_path = task.get("skill_path")
        if not isinstance(task_code, str) or not task_code.strip() or (skill_path is not None and (not isinstance(skill_path, str) or not skill_path.strip())):
            raise TaskContextError("Setup-task plan task must contain task_code and an optional skill_path.")
        context_tasks.append({"sequence": sequence, "task_name": " ".join(task_name.split()), **context_metadata, "task_code": task_code.strip(), "skill_path": skill_path.strip() if isinstance(skill_path, str) else None, "skill_selection": task.get("skill_selection"), "match_status": "matched", "business_objects": _normalized_business_objects(task.get("business_objects", []))})
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
    result = {
        "sequence": wanted_sequence,
        "task_name": " ".join(task_name.split()),
        "task_code": task["task_code"].strip(),
        "skill_path": skill_path.strip() if isinstance(skill_path, str) else None,
        **metadata,
    }
    if task.get("execution_route") == MANUAL_TASKS_EXECUTION_ROUTE:
        if task.get("execution_skill_path") != MANUAL_TASKS_SKILL_PATH:
            raise TaskContextError("Manual-task fallback must target the shared Manual Tasks skill.")
        task_description = task.get("task_description")
        if task_description is not None and not isinstance(task_description, str):
            raise TaskContextError("Manual-task fallback task_description must be text when supplied.")
        result.update(
            {
                "execution_mode": "manual",
                "execution_route": MANUAL_TASKS_EXECUTION_ROUTE,
                "execution_skill_path": MANUAL_TASKS_SKILL_PATH,
                "match_reason": task.get("match_reason"),
                "skill_selection": task.get("skill_selection"),
                "business_objects": _normalized_business_objects(task.get("business_objects", [])),
                "task_description": task_description or "",
            }
        )
    return result

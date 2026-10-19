#!/usr/bin/env python3
"""Resolve non-REST task rules and enforce immutable Data Loader previews."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping

from task_context import TaskContextError, resolve_task_context


SCHEMA_VERSION = "1.0"
REST_RESOURCE_NAME = "ora_rest_execution.md"
REST_WRITE_ACTIONS = {"rest_post", "rest_patch", "rest_delete", "rest_action"}
TERMINAL_ACTION = "terminal"
LEGACY_SCHEMA_VERSION = "2.0"
CURRENT_SCHEMA_VERSION = "3.0"
LEGACY_ACTION_TYPES = {
    "collect_input", "process_bulk", "rest_describe_attribute_cache", "rest_payload_contract",
    "rest_get", "rest_post", "rest_patch", "rest_delete", "rest_action", "preview_gate",
    "approval_gate", "design_advisory", "execution_gate", "terminal",
}
CURRENT_ACTION_TYPES = {
    "validate_input", "resolve_dependency", "reference_lookup", "apply_default",
    "design_enforcement", "error_handler", "execution_gate", "evaluate_result", "terminal",
}
RULE_RESULT_STATUSES = {"passed", "blocked", "overridden", "not_applicable"}
class TaskRuleContractError(ValueError):
    """The task rule or preview contract is invalid or unsafe."""


def _normalized_name(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TaskRuleContractError("Task name must be non-empty text.")
    return " ".join(value.split()).casefold()


def _canonical_json(value: Any) -> bytes:
    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as error:
        raise TaskRuleContractError(
            "Task execution data must be finite, JSON-compatible data."
        ) from error
    return encoded.encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _repository_relative(path: Path, repository_root: Path) -> str:
    return path.relative_to(repository_root).as_posix()


def _read_json_object(path: Path, description: str) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise TaskRuleContractError(
            f"{description} is not valid JSON: {error.msg}."
        ) from error
    if not isinstance(value, dict):
        raise TaskRuleContractError(f"{description} must be a JSON object.")
    return value


def _resolve_skill_location(
    repository_root: Path,
    supplied_skill_path: str,
) -> tuple[Path, Path]:
    """Return the rule-resource directory and exact Task Context guidance path."""

    if not isinstance(supplied_skill_path, str) or not supplied_skill_path.strip():
        raise TaskRuleContractError("skill_path must be non-empty text.")
    root = repository_root.resolve(strict=True)
    supplied = Path(supplied_skill_path.strip())
    candidate = supplied if supplied.is_absolute() else root / supplied
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as error:
        raise TaskRuleContractError("skill_path does not exist.") from error
    if not _inside(resolved, root):
        raise TaskRuleContractError("skill_path must resolve inside the repository.")
    if resolved.is_file():
        if resolved.suffix.casefold() != ".md":
            raise TaskRuleContractError("skill_path file must be Markdown guidance.")
        return resolved.parent, resolved
    manifest = resolved / "SKILL.md"
    if not manifest.is_file():
        raise TaskRuleContractError("skill_path directory must contain SKILL.md.")
    return resolved, manifest


def _required_task_code(value: str | None) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TaskRuleContractError(
            "task_code is required from the persisted Task Context."
        )
    return value.strip()


def _skipped_rule_plan(
    *, repository_root: Path, skill_path: Path, task_name: str, reason: str,
    task_code: str,
) -> Dict[str, Any]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "taskCode": task_code,
        "taskName": task_name,
        "skillPath": _repository_relative(skill_path, repository_root),
        "executionRoute": "data-loader",
        "taskValidationStatus": "skipped",
        "taskValidationSkipReason": reason,
        "ruleResources": [],
        "skippedNodes": [],
        "excludedResources": [],
    }


def _skipped_missing_guidance_plan(
    *, context: Mapping[str, Any], reason: str
) -> Dict[str, Any]:
    """Return a warning instead of failing when persisted guidance disappeared."""

    return {
        "schemaVersion": SCHEMA_VERSION,
        "taskCode": context["task_code"],
        "taskName": context["task_name"],
        "executionRoute": "data-loader",
        "taskValidationStatus": "skipped",
        "taskValidationSkipReason": reason,
        "taskValidationWarning": reason,
        "ruleResources": [],
        "skippedNodes": [],
        "excludedResources": [],
        "sequence": context["sequence"],
    }


def _validated_registry_task(
    registry: Mapping[str, Any],
    task_name: str,
    task_code: str,
    *,
    allow_readiness_override: bool = False,
) -> Dict[str, Any]:
    tasks = registry.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise TaskRuleContractError("ora_rule_registry.json must contain tasks.")
    matching = [
        item
        for item in tasks
        if isinstance(item, dict)
        and _normalized_name(item.get("task_name")) == _normalized_name(task_name)
        and isinstance(item.get("task_code"), str)
        and item["task_code"].strip() == task_code
    ]
    if not matching:
        raise TaskRuleContractError(
            "The supplied Task Context code and name do not match any task in the skill registry."
        )
    if len(matching) != 1:
        raise TaskRuleContractError(
            "The supplied Task Context code and name must match exactly one task in the skill registry."
        )
    task = matching[0]
    task_code = task.get("task_code")
    if not isinstance(task_code, str) or not task_code.strip():
        raise TaskRuleContractError("The matched registry task is missing task_code.")
    nodes = task.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise TaskRuleContractError("The matched registry task has no rule nodes.")
    version = registry.get("schema_version", CURRENT_SCHEMA_VERSION)
    if version not in {LEGACY_SCHEMA_VERSION, CURRENT_SCHEMA_VERSION}:
        raise TaskRuleContractError(f"Unsupported registry schema_version: {version!r}.")
    readiness = task.get("readiness")
    readiness_invalid = (
        not isinstance(readiness, dict)
        or readiness.get("status") not in {"ready", "incomplete"}
        or not isinstance(readiness.get("blocking_reasons"), list)
    )
    if readiness_invalid and version == LEGACY_SCHEMA_VERSION:
        _legacy_structural_check(task)
        task = dict(task)
        task["readiness"] = {"status": "ready", "blocking_reasons": []}
        return task
    if readiness_invalid and not allow_readiness_override:
        raise TaskRuleContractError("The matched registry task has invalid readiness.")
    if readiness_invalid:
        task = dict(task)
        task["readiness"] = {"status": "overridden", "blocking_reasons": [], "warning": "Task registry has no valid readiness definition."}
        return task
    if readiness["status"] == "incomplete" and not allow_readiness_override:
        messages = [
            str(reason.get("message"))
            for reason in readiness["blocking_reasons"]
            if isinstance(reason, dict) and isinstance(reason.get("message"), str)
        ]
        raise TaskRuleContractError(
            "The matched registry task is incomplete: "
            + ("; ".join(messages) or "resolve authoring blockers.")
        )
    if readiness["status"] == "incomplete":
        task = dict(task)
        task["readiness"] = {
            **readiness,
            "status": "overridden",
            "warning": "Task registry readiness was explicitly overridden.",
        }
    return task


def _legacy_structural_check(task: Mapping[str, Any]) -> None:
    nodes = _validated_nodes(task)
    identifiers = {node["id"] for node in nodes}
    start_node = task.get("start_node")
    if not isinstance(start_node, str) or start_node not in identifiers:
        raise TaskRuleContractError("The legacy registry task has an invalid start_node.")
    for node in nodes:
        if node["action_type"] not in LEGACY_ACTION_TYPES | CURRENT_ACTION_TYPES:
            raise TaskRuleContractError(
                f"Legacy registry node {node['id']} has unsupported action_type {node['action_type']!r}."
            )
        transitions = node.get("transitions", {})
        if not isinstance(transitions, dict) or not all(
            isinstance(outcome, str) and isinstance(target, str) for outcome, target in transitions.items()
        ):
            raise TaskRuleContractError(f"Legacy registry node {node['id']} has invalid transitions.")
        missing_targets = [target for target in transitions.values() if target not in identifiers]
        if missing_targets:
            raise TaskRuleContractError(
                f"Legacy registry node {node['id']} has missing transition target(s): {', '.join(missing_targets)}."
            )
        missing_prerequisites = [dependency for dependency in node["prerequisites"] if dependency not in identifiers]
        if missing_prerequisites:
            raise TaskRuleContractError(
                f"Legacy registry node {node['id']} has missing prerequisite(s): {', '.join(missing_prerequisites)}."
            )


def _validated_nodes(task: Mapping[str, Any]) -> List[Dict[str, Any]]:
    nodes = task["nodes"]
    validated: List[Dict[str, Any]] = []
    identifiers: set[str] = set()
    for node in nodes:
        if not isinstance(node, dict):
            raise TaskRuleContractError("Every registry node must be an object.")
        identifier = node.get("id")
        sequence = node.get("sequence")
        action_type = node.get("action_type")
        source = node.get("source")
        prerequisites = node.get("prerequisites")
        if not isinstance(identifier, str) or not identifier.strip():
            raise TaskRuleContractError("Every registry node must have an id.")
        if identifier in identifiers:
            raise TaskRuleContractError(f"Duplicate registry node id: {identifier}.")
        if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 1:
            raise TaskRuleContractError(f"Registry node {identifier} has invalid sequence.")
        if not isinstance(action_type, str) or not action_type:
            raise TaskRuleContractError(f"Registry node {identifier} has no action_type.")
        if not isinstance(source, dict) or not isinstance(source.get("file"), str):
            raise TaskRuleContractError(f"Registry node {identifier} has invalid source.")
        if not isinstance(prerequisites, list) or not all(
            isinstance(value, str) and value for value in prerequisites
        ):
            raise TaskRuleContractError(
                f"Registry node {identifier} has invalid prerequisites."
            )
        identifiers.add(identifier)
        validated.append(node)
    return sorted(validated, key=lambda item: (item["sequence"], item["id"]))


def resolve_task_rules(
    *,
    repository_root: Path,
    skill_path: str,
    task_name: str,
    allow_readiness_override: bool = False,
    task_code: str | None = None,
) -> Dict[str, Any]:
    """Resolve one task and return its ordered, non-REST rule-resource plan."""

    root = repository_root.resolve(strict=True)
    skill_directory, resolved_skill_path = _resolve_skill_location(root, skill_path)
    resolved_task_code = _required_task_code(task_code)
    resource_directory = skill_directory / "ora-resource"
    registry_path = resource_directory / "ora_rule_registry.json"
    if not resource_directory.is_dir():
        return _skipped_rule_plan(
            repository_root=root,
            skill_path=resolved_skill_path,
            task_name=task_name,
            reason="The selected skill has no ora-resource directory.",
            task_code=resolved_task_code,
        )
    if not registry_path.is_file():
        return _skipped_rule_plan(
            repository_root=root,
            skill_path=resolved_skill_path,
            task_name=task_name,
            reason="The selected skill has no ora_rule_registry.json.",
            task_code=resolved_task_code,
        )
    registry = _read_json_object(registry_path, "ora_rule_registry.json")
    task = _validated_registry_task(
        registry,
        task_name,
        resolved_task_code,
        allow_readiness_override=allow_readiness_override,
    )
    nodes = _validated_nodes(task)

    # Read-only REST nodes remain part of validation. Write actions are never
    # included in the task-validation plan.
    excluded_node_ids = {
        node["id"] for node in nodes if node["action_type"] in REST_WRITE_ACTIONS
    }
    skipped: Dict[str, str] = {
        node["id"]: "REST write actions are excluded until task-preview approval."
        for node in nodes if node["id"] in excluded_node_ids
    }
    # A non-REST node that requires an excluded REST node cannot execute safely.
    changed = True
    while changed:
        changed = False
        for node in nodes:
            if node["id"] in excluded_node_ids:
                continue
            excluded_dependencies = [
                value for value in node["prerequisites"] if value in excluded_node_ids
            ]
            if excluded_dependencies:
                excluded_node_ids.add(node["id"])
                skipped[node["id"]] = (
                    "Depends on excluded node(s): " + ", ".join(excluded_dependencies) + "."
                )
                changed = True

    selected = [
        node
        for node in nodes
        if node["id"] not in excluded_node_ids
        and node["action_type"] != TERMINAL_ACTION
    ]
    nodes_by_file: Dict[str, List[Dict[str, Any]]] = {}
    for node in selected:
        nodes_by_file.setdefault(node["source"]["file"], []).append(node)

    resources: List[Dict[str, Any]] = []
    for filename, file_nodes in nodes_by_file.items():
        if not filename.startswith("ora_") or not filename.endswith(".md"):
            raise TaskRuleContractError(
                f"Registry source {filename!r} is not an ora-resource Markdown file."
            )
        source_path = (resource_directory / filename).resolve(strict=True)
        if not _inside(source_path, resource_directory.resolve(strict=True)):
            raise TaskRuleContractError(
                f"Rule resource {filename} resolves outside ora-resource."
            )
        resources.append(
            {
                "sequence": min(node["sequence"] for node in file_nodes),
                "file": filename,
                "path": _repository_relative(source_path, root),
                "nodes": [
                    {
                        "id": node["id"],
                        "sequence": node["sequence"],
                        "actionType": node["action_type"],
                        "appliesWhen": node.get("applies_when"),
                        "prerequisites": node.get("prerequisites", []),
                        "transitions": node.get("transitions", {}),
                    }
                    for node in file_nodes
                ],
            }
        )

    if not resources:
        raise TaskRuleContractError(
            "No task rule resources remain after applying exclusions."
        )
    resources.sort(key=lambda item: (item["sequence"], item["file"]))
    return {
        "schemaVersion": SCHEMA_VERSION,
        "taskCode": task["task_code"],
        "taskName": task["task_name"],
        "skillPath": _repository_relative(resolved_skill_path, root),
        "registryPath": _repository_relative(registry_path, root),
        "executionRoute": "data-loader",
        "taskValidationStatus": "overridden" if task.get("readiness", {}).get("status") == "overridden" else "ready",
        "taskValidationWarning": task.get("readiness", {}).get("warning"),
        "ruleResources": resources,
        "skippedNodes": [
            {"id": node["id"], "reason": skipped[node["id"]]}
            for node in nodes
            if node["id"] in skipped
        ],
        "excludedResources": [],
    }


def resolve_task_rules_from_context(
    *,
    repository_root: Path,
    task_context_path: Path,
    task_name: str,
    sequence: int,
    allow_readiness_override: bool = False,
) -> Dict[str, Any]:
    """Resolve task rules only from the project-persisted task context."""
    try:
        context = resolve_task_context(task_context_path, task_name, sequence)
    except TaskContextError as error:
        raise TaskRuleContractError(str(error)) from error
    if context["skill_path"] is None:
        return {
            "schemaVersion": SCHEMA_VERSION,
            "taskCode": context["task_code"],
            "taskName": context["task_name"],
            "executionRoute": "data-loader",
            "taskValidationStatus": "skipped",
            "taskValidationSkipReason": "No skill_path is available for the persisted task context.",
            "ruleResources": [],
            "skippedNodes": [],
            "excludedResources": [],
            "sequence": context["sequence"],
        }
    try:
        plan = resolve_task_rules(
            repository_root=repository_root,
            skill_path=str(context["skill_path"]),
            task_name=str(context["task_name"]),
            allow_readiness_override=allow_readiness_override,
            task_code=str(context["task_code"]),
        )
    except TaskRuleContractError as error:
        if str(error) == (
            "The supplied Task Context code and name do not match any task in the skill registry."
        ):
            return _skipped_missing_guidance_plan(
                context=context,
                reason="The selected task is not registered in the skill rule registry.",
            )
        if str(error) not in {
            "skill_path does not exist.",
            "skill_path directory must contain SKILL.md.",
        }:
            raise
        return _skipped_missing_guidance_plan(
            context=context,
            reason=(
                "The persisted task guidance is no longer available; "
                f"Task Validation was skipped. ({error})"
            ),
        )
    if plan["taskCode"] != context["task_code"]:
        raise TaskRuleContractError(
            "Persisted task context task_code does not match the resolved skill registry."
        )
    plan["sequence"] = context["sequence"]
    return plan


def _validate_rule_results(
    plan: Mapping[str, Any],
    results: Any,
    *,
    allow_readiness_override: bool = False,
) -> List[Dict[str, Any]]:
    if not isinstance(results, list):
        raise TaskRuleContractError("ruleResults must be an array.")
    expected = [resource["file"] for resource in plan["ruleResources"]]
    actual: List[str] = []
    validated: List[Dict[str, Any]] = []
    for index, result in enumerate(results):
        if not isinstance(result, dict):
            raise TaskRuleContractError("Every rule result must be an object.")
        source = result.get("source")
        status = result.get("status")
        if "issues" not in result or "changes" not in result:
            raise TaskRuleContractError(
                f"Rule result {source or index} must include issues and changes arrays."
            )
        issues = result["issues"]
        changes = result["changes"]
        if not isinstance(source, str):
            raise TaskRuleContractError(f"Rule result {index} is missing source.")
        if status not in RULE_RESULT_STATUSES:
            raise TaskRuleContractError(
                f"Rule result {source} status must be passed, blocked, overridden, or not_applicable."
            )
        if status == "overridden" and not allow_readiness_override:
            raise TaskRuleContractError(
                f"Rule result {source} requires an explicit user override."
            )
        if not isinstance(issues, list) or not all(
            isinstance(issue, dict) for issue in issues
        ):
            raise TaskRuleContractError(f"Rule result {source} has invalid issues.")
        if not isinstance(changes, list) or not all(
            isinstance(change, dict) for change in changes
        ):
            raise TaskRuleContractError(f"Rule result {source} has invalid changes.")
        for issue in issues:
            if not isinstance(issue.get("message"), str) or not issue["message"].strip():
                raise TaskRuleContractError(
                    f"Every issue for {source} must include a non-empty message."
                )
            if issue.get("severity") not in (None, "error", "warning", "info"):
                raise TaskRuleContractError(
                    f"Every issue for {source} must use error, warning, or info severity."
                )
        for change in changes:
            if not {"path", "before", "after", "reason"} <= set(change):
                raise TaskRuleContractError(
                    f"Every change for {source} must include path, before, after, and reason."
                )
            if not isinstance(change["path"], str) or not change["path"].strip():
                raise TaskRuleContractError(
                    f"Every change for {source} must include a non-empty path."
                )
            if not isinstance(change["reason"], str) or not change["reason"].strip():
                raise TaskRuleContractError(
                    f"Every change for {source} must include a non-empty reason."
                )
        if status in {"blocked", "overridden"} and not issues:
            raise TaskRuleContractError(
                f"Blocked or overridden rule result {source} must include at least one issue."
            )
        if status in {"passed", "not_applicable"} and any(
            issue.get("severity") == "error" for issue in issues
        ):
            raise TaskRuleContractError(
                f"Non-blocking rule result {source} cannot contain an error issue."
            )
        actual.append(source)
        validated.append(
            {
                "source": source,
                "status": status,
                "issues": issues,
                "changes": changes,
            }
        )
    if actual != expected:
        raise TaskRuleContractError(
            "ruleResults must cover every planned rule resource exactly once and in order."
        )
    blocked = [result["source"] for result in validated if result["status"] == "blocked"]
    if blocked:
        raise TaskRuleContractError(
            "Preview is blocked until user corrections are supplied and all rules pass: "
            + ", ".join(blocked)
            + "."
        )
    return validated


def validate_rule_results(
    plan: Mapping[str, Any],
    results: Any,
    *,
    allow_readiness_override: bool = False,
) -> List[Dict[str, Any]]:
    """Validate one ordered set of rule-evaluation results for a resolved plan."""
    return _validate_rule_results(
        plan,
        results,
        allow_readiness_override=allow_readiness_override,
    )


def build_task_preview(
    *,
    repository_root: Path,
    skill_path: str,
    task_name: str,
    final_data: Any,
    rule_results: Any,
    allow_readiness_override: bool = False,
    task_code: str | None = None,
    now: Callable[[], datetime] | None = None,
) -> Dict[str, Any]:
    """Build a preview only after all non-REST rules pass."""

    plan = resolve_task_rules(
        repository_root=repository_root,
        skill_path=skill_path,
        task_name=task_name,
        allow_readiness_override=allow_readiness_override,
        task_code=task_code,
    )
    validated_results = _validate_rule_results(
        plan,
        rule_results,
        allow_readiness_override=allow_readiness_override,
    )
    _canonical_json(final_data)
    clock = now or (lambda: datetime.now(timezone.utc))
    generated_at = clock()
    if generated_at.tzinfo is None:
        raise TaskRuleContractError("Preview time must include a timezone.")
    return {
        "schemaVersion": SCHEMA_VERSION,
        "taskCode": plan["taskCode"],
        "taskName": plan["taskName"],
        "executionRoute": "data-loader",
        "generatedAt": generated_at.astimezone(timezone.utc).isoformat().replace(
            "+00:00", "Z"
        ),
        "ruleResults": validated_results,
        "finalData": final_data,
    }


def verify_preview(preview: Any) -> Dict[str, Any]:
    if not isinstance(preview, dict):
        raise TaskRuleContractError("preview must be an object.")
    if preview.get("executionRoute") != "data-loader":
        raise TaskRuleContractError("Only the data-loader execution route is supported.")
    return preview


def approve_task_preview(
    preview: Any,
    *,
    now: Callable[[], datetime] | None = None,
) -> Dict[str, Any]:
    """Create an explicit approval for a verified preview."""

    verified = verify_preview(preview)
    clock = now or (lambda: datetime.now(timezone.utc))
    approved_at = clock()
    if approved_at.tzinfo is None:
        raise TaskRuleContractError("Approval time must include a timezone.")
    return {
        "schemaVersion": SCHEMA_VERSION,
        "approved": True,
        "approvedAt": approved_at.astimezone(timezone.utc).isoformat().replace(
            "+00:00", "Z"
        ),
        "taskCode": verified.get("taskCode"),
        "executionRoute": "data-loader",
    }


def approved_loader_payload(preview: Any, approval: Any) -> Dict[str, Any]:
    """Return exactly the final data covered by a valid approval."""

    verified = verify_preview(preview)
    if not isinstance(approval, dict) or approval.get("approved") is not True:
        raise TaskRuleContractError("An explicit approval record is required.")
    for field in ("taskCode", "executionRoute"):
        if approval.get(field) != verified.get(field):
            raise TaskRuleContractError(f"Approval {field} does not match the preview.")
    return {
        "schemaVersion": SCHEMA_VERSION,
        "approved": True,
        "taskCode": verified["taskCode"],
        "taskName": verified["taskName"],
        "executionRoute": "data-loader",
        "finalData": verified["finalData"],
    }

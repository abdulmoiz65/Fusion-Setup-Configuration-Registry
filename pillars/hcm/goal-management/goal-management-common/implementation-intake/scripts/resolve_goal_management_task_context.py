#!/usr/bin/env python3
"""Resolve Goal Management setup tasks to one exact task-skill manifest."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence


class GoalManagementTaskContextError(ValueError):
    """The mapping cannot identify exactly one Goal Management task skill."""


def _normalized(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GoalManagementTaskContextError(f"{label} must be non-empty text")
    return " ".join(value.split())


def _sequence(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise GoalManagementTaskContextError("Resolver Sequence must be a positive integer")
    return value


def _operations(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise GoalManagementTaskContextError("Operations must be a list")
    operations = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, Mapping):
            raise GoalManagementTaskContextError(f"Operations item {index} must be an object")
        activity = item.get("activity", item.get("operation"))
        if not isinstance(activity, str) or not activity.strip():
            raise GoalManagementTaskContextError(
                f"Operations item {index} must contain non-empty activity or operation text"
            )
        operation = dict(item)
        operation["activity"] = " ".join(activity.split())
        operation.setdefault("sequence", index)
        if type(operation["sequence"]) is not int or operation["sequence"] < 1:
            raise GoalManagementTaskContextError(f"Operations item {index} sequence must be a positive integer")
        operations.append(operation)
    sequences = [item["sequence"] for item in operations]
    if len(sequences) != len(set(sequences)):
        raise GoalManagementTaskContextError("Operation sequence values must be unique within a task")
    return sorted(operations, key=lambda item: item["sequence"])


def _manifest_value(path: Path, field: str) -> str | None:
    match = re.search(rf"^{re.escape(field)}:\s*[\"']?([^\"'#\r\n]+)", path.read_text(encoding="utf-8"), re.MULTILINE)
    return match.group(1).strip() if match else None


def _repository_root(value: Path | None = None) -> Path:
    candidates = [value.resolve()] if value else Path(__file__).resolve().parents
    for candidate in candidates:
        if (
            (candidate / "schemas/skill-manifest.schema.json").is_file()
            and (candidate / "pillars/hcm/goal-management").is_dir()
        ):
            return candidate
    qualifier = "configured " if value else ""
    raise GoalManagementTaskContextError(
        f"Cannot locate the {qualifier}FSCR repository root"
    )


def _manifest_candidates(repository_root: Path, task_code: str, task_name: str, offering: str, functional_area: str) -> list[Path]:
    candidates = []
    for manifest in (repository_root / "pillars" / "hcm" / "goal-management").glob("**/SKILL.md"):
        fields = {
            "task_code": _manifest_value(manifest, "task_code"),
            "task_name": _manifest_value(manifest, "task_name"),
            "offering": _manifest_value(manifest, "offering"),
            "functional_area": _manifest_value(manifest, "functional_area"),
        }
        if not all(fields.values()):
            continue
        if (
            _normalized(fields["task_code"], "manifest task_code") == task_code
            and _normalized(fields["task_name"], "manifest task_name").casefold() == task_name.casefold()
            and _normalized(fields["offering"], "manifest offering").casefold() == offering.casefold()
            and _normalized(fields["functional_area"], "manifest functional_area").casefold() == functional_area.casefold()
        ):
            candidates.append(manifest)
    return sorted(candidates)


def build_goal_management_task_context(rows: Sequence[Mapping[str, Any]], repository_root: Path | None = None) -> dict[str, Any]:
    """Resolve rows using task code, name, offering, and functional area."""

    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)) or not rows:
        raise GoalManagementTaskContextError("identified task mapping must contain one or more rows")
    root = _repository_root(repository_root)
    tasks, seen_sequences, seen_identities = [], set(), set()
    for row in rows:
        if not isinstance(row, Mapping):
            raise GoalManagementTaskContextError("identified task mapping contains an invalid row")
        offering = _normalized(row.get("Offering"), "Offering")
        if offering.casefold() != "goal management":
            raise GoalManagementTaskContextError("Goal Management task context accepts only Goal Management rows")
        task_name = _normalized(row.get("Matched Task Name", row.get("Source Task Name")), "Task Name")
        task_code = _normalized(row.get("Matched Task Code"), "Matched Task Code")
        functional_area = _normalized(row.get("Functional Area"), "Functional Area")
        sequence = _sequence(row.get("Resolver Sequence"))
        operations = _operations(row.get("Operations"))
        candidates = _manifest_candidates(root, task_code, task_name, offering, functional_area)
        if len(candidates) != 1:
            paths = [path.relative_to(root).as_posix() for path in candidates]
            raise GoalManagementTaskContextError(
                f"Route confirmation required for {task_name!r} in {functional_area!r}: found {len(paths)} exact manifest candidates {paths}"
            )
        if sequence in seen_sequences:
            raise GoalManagementTaskContextError("Resolver Sequence values must be unique")
        identity = (task_code.casefold(), task_name.casefold(), offering.casefold(), functional_area.casefold())
        if identity in seen_identities:
            raise GoalManagementTaskContextError(
                "Duplicate stable task identity; combine object work under one task Operations list"
            )
        seen_sequences.add(sequence)
        seen_identities.add(identity)
        tasks.append(
            {
                "sequence": sequence,
                "source_sequence": row.get("Source Sequence"),
                "task_name": task_name,
                "task_code": task_code,
                "skill_path": candidates[0].relative_to(root).as_posix(),
                "offering": offering,
                "functional_area": functional_area,
                "task_identity": {
                    "task_code": task_code,
                    "task_name": task_name,
                    "offering": offering,
                    "functional_area": functional_area,
                },
                "operations": operations,
                "skill_selection": {
                    "status": "selected",
                    "selected_by": "EXACT_TASK_CODE_NAME_OFFERING_FUNCTIONAL_AREA",
                    "candidates": [candidates[0].relative_to(root).as_posix()],
                },
            }
        )
    return {"schema_version": "1.2", "tasks": sorted(tasks, key=lambda task: task["sequence"])}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mapping", type=Path, required=True, help="Confirmed identified-task-mapping.json")
    parser.add_argument("--output", type=Path, required=True, help="Goal Management task-context.json output")
    parser.add_argument("--repository-root", type=Path, help="Repository root; defaults to this script's repository")
    args = parser.parse_args()
    try:
        mapping = json.loads(args.mapping.read_text(encoding="utf-8"))
        if not isinstance(mapping, Mapping) or not isinstance(mapping.get("tasks"), list):
            raise GoalManagementTaskContextError("identified task mapping must contain a tasks array")
        result = build_goal_management_task_context(mapping["tasks"], args.repository_root)
    except (OSError, json.JSONDecodeError, GoalManagementTaskContextError) as exc:
        parser.error(str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

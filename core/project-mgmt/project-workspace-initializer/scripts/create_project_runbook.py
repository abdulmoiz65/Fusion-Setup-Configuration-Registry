#!/usr/bin/env python3
"""Generate Run Book planning artifacts for an initialized project.

This command neither creates an Oracle Run Book nor chooses tasks. The mapping
artifact selected during workspace initialization is the input, and the core
task-context resolver remains the authority for task codes and pillar skills.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[3]
DEFAULT_MAPPING = Path("artifacts/shared/runbook/current/identified-task-mapping.json")
RUNBOOK_ROOT = Path("artifacts/shared/runbook/current")
OFFERING_CONTEXT_CATALOG = Path("knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json")
MULTI_CONTEXT_OFFERING = "Multiple Offerings"
MULTI_CONTEXT_FUNCTIONAL_AREA = "Multiple Functional Areas"
PROJECT_STATUSES = frozenset({"initialized", "in_progress", "blocked", "ready_for_review"})

sys.path.insert(0, str(ROOT / "core" / "runbook" / "scripts"))
sys.path.insert(0, str(ROOT / "shared" / "implementation-planning" / "offering-task-map-builder" / "scripts"))
from task_context import build_task_context_from_setup_task_plan  # noqa: E402
from task_to_skill_mapping import build_task_to_skill_mapping  # noqa: E402


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Cannot read JSON artifact {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"JSON artifact must be an object: {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def pending_runbook_control() -> dict[str, Any]:
    return {
        "status": "pending",
        "active_runbook_ref": None,
        "server_url": None,
        "created_at": None,
        "failure": None,
    }


def project_root(value: str) -> Path:
    root = Path(value).resolve()
    allowed_root = (ROOT / "project").resolve()
    if root.parent != allowed_root:
        raise ValueError("--project-root must be a direct workspace under project/.")
    state = root / "state" / "project-state.json"
    if not state.is_file() or read_json(state).get("status") not in PROJECT_STATUSES:
        raise ValueError("Project workspace is missing or has not been initialized successfully.")
    return root


def mapping_path(workspace: Path, value: str | None) -> Path:
    path = (Path(value).resolve() if value else (workspace / DEFAULT_MAPPING).resolve())
    if workspace not in path.parents:
        raise ValueError("--task-mapping must be an artifact inside the specified project workspace.")
    if not path.is_file():
        raise FileNotFoundError(f"Task mapping artifact not found: {path}")
    return path


def _normalized_task_name(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Mapped task name must be non-empty text.")
    return " ".join(value.split()).casefold()


def _normalized_context_name(value: Any) -> str:
    return " ".join(value.split()).casefold() if isinstance(value, str) and value.strip() else ""


def validate_offering_contexts(mapping: dict[str, Any]) -> list[dict[str, Any]]:
    """Record unresolved offering contexts without blocking available planning work."""

    catalog = read_json(ROOT / OFFERING_CONTEXT_CATALOG)
    offerings = catalog.get("offerings")
    rows = mapping.get("tasks")
    if not isinstance(offerings, dict):
        raise ValueError("Effective offering-functional-area-task catalog must contain offerings.")
    if not isinstance(rows, list) or not rows:
        raise ValueError("Task mapping must contain a non-empty tasks array.")

    unresolved: list[dict[str, Any]] = []
    for position, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError("Task mapping contains an invalid task.")
        task_name = source_name = row.get("Source Task Name", row.get("Oracle Setup Task / Activity", row.get("task_name", row.get("task"))))
        normalized_task = _normalized_task_name(source_name)
        candidates: set[tuple[str, str]] = set()
        for offering in offerings.values():
            if not isinstance(offering, dict):
                continue
            offering_name = offering.get("offeringName")
            functional_areas = offering.get("functionalAreas")
            if not isinstance(offering_name, str) or not isinstance(functional_areas, dict):
                continue
            for functional_area in functional_areas.values():
                if not isinstance(functional_area, dict):
                    continue
                functional_area_name = functional_area.get("functionalAreaName")
                tasks = functional_area.get("tasks")
                if not isinstance(functional_area_name, str) or not isinstance(tasks, list):
                    continue
                if any(isinstance(task, dict) and _normalized_context_name(task.get("taskName")) == normalized_task for task in tasks):
                    candidates.add((offering_name, functional_area_name))

        supplied_offering = _normalized_context_name(row.get("Offering"))
        supplied_functional_area = _normalized_context_name(row.get("Functional Area"))
        matching = [
            candidate for candidate in candidates
            if candidate[0].casefold() == supplied_offering
            and candidate[1].casefold() == supplied_functional_area
        ]
        if matching:
            row["Offering Context Status"] = "matched"
            row.pop("Offering Context Candidates", None)
            continue
        options = sorted({offering_name for offering_name, _ in candidates})
        issue = {
            "sequence": position,
            "task_name": " ".join(str(source_name).split()),
            "candidate_offerings": options,
        }
        row["Offering Context Status"] = "unmatched"
        row["Offering Context Candidates"] = options
        unresolved.append(issue)
    return unresolved


def mapping_tasks(mapping: dict[str, Any]) -> list[dict[str, Any]]:
    """Consume the initializer's persisted exact-name validation result."""
    validation = mapping.get("catalog_validation")
    if not isinstance(validation, dict) or validation.get("method") != "exact-name":
        raise ValueError("Task mapping must be refreshed by the project initializer before Run Book creation.")
    rows = mapping.get("tasks")
    if not isinstance(rows, list) or not rows:
        raise ValueError("Task mapping must contain a non-empty tasks array.")
    resolver_sequences = [row.get("Resolver Sequence") for row in rows if isinstance(row, dict)]
    if len(resolver_sequences) != len(rows) or any(value is None for value in resolver_sequences):
        raise ValueError("Resolver Sequence is required for every mapping task.")
    if (
        any(isinstance(value, bool) or not isinstance(value, int) or value < 1 for value in resolver_sequences)
        or len(set(resolver_sequences)) != len(resolver_sequences)
    ):
        raise ValueError("Resolver Sequence values must be unique positive integers.")
    ordered_rows = sorted(rows, key=lambda row: row["Resolver Sequence"])
    result = []
    for sequence, row in enumerate(ordered_rows, start=1):
        if not isinstance(row, dict):
            raise ValueError("Task mapping contains an invalid task.")
        source_name = row.get("Source Task Name", row.get("Oracle Setup Task / Activity", row.get("task_name", row.get("task"))))
        _normalized_task_name(source_name)
        method = str(row.get("Match Method", "exact-name")).strip().casefold()
        status = str(row.get("Match Status", "matched")).strip().casefold()
        eligible = status == "matched" and method == "exact-name"
        offering, functional_area = row.get("Offering"), row.get("Functional Area")
        if not isinstance(offering, str) or not offering.strip():
            raise ValueError("Each selected task mapping row requires a catalog-resolved Offering.")
        if not isinstance(functional_area, str) or not functional_area.strip():
            raise ValueError("Each selected task mapping row requires a catalog-resolved Functional Area.")
        mapped_pillar = row.get("Pillar", row.get("pillar"))
        if mapped_pillar is not None and (not isinstance(mapped_pillar, str) or not mapped_pillar.strip()):
            raise ValueError("Task mapping Pillar must be non-empty text when supplied.")
        task = {"name": " ".join(str(source_name).split()), "sequence": sequence, "id": row.get("ID", row.get("id", sequence)), "phase": row.get("Phase", row.get("phase", "Unspecified")), "offering": offering.strip(), "functional_area": functional_area.strip(), "pillar": mapped_pillar.strip() if isinstance(mapped_pillar, str) else None, "match_status": status, "match_method": method, "confidence": row.get("Confidence"), "match_reason": row.get("Match Rationale"), "data_paths": row.get("Data Paths", [])}
        task["resolver_sequence"] = row["Resolver Sequence"]
        task["resolver_task_list_item_id"] = row.get("Resolver Task List Item ID")
        if not eligible:
            task["execution_mode"] = "manual"
            task["match_reason"] = task["match_reason"] or "Task match is not eligible for Run Book creation."
        result.append(task)
    return result

def catalog_task_descriptions(tasks: list[dict[str, Any]]) -> dict[int, str]:
    """Resolve notes by the selected task's full effective-catalog identity."""

    catalog = read_json(ROOT / OFFERING_CONTEXT_CATALOG)
    offerings = catalog.get("offerings")
    if not isinstance(offerings, dict):
        raise ValueError("Effective offering-functional-area-task catalog must contain offerings.")
    selected_keys = {
        (
            _normalized_context_name(task.get("offering")),
            _normalized_context_name(task.get("functional_area")),
            _normalized_context_name(task.get("task_name")),
            _normalized_context_name(task.get("task_code")),
        )
        for task in tasks
    }
    descriptions: dict[tuple[str, str, str, str], str] = {}
    for offering in offerings.values():
        if not isinstance(offering, dict):
            continue
        offering_name = _normalized_context_name(offering.get("offeringName"))
        areas = offering.get("functionalAreas")
        if not isinstance(areas, dict):
            continue
        for area in areas.values():
            if not isinstance(area, dict):
                continue
            area_name = _normalized_context_name(area.get("functionalAreaName"))
            catalog_tasks = area.get("tasks")
            if not isinstance(catalog_tasks, list):
                continue
            for catalog_task in catalog_tasks:
                if not isinstance(catalog_task, dict):
                    continue
                key = (
                    offering_name,
                    area_name,
                    _normalized_context_name(catalog_task.get("taskName")),
                    _normalized_context_name(catalog_task.get("taskShortName")),
                )
                if key not in selected_keys:
                    continue
                description = catalog_task.get("taskDescription")
                if description is not None and not isinstance(description, str):
                    raise ValueError("Effective catalog taskDescription must be text or null.")
                value = description or ""
                if key in descriptions and descriptions[key] != value:
                    raise ValueError("Effective catalog has conflicting descriptions for one task identity.")
                descriptions[key] = value
    return {
        task["sequence"]: descriptions.get((
            _normalized_context_name(task.get("offering")),
            _normalized_context_name(task.get("functional_area")),
            _normalized_context_name(task.get("task_name")),
            _normalized_context_name(task.get("task_code")),
        ), "")
        for task in tasks
    }


def build_runbook_contract_from_task_mapping(
    mapping: dict[str, Any], *, project_name: str
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Preserve the shared catalog-to-skill task-context resolution contract."""

    validate_offering_contexts(mapping)
    tasks = mapping_tasks(mapping)
    resolver_input = {
        "plan": {
            "offering": tasks[0]["offering"],
            "functional_area": tasks[0]["functional_area"],
            "tasks": [{"name": task["name"], "sequence": task["sequence"], "offering": task["offering"], "functional_area": task["functional_area"], **({"execution_mode": "manual"} if task.get("execution_mode") == "manual" else {})} for task in tasks],
        },
        "taskNotesHtml": [
            "<p>Task context resolution.</p>" for _ in tasks
        ],
    }
    setup_task_plan = build_task_to_skill_mapping(ROOT, resolver_input)
    source_by_sequence = {task["sequence"]: task for task in tasks}
    for task in setup_task_plan["tasks"]:
        source_task = source_by_sequence[task["sequence"]]
        task.update({key: source_task[key] for key in ("offering", "functional_area")})
    task_context = build_task_context_from_setup_task_plan(setup_task_plan)
    resolved = [task for task in task_context["tasks"] if isinstance(task.get("task_code"), str) and task["task_code"].strip()]
    descriptions = catalog_task_descriptions(resolved)
    for task in resolved:
        if task.get("execution_route") == "manual-tasks":
            task["task_description"] = descriptions[task["sequence"]]
    offerings = list(dict.fromkeys(task["offering"] for task in resolved))
    functional_areas = list(dict.fromkeys(task["functional_area"] for task in resolved))
    plan_offering = offerings[0] if len(offerings) == 1 else MULTI_CONTEXT_OFFERING
    plan_functional_area = (
        functional_areas[0]
        if len(functional_areas) == 1
        else MULTI_CONTEXT_FUNCTIONAL_AREA
    )
    setup_task_plan["offering"] = plan_offering
    setup_task_plan["functional_area"] = plan_functional_area
    runbook_plan = {
        "project_id": project_name,
        "offering": plan_offering,
        "functional_area": plan_functional_area,
        "sequence_status": "draft",
        "tasks": [
            {
                "task_id": task["task_code"],
                "name": task["task_name"],
                "task_description": descriptions[task["sequence"]],
                **(
                    {"pillar": source_by_sequence[task["sequence"]]["pillar"]}
                    if source_by_sequence[task["sequence"]].get("pillar")
                    else {}
                ),
                "offering": task["offering"],
                "functional_area": task["functional_area"],
                "skill_path": task.get("skill_path"),
                "business_objects": task.get("business_objects", []),
                "taskType": (
                    "ORA_CHK_MANUAL"
                    if task.get("execution_route") == "manual-tasks"
                    else "ORA_CHK_DATA_LOADER"
                    if isinstance(task.get("skill_path"), str) and task["skill_path"].strip()
                    else None
                ),
                "sequence": task["sequence"],
                "depends_on": [],
                "execution_mode": task.get("execution_mode", "assisted"),
                "load_method": "manual",
                **(
                    {
                        "execution_route": "manual-tasks",
                        "execution_skill_path": "shared/common/manual-tasks/SKILL.md",
                        "manual_task_input": {
                            "task_code": task["task_code"],
                            "task_name": task["task_name"],
                            "task_description": descriptions[task["sequence"]],
                            "offering": task["offering"],
                            "functional_area": task["functional_area"],
                            "sequence": task["sequence"],
                            "pillar": source_by_sequence[task["sequence"]].get("pillar"),
                            "skill_selection": task.get("skill_selection"),
                            "business_objects": task.get("business_objects", []),
                            "match_reason": task.get("match_reason"),
                        },
                    }
                    if task.get("execution_route") == "manual-tasks"
                    else {}
                ),
            }
            for task in resolved
        ],
        "planning_notes": [],
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "project_metadata": {
            "contexts": [
                {"offering": offering, "functional_area": functional_area}
                for offering, functional_area in dict.fromkeys(
                    (task["offering"], task["functional_area"]) for task in resolved
                )
            ],
        },
    }
    return setup_task_plan, task_context, runbook_plan


def create_runbook_from_task_mapping(
    workspace: Path,
    mapping: Path,
    *,
    dry_run: bool = False,
    refresh_artifacts: bool = False,
) -> dict[str, Any]:
    """Build and optionally persist local Run Book planning artifacts."""

    if dry_run and refresh_artifacts:
        raise ValueError("--dry-run cannot be combined with --refresh-artifacts.")
    state = read_json(workspace / "state" / "project-state.json")
    has_control = "runbook_control" in state
    root = workspace / RUNBOOK_ROOT
    setup_path = root / "setup-task-plan.json"
    context_path = root / "task-context.json"
    plan_path = root / "runbook-plan.json"
    if not dry_run and not refresh_artifacts and any(
        path.exists() for path in (setup_path, context_path, plan_path)
    ):
        raise FileExistsError(
            "Run Book planning artifacts already exist; use --refresh-artifacts "
            "to regenerate them."
        )
    project_name = state.get("project_name")
    if not isinstance(project_name, str) or not project_name.strip():
        raise ValueError("Initialized project state has no project_name.")
    mapping_payload = read_json(mapping)
    setup_task_plan, task_context, runbook_plan = build_runbook_contract_from_task_mapping(
        mapping_payload, project_name=project_name
    )
    if dry_run:
        return {"setup_task_plan": setup_task_plan, "task_context": task_context, "runbook_plan": runbook_plan}

    write_json(mapping, mapping_payload)

    write_json(setup_path, setup_task_plan)
    write_json(context_path, task_context)
    write_json(plan_path, runbook_plan)
    if not has_control:
        state["runbook_control"] = pending_runbook_control()
        write_json(workspace / "state" / "project-state.json", state)
    return {
        "setup_task_plan": setup_task_plan,
        "task_context": task_context,
        "runbook_plan": runbook_plan,
        "generated": not refresh_artifacts,
        "refreshed": refresh_artifacts,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Run Book planning artifacts for an initialized implementation project.")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--task-mapping", help="Mapping artifact within the project; defaults to the initializer-persisted mapping.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Resolve the task context and plan without writing or calling Oracle.")
    mode.add_argument(
        "--refresh-artifacts",
        action="store_true",
        help="Regenerate local planning artifacts without changing existing Run Book state; initialize pending control only when absent.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    workspace = project_root(args.project_root)
    mapping = mapping_path(workspace, args.task_mapping)
    result = create_runbook_from_task_mapping(
        workspace,
        mapping,
        dry_run=args.dry_run,
        refresh_artifacts=args.refresh_artifacts,
    )
    if args.dry_run:
        print(f"Would generate Run Book planning artifacts with {len(result['runbook_plan']['tasks'])} tasks.")
    elif args.refresh_artifacts:
        print("Refreshed local Run Book planning artifacts. No Oracle Run Book was created or updated.")
    else:
        print("Generated initial Run Book planning artifacts. No Oracle Run Book was created or updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

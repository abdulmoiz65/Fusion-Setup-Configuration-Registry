#!/usr/bin/env python3
"""Initialize a local FSCR implementation project workspace."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from token_usage_logger import append_token_usage_log, estimate_path_tokens  # noqa: E402


SKILL_ID = "core.project-mgmt.project-workspace-initializer"
STATE_VERSION = "0.1.0"
README_IGNORE_NOTICE = (
    "The repo intentionally ignores local implementation workspaces under project/, "
    "so this project exists locally but won\u2019t show as a tracked git change unless "
    "you force-add it later."
)
PHASES = {"discovery", "design", "build", "test", "deploy", "operate"}
PILLARS = {"ERP", "HCM", "SCM", "CX"}
TEMPLATE_RENAMES = {
    "project-state.template.json": "project-state.json",
    "artifact-index.template.json": "artifact-index.json",
}
IGNORED_TEMPLATE_NAMES = {".DS_Store"}
CATALOG_PATH = Path("knowledge/setup-task-catalog/effective/setupTasksAll.json")
MAX_DERIVED_PROJECT_NAME_LENGTH = 50


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    if not slug:
        raise ValueError("Project name must contain at least one alphanumeric character.")
    return slug


def validate_project_id(project_id: str) -> str:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", project_id):
        raise ValueError(
            "Project ID must use lowercase letters, numbers, and single hyphens "
            "(example: order-management-implementation)."
        )
    return project_id


def cap_project_name(value: str) -> str:
    """Cap a generated project name without splitting a word."""

    if len(value) <= MAX_DERIVED_PROJECT_NAME_LENGTH:
        return value
    truncated = value[: MAX_DERIVED_PROJECT_NAME_LENGTH - 3].rsplit(" ", 1)[0].rstrip(" ,.;:-")
    return f"{truncated}..."


def derive_project_name(implementation_objective: str) -> str:
    """Create a concise, objective-derived project name of at most 50 characters."""

    scope = re.sub(
        r"^(?:implement|deploy|configure|design)\s+(?:oracle\s+fusion(?:\s+cloud)?\s+)?",
        "",
        implementation_objective,
        flags=re.IGNORECASE,
    ).strip(" .")
    subject, separator, customer = scope.partition(" for ")
    if separator:
        customer = re.split(r"[,.;]", customer, maxsplit=1)[0].strip()
        candidate = f"{customer} {subject} Implementation"
    else:
        candidate = scope if re.search(r"\bimplementation\b", scope, flags=re.IGNORECASE) else f"{scope} Implementation"
    return cap_project_name(candidate)


def resolve_project_identity(args: argparse.Namespace, timestamp: str) -> tuple[str, str, str]:
    """Resolve a human-readable project name, workspace ID, and objective.

    An implementation objective is the canonical naming source whenever it is
    available. The draft identity is deliberately reserved for early project
    creation where no objective has been captured yet.
    """

    objective = " ".join(str(getattr(args, "implementation_objective", "") or "").split())
    supplied_name = " ".join(str(getattr(args, "project_name", "") or "").split())
    date = timestamp[:10]
    project_name = supplied_name or (derive_project_name(objective) if objective else f"Draft Implementation Project {date}")
    supplied_id = getattr(args, "project_id", None)
    project_id = (
        validate_project_id(supplied_id)
        if supplied_id
        else validate_project_id(slugify(project_name if objective else f"draft-impl-project-{date}"))
    )
    persisted_objective = objective or "Pending implementation objective"
    return project_name, project_id, persisted_objective


def parse_timestamp(value: str | None) -> str:
    if not value:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    normalized = value
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_id_from_timestamp(timestamp: str) -> str:
    compact = re.sub(r"[-:]", "", timestamp).replace("Z", "Z")
    return f"{compact}-project-workspace-initializer"


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def copy_template(template_root: Path, project_root: Path) -> None:
    for source in sorted(template_root.rglob("*")):
        if any(part in IGNORED_TEMPLATE_NAMES for part in source.relative_to(template_root).parts):
            continue

        relative = source.relative_to(template_root)
        target_name = TEMPLATE_RENAMES.get(relative.name, relative.name)
        target = project_root / relative.parent / target_name

        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def render_readme(
    *,
    project_id: str,
    project_name: str,
    customer: str,
    implementation_objective: str,
    implementation_phase: str,
) -> str:
    return f"""# {project_name}

{implementation_objective}

## Project Identity

- Project ID: `{project_id}`
- Customer: `{customer}`
- Phase: `{implementation_phase}`

## Local Workspace Notice

{README_IGNORE_NOTICE}

Do not store customer secrets, passwords, access tokens, or private keys in this workspace.
"""


def objective_payload(
    *,
    implementation_objective: str,
    customer: str,
    pillars: list[str],
    offerings: list[str],
    countries: list[str],
    industry: str,
    implementation_phase: str,
) -> dict[str, Any]:
    return {
        "$schema": "../../../../../../schemas/implementation-objective.schema.json",
        "objective": implementation_objective,
        "customer": customer,
        "pillars": pillars,
        "offerings": offerings,
        "countries": countries,
        "industry": industry,
        "implementation_phase": implementation_phase,
    }


def run_payload(
    *,
    run_id: str,
    timestamp: str,
    project_id: str,
    project_name: str,
    customer: str,
    implementation_objective: str,
    create_runbook: bool,
) -> dict[str, Any]:
    return {
        "$schema": "../../../../schemas/skill-run.schema.json",
        "run_id": run_id,
        "skill_id": SKILL_ID,
        "started_at": timestamp,
        "completed_at": timestamp,
        "status": "completed",
        "inputs": [
            f"project_id={project_id}",
            f"project_name={project_name}",
            f"customer={customer}",
            f"implementation_objective={implementation_objective}",
            f"workspace_root=project/{project_id}",
        ],
        "outputs": [
            "project_state",
            "artifact_index",
            "workspace_folder_structure",
            "objective",
            "project_readme",
            "runbook_plan" if create_runbook else "runbook_creation_deferred",
        ],
        "artifact_refs": [
            f"project/{project_id}/state/project-state.json",
            f"project/{project_id}/artifacts/artifact-index.json",
            f"project/{project_id}/artifacts/router/project-objective-classifier/current/objective.json",
            f"project/{project_id}/state/runs/{run_id}.json",
            f"project/{project_id}/README.md",
        ],
        "notes": (
            "Initialized a local implementation project workspace from project/_template. "
            + ("Run Book creation is requested; the Run Book skill must create it from the persisted plan." if create_runbook
               else "Run Book creation was deferred with --no-create-runbook.")
        ),
    }


def artifact_record(
    *,
    artifact_id: str,
    name: str,
    artifact_type: str,
    location: str,
    timestamp: str,
) -> dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "name": name,
        "artifact_type": artifact_type,
        "skill_id": SKILL_ID,
        "location": location,
        "version": "1.0.0",
        "status": "draft",
        "change_type": "initial",
        "supersedes": None,
        "checksum": None,
        "created_at": timestamp,
        "updated_at": timestamp,
    }


def normalized_task_name(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Each mapped task must contain a non-empty source task name.")
    return " ".join(value.split()).casefold()


def source_task_name(row: dict[str, Any]) -> str:
    return str(row.get("Source Task Name") or row.get("Oracle Setup Task / Activity") or row.get("task_name") or row.get("task") or "").strip()


def validate_identified_task_mapping(value: str | None, root: Path) -> dict[str, Any]:
    """Apply the single authoritative exact-name catalog validation at intake."""

    if not value:
        raise ValueError("Project initialization requires --identified-task-mapping.")
    path = Path(value).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Identified task mapping not found: {path}")
    payload = read_json(path)
    tasks = payload.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("Identified task mapping must contain a non-empty tasks array.")
    catalog = read_json(root / CATALOG_PATH).get("items")
    if not isinstance(catalog, list):
        raise ValueError("Setup-task catalog must contain an items array.")
    by_name: dict[str, list[dict[str, Any]]] = {}
    for item in catalog:
        if isinstance(item, dict):
            name = item.get("TaskName")
            if isinstance(name, str) and name.strip():
                by_name.setdefault(normalized_task_name(name), []).append(item)
    exact = unresolved = ambiguous = 0
    for row in tasks:
        if not isinstance(row, dict):
            raise ValueError("Identified task mapping contains an invalid task row.")
        name = source_task_name(row)
        key = normalized_task_name(name)
        matches = by_name.get(key, [])
        row["Source Task Name"] = name
        row["Data Paths"] = row.get("Data Paths") if isinstance(row.get("Data Paths"), list) else []
        if len(matches) == 1 and isinstance(matches[0].get("TaskCode"), str) and matches[0]["TaskCode"].strip():
            row.update({"Match Status": "matched", "Match Method": "exact-name", "Confidence": 1.0,
                        "Matched Task Code": matches[0]["TaskCode"].strip(), "Matched Task Name": matches[0]["TaskName"].strip(),
                        "Match Rationale": "Exact normalized source task name match in the current setup-task catalog."})
            exact += 1
        else:
            row.pop("Matched Task Code", None); row.pop("Matched Task Name", None)
            row["Match Status"] = "ambiguous" if len(matches) > 1 else "unmatched"
            row["Match Method"] = "exact-name"
            row["Confidence"] = None
            row["Match Rationale"] = (f"Exact normalized name matches {len(matches)} current catalog tasks; reviewer mapping is required." if matches else "No exact normalized name match exists in the current setup-task catalog.")
            ambiguous += int(len(matches) > 1); unresolved += int(not matches)
    payload["catalog_validation"] = {"method": "exact-name", "catalog": str(CATALOG_PATH).replace("\\", "/"), "matched": exact, "unmatched": unresolved, "ambiguous": ambiguous, "total": len(tasks)}
    return payload



def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def initialize_workspace(args: argparse.Namespace) -> Path:
    root = repo_root()
    template_root = root / "project" / "_template"
    timestamp = parse_timestamp(args.created_at)
    project_name, project_id, implementation_objective = resolve_project_identity(args, timestamp)
    project_root = root / "project" / project_id
    run_id = run_id_from_timestamp(timestamp)
    identified_task_mapping = validate_identified_task_mapping(getattr(args, "identified_task_mapping", None), root)

    if args.implementation_phase not in PHASES:
        allowed = ", ".join(sorted(PHASES))
        raise ValueError(f"Invalid implementation phase {args.implementation_phase!r}. Allowed: {allowed}.")
    invalid_pillars = sorted(set(args.pillar) - PILLARS)
    if invalid_pillars:
        allowed = ", ".join(sorted(PILLARS))
        raise ValueError(f"Invalid pillar value(s): {', '.join(invalid_pillars)}. Allowed: {allowed}.")
    if not template_root.exists():
        raise FileNotFoundError(f"Template folder not found: {template_root}")
    if project_root.exists() and not args.force:
        raise FileExistsError(
            f"Project workspace already exists: {project_root}. "
            "Use --force only when you intend to refresh initializer-managed files."
        )

    if not args.dry_run:
        project_root.mkdir(parents=True, exist_ok=True)
        copy_template(template_root, project_root)

        objective_path = project_root / "artifacts" / "router" / "project-objective-classifier" / "current" / "objective.json"
        run_path = project_root / "state" / "runs" / f"{run_id}.json"
        readme_path = project_root / "README.md"
        state_path = project_root / "state" / "project-state.json"
        artifact_index_path = project_root / "artifacts" / "artifact-index.json"
        mapping_path = project_root / "artifacts" / "shared" / "runbook" / "current" / "identified-task-mapping.json"
        mapping_path.parent.mkdir(parents=True, exist_ok=True)

        state = read_json(state_path)
        state.update(
            {
                "project_id": project_id,
                "project_name": project_name,
                "customer": args.customer,
                "implementation_phase": args.implementation_phase,
                "state_version": STATE_VERSION,
                "created_at": timestamp,
                "updated_at": timestamp,
                "current_objective_ref": f"project/{project_id}/artifacts/router/project-objective-classifier/current/objective.json",
                "current_scope_ref": None,
                "artifact_index_ref": f"project/{project_id}/artifacts/artifact-index.json",
                "latest_run_ref": f"project/{project_id}/state/runs/{run_id}.json",
                "baseline_refs": [],
                "decision_refs": [],
                "active_skill_path": [SKILL_ID],
                "status": "initialized",
            }
        )

        index = read_json(artifact_index_path)
        artifacts = [
            artifact_record(
                artifact_id=f"objective-{project_id}-v1",
                name=f"{project_name} Objective",
                artifact_type="objective",
                location=f"project/{project_id}/artifacts/router/project-objective-classifier/current/objective.json",
                timestamp=timestamp,
            ),
            artifact_record(
                artifact_id=f"skill-run-project-workspace-initializer-{run_id}",
                name="Project Workspace Initializer Run",
                artifact_type="skill_run",
                location=f"project/{project_id}/state/runs/{run_id}.json",
                timestamp=timestamp,
            ),
        ]
        if identified_task_mapping:
            write_json(mapping_path, identified_task_mapping)
            mapping_record = artifact_record(
                artifact_id=f"identified-task-mapping-{project_id}-v1",
                name="Identified Task Mapping",
                artifact_type="task_mapping",
                location=f"project/{project_id}/artifacts/shared/runbook/current/identified-task-mapping.json",
                timestamp=timestamp,
            )
            mapping_record["checksum"] = sha256_file(mapping_path)
            artifacts.append(mapping_record)
        index.update(
            {
                "project_id": project_id,
                "updated_at": timestamp,
                "artifacts": artifacts,
            }
        )

        write_json(state_path, state)
        write_json(artifact_index_path, index)
        write_json(
            objective_path,
            objective_payload(
                implementation_objective=implementation_objective,
                customer=args.customer,
                pillars=args.pillar,
                offerings=args.offering,
                countries=args.country,
                industry=args.industry,
                implementation_phase=args.implementation_phase,
            ),
        )
        write_json(
            run_path,
            run_payload(
                run_id=run_id,
                timestamp=timestamp,
                project_id=project_id,
                project_name=project_name,
                customer=args.customer,
                implementation_objective=implementation_objective,
                create_runbook=not getattr(args, "no_create_runbook", False),
            ),
        )
        readme_path.write_text(
            render_readme(
                project_id=project_id,
                project_name=project_name,
                customer=args.customer,
                implementation_objective=implementation_objective,
                implementation_phase=args.implementation_phase,
            ),
            encoding="utf-8",
        )
        generated_paths = [state_path, artifact_index_path, objective_path, run_path, readme_path]
        if identified_task_mapping:
            generated_paths.append(mapping_path)
        input_tokens = estimate_path_tokens(template_root / "state" / "project-state.template.json") + estimate_path_tokens(
            template_root / "artifacts" / "artifact-index.template.json"
        )
        output_tokens = sum(estimate_path_tokens(path) for path in generated_paths)
        token_log_path = append_token_usage_log(
            project_id=project_id,
            skill_id=SKILL_ID,
            task="Initialize project workspace",
            trigger="project workspace initializer",
            activity_start_time=timestamp,
            artifact_paths=generated_paths,
            files_read=2,
            estimated_input_tokens=input_tokens,
            estimated_output_tokens=output_tokens,
            notes="Default token usage row for initializer-managed workspace files.",
            root=root,
        )
        run = read_json(run_path)
        run["token_usage"] = {
            "estimation_method": "chars/4 estimate",
            "estimated_input_tokens": input_tokens,
            "estimated_output_tokens": output_tokens,
            "estimated_total_tokens": input_tokens + output_tokens,
            "artifacts_written": len(generated_paths),
            "files_read": 2,
            "log_ref": str(token_log_path.relative_to(root)),
            "notes": "Default token usage estimate for project workspace initialization.",
        }
        write_json(run_path, run)

    return project_root


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create project/{project_id} from project/_template and seed initial project state."
    )
    parser.add_argument(
        "--project-name",
        help="Optional human-readable name. Defaults to the implementation objective when one is supplied.",
    )
    parser.add_argument("--customer", required=True, help="Customer or implementation owner name.")
    parser.add_argument(
        "--implementation-objective",
        default="",
        help="Initial project objective. When present, it supplies the default project name and workspace ID.",
    )
    parser.add_argument(
        "--pillar",
        action="append",
        choices=sorted(PILLARS),
        required=True,
        help="In-scope Fusion pillar. Repeat to add multiple pillars.",
    )
    parser.add_argument(
        "--offering",
        action="append",
        default=[],
        help="In-scope Fusion offering. Repeat to add multiple offerings.",
    )
    parser.add_argument(
        "--country",
        action="append",
        default=[],
        help="In-scope country. Repeat to add multiple countries.",
    )
    parser.add_argument("--industry", default="TBD", help="Industry label for the objective artifact.")
    parser.add_argument(
        "--project-id",
        help="Workspace folder name. Defaults to a slug generated from the implementation objective; without an objective, defaults to draft-impl-project-<date>.",
    )
    parser.add_argument(
        "--implementation-phase",
        default="discovery",
        choices=sorted(PHASES),
        help="Initial implementation phase.",
    )
    parser.add_argument(
        "--created-at",
        help="UTC ISO-8601 timestamp to use for deterministic output. Defaults to current UTC time.",
    )
    parser.add_argument(
        "--identified-task-mapping",
        required=True,
        help="Required JSON task mapping persisted for project traceability and later workflow use.",
    )
    parser.add_argument(
        "--no-create-runbook",
        action="store_true",
        help="Initialize locally without requesting the default Run Book creation workflow.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow refreshing initializer-managed files in an existing workspace.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Resolve and print the project path without writing files.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        project_root = initialize_workspace(args)
    except Exception as exc:
        parser.exit(1, f"error: {exc}\n")

    action = "Would create" if args.dry_run else "Created"
    print(f"{action} project workspace: {project_root.relative_to(repo_root())}")
    if not args.dry_run:
        if args.no_create_runbook:
            print("Run Book creation deferred.")
        else:
            print("Run Book creation requested. Generate the persisted Run Book plan, then invoke core.runbook for creation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

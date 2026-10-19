#!/usr/bin/env python3
"""Reconcile Core's local Run Book artifacts with exact Goal Management routes.

This is a local planning handoff. It never creates a Fusion Run Book or calls
Fusion. Run it after create_project_runbook.py --refresh-artifacts and before
binding a plan checksum or requesting Run Book creation approval.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any

from resolve_goal_management_task_context import build_goal_management_task_context


SCRIPT_PATH = Path(__file__).resolve()
REPOSITORY_ROOT = SCRIPT_PATH.parents[6]
RUNBOOK_RELATIVE = Path("artifacts/shared/runbook/current")
GOAL_CONTEXT_RELATIVE = Path("artifacts/pillars/hcm/goal-management/current/exact-task-context.json")
AUDIT_RELATIVE = Path("artifacts/pillars/hcm/goal-management/current/runbook-route-reconciliation.json")
SKILL_ID = "hcm.goal-management"
EXACT_SELECTION = "EXACT_TASK_CODE_NAME_OFFERING_FUNCTIONAL_AREA"


class ReconciliationError(ValueError):
    """The generated local plan cannot be safely reconciled."""


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ReconciliationError(f"Cannot read {path}: {error}") from error
    if not isinstance(value, dict):
        raise ReconciliationError(f"Expected a JSON object: {path}")
    return value


def _identity(task: dict[str, Any], *, plan: bool = False) -> tuple[str, str, str, str]:
    fields = (
        task.get("task_id" if plan else "task_code"),
        task.get("name" if plan else "task_name"),
        task.get("offering"),
        task.get("functional_area"),
    )
    if any(not isinstance(value, str) or not value.strip() for value in fields):
        raise ReconciliationError("Every task requires code, name, offering, and functional area")
    return (fields[0].strip(), *(" ".join(value.split()).casefold() for value in fields[1:]))


def _indexed(tasks: Any, *, label: str, plan: bool = False) -> dict[tuple[str, str, str, str], dict[str, Any]]:
    if not isinstance(tasks, list) or not tasks:
        raise ReconciliationError(f"{label} must contain a nonempty tasks array")
    result = {}
    sequences = set()
    for task in tasks:
        if not isinstance(task, dict):
            raise ReconciliationError(f"{label} contains a non-object task")
        key = _identity(task, plan=plan)
        sequence = task.get("sequence")
        if type(sequence) is not int or sequence < 1 or sequence in sequences or key in result:
            raise ReconciliationError(f"{label} has a duplicate or invalid task identity/sequence")
        sequences.add(sequence)
        result[key] = task
    return result


def _business_objects(manifest: Path) -> list[str]:
    """Read only the generator-owned businessObject(s) frontmatter fields."""
    content = manifest.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", content, re.DOTALL)
    if not frontmatter:
        raise ReconciliationError(f"Missing manifest frontmatter: {manifest}")
    metadata = frontmatter.group(1)
    singular = re.search(r"^businessObject:\s*(.*?)\s*$", metadata, re.MULTILINE)
    plural = re.search(r"^businessObjects:\s*\r?\n((?:[ \t]+-\s+.*(?:\r?\n|\Z))+)", metadata, re.MULTILINE)
    raw_values = ([singular.group(1)] if singular else
                  re.findall(r"^[ \t]+-\s+(.+?)\s*$", plural.group(1), re.MULTILINE) if plural else [])
    values = []
    for raw in raw_values:
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            value = raw.strip().strip("\"'")
        if isinstance(value, str) and value.strip() and value.strip() not in values:
            values.append(value.strip())
    return values


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _encoded(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def _registry(root: Path, outputs: dict[Path, bytes], timestamp: str, *, update: bool) -> tuple[Path, bytes, bool]:
    index_path = root / "artifacts/artifact-index.json"
    index = _read_json(index_path)
    records = index.get("artifacts")
    if (index.get("project_id") != root.name or not isinstance(records, list)
            or any(not isinstance(row, dict) for row in records)):
        raise ReconciliationError("Project artifact index has an invalid identity or artifacts array")
    specs = {
        root / RUNBOOK_RELATIVE / "setup-task-plan.json": ("setup_task_plan", "Reconciled Setup Task Plan"),
        root / RUNBOOK_RELATIVE / "task-context.json": ("task_context", "Reconciled Run Book Task Context"),
        root / RUNBOOK_RELATIVE / "runbook-plan.json": ("runbook_plan", "Reconciled Run Book Plan"),
        root / GOAL_CONTEXT_RELATIVE: ("task_context", "Exact Goal Management Task Context"),
        root / AUDIT_RELATIVE: ("validation_result", "Goal Management Run Book Route Reconciliation"),
    }
    mapping_path = root / RUNBOOK_RELATIVE / "identified-task-mapping.json"
    checksums = {path.relative_to(REPOSITORY_ROOT).as_posix(): _sha(outputs[path]) for path in specs}
    checksums[mapping_path.relative_to(REPOSITORY_ROOT).as_posix()] = _sha(mapping_path.read_bytes())
    current = True
    for location, checksum in checksums.items():
        matches = [row for row in records if isinstance(row, dict) and row.get("location") == location]
        if len(matches) > 1:
            raise ReconciliationError(f"Duplicate artifact index location: {location}")
        if not matches or matches[0].get("checksum") != checksum:
            current = False
    if not update or current:
        return index_path, index_path.read_bytes(), current
    for path, (artifact_type, name) in specs.items():
        location = path.relative_to(REPOSITORY_ROOT).as_posix()
        match = next((row for row in records if row.get("location") == location), None)
        if match is None:
            records.append({"artifact_id": f"goal-management-{path.stem}-{root.name}-v1",
                            "name": name, "artifact_type": artifact_type, "skill_id": SKILL_ID,
                            "location": location, "version": "1.0.0", "status": "draft",
                            "change_type": "initial", "supersedes": None,
                            "checksum": checksums[location], "created_at": timestamp,
                            "updated_at": timestamp})
        else:
            match.update({"checksum": checksums[location], "updated_at": timestamp,
                          "change_type": "update"})
    mapping_location = mapping_path.relative_to(REPOSITORY_ROOT).as_posix()
    mapping_record = next((row for row in records if row.get("location") == mapping_location), None)
    if mapping_record is None:
        records.append({"artifact_id": f"identified-task-mapping-{root.name}-v1",
                        "name": "Identified Task Mapping", "artifact_type": "task_mapping",
                        "skill_id": SKILL_ID, "location": mapping_location, "version": "1.0.0",
                        "status": "draft", "change_type": "initial", "supersedes": None,
                        "checksum": checksums[mapping_location], "created_at": timestamp,
                        "updated_at": timestamp})
    elif mapping_record.get("checksum") != checksums[mapping_location]:
        mapping_record.update({"checksum": checksums[mapping_location],
                               "updated_at": timestamp, "change_type": "update"})
    index["updated_at"] = timestamp
    return index_path, _encoded(index), False


def _replace_files(changes: dict[Path, bytes]) -> None:
    """Pre-stage all local files; roll back ordinary write errors."""
    originals = {path: path.read_bytes() if path.exists() else None for path in changes}
    staged = {}
    replaced = []
    try:
        for path, data in changes.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
                handle.write(data)
                staged[path] = Path(handle.name)
        for path, temporary in staged.items():
            os.replace(temporary, path)
            replaced.append(path)
        for path, data in changes.items():
            if path.read_bytes() != data:
                raise OSError(f"Post-write verification failed for {path}")
    except OSError:
        for path in reversed(replaced):
            original = originals[path]
            if original is None:
                path.unlink(missing_ok=True)
            else:
                with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.rollback.", delete=False) as handle:
                    handle.write(original)
                    rollback = Path(handle.name)
                os.replace(rollback, path)
        raise
    finally:
        for temporary in staged.values():
            temporary.unlink(missing_ok=True)


def reconcile(project_root: Path, *, apply: bool = False) -> dict[str, Any]:
    root = project_root.resolve(strict=True)
    if root.parent != (REPOSITORY_ROOT / "project").resolve():
        raise ReconciliationError("Project root must be one direct workspace under project/")
    state = _read_json(root / "state/project-state.json")
    control = state.get("runbook_control")
    if (not isinstance(control, dict) or control.get("mode") != "required"
            or control.get("status") != "pending" or control.get("plan_sha256")
            or control.get("active_runbook_ref")
            or (root / "state/runbook/current/create-runbook-response.json").exists()):
        raise ReconciliationError("Reconciliation requires a pending, unbound initial Run Book")

    paths = {name: root / RUNBOOK_RELATIVE / name for name in (
        "identified-task-mapping.json", "setup-task-plan.json", "task-context.json", "runbook-plan.json")}
    mapping = _read_json(paths["identified-task-mapping.json"])
    validation = mapping.get("catalog_validation")
    if (not isinstance(validation, dict) or validation.get("method") != "exact-name"
            or validation.get("matched") != validation.get("total")
            or validation.get("unmatched") or validation.get("ambiguous")):
        raise ReconciliationError("Confirmed, exact-name catalog task mapping is required")
    exact = build_goal_management_task_context(mapping.get("tasks"), REPOSITORY_ROOT)
    exact_by_key = _indexed(exact["tasks"], label="exact Goal Management context")
    setup = _read_json(paths["setup-task-plan.json"])
    context = _read_json(paths["task-context.json"])
    plan = _read_json(paths["runbook-plan.json"])
    if setup.get("schema_version") != "1.0" or context.get("schema_version") != "1.0":
        raise ReconciliationError("Unsupported Core planning artifact schema")
    setup_by_key = _indexed(setup.get("tasks"), label="setup-task-plan")
    context_by_key = _indexed(context.get("tasks"), label="task-context")
    plan_by_key = _indexed(plan.get("tasks"), label="runbook-plan", plan=True)
    if not (exact_by_key.keys() == setup_by_key.keys() == context_by_key.keys() == plan_by_key.keys()):
        raise ReconciliationError("Generated task set differs from exact Goal Management task context")

    output = {"setup-task-plan.json": deepcopy(setup), "task-context.json": deepcopy(context),
              "runbook-plan.json": deepcopy(plan)}
    output_indexes = {
        "setup-task-plan.json": _indexed(output["setup-task-plan.json"]["tasks"], label="setup-task-plan"),
        "task-context.json": _indexed(output["task-context.json"]["tasks"], label="task-context"),
        "runbook-plan.json": _indexed(output["runbook-plan.json"]["tasks"], label="runbook-plan", plan=True),
    }
    reconciled_tasks = []
    for key, exact_task in exact_by_key.items():
        rows = [setup_by_key[key], context_by_key[key], plan_by_key[key]]
        if len({row["sequence"] for row in rows}) != 1:
            raise ReconciliationError(f"Sequence drift for {key}")
        if any(row.get("match_status") != "matched" for row in rows[:2]):
            raise ReconciliationError(f"Unmatched generated task: {key}")
        old_paths = [row.get("skill_path") for row in rows]
        if len(set(old_paths)) != 1:
            raise ReconciliationError(f"Conflicting generated skill paths for {key}")
        old_objects = [row.get("business_objects") for row in rows]
        if any(not isinstance(value, list) for value in old_objects) or not all(value == old_objects[0] for value in old_objects):
            raise ReconciliationError(f"Conflicting business object metadata for {key}")
        selection = rows[0].get("skill_selection")
        if selection != rows[1].get("skill_selection") or not isinstance(selection, dict):
            raise ReconciliationError(f"Conflicting generated selection evidence for {key}")
        expected_path = exact_task["skill_path"]
        if (selection.get("status") != "selected" or
                old_paths[0] not in selection.get("candidates", []) or
                expected_path not in selection.get("candidates", [])):
            raise ReconciliationError(f"Exact route is absent from generated candidate evidence for {key}")
        if old_paths[0] != expected_path and selection.get("selected_by") != "LEXICOGRAPHIC_PATH":
            raise ReconciliationError(f"Non-lexical route mismatch for {key}")
        new_objects = _business_objects(REPOSITORY_ROOT / expected_path)
        new_selection = exact_task["skill_selection"]
        for artifact_name, artifact_rows in output_indexes.items():
            row = artifact_rows[key]
            row["skill_path"] = expected_path
            row["business_objects"] = new_objects
            if artifact_name != "runbook-plan.json":
                row["skill_selection"] = deepcopy(new_selection)
        if old_paths[0] != expected_path or selection != new_selection or old_objects[0] != new_objects:
            reconciled_tasks.append({"task_code": key[0], "functional_area": exact_task["functional_area"],
                                     "before": old_paths[0], "after": expected_path})

    updates = {paths[name]: _encoded(value) for name, value in output.items()}
    exact_path = root / GOAL_CONTEXT_RELATIVE
    updates[exact_path] = _encoded(exact)
    before = {name: _sha(paths[name].read_bytes()) for name in output}
    after = {name: _sha(updates[paths[name]]) for name in output}
    result = {"status": "reconciliation_needed" if reconciled_tasks else "already_exact", "project_id": root.name,
              "reconciled_tasks": reconciled_tasks, "before_sha256": before, "after_sha256": after,
              "exact_context": str(exact_path.relative_to(REPOSITORY_ROOT)),
              "oracle_requests": 0}
    if apply:
        audit_path = root / AUDIT_RELATIVE
        mapping_sha = _sha(paths["identified-task-mapping.json"].read_bytes())
        timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        audit = {**result, "status": "completed", "stage": "local_runbook_route_reconciliation",
                 "timestamp": timestamp, "mapping_sha256": mapping_sha}
        updates[audit_path] = _encoded(audit)
        registry_probe = dict(updates)
        if audit_path.is_file():
            registry_probe[audit_path] = audit_path.read_bytes()
        _, _, registry_current = _registry(root, registry_probe, timestamp, update=False)
        if not reconciled_tasks and exact_path.is_file() and audit_path.is_file():
            previous_audit = _read_json(audit_path)
            if (exact_path.read_bytes() == updates[exact_path]
                    and previous_audit.get("mapping_sha256") == mapping_sha
                    and previous_audit.get("after_sha256") == after):
                if not registry_current:
                    index_path, index_bytes, _ = _registry(root, registry_probe, timestamp, update=True)
                    _replace_files({index_path: index_bytes})
                result["audit"] = str(audit_path.relative_to(REPOSITORY_ROOT))
                return result
        index_path, index_bytes, _ = _registry(root, updates, timestamp, update=True)
        updates[index_path] = index_bytes
        _replace_files(updates)
        result["status"] = "reconciled" if reconciled_tasks else "already_exact"
        result["audit"] = str(audit_path.relative_to(REPOSITORY_ROOT))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--apply", action="store_true", help="Persist the reconciled local artifacts")
    args = parser.parse_args()
    try:
        result = reconcile(args.project_root, apply=args.apply)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

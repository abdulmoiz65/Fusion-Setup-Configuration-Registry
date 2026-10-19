"""Synchronize execution contexts from the authoritative Touchpoints task plan.

The legacy command name is retained for existing projects. All selected mapped
Data Loader/ESS tasks are synchronized; REST/manual tasks receive owner handoffs.
No Oracle Run Book or initial creation payload is changed by this local step.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "core/runbook/scripts"))
sys.path.insert(0, str(ROOT / "shared/implementation-planning/offering-task-map-builder/scripts"))
from task_context import build_task_context_from_setup_task_plan  # noqa: E402
from task_to_skill_mapping import build_task_to_skill_mapping  # noqa: E402
from touchpoints_runbook import build  # noqa: E402

CONTEXT = Path("artifacts/shared/runbook/current/task-context.json")
CURRENT = Path("artifacts/pillars/hcm/hcm-tool/touchpoints-aggregate-data-process/current")
STATE = CURRENT / "touchpoints-workflow-state.json"
SNAPSHOT = CURRENT / "runbook-task-snapshot.json"
PROVENANCE = CURRENT / "task-context-provenance.json"


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def resolve_identity(identity, sequence):
    fields = ("task_code", "task_name", "offering", "functional_area")
    if not isinstance(identity, dict) or any(not isinstance(identity.get(k), str) or not identity[k].strip() for k in fields):
        raise ValueError("Mapped owner route requires exact catalog identity")
    source = {"plan": {"offering": identity["offering"], "functional_area": identity["functional_area"],
                       "tasks": [{"name": identity["task_name"], "sequence": sequence}]},
              "taskNotesHtml": ["<p>Verified Touchpoints owner task context.</p>"]}
    mapping = build_task_to_skill_mapping(ROOT, source)
    for task in mapping["tasks"]:
        task.update({k: identity[k] for k in ("offering", "functional_area")})
    tasks = build_task_context_from_setup_task_plan(mapping)["tasks"]
    if len(tasks) != 1 or tasks[0].get("task_code") != identity["task_code"] or not tasks[0].get("skill_path"):
        raise ValueError("Owner task did not resolve to the exact catalog identity and skill")
    return tasks[0]


def build_synced_artifacts(project: Path):
    control = read_json(project / "state/project-state.json").get("runbook_control", {})
    state = read_json(project / STATE)
    snapshot = read_json(project / SNAPSHOT)
    if state.get("run_status") in ("stopped", "paused", "abandoned"):
        raise ValueError("Run stopped; context synchronization requires an explicit resume")
    journey = state.get("runbook", {}).get("journey_id")
    if control.get("status") != "active" or str(control.get("active_runbook_ref")) != journey:
        raise ValueError("Active project and Touchpoints Run Book bindings must agree")
    plan = build(state, snapshot)
    if not plan["runbook_complete"]:
        raise ValueError("Reconcile the complete selected Run Book before context synchronization")
    current = read_json(project / CONTEXT)
    if current.get("schema_version") != "1.0" or not isinstance(current.get("tasks"), list):
        raise ValueError("Generated project task context is invalid")
    bindings = state["runbook"]["bindings"]
    generated, evidence, handoffs = [], [], []
    for row in plan["tasks"]:
        key = row["key"]
        binding = bindings[key]
        handoffs.append({"key": key, "display_name": row["name"], "owner_skill_id": row.get("owner_skill_id"),
                         "execution_route": row["execution_route"], "catalog_identity": row.get("catalog_identity"),
                         "depends_on": row["depends_on"], "sequence": row["runbook_sequence"],
                         "runbook_binding": binding, "requirements": row["requirements"],
                         "technical_evidence_owner": "executing_agent", "write_authorized": False})
        if key == "feedback":
            handoffs[-1]["parent_skill_id"] = "hcm.performance-management.requested-feedback-template"
            handoffs[-1]["mandatory_profile_baseline"] = plan["feedback_profile_baseline"]
            handoffs[-1]["refresh_profile_evidence_before_template_write"] = True
        if row["execution_route"] == "ess":
            handoffs[-1]["operation_intent"] = "daily_incremental_schedule" if key == "daily" else "implementation_full" if plan["scope"]["mode"] == "implementation" or "daily" in plan["scope"]["selected_tasks"] else "standalone_run"
            handoffs[-1]["coordination_module"] = "scripts/touchpoints_ess_handoff.py"
            handoffs[-1]["core_dependency"] = "core.fusion-api.ess-job-submitter"
            handoffs[-1]["requires_verified_full_success"] = key == "daily"
        if row["execution_route"] not in ("data-loader", "ess"):
            continue
        if row["execution_route"] == "ess" and not row.get("catalog_identity"):
            continue  # Scheduling handoff uses the existing ESS owner and manual row.
        entry = resolve_identity(row.get("catalog_identity"), row["runbook_sequence"])
        generated.append(entry)
        evidence.append({"key": key, "task_id": binding["task_id"], "parent_id": binding["parent_id"],
                         "task_code": entry["task_code"], "sequence": entry["sequence"],
                         "snapshot_captured_at": snapshot["captured_at"]})
    names = {r["task_name"] for r in generated}
    for entry in generated:
        existing = [r for r in current["tasks"] if r.get("task_name") == entry["task_name"]]
        if len(existing) > 1 or any(r.get("task_code") != entry["task_code"] for r in existing):
            raise ValueError("Existing generated task identity conflicts with the selected catalog task")
    old_evidence = read_json(project / PROVENANCE).get("tasks", []) if (project / PROVENANCE).exists() else []
    old_keys = {r["key"] for r in old_evidence}
    # A scope change is governed by approved_scope. Existing owned entries may be
    # replaced only after their selected Run Book bindings have been reconciled.
    if old_keys - {r["key"] for r in evidence}:
        raise ValueError("Previously synchronized task removed; reconcile the explicit scope amendment")
    for previous in old_evidence:
        matches = [r for r in evidence if r["key"] == previous["key"]]
        if len(matches) != 1 or any(matches[0][k] != previous[k] for k in ("task_id", "parent_id", "task_code")):
            raise ValueError("Synchronized Run Book task identity changed; reconcile before replacement")
    others = [r for r in current["tasks"] if r.get("task_name") not in names]
    sequences = [r["sequence"] for r in others + generated]
    if len(sequences) != len(set(sequences)):
        raise ValueError("Owner sequence collides with an unrelated generated context entry")
    context = {**current, "tasks": sorted(others + generated, key=lambda r: r["sequence"])}
    provenance = {"project_id": state["project_id"], "environment": state["environment"],
                  "configuration_revision": state["configuration_revision"], "runbook_id": journey,
                  "tasks": evidence}
    return context, provenance, {**provenance, "tasks": handoffs}


def build_synced_context(project: Path):
    """Compatibility wrapper for the original Check-In helper."""
    context, provenance, _ = build_synced_artifacts(project)
    return context, provenance


def sync_project_context(project: Path, dry_run=False):
    context, provenance, handoffs = build_synced_artifacts(project)
    if not dry_run:
        # Persist provenance first. A partial local persistence can be regenerated
        # from the same verified plan; no external write occurs here.
        for relative, value in ((PROVENANCE, provenance), (CURRENT / "owner-handoffs.json", handoffs), (CONTEXT, context)):
            path = project / relative
            temporary = path.with_suffix(".json.tmp")
            temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
            temporary.replace(path)
    return {"context": str(project / CONTEXT), "tasks": provenance["tasks"],
            "owner_handoffs": str(project / CURRENT / "owner-handoffs.json"), "dry_run": dry_run}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    project = Path(args.project_root).resolve(strict=True)
    if project.parent != (ROOT / "project").resolve():
        raise ValueError("Project root must be a direct workspace under project/")
    print(json.dumps(sync_project_context(project, args.dry_run)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

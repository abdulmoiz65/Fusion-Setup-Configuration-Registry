"""One local entry point for Touchpoints planning, context sync and next task.

Owner skills perform live operations with their own preflight and approvals.
This command never calls Fusion and never resumes a stopped implementation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from touchpoints_runbook import build
from sync_checkin_task_context import (
    ROOT, STATE, SNAPSHOT, CONTEXT, CURRENT, build_synced_artifacts, sync_project_context,
)


def orchestrate(project, sync=False):
    state = json.loads((project / STATE).read_text())
    snapshot = json.loads((project / SNAPSHOT).read_text()) if (project / SNAPSHOT).exists() else None
    plan = build(state, snapshot)
    if state.get("run_status") in ("stopped", "paused", "abandoned"):
        return {"plan": plan, "context_status": "stopped"}
    if not plan["runbook_complete"]:
        return {"plan": plan, "context_status": "awaiting_runbook_provisioning"}
    context, _, handoffs = build_synced_artifacts(project)
    current = json.loads((project / CONTEXT).read_text())
    path = project / CURRENT / "owner-handoffs.json"
    synced = context == current and path.exists() and json.loads(path.read_text()) == handoffs
    if sync:
        sync_project_context(project)
        synced = True
    if not synced:
        plan["execution"].update(next_task=None, independent_ready_tasks=[], run_state="synchronize_context")
    return {"plan": plan, "context_status": "synchronized" if synced else "repair_required",
            "next_action": "Execute the next task through its owning skill" if synced else
                           "Run this entry point with --sync-context to reconcile local owner contexts"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--sync-context", action="store_true", help="Synchronize local contexts; no Fusion operations")
    args = parser.parse_args()
    project = Path(args.project_root).resolve(strict=True)
    if project.parent != (ROOT / "project").resolve():
        raise ValueError("Project root must be a direct workspace under project/")
    try:
        result = orchestrate(project, args.sync_context)
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({"status": "technical_failure", "user_action_required": False,
                          "stage": "local_context_reconciliation", "message": str(error)}))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

---
skill_id: "core.project-mgmt.project-state-manager"
name: "Project State Manager"
description: "Reads and updates the durable project state used to resume Fusion implementation workflows across sessions."
layer: "core"
pillar: "Core"
type: "import"
execution_mode: "hybrid"
owner_team: "Central platform team"
version: "0.1.0"
inputs:
  - "project_state"
  - "state_update"
  - "skill_run"
outputs:
  - "updated_project_state"
  - "state_change_summary"
depends_on:
  - "core.project-mgmt.artifact-registry-manager"
uses_core: []
persists_project_state: true
state_updates:
  - "objective"
  - "requirements"
  - "scope"
  - "skill_path"
  - "setup_task_sequence"
  - "design_decisions"
  - "configuration_blueprints"
  - "exports"
  - "baselines"
  - "validation_results"
  - "reports"
workspace_outputs:
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Updates local project state after user-approved workflow changes."
required_privileges: []
---

# Project State Manager

## Purpose

Reads and updates the durable project state used to resume Fusion implementation workflows across sessions.

## When to Use

Use this skill whenever a router, shared, core, or pillar skill produces output that changes the current implementation objective, scope, sequence, baseline, decision, blueprint, validation, or report state.

## Inputs

- `project_state`
- `state_update`
- `skill_run`

## Outputs

- `updated_project_state`
- `state_change_summary`

## Implementation Notes

State updates must be deterministic and auditable. Record the skill run reference that caused each state transition so a future session can reconstruct how the project reached its current state.

Any activity that creates or updates files under `project/{project_id}` must log
token usage by default at:

```text
project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md
```

Use `core/project-mgmt/scripts/token_usage_logger.py` for repository scripts and
include the same estimate in the skill-run record when one is written. Estimates
are operational planning values, not billing-grade counts. Exclude secrets,
token-cache contents, and credential properties from token estimates.

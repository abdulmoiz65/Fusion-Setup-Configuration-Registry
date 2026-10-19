---
skill_id: "shared.project-intake.scope-definition"
name: "Scope Definition"
description: "Defines and persists the confirmed implementation scope across pillars, offerings, functional areas, countries, integrations, and delivery phases."
layer: "shared"
pillar: "Common"
type: "assessment"
execution_mode: "assisted"
owner_team: "Shared enablement team with pillar review"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "business_requirements"
  - "project_context"
  - "objective_classification"
outputs:
  - "confirmed_scope"
  - "scope_assumptions"
  - "scope_exclusions"
  - "project_state_update"
  - "token_usage_record"
depends_on:
  - "router.project-objective-classifier"
uses_core:
  - "core.project-mgmt.project-state-manager"
  - "core.project-mgmt.artifact-registry-manager"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
state_updates:
  - "scope"
  - "requirements"
workspace_outputs:
  - artifact_type: "scope"
    default_location: "project/{project_id}/artifacts/shared/project-intake/scope-definition/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "requirement"
    default_location: "project/{project_id}/artifacts/shared/project-intake/scope-definition/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Updates local project state with confirmed implementation scope."
required_privileges: []
---

# Scope Definition

## Purpose

Defines and persists the confirmed implementation scope across pillars, offerings, functional areas, countries, integrations, and delivery phases.

## When to Use

Use this skill after objective classification and initial intake, before setup task planning or pillar-specific implementation guidance begins.

## Inputs

- `implementation_objective`
- `business_requirements`
- `project_context`
- `objective_classification`

## Outputs

- `confirmed_scope`
- `scope_assumptions`
- `scope_exclusions`
- `project_state_update`

## Implementation Notes

Persist the confirmed scope under `project/{project_id}/artifacts/shared/project-intake/scope-definition/` and update `project/{project_id}/state/project-state.json` so downstream planning and pillar skills can resolve the same scope across sessions.

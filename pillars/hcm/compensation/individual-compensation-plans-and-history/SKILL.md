---
skill_id: "hcm.compensation.individual-compensation-plans-and-history"
name: "Individual Compensation Plans and History Implementation Guidance"
description: "Provides HCM Compensation implementation guidance for the Individual Compensation Plans and History functional area."
layer: "pillar"
pillar: "HCM"
offering: "Compensation"
functional_area: "Individual Compensation Plans and History"
functional_area_code: "ORA_INDIVIDUAL_COMPENSATION_PLANS_AND_HISTORY"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM compensation pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "individual_compensation_plans_and_history_scope"
  - "individual_compensation_plans_and_history_requirements"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
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
  - "setup_task_sequence"
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/individual-compensation-plans-and-history/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/individual-compensation-plans-and-history/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/compensation/individual-compensation-plans-and-history/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "CMP_MANAGE_INDIVIDUAL_COMPENSATION_PLANS"
  - "CMP_MANAGE_COMPENSATION_HISTORY"
  - "ORA_CMP_MAP_THIRD_PARTY_COMPENSATION_PLANS"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects: []
required_privileges: []
---

# Individual Compensation Plans and History Implementation Guidance

## Purpose

Provides HCM Compensation implementation guidance for the Individual Compensation Plans and History functional area.

## When to Use

Use this functional-area skill after Compensation scope is confirmed and the project needs individual compensation plans and history setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Compensation` (`ORA_COMPENSATION`)
- Functional area / Setup Object: `Individual Compensation Plans and History` (`ORA_INDIVIDUAL_COMPENSATION_PLANS_AND_HISTORY`)

## Setup Tasks

1. [Individual Compensation Plans](individual-compensation-plans/SKILL.md) (`CMP_MANAGE_INDIVIDUAL_COMPENSATION_PLANS`)
2. [Configure Compensation History](configure-compensation-history/SKILL.md) (`CMP_MANAGE_COMPENSATION_HISTORY`)
3. [Map Third-Party Compensation Plans](map-third-party-compensation-plans/SKILL.md) (`ORA_CMP_MAP_THIRD_PARTY_COMPENSATION_PLANS`)

## Inputs

- `implementation_objective`
- `project_context`
- `individual_compensation_plans_and_history_scope`
- `individual_compensation_plans_and_history_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.

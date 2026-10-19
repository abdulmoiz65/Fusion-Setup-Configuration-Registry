---
skill_id: "hcm.goal-management.goal-plan"
name: "Goal Plan Implementation Guidance"
description: "Provides HCM Goal Management implementation guidance for the Goal Plan functional area."
layer: "pillar"
pillar: "HCM"
offering: "Goal Management"
functional_area: "Goal Plan"
functional_area_code: "ORA_GOAL_PLAN"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM goal management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "goal_plan_scope"
  - "goal_plan_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-plan/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-plan/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/goal-management/goal-plan/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "HRG_MANAGE_GOAL_PLANS"
  - "HRG_MANAGE_WORKFORCE_GOALS_DESCRIPTIVE_FLEXFIELD"
  - "HRG_MANAGE_WORKER_GOAL_SETTING_PROFILE_OPTIONS"
  - "HRG_MANAGE_GOALS_VALUE_SETS"
  - "HRG_MANAGE_WORKER_GOAL_SETTING_LOOKUPS"
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

# Goal Plan Implementation Guidance

## Purpose

Provides HCM Goal Management implementation guidance for the Goal Plan functional area.

## When to Use

Use this functional-area skill after Goal Management scope is confirmed and the project needs goal plan setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Goal Management` (`ORA_GOAL_MANAGEMENT`)
- Functional area / Setup Object: `Goal Plan` (`ORA_GOAL_PLAN`)

## Setup Tasks

1. [Goal Plans](goal-plans/SKILL.md) (`HRG_MANAGE_GOAL_PLANS`)
2. [Worker Goal Descriptive Flexfields](worker-goal-descriptive-flexfields/SKILL.md) (`HRG_MANAGE_WORKFORCE_GOALS_DESCRIPTIVE_FLEXFIELD`)
3. [Worker Goal Setting Profile Option Values](worker-goal-setting-profile-option-values/SKILL.md) (`HRG_MANAGE_WORKER_GOAL_SETTING_PROFILE_OPTIONS`)
4. [Goals Value Sets](goals-value-sets/SKILL.md) (`HRG_MANAGE_GOALS_VALUE_SETS`)
5. [Worker Goal Setting Lookups](worker-goal-setting-lookups/SKILL.md) (`HRG_MANAGE_WORKER_GOAL_SETTING_LOOKUPS`)

## Inputs

- `implementation_objective`
- `project_context`
- `goal_plan_scope`
- `goal_plan_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.

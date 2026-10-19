---
skill_id: "cx.service.action-plans"
name: "Action Plans Implementation Guidance"
description: "Provides CX Service implementation guidance for the Action Plans functional area."
layer: "pillar"
pillar: "CX"
offering: "Service"
functional_area: "Action Plans"
functional_area_code: "ORA_SVC_ACTION_PLANS"
type: "planning"
execution_mode: "assisted"
owner_team: "CX service pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "action_plans_scope"
  - "action_plans_requirements"
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
  - "core.auth.fusion-oauth-authentication"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.apps-common.lookups"
  - "core.fusion-api.apps-common.profile-options"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/service/action-plans/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/service/action-plans/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/service/action-plans/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_SVC_MANAGE_ACTION_PLAN_PROFILE_OPTIONS"
  - "ORA_SVC_MANAGE_ACTION_CATEGORIES_FOR_ACTION_PLANS"
  - "ORA_SVC_MANAGE_TEMPLATE_CATEGORIES_FOR_ACTION_PLANS"
  - "ORA_SVC_MANAGE_ACTION_PLAN_ACTION_STATUS_MAPPING"
  - "ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS"
  - "ORA_SVC_MANAGE_ACTION_PLAN_TEMPLATES"
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

# Action Plans Implementation Guidance

## Purpose

Provides CX Service implementation guidance for the Action Plans functional area.

## When to Use

Use this functional-area skill after Service scope is confirmed and the project needs action plans setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Service` (`ORA_SVC`)
- Functional area / Setup Object: `Action Plans` (`ORA_SVC_ACTION_PLANS`)

## Setup Tasks

1. [Manage Action Plan Profile Options](manage-action-plan-profile-options.md) (`ORA_SVC_MANAGE_ACTION_PLAN_PROFILE_OPTIONS`)
2. [Manage Action Categories for Action Plans](manage-action-categories-for-action-plans.md) (`ORA_SVC_MANAGE_ACTION_CATEGORIES_FOR_ACTION_PLANS`)
3. [Manage Template Categories for Action Plans](manage-template-categories-for-action-plans.md) (`ORA_SVC_MANAGE_TEMPLATE_CATEGORIES_FOR_ACTION_PLANS`)
4. [Manage Mapping of Action Plan Status Values](manage-mapping-of-action-plan-status-values.md) (`ORA_SVC_MANAGE_ACTION_PLAN_ACTION_STATUS_MAPPING`)
5. [Manage Action Plan Actions](manage-action-plan-actions.md) (`ORA_SVC_MANAGE_ACTION_PLAN_ACTIONS`)
6. [Manage Action Plan Templates](manage-action-plan-templates.md) (`ORA_SVC_MANAGE_ACTION_PLAN_TEMPLATES`)

## Inputs

- `implementation_objective`
- `project_context`
- `action_plans_scope`
- `action_plans_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.

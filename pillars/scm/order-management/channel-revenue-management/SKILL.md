---
skill_id: "scm.order-management.channel-revenue-management"
name: "Channel Revenue Management Implementation Guidance"
description: "Provides SCM Order Management implementation guidance for the Channel Revenue Management functional area."
layer: "pillar"
pillar: "SCM"
offering: "Order Management"
functional_area: "Channel Revenue Management"
functional_area_code: "ORA_FOM_CHANNEL_REV_MGMT"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM order management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "channel_revenue_management_scope"
  - "channel_revenue_management_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/channel-revenue-management/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/channel-revenue-management/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/channel-revenue-management/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_CJM_MANAGE_CHANNEL_USER_STATUSES"
  - "ORA_CJM_MANAGE_ADJ_TYPES"
  - "ORA_CJM_MANAGE_CHANNEL_LOOKUPS"
  - "ORA_CJM_MANAGE_CHANNEL_PROFILE_OPTIONS"
  - "ORA_CJM_MANAGE_CLAIM_REASONS"
  - "ORA_CJM_MANAGE_CLAIM_TYPES"
  - "ORA_CJM_MANAGE_CLAIM_SOURCES"
  - "ORA_CJM_MANAGE_CHANNEL_DESCRIPTIVE_FLEXFIELDS"
  - "ORA_CJM_MANAGE_CHANNEL_VALUE_SETS"
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

# Channel Revenue Management Implementation Guidance

## Purpose

Provides SCM Order Management implementation guidance for the Channel Revenue Management functional area.

## When to Use

Use this functional-area skill after Order Management scope is confirmed and the project needs channel revenue management setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `SCM`
- Offering: `Order Management` (`DOO_ORCHESTRATION`)
- Functional area / Setup Object: `Channel Revenue Management` (`ORA_FOM_CHANNEL_REV_MGMT`)

## Setup Tasks

1. [Manage Channel User Statuses](manage-channel-user-statuses.md) (`ORA_CJM_MANAGE_CHANNEL_USER_STATUSES`)
2. [Manage Channel Adjustment Types](manage-channel-adjustment-types.md) (`ORA_CJM_MANAGE_ADJ_TYPES`)
3. [Manage Channel Lookups](manage-channel-lookups.md) (`ORA_CJM_MANAGE_CHANNEL_LOOKUPS`)
4. [Manage Channel Profile Options](manage-channel-profile-options.md) (`ORA_CJM_MANAGE_CHANNEL_PROFILE_OPTIONS`)
5. [Manage Channel Claim Reasons](manage-channel-claim-reasons/SKILL.md) (`ORA_CJM_MANAGE_CLAIM_REASONS`)
6. [Manage Channel Claim Types](manage-channel-claim-types/SKILL.md) (`ORA_CJM_MANAGE_CLAIM_TYPES`)
7. [Manage Channel Claim Sources](manage-channel-claim-sources/SKILL.md) (`ORA_CJM_MANAGE_CLAIM_SOURCES`)
8. [Manage Channel Descriptive Flexfields](manage-channel-descriptive-flexfields.md) (`ORA_CJM_MANAGE_CHANNEL_DESCRIPTIVE_FLEXFIELDS`)
9. [Manage Channel Value Sets](manage-channel-value-sets.md) (`ORA_CJM_MANAGE_CHANNEL_VALUE_SETS`)

## Inputs

- `implementation_objective`
- `project_context`
- `channel_revenue_management_scope`
- `channel_revenue_management_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated flat setup-task metadata for task-level planning, setup-data routing, and validation. Task-specific authored rules are stored in the functional-area `ora-resource/` folder and scoped by task code and task name. Track token usage for any generated project artifact or skill-run record using the manifest policy.

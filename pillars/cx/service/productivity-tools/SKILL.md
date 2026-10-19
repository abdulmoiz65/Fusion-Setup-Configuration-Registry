---
skill_id: "cx.service.productivity-tools"
name: "Productivity Tools Implementation Guidance"
description: "Provides CX Service implementation guidance for the Productivity Tools functional area."
layer: "pillar"
pillar: "CX"
offering: "Service"
functional_area: "Productivity Tools"
functional_area_code: "ORA_SVC_PRODUCTIVITY"
type: "planning"
execution_mode: "assisted"
owner_team: "CX service pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "productivity_tools_scope"
  - "productivity_tools_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/service/productivity-tools/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/service/productivity-tools/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/service/productivity-tools/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_SVC_MANAGE_SEARCH_OPTIONS"
  - "ORA_SVC_MANAGE_STANDARD_TEXT_PROFILE_OPTS"
  - "ORA_SVC_MANAGE_SERVICE_REQUEST_DYNAMIC_LINKS"
  - "ORA_SVC_MANAGE_TAGS"
  - "ORA_CONFIGURE_ACTION_BAR_PARAMETERS"
  - "ORA_SVC_MANAGE_NOTE_TYPES"
  - "ORA_MANAGE_SERVICE_REQUEST_MESSAGE_TYPES_AND_SUBTYPES"
  - "ORA_SVC_MANAGE_PASSIVE_BEACON_CONFIGURATION"
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

# Productivity Tools Implementation Guidance

## Purpose

Provides CX Service implementation guidance for the Productivity Tools functional area.

## When to Use

Use this functional-area skill after Service scope is confirmed and the project needs productivity tools setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Service` (`ORA_SVC`)
- Functional area / Setup Object: `Productivity Tools` (`ORA_SVC_PRODUCTIVITY`)

## Setup Tasks

1. [Manage Global Search Profile Options](manage-global-search-profile-options.md) (`ORA_SVC_MANAGE_SEARCH_OPTIONS`)
2. [Manage Standard Text Profile Options](manage-standard-text-profile-options.md) (`ORA_SVC_MANAGE_STANDARD_TEXT_PROFILE_OPTS`)
3. [Manage Service Request Dynamic Links](manage-service-request-dynamic-links.md) (`ORA_SVC_MANAGE_SERVICE_REQUEST_DYNAMIC_LINKS`)
4. [Manage Tags](manage-tags.md) (`ORA_SVC_MANAGE_TAGS`)
5. [Configure Action Bar Parameters](configure-action-bar-parameters.md) (`ORA_CONFIGURE_ACTION_BAR_PARAMETERS`)
6. [Manage Note Types](manage-note-types.md) (`ORA_SVC_MANAGE_NOTE_TYPES`)
7. [Manage Service Request Message Types and Subtypes](manage-service-request-message-types-and-subtypes.md) (`ORA_MANAGE_SERVICE_REQUEST_MESSAGE_TYPES_AND_SUBTYPES`)
8. [Manage Passive Beacon Configuration](manage-passive-beacon-configuration.md) (`ORA_SVC_MANAGE_PASSIVE_BEACON_CONFIGURATION`)

## Inputs

- `implementation_objective`
- `project_context`
- `productivity_tools_scope`
- `productivity_tools_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.

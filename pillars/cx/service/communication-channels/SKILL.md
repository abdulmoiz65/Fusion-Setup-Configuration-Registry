---
skill_id: "cx.service.communication-channels"
name: "Communication Channels Implementation Guidance"
description: "Provides CX Service implementation guidance for the Communication Channels functional area."
layer: "pillar"
pillar: "CX"
offering: "Service"
functional_area: "Communication Channels"
functional_area_code: "ORA_SVC_COMM_CHANNELS"
type: "planning"
execution_mode: "assisted"
owner_team: "CX service pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "communication_channels_scope"
  - "communication_channels_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/service/communication-channels/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/service/communication-channels/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/service/communication-channels/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_SVC_MANAGE_COMM_CHANNELS"
  - "ORA_SVC_MANAGE_INBOUND_EMAIL_PROFILE_OPTS"
  - "ORA_SVC_MANAGE_OUTBOUND_EMAIL_PROFILE_OPTS"
  - "ORA_SVC_MANAGE_EMAIL_FILTERS"
  - "ORA_SVC_MANAGE_OMNI_CHANNEL_PROFILE_OPTS"
  - "ORA_MANAGE_MCA_PROFILE_OPTIONS"
  - "ORA_SVC_MANAGE_SERVICE_REQUEST_ASSIGNMENT_OBJECTS"
  - "ORA_SVC_MANAGE_SERVICE_ZONES"
  - "ORA_SVC_MANAGE_SERVICE_REQUEST_ASSIGNMENT_RULES"
  - "ORA_SVC_INTERACTION_PROFILE_OPTIONS"
  - "ORA_MANAGE_EMAIL_PROFILE_OPTIONS"
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

# Communication Channels Implementation Guidance

## Purpose

Provides CX Service implementation guidance for the Communication Channels functional area.

## When to Use

Use this functional-area skill after Service scope is confirmed and the project needs communication channels setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Service` (`ORA_SVC`)
- Functional area / Setup Object: `Communication Channels` (`ORA_SVC_COMM_CHANNELS`)

## Setup Tasks

1. [Manage Communication Channels](manage-communication-channels.md) (`ORA_SVC_MANAGE_COMM_CHANNELS`)
2. [Manage Inbound E-Mail Profile Options](manage-inbound-e-mail-profile-options.md) (`ORA_SVC_MANAGE_INBOUND_EMAIL_PROFILE_OPTS`)
3. [Manage Outbound E-Mail Profile Options](manage-outbound-e-mail-profile-options.md) (`ORA_SVC_MANAGE_OUTBOUND_EMAIL_PROFILE_OPTS`)
4. [Manage E-Mail Filters](manage-e-mail-filters.md) (`ORA_SVC_MANAGE_EMAIL_FILTERS`)
5. [Manage Omnichannel Profile Options](manage-omnichannel-profile-options.md) (`ORA_SVC_MANAGE_OMNI_CHANNEL_PROFILE_OPTS`)
6. [Manage MCA Profile Options](manage-mca-profile-options.md) (`ORA_MANAGE_MCA_PROFILE_OPTIONS`)
7. [Manage Service Assignment Objects](manage-service-assignment-objects.md) (`ORA_SVC_MANAGE_SERVICE_REQUEST_ASSIGNMENT_OBJECTS`)
8. [Manage Service Regions](manage-service-regions.md) (`ORA_SVC_MANAGE_SERVICE_ZONES`)
9. [Manage Service Assignment Rules](manage-service-assignment-rules.md) (`ORA_SVC_MANAGE_SERVICE_REQUEST_ASSIGNMENT_RULES`)
10. [Manage Interaction Profile Options](manage-interaction-profile-options.md) (`ORA_SVC_INTERACTION_PROFILE_OPTIONS`)
11. [Manage Email Profile Options](manage-email-profile-options.md) (`ORA_MANAGE_EMAIL_PROFILE_OPTIONS`)

## Inputs

- `implementation_objective`
- `project_context`
- `communication_channels_scope`
- `communication_channels_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.

---
skill_id: "cx.service.service-request"
name: "Service Request Implementation Guidance"
description: "Provides CX Service implementation guidance for the Service Request functional area."
layer: "pillar"
pillar: "CX"
offering: "Service"
functional_area: "Service Request"
functional_area_code: "ORA_SVC_SERVICE_REQUEST"
type: "planning"
execution_mode: "assisted"
owner_team: "CX service pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "service_request_scope"
  - "service_request_requirements"
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
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "core.data-loader"
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.apps-common"
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/service/service-request/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/service/service-request/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/service/service-request/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_SVC_MANAGE_SR_SEVERITIES_R13"
  - "ORA_SVC_MANAGE_SERVICE_REQUEST_INTERNAL_PRIORITIES"
  - "ORA_SVC_MANAGE_SERVICE_REQUEST_CHANNEL_TYPES"
  - "ORA_MANAGE_CHANNEL_TYPE_PROPERTIES"
  - "ORA_SVC_SERVICE_REQUEST_SOURCES"
  - "ORA_SVC_MANAGE_SERVICE_REQUEST_PROBLEM_TYPES"
  - "ORA_SVC_MANAGE_SERVICE_REQUEST_CONTACT_RELATIONSHIP_TYPES"
  - "ORA_SVC_SERVICE_REQUEST_STATUS"
  - "ORA_MANAGE_SERVICE_REQUEST_OUTCOMES_AND_RESOLUTIONS"
  - "ORA_SVC_MANAGE_SERVICE_REQUEST_PROFILE_OPTIONS"
  - "ORA_SVC_SERVICE_REQUEST_CATEGORIES"
  - "ORA_SVC_MANAGE_SR_KNOWLEDGE_PROFILE_OPTIONS"
  - "ORA_MANAGE_OBJECT_LINK_TYPES"
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

# Service Request Implementation Guidance

## Purpose

Provides CX Service implementation guidance for the Service Request functional area.

## When to Use

Use this functional-area skill after Service scope is confirmed and the project needs service request setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Service` (`ORA_SVC`)
- Functional area / Setup Object: `Service Request` (`ORA_SVC_SERVICE_REQUEST`)

## Setup Tasks

1. [Manage Service Request Severities](manage-service-request-severities.md) (`ORA_SVC_MANAGE_SR_SEVERITIES_R13`)
2. [Manage Service Request Internal Priorities](manage-service-request-internal-priorities.md) (`ORA_SVC_MANAGE_SERVICE_REQUEST_INTERNAL_PRIORITIES`)
3. [Manage Service Request Channel Types](manage-service-request-channel-types.md) (`ORA_SVC_MANAGE_SERVICE_REQUEST_CHANNEL_TYPES`)
4. [Manage Service Request Channel Type Visibility](manage-service-request-channel-type-visibility.md) (`ORA_MANAGE_CHANNEL_TYPE_PROPERTIES`)
5. [Manage Service Request Sources](manage-service-request-sources.md) (`ORA_SVC_SERVICE_REQUEST_SOURCES`)
6. [Manage Service Request Problem Types](manage-service-request-problem-types.md) (`ORA_SVC_MANAGE_SERVICE_REQUEST_PROBLEM_TYPES`)
7. [Manage Service Request Contact Relationship Types](manage-service-request-contact-relationship-types.md) (`ORA_SVC_MANAGE_SERVICE_REQUEST_CONTACT_RELATIONSHIP_TYPES`)
8. [Manage Service Request Status Values](manage-service-request-status-values.md) (`ORA_SVC_SERVICE_REQUEST_STATUS`)
9. [Manage Service Request Outcomes and Resolutions](manage-service-request-outcomes-and-resolutions.md) (`ORA_MANAGE_SERVICE_REQUEST_OUTCOMES_AND_RESOLUTIONS`)
10. [Manage Service Request Profile Options](manage-service-request-profile-options.md) (`ORA_SVC_MANAGE_SERVICE_REQUEST_PROFILE_OPTIONS`)
11. [Manage Service Request Categories](manage-service-request-categories.md) (`ORA_SVC_SERVICE_REQUEST_CATEGORIES`)
12. [Manage Service Request Knowledge Profile Options](manage-service-request-knowledge-profile-options.md) (`ORA_SVC_MANAGE_SR_KNOWLEDGE_PROFILE_OPTIONS`)
13. [Manage Object Link Types](manage-object-link-types.md) (`ORA_MANAGE_OBJECT_LINK_TYPES`)

## Inputs

- `implementation_objective`
- `project_context`
- `service_request_scope`
- `service_request_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.

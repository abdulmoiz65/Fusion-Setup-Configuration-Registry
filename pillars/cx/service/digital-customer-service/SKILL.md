---
skill_id: "cx.service.digital-customer-service"
name: "Digital Customer Service Implementation Guidance"
description: "Provides CX Service implementation guidance for the Digital Customer Service functional area."
layer: "pillar"
pillar: "CX"
offering: "Service"
functional_area: "Digital Customer Service"
functional_area_code: "ORA_SVC_DIGITAL_CUSTOMER_SERVICE"
type: "planning"
execution_mode: "assisted"
owner_team: "CX service pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "digital_customer_service_scope"
  - "digital_customer_service_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/service/digital-customer-service/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/service/digital-customer-service/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/service/digital-customer-service/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS"
  - "ORA_SVC_MANAGE_CSS_ACCOUNT_SETUP_OPTS"
  - "ORA_MANAGE_PROXY_USER_CONFIGURATION_DATA"
  - "ORA_SVC_MANAGE_SELF_SERVICE_RELATIONSHIP_TYPE_STANDARD_LOOKUP"
  - "ORA_CREATE_DIGITAL_CUSTOMER_SERVICE_CUSTOM_ROLE_MAPPING"
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

# Digital Customer Service Implementation Guidance

## Purpose

Provides CX Service implementation guidance for the Digital Customer Service functional area.

## When to Use

Use this functional-area skill after Service scope is confirmed and the project needs digital customer service setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Service` (`ORA_SVC`)
- Functional area / Setup Object: `Digital Customer Service` (`ORA_SVC_DIGITAL_CUSTOMER_SERVICE`)

## Setup Tasks

1. [Manage Digital Customer Service Profile Options](manage-digital-customer-service-profile-options.md) (`ORA_SVC_MANAGE_CSS_REG_PROFILE_OPTS`)
2. [Manage Digital Customer Service Account Setup Profile Options](manage-digital-customer-service-account-setup-profile-options.md) (`ORA_SVC_MANAGE_CSS_ACCOUNT_SETUP_OPTS`)
3. [Manage Proxy User Configuration Data](manage-proxy-user-configuration-data.md) (`ORA_MANAGE_PROXY_USER_CONFIGURATION_DATA`)
4. [Manage Self-Service Relationship Type Standard Lookup](manage-self-service-relationship-type-standard-lookup.md) (`ORA_SVC_MANAGE_SELF_SERVICE_RELATIONSHIP_TYPE_STANDARD_LOOKUP`)
5. [Manage Custom Role Mapping for Digital Customer Service](manage-custom-role-mapping-for-digital-customer-service.md) (`ORA_CREATE_DIGITAL_CUSTOMER_SERVICE_CUSTOM_ROLE_MAPPING`)

## Inputs

- `implementation_objective`
- `project_context`
- `digital_customer_service_scope`
- `digital_customer_service_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated setup-task metadata files for task-level planning and sequencing. Track token usage for any generated project artifact or skill-run record using the manifest policy.

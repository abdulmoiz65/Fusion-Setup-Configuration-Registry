---
skill_id: "cx.customer-data-management.customer-hub"
name: "Customer Hub Implementation Guidance"
description: "Provides CX Customer Data Management implementation guidance for the Customer Hub functional area."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Customer Hub"
functional_area_code: "ZCH_CUST_HUB_OPT"
type: "planning"
execution_mode: "assisted"
owner_team: "CX customer data management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "customer_hub_scope"
  - "customer_hub_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/customer-hub/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/customer-hub/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/customer-hub/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "ZCH_MANAGE_CUSTOMER_HUB_COMMON_LOOKUPS"
  - "ZCH_MANAGE_CUSTOMER_HUB_LOOKUPS"
  - "ZCH_MANAGE_CUSTOMER_HUB_DATA_CLEANSING_LOOKUPS"
  - "ZCH_MANAGE_CUSTOMER_HUB_PROFILE_OPTIONS"
  - "ORA_ZCH_MANAGE_CUSTOMER_DATA_MANAGEMENT_OPTIONS"
  - "ZCH_MANAGE_DUPLICATE_RESOLUTION_REQUEST_NOTE_TYPE"
  - "ZCH_MANAGE_DUPLICATE_RESOLUTION_REQUEST_NOTE_TYPE_MAPPING"
  - "ORA_ZCH_MANAGE_SOURCE_SYSTEM_CONFIDENCE"
  - "ZCH_RUN_REQUEST_DISPATCH_JOB"
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

# Customer Hub Implementation Guidance

## Purpose

Provides CX Customer Data Management implementation guidance for the Customer Hub functional area.

## When to Use

Use this functional-area skill after Customer Data Management scope is confirmed and the project needs customer hub setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Customer Data Management` (`ZCH_CDM`)
- Functional area / Setup Object: `Customer Hub` (`ZCH_CUST_HUB_OPT`)

## Setup Tasks

1. [Manage Customer Hub Common Lookups](manage-customer-hub-common-lookups/SKILL.md) (`ZCH_MANAGE_CUSTOMER_HUB_COMMON_LOOKUPS`)
2. [Manage Customer Hub Duplicate Management Lookups](manage-customer-hub-duplicate-management-lookups/SKILL.md) (`ZCH_MANAGE_CUSTOMER_HUB_LOOKUPS`)
3. [Manage Customer Hub Data Cleansing Lookups](manage-customer-hub-data-cleansing-lookups/SKILL.md) (`ZCH_MANAGE_CUSTOMER_HUB_DATA_CLEANSING_LOOKUPS`)
4. [Manage Customer Hub Profile Options](manage-customer-hub-profile-options/SKILL.md) (`ZCH_MANAGE_CUSTOMER_HUB_PROFILE_OPTIONS`)
5. [Manage Customer Data Management Options](manage-customer-data-management-options/SKILL.md) (`ORA_ZCH_MANAGE_CUSTOMER_DATA_MANAGEMENT_OPTIONS`)
6. [Manage Customer Data Hub Note Type](manage-customer-data-hub-note-type/SKILL.md) (`ZCH_MANAGE_DUPLICATE_RESOLUTION_REQUEST_NOTE_TYPE`)
7. [Manage Customer Data Hub Note Type Mapping](manage-customer-data-hub-note-type-mapping/SKILL.md) (`ZCH_MANAGE_DUPLICATE_RESOLUTION_REQUEST_NOTE_TYPE_MAPPING`)
8. [Manage Source System Confidence](manage-source-system-confidence/SKILL.md) (`ORA_ZCH_MANAGE_SOURCE_SYSTEM_CONFIDENCE`)
9. [Run Request Dispatch Job](run-request-dispatch-job/SKILL.md) (`ZCH_RUN_REQUEST_DISPATCH_JOB`)

## Inputs

- `implementation_objective`
- `project_context`
- `customer_hub_scope`
- `customer_hub_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.

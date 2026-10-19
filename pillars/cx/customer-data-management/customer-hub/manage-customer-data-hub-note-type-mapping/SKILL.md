---
skill_id: "cx.customer-data-management.customer-hub.manage-customer-data-hub-note-type-mapping"
name: "Manage Customer Data Hub Note Type Mapping Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Customer Data Hub Note Type Mapping under the Customer Hub functional area."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Customer Hub"
functional_area_code: "ZCH_CUST_HUB_OPT"
task_code: "ZCH_MANAGE_DUPLICATE_RESOLUTION_REQUEST_NOTE_TYPE_MAPPING"
task_name: "Manage Customer Data Hub Note Type Mapping"
parent_skill_id: "cx.customer-data-management.customer-hub"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "CX customer data management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.rest-api-client"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
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
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/customer-hub/manage-customer-data-hub-note-type-mapping/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/customer-hub/manage-customer-data-hub-note-type-mapping/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Reads effective note-type mappings through the documented CRM noteTypes list-of-values resource."
required_privileges: []
---

# Manage Customer Data Hub Note Type Mapping Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Customer Data Hub Note Type Mapping` under `Customer Hub`.

## Setup Task Skill Contract

- task_code: `ZCH_MANAGE_DUPLICATE_RESOLUTION_REQUEST_NOTE_TYPE_MAPPING`
- task_name: `Manage Customer Data Hub Note Type Mapping`
- parent_skill_id: `cx.customer-data-management.customer-hub`
- pillar: `CX`
- offering: `Customer Data Management`
- functional_area: `Customer Hub`
- functional_area_code: `ZCH_CUST_HUB_OPT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Customer Data Hub Note Type Mapping` under `Customer Hub`.

## REST Operations

Use read-only `GET /crmRestApi/resources/11.13.18.05/noteTypes` with the documented `NoteTypeFinder` and exact `BindSourceObjectCode` when resolving effective note-type mappings. Current live describe exposes only GET and marks `SourceObjectCode`, `MappedLookupCode`, and `Meaning` non-updatable. Do not route mapping POST, PATCH, or DELETE through Apps Common or the shared REST client. Use FSM only for an explicit supported task export or import.

Read `ora-resource/ora_rule_registry.json` and its source files before planning a REST read.

## Setup Task Metadata

- Task name: `Manage Customer Data Hub Note Type Mapping`
- Task code: `ZCH_MANAGE_DUPLICATE_RESOLUTION_REQUEST_NOTE_TYPE_MAPPING`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Customer Data Management`
- Functional area / Setup Object: `Customer Hub`
- Setup task name: `Manage Customer Data Hub Note Type Mapping`
- Setup task code: `ZCH_MANAGE_DUPLICATE_RESOLUTION_REQUEST_NOTE_TYPE_MAPPING`




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.customer-data-management.customer-hub` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

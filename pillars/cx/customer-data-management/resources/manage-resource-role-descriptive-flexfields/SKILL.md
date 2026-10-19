---
skill_id: "cx.customer-data-management.resources.manage-resource-role-descriptive-flexfields"
name: "Manage Resource Role Descriptive Flexfields Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Resource Role Descriptive Flexfields under the Resources functional area."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Resources"
functional_area_code: "ORA_CRM_RESOURCES"
task_code: "HZ_MANAGE_RESOURCE_ROLE_DESCRIPTIVE_FLEXFIELDS"
task_name: "Manage Resource Role Descriptive Flexfields"
parent_skill_id: "cx.customer-data-management.resources"
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
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/resources/manage-resource-role-descriptive-flexfields/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/resources/manage-resource-role-descriptive-flexfields/current/"
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
side_effects: []
required_privileges: []
---

# Manage Resource Role Descriptive Flexfields Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Resource Role Descriptive Flexfields` under `Resources`.

## Setup Task Skill Contract

- task_code: `HZ_MANAGE_RESOURCE_ROLE_DESCRIPTIVE_FLEXFIELDS`
- task_name: `Manage Resource Role Descriptive Flexfields`
- parent_skill_id: `cx.customer-data-management.resources`
- pillar: `CX`
- offering: `Customer Data Management`
- functional_area: `Resources`
- functional_area_code: `ORA_CRM_RESOURCES`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Resource Role Descriptive Flexfields` under `Resources`.

## Apps Common Routing

Route every resource-role DFF request to `core.fusion-api.apps-common` as a
Descriptive Flexfield request with:

- Flexfield code: `JTF_RS_ROLES_B`
- Setup task code: `HZ_MANAGE_RESOURCE_ROLE_DESCRIPTIVE_FLEXFIELDS`
- Offering: `Customer Data Management`
- Functional area: `Resources`

Pass the flexfield code with the task context for DFF discovery, export, and
validation. Use `core.fusion-api.apps-common` for that DFF context and
`shared.setup-export.task-level-export` for read-only baseline capture.

Route imports through `core.data-loader` in `FSM` mode. Do not call
`setupTaskCSVImports` or a shared task-level import runner directly from this
pillar skill. Before import, obtain explicit approval for the target
environment, the immutable `JTF_RS_ROLES_B` package, and the intended change.

## Setup Task Metadata

- Task name: `Manage Resource Role Descriptive Flexfields`
- Task code: `HZ_MANAGE_RESOURCE_ROLE_DESCRIPTIVE_FLEXFIELDS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the shared skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Customer Data Management`
- Functional area / Setup Object: `Resources`
- Setup task name: `Manage Resource Role Descriptive Flexfields`
- Setup task code: `HZ_MANAGE_RESOURCE_ROLE_DESCRIPTIVE_FLEXFIELDS`


## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `resource_role_dff_request`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `dff_routing_result`
- `diagnostics`
- `audit_summary`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.customer-data-management.resources` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

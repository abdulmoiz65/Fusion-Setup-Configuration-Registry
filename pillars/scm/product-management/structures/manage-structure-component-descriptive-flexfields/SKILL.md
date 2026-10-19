---
skill_id: "scm.product-management.structures.manage-structure-component-descriptive-flexfields"
name: "Manage Structure Component Descriptive Flexfields Setup Task Guidance"
description: "Provides setup-data routing and Application Common descriptive-flexfield guidance for Manage Structure Component Descriptive Flexfields under the Structures functional area."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "Structures"
functional_area_code: "EGO_ADVANCED_PRODUCT_STRUCT"
task_code: "EGO_MANAGE_STRUCTURE_COMPONENT_ATTRIBUTES"
task_name: "Manage Structure Component Descriptive Flexfields"
parent_skill_id: "scm.product-management.structures"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM product management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "flexfield_change_request"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "flexfield_change_preview"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.fusion-api.apps-common"
  - "shared.setup-import.task-level-import"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/structures/manage-structure-component-descriptive-flexfields/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/structures/manage-structure-component-descriptive-flexfields/current/"
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

# Manage Structure Component Descriptive Flexfields Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Structure Component Descriptive Flexfields` under `Structures`.

## Setup Task Skill Contract

- task_code: `EGO_MANAGE_STRUCTURE_COMPONENT_ATTRIBUTES`
- task_name: `Manage Structure Component Descriptive Flexfields`
- parent_skill_id: `scm.product-management.structures`
- pillar: `SCM`
- offering: `Product Management`
- functional_area: `Structures`
- functional_area_code: `EGO_ADVANCED_PRODUCT_STRUCT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Structure Component Descriptive Flexfields` under `Structures`.

## Setup Task Metadata

- Task name: `Manage Structure Component Descriptive Flexfields`
- Task code: `EGO_MANAGE_STRUCTURE_COMPONENT_ATTRIBUTES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Route DFF setup through `core.fusion-api.apps-common` and its Descriptive Flexfields reference.
2. Export setup task data with `shared.setup-export.task-level-export`.
3. Validate setup task data with `shared.validation.setup-data-validator`.
4. Validate reference data with `shared.validation.reference-data-validator`.

Do not invoke a direct Fusion endpoint, create a Data Loader business object, or generate an API sample workbook for this DFF task. The supported route delegates task discovery, CSV processing, polling, and artifact persistence to the shared task-level workflows.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Structures`
- Setup task name: `Manage Structure Component Descriptive Flexfields`
- Setup task code: `EGO_MANAGE_STRUCTURE_COMPONENT_ATTRIBUTES`

## Application Common Descriptive Flexfield Routing

Route descriptive-flexfield requests for this task through
`core.fusion-api.apps-common`. Identify the requested flexfield code explicitly;
do not implement OAuth or REST transport in this task skill.

Use this flexfield code:

- `EGP_COMPONENT_DFF`

For a change request, use the core skill's read-before-write, preview, and
explicit approval gates. For DFF setup guidance, follow the descriptive-flexfield
routing defined by `core.fusion-api.apps-common`.




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `flexfield_change_request`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `flexfield_change_preview`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `scm.product-management.structures` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

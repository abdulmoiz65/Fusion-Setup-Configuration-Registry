---
skill_id: "cx.sales.sales-foundation.manage-sales-note-type"
name: "Manage Sales Note Type Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Sales Note Type under the Sales Foundation functional area."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Sales Foundation"
functional_area_code: "ORA_ZBS_SALES_FOUNDATION"
task_code: "ZBS_MANAGE_SALES_NOTE_TYPE"
task_name: "Manage Sales Note Type"
parent_skill_id: "cx.sales.sales-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "CX sales pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-foundation/manage-sales-note-type/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-foundation/manage-sales-note-type/current/"
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

# Manage Sales Note Type Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Sales Note Type` under `Sales Foundation`.

## Setup Task Skill Contract

- task_code: `ZBS_MANAGE_SALES_NOTE_TYPE`
- task_name: `Manage Sales Note Type`
- parent_skill_id: `cx.sales.sales-foundation`
- pillar: `CX`
- offering: `Sales`
- functional_area: `Sales Foundation`
- functional_area_code: `ORA_ZBS_SALES_FOUNDATION`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Sales Note Type` under `Sales Foundation`.

## Supported Scenarios

- Review the current note-type design and effective state.
- Create a note type in the `ZMM_NOTE_TYPE` lookup.
- Update the meaning, description, enablement, or effective dates when the lookup configuration permits it.
- Deactivate or end-date a custom note type with historical-impact safeguards.
- Add or review translated meanings and descriptions.
- Coordinate object-specific or default-note availability through the separate `Manage Sales Note Type Mapping` task.
- Export, validate, import, and verify catalog-supported setup data using the current task package.
- Validate mapped runtime availability for a source object through the read-only Sales Note Types resource.

## Oracle Resource Read Order

For task-specific execution planning, read the generated resource guidance in this order:

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_dependency_readiness.md`
3. `ora-resource/ora_reference_lookups.md`
4. `ora-resource/ora_defaulting_rules.md`
5. `ora-resource/ora_design_enforcement.md`
6. `ora-resource/ora_error_handling.md`
7. `ora-resource/ora_rule_registry.json`

## Setup Task Metadata

- Task name: `Manage Sales Note Type`
- Task code: `ZBS_MANAGE_SALES_NOTE_TYPE`
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

- Offering: `Sales`
- Functional area / Setup Object: `Sales Foundation`
- Setup task name: `Manage Sales Note Type`
- Setup task code: `ZBS_MANAGE_SALES_NOTE_TYPE`

## Execution Route Selection

For a supported mutation, default to the CSV/FSM workflow above and `core.data-loader`; do not initialize browser control or substitute a guided UI action. Use guided UI only when the requester explicitly asks for manual setup. If the current task package cannot represent the requested operation, report that limitation before any live action.


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

Use the parent functional-area skill `cx.sales.sales-foundation` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

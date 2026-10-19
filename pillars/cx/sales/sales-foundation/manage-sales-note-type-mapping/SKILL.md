---
skill_id: "cx.sales.sales-foundation.manage-sales-note-type-mapping"
name: "Manage Sales Note Type Mapping Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Sales Note Type Mapping under the Sales Foundation functional area."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Sales Foundation"
functional_area_code: "ORA_ZBS_SALES_FOUNDATION"
task_code: "ZBS_MANAGE_SALES_NOTE_TYPE_MAPPING"
task_name: "Manage Sales Note Type Mapping"
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
version: "0.1.1"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-foundation/manage-sales-note-type-mapping/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/sales-foundation/manage-sales-note-type-mapping/current/"
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

# Manage Sales Note Type Mapping Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Sales Note Type Mapping` under `Sales Foundation`.

## Setup Task Skill Contract

- task_code: `ZBS_MANAGE_SALES_NOTE_TYPE_MAPPING`
- task_name: `Manage Sales Note Type Mapping`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Sales Note Type Mapping` under `Sales Foundation`.

## Supported Scenarios

- Review the mappings defined for a Sales business object or for Default Note Types.
- Create an object-specific mapping from an existing enabled `ZMM_NOTE_TYPE` lookup code only after the requester explicitly chooses whether to preserve the currently effective note-type list or restrict the object to the requested values.
- Update a mapping's default decision or optional end date through the guided setup task when the page permits it.
- End-date a mapping after reviewing the effective fallback and downstream user impact.
- Review or change Default Note Types with an impact assessment for every business object that has no specific mapping.
- Coordinate prerequisite lookup-code creation through `cx.sales.sales-foundation.manage-sales-note-type`.
- Export, validate, import, and verify task-package-supported mapping setup data using the current task package. A current export lists persisted mapping rows; its absence of a selectable business object is not evidence that the object is unsupported.
- Validate effective note-type availability for an exact source object through the read-only Sales Note Types resource.
- Resolve UI business-object labels and `SourceObjectCode` values from `ora-resource/ora_supported_object_codes.md`; do not derive a code by transforming its display label or an Object Metadata `ObjectCode`.

## Oracle Resource Read Order

For task-specific execution planning, read the generated resource guidance in this order:

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_dependency_readiness.md`
3. `ora-resource/ora_supported_object_codes.md`
4. `ora-resource/ora_reference_lookups.md`
5. `ora-resource/ora_defaulting_rules.md`
6. `ora-resource/ora_design_enforcement.md`
7. `ora-resource/ora_error_handling.md`
8. `ora-resource/ora_rule_registry.json`

## Setup Task Metadata

- Task name: `Manage Sales Note Type Mapping`
- Task code: `ZBS_MANAGE_SALES_NOTE_TYPE_MAPPING`
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
- Setup task name: `Manage Sales Note Type Mapping`
- Setup task code: `ZBS_MANAGE_SALES_NOTE_TYPE_MAPPING`

## Execution Route Selection

For a supported mutation, default to the CSV/FSM workflow and `core.data-loader`; do not initialize browser control. Guided UI is available only when explicitly requested. If the current task package cannot represent the requested operation, report that limitation before any live action.




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

Use the parent functional-area skill `cx.sales.sales-foundation` for functional-area sequencing and scope decisions. Use `cx.sales.sales-foundation.manage-sales-note-type` when a required `ZMM_NOTE_TYPE` code does not yet exist. Do not treat the read-only Sales Note Types REST result as proof that an explicit setup mapping row exists, because Default Note Types can supply the effective values. Track token usage for any generated project artifact or skill-run record using the manifest policy.

When an object has no persisted mapping row, creating its first object-specific row replaces its inherited Default Note Types list. Before preparing a UI plan or FSM ZIP, ask the requester to choose exactly one outcome: preserve the current effective list by explicitly mapping every desired value, or restrict the object to the specifically requested values. Never copy inherited values automatically.

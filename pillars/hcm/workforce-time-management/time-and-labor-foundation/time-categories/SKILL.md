---
skill_id: "hcm.workforce-time-management.time-and-labor-foundation.time-categories"
name: "Time Categories Setup Task Guidance"
description: "Provides task-specific setup guidance for Time Categories under the Time and Labor Foundation functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Time Management"
functional_area: "Time and Labor Foundation"
functional_area_code: "ORA_TIME_AND_LABOR_FOUNDATION"
task_code: "ORA_HWM_MANAGE_TIME_CATEGORIES"
task_name: "Time Categories"
parent_skill_id: "hcm.workforce-time-management.time-and-labor-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM workforce time management pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-foundation/time-categories/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-foundation/time-categories/current/"
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

# Time Categories Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Time Categories` under `Time and Labor`.

## Setup Task Skill Contract

- task_code: `ORA_HWM_MANAGE_TIME_CATEGORIES`
- task_name: `Time Categories`
- parent_skill_id: `hcm.workforce-time-management.time-and-labor-foundation`
- pillar: `HCM`
- offering: `Time and Labor`
- functional_area: `Time and Labor`
- functional_area_code: `ORA_TIME_AND_LABOR_FOUNDATION`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Time Categories` under `Time and Labor`.

## Setup Task Metadata

- Task name: `Time Categories`
- Task code: `ORA_HWM_MANAGE_TIME_CATEGORIES`
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

- Offering: `Time and Labor`
- Functional area / Setup Object: `Time and Labor`
- Setup task name: `Time Categories`
- Setup task code: `ORA_HWM_MANAGE_TIME_CATEGORIES`

## Export-Shaped FSM Package Preparation

For every create or edit, use a fresh export as the authoritative FSM package
baseline. Retain its exact-case metadata, declared CSV members, headers, key
fields, and unrelated rows. Apply only the approved Time Category change to
the category, expression-group, and ordered condition rows; do not clone an
existing category as a template.

Resolve every condition field before package preparation. For a Specific Value,
preserve every value field required by the fresh expression CSV contract: map
the resolved business display value to each required display field and map the
resolved selection value to its corresponding selection field. A blank required
display or selection field blocks validation and approval.

Validate the prepared FSM ZIP against the same fresh export and the task-local
rules before Core Data Loader validation or approval. Reject any package that
changes metadata, member names, headers, row widths, unrelated rows, cross-file
references, populated display-sequence ordering, expression-group linkage, or
the final-condition operator.

For every import, complete Core Data Loader validation, persist the immutable preflight artifact, and complete Task Hook validation before requesting approval. Show one clickable link to the exact validated FSM ZIP outside the business-only Complete Summary, then request one approval immediately before upload and import.

## Final Completion Verification

After an approved FSM submission is accepted, do not treat acceptance or a
successful load count as completion. Monitor the accepted request through the
selected Data Loader status route. On terminal success, obtain a fresh Time
Categories export and compare the persisted category with the approved
normalized configuration. Completion requires matching parent business fields,
the group-expression row, and every ordered condition's attribute, value type,
explicit value, operators, parentheses, and structural linkage. A mismatch
stops the workflow without an automatic retry.




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

Use the parent functional-area skill `hcm.workforce-time-management.time-and-labor-foundation` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

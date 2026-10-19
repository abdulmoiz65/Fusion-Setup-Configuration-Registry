---
skill_id: "hcm.workforce-time-management.time-and-labor-additional.workday-definitions"
name: "WorkDay Definitions Setup Task Guidance"
description: "Provides task-specific setup guidance for WorkDay Definitions under the Time and Labor Additional functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Time Management"
functional_area: "Time and Labor Additional"
functional_area_code: "ORA_TIME_AND_LABOR_ADDITIONAL"
task_code: "ORA_HWM_MANAGE_WORK_DAY_DEFINITIONS"
task_name: "WorkDay Definitions"
parent_skill_id: "hcm.workforce-time-management.time-and-labor-additional"
available_flag: "Y"
export_import_supported_flag: "UNKNOWN"
csv_export_import_supported_flag: "UNKNOWN"
dataloader_import_mode: "REST"
businessObject: "workDayDefinitions"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM workforce time management pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-additional/workday-definitions/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-additional/workday-definitions/current/"
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

# WorkDay Definitions Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `WorkDay Definitions` under `Time and Labor Additional`.

## Setup Task Skill Contract

- task_code: `ORA_HWM_MANAGE_WORK_DAY_DEFINITIONS`
- task_name: `WorkDay Definitions`
- parent_skill_id: `hcm.workforce-time-management.time-and-labor-additional`
- pillar: `HCM`
- offering: `Time and Labor`
- functional_area: `Time and Labor Additional`
- functional_area_code: `ORA_TIME_AND_LABOR_ADDITIONAL`
- available_flag: `Y`
- export_import_supported_flag: `UNKNOWN`
- csv_export_import_supported_flag: `UNKNOWN`
- dataloader_import_mode: `REST`
- businessObject: `workDayDefinitions`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `WorkDay Definitions` under `Time and Labor Additional`.

## Setup Task Metadata

- Task name: `WorkDay Definitions`
- Task code: `ORA_HWM_MANAGE_WORK_DAY_DEFINITIONS`
- Available: `Y`
- Export/import supported: `UNKNOWN`
- CSV export/import supported: `UNKNOWN`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `workDayDefinitions`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `UNKNOWN` for this task, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` unless live Fusion metadata or Oracle guidance confirms support. For the explicitly selected REST setup-data import path, use `core.data-loader` with `workDayDefinitions` as the registered BusinessObject. Use the shared validation skills when a setup-data artifact or cross-pillar reference dependency is available for review.

Use this task metadata when invoking `core.data-loader`:

- Offering: `Time and Labor`
- Functional area / Setup Object: `Time and Labor Additional`
- Setup task name: `WorkDay Definitions`
- Setup task code: `ORA_HWM_MANAGE_WORK_DAY_DEFINITIONS`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `workDayDefinitions` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "workDayDefinitions" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

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

Use the parent functional-area skill `hcm.workforce-time-management.time-and-labor-additional` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

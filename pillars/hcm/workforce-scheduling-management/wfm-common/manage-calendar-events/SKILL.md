---
skill_id: "hcm.workforce-scheduling-management.wfm-common.manage-calendar-events"
name: "Manage Calendar Events Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Calendar Events under the WFM Common functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Scheduling Management"
functional_area: "WFM Common"
functional_area_code: "ORA_WFM_COMMON"
task_code: "PER_MANAGE_CALENDAR_EVENT"
task_name: "Manage Calendar Events"
parent_skill_id: "hcm.workforce-scheduling-management.wfm-common"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObjects:
  - "calendarEvents"
  - "absenceCalendars"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM workforce scheduling management pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-scheduling-management/wfm-common/manage-calendar-events/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-scheduling-management/wfm-common/manage-calendar-events/current/"
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

# Manage Calendar Events Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Calendar Events` under `WFM Common`.

## Setup Task Skill Contract

- task_code: `PER_MANAGE_CALENDAR_EVENT`
- task_name: `Manage Calendar Events`
- parent_skill_id: `hcm.workforce-scheduling-management.wfm-common`
- pillar: `HCM`
- offering: `Workforce Scheduling Management`
- functional_area: `WFM Common`
- functional_area_code: `ORA_WFM_COMMON`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObjects: `calendarEvents`, `absenceCalendars`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business objects.

1. Confirm that `calendarEvents`, `absenceCalendars` are the exact registered Data Loader business objects.
2. Generate the default editable XLSX samples through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "calendarEvents" \
     "absenceCalendars" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep each business object's generated workbook set together:
   - editable sample workbook
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbooks as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Calendar Events` under `WFM Common`.

## Data Loader Status Reporting

When the user requests status for a Data Loader submission made through this task, use the core Data Loader status workflow. If the data set status is **Succeeded**, append a business-only **Created Setup Summary** drawn from the validated, approved task data for that same submission:

- List each calendar created or updated, including its name and date-only start or end date when supplied.
- Under each calendar, list every event attached by the load using its verified event name, category meaning, and start or end date when supplied.
- Use `YYYY-MM-DD` for every displayed date-only value. Do not expose IDs, category codes, archive details, request IDs, or other implementation values in the summary.
- Do not show the Created Setup Summary for an in-progress, failed, partially successful, or unmatched data set. Instead, return the core status result and any applicable diagnostics.

## Setup Task Metadata

- Task name: `Manage Calendar Events`
- Task code: `PER_MANAGE_CALENDAR_EVENT`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Objects: `calendarEvents`, `absenceCalendars`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `calendarEvents` and `absenceCalendars` as ordered Business Objects.

Use this task metadata when invoking those skills:

- Offering: `Workforce Scheduling Management`
- Functional area / Setup Object: `WFM Common`
- Setup task name: `Manage Calendar Events`
- Setup task code: `PER_MANAGE_CALENDAR_EVENT`




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

Use the parent functional-area skill `hcm.workforce-scheduling-management.wfm-common` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

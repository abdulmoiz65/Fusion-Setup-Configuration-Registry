---
skill_id: "hcm.workforce-time-management.time-and-labor-foundation.time-profiles"
name: "Time Profiles Setup Task Guidance"
description: "Provides task-specific setup guidance for Time Profiles under the Time and Labor Foundation functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Time Management"
functional_area: "Time and Labor Foundation"
functional_area_code: "ORA_TIME_AND_LABOR_FOUNDATION"
task_code: "ORA_HXT_TIME_PROFILES"
task_name: "Time Profiles"
parent_skill_id: "hcm.workforce-time-management.time-and-labor-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "timeProfiles"
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
depends_on:
  - "hcm.workforce-time-management.time-and-labor-common.manage-profile-options"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-foundation/time-profiles/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-foundation/time-profiles/current/"
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

# Time Profiles Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Time Profiles` under `Time and Labor Foundation`.

## Setup Task Skill Contract

- task_code: `ORA_HXT_TIME_PROFILES`
- task_name: `Time Profiles`
- parent_skill_id: `hcm.workforce-time-management.time-and-labor-foundation`
- pillar: `HCM`
- offering: `Workforce Time Management`
- functional_area: `Time and Labor Foundation`
- functional_area_code: `ORA_TIME_AND_LABOR_FOUNDATION`
- available_flag: `Y`
- export_import_supported_flag: `UNKNOWN`
- csv_export_import_supported_flag: `UNKNOWN`
- dataloader_import_mode: `REST`
- businessObject: `timeProfiles`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Time Profiles` under `Time and Labor Foundation`.

## Setup Task Metadata

- Task name: `Time Profiles`
- Task code: `ORA_HXT_TIME_PROFILES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `timeProfiles`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y`, so CSV export/import is supported in the effective setup-task catalog. Route export work to `shared.setup-export.task-level-export`, import work to `core.data-loader`, and artifact validation to `shared.validation.setup-data-validator`.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `timeProfiles` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "timeProfiles" \
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

Use the parent functional-area skill `hcm.workforce-time-management.time-and-labor-foundation` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

---
skill_id: "hcm.workforce-time-management.time-and-labor-foundation.time-consumer-sets"
name: "Time Consumer Sets Setup Task Guidance"
description: "Provides task-specific setup guidance for Time Consumer Sets under the Time and Labor Foundation functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Time Management"
functional_area: "Time and Labor Foundation"
functional_area_code: "ORA_TIME_AND_LABOR_FOUNDATION"
task_code: "ORA_HWM_MANAGE_TIME_C0NSUMER_SETS"
task_name: "Time Consumer Sets"
parent_skill_id: "hcm.workforce-time-management.time-and-labor-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "timeConsumerSets"
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
  - "environment_version_details"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.baseline-assessment.topology-manager.environment-info"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-foundation/time-consumer-sets/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-time-management/time-and-labor-foundation/time-consumer-sets/current/"
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

# Time Consumer Sets Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Time Consumer Sets` under `Time and Labor`.

## Setup Task Skill Contract

- task_code: `ORA_HWM_MANAGE_TIME_C0NSUMER_SETS`
- task_name: `Time Consumer Sets`
- parent_skill_id: `hcm.workforce-time-management.time-and-labor-foundation`
- pillar: `HCM`
- offering: `Time and Labor`
- functional_area: `Time and Labor`
- functional_area_code: `ORA_TIME_AND_LABOR_FOUNDATION`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `timeConsumerSets`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow only after the environment release gate confirms release 27A or later and the live REST-capability gate confirms a usable current `timeConsumerSets` registration. Do not generate a sample for a release before 27A.

1. Confirm that `timeConsumerSets` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "timeConsumerSets" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Time Consumer Sets` under `Time and Labor`. Retrieve `environment_version_details` through `shared.baseline-assessment.topology-manager.environment-info` before any task validation, lookup, REST sample generation, provider approval, or execution. For a release before `27A`, inform the user that Time Consumer Sets is not available through this skill and stop. For `27A` and later, or when release details are unavailable, confirm one exact usable current `timeConsumerSets` Data Loader registration and metadata set before continuing. This skill has no FSM fallback.

## Setup Task Metadata

- Task name: `Time Consumer Sets`
- Task code: `ORA_HWM_MANAGE_TIME_C0NSUMER_SETS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `timeConsumerSets`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Retrieve the target environment release through `shared.baseline-assessment.topology-manager.environment-info` before further task processing.
   - Before `27A`, inform the user that Time Consumer Sets is not available through this skill and stop.
   - For `27A` and later, or when release details are unavailable, use `core.data-loader` to confirm one exact usable current `timeConsumerSets` registration and metadata set. Stop when the capability is unavailable; do not select FSM.
5. Import setup task data with `core.data-loader` using `timeConsumerSets` as the Business Object only after the release and REST-capability gates pass.

Use this task metadata when invoking those skills:

- Offering: `Time and Labor`
- Functional area / Setup Object: `Time and Labor`
- Setup task name: `Time Consumer Sets`
- Setup task code: `ORA_HWM_MANAGE_TIME_C0NSUMER_SETS`




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `environment_version_details`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.workforce-time-management.time-and-labor-foundation` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

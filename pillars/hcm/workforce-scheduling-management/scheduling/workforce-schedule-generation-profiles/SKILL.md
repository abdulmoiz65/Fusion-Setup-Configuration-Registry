---
skill_id: "hcm.workforce-scheduling-management.scheduling.workforce-schedule-generation-profiles"
name: "Workforce Schedule Generation Profiles Setup Task Guidance"
description: "Provides task-specific setup guidance for Workforce Schedule Generation Profiles under the Scheduling functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Scheduling Management"
functional_area: "Scheduling"
functional_area_code: "ORA_SCHEDULING"
task_code: "ORA_HTS_MANAGE_SCHED_GEN_PROFILES"
task_name: "Workforce Schedule Generation Profiles"
parent_skill_id: "hcm.workforce-scheduling-management.scheduling"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "scheduleGenerationProfiles"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-scheduling-management/scheduling/workforce-schedule-generation-profiles/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-scheduling-management/scheduling/workforce-schedule-generation-profiles/current/"
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

# Workforce Schedule Generation Profiles Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Workforce Schedule Generation Profiles` under `Scheduling`.

## Setup Task Skill Contract

- task_code: `ORA_HTS_MANAGE_SCHED_GEN_PROFILES`
- task_name: `Workforce Schedule Generation Profiles`
- parent_skill_id: `hcm.workforce-scheduling-management.scheduling`
- pillar: `HCM`
- offering: `Workforce Scheduling Management`
- functional_area: `Scheduling`
- functional_area_code: `ORA_SCHEDULING`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `scheduleGenerationProfiles`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `scheduleGenerationProfiles` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "scheduleGenerationProfiles" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Workforce Schedule Generation Profiles` under `Scheduling`.

## Setup Task Metadata

- Task name: `Workforce Schedule Generation Profiles`
- Task code: `ORA_HTS_MANAGE_SCHED_GEN_PROFILES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `scheduleGenerationProfiles`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `scheduleGenerationProfiles` as the Business Object.

Use this task metadata when invoking those skills:

- Offering: `Workforce Scheduling Management`
- Functional area / Setup Object: `Scheduling`
- Setup task name: `Workforce Schedule Generation Profiles`
- Setup task code: `ORA_HTS_MANAGE_SCHED_GEN_PROFILES`

## Data Load Status Reporting

When the user asks to show or check the status of a Data Loader request for
this task, first use `core.data-loader` to return the complete data-set status,
counts, and any actionable errors. Retain the submitted operation and exact
profile business identity in the task's validated configuration blueprint so a
later status check can verify the correct target.

- On a successful terminal status with no returned diagnostics, perform the
  required read-only profile verification in
  `ora-resource/ora_reference_lookups.md`, then append the required
  post-status profile summary described in
  `ora-resource/ora_error_handling.md`.
- On a failed, active, unavailable, or uncertain status, show the Data Loader
  error details and its next action only. Do not claim that the profile was
  created, updated, deleted, or duplicated, even if a partial change might be
  visible in Fusion.
- Do not substitute a prior local source, chat message, or unverified profile
  state for the required read-back. If the retained operation or exact profile
  identity is missing, report that verification cannot be completed rather
  than inventing a profile summary.




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

Use the parent functional-area skill `hcm.workforce-scheduling-management.scheduling` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

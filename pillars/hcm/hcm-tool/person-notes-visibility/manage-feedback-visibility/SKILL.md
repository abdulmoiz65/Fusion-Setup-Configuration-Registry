---
skill_id: "hcm.hcm-tool.person-notes-visibility.manage-feedback-visibility"
name: "Manage Feedback Visibility Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Feedback Visibility under the Person Notes Visibility functional area."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Person Notes Visibility"
functional_area_code: "CUSTOM_PERSON_NOTES"
task_code: "ORA_HRT_MANAGE_FEEDBACK_VISIBILITY"
task_name: "Manage Feedback Visibility"
parent_skill_id: "hcm.hcm-tool.person-notes-visibility"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "personNotesVisibilityConfigurations"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM hcm tool pillar team"
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
  - "core.fusion-api.rest-api-client"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/person-notes-visibility/manage-feedback-visibility/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/person-notes-visibility/manage-feedback-visibility/current/"
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

# Manage Feedback Visibility Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Feedback Visibility` under `Person Notes Visibility`.

## Setup Task Skill Contract

- task_code: `ORA_HRT_MANAGE_FEEDBACK_VISIBILITY`
- task_name: `Manage Feedback Visibility`
- parent_skill_id: `hcm.hcm-tool.person-notes-visibility`
- pillar: `HCM`
- offering: `HCM Tool`
- functional_area: `Person Notes Visibility`
- functional_area_code: `CUSTOM_PERSON_NOTES`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `personNotesVisibilityConfigurations`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `personNotesVisibilityConfigurations` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "personNotesVisibilityConfigurations" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Feedback Visibility` under `Person Notes Visibility`.

## Setup Task Metadata

- Task name: `Manage Feedback Visibility`
- Task code: `ORA_HRT_MANAGE_FEEDBACK_VISIBILITY`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `personNotesVisibilityConfigurations`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Route create, update, and delete operations through `core.data-loader` using the registered REST business object `personNotesVisibilityConfigurations`.

Use this task metadata when invoking those skills:

- Offering: `HCM Tool`
- Functional area / Setup Object: `Person Notes Visibility`
- Setup task name: `Manage Feedback Visibility`
- Setup task code: `ORA_HRT_MANAGE_FEEDBACK_VISIBILITY`
- Data Loader import mode: `REST`
- Business Object: `personNotesVisibilityConfigurations`

## REST Scope and Update Decision

Use the supported surface appropriate to the requested operation:

| Operation | Supported route | Decision |
|---|---|---|
| List published visibility options | `core.fusion-api.rest-api-client` with `GET /hcmRestApi/resources/11.13.18.05/personNotesVisibilityOptions` | Supported read-only REST resource. |
| Get one published visibility option | `core.fusion-api.rest-api-client` with `GET /hcmRestApi/resources/11.13.18.05/personNotesVisibilityOptions/{personNotesVisibilityOptionsUniqID}` | Supported read-only REST resource. |
| List current Feedback Visibility configurations | `core.fusion-api.rest-api-client` with `GET /hcmRestApi/resources/11.13.18.05/personNotesVisibilityConfigurations` | Page the complete collection and resolve returned codes through the declared Common Lookups routes. |
| Create, update, or delete Feedback Visibility configuration | `core.data-loader` with `personNotesVisibilityConfigurations` | This is the exclusive mutation route. Validate the generated workbook and immutable preview before execution. |
| Direct REST mutation outside Data Loader | None | Unsupported. Do not construct or replay POST, PATCH, PUT, DELETE, or action URLs independently. |

The registered Data Loader business object for this task is
`personNotesVisibilityConfigurations`. Use it only for create, update, or
delete operations. Route every Person Notes Visibility GET through
`core.fusion-api.rest-api-client`. The page observations also identify the
supporting read-only lookups `ORA_FEEDBACK_CONTEXT_TYPE`,
`ORA_NOTE_VISIBILITY_CODE`, and `PER_SUPERVISOR_TYPE`. The separately published
`personNotesVisibilityOptions` resource remains a read-only option resource and
must not replace the registered configuration business object for mutations.

For update or delete, first use the generated key-fields workbook and a fresh
read to identify exactly one existing configuration. Prepare the Data Loader
artifact, validate it, and present an immutable preview containing the target
environment, operation, key fields, and material values. Obtain approval under
the `core.data-loader` workflow immediately before execution. Do not guess a
REST method or item URL: Data Loader owns method selection, request shape,
execution, monitoring, and readback. Never retry a live mutation automatically.

See this task's [lookup and route rules](ora-resource/ora_reference_lookups.md).




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

Use the parent functional-area skill `hcm.hcm-tool.person-notes-visibility` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

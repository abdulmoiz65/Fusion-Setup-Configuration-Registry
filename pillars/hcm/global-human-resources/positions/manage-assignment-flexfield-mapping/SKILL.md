---
skill_id: "hcm.global-human-resources.positions.manage-assignment-flexfield-mapping"
name: "Manage Assignment Flexfield Mapping Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Assignment Flexfield Mapping under the Positions functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Positions"
functional_area_code: "ORA_POSITIONS"
task_code: "ORA_PER_MANAGE_ASSIGNMENT_FLEXFIELD_MAPPING"
task_name: "Manage Assignment Flexfield Mapping"
parent_skill_id: "hcm.global-human-resources.positions"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "AssignmentFlexfieldsMapping"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/positions/manage-assignment-flexfield-mapping/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/positions/manage-assignment-flexfield-mapping/current/"
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

# Manage Assignment Flexfield Mapping Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Assignment Flexfield Mapping` under `Positions`.

## Setup Task Skill Contract

- task_code: `ORA_PER_MANAGE_ASSIGNMENT_FLEXFIELD_MAPPING`
- task_name: `Manage Assignment Flexfield Mapping`
- parent_skill_id: `hcm.global-human-resources.positions`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Positions`
- functional_area_code: `ORA_POSITIONS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `AssignmentFlexfieldsMapping`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `AssignmentFlexfieldsMapping` is the exact registered Data Loader business object and that Fusion supplies `AssignmentFlexfieldsMapping.dat` as its raw DAT template.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "AssignmentFlexfieldsMapping" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Assignment Flexfield Mapping` under `Positions`.

## Read-Only Result Display

For a read-only mapping list or details response, render a Markdown table with
these columns in this exact order:

1. `Position Flexfield Context`
2. `Position Flexfield Segment`
3. `Assignment Flexfield Context`
4. `Assignment Flexfield Segment`

Show the complete matched collection and its count. Do not display mapping IDs
or other internal execution values. For the authoritative field mappings and
the full exclusion list, read
[`ora-resource/ora_reference_lookups.md`](ora-resource/ora_reference_lookups.md).

For an unfiltered collection, introduce the table with
`All <count> Assignment Flexfield mappings (4 columns):`. For a filtered
collection or details response, use the matching count-led plain-language
introduction, then render the same table.

For a mutation approval preview, retain the same user-facing fields and omit
internal execution values. When the preview contains multiple mappings, render
them as one compact row per mapping in the four-column table. When it contains
one mapping, render a neat two-column `Field | Value` table instead, using
Position Flexfield Context, Position Flexfield Segment, Assignment Flexfield
Context, and Assignment Flexfield Segment as the fields.

## Setup Task Metadata

- Task name: `Manage Assignment Flexfield Mapping`
- Task code: `ORA_PER_MANAGE_ASSIGNMENT_FLEXFIELD_MAPPING`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `AssignmentFlexfieldsMapping`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using AssignmentFlexfieldsMapping as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Global Human Resources`
- Functional area / Setup Object: `Positions`
- Setup task name: `Manage Assignment Flexfield Mapping`
- Setup task code: `ORA_PER_MANAGE_ASSIGNMENT_FLEXFIELD_MAPPING`




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

Use the parent functional-area skill `hcm.global-human-resources.positions` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

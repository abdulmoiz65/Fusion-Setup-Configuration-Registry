---
skill_id: "hcm.performance-management.performance-document-type.performance-document-types"
name: "Performance Document Types Setup Task Guidance"
description: "Provides task-specific setup guidance for Performance Document Types under the Performance Document Type functional area."
layer: "pillar"
pillar: "HCM"
offering: "Performance Management"
functional_area: "Performance Document Type"
functional_area_code: "ORA_PERFORMANCE_DOCUMENT_TYPE"
task_code: "HRA_MANAGE_DOCUMENT_TYPES"
task_name: "Performance Document Types"
parent_skill_id: "hcm.performance-management.performance-document-type"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM performance management pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/performance-management/performance-document-type/performance-document-types/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/performance-management/performance-document-type/performance-document-types/current/"
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

# Performance Document Types Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Performance Document Types` under `Performance Document Type`.

## Setup Task Skill Contract

- task_code: `HRA_MANAGE_DOCUMENT_TYPES`
- task_name: `Performance Document Types`
- parent_skill_id: `hcm.performance-management.performance-document-type`
- pillar: `HCM`
- offering: `Performance Management`
- functional_area: `Performance Document Type`
- functional_area_code: `ORA_PERFORMANCE_DOCUMENT_TYPE`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Performance Document Types` under `Performance Document Type`.

## Setup Task Metadata

- Task name: `Performance Document Types`
- Task code: `HRA_MANAGE_DOCUMENT_TYPES`
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

Apply the offering-wide [CSV Import Guidance](../../csv_import_guidance.md)
when preparing an import archive.

Use this task metadata when invoking those skills:

- Offering: `Performance Management`
- Functional area / Setup Object: `Performance Document Type`
- Setup task name: `Performance Document Types`
- Setup task code: `HRA_MANAGE_DOCUMENT_TYPES`

## CSV Export Result Summary

After a successful export, inspect every `*.csv` member in the downloaded ZIP
or extracted folder. Count data rows only, excluding the header row, and exclude
non-CSV files. Include this in the final response with comma-formatted counts:

The ZIP contains **<total> total data records** across its CSV files.

| File | Records |
| --- | ---: |
| `<CSV filename>` | `<data-row count>` |




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

Use the parent functional-area skill `hcm.performance-management.performance-document-type` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Post-import verification

After Fusion reports an import as successful, include this clickable verification link in the final result: [Open Performance Document Types]({restBaseUrl}/fscmUI/redwood/performance/performance-document-types/performance-document-types-search). Resolve `{restBaseUrl}` from the active target Fusion environment and remove any trailing slash; never hard-code an environment URL. The link lets the user verify the data and must not be opened automatically or used to imply an import succeeded before Fusion reports success.

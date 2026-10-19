---
skill_id: "scm.procurement.self-service-procurement.manage-requisition-descriptive-flexfields"
name: "Manage Requisition Descriptive Flexfields Setup Task Guidance"
description: "Provides setup-data routing and Application Common descriptive-flexfield guidance for requisitions under the Self Service Procurement functional area."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Self Service Procurement"
functional_area_code: "PO_SSP_DEPLOYED"
task_code: "POR_MANAGE_REQUISITION_DESCRIPTIVE_FLEXFIELDS"
task_name: "Manage Requisition Descriptive Flexfields"
parent_skill_id: "scm.procurement.self-service-procurement"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM procurement pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "flexfield_change_request"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "flexfield_change_preview"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.apps-common"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.diagnostics.role-access-check"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/self-service-procurement/manage-requisition-descriptive-flexfields/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/self-service-procurement/manage-requisition-descriptive-flexfields/current/"
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

# Manage Requisition Descriptive Flexfields Setup Task Guidance

## Purpose

Provides setup-data routing and Application Common descriptive-flexfield guidance for requisitions under `Self Service Procurement`.

## Setup Task Skill Contract

- task_code: `POR_MANAGE_REQUISITION_DESCRIPTIVE_FLEXFIELDS`
- task_name: `Manage Requisition Descriptive Flexfields`
- parent_skill_id: `scm.procurement.self-service-procurement`
- pillar: `SCM`
- offering: `Procurement`
- functional_area: `Self Service Procurement`
- functional_area_code: `PO_SSP_DEPLOYED`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Requisition Descriptive Flexfields` under `Self Service Procurement`.

## Setup Task Metadata

- Task name: `Manage Requisition Descriptive Flexfields`
- Task code: `POR_MANAGE_REQUISITION_DESCRIPTIVE_FLEXFIELDS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the shared skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Validate referenced value sets and other reference data with `shared.validation.reference-data-validator` when applicable.
4. Import reviewed task setup data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Procurement`
- Functional area / Setup Object: `Self Service Procurement`
- Setup task name: `Manage Requisition Descriptive Flexfields`
- Setup task code: `POR_MANAGE_REQUISITION_DESCRIPTIVE_FLEXFIELDS`

## Application Common Descriptive Flexfield Routing

Route descriptive-flexfield requests for this task through `core.fusion-api.apps-common`. Identify the requested flexfield code explicitly; do not implement OAuth or REST transport in this task skill.

Use these flexfield codes:

- `POR_REQUISITION_HEADERS`
- `POR_REQUISITION_LINES`
- `POR_REQ_DISTRIBUTIONS`

For a change request, use the core skill's read-before-write, preview, and explicit approval gates. For DFF setup guidance, follow the descriptive-flexfield routing defined by `core.fusion-api.apps-common`.

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `flexfield_change_request`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `flexfield_change_preview`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `scm.procurement.self-service-procurement` for functional-area sequencing and scope decisions. Persist a redacted change preview, validation evidence, and any failure diagnostics in the task workspace outputs. Track token usage for any generated project artifact or skill-run record using the manifest policy.

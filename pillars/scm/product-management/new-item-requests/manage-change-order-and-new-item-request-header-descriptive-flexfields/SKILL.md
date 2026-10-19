---
skill_id: "scm.product-management.new-item-requests.manage-change-order-and-new-item-request-header-descriptive-flexfields"
name: "Manage Change Order and New Item Request Header Descriptive Flexfields Setup Task Guidance"
description: "Provides task-specific setup guidance and Application Common DFF routing for Manage Change Order and New Item Request Header Descriptive Flexfields under the New Item Requests functional area."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "New Item Requests"
functional_area_code: "EGO_NEW_ITEM_REQUESTS"
task_code: "EGO_MANAGE_CHANGE_ORDER_DFFS"
task_name: "Manage Change Order and New Item Request Header Descriptive Flexfields"
parent_skill_id: "scm.product-management.new-item-requests"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM product management pillar team"
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
  - "core.fusion-api.apps-common"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/new-item-requests/manage-change-order-and-new-item-request-header-descriptive-flexfields/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/new-item-requests/manage-change-order-and-new-item-request-header-descriptive-flexfields/current/"
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

# Manage Change Order and New Item Request Header Descriptive Flexfields Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Change Order and New Item Request Header Descriptive Flexfields` under `New Item Requests`.

## Setup Task Skill Contract

- task_code: `EGO_MANAGE_CHANGE_ORDER_DFFS`
- task_name: `Manage Change Order and New Item Request Header Descriptive Flexfields`
- parent_skill_id: `scm.product-management.new-item-requests`
- pillar: `SCM`
- offering: `Product Management`
- functional_area: `New Item Requests`
- functional_area_code: `EGO_NEW_ITEM_REQUESTS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Change Order and New Item Request Header Descriptive Flexfields` under `New Item Requests`.

## Apps Common Routing

Route every Change Order and New Item Request Header DFF request through
`core.fusion-api.apps-common` as a Descriptive Flexfield request with:

- Flexfield code: `EGO_ENGINEERING_CHANGES`
- Setup task code: `EGO_MANAGE_CHANGE_ORDER_DFFS`
- Offering: `Product Management`
- Functional area: `New Item Requests`

Pass the flexfield code with the task context for DFF discovery, export, and
validation. The core skill selects its Descriptive Flexfields route; this task
skill must not implement OAuth or direct REST transport.

For baseline capture, use `shared.setup-export.task-level-export`. For import,
route the immutable `EGO_ENGINEERING_CHANGES` FSM package only through
`core.data-loader`. Let its Task Hook validation and approval-preview lifecycle
bind the confirmed target environment, exact archive, task context, and intended
change; do not invoke `setupTaskCSVImports`, another import endpoint, or a
shared task-level import runner directly, or request a separate pillar-level
approval.

## Setup Task Metadata

- Task name: `Manage Change Order and New Item Request Header Descriptive Flexfields`
- Task code: `EGO_MANAGE_CHANGE_ORDER_DFFS`
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

- Offering: `Product Management`
- Functional area / Setup Object: `New Item Requests`
- Setup task name: `Manage Change Order and New Item Request Header Descriptive Flexfields`
- Setup task code: `EGO_MANAGE_CHANGE_ORDER_DFFS`
- Flexfield code: `EGO_ENGINEERING_CHANGES`




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

Use the parent functional-area skill `scm.product-management.new-item-requests` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

---
skill_id: "scm.order-management.orders.manage-business-event-trigger-points"
name: "Manage Business Event Trigger Points Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Business Event Trigger Points under the Orders functional area."
layer: "pillar"
pillar: "SCM"
offering: "Order Management"
functional_area: "Orders"
functional_area_code: "ORA_DOO_ORDER_FULLFILLMENT"
task_code: "ORA_DOO_MANAGE_BUSINESS_EVENT_TRIGGER_POINTS"
task_name: "Manage Business Event Trigger Points"
parent_skill_id: "scm.order-management.orders"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObjects:
  - "eventDetails"
  - "connectors"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM order management pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/orders/manage-business-event-trigger-points/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/orders/manage-business-event-trigger-points/current/"
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

# Manage Business Event Trigger Points Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Business Event Trigger Points` under `Orders`.

## Setup Task Skill Contract

- task_code: `ORA_DOO_MANAGE_BUSINESS_EVENT_TRIGGER_POINTS`
- task_name: `Manage Business Event Trigger Points`
- parent_skill_id: `scm.order-management.orders`
- pillar: `SCM`
- offering: `Order Management`
- functional_area: `Orders`
- functional_area_code: `ORA_DOO_ORDER_FULLFILLMENT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObjects: `eventDetails`; `connectors` when a connector or service is specified
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business objects.

1. Select the exact registered REST Data Loader business object: use `eventDetails` for event-detail configuration, or `connectors` whenever the requested setup data specifies a connector or service.
2. Generate the default editable XLSX samples through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "<eventDetails-or-connectors>" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep each business object's generated workbook set together:
   - editable sample workbook
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbooks as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Business Event Trigger Points` under `Orders`.

## Setup Task Metadata

- Task name: `Manage Business Event Trigger Points`
- Task code: `ORA_DOO_MANAGE_BUSINESS_EVENT_TRIGGER_POINTS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Objects: `eventDetails`; `connectors` when a connector or service is specified

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using REST business object `eventDetails`, except use `connectors` whenever the requested setup data specifies a connector or service.

For `ORDER_ATTRIBUTE_UPDATE`, prepare distinct `eventDetails` rows. The parent event row has `EventCriteriaId` `-1`; prepare it and set its `EventEnabledFlag` only when the user explicitly asks to enable or inactivate that parent event. Attribute activity must never implicitly enable or inactivate the parent row. Each supplied triggering attribute produces a separate attribute row. Resolve every attribute through `omBusinessEventDetails/ORDER_ATTRIBUTE_UPDATE/child/eventOrderAttributesLOV`, match `AttributeName` exactly, and use the matched `EventCriteriaId`. For an add request, set `EventEnabledFlag` to `true` on every new attribute row as its implicit enablement. For a removal request, retain every matched attribute row and set its `EventEnabledFlag` to `false`; never delete the row. Before adding or re-adding attributes, resolve the configured attribute rows and compare `EventCriteriaId` values per requested attribute: create a new row with `EventEnabledFlag` `true` when no configured row exists; set the flag to `true` when the configured row is `false`; and report a duplicate without preparing an import row when it is already `true`. Stop only on an incomplete or ambiguous configured-row result. Do not treat an attribute row as the explicit parent-event enablement row.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Orders`
- Setup task name: `Manage Business Event Trigger Points`
- Setup task code: `ORA_DOO_MANAGE_BUSINESS_EVENT_TRIGGER_POINTS`




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

Use the parent functional-area skill `scm.order-management.orders` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

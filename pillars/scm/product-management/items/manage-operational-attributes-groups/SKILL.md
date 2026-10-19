---
skill_id: "scm.product-management.items.manage-operational-attributes-groups"
name: "Manage Operational Attributes Groups Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Operational Attributes Groups under the Items functional area."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "Items"
functional_area_code: "ORA_EGP_FA_ITEMS"
task_code: "EGP_MANAGE_OPERATIONAL_ATTRIBUTES_GROUPS"
task_name: "Manage Operational Attributes Groups"
parent_skill_id: "scm.product-management.items"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "itemOperationalAttributeControlLevels"
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
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
uses_core:
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/items/manage-operational-attributes-groups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/items/manage-operational-attributes-groups/current/"
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

# Manage Operational Attributes Groups Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Operational Attributes Groups` under `Items`.

## Setup Task Skill Contract

- task_code: `EGP_MANAGE_OPERATIONAL_ATTRIBUTES_GROUPS`
- task_name: `Manage Operational Attributes Groups`
- parent_skill_id: `scm.product-management.items`
- pillar: `SCM`
- offering: `Product Management`
- functional_area: `Items`
- functional_area_code: `ORA_EGP_FA_ITEMS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `itemOperationalAttributeControlLevels`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Operational Attributes Groups` under `Items`.

## Required User Input

Before preparing a task plan, collect the following information from the user:

- The implementation objective and whether the request is for planning, export, import preparation, or validation.
- The target project context, including the project ID when durable artifacts or run records are required.
- The intended setup-task scope, including whether the work applies to an existing configuration or a new configuration.
- Any available setup-data artifacts, such as exported CSV files, source workbooks, or validation results.

Do not infer missing business values, target-environment details, or source-data content. Request the missing input before routing the task to export, validation, sample generation, or import preparation.

## Setup Task Metadata

- Task name: `Manage Operational Attributes Groups`
- Task code: `EGP_MANAGE_OPERATIONAL_ATTRIBUTES_GROUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `itemOperationalAttributeControlLevels`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using itemOperationalAttributeControlLevels as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Product Management`
- Functional area / Setup Object: `Items`
- Setup task name: `Manage Operational Attributes Groups`
- Setup task code: `EGP_MANAGE_OPERATIONAL_ATTRIBUTES_GROUPS`


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `itemOperationalAttributeControlLevels` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "itemOperationalAttributeControlLevels" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## REST Operation Guardrail

Delegate every Fusion REST lookup and any approved update exclusively to `core.fusion-api.rest-api-client`. This skill owns only the SCM-specific identity, validation, approval, and postcondition rules; it must not implement REST transport, OAuth, retry, response redaction, or diagnostics.

For `itemOperationalAttributeControlLevels`, the permitted REST operation is **PATCH only**. Do not prepare or execute `POST`, `PUT`, `DELETE`, or any other HTTP method through this skill. Validate the target record identity and present the exact PATCH payload for approval before delegating a live update to `core.fusion-api.rest-api-client`.

For delegated item-level reads and PATCH requests, require `REST-Framework-Version: 9`. Resolve the record first with that header, then use the Fusion-issued composite-key item link returned by the versioned response (for example, `{AttrGroupName}%2C{AttrName}`). Do not use an item link returned by an unversioned collection response without first validating it with a versioned item-level GET. If an item-level request returns `404`, do not retry the PATCH; validate the versioned composite-key route read-only through `core.fusion-api.rest-api-client`, prepare a new preview, and obtain fresh approval.



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

Use the parent functional-area skill `scm.product-management.items` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

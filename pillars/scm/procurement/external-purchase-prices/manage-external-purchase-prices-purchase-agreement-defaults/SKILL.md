---
skill_id: "scm.procurement.external-purchase-prices.manage-external-purchase-prices-purchase-agreement-defaults"
name: "Manage External Purchase Prices Purchase Agreement Defaults Setup Task Guidance"
description: "Retrieves purchase agreement defaults through direct read-only REST and routes maintenance exclusively through Data Loader."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "External Purchase Prices"
functional_area_code: "ORA_EXTERNAL_PURCHASE_PRICES"
task_code: "ORA_MANAGE_EXTERNAL_PURCHASE_PRICES_PA_DEFAULTS"
task_name: "Manage External Purchase Prices Purchase Agreement Defaults"
parent_skill_id: "scm.procurement.external-purchase-prices"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "externalPurchasePricesPurchaseAgreementDefaults"
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
  - "purchase_agreement_defaults_query"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
  - "purchase_agreement_defaults_read_result"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/external-purchase-prices/manage-external-purchase-prices-purchase-agreement-defaults/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/external-purchase-prices/manage-external-purchase-prices-purchase-agreement-defaults/current/"
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
side_effects:
  - "Uses core.fusion-api.rest-api-client for selected read-only GET requests."
  - "Routes imports and all mutations to core.data-loader."
required_privileges:
  - "Read privileges for current default-record retrieval."
  - "Applicable Procurement maintenance privileges for Data Loader-routed mutations."
---

# Manage External Purchase Prices Purchase Agreement Defaults Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage External Purchase Prices Purchase Agreement Defaults` under `External Purchase Prices`.

## Setup Task Skill Contract

- task_code: `ORA_MANAGE_EXTERNAL_PURCHASE_PRICES_PA_DEFAULTS`
- task_name: `Manage External Purchase Prices Purchase Agreement Defaults`
- parent_skill_id: `scm.procurement.external-purchase-prices`
- pillar: `SCM`
- offering: `Procurement`
- functional_area: `External Purchase Prices`
- functional_area_code: `ORA_EXTERNAL_PURCHASE_PRICES`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `externalPurchasePricesPurchaseAgreementDefaults`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage External Purchase Prices Purchase Agreement Defaults` under `External Purchase Prices`.

## Operation Routing

| Requested Outcome | Execution Route | Completion |
|---|---|---|
| Retrieve current default records (GET) | core.fusion-api.rest-api-client | Return current details or confirmed not-found; do not invoke Data Loader |
| Create, update, or delete defaults (POST, PATCH, DELETE) | core.data-loader | Validate the exact artifact and obtain the required approval before mutation |
| Read state during a selected mutation workflow | core.fusion-api.rest-api-client | Return read evidence only; a GET never authorizes a write |
| Generate a template, validate a file, check a load, or export | Existing template, loader-status, or export workflow | Do not classify as record retrieval |

The Data Loader dependency is conditional on import work, not GET. Never route a pure record read through Data Loader, Task Hook, or a loader validator.

## Read-Only Defaults Workflow

1. Select the active project and environment. Require an exact default-record identity or finite filter in `purchase_agreement_defaults_query`; never infer a create operation.
2. Confirm task identity, read privileges, safe evidence destination, and a finite read budget.
3. Read [Core REST API Client](../../../../../core/fusion-api/rest-api-client/SKILL.md) and use only the workflow-selected GET path. Do not construct a write request.
4. Resolve complete paginated results and return current values or confirmed not-found. Partial, ambiguous, or inaccessible results are issues.
5. Do not stage an artifact, request mutation approval, upload, initiate a load, or fall back to Data Loader if the GET fails.

## Setup Task Metadata

- Task name: `Manage External Purchase Prices Purchase Agreement Defaults`
- Task code: `ORA_MANAGE_EXTERNAL_PURCHASE_PRICES_PA_DEFAULTS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `externalPurchasePricesPurchaseAgreementDefaults`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `externalPurchasePricesPurchaseAgreementDefaults` as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Procurement`
- Functional area / Setup Object: `External Purchase Prices`
- Setup task name: `Manage External Purchase Prices Purchase Agreement Defaults`
- Setup task code: `ORA_MANAGE_EXTERNAL_PURCHASE_PRICES_PA_DEFAULTS`


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `externalPurchasePricesPurchaseAgreementDefaults` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "externalPurchasePricesPurchaseAgreementDefaults" \
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
- `purchase_agreement_defaults_query`: read-only identity or filters; required for a record retrieval, not loader work

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`
- `purchase_agreement_defaults_read_result`: current details or confirmed not-found; read-only route only

## Implementation Notes

Use the parent functional-area skill `scm.procurement.external-purchase-prices` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

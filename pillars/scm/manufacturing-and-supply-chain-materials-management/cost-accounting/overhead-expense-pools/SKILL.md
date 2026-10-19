---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.cost-accounting.overhead-expense-pools"
name: "Overhead Expense Pools Setup Task Guidance"
description: "Provides task-specific setup guidance for Overhead Expense Pools under the Cost Accounting functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Cost Accounting"
functional_area_code: "CST_DEFINE_COST_MANAGEMENT"
task_code: "ORA_CST_OVERHEAD_EXPENSE_POOLS"
task_name: "Overhead Expense Pools"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.cost-accounting"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "costAccountingOverheadExpensePools"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM manufacturing and supply chain materials management pillar team"
version: "0.1.1"
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
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/overhead-expense-pools/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/overhead-expense-pools/current/"
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

# Overhead Expense Pools Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Overhead Expense Pools` under `Cost Accounting`.

## Setup Task Skill Contract

- task_code: `ORA_CST_OVERHEAD_EXPENSE_POOLS`
- task_name: `Overhead Expense Pools`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.cost-accounting`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Cost Accounting`
- functional_area_code: `CST_DEFINE_COST_MANAGEMENT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `costAccountingOverheadExpensePools`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Overhead Expense Pools` under `Cost Accounting`.

## Setup Task Metadata

- Task name: `Overhead Expense Pools`
- Task code: `ORA_CST_OVERHEAD_EXPENSE_POOLS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `costAccountingOverheadExpensePools`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using costAccountingOverheadExpensePools as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Cost Accounting`
- Setup task name: `Overhead Expense Pools`
- Setup task code: `ORA_CST_OVERHEAD_EXPENSE_POOLS`


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `costAccountingOverheadExpensePools` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "costAccountingOverheadExpensePools" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

### Data Loader Source Completeness Gate

Prepare every populated `costAccountingOverheadExpensePools` JSON row as a complete source record before invoking `generate_sample_dat.py --populate-json`. `RestAction` is mandatory alongside the operation's required fields; it is not a generator default and it must not be added after source preparation.

For `InactiveFlag`, the only accepted stored values are uppercase `Y` and `N`. Normalize user terms before source preparation: `Y`/`y`, `true`, and `inactive` become `Y`; `N`/`n`, `false`, and `active` become `N`. Reject every other supplied value. The field is optional: source records may omit it and no default is applied.

| User intent | Generator operation | Required `RestAction` |
|---|---|---|
| Create | `create` | `POST` |
| Update | `update` | `PATCH` |
| Delete | `delete` | `DELETE` |

Use only resolver outputs in the prepared source: use the resolved `ExpensePoolTypeCode` and `SetId`, never the user's `SetName`, `SetId`, or `SetCode` input. Require these fields in addition to `RestAction`:

| Operation | Required prepared-source fields |
|---|---|
| Create | `ExpensePoolCode`, resolved `ExpensePoolTypeCode`, resolved `SetId`, `RestAction=POST`; when supplied, normalized `InactiveFlag` (`Y` or `N`) |
| Update | `ExpensePoolCode`, at least one supplied and validated mutable change field other than immutable SetName or SetId, `RestAction=PATCH` |
| Delete | verified `ExpensePoolCode`, `RestAction=DELETE`; do not include a mutable attribute or target qualifier |

Before preview, inspect the generated workbook rather than only the JSON. Reject the draft when any required field or `RestAction` is missing, blank, or mismatched with the requested operation; correct the prepared source and regenerate the workbook before Data Loader validation, upload, or initiation.

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

Use the parent functional-area skill `scm.manufacturing-and-supply-chain-materials-management.cost-accounting` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

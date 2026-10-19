---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.cost-accounting.manage-costing-lookups"
name: "Manage Costing Lookups Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Costing Lookups under the Cost Accounting functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Cost Accounting"
functional_area_code: "CST_DEFINE_COST_MANAGEMENT"
task_code: "ORA_CST_COSTING_LOOKUPS"
task_name: "Manage Costing Lookups"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.cost-accounting"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM manufacturing and supply chain materials management pillar team"
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
  - "core.fusion-api.apps-common"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/manage-costing-lookups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/manage-costing-lookups/current/"
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

# Manage Costing Lookups Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Costing Lookups` under `Cost Accounting`.

## Setup Task Skill Contract

- task_code: `ORA_CST_COSTING_LOOKUPS`
- task_name: `Manage Costing Lookups`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.cost-accounting`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Cost Accounting`
- functional_area_code: `CST_DEFINE_COST_MANAGEMENT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Costing Lookups` under `Cost Accounting`.

## Setup Task Metadata

- Task name: `Manage Costing Lookups`
- Task code: `ORA_CST_COSTING_LOOKUPS`
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

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Cost Accounting`
- Setup task name: `Manage Costing Lookups`
- Setup task code: `ORA_CST_COSTING_LOOKUPS`

## Apps Common Lookup Workflow

Route every `Manage Costing Lookups` request to
`core.fusion-api.apps-common`. Apps Common selects its `lookups` nested skill
and the Standard Lookups workflow for Costing lookup type and lookup-code
operations. This task must not bypass Apps Common by selecting a REST client or
its nested lookup skill directly.

1. Confirm that the requested `LookupType` is in the Costing lookup type list
   in this task skill.
2. Read the current lookup type or lookup code and verify its returned identity
   before proposing a change.
3. For a create, update, or delete, present the exact environment, lookup type,
   lookup code when applicable, current state, and proposed change for explicit
   approval immediately before the write.
4. Do not retry a lookup POST, PATCH, or DELETE automatically.

The generated CSV/FSM workflow remains available only for catalog-supported
setup-data export and import artifacts. It does not replace the Apps Common
route for Costing lookup definition or lookup-code requests.

## Costing Lookup Type Codes

Use the lookup type exactly as listed. Confirm its current definition and
lookup-code state at runtime because availability, active dates, and values can
vary by environment and release.

### `CST_*`

- `CST_ABSORPTION_TYPE`
- `CST_ACCOUNTING_STATUS`
- `CST_COMPONENT_CODES`
- `CST_COMPONENT_SOURCES`
- `CST_COMP_CODES_FOR_TXN_ENTRY`
- `CST_COSTING_ATTRIBUTES`
- `CST_COST_BY_UOM_CODES`
- `CST_COST_CUTOFF_FLAG`
- `CST_COST_DRIVER`
- `CST_COST_ELEMENT_TYPES`
- `CST_COST_METHODS`
- `CST_COST_STATUS`
- `CST_INTF_PROC_STATUS`
- `CST_ITEM_PROF_APPRV_STATUSES`
- `CST_MASS_EDIT_LEVEL`
- `CST_MASS_EDIT_TYPE`
- `CST_MASS_EDIT_VALUE_TYPE`
- `CST_NEGATIVE_QUANTITY_CODES`
- `CST_OVRUL_STATUS`
- `CST_PERIOD_STATUSES`
- `CST_PERIOD_VALIDATION_ACTIONS`
- `CST_PERIOD_VALIDATION_TYPES`
- `CST_PROCESSOR_NAME`
- `CST_PROFILE_CREATION_CODES`
- `CST_PROFILE_CREATION_SOURCES`
- `CST_QUANTITY_FLOW`
- `CST_QUANTITY_FLOW_CODES`
- `CST_REASON_CODES`
- `CST_RECEIPT_WITHOUT_COST`
- `CST_REFERENCED_RMA_COST`
- `CST_STD_COST_ATTRIBUTE_TYPES`
- `CST_TRANSACTION_GROUPS`
- `CST_VALUATION_STRUCTURE_MODES`
- `CST_VALUATION_STRUCTURE_TYPES`
- `CST_VARIANCE_TYPES`

### `ORA_CST_*`

- `ORA_CST_ABSORPTION_BASIS_DTLS`
- `ORA_CST_ABSORPTION_LEVEL_DTLS`
- `ORA_CST_ABSORPTION_TYPE`
- `ORA_CST_COMPARISON_SCOPE`
- `ORA_CST_COMPONENT_COST_TYPE`
- `ORA_CST_CONFIG_ROLLUP_SCOPE`
- `ORA_CST_CONSIGN_ACCT_DIS_BASIS`
- `ORA_CST_COST_BOOK_OPTIONS`
- `ORA_CST_COST_COMPARE_OPTIONS`
- `ORA_CST_COST_COMPARE_VIEW`
- `ORA_CST_COST_LEVEL`
- `ORA_CST_DCOGS_AGE`
- `ORA_CST_DOC_FLOW_TYPES`
- `ORA_CST_EVENT_CREATION_STATUS`
- `ORA_CST_EXPENSE_POOL_TYPES`
- `ORA_CST_EXPLOSION_BASIS`
- `ORA_CST_INV_OR_COSTED_VAL`
- `ORA_CST_INV_VAL_VIEW_BY`
- `ORA_CST_MSG_TYPE`
- `ORA_CST_OH_ACTION_TYPE`
- `ORA_CST_OPERATION_SCRAP`
- `ORA_CST_OP_SCRAP_VALUATION`
- `ORA_CST_ORGANIZATION_CONTEXT`
- `ORA_CST_OVERHEAD_RATE_TYPE`
- `ORA_CST_OVRUL_REV_PROCESSED`
- `ORA_CST_PAC_ADJUSTMENT_TYPE`
- `ORA_CST_PAC_ADJ_DATE_RANGE`
- `ORA_CST_PAC_ADJ_PROCESSED_FLAG`
- `ORA_CST_PARTIAL_COMPLETION`
- `ORA_CST_PERIOD_CLOSE_AT`
- `ORA_CST_PLN_PROCEESED_FLAG`
- `ORA_CST_PUBLISH_STATUS`
- `ORA_CST_RCAD_SEARCH_BY`
- `ORA_CST_REVIEW_ABSORPTION_FLAG`
- `ORA_CST_ROLLUP_DETAIL_TYPE`
- `ORA_CST_ROLLUP_SCOPE`
- `ORA_CST_RUNCONTROL_RQST_STATUS`
- `ORA_CST_SCENARIO_REASON_CODE`
- `ORA_CST_SCENARIO_STATE`
- `ORA_CST_SCENARIO_STATUS`
- `ORA_CST_SCENARIO_STATUS_SMPL`
- `ORA_CST_SCENARIO_TYPES`
- `ORA_CST_SCENARIO_VERSION_TYPES`
- `ORA_CST_SELECTION_CRITERIA`
- `ORA_CST_STD_COST_LEVEL`
- `ORA_CST_STD_COST_SOURCES`
- `ORA_CST_STD_COST_STATUSES`
- `ORA_CST_SVC_COST_RECOG_SRC`
- `ORA_CST_SVC_COST_REP_FORMAT`
- `ORA_CST_TRANSACTION_FLOW_TYPES`
- `ORA_CST_TRANSFER_CHARGE_TYPE`
- `ORA_CST_UNREFERENCED_RMA_COST`
- `ORA_CST_WIP_VARIANCE_TYPES`
- `ORA_CST_WIP_VARIANCE_TYPES_PM`




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

---
skill_id: "scm.order-management.orders.manage-order-lookups"
name: "Manage Order Lookups Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Order Lookups under the Orders functional area."
layer: "pillar"
pillar: "SCM"
offering: "Order Management"
functional_area: "Orders"
functional_area_code: "ORA_DOO_ORDER_FULLFILLMENT"
task_code: "DOO_MANAGE_ORCHESTRATION_LOOKUPS"
task_name: "Manage Order Lookups"
parent_skill_id: "scm.order-management.orders"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
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
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/orders/manage-order-lookups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/orders/manage-order-lookups/current/"
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

# Manage Order Lookups Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Order Lookups` under `Orders`.

## Setup Task Skill Contract

- task_code: `DOO_MANAGE_ORCHESTRATION_LOOKUPS`
- task_name: `Manage Order Lookups`
- parent_skill_id: `scm.order-management.orders`
- pillar: `SCM`
- offering: `Order Management`
- functional_area: `Orders`
- functional_area_code: `ORA_DOO_ORDER_FULLFILLMENT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Order Lookups` under `Orders`.

## Setup Task Metadata

- Task name: `Manage Order Lookups`
- Task code: `DOO_MANAGE_ORCHESTRATION_LOOKUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Apps Common Lookup Routing

Route each Manage Order Lookups request to `core.fusion-api.apps-common` with
the lookup request context. The Apps Common router must select its `lookups`
nested skill and the appropriate common, standard, generic, or set-enabled
lookup workflow. Do not select a direct REST endpoint from this task skill.

Pass only the following Order Management lookup types to the routed request.

### User Extensible Lookups

- `ORA_DOO_FS_RESP_REC_SET_OPT`
- `ORA_DOO_PURGE_REC_SET_OPT`
- `ORA_DOO_LINE_TYPES`
- `ORA_DOO_RETURN_LINE_TYPES`
- `ORA_DOO_DEMAND_CLASS`
- `ORA_DOO_TRADE_CONTROL_CODE`
- `ORA_DOO_ORDER_LINE_CATEGORY`
- `ORA_DOO_ADJ_PARENT_ENTITY_TYPE`
- `ORA_DOO_ORDER_TYPES`
- `ORA_DOO_DFLT_TAX_DETERMINANTS`
- `DOO_ACTIVITY_TYPE`
- `DOO_SUBSTITUTION_REASON`
- `DOO_SCHEDULE_REASON`
- `DOO_MSG_REQUEST_FUNCTION`
- `DOO_RETURN_REASON`
- `DOO_HLD_RELEASE_REASON`

### System Lookups

- `ORA_DOO_REQUEST_TYPE`
- `ORA_DOO_ORDERS_WATCHLIST`
- `ORA_DOO_DUOM_RETURN_QTY_TYPE`
- `ORA_DOO_INCL_ITEM_EXP_DATE`
- `ORA_DOO_CLOSE_ORDER_AGE`
- `ORA_DOO_CLOSE_ORDER_AGE_UOM`
- `ORA_DOO_CLOSE_ORDER_SCOPE`
- `ORA_DOO_ORDER_HDR_STATUS`
- `ORA_DOO_ITEM_SUB_TYPE_CODE`
- `ORA_DOO_PROCESS_DEPLOY_CHECK`
- `ORA_DOO_REL_TYPE_SHIP_TO`
- `ORA_DOO_CONFIG_EFFEC_DATE`
- `ORA_DOO_CUST_REL_TYPE`
- `ORA_DOO_INTERFACE_STATUS`
- `ORA_DOO_BILLING_FREQUENCY_CODE`
- `ORA_DOO_BILLING_PLAN_TYPE_CODE`
- `ORA_DOO_COVERAGE_START_DATE`
- `ORA_DOO_RETRY_PAUSE`
- `ORA_DOO_PAUSE_MANUAL_RELEASE`
- `ORA_DOO_FULFILLMENT_MODE`
- `ORA_DOO_TP_STATUS`
- `ORA_DOO_ERROR_RECOVERY_SCOPE`
- `ORA_DOO_HOLD_APPLICABLE_ROLE`
- `ORA_DOO_TRADE_COMPLIANCE_TYPE`
- `ORA_DOO_TL_USER_NOTE`
- `ORA_DOO_EXTENSION_USAGE`
- `ORA_DOO_INVOCATION_MODE`
- `ORA_DOO_VALIDATION_RESULT`
- `ORA_DOO_RESPONSE_PROCESS_OPTNS`
- `ORA_DOO_REPLAN_INSTANCES`
- `ORA_DOO_EXTENSION_EVENT`
- `ORA_DOO_REDO_PROMISE_DATES`
- `ORA_DOO_SOURCE_DOC_TYPE_CODE`
- `ORA_DOO_SUMMARY_TIME_INTERVALS`
- `ORA_DOO_SUPPLY_STATUS_CODE`
- `DOO_ATTACHMENT_SOURCE`
- `DOO_MSG_ENTITY_TYPE`
- `DOO_SOURCE_ORDER_STATUS`
- `DOO_PC_ON_OPERATION_ACTION`
- `DOO_PC_OPERATION`
- `DOO_PC_SCOPE_OP`
- `DOO_PC_VALIDATION_OP`
- `DOO_PC_VALIDATION_TYPE`
- `DOO_PROC_SPLIT_DISPLAY`
- `DOO_JEOPARDY_PRIORITY_CODE`
- `DOO_LEAD_TIME_UOM`
- `DOO_OPERATION_CODE`
- `DOO_PARENT_NAME`
- `DOO_PROCESS_ACTIVE`
- `DOO_PROCESS_RELEASE_STATUS_CD`
- `DOO_STEP_ACTIVE`
- `DOO_USER_ACTION_STATUS`
- `DOO_WB_ACTION_CODE`
- `DOO_CHANGE_MODE`
- `DOO_STEP_STATUS`
- `DOO_STEP_TYPE_CODE`
- `DOO_LINE_CATEGORY`
- `DOO_COMMON_YES_NO_NA`
- `DOO_STAT_DFLT_CATEGORY`
- `DOO_MSG_REQUEST_RESULT`
- `DOO_PC_ENTITY_TYPE`
- `DOO_EVENT_TRIGGER_POINTS`
- `DOO_SUBTYPE_CODE`
- `DOO_ADJUSTMENT_TYPE`
- `DOO_ANALYTIC_PIECHART`
- `DOO_DEFAULT_DISPLAY_VALUES`
- `DOO_EXCEPTION_TYPES`
- `DOO_FLINES_WATCHLIST`
- `DOO_PROCESSES_WATCHLIST`
- `DOO_RECENT_OBJECT_TYPES`

### Category Enforcement

Only lookup types under **User Extensible Lookups** may be extended through
this task.

Treat lookup types under **System Lookups** as system-managed. Do not add,
delete, or change the identity of their lookup codes through this task. Allow
updates only to `Meaning`, `Description`, and `DisplaySequence`.

### ORA_DOO_ORDER_TYPES Guidance

For `ORA_DOO_ORDER_TYPES`, use Oracle's [Manage Order Management's Lookups —
26c](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faiom/manage-lookups-in-order-management.html)
and [Use Groups to Manage and Control Sales Orders —
26c](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faiom/use-groups-to-manage-and-control-sales-orders.html#Set-Up-Order-Types)
as functional guidance sources. Apply them together with the Apps Common lookup
workflow when reviewing or changing order-type lookup codes.

### DOO_RETURN_REASON Guidance

For `DOO_RETURN_REASON`, use Oracle's [Create Return Reasons —
26c](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faiom/create-a-return-reason.html)
as the functional guidance source. Apply it together with the Apps Common
lookup workflow when reviewing or changing return-reason lookup codes.

### ORA_DOO_RETURN_LINE_TYPES Guidance

For `ORA_DOO_RETURN_LINE_TYPES`, use Oracle's [Return Sales Orders Without
Credit Memo — 26c](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faiom/return-sales-orders-without-credit-memo.html#Set-up-the-Lookup)
as the functional guidance source. Apply it together with the Apps Common
lookup workflow when reviewing or changing return-line-type lookup codes.

### Trade Compliance and Trade Control Guidance

For `ORA_DOO_TRADE_COMPLIANCE_TYPE` and `ORA_DOO_TRADE_CONTROL_CODE`, use
Oracle's [Set Up Trade Control Types —
26c](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faiom/set-up-trade-control-types.html)
as the functional guidance source. Apply the page's trade-compliance setup
guidance together with the Apps Common lookup workflow when reviewing these
lookup types or proposing changes to their codes.

For any allowed lookup change, use the selected lookup workflow's discovery
and resource-identity checks, read the current lookup resource, and obtain
explicit approval immediately before the mutation.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Orders`
- Setup task name: `Manage Order Lookups`
- Setup task code: `DOO_MANAGE_ORCHESTRATION_LOOKUPS`




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

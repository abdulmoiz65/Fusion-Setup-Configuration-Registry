---
skill_id: "scm.order-management.orders.manage-order-profiles"
name: "Manage Order Profiles Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Order Profiles under the Orders functional area."
layer: "pillar"
pillar: "SCM"
offering: "Order Management"
functional_area: "Orders"
functional_area_code: "ORA_DOO_ORDER_FULLFILLMENT"
task_code: "DOO_MANAGE_ORCHESTRATION_PROFILES"
task_name: "Manage Order Profiles"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/orders/manage-order-profiles/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/orders/manage-order-profiles/current/"
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

# Manage Order Profiles Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Order Profiles` under `Orders`.

## Setup Task Skill Contract

- task_code: `DOO_MANAGE_ORCHESTRATION_PROFILES`
- task_name: `Manage Order Profiles`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Order Profiles` under `Orders`.

## Setup Task Metadata

- Task name: `Manage Order Profiles`
- Task code: `DOO_MANAGE_ORCHESTRATION_PROFILES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Oracle Guidance Sources

Use Oracle's [Use Order Profiles to Control Order Management's Behavior —
26c](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faiom/use-order-profiles-to-control-order-management-behavior.html#Manage-Order-Profiles)
as the functional guidance source for profile-value behavior, hierarchy, and
level-specific configuration decisions.

### Recovery Profiles

For `ORA_FOM_TOTAL_LINES_EACH_HOUR` and
`ORA_FOM_PERCENT_ERROR_LINES_EACH_HOUR`, use Oracle's [Fix Errors in All Sales
Orders —
26c](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faiom/fix-errors-in-all-sales-orders.html#Use-Profile-Options-to-Control-Recovery).
Apply the two profile options together when controlling the Recover Errors
scheduled process, and assess performance before raising the recovery volume.

### Source Order Number Profile

For `DOO_RT_USE_ORDER_NUMBER`, use Oracle's [Keep Your Order Number When You
Import —
26c](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faiom/retain-sales-order-number-during-import.html#Use-the-Number-From-Your-Source-System).
Validate source-order-number uniqueness and the import behavior before enabling
use of the source-system number.

## Apps Common Profile Option Routing

Route each Manage Order Profiles request to `core.fusion-api.apps-common` with
the profile-option request context. The Apps Common router must select its
`profile-options` nested skill. Do not select a direct REST endpoint from this
task skill.

Pass only these Profile Option Codes to the routed request:

- `ORA_DOO_SKIP_AVAILABILITY`
- `ORA_DOO_SKIP_PRICE_VAL`
- `ORA_DOO_ENHANCED_REVISION`
- `ORA_DOO_DS_FDTL_AR_MAPPING`
- `ORA_DOO_RECOMPUTE_PROMISE_DATE`
- `ORA_DOO_ALLOW_DIFF_BU_REF_RTN`
- `ORA_DOO_AGGR_HOLD_TIMEOUT`
- `ORA_DOO_ENABLE_AGGR_V2`
- `ORA_DOO_FULFILLMENT_TASK_RETRIES`
- `ORA_DOO_LOG_ENABLED`
- `ORA_DOO_LOG_LEVEL`
- `ORA_FOM_ORCH_PROCESS_BATCH_SIZE`
- `ORA_FOM_DEFAULT_ADJ_REASON`
- `ORA_FOM_SHOW_MARGIN`
- `ORA_FOM_ENABLE_CARD_PAYMENT`
- `ORA_FOM_CPA_AGENT_WORKFLOW_ACCESS`
- `ORA_FOM_RESPOND_ON_SUBMISSION_START`
- `ORA_FOM_COPY_EFF_ON_CPLN`
- `ORA_FOM_DEFAULT_BUSINESS_UNIT`
- `ORA_FOM_SET_FULFILLMENT_DATE`
- `ORA_FOM_POPULATE_VALUES_ON_SPLIT_LINE`
- `ORA_FOM_GET_CUSTOMER_ITEM`
- `ORA_FOM_TRADE_COMPLIANCE_HEADER_STATUS`
- `ORA_FOM_PERCENT_ERROR_LINES_EACH_HOUR`
- `ORA_FOM_TOTAL_LINES_EACH_HOUR`
- `ORA_FOM_WAIT_TO_PROCESS_SUBS_UPDATES`
- `ORA_FOM_REDESIGNED_MANAGE_EXT_INT_WS_DETAILS`
- `ORA_FOM_RW_MANAGE_BUSINESS_EVENTS`
- `ORA_FOM_RW_MANAGE_HOLD_CODES`
- `ORA_FOM_SEND_KIT_STRUCTURE`
- `ORA_FOM_COMMAND_CENTER_AGENTIC_APP_ENABLED`
- `DOO_CURRENCY_CONVERSION_TYPE`
- `DOO_DISPLAY_CURRENCY`
- `DOO_OVERVIEW_REQ_USER_FILTER`
- `DOO_RT_USE_ORDER_NUMBER`
- `DOO_USER_REQUEST_WAIT_PERIOD`

For a read request, validate the profile definition and effective or configured
value target through the selected profile-options workflow. For a create,
update, or delete request, read the current value and obtain explicit approval
immediately before the mutation.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Orders`
- Setup task name: `Manage Order Profiles`
- Setup task code: `DOO_MANAGE_ORCHESTRATION_PROFILES`




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

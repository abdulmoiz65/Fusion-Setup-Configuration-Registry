---
skill_id: "erp.financials.customer-billing.manage-autoaccounting-rules"
name: "Manage AutoAccounting Rules Setup Task Guidance"
description: "Handles natural-language AutoAccounting requests for exact Receivables business units and account types, including create and update of segment derivation rules, deterministic FSM CSV preparation, governed Data Loader import, and persisted-state verification."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Customer Billing"
functional_area_code: "ORA_FIN_CUST_BILL"
task_code: "AR_MANAGE_AUTOACCOUNTING_RULES"
task_name: "Manage AutoAccounting Rules"
parent_skill_id: "erp.financials.customer-billing"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP financials pillar team"
version: "0.2.0"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-billing/manage-autoaccounting-rules/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-billing/manage-autoaccounting-rules/current/"
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
  - "After the active Run Book and Core Data Loader complete their required preview and approval gates, the authorized FSM adapter may create or update AutoAccounting setup in the approved Fusion environment."
required_privileges:
  - "AR_SET_UP_RECEIVABLES_DEFAULT_DISTRIBUTION_RULE_PRIV or an equivalent privilege inherited through ORA_AR_RECEIVABLES_ADMINISTRATION_DUTY."
  - "ORA_ASM_FUNCTIONAL_SETUPS_USER_ABSTRACT plus task-specific access for FSM CSV export and import."
---

<!-- fscr-supported-operations: create, update -->
<!-- fscr-create-fields: AR_AUTO_ACCOUNTING::Attribute1, AR_AUTO_ACCOUNTING::Attribute10, AR_AUTO_ACCOUNTING::Attribute11, AR_AUTO_ACCOUNTING::Attribute12, AR_AUTO_ACCOUNTING::Attribute13, AR_AUTO_ACCOUNTING::Attribute14, AR_AUTO_ACCOUNTING::Attribute15, AR_AUTO_ACCOUNTING::Attribute2, AR_AUTO_ACCOUNTING::Attribute3, AR_AUTO_ACCOUNTING::Attribute4, AR_AUTO_ACCOUNTING::Attribute5, AR_AUTO_ACCOUNTING::Attribute6, AR_AUTO_ACCOUNTING::Attribute7, AR_AUTO_ACCOUNTING::Attribute8, AR_AUTO_ACCOUNTING::Attribute9, AR_AUTO_ACCOUNTING::AttributeCategory, AR_AUTO_ACCOUNTING::BuName, AR_AUTO_ACCOUNTING::Type, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute1, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute10, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute11, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute12, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute13, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute14, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute15, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute2, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute3, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute4, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute5, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute6, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute7, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute8, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute9, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::AttributeCategory, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Constant, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Segment, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::SegmentNum, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::TableName -->
<!-- fscr-update-fields: AR_AUTO_ACCOUNTING::Attribute1, AR_AUTO_ACCOUNTING::Attribute10, AR_AUTO_ACCOUNTING::Attribute11, AR_AUTO_ACCOUNTING::Attribute12, AR_AUTO_ACCOUNTING::Attribute13, AR_AUTO_ACCOUNTING::Attribute14, AR_AUTO_ACCOUNTING::Attribute15, AR_AUTO_ACCOUNTING::Attribute2, AR_AUTO_ACCOUNTING::Attribute3, AR_AUTO_ACCOUNTING::Attribute4, AR_AUTO_ACCOUNTING::Attribute5, AR_AUTO_ACCOUNTING::Attribute6, AR_AUTO_ACCOUNTING::Attribute7, AR_AUTO_ACCOUNTING::Attribute8, AR_AUTO_ACCOUNTING::Attribute9, AR_AUTO_ACCOUNTING::AttributeCategory, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute1, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute10, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute11, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute12, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute13, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute14, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute15, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute2, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute3, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute4, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute5, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute6, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute7, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute8, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Attribute9, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::AttributeCategory, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::Constant, ORA_LE_AR_AUTO_ACCOUNTING_SEGMENT::TableName -->

# Manage AutoAccounting Rules Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage AutoAccounting Rules` under `Customer Billing`.

## Setup Task Skill Contract

- task_code: `AR_MANAGE_AUTOACCOUNTING_RULES`
- task_name: `Manage AutoAccounting Rules`
- parent_skill_id: `erp.financials.customer-billing`
- pillar: `ERP`
- offering: `Financials`
- functional_area: `Customer Billing`
- functional_area_code: `ORA_FIN_CUST_BILL`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage AutoAccounting Rules` under `Customer Billing`.

Business-language requests are sufficient. Do not ask customers to name the FSM task, CSV members, database tables, or loader APIs. Accept requests such as "For Vision Operations, derive Receivable from transaction type and use constant 000 for Department" or "Change the Revenue Product segment from a constant to Standard Lines and leave everything else unchanged."

## Customer Interaction and Lifecycle Contract

Resolve the exact business unit, account type, and every accounting segment from fresh task evidence. A create requires the complete segment design for one `BuName` plus `Type`. An update requires one exact existing parent and one or more exact child `Segment` values; preserve every unrequested field, segment, DFF value, and unrelated rule.

Ask one consolidated business question when a required value is missing or ambiguous. Never infer a business unit, account type, segment, source, constant value, chart of accounts, DFF context, or accounting value from conversation history or another environment. One unresolved operation blocks the entire mixed or bulk candidate.

Supported operations are create and update. Physical delete, identity rename, business-unit or account-type movement, and segment identity changes are unsupported. Suppress no-op updates.

`BuName`, `Type`, `Segment`, and `SegmentNum` are identity values. The five audit columns on each entity are Fusion-owned and must be blank in candidates. Each segment rule must contain exactly one derivation: a compatible `TableName`, or a value-set-valid `Constant`, never both and never neither.

## Account Types and Sources

Normalize only unambiguous account-type labels to the seeded codes evidenced for this task: `BR_FACTOR`, `BR_REC`, `BR_REMITTANCE`, `BR_UNPAID_REC`, `CHARGES`, `DEFERRED_TAX`, `FREIGHT`, `ORA_PREPAYMENT`, `REC`, `REV`, `SUSPENSE`, `TAX`, `UNBILL`, and `UNEARN`.

Normalize supported source labels to canonical package values only when compatible with the selected account type: Transaction Types to `RA_CUST_TRX_TYPES`, Salesperson to `RA_SALESREPS`, Bill-to Site to `RA_SITE_USES`, Standard Lines to `RA_STD_TRX_LINES`, and Tax to `RA_TAXES`. A constant derivation uses blank `TableName` and the confirmed value in `Constant`.

## Source-Backed Task Behavior

- Treat `BuName` plus `Type` as the parent rule identity and require fresh target-environment evidence for the business unit.
- Treat `Segment` and `SegmentNum` as child identity evidence beneath the exact parent; never infer a missing or ambiguous segment from another rule.
- Support create and update only; reject physical delete, identity rename, business-unit or account-type movement, and segment identity changes.
- Require exactly one derivation for each segment row: a compatible `TableName` or a validated `Constant`, never both and never neither.
- Normalize account types and table sources only from the closed, source-backed code sets stated above; ask a follow-up question for an unsupported or ambiguous business label.
- Leave Fusion-owned audit columns blank in candidates and retain their exported values only as read-only baseline evidence.
- Keep DFF columns blank on create and preserve them on update unless the exact deployed context, segment mapping, and value-set evidence are available.
- Preserve all unrequested fields and unrelated rows, suppress no-op updates, and fail closed when any mixed or bulk operation remains unresolved.
- Do not claim a requested target is live-ready unless its complete portable key resolves to exactly one row in the fresh exact-task export. Block a duplicated or conflicting requested target before package generation; preserve byte-identical duplicate rows outside the requested scope without treating them as target evidence.

## Preview, Handoff, and Verification

Show a complete normalized preview with action, business unit, account type, every segment name/number, source or constant, DFF changes, preserved values, applied normalization, warnings, and operation counts. Route design confirmation to the active Run Book. Route deterministic package creation, immutable candidate hashing, import approval, submission, monitoring, and result collection exclusively to `core.data-loader`.

After terminal import success, obtain a fresh exact-task export and reconcile every submitted identity and requested value. Fail verification when a requested row is absent, duplicated, or different, or when a confirmed baseline row changed unexpectedly. Allow unrelated rows created concurrently after the baseline unless they duplicate or alter a requested target.

Customer-configured business units, segment structures, constants, and DFF deployments require fresh target-environment evidence. Public documentation and CodeSearch establish behavior and seeded contracts, not customer-specific contents. DFF values require the exact deployed context, segment-to-`AttributeN` mapping, and value-set evidence; otherwise keep them blank on create and preserve them on update.

## Setup Task Metadata

- Task name: `Manage AutoAccounting Rules`
- Task code: `AR_MANAGE_AUTOACCOUNTING_RULES`
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

- Offering: `Financials`
- Functional area / Setup Object: `Customer Billing`
- Setup task name: `Manage AutoAccounting Rules`
- Setup task code: `AR_MANAGE_AUTOACCOUNTING_RULES`




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

Use the parent functional-area skill `erp.financials.customer-billing` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

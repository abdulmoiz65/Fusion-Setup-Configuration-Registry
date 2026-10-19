---
skill_id: "erp.financials.customer-billing.manage-transaction-types"
name: "Manage Transaction Types Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Transaction Types under the Customer Billing functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Customer Billing"
functional_area_code: "ORA_FIN_CUST_BILL"
task_code: "AR_MANAGE_TRANSACTION_TYPES"
task_name: "Manage Transaction Types"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-billing/manage-transaction-types/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-billing/manage-transaction-types/current/"
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

<!-- fscr-supported-operations: create, update -->
<!-- fscr-create-fields: AR_REF_ACCT_TRX_TYPE::AR_TRANSACTION_TYPE.Name, AR_REF_ACCT_TRX_TYPE::AR_TRANSACTION_TYPE.SetCode, AR_REF_ACCT_TRX_TYPE::BrFactorSegments, AR_REF_ACCT_TRX_TYPE::BrRemitSegments, AR_REF_ACCT_TRX_TYPE::BrUnpaidSegments, AR_REF_ACCT_TRX_TYPE::BuName, AR_REF_ACCT_TRX_TYPE::ClearingSegments, AR_REF_ACCT_TRX_TYPE::DepositOffsetSegments, AR_REF_ACCT_TRX_TYPE::DistSetSegments, AR_REF_ACCT_TRX_TYPE::DrcSegments, AR_REF_ACCT_TRX_TYPE::FreightSegments, AR_REF_ACCT_TRX_TYPE::LedgerName, AR_REF_ACCT_TRX_TYPE::Name, AR_REF_ACCT_TRX_TYPE::RecSegments, AR_REF_ACCT_TRX_TYPE::RevSegments, AR_REF_ACCT_TRX_TYPE::SourceRefTable, AR_REF_ACCT_TRX_TYPE::TaxSegments, AR_REF_ACCT_TRX_TYPE::UnbilledSegments, AR_REF_ACCT_TRX_TYPE::UnearnedSegments, AR_TRANSACTION_TYPE::AccountingAffectFlag, AR_TRANSACTION_TYPE::AdjPostToGlFlag, AR_TRANSACTION_TYPE::AllocateTaxFreight, AR_TRANSACTION_TYPE::AllowFreightFlag, AR_TRANSACTION_TYPE::AllowFutureAcctDateFlag, AR_TRANSACTION_TYPE::AllowOverapplicationFlag, AR_TRANSACTION_TYPE::Attribute1, AR_TRANSACTION_TYPE::Attribute10, AR_TRANSACTION_TYPE::Attribute11, AR_TRANSACTION_TYPE::Attribute12, AR_TRANSACTION_TYPE::Attribute13, AR_TRANSACTION_TYPE::Attribute14, AR_TRANSACTION_TYPE::Attribute15, AR_TRANSACTION_TYPE::Attribute2, AR_TRANSACTION_TYPE::Attribute3, AR_TRANSACTION_TYPE::Attribute4, AR_TRANSACTION_TYPE::Attribute5, AR_TRANSACTION_TYPE::Attribute6, AR_TRANSACTION_TYPE::Attribute7, AR_TRANSACTION_TYPE::Attribute8, AR_TRANSACTION_TYPE::Attribute9, AR_TRANSACTION_TYPE::AttributeCategory, AR_TRANSACTION_TYPE::ControlCompletion, AR_TRANSACTION_TYPE::CreationSign, AR_TRANSACTION_TYPE::CreditMemoTypeName, AR_TRANSACTION_TYPE::CreditMemoTypeSetCode, AR_TRANSACTION_TYPE::DefaultPrintingOption, AR_TRANSACTION_TYPE::DefaultStatus, AR_TRANSACTION_TYPE::DefaultTermName, AR_TRANSACTION_TYPE::DefaultTermSetCode, AR_TRANSACTION_TYPE::Description, AR_TRANSACTION_TYPE::DraweeIssuedFlag, AR_TRANSACTION_TYPE::EndDate, AR_TRANSACTION_TYPE::ExcludeFromLateCharges, AR_TRANSACTION_TYPE::GlobalAttribute1, AR_TRANSACTION_TYPE::GlobalAttribute10, AR_TRANSACTION_TYPE::GlobalAttribute11, AR_TRANSACTION_TYPE::GlobalAttribute12, AR_TRANSACTION_TYPE::GlobalAttribute13, AR_TRANSACTION_TYPE::GlobalAttribute14, AR_TRANSACTION_TYPE::GlobalAttribute15, AR_TRANSACTION_TYPE::GlobalAttribute16, AR_TRANSACTION_TYPE::GlobalAttribute17, AR_TRANSACTION_TYPE::GlobalAttribute18, AR_TRANSACTION_TYPE::GlobalAttribute19, AR_TRANSACTION_TYPE::GlobalAttribute2, AR_TRANSACTION_TYPE::GlobalAttribute20, AR_TRANSACTION_TYPE::GlobalAttribute3, AR_TRANSACTION_TYPE::GlobalAttribute4, AR_TRANSACTION_TYPE::GlobalAttribute5, AR_TRANSACTION_TYPE::GlobalAttribute6, AR_TRANSACTION_TYPE::GlobalAttribute7, AR_TRANSACTION_TYPE::GlobalAttribute8, AR_TRANSACTION_TYPE::GlobalAttribute9, AR_TRANSACTION_TYPE::GlobalAttributeCategory, AR_TRANSACTION_TYPE::GlobalAttributeDate1, AR_TRANSACTION_TYPE::GlobalAttributeDate2, AR_TRANSACTION_TYPE::GlobalAttributeDate3, AR_TRANSACTION_TYPE::GlobalAttributeDate4, AR_TRANSACTION_TYPE::GlobalAttributeDate5, AR_TRANSACTION_TYPE::GlobalAttributeNumber1, AR_TRANSACTION_TYPE::GlobalAttributeNumber2, AR_TRANSACTION_TYPE::GlobalAttributeNumber3, AR_TRANSACTION_TYPE::GlobalAttributeNumber4, AR_TRANSACTION_TYPE::GlobalAttributeNumber5, AR_TRANSACTION_TYPE::LegalEntityIdentifier, AR_TRANSACTION_TYPE::Name, AR_TRANSACTION_TYPE::NaturalApplicationOnlyFlag, AR_TRANSACTION_TYPE::PostToGl, AR_TRANSACTION_TYPE::RuleSetName, AR_TRANSACTION_TYPE::SetCode, AR_TRANSACTION_TYPE::SignedFlag, AR_TRANSACTION_TYPE::StartDate, AR_TRANSACTION_TYPE::Status, AR_TRANSACTION_TYPE::SubsequentTrxTypeName, AR_TRANSACTION_TYPE::SubsequentTrxTypeSetCode, AR_TRANSACTION_TYPE::TaxCalculationFlag, AR_TRANSACTION_TYPE::TrxSubclassCode, AR_TRANSACTION_TYPE::Type, AR_TRANSACTION_TYPE::UsageCategoryCode -->
<!-- fscr-update-fields: AR_TRANSACTION_TYPE::Description, AR_TRANSACTION_TYPE::EndDate, AR_TRANSACTION_TYPE::Status -->

# Manage Transaction Types Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Transaction Types` under `Customer Billing`.

## Setup Task Skill Contract

- task_code: `AR_MANAGE_TRANSACTION_TYPES`
- task_name: `Manage Transaction Types`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Transaction Types` under `Customer Billing`.

## Setup Task Metadata

- Task name: `Manage Transaction Types`
- Task code: `AR_MANAGE_TRANSACTION_TYPES`
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
- Setup task name: `Manage Transaction Types`
- Setup task code: `AR_MANAGE_TRANSACTION_TYPES`

## Source-Backed Task Behavior

- Treat `AR_TRANSACTION_TYPE` as the parent entity and `AR_REF_ACCT_TRX_TYPE` as its reference-account child; preserve the exact parent `SetCode` and `Name` in every emitted child row. Evidence: `SRC-FSM-PACKAGE`, `SRC-CODE-AM-DEF`, `SRC-CODE-REF-VO`.
- Use `SetCode` plus `Name` as the parent transaction-type business identity; never identify a transaction type by `Name` alone. Evidence: `SRC-CODE-BO-META`, `SRC-CODE-PRIMARY-VO`, `SRC-EDM-RA-CUST-26B`.
- Support source-backed create and existing-row update preparation. Match updates only by `SetCode` plus `Name`. The exact supported update fields are `Description`, `Status`, and `EndDate`; every other field remains blocked unless later operation-specific evidence promotes it. Physical delete remains unsupported, and `Status` or `EndDate` changes are retirement updates rather than delete. Evidence: `SRC-HELP-TRXTYPE-26C`, `SRC-CODE-CREATE-VO`, `SRC-CODE-AM-IMPL`, `SRC-CODE-PRIMARY-VO`, `SRC-CODE-PRIMARY-EO`, `SRC-E2E-MTT-DESCRIPTION-UPDATE-20260905`, `SRC-E2E-MTT-DESCRIPTION-ROLLBACK-20260905`.
- Treat developer-test fixtures, campaign policies, and test approvals as test-only controls. They never limit ordinary implementor create or update row counts and never override the source-backed task behavior in this skill and its active `ora-resource/` files.
- Require explicit create values for `SetCode`, `Name`, `PostToGl`, `AccountingAffectFlag`, `Status`, `Type`, `DefaultPrintingOption`, `DefaultStatus`, `AllowFreightFlag`, `AllowOverapplicationFlag`, `CreationSign`, `StartDate`, `TaxCalculationFlag`, and `NaturalApplicationOnlyFlag`; do not invent defaults for these fields. Evidence: `SRC-FSM-PACKAGE`, `SRC-CODE-CREATE-VO`, `SRC-CODE-PRIMARY-EO`, `SRC-BO-TRXTYPE-26C`.
- Require `AR_TRANSACTION_TYPE.Name` to be no more than 20 characters and an explicitly supplied `AR_TRANSACTION_TYPE.Description` to be no more than 80 characters. Enforce these source-backed limits before immutable preview or candidate generation for every requested row, report the actual and maximum character counts, and never silently truncate, abbreviate, or rewrite business text. Evidence: `SRC-EDM-RA-CUST-26B`, `SRC-E2E-MTT-FIELD-LENGTH-20260909`.
- Accept only `Y` or `N` for source-backed Boolean option fields, and reject a row when `NaturalApplicationOnlyFlag` and `AllowOverapplicationFlag` are both `Y`. Evidence: `SRC-BO-TRXTYPE-26C`, `SRC-CODE-PRIMARY-EO`, `SRC-CODE-PRIMARY-VO`.
- Validate fixed domains before package generation: transaction class `ADJ`, `BR`, `CB`, `CM`, `DEP`, `DM`, `GUAR`, or `INV`; record status `A`, `D`, or `I`; printing option `N`, `NOT`, or `PRI`; completion control `ALL`, `NEGATIVE_LINE_AMT`, or `NONE`. Evidence: `SRC-BO-TRXTYPE-26C`, `SRC-CODE-CREATE-VO`, `SRC-EDM-RA-CUST-26B`.
- Omit the five Fusion who/audit fields from generated parent and child rows and preserve them only as baseline comparison evidence. Evidence: `SRC-CODE-AM-IMPL`, `SRC-CODE-PRIMARY-EO`, `SRC-CODE-PRIMARY-VO`, `SRC-CODE-REF-VO`.
- Require ISO date values and reject `EndDate` earlier than `StartDate`; malformed date and date-time values must not be stringified into a package. Evidence: `SRC-BO-TRXTYPE-26C`, `SRC-CODE-PRIMARY-EO`, `SRC-EDM-RA-CUST-26B`.
- During reconciliation, apply strict separator canonicalization to every package field whose exact `ASM_SETUP_CSV_METADATA.xml` type is `date`: requested and candidate values must be identical strict `YYYY-MM-DD`, and a persisted strict `YYYY/MM/DD` value is equivalent only when all values parse to the same valid Gregorian calendar date. Retain all raw values, the canonical ISO date, declared type, generic rule ID, and metadata-contract evidence. Do not extend this rule to date-time/timestamp fields, strings whose names merely contain `Date`, blanks, malformed or locale-ambiguous values, unequal dates, or candidate drift. Evidence: `SRC-E2E-MTT-STARTDATE-CANON-20260905`, `SRC-E2E-MTT-ENDDATE-CANON-20260909`, `SRC-FSM-PACKAGE`.
- For a reference-account child row, require exact `BuName` and `LedgerName`, set `SourceRefTable` to `RA_CUST_TRX_TYPES_ALL`, and never accept a caller override for that constant. Evidence: `SRC-CODE-REF-VO`, `SRC-CODE-AM-IMPL`, `SRC-EDM-AR-REF-26A`.
- Treat every account-segment field as an ordered, ledger-specific programmatic reference. Never invent, pad, reorder, truncate, or reuse combinations across ledgers; live use remains blocked until explicit nonproduction validation. Evidence: `SRC-CODE-AM-IMPL`, `SRC-CODE-GL-BULK`, `SRC-CODE-ARPT-VALIDATE`, `SRC-CODE-REF-VO`.
- For `CreationSign`, accept only verified code `P` or the case-insensitive business label `Positive Sign` and normalize it to `P`. For `DefaultStatus`, accept only verified code `OP` or the case-insensitive business label `Open` and normalize it to `OP`. Their general resolvers remain Partial, so block or clarify every other value. Keep `UsageCategoryCode` and `TrxSubclassCode` blocked unless their exact environment-supported codes are verified; omit an optional unresolved field instead of inferring a code from a label. Evidence: `SRC-CODE-CREATE-VO`, `SRC-BO-TRXTYPE-26C`, `SRC-E2E-MTT-CREATE-IMPORT-VALUES-20260905`, `SRC-E2E-MTT-CREATE-RECONCILIATION-20260905`.
- Serialize descriptive-flexfield values only with their matching context code and source-backed datatype; never fabricate contexts or coerce values across contexts. Evidence: `SRC-CODE-PRIMARY-EO`, `SRC-CODE-PRIMARY-VO`, `SRC-EDM-RA-CUST-26B`.
- Build from a fresh same-task template/current export pair, preserve `ASM_SETUP_CSV_METADATA.xml` unchanged from the current-data baseline, preserve ordered headers and explicit trailing blanks, and reject every short or long CSV row. Evidence: `SRC-FSM-PACKAGE`.
- If every requested update already matches the fresh current-data baseline exactly, complete source, field, ownership, and requirement validation and return `NO_OP` without creating an import ZIP. The result retains input/design hashes and the business summary; `candidateSha256` is null, the member inventory is empty, and no candidate may be submitted to Data Loader. Record the no-change outcome. The same rule applies to an already-restored update rollback. Do not treat approximate text or date formatting differences as exact equality; ordinary typed-date reconciliation remains unchanged. A batch containing any real change follows the normal package, validation, preview, and approval workflow.
- Route every import through `core.data-loader` in `FSM` mode with an empty `businessObject`; use metadata `ObjectShortName` `AR_MANAGE_TRANSACTION_TYPES` as task identity, require the validation, immutable preview, and approval prescribed by core.data-loader and Task Hook, and never retry a failed or uncertain submission automatically. Evidence: current repository contracts and `SRC-FSM-PACKAGE`.




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

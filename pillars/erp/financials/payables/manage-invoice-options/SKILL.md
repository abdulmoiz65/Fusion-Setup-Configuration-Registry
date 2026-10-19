---
skill_id: "erp.financials.payables.manage-invoice-options"
name: "Manage Invoice Options Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Invoice Options under the Payables functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Payables"
functional_area_code: "FIN_PAYABLES_DEPLOYED"
task_code: "AP_MANAGE_INVOICE_OPTIONS"
task_name: "Manage Invoice Options"
parent_skill_id: "erp.financials.payables"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/payables/manage-invoice-options/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/payables/manage-invoice-options/current/"
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

# Manage Invoice Options Setup Task Guidance

<!-- fscr-supported-operations: create, update -->
<!-- fscr-create-fields: AP_SYSTEM_PARAMETER::BuName, AP_SYSTEM_PARAMETER::InterestSegments, AP_SYSTEM_PARAMETER::BaseCurrencyCode, AP_SYSTEM_PARAMETER::InvoiceCurrencyCode, AP_SYSTEM_PARAMETER::PaymentCurrencyCode, AP_SYSTEM_PARAMETER::AlwaysTakeDiscFlag, AP_SYSTEM_PARAMETER::PayDateBasisLookupCode, AP_SYSTEM_PARAMETER::AddDaysSettlementDate, AP_SYSTEM_PARAMETER::DaysBetweenCheckCycles, AP_SYSTEM_PARAMETER::FederalIdentificationNum, AP_SYSTEM_PARAMETER::UpdatePaySiteFlag, AP_SYSTEM_PARAMETER::GlDateFromReceiptFlag, AP_SYSTEM_PARAMETER::DiscIsInvLessTaxFlag, AP_SYSTEM_PARAMETER::AccountingMethodOption, AP_SYSTEM_PARAMETER::OnlinePrintFlag, AP_SYSTEM_PARAMETER::EftUserNumber, AP_SYSTEM_PARAMETER::MaxOutlay, AP_SYSTEM_PARAMETER::VendorPayGroupLookupCode, AP_SYSTEM_PARAMETER::RequireTaxEntryFlag, AP_SYSTEM_PARAMETER::PostDatedPaymentsFlag, AP_SYSTEM_PARAMETER::SecondaryAccountingMethod, AP_SYSTEM_PARAMETER::InterestToleranceAmount, AP_SYSTEM_PARAMETER::TermsDateBasis, AP_SYSTEM_PARAMETER::LiabilityPostLookupCode, AP_SYSTEM_PARAMETER::DiscountDistributionMethod, AP_SYSTEM_PARAMETER::CombinedFilingFlag, AP_SYSTEM_PARAMETER::IncomeTaxRegion, AP_SYSTEM_PARAMETER::IncomeTaxRegionFlag, AP_SYSTEM_PARAMETER::AllowFinalMatchFlag, AP_SYSTEM_PARAMETER::AllowFlexOverrideFlag, AP_SYSTEM_PARAMETER::AllowPaidInvoiceAdjust, AP_SYSTEM_PARAMETER::UssglTransactionCode, AP_SYSTEM_PARAMETER::UssglTrxCodeContext, AP_SYSTEM_PARAMETER::InvDocCategoryOverride, AP_SYSTEM_PARAMETER::PayDocCategoryOverride, AP_SYSTEM_PARAMETER::VendorAutoIntDefault, AP_SYSTEM_PARAMETER::TransferDescFlexFlag, AP_SYSTEM_PARAMETER::AllowAwtFlag, AP_SYSTEM_PARAMETER::AllowAwtOverride, AP_SYSTEM_PARAMETER::CreateAwtDistsType, AP_SYSTEM_PARAMETER::CreateAwtInvoicesType, AP_SYSTEM_PARAMETER::AwtIncludeDiscountAmt, AP_SYSTEM_PARAMETER::AwtIncludeTaxAmt, AP_SYSTEM_PARAMETER::AutoCreateFreightFlag, AP_SYSTEM_PARAMETER::GlobalAttributeCategory, AP_SYSTEM_PARAMETER::GlobalAttribute1, AP_SYSTEM_PARAMETER::GlobalAttribute2, AP_SYSTEM_PARAMETER::GlobalAttribute3, AP_SYSTEM_PARAMETER::GlobalAttribute4, AP_SYSTEM_PARAMETER::GlobalAttribute5, AP_SYSTEM_PARAMETER::GlobalAttribute6, AP_SYSTEM_PARAMETER::GlobalAttribute7, AP_SYSTEM_PARAMETER::GlobalAttribute8, AP_SYSTEM_PARAMETER::GlobalAttribute9, AP_SYSTEM_PARAMETER::GlobalAttribute10, AP_SYSTEM_PARAMETER::GlobalAttribute11, AP_SYSTEM_PARAMETER::GlobalAttribute12, AP_SYSTEM_PARAMETER::GlobalAttribute13, AP_SYSTEM_PARAMETER::GlobalAttribute14, AP_SYSTEM_PARAMETER::GlobalAttribute15, AP_SYSTEM_PARAMETER::GlobalAttribute16, AP_SYSTEM_PARAMETER::GlobalAttribute17, AP_SYSTEM_PARAMETER::GlobalAttribute18, AP_SYSTEM_PARAMETER::GlobalAttribute19, AP_SYSTEM_PARAMETER::GlobalAttribute20, AP_SYSTEM_PARAMETER::AllowSupplierBankOverride, AP_SYSTEM_PARAMETER::UseBankChargeFlag, AP_SYSTEM_PARAMETER::BankChargeBearer, AP_SYSTEM_PARAMETER::MrcBaseCurrencyCode, AP_SYSTEM_PARAMETER::GainLossCalcLevel, AP_SYSTEM_PARAMETER::WhenToAccountPmt, AP_SYSTEM_PARAMETER::FutureDatedPmtLiabRelief, AP_SYSTEM_PARAMETER::GlTransferAllowOverride, AP_SYSTEM_PARAMETER::GlTransferMode, AP_SYSTEM_PARAMETER::GlTransferSubmitJournalImp, AP_SYSTEM_PARAMETER::IncludeReportingSob, AP_SYSTEM_PARAMETER::ApprovalWorkflowFlag, AP_SYSTEM_PARAMETER::AllowForceApprovalFlag, AP_SYSTEM_PARAMETER::ValidateBeforeApprovalFlag, AP_SYSTEM_PARAMETER::XmlPaymentsAutoConfirmFlag, AP_SYSTEM_PARAMETER::BuildPrepaymentAccountsFlag, AP_SYSTEM_PARAMETER::Enable1099OnAwtFlag, AP_SYSTEM_PARAMETER::ApprovalTiming, AP_SYSTEM_PARAMETER::ReceiptAcceptanceDays, AP_SYSTEM_PARAMETER::PaymentPriority, AP_SYSTEM_PARAMETER::ExcludeFreightFromDiscount, AP_SYSTEM_PARAMETER::AutoCalculateInterestFlag, AP_SYSTEM_PARAMETER::ProrateIntInvAcrossDists, AP_SYSTEM_PARAMETER::RequireInvoiceGroupFlag, AP_SYSTEM_PARAMETER::EmployeePaymentPriority, AP_SYSTEM_PARAMETER::EmployeePayGroupLookupCode, AP_SYSTEM_PARAMETER::SsInvoiceBackdatingFlag, AP_SYSTEM_PARAMETER::SsLimitToSinglePoFlag, AP_SYSTEM_PARAMETER::SsUpriceChangeForQtymatch, AP_SYSTEM_PARAMETER::SOBName, AP_SYSTEM_PARAMETER::TermName, AP_SYSTEM_PARAMETER::EmployeeTermName, AP_SYSTEM_PARAMETER::PrepaymentTermName, AP_SYSTEM_PARAMETER::ToleranceName, AP_SYSTEM_PARAMETER::ServicesToleranceName, AP_SYSTEM_PARAMETER::AwtName, AP_SYSTEM_PARAMETER::EnterpriseId, AP_SYSTEM_PARAMETER::PrepaymentAvailableMesgFlag, AP_SYSTEM_PARAMETER::RecalcPayScheduleFlag, AP_SYSTEM_PARAMETER::BudgetDateBasis, AP_SYSTEM_PARAMETER::OverrideMatchRejectionFlag, AP_SYSTEM_PARAMETER::RouteInterfaceRejectionFlag, AP_SYSTEM_PARAMETER::AllowInvThirdPartyOvrd, AP_SYSTEM_PARAMETER::AllowPymtThirdPartyOvrd, AP_SYSTEM_PARAMETER::RoutingFlag, AP_SYSTEM_PARAMETER::AttachmentMandatorySsFlag, AP_SYSTEM_PARAMETER::DisallowAttachmentDelFlag, AP_SYSTEM_PARAMETER::BankChargeDeductionTypeDes, AP_SYSTEM_PARAMETER::ReleaseDupInvoiceHoldFlag, AP_SYSTEM_PARAMETER::SsQtyMatchOverbillFlag, AP_SYSTEM_PARAMETER::SsAmtMatchOverbillFlag, AP_SYSTEM_PARAMETER::EscheatmentEligibilityPeriod, AP_SYSTEM_PARAMETER::AccountDefaultBasisCodeDes -->
<!-- fscr-update-fields: AP_SYSTEM_PARAMETER::InterestSegments, AP_SYSTEM_PARAMETER::BaseCurrencyCode, AP_SYSTEM_PARAMETER::InvoiceCurrencyCode, AP_SYSTEM_PARAMETER::PaymentCurrencyCode, AP_SYSTEM_PARAMETER::AlwaysTakeDiscFlag, AP_SYSTEM_PARAMETER::PayDateBasisLookupCode, AP_SYSTEM_PARAMETER::AddDaysSettlementDate, AP_SYSTEM_PARAMETER::DaysBetweenCheckCycles, AP_SYSTEM_PARAMETER::FederalIdentificationNum, AP_SYSTEM_PARAMETER::UpdatePaySiteFlag, AP_SYSTEM_PARAMETER::GlDateFromReceiptFlag, AP_SYSTEM_PARAMETER::DiscIsInvLessTaxFlag, AP_SYSTEM_PARAMETER::AccountingMethodOption, AP_SYSTEM_PARAMETER::OnlinePrintFlag, AP_SYSTEM_PARAMETER::EftUserNumber, AP_SYSTEM_PARAMETER::MaxOutlay, AP_SYSTEM_PARAMETER::VendorPayGroupLookupCode, AP_SYSTEM_PARAMETER::RequireTaxEntryFlag, AP_SYSTEM_PARAMETER::PostDatedPaymentsFlag, AP_SYSTEM_PARAMETER::SecondaryAccountingMethod, AP_SYSTEM_PARAMETER::InterestToleranceAmount, AP_SYSTEM_PARAMETER::TermsDateBasis, AP_SYSTEM_PARAMETER::LiabilityPostLookupCode, AP_SYSTEM_PARAMETER::DiscountDistributionMethod, AP_SYSTEM_PARAMETER::CombinedFilingFlag, AP_SYSTEM_PARAMETER::IncomeTaxRegion, AP_SYSTEM_PARAMETER::IncomeTaxRegionFlag, AP_SYSTEM_PARAMETER::AllowFinalMatchFlag, AP_SYSTEM_PARAMETER::AllowFlexOverrideFlag, AP_SYSTEM_PARAMETER::AllowPaidInvoiceAdjust, AP_SYSTEM_PARAMETER::UssglTransactionCode, AP_SYSTEM_PARAMETER::UssglTrxCodeContext, AP_SYSTEM_PARAMETER::InvDocCategoryOverride, AP_SYSTEM_PARAMETER::PayDocCategoryOverride, AP_SYSTEM_PARAMETER::VendorAutoIntDefault, AP_SYSTEM_PARAMETER::TransferDescFlexFlag, AP_SYSTEM_PARAMETER::AllowAwtFlag, AP_SYSTEM_PARAMETER::AllowAwtOverride, AP_SYSTEM_PARAMETER::CreateAwtDistsType, AP_SYSTEM_PARAMETER::CreateAwtInvoicesType, AP_SYSTEM_PARAMETER::AwtIncludeDiscountAmt, AP_SYSTEM_PARAMETER::AwtIncludeTaxAmt, AP_SYSTEM_PARAMETER::AutoCreateFreightFlag, AP_SYSTEM_PARAMETER::GlobalAttributeCategory, AP_SYSTEM_PARAMETER::GlobalAttribute1, AP_SYSTEM_PARAMETER::GlobalAttribute2, AP_SYSTEM_PARAMETER::GlobalAttribute3, AP_SYSTEM_PARAMETER::GlobalAttribute4, AP_SYSTEM_PARAMETER::GlobalAttribute5, AP_SYSTEM_PARAMETER::GlobalAttribute6, AP_SYSTEM_PARAMETER::GlobalAttribute7, AP_SYSTEM_PARAMETER::GlobalAttribute8, AP_SYSTEM_PARAMETER::GlobalAttribute9, AP_SYSTEM_PARAMETER::GlobalAttribute10, AP_SYSTEM_PARAMETER::GlobalAttribute11, AP_SYSTEM_PARAMETER::GlobalAttribute12, AP_SYSTEM_PARAMETER::GlobalAttribute13, AP_SYSTEM_PARAMETER::GlobalAttribute14, AP_SYSTEM_PARAMETER::GlobalAttribute15, AP_SYSTEM_PARAMETER::GlobalAttribute16, AP_SYSTEM_PARAMETER::GlobalAttribute17, AP_SYSTEM_PARAMETER::GlobalAttribute18, AP_SYSTEM_PARAMETER::GlobalAttribute19, AP_SYSTEM_PARAMETER::GlobalAttribute20, AP_SYSTEM_PARAMETER::AllowSupplierBankOverride, AP_SYSTEM_PARAMETER::UseBankChargeFlag, AP_SYSTEM_PARAMETER::BankChargeBearer, AP_SYSTEM_PARAMETER::MrcBaseCurrencyCode, AP_SYSTEM_PARAMETER::GainLossCalcLevel, AP_SYSTEM_PARAMETER::WhenToAccountPmt, AP_SYSTEM_PARAMETER::FutureDatedPmtLiabRelief, AP_SYSTEM_PARAMETER::GlTransferAllowOverride, AP_SYSTEM_PARAMETER::GlTransferMode, AP_SYSTEM_PARAMETER::GlTransferSubmitJournalImp, AP_SYSTEM_PARAMETER::IncludeReportingSob, AP_SYSTEM_PARAMETER::ApprovalWorkflowFlag, AP_SYSTEM_PARAMETER::AllowForceApprovalFlag, AP_SYSTEM_PARAMETER::ValidateBeforeApprovalFlag, AP_SYSTEM_PARAMETER::XmlPaymentsAutoConfirmFlag, AP_SYSTEM_PARAMETER::BuildPrepaymentAccountsFlag, AP_SYSTEM_PARAMETER::Enable1099OnAwtFlag, AP_SYSTEM_PARAMETER::ApprovalTiming, AP_SYSTEM_PARAMETER::ReceiptAcceptanceDays, AP_SYSTEM_PARAMETER::PaymentPriority, AP_SYSTEM_PARAMETER::ExcludeFreightFromDiscount, AP_SYSTEM_PARAMETER::AutoCalculateInterestFlag, AP_SYSTEM_PARAMETER::ProrateIntInvAcrossDists, AP_SYSTEM_PARAMETER::RequireInvoiceGroupFlag, AP_SYSTEM_PARAMETER::EmployeePaymentPriority, AP_SYSTEM_PARAMETER::EmployeePayGroupLookupCode, AP_SYSTEM_PARAMETER::SsInvoiceBackdatingFlag, AP_SYSTEM_PARAMETER::SsLimitToSinglePoFlag, AP_SYSTEM_PARAMETER::SsUpriceChangeForQtymatch, AP_SYSTEM_PARAMETER::SOBName, AP_SYSTEM_PARAMETER::TermName, AP_SYSTEM_PARAMETER::EmployeeTermName, AP_SYSTEM_PARAMETER::PrepaymentTermName, AP_SYSTEM_PARAMETER::ToleranceName, AP_SYSTEM_PARAMETER::ServicesToleranceName, AP_SYSTEM_PARAMETER::AwtName, AP_SYSTEM_PARAMETER::EnterpriseId, AP_SYSTEM_PARAMETER::PrepaymentAvailableMesgFlag, AP_SYSTEM_PARAMETER::RecalcPayScheduleFlag, AP_SYSTEM_PARAMETER::BudgetDateBasis, AP_SYSTEM_PARAMETER::OverrideMatchRejectionFlag, AP_SYSTEM_PARAMETER::RouteInterfaceRejectionFlag, AP_SYSTEM_PARAMETER::AllowInvThirdPartyOvrd, AP_SYSTEM_PARAMETER::AllowPymtThirdPartyOvrd, AP_SYSTEM_PARAMETER::RoutingFlag, AP_SYSTEM_PARAMETER::AttachmentMandatorySsFlag, AP_SYSTEM_PARAMETER::DisallowAttachmentDelFlag, AP_SYSTEM_PARAMETER::BankChargeDeductionTypeDes, AP_SYSTEM_PARAMETER::ReleaseDupInvoiceHoldFlag, AP_SYSTEM_PARAMETER::SsQtyMatchOverbillFlag, AP_SYSTEM_PARAMETER::SsAmtMatchOverbillFlag, AP_SYSTEM_PARAMETER::EscheatmentEligibilityPeriod, AP_SYSTEM_PARAMETER::AccountDefaultBasisCodeDes -->

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Invoice Options` under `Payables`.

## Supported Operations

This task supports creating a new Invoice Options setup row and updating an exact existing setup row. It does not support delete or end-date operations. Only the operation-specific fields documented in [Input Validation](ora-resource/ora_input_validation.md) and [Design Enforcement](ora-resource/ora_design_enforcement.md) are permitted; all other fields remain blocked.

## Task Behavior

- Use the exact `AP_SYSTEM_PARAMETER` package and CSV header contract. The
  supported create and update fields are defined by the local resources and
  adapter.

- Keep the exact `AP_SYSTEM_PARAMETER` package root
  (`/SystemOptionVO/SystemOptionVORow`) and the current template's header order
  and field count. Do not create a replacement schema. For a create, find the
  business unit in `finBusinessUnitsLOV`, use its `PrimaryLedgerId` to find the
  ledger in `ledgersLOV`, and write that ledger name to `SOBName`.
  For `EnterpriseId`, use (in order): the value explicitly requested for that
  row, the current-run default, or the fresh FSM export when it has exactly one
  nonblank value. Record this choice as `enterpriseIdResolution`. An update
  keeps the value from its uniquely matched export row. Fusion then resolves
  `BuName` and `EnterpriseId` to `OrgId`.
- The three payment-term fields are separate defaults. In the CSV, the Payment
  Request Payment Terms control is `EmployeeTermName`. Check each supplied name
  with the read-only `payablesPaymentTerms` service and keep the result as
  evidence only; do not choose an ID from multiple results. On import, Fusion
  resolves `TermName`, `PrepaymentTermName`, and `EmployeeTermName` to their
  corresponding IDs. A missing value is reported as an import dependency.
- Before normalization, run `scripts/resolve_lookup_prerequisites.py` for any
  populated page lookup fields. The adapter checks fixed system values locally.
  It preserves customer-controlled values and lets Fusion validate them during
  the separately approved import.
- Route every import through `core.data-loader` in FSM mode. A static artifact
  never authorizes an import: Data Loader still requires an immutable preview
  and approval for that candidate.

## Setup Task Skill Contract

- task_code: `AP_MANAGE_INVOICE_OPTIONS`
- task_name: `Manage Invoice Options`
- parent_skill_id: `erp.financials.payables`
- pillar: `ERP`
- offering: `Financials`
- functional_area: `Payables`
- functional_area_code: `FIN_PAYABLES_DEPLOYED`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Invoice Options` under `Payables`.

## Setup Task Metadata

- Task name: `Manage Invoice Options`
- Task code: `AP_MANAGE_INVOICE_OPTIONS`
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
- Functional area / Setup Object: `Payables`
- Setup task name: `Manage Invoice Options`
- Setup task code: `AP_MANAGE_INVOICE_OPTIONS`

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

`AP_SYSTEM_PARAMETER` is a shared row with separate Invoice and Payment
ownership rules. For an Invoice Options setup update, merge the requested change
with the baseline, then validate all resulting Payment-owned values with the
Manage Payment Options field contract. For a new Invoice Options setup row,
validate only supplied Payment-owned values and never invent optional ones.
Invoke only the sibling validator, not the full Payment Options skill, to avoid
a recursive workflow.

For one business unit, a single NLP request that includes both Invoice Options
and Payment Options changes is one shared-row transaction. Merge all requested
fields into one canonical `AP_SYSTEM_PARAMETER` row before candidate generation,
validate both field contracts against that row, and submit only this Invoice
Options package when any Invoice Options field is present. Do not create or
submit a second full-row package with a different baseline or values. A
Payment-only request remains a Manage Payment Options package.

Use the parent functional-area skill `erp.financials.payables` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

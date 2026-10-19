# Manage Common Options for Payables and Procurement Input Validation

## Validation Policy

The adapter blocks malformed transport data, violations of proven import-hook/entity/GL rules, and violations of explicitly user-approved preparation guardrails. If neither source nor an approved local rule establishes a field-specific check, the adapter accepts a structurally valid value and records it as transport-sanity-only. It does not infer business meaning from a column name, a UI label, another product object's lookup, or an observed export row.

## Required Candidate Context

| Input | Validation | Applies When |
|---|---|---|
| Exact package shape | Same-task header order, 81 fields per row, and `/FinancialsOptionVO/FinancialsOptionVORow` | Every package. |
| `BuName`, optional `EnterpriseId` | Select EnterpriseId by ora_defaulting_rules.md precedence; retain long-integer sanity. Exact ERP Financials BU/primary-ledger and ledger responses derive SOBName, not EnterpriseId. | Every row; ask for EnterpriseId only when no explicit or unambiguous export-derived value is available. |
| `SOBName`, `AcctsPaySegments`, `PrepaySegments`, `DiscTakenSegments`, `RateVarGainSegments`, `RateVarLossSegments`, `GainSegments`, `LossSegments` | Nonblank for a new row; each supplied account segment has its own current no-create account-combination receipt | Create only. |
| Target identity | Fresh export proves absent target for create or one existing target for update | Before build/reconciliation. |

## Product-Backed and User-Approved Field Validation

| Field or group | Check | Applies When |
|---|---|---|
| `SetCode` | Require a source-backed reference-set resolution. | Supplied. |
| Bill-to Location name; or `InternalLocationCode` after an HCM access or endpoint error | Resolve a supplied name through HCM, then verify the same record is active, bill-to enabled, and effective. Only after an HCM error, ask for the exact internal code and use FSCM to verify one eligible code, set, and effective-date composite. | Name supplied; or code explicitly supplied after HCM error. |
| `UserConversionRateType`, `UserDefaultPmtExchangeRateType` | Require at least one exact current conversion-rate-type result; response cardinality is not a gate. | Supplied. |
| ExpenseAccrualCode | Apply validate_approved_option_choices using the fixed choices in ora_reference_lookups.md; normalize a listed label or exact code. No live LOV/REST receipt. Reject blank or unlisted values. | Supplied. |
| LiabilityPostLookupCode | Apply validate_approved_option_choices using the fixed choices in ora_reference_lookups.md. No live LOV/REST receipt. Reject blank or unlisted values; do not supply entity-derived automatic-offset flags. | Supplied. |
| `VatCountryCode` | Require an exact enabled, non-obsolete territory result; response cardinality is not a gate. | Supplied. |
| `GaplessInvNumFlag`, `MakeRateMandatoryFlag` | Normalize exact labels/codes to, and allow only, `Y` or `N`. | Supplied. |
| BuyingCompanyIdentifier | Maximum 10 characters; apply the confirmed-Yes dependency in ora_design_enforcement.md via validate_gapless_identifier_dependency. | Supplied or gapless changes. |
| All sixteen `…Segments` fields | One-through-30 segment values and a field/value/ledger-bound `DynamicInsertion=No` `Valid` SOAP receipt. | Supplied. |

The location name is an intake selector, not a CSV column. Only the verified
`InternalLocationCode` from the selected record enters the candidate row.

## Transport-Sanity-Only Fields

| Fields | Check | Local outcome |
|---|---|---|
| `PaymentMethodLookupCode`, `UserDefinedVendorNumCode`, `PayDateBasisLookupCode`, `ManualVendorNumType`, `TermsDateBasis`, `MatchOption` | String, maximum 25 characters | Accept when in range; no lookup or code normalization. |
| `InvoiceCurrencyCode`, `PaymentCurrencyCode` | String, maximum 15 characters | Accept when in range; no current-currency receipt. |
| `AlwaysTakeDiscFlag`, `ReqEncumbranceFlag`, `PurchEncumbranceFlag`, `HoldUnmatchedInvoicesFlag`, `ExclusivePaymentFlag`, `BankChargeBearer`, `MakeRateMandatoryPmtFlag` | String, maximum 1 character | Accept when in range; no assumed Boolean/lookup encoding. |
| `VendorNumStartNum` | Integer lexical form | Accept valid integer syntax. |
| `FuturePeriodLimit` | Integer lexical form, at most 3 digits | Accept when precision passes. |
| `ReceiptAcceptanceDays` | Long-integer lexical form, at most 18 digits | Accept when precision passes. |
| `VatRegistrationNum` | String, maximum 20 characters | Accept when in range. |
| `NrTaxRounding` | String, maximum 30 characters | Accept when in range. |
| `TransEffectiveStartDate`, `TransEffectiveEndDate` | ISO date syntax | Accept syntactically valid dates. |
| `GlobalAttributeCategory`, `GlobalAttribute1`–`GlobalAttribute20` | String, maximum 150 characters | Accept when in range; disclose that DFF semantics are not locally validated. |


## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| APCO.VALIDATE_INPUT | step | 10 | validate_input | valid->APCO.RESOLVE_REFERENCES;blocked->APCO.HANDLE_ERROR | none | stop | Before any lookup, default, preview, or submission |

## Adapter lifecycle and input-field contract

<!-- fscr-supported-operations: create, update -->
<!-- fscr-create-fields: AP_FINANCIAL_SYS_PARAM::BuName, AP_FINANCIAL_SYS_PARAM::SOBName, AP_FINANCIAL_SYS_PARAM::AcctsPaySegments, AP_FINANCIAL_SYS_PARAM::PrepaySegments, AP_FINANCIAL_SYS_PARAM::FutureDatedPaymentSegments, AP_FINANCIAL_SYS_PARAM::RateVarGainSegments, AP_FINANCIAL_SYS_PARAM::RateVarLossSegments, AP_FINANCIAL_SYS_PARAM::DiscTakenSegments, AP_FINANCIAL_SYS_PARAM::MiscChargeSegments, AP_FINANCIAL_SYS_PARAM::FreightSegments, AP_FINANCIAL_SYS_PARAM::PrepayTaxDiffSegments, AP_FINANCIAL_SYS_PARAM::GainSegments, AP_FINANCIAL_SYS_PARAM::LossSegments, AP_FINANCIAL_SYS_PARAM::ExpenseAccrualSegments, AP_FINANCIAL_SYS_PARAM::PaymentMethodLookupCode, AP_FINANCIAL_SYS_PARAM::UserDefinedVendorNumCode, AP_FINANCIAL_SYS_PARAM::VendorNumStartNum, AP_FINANCIAL_SYS_PARAM::AlwaysTakeDiscFlag, AP_FINANCIAL_SYS_PARAM::PayDateBasisLookupCode, AP_FINANCIAL_SYS_PARAM::InvoiceCurrencyCode, AP_FINANCIAL_SYS_PARAM::PaymentCurrencyCode, AP_FINANCIAL_SYS_PARAM::FuturePeriodLimit, AP_FINANCIAL_SYS_PARAM::ReqEncumbranceFlag, AP_FINANCIAL_SYS_PARAM::PurchEncumbranceFlag, AP_FINANCIAL_SYS_PARAM::ManualVendorNumType, AP_FINANCIAL_SYS_PARAM::ReceiptAcceptanceDays, AP_FINANCIAL_SYS_PARAM::TermsDateBasis, AP_FINANCIAL_SYS_PARAM::HoldUnmatchedInvoicesFlag, AP_FINANCIAL_SYS_PARAM::ExclusivePaymentFlag, AP_FINANCIAL_SYS_PARAM::VatRegistrationNum, AP_FINANCIAL_SYS_PARAM::VatCountryCode, AP_FINANCIAL_SYS_PARAM::BankChargeBearer, AP_FINANCIAL_SYS_PARAM::MatchOption, AP_FINANCIAL_SYS_PARAM::GlobalAttributeCategory, AP_FINANCIAL_SYS_PARAM::GlobalAttribute1, AP_FINANCIAL_SYS_PARAM::GlobalAttribute2, AP_FINANCIAL_SYS_PARAM::GlobalAttribute3, AP_FINANCIAL_SYS_PARAM::GlobalAttribute4, AP_FINANCIAL_SYS_PARAM::GlobalAttribute5, AP_FINANCIAL_SYS_PARAM::GlobalAttribute6, AP_FINANCIAL_SYS_PARAM::GlobalAttribute7, AP_FINANCIAL_SYS_PARAM::GlobalAttribute8, AP_FINANCIAL_SYS_PARAM::GlobalAttribute9, AP_FINANCIAL_SYS_PARAM::GlobalAttribute10, AP_FINANCIAL_SYS_PARAM::GlobalAttribute11, AP_FINANCIAL_SYS_PARAM::GlobalAttribute12, AP_FINANCIAL_SYS_PARAM::GlobalAttribute13, AP_FINANCIAL_SYS_PARAM::GlobalAttribute14, AP_FINANCIAL_SYS_PARAM::GlobalAttribute15, AP_FINANCIAL_SYS_PARAM::GlobalAttribute16, AP_FINANCIAL_SYS_PARAM::GlobalAttribute17, AP_FINANCIAL_SYS_PARAM::GlobalAttribute18, AP_FINANCIAL_SYS_PARAM::GlobalAttribute19, AP_FINANCIAL_SYS_PARAM::GlobalAttribute20, AP_FINANCIAL_SYS_PARAM::NrTaxRounding, AP_FINANCIAL_SYS_PARAM::BuyingCompanyIdentifier, AP_FINANCIAL_SYS_PARAM::GaplessInvNumFlag, AP_FINANCIAL_SYS_PARAM::ExpenseAccrualCode, AP_FINANCIAL_SYS_PARAM::LiabilityPostLookupCode, AP_FINANCIAL_SYS_PARAM::TransEffectiveStartDate, AP_FINANCIAL_SYS_PARAM::TransEffectiveEndDate, AP_FINANCIAL_SYS_PARAM::MakeRateMandatoryFlag, AP_FINANCIAL_SYS_PARAM::EnterpriseId, AP_FINANCIAL_SYS_PARAM::EffectiveStartDate, AP_FINANCIAL_SYS_PARAM::EffectiveEndDate, AP_FINANCIAL_SYS_PARAM::SetCode, AP_FINANCIAL_SYS_PARAM::InternalLocationCode, AP_FINANCIAL_SYS_PARAM::MakeRateMandatoryPmtFlag, AP_FINANCIAL_SYS_PARAM::UserConversionRateType, AP_FINANCIAL_SYS_PARAM::UserDefaultPmtExchangeRateType, AP_FINANCIAL_SYS_PARAM::OneTimePayLiabSegments, AP_FINANCIAL_SYS_PARAM::OneTimePayExpenseSegments, AP_FINANCIAL_SYS_PARAM::RetainageSegments, AP_FINANCIAL_SYS_PARAM::UnclaimedFundsSegments -->
<!-- fscr-update-fields: AP_FINANCIAL_SYS_PARAM::SOBName, AP_FINANCIAL_SYS_PARAM::AcctsPaySegments, AP_FINANCIAL_SYS_PARAM::PrepaySegments, AP_FINANCIAL_SYS_PARAM::FutureDatedPaymentSegments, AP_FINANCIAL_SYS_PARAM::RateVarGainSegments, AP_FINANCIAL_SYS_PARAM::RateVarLossSegments, AP_FINANCIAL_SYS_PARAM::DiscTakenSegments, AP_FINANCIAL_SYS_PARAM::MiscChargeSegments, AP_FINANCIAL_SYS_PARAM::FreightSegments, AP_FINANCIAL_SYS_PARAM::PrepayTaxDiffSegments, AP_FINANCIAL_SYS_PARAM::GainSegments, AP_FINANCIAL_SYS_PARAM::LossSegments, AP_FINANCIAL_SYS_PARAM::ExpenseAccrualSegments, AP_FINANCIAL_SYS_PARAM::PaymentMethodLookupCode, AP_FINANCIAL_SYS_PARAM::UserDefinedVendorNumCode, AP_FINANCIAL_SYS_PARAM::VendorNumStartNum, AP_FINANCIAL_SYS_PARAM::AlwaysTakeDiscFlag, AP_FINANCIAL_SYS_PARAM::PayDateBasisLookupCode, AP_FINANCIAL_SYS_PARAM::InvoiceCurrencyCode, AP_FINANCIAL_SYS_PARAM::PaymentCurrencyCode, AP_FINANCIAL_SYS_PARAM::FuturePeriodLimit, AP_FINANCIAL_SYS_PARAM::ReqEncumbranceFlag, AP_FINANCIAL_SYS_PARAM::PurchEncumbranceFlag, AP_FINANCIAL_SYS_PARAM::ManualVendorNumType, AP_FINANCIAL_SYS_PARAM::ReceiptAcceptanceDays, AP_FINANCIAL_SYS_PARAM::TermsDateBasis, AP_FINANCIAL_SYS_PARAM::HoldUnmatchedInvoicesFlag, AP_FINANCIAL_SYS_PARAM::ExclusivePaymentFlag, AP_FINANCIAL_SYS_PARAM::VatRegistrationNum, AP_FINANCIAL_SYS_PARAM::VatCountryCode, AP_FINANCIAL_SYS_PARAM::BankChargeBearer, AP_FINANCIAL_SYS_PARAM::MatchOption, AP_FINANCIAL_SYS_PARAM::GlobalAttributeCategory, AP_FINANCIAL_SYS_PARAM::GlobalAttribute1, AP_FINANCIAL_SYS_PARAM::GlobalAttribute2, AP_FINANCIAL_SYS_PARAM::GlobalAttribute3, AP_FINANCIAL_SYS_PARAM::GlobalAttribute4, AP_FINANCIAL_SYS_PARAM::GlobalAttribute5, AP_FINANCIAL_SYS_PARAM::GlobalAttribute6, AP_FINANCIAL_SYS_PARAM::GlobalAttribute7, AP_FINANCIAL_SYS_PARAM::GlobalAttribute8, AP_FINANCIAL_SYS_PARAM::GlobalAttribute9, AP_FINANCIAL_SYS_PARAM::GlobalAttribute10, AP_FINANCIAL_SYS_PARAM::GlobalAttribute11, AP_FINANCIAL_SYS_PARAM::GlobalAttribute12, AP_FINANCIAL_SYS_PARAM::GlobalAttribute13, AP_FINANCIAL_SYS_PARAM::GlobalAttribute14, AP_FINANCIAL_SYS_PARAM::GlobalAttribute15, AP_FINANCIAL_SYS_PARAM::GlobalAttribute16, AP_FINANCIAL_SYS_PARAM::GlobalAttribute17, AP_FINANCIAL_SYS_PARAM::GlobalAttribute18, AP_FINANCIAL_SYS_PARAM::GlobalAttribute19, AP_FINANCIAL_SYS_PARAM::GlobalAttribute20, AP_FINANCIAL_SYS_PARAM::NrTaxRounding, AP_FINANCIAL_SYS_PARAM::BuyingCompanyIdentifier, AP_FINANCIAL_SYS_PARAM::GaplessInvNumFlag, AP_FINANCIAL_SYS_PARAM::ExpenseAccrualCode, AP_FINANCIAL_SYS_PARAM::LiabilityPostLookupCode, AP_FINANCIAL_SYS_PARAM::TransEffectiveStartDate, AP_FINANCIAL_SYS_PARAM::TransEffectiveEndDate, AP_FINANCIAL_SYS_PARAM::MakeRateMandatoryFlag, AP_FINANCIAL_SYS_PARAM::EffectiveStartDate, AP_FINANCIAL_SYS_PARAM::EffectiveEndDate, AP_FINANCIAL_SYS_PARAM::SetCode, AP_FINANCIAL_SYS_PARAM::InternalLocationCode, AP_FINANCIAL_SYS_PARAM::MakeRateMandatoryPmtFlag, AP_FINANCIAL_SYS_PARAM::UserConversionRateType, AP_FINANCIAL_SYS_PARAM::UserDefaultPmtExchangeRateType, AP_FINANCIAL_SYS_PARAM::OneTimePayLiabSegments, AP_FINANCIAL_SYS_PARAM::OneTimePayExpenseSegments, AP_FINANCIAL_SYS_PARAM::RetainageSegments, AP_FINANCIAL_SYS_PARAM::UnclaimedFundsSegments -->

The declarations allow 74 create inputs (including two `targetKey` selectors)
and 72 update inputs. Audit and derived automatic-offset fields are not caller
inputs; update keys are immutable and unspecified update values remain unchanged.
`SOBName` comes from ERP ledger evidence.
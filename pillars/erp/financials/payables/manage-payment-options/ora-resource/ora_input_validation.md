# Input Validation

<!-- fscr-supported-operations: create, update -->
<!-- fscr-create-fields: AP_SYSTEM_PARAMETER::BuName, AP_SYSTEM_PARAMETER::EnterpriseId, AP_SYSTEM_PARAMETER::BankChargeBearer, AP_SYSTEM_PARAMETER::BankChargeDeductionTypeDes, AP_SYSTEM_PARAMETER::TermName -->
<!-- fscr-update-fields: AP_SYSTEM_PARAMETER::WhenToAccountPmt, AP_SYSTEM_PARAMETER::PostDatedPaymentsFlag, AP_SYSTEM_PARAMETER::AllowSupplierBankOverride, AP_SYSTEM_PARAMETER::PayDocCategoryOverride, AP_SYSTEM_PARAMETER::AllowPymtThirdPartyOvrd, AP_SYSTEM_PARAMETER::BankChargeBearer, AP_SYSTEM_PARAMETER::BankChargeDeductionTypeDes -->

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Exact FSM package contract | Matching AP_SYSTEM_PARAMETER.csv header, ASM_SETUP_CSV_METADATA.xml, and task identity AP_MANAGE_PAYMENT_OPTIONS | Block preview | Use the supplied current-data and template exports for this exact task | Always | |
| Target business-unit scope | Business unit identity from the requested change and one unique package row | Block preview | Provide an unambiguous target business unit and reconcile it to a fresh same-task export | Before any candidate is prepared | |
| Shared system-options contract | A compatible Manage Invoice Options AP_SYSTEM_PARAMETER adapter/runtime is available and accepts the complete candidate row | Block preview | Restore or refresh the sibling task contract; do not bypass it with a payment-only package | Every supported Payment operation | `../manage-invoice-options/e2e-adapter.json`; `../manage-invoice-options/scripts/fsm_task_adapter.py` |
| Submitted optional Payment field | A value for each Payment Options control the requester chose to change | Block preview | Validate the submitted value against that field's exact task contract; preserve the baseline value for every omitted optional field | When a Payment Options value is supplied | Field-specific task contract |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Package identity, target scope, or field contract is incomplete | Blocked | Do not build a candidate; resolve the missing evidence | |
| Sibling Invoice Options shared-row contract rejects the complete proposed AP_SYSTEM_PARAMETER row | Blocked | Correct the reported shared field, prerequisite, lookup receipt, or default; then regenerate the Payment candidate | Manage Invoice Options runtime |
| Package, target scope, and requested payment-accounting evidence are complete | Ready for governed preview | Route preview and any import only through core.data-loader | |

## Field Validation

## Business-Control-to-Package Mapping

| UI control | Exact task-package field | Customer validation behavior |
|---|---|---|
| Allow payment date before the system date | `PostDatedPaymentsFlag` (`Y`/`N`) | Validate `Y` or `N`; do not substitute `FutureDatedPmtLiabRelief`. |
| Allow override of supplier site bank account | `AllowSupplierBankOverride` | Validate `Y` or `N`. |
| Allow document category override | `PayDocCategoryOverride` | Validate `Y` or `N`. |
| Allow payee override for third-party payments | `AllowPymtThirdPartyOvrd` | Validate `Y` or `N`. |
| Account for Payment | `WhenToAccountPmt` | Use the observed package code: `PAYMENT ONLY` (At payment issue), `CLEARING ONLY` (At payment clearing), or `BOTH` (At payment issue and clearing). Oracle's [SystemOptionEO declaration](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBFPHDEV_LINUX.X64/fusionapps/fin/components/payables/ap/sharedSetup/payablesSystemOptions/model/src/oracle/apps/financials/payables/sharedSetup/payablesSystemOptions/model/entity/SystemOptionEO.xml#2207) sets `Precision="30"` for this field, so reject values longer than 30 characters before preview. |
| Bank Charge Deduction Type | `BankChargeDeductionTypeDes` | Use `S` for Standard, `N` for Negotiated, or `X` for None. |
| Minimum days to initiate escheatment | `EscheatmentEligibilityPeriod` | Require a nonnegative integer. |

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Archive identity | Accept only the exact AP_SYSTEM_PARAMETER setup archive whose metadata matches Manage Payment Options | Always | |
| Header and node fidelity | Preserve the exact template header order, XML node path, and CSV field count including trailing blanks | Always | |
| Shared-row integrity | Merge the approved Payment fields onto the exact baseline row, then validate that complete row through the Invoice Options AP_SYSTEM_PARAMETER contract. When Payment create is lifecycle-enabled from fresh task evidence, validate the complete proposed row and its Invoice-owned prerequisites/defaults through the same contract. | Every supported Payment operation | Manage Invoice Options runtime |
| Submitted Payment field | Serialize only a Payment Options field the requester explicitly supplies. Validate it against its own code/value contract and preserve the baseline value for every omitted optional field. | When any Payment Options field is edited | Field-specific task contract |
| Optional-field update evidence | Apply the same validation to every optional Payment field. If updateability for a requested field is not confirmed, require a governed application-validation override bound exactly to that field; do not treat another field's successful import evidence as exclusive support. | When an optional Payment field is edited | Field-specific update contract |
| Payment-date override | Map **Allow payment date before the system date** to `PostDatedPaymentsFlag` (`Y`/`N`). Do not substitute `FutureDatedPmtLiabRelief`. | When supplied | Exact current/template export |
| Supplier-bank override | Map **Allow override of supplier site bank account** to AllowSupplierBankOverride. Accept only Y or N when supplied; preserve the baseline value otherwise. | When supplied | |
| Payment document-category override | Map **Allow document category override** to PayDocCategoryOverride. Accept only Y or N when supplied; do not substitute the invoice-side InvDocCategoryOverride field. | When supplied | |
| Third-party payee override | Map **Allow payee override for third-party payments** to AllowPymtThirdPartyOvrd. Accept only Y or N when supplied. | When supplied | |
| Conversion-rate requirement | Map **require** or **enable** to Yes (`Y`) and **do not require** to No (`N`). Preserve the exported value when omitted. | When supplied | |
| Bank-charge deduction type | Map **Standard** to `S`, **Negotiated** to `N`, and **None** to `X` in `BankChargeDeductionTypeDes`. | When supplied | |
| Escheatment minimum days | Map **Minimum days to initiate escheatment** to `EscheatmentEligibilityPeriod`. Require a nonnegative integer when supplied. | When supplied | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PAYOPT.VALIDATE_INPUT | step | 10 | validate_input | valid->PAYOPT.CHECK_DEPENDENCIES;invalid->PAYOPT.INPUT_BLOCKED | none | stop | Always |

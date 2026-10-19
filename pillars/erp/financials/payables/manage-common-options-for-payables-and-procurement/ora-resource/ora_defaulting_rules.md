# Manage Common Options for Payables and Procurement Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| GaplessInvNumFlag | N | A new Financials Options entity row is initialized and the user has not supplied a value | No |  |
| ExpenseAccrualCode | RECEIPT | A new Financials Options entity row is initialized and the user has not supplied a value | No |  |
| DefaultExchangeRateType | Corporate | A new Financials Options entity row is initialized; this is an internal entity attribute with no direct FSM CSV header | No |  |
| LiabilityPostLookupCode | NONE | A new Financials Options entity row is initialized and the user has not supplied a value | No |  |
| MakeRateMandatoryFlag | Y | A new Financials Options entity row is initialized and the user has not supplied a value | No |  |
| DefaultPmtExchangeRateType | Corporate | A new Financials Options entity row is initialized; this is an internal entity attribute with no direct FSM CSV header | No |  |
| MakeRateMandatoryPmtFlag | Y | A new Financials Options entity row is initialized and the user has not supplied a value | No |  |
| PaymentMethodLookupCode, UserDefinedVendorNumCode, VendorNumStartNum, FuturePeriodLimit, ManualVendorNumType, ReceiptAcceptanceDays, TermsDateBasis | NULL; omit from create operation values and retain the empty CSV cells | Fusion creates a first-time Financials Options row and the user has not supplied one of these fields | No |  |
| EnterpriseId | Explicit row value first; otherwise the uniquely matched update-row value, then the single distinct nonblank export value | Every candidate row; apply Enterprise ID precedence below | No; always honor a nonblank explicit row value | resolve_bu_context_from_name |
| SOBName | `Name` returned by `ledgersLOV/{PrimaryLedgerId}` | A candidate is constructed after the exact Financials BU lookup returns `PrimaryLedgerId` | No; reject a manual override | resolve_bu_context_from_name |
| Any other AP_FINANCIAL_SYS_PARAM field without a listed entity default | No automatic task default | A new or existing row | No |  |

The entity metadata defaults above are not values to synthesize into an update of an existing options row; a supplied candidate value takes precedence for those entity defaults. `EnterpriseId` follows the explicit-input precedence below.

The seven `NULL` defaults are deliberately narrow. They are initialization behavior, not an accepted raw-value domain. The adapter therefore removes only an empty or null **create** input for these fields before it validates and builds the full 81-column CSV row. An empty value on an **update** remains an explicit clear request; it receives the same transport-sanity treatment as any other non-product-validated value and is not silently defaulted. No other unresolved export-only field gains an automatic default from this rule.

## Enterprise ID Precedence

Apply this user-approved preparation policy in order for each row:

1. Use a nonblank user-supplied `EnterpriseId` for that row, even when it differs from the export. Do not request confirmation just because it differs. Retain the CSV long-integer sanity check.
2. Without an explicit value, use the nonblank `EnterpriseId` on the uniquely matched existing update row.
3. Otherwise, use the fresh exact-task export's single distinct nonblank `EnterpriseId` automatically, without confirmation. Ignore blank cells, and count repeated occurrences of the same nonblank ID as one distinct value.
4. Ask for `EnterpriseId` only when neither an explicit value, a uniquely matched update-row value, nor a single export value resolves it. An empty export, all-blank export, or multiple distinct IDs is not a blocker when the user supplies the row's ID.
5. An explicit row value affects only that row. It never replaces, seeds, or invalidates the export-derived default for other rows, and it does not introduce an ambiguous-default state.
6. Persist the export default, its source, status, and baseline fingerprint only in the current design/preflight artifact (`enterpriseIdDefaults`). Recompute it from that run's fresh export; do not save it in skill configuration or carry it to another run.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| APCO.APPLY_DEFAULTS | step | 40 | apply_default | applied->APCO.ENFORCE_DESIGN;not_applicable->APCO.ENFORCE_DESIGN;blocked->APCO.HANDLE_ERROR | APCO.CHECK_DEPENDENCIES | stop | Apply EnterpriseId precedence for every row; for a first-time UI row, report fixed entity defaults and conditional Reference Integration defaults without auto-populating Reference Integration accounts into an FSM candidate |

# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_business_unit_by_name_and_enterprise | A create candidate needs FSM import context | Requester-supplied BuName and optional EnterpriseId | `resolve_lookup_prerequisites.py` calls `GET /fscmRestApi/resources/11.13.18.05/finBusinessUnitsLOV` for the exact active BU and records its ID and PrimaryLedgerId. EnterpriseId is resolved locally from the explicit create row, current-run default, or one distinct nonblank value in the fresh FSM export; no CRM, BICC, SQL, or BU-to-enterprise call is used. | BusinessUnitId, ActiveFlag, EnterpriseId | Require one active exact BU and one deterministic EnterpriseId under the documented precedence | EnterpriseId -> BusinessUnitId -> OrgId | Block zero or multiple BU matches, an inactive BU, or a blank EnterpriseId with no unambiguous current-run default. Never create a business unit. |
| resolve_payment_term_from_name | TermName, PrepaymentTermName, or EmployeeTermName is populated | One supplied term name | `GET /fscmRestApi/resources/11.13.18.05/payablesPaymentTerms?onlyData=true&fields=name,termsId&q=name='<requested-name>'`; `resolve_lookup_prerequisites.py` records the response receipt. | Returned record count | One readable result continues. Multiple results are advisory without local ID selection. | Submitted term name; returned names and IDs are corroborating evidence only. FSM resolves TermName, PrepaymentTermName, and EmployeeTermName in its import context. | Block a readable zero-result. Multiple results or unavailable read access are advisory; Fusion import validates and resolves the value again. |
| resolve_terms_date_basis | `TermsDateBasis` is supplied | Requested code | Built-in system allowlist; no REST request | exact code | Allow `Current` (System date), `Goods Received` (Goods received date), `Invoice` (Invoice date), or `Invoice Received` (Invoice received date). | Validated Terms Date Basis code | Block any other value. |
| resolve_accounting_date_basis | `GlDateFromReceiptFlag` is supplied | Requested code | Built-in system allowlist; no REST request | exact code | Allow `CURRENT` (System date), `GOODS RECEIVED/CURRENT` (Goods received or system date), `GOODS RECEIVED/INVOICE` (Goods received or invoice date), or `INVOICE` (Invoice date). | Validated Accounting Date Basis code | Block any other value. |
| resolve_pay_date_basis | `PayDateBasisLookupCode` is supplied | Requested code | Built-in system allowlist; no REST request | exact code | Allow only `DISCOUNT` or `DUE`. | Validated Pay Date Basis code | Block any other value. |
| Budget Date Basis | `BudgetDateBasis` is supplied | Requested code | No task-owned lookup; no REST request | N/A | Recognized codes are `ACC` (Accounting date), `INV` (Invoice date), and `SYS` (System date). | Submitted code | Fusion validates the submitted code during import. |
| pass_through_budget_date_basis | `BudgetDateBasis` is supplied | Requested code | No task-owned preflight; customer-configured lookup | N/A | Preserve the supplied CSV code. | Submitted value | Fusion validates it during the governed import. |
| pass_through_vendor_pay_group | `VendorPayGroupLookupCode` is supplied | Requested code | No task-owned preflight; customer-configured lookup | N/A | Preserve the supplied CSV code. | Submitted value | Fusion validates it during the governed import. |
| pass_through_employee_pay_group | `EmployeePayGroupLookupCode` is supplied | Requested code | No task-owned preflight; customer-configured lookup | N/A | Preserve the supplied CSV code. | Submitted value | Fusion validates it during the governed import. |
| resolve_account_derivation_method | Account Derivation Method is supplied | Requested display value | Built-in system allowlist; no REST request | exact value | A blank represents None. Otherwise allow only `Transaction Account Builder`. | Validated Account Derivation Method value | Block any other nonblank value. |
| resolve_discount_distribution_method | Nonblank `DiscountDistributionMethod` is supplied | Requested code | Built-in system allowlist; no REST request | exact code | A blank is permitted; otherwise allow `EXPENSE` (All invoice lines), `SYSTEM` (Single distribution), or `TAX` (Tax lines and single distribution). | Validated Discount Allocation Method code | Block any other nonblank value. |
| resolve_approval_timing | `ApprovalTiming` is supplied | Requested code | Built-in system allowlist; no REST request | exact code | Allow `A` (Require approval before accounting), `N` (Account regardless of approval status), or `Y` (Require accounting before approval). The control is editable only when Enable invoice approval is Yes. | Validated Accounting Preference code | Block any other nonblank value. When invoice approval is No, preserve the existing blank or `N` value and do not set `A` or `Y`. |
| resolve_interest_proration_method | Nonblank `ProrateIntInvAcrossDists` is supplied | Requested code | Built-in system allowlist; no REST request | exact code | A blank is permitted; otherwise allow `N` (Single distribution) or `Y` (All invoice lines). | Validated Interest Allocation Method code | Block any other nonblank value. |
| resolve_ss_unit_price_change | Nonblank `SsUpriceChangeForQtymatch` is supplied | Requested code | Built-in system allowlist; no REST request | exact code | A blank is permitted; otherwise allow `NO` (No), `PRICE DECREASE ONLY` (Price decrease only), `PRICE INCREASE ONLY` (Price increase only), or `PRICE INCREASE OR DECREASE` (Price increase or decrease). | Validated Quantity-Based Match Unit Price Change code | Block any other nonblank value. |
| resolve_invoice_currency | `InvoiceCurrencyCode` is supplied | Requested `InvoiceCurrencyCode`, trimmed and uppercased, and a read-only currency receipt | `GET /fscmRestApi/resources/11.13.18.05/currenciesLOV?finder=CurrencyCodeAllRowsFinder;CurrencyCode=<canonical-code>`; `resolve_lookup_prerequisites.py` records the canonical receipt. | Returned record count | One readable result continues. Multiple results are advisory without selecting a returned value. | Canonical uppercase invoice currency code; returned values are corroborating evidence only. FSM validates the code in import context. | Block a readable zero-result. Multiple results or unavailable read access are advisory. |
| resolve_payment_currency | `PaymentCurrencyCode` is supplied | Requested `PaymentCurrencyCode`, trimmed and uppercased, and a read-only currency receipt | `GET /fscmRestApi/resources/11.13.18.05/currenciesLOV?finder=CurrencyCodeAllRowsFinder;CurrencyCode=<canonical-code>`; `resolve_lookup_prerequisites.py` records the canonical receipt. | Returned record count | One readable result continues. Multiple results are advisory without selecting a returned value. | Canonical uppercase payment currency code; returned values are corroborating evidence only. FSM validates the code in import context. | Block a readable zero-result. Multiple results or unavailable read access are advisory. |
| InterestSegments | `AutoCalculateInterestFlag` is Y and `SOBName` or `InterestSegments` is supplied | Requested `SOBName` and complete `InterestSegments` | No task-owned CCID/SOAP preflight. | N/A | Preserve the submitted values without a CCID validation call. | Submitted ledger and segments | Fusion FSM Import performs the authoritative account-combination validation. |
| resolve_business_unit_primary_ledger | A new AP_SYSTEM_PARAMETER row is created from BuName | Requested `BuName` and two read-only REST receipts | `resolve_lookup_prerequisites.py` queries `finBusinessUnitsLOV` for the exact BU and `ledgersLOV/{PrimaryLedgerId}` for Name and CurrencyCode. | BU: `matchedBuName`, `primaryLedgerId`; ledger: `ledgerId`, `name` | Require one or more active exact BU rows with one shared, nonblank PrimaryLedgerId, and a ledger receipt whose ID and Name match it. | Attested SOBName and BaseCurrencyCode for the new row | Block a missing, malformed, or conflicting-primary-ledger receipt. |

## Business Labels to CSV Codes

When a requester supplies one of these business labels, normalize it to the listed code before serializing the CSV. The CSV contains the code, not the business label.

| Customer-Facing Label (CSV Field) | Requester Wording | CSV Code |
|---|---|---|
| Invoice Entry — Terms Date Basis (`TermsDateBasis`) | System date | `Current` |
| Invoice Entry — Terms Date Basis (`TermsDateBasis`) | Goods received date | `Goods Received` |
| Invoice Entry — Terms Date Basis (`TermsDateBasis`) | Invoice date | `Invoice` |
| Invoice Entry — Terms Date Basis (`TermsDateBasis`) | Invoice received date | `Invoice Received` |
| Invoice Entry — Accounting Date Basis (`GlDateFromReceiptFlag`) | System date | `CURRENT` |
| Invoice Entry — Accounting Date Basis (`GlDateFromReceiptFlag`) | Goods received or system date | `GOODS RECEIVED/CURRENT` |
| Invoice Entry — Accounting Date Basis (`GlDateFromReceiptFlag`) | Goods received or invoice date | `GOODS RECEIVED/INVOICE` |
| Invoice Entry — Accounting Date Basis (`GlDateFromReceiptFlag`) | Invoice date | `INVOICE` |
| Invoice Entry — Pay Date Basis (`PayDateBasisLookupCode`) | Discount date | `DISCOUNT` |
| Invoice Entry — Pay Date Basis (`PayDateBasisLookupCode`) | Due date | `DUE` |
| Invoice Entry — Budget Date Basis (`BudgetDateBasis`) | Accounting date | `ACC` |
| Invoice Entry — Budget Date Basis (`BudgetDateBasis`) | Invoice date | `INV` |
| Invoice Entry — Budget Date Basis (`BudgetDateBasis`) | System date | `SYS` |
| Discount — Discount Allocation Method (`DiscountDistributionMethod`) | All invoice lines | `EXPENSE` |
| Discount — Discount Allocation Method (`DiscountDistributionMethod`) | Single distribution | `SYSTEM` |
| Discount — Discount Allocation Method (`DiscountDistributionMethod`) | Tax lines and single distribution | `TAX` |
| Invoice Entry — Account Derivation Method (`AccountDefaultBasisCodeDes`) | None | blank |
| Invoice Entry — Account Derivation Method (`AccountDefaultBasisCodeDes`) | Transaction Account Builder | `Transaction Account Builder` |
| Approval — Accounting Preference (`ApprovalTiming`) | Require approval before accounting | `A` |
| Approval — Accounting Preference (`ApprovalTiming`) | Account regardless of approval status | `N` |
| Approval — Accounting Preference (`ApprovalTiming`) | Require accounting before approval | `Y` |
| Interest — Interest Allocation Method (`ProrateIntInvAcrossDists`) | Single distribution | `N` |
| Interest — Interest Allocation Method (`ProrateIntInvAcrossDists`) | All invoice lines | `Y` |
| Self-Service Invoices — Allow Unit Price Change for Quantity-Based Matches (`SsUpriceChangeForQtymatch`) | No | `NO` |
| Self-Service Invoices — Allow Unit Price Change for Quantity-Based Matches (`SsUpriceChangeForQtymatch`) | Price decrease only | `PRICE DECREASE ONLY` |
| Self-Service Invoices — Allow Unit Price Change for Quantity-Based Matches (`SsUpriceChangeForQtymatch`) | Price increase only | `PRICE INCREASE ONLY` |
| Self-Service Invoices — Allow Unit Price Change for Quantity-Based Matches (`SsUpriceChangeForQtymatch`) | Price increase or decrease | `PRICE INCREASE OR DECREASE` |
| Payment Accounting and Overrides — Account for Payment (`WhenToAccountPmt`) | At payment issue | `PAYMENT ONLY` |
| Payment Accounting and Overrides — Account for Payment (`WhenToAccountPmt`) | At payment clearing | `CLEARING ONLY` |
| Payment Accounting and Overrides — Account for Payment (`WhenToAccountPmt`) | At payment issue and clearing | `BOTH` |

Payment-term names, currency codes, and pay-group codes are not translated by this table. Preserve or resolve them using their documented lookup rules.

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A business-unit create is requested | The executor resolves the active BU using `finBusinessUnitsLOV`. For EnterpriseId it uses the explicit requester value for that row, then the current-run default, then exactly one distinct nonblank value in the fresh FSM export. A conflicting explicit value applies only to that row and makes later blank create rows require requester confirmation. No CRM, BICC, or SQL evidence path is used. |
| A payment-term name is changed | `resolve_lookup_prerequisites.py` blocks a readable zero-result. One readable result continues; multiple results and unavailable reads are recorded as advisory evidence. The offline adapter does not apply local case or uniqueness matching and does not issue the REST request; Fusion import remains authoritative for advisory outcomes. |
| A page-bound lookup value is changed | For immutable system lookup types, the adapter validates the submitted code against the task-owned allowlist and makes no REST request. For extensible or user-controlled types (`BUDGET_DATE_BASIS`, `PAY GROUP`, and `ORA_APPRVL_ACCNTNG_PREFERENCE`), preserve the supplied CSV code without task-owned lookup preflight; Fusion validates it during the governed import. |
| An invoice or payment currency is changed | The executor trims and uppercases the code before querying `currenciesLOV` with `CurrencyCodeAllRowsFinder`; the canonical uppercase code is retained for FSM CSV generation. A readable zero-result blocks. One readable record continues; multiple records or an unavailable read are advisory. The offline adapter performs the same currency-code normalization but does not issue the lookup request. |
| A controlled FSM import is later approved | Let core.data-loader and Fusion's task import validation assess the candidate package; preserve the returned dependency diagnostic and do not retry automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LOOKUP.PREFLIGHT | step | 15 | reference_lookup | success->DEP.CHECK;failure->ERROR.BLOCK | INPUT.VALIDATE | stop | Any populated field has a resolver in the Live Lookups table. Run every applicable read-only REST or SOAP resolver and retain its receipt. |

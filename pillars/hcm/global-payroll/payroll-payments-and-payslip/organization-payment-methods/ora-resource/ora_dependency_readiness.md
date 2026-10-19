# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Legislative context | Confirm the LDG and its legislation before selecting country-specific payment types and rules |
| 2 | Cash Management setup | Resolve legal-employer names for the LDG, then confirm banks, branches, and the intended account are configured before mapping a PaymentSource |
| 3 | Payroll bank-account eligibility | Confirm the account is active, enabled for Payroll account use, and associated with a PSU legal entity or a legal employer whose parent is a PSU |
| 4 | Tax reporting units | Confirm referenced TRUs exist before loading TRU-specific PaymentMethodRule rows |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| OPM.LDG_CONTEXT | Legislative data group and legislation | Yes | Every request | Verify | Oracle HCM legislative setup | resolve_ldg_by_exact_name | Payment types and country rules vary by legislation | Provide or verify the exact LDG and legislation | LegislativeDataGroupName, LegislationCode |
| OPM.CASH_MANAGEMENT | Banks, branches, and bank account | Yes | Payment sources are loaded | Verify | Oracle Cloud Cash Management | resolve_legal_employer_names_by_ldg | PaymentSource must reference an existing source bank account or other documented source of funds | Resolve legal-employer names before the bank-account resolver, then configure and identify the exact account | LegalEmployerNames |
| OPM.PAYROLL_ACCOUNT | Payroll-eligible active bank account | Yes | Oracle Fusion Global Payroll or Cloud Payroll processes payments | Verify | Oracle Cloud Cash Management and payroll bank-account setup | resolve_bank_account_by_legal_employer | The account must be active, enabled for Payroll use, and associated with a PSU legal entity or qualifying legal employer | Resolve identity and activity together using the resolver's declared metadata and detail reads when needed; complete available read-only verification before declaring a workflow gap; correct actual bank-account eligibility failures before preview | BankAccountId or BankAccountName, Active status for the effective date, startDate and endDate evidence, Account Use, PSU association |
| OPM.TRU | Tax reporting units | Conditional | PaymentMethodRule uses TaxReportingUnitName | Verify | Oracle HCM tax reporting unit setup | resolve_tax_reporting_unit_by_ldg | TRU rules select the appropriate PaymentSource | Create or identify each referenced TRU before loading rules | TaxReportingUnitName |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Every applicable dependency is verified | Yes, read-only lookup only; loading remains HCM Data Loader |
| Needs verification contract | A documented dependency has no authorized resolver contract | No |
| Needs prerequisite setup | Bank, PSU, or TRU setup is missing | No |
| Not applicable | The conditional dependency does not apply to the requested HDL hierarchy | No lookup needed |

## Supplemental Scoped-Authentication Prerequisites

These requirements supplement the existing dependency rules. They do not replace any existing dependency, resolver, or execution instruction.

| Sequence | Prerequisite | What Must Happen |
|---|---|---|
| 0a | Fusion-scoped client | Before any Organization Payment Methods task work, obtain a Fusion client and access token using the Fusion scope. |
| 0b | BOSS-scoped client | Before any Organization Payment Methods task work, obtain a separate BOSS client and access token using the BOSS scope. |
| 0c | Scoped-client selection | Select the client by endpoint class for every request; never treat a Fusion-scoped token as sufficient for a BOSS service. |

| Endpoint Class | Applies When | Required Client and Scope | Readiness Result |
|---|---|---|---|
| Fusion service | A request targets a non-BOSS Fusion endpoint | Fusion client with a Fusion-scope access token | Block the request if the Fusion-scoped client cannot be obtained. |
| BOSS service | A request targets `/api/boss/data/objects/ora/erpCore/bankingSetup/v1/bankAccounts`, its exact-account item, or the bank-account OpenAPI metadata declared in ora_reference_lookups.md | BOSS client with a BOSS-scope access token | Block the request if the BOSS-scoped client cannot be obtained; do not substitute the Fusion-scoped token. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| OPM.VALIDATE_DEPENDENCIES | decision | 3 | resolve_dependency | ready->OPM.CHECK_DUPLICATE;blocked->OPM.FAILED | OPM.VALIDATE_RULE_CONDITIONS | stop | Every request | |

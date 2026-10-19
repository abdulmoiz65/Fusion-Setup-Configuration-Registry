# Payroll Definitions Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Classify the object and operation | Keep HDL preparation for PayrollDefinition, ValidPaymentMethod, and PayrollTimePeriod on HCM Data Loader. Validate VBCS/Redwood calendar inputs against PayrollDVO and the read-only resolvers; do not infer a VBCS mutation route. |
| 2 | Confirm target metadata | Reconcile the exact target header, action, key, requiredness, type, length, reference, and localization contract before production preparation. |
| 3 | Resolve dependencies | Validate the LDG, Consolidation Group / Consolidation Set business object, mapped lookup values, period type, existing payroll definition, default OPM, additional OPMs, and their effective dates in dependency order. |
| 4 | Apply supported defaults | Default a valid PlannedSubmissionFixedDate date-only value to start-of-day before design enforcement. |
| 5 | Validate calendar design | Use one coherent dynamic-offset pattern or a target-supported fixed-date pattern and preserve payroll-cycle date relationships. |
| 6 | Preserve effective-dated identity | Keep stable source or user keys, immutable outer effective boundaries, generated-period user keys, and unique schedule names. |
| 7 | Protect mutation handoff | Require a complete preview, explicit approval, authorized HDL workflow, single submission, and safe result verification for any live load. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| An HDL create, update, bulk migration, calendar extension, or period adjustment is prepared | Error | | A REST or internal UI mutation route is selected | Use HCM Data Loader and the exact target-exported business-object header | Yes |
| A VBCS/Redwood create or update is requested | Error | | The exact method, payrollGeneric endpoint, PayRestName, payload, required fields, and date serialization are not source-evidenced | Validate the sourced PayrollDVO fields and read-only references, then stop with a missing-VBCS-create-contract blocker; do not demand an HDL template for VBCS-only calendar fields | Yes |
| A production DAT is prepared | Error | | The applicable target View Business Objects attribute export is missing or has not been reconciled | Export and review the target metadata for every in-scope object before finalizing the DAT | Yes |
| An LDG reference is used | Error | resolve_legislative_data_group | The value does not resolve exactly once, is invalid for the load date, or uses a reference form different from the exported header | Preserve the exact target-supported name or source-key reference and retain runtime REST IDs separately | Yes |
| A Consolidation Group or Consolidation Set is used | Error | resolve_consolidation_group_or_set_by_ldg | The same business object is missing, ambiguous, incompletely paged, or belongs to another LDG; absence of a separately supplied ConsolidationSetCode is not a blocker when a documented name alias is supplied | Derive ConsolidationSetCode from the same exact supplied name alias and resolve exactly one Consolidation Group / Consolidation Set in the payroll LDG without prompting for the code | Yes |
| A mapped Payroll Definition lookup value is used | Error | resolve_payroll_definition_lookup_code | The exact supplied value does not resolve exactly once against Code or Meaning within its explicit mapped LookupType | Use only PAY_BASE_DATE, PAY_BASE_OFFSET, HRC_YES_NO, PAY_DATE_OFFSET, or PAY_PROC_PERIOD_TYPE mappings supported by the supplied source | Yes |
| Allow Negative Payments is supplied | Error | resolve_allow_negative_payments_lookup_code | The exact supplied value does not resolve to exactly one HRC_YES_NO Code or Meaning | Preserve the matched actual Code under AllowNegativePaymentsFlag | Yes |
| A period type or calendar pattern is selected | Error | resolve_period_type_by_legislation | The code is unresolved, unsupported for the legislation, or paired with an unconfirmed calendar pattern | Select a target-supported period type and validate all schedule fields as one design | Yes |
| Fixed dates are proposed | Error | resolve_period_type_by_legislation | Target metadata does not confirm fixed-date support for the selected period type | Use fixed dates only for a confirmed supported period type; the supplied public example establishes Calendar Month only | Yes |
| Dynamic offsets are proposed | Error | resolve_period_type_by_legislation | Falls, day type, offset, and base-date values are incomplete or copied from another period type without validation | Confirm the complete schedule for the selected LDG and period type | Yes |
| A PayrollDefinition default OPM is selected | Error | resolve_organization_payment_method_by_ldg_and_date | The OPM is missing, ambiguous, incompletely paged, outside the LDG or effective date, is EFT, or is placed in an unsupported final reference field; absence of a separately supplied OrganizationPaymentMethodCode is not a blocker when a documented name alias is supplied | Derive OrganizationPaymentMethodCode from the same exact supplied OPM name or base-name alias, resolve one effective non-EFT OPM, and use only the target-supported final reference form without prompting for the code | Yes |
| A ValidPaymentMethod row is prepared | Error | resolve_organization_payment_method_by_ldg_and_date | The eligible-OPM contract is unresolved, the OPM is unresolved, incompletely paged, or the child range falls outside the payroll or OPM range | Confirm the target lookup and header, then use one eligible OPM with compatible dates | Yes |
| An existing PayrollDefinition is updated or extended | Error | resolve_payroll_definition_by_ldg_and_effective_date | PayrollName is not an exact match in the requested LDG, its effective range excludes SysEffectiveDate, or more than one row remains | Resolve and retain the one effective PayrollId before using any metadata-supported update key | Yes |
| The payroll definition supports dependent or historical data | Error | | EffectiveStartDate is later than any referring data | Start the definition on or before the earliest dependent date | Yes |
| An existing PayrollDefinition is updated | Error | | The first effective start date or last effective end date changes | Preserve both existing outer effective boundaries | No |
| NumberOfYears changes | Error | | The value decreases or one extension exceeds ten years | Increase only, in increments of ten years or fewer | Yes |
| A generated schedule is created or extended | Error | | A payroll name is duplicated within the definition | Use unique names throughout the generated schedule | Yes |
| DateEarned is generated or adjusted | Error | | DateEarned falls outside the payroll period effective dates | Correct the calendar event date before preparation | Yes |
| A PayrollTimePeriod is adjusted | Error | | An application-generated source key is invented or target-confirmed user keys are missing | Use the documented PayrollCode, LDG, PeriodCategory, StartDate, and any additional target-confirmed user keys | Yes |
| Ledger, costing accounts, negative-payment behavior, DFF, or EFF data is proposed | Error | resolve_payroll_ledger_by_ldg | The target business-object export does not confirm the attribute and constraints | Omit the field until target metadata confirms it; a lookup route alone does not establish HDL support | Yes |
| Delete, end-date, correction, or retroactive time-period behavior is proposed | Error | | The target metadata does not confirm the action and key contract | Stop and obtain target-pod evidence before preparation or execution | No |
| A localized field, label, period type, flexfield, or validation is used | Error | | It is generalized from another country or is absent from target metadata | Validate it against the intended LDG, localized UI, and target View Business Objects export | Yes |
| Any lookup contract field remains unresolved | Error | | A live lookup or production-readiness claim depends on the unresolved contract | Keep the task incomplete and obtain target-pod evidence | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_legislative_data_group | Any in-scope object uses an LDG reference | Target-supported LDG reference, display name, legislation code, effective validity | ora_reference_lookups.md |
| resolve_consolidation_group_or_set_by_ldg | PayrollDefinition uses the Consolidation Group / Consolidation Set business object | ConsolidationSetId, ConsolidationSetName, ConsolidationSetCode, LDG relationship, and audit evidence | ora_reference_lookups.md |
| resolve_payroll_definition_lookup_code | A mapped Payroll Definition lookup value is supplied | Exact Code and Meaning for its explicit LookupType mapping | ora_reference_lookups.md |
| resolve_allow_negative_payments_lookup_code | AllowNegativePaymentsFlag is supplied | Matched actual HRC_YES_NO Code and Meaning | ora_reference_lookups.md |
| resolve_period_type_by_legislation | PayrollDefinition selects a period type or calendar pattern | PeriodTypeCode and target-supported dynamic or fixed-date behavior | ora_reference_lookups.md |
| resolve_organization_payment_method_by_ldg_and_date | PayrollDefinition or ValidPaymentMethod selects an OPM | OrgPaymentMethodId, OPM name, base name, payment type, category, currency, LDG, and effective range | ora_reference_lookups.md |
| resolve_payroll_definition_by_ldg_and_effective_date | PayrollDefinition is updated or extended | PayrollId, exact name, LDG, Consolidation Group / Consolidation Set, period type, effective dates, and audit evidence | ora_reference_lookups.md |
| resolve_payroll_ledger_by_ldg | Target metadata confirms a ledger field | Target-supported ledger reference | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PD.ENFORCE_DESIGN | decision | 5 | design_enforcement | pass->PD.EXECUTION_GATE;blocked->PD.HANDLE_ERROR | PD.APPLY_DEFAULTS | stop | Any Payroll Definitions request |

## Sources

- Developer-provided PayrollDefinition-HDL.md, accessed 2026-08-13.
- Developer-provided PayrollDVO source, accessed 2026-08-14.
- Oracle Fusion Cloud HCM, Payroll Definitions and Time Periods: Overview: https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/payroll-definitions-and-time-periods-overview.html
- Oracle Fusion Cloud HCM, Payroll Definitions: https://docs.oracle.com/en/cloud/saas/human-resources/25b/faipk/payroll-definitions.html
- Oracle Fusion Cloud HCM, How Pay Frequency Components Work Together: https://docs.oracle.com/en/cloud/saas/human-resources/fapid/how-pay-frequency-components-work-together.html

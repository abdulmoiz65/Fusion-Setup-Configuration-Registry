# Payroll Definitions Input Validation

This resource validates HDL guidance for PayrollDefinition, ValidPaymentMethod, and generated PayrollTimePeriod adjustments. It also validates the supplied read-only VBCS/Redwood PayrollDVO calendar-field contract. It does not define a REST mutation contract: a VBCS create payload must be evidenced separately, and target-pod View Business Objects exports remain required for an HDL DAT.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation and business object | Prepare or validate an HDL PayrollDefinition MERGE, ValidPaymentMethod MERGE, PayrollTimePeriod MERGE, calendar extension, or VBCS/Redwood Payroll Definition validation | Stop and identify the requested object and operation | Route HDL preparation to the exported HDL contract; route VBCS/Redwood validation to the supplied PayrollDVO fields and read-only resolvers | Always | |
| Target business-object metadata | View Business Objects attribute exports for PayrollDefinition, ValidPaymentMethod, and PayrollTimePeriod as applicable | Block production DAT preparation | Export Attributes from the target pod and reconcile the final header, actions, required flags, types, lengths, keys, and reference syntax | Any production DAT or behavior beyond the documented examples | |
| Payroll identity and effective range | PayrollCode, EffectiveStartDate, and EffectiveEndDate when required by the exported header; SourceSystemOwner and SourceSystemId only when supported | Stop and identify each missing value | Use the exact target header and a stable supported source key or user key | PayrollDefinition create or update | |
| Legislative Data Group | LegislativeDataGroupName or LegislativeDataGroupId(SourceSystemId), exactly as exported | Stop before reference resolution or DAT preparation | Resolve exactly one LDG valid for the load effective date and use only the exported reference form | PayrollDefinition, ValidPaymentMethod, or PayrollTimePeriod work | resolve_legislative_data_group |
| Payroll calendar definition | ReportingName, one of ConsolidationSetName, Name, Consolidation Group, Consolidation Group Name, ConsolidationGroupCode, or ConsolidationSetCode, PeriodTypeCode, FirstPeriodEndDate, NumberOfYears, and one target-supported dynamic-offset or fixed-date field set | Stop only when every Consolidation Group / Set name and code alias is absent, or another calendar-design value is missing | Derive ConsolidationSetCode automatically from the same exact supplied name alias when no code is supplied; continue without prompting for the code. For HDL, confirm the selected calendar pattern in target metadata. For VBCS/Redwood validation, use the supplied PayrollDVO fields and resolvers; do not require an HDL template merely because the fields are absent from its export. | PayrollDefinition create or calendar extension | resolve_consolidation_group_or_set_by_ldg |
| Default payment method | One of Organization Payment Method Name, OrgPaymentMethodName, BaseOrgPayMethodName, OrganizationPaymentMethodCode, DefaultPaymentMethodCode, or DefaultPaymentMethodId(SourceSystemId), exactly as exported where applicable | Stop only when every Organization Payment Method name, code, and ID alias is absent | Derive OrganizationPaymentMethodCode automatically from the same exact supplied OPM name alias when no code is supplied; continue without prompting for the code, then use only the target-export-supported code or ID reference form | PayrollDefinition create or update | resolve_organization_payment_method_by_ldg_and_date |
| Allow Negative Payments | One supplied AllowNegativePaymentsFlag lookup name or value | Stop before PayrollDefinition preparation | Resolve the exact supplied value against Code and Meaning in the HRC_YES_NO lookup | PayrollDefinition create or update when Allow Negative Payments is supplied | resolve_allow_negative_payments_lookup_code |
| Valid payment method relationship | Effective dates, PayrollCode or metadata-supported parent reference, OrganizationPaymentMethodCode or metadata-supported source-key reference, and LDG reference | Stop before preparing the child row | Confirm the target ValidPaymentMethod header and resolve one eligible OPM | ValidPaymentMethod MERGE | resolve_organization_payment_method_by_ldg_and_date |
| Generated time-period identity | PayrollCode, LDG reference, PeriodCategory, StartDate, and the target-supported user-key fields | Stop before preparing the adjustment | Use documented user keys from the target metadata; do not invent source keys for an application-generated period | PayrollTimePeriod MERGE | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An LDG name or source-system reference is supplied | Valid only when exactly one LDG match is effective on the load date | Preserve the resolved value in the reference form required by the exported HDL header | resolve_legislative_data_group |
| A Consolidation Group or Consolidation Set name or code alias is supplied | Derive ConsolidationSetCode from the same exact supplied Name, ConsolidationSetName, Consolidation Group, or Consolidation Group Name when no code is supplied; then validate exactly one instance of the same business object in the selected LDG | Preserve the derived code candidate, ConsolidationSetId, returned code, name, audit values, and LDG relationship; never request the code separately | resolve_consolidation_group_or_set_by_ldg |
| A period-type code is supplied | Valid only when the value is supported for the LDG legislation | Preserve the returned code and use only its supported calendar pattern | resolve_period_type_by_legislation |
| A default OPM name, base name, code, or ID is supplied | Derive OrganizationPaymentMethodCode from the same exact supplied OPM name or base-name alias when no code is supplied; validate exactly one OPM in the LDG that is effective for the load date and is not EFT | Preserve the derived code candidate and use the resolved reference in the exact form required by the exported header; never request the code separately | resolve_organization_payment_method_by_ldg_and_date |
| Allow Negative Payments is supplied | Valid only when exactly one HRC_YES_NO row matches the exact supplied value as Code or Meaning | Preserve the matched actual Code under AllowNegativePaymentsFlag and retain its Meaning as evidence | resolve_allow_negative_payments_lookup_code |
| An additional valid OPM is supplied | Valid only when exactly one eligible OPM is effective for the child range and the range fits within the payroll and OPM ranges | Preserve the reference in the exact form required by the exported ValidPaymentMethod header | resolve_organization_payment_method_by_ldg_and_date |
| Target metadata is absent | Blocked for a production DAT | Export the applicable business-object attributes and reconcile every final header before load | |
| A VBCS/Redwood calendar request is supplied | Valid for field and reference validation when it uses the sourced PayrollDVO attributes: PeriodTypeCode, FirstPeriodEndDate, ConsolidationSetId, DefaultPaymentMethodId, FixedDate, CutoffFixedDate, DateEarnedFixedDate, DatePaidFixedDate, PayrollRunFixedDate, PayslipAvailabilityFixedDate, and PlannedSubmissionFixedDate | Resolve the referenced values and report a missing VBCS create-payload contract separately; do not request an HDL template for these fields | resolve_payroll_definition_lookup_code |
| Ledger, costing, DFF, or EFF data is requested | Unsupported from the supplied HDL evidence | Keep the fields out of the DAT until target metadata confirms their names, actions, and constraints | |
| Delete, end-date, correction, or retroactive time-period behavior is requested | Unsupported from the supplied public evidence | Stop until target metadata confirms the supported action and key contract | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| The DAT header exactly matches the applicable target View Business Objects export | Reject a mixed, archived, or cross-environment header | Any production DAT is prepared | |
| Record action is MERGE for the documented create, update, migration, or future-period adjustment patterns | Reject an undocumented action | Any in-scope HDL row is prepared | |
| SourceSystemOwner and SourceSystemId are used only when the target metadata supports that source-key shape | Reject invented or unsupported source keys | A source-key header is proposed | |
| Reference columns use either the exact exported name, code, ID, or source-key syntax | Reject an unresolved display value or a runtime REST ID placed in an incompatible HDL reference field | Any reference or LOV-style value is supplied | |
| Effective dates use the target-supported HDL representation; supplied examples use YYYY/MM/DD | Reject an invalid or unconfirmed representation | Any effective or calendar date is supplied | |
| EffectiveStartDate is on or before dependent and historical data dates | Reject a payroll definition that starts after referring data | PayrollDefinition create or migration | |
| Existing first effective start date and last effective end date remain unchanged | Reject an attempted boundary change | PayrollDefinition update | |
| Existing Payroll Definition identity | Require LegislativeDataGroupId, PayrollName, and SysEffectiveDate; resolve exactly one effective PayrollId in the same LDG | PayrollDefinition update or calendar extension | resolve_payroll_definition_by_ldg_and_effective_date |
| NumberOfYears is a whole number, is not reduced, and each extension is ten years or fewer | Reject a decrease, non-whole value, or oversized extension | PayrollDefinition create or calendar extension | |
| Dynamic offset fields form one coherent schedule for the selected PeriodTypeCode | Reject mixed or unvalidated falls, day type, offset, and base-date values | Dynamic-offset calendar is used | resolve_period_type_by_legislation |
| Fixed-date fields are used only when the selected period type supports them | Reject fixed dates copied to an unsupported period type; the supplied public example confirms Calendar Month only. The supplied PayrollDVO is field evidence for VBCS/Redwood validation, not an HDL-header substitute. | Fixed-date calendar is used | resolve_period_type_by_legislation |
| Fixed-date values are real Gregorian calendar dates, in addition to matching their stated pattern | Reject syntactically formatted but impossible dates | Any supplied fixed-date field | |
| DateEarnedFixedDate format | You must enter the date for the DateEarnedFixedDate attribute in YYYY/MM/DD format. | DateEarnedFixedDate is supplied | |
| DatePaidFixedDate format | You must enter the date for the DatePaidFixedDate attribute in YYYY/MM/DD format. | DatePaidFixedDate is supplied | |
| PlannedSubmissionFixedDate format | Accept a valid YYYY/MM/DD input for start-of-day defaulting or an exact YYYY/MM/DD HH24:MI:SS value. Reject invalid date or time values. You must enter the date for the PlannedSubmissionFixedDate attribute in YYYY/MM/DD HH24:MI:SS format. | PlannedSubmissionFixedDate is supplied | |
| FirstPeriodEndDate format | You must enter the date for the FirstPeriodEndDate attribute in YYYY/MM/DD format. | FirstPeriodEndDate is supplied | |
| PayrollRunFixedDate format | You must enter the date for the PayrollRunFixedDate attribute in YYYY/MM/DD format. | PayrollRunFixedDate is supplied | |
| PayslipAvailabilityFixedDate format | You must enter the date for the PayslipAvailabilityFixedDate attribute in YYYY/MM/DD format. | PayslipAvailabilityFixedDate is supplied | |
| DateEarned is within the payroll period effective dates | Reject an out-of-period DateEarned | PayrollTimePeriod is generated or adjusted | |
| Payroll names in the generated schedule remain unique within the definition | Reject a duplicate schedule name | PayrollDefinition calendar is generated or extended | |
| Default OPM is not EFT | Reject EFT as the default payroll payment method | PayrollDefinition default payment method is supplied | resolve_organization_payment_method_by_ldg_and_date |
| Each valid OPM effective range fits within both the payroll definition and OPM ranges | Reject an out-of-range relationship | ValidPaymentMethod MERGE | resolve_organization_payment_method_by_ldg_and_date |
| Generated PayrollTimePeriod source keys are absent unless exported metadata explicitly supplies them | Reject invented source keys and require documented user keys | PayrollTimePeriod MERGE | |
| Unknown required flags, types, lengths, code lists, flexfields, or localized attributes remain unresolved | Block production preparation instead of inventing the contract | Target metadata does not confirm an attribute | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PD.VALIDATE_INPUT | decision | 1 | validate_input | valid->PD.RESOLVE_DEPENDENCIES;invalid->PD.HANDLE_ERROR;unsupported->PD.HANDLE_ERROR | none | stop | Always |

## Sources

- Developer-provided PayrollDefinition-HDL.md, accessed 2026-08-13.
- Developer-provided PayrollDVO source, accessed 2026-08-14.
- Oracle Fusion Cloud HCM, HCM Data Loader: https://docs.oracle.com/en/cloud/saas/human-resources/faihm/hcm-data-loader.html
- Oracle Fusion Cloud HCM, Payroll Definitions and Time Periods: Overview: https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/payroll-definitions-and-time-periods-overview.html
- Oracle Fusion Cloud HCM, Examples of Loading Payroll Definitions and Time Periods: https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/examples-of-loading-payroll-definitions-and-time-periods.html

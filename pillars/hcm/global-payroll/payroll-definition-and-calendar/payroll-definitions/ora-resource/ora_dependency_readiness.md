# Payroll Definitions Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Route-specific contract | Export and review the applicable business-object attributes before producing a production DAT; use the supplied PayrollDVO only for VBCS/Redwood field validation. |
| 2 | Legislative Data Group | Establish exactly one LDG that is valid for the load effective date and retain the exact target-supported HDL reference. |
| 3 | Consolidation Group / Consolidation Set | Establish exactly one instance of the same Consolidation Group / Consolidation Set business object in the selected LDG. |
| 4 | Organization Payment Methods | Establish the default non-EFT OPM and every additional valid OPM before the payroll definition or child relationship is loaded. |
| 5 | Calendar design | Confirm the legislation-supported period type, first period end date, years, and one coherent dynamic-offset or supported fixed-date design. |
| 6 | Payroll definition | Load the definition on or before dependent data and preserve its effective-range boundaries on later updates. |
| 7 | Valid payment methods | Load child OPM relationships only after the payroll and OPMs exist and their effective ranges are compatible. |
| 8 | Generated payroll time periods | Adjust only a generated future period identified by documented user keys after the payroll calendar exists. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| target_payroll_definition_metadata | Target PayrollDefinition attribute export | Yes | PayrollDefinition production DAT or an unconfirmed action or attribute is requested | Blocked | Target-pod View Business Objects export | | Headers, required flags, types, lengths, key hints, actions, and reference syntax are environment and release dependent | Export PayrollDefinition Attributes and supply the relevant rows before production preparation | Supported actions, required attributes, data types, lengths, key and reference forms |
| target_vbcs_payroll_definition_create_contract | VBCS/Redwood Payroll Definition create payload contract | Yes | A VBCS/Redwood create, update, or mutation payload is requested | Blocked | Source or HAR showing the exact payrollGeneric create/update endpoint, PayRestName, payload attributes, required fields, and date serialization | | PayrollDVO proves the field names used for validation but does not prove a mutation endpoint or payload shape | Supply the exact VBCS request evidence; do not substitute an HDL template request | Endpoint, method, PayRestName, payload attributes, requiredness, date serialization, and response identity |
| target_valid_payment_method_metadata | Target ValidPaymentMethod attribute export | Yes | ValidPaymentMethod production DAT is requested | Blocked | Target-pod View Business Objects export | | The supplied rows do not establish the universal parent-key and OPM-reference form | Export ValidPaymentMethod Attributes and reconcile the intended header | Supported actions, effective-date fields, parent reference, OPM reference, requiredness |
| target_payroll_time_period_metadata | Target PayrollTimePeriod attribute export | Yes | PayrollTimePeriod production DAT or adjustment is requested | Blocked | Target-pod View Business Objects export | | Generated periods require documented user keys and target-supported adjustable attributes | Export PayrollTimePeriod Attributes and reconcile the intended header | Supported actions, user keys, adjustable fields, requiredness |
| legislative_data_group | Effective Legislative Data Group | Yes | Any in-scope object is prepared or validated | Lookup | Supplied LDG name or metadata-supported source-system reference and load date | resolve_legislative_data_group | Every referenced dependency and localized value is LDG-scoped | Provide an exact LDG reference and load effective date | LegislativeDataGroupName or LegislativeDataGroupId(SourceSystemId), LegislationCode |
| consolidation_group_or_set | Consolidation Group / Consolidation Set in the LDG | Yes | PayrollDefinition is prepared | Lookup | Resolved LDG and one supplied ConsolidationSetName, Name, Consolidation Group, Consolidation Group Name, ConsolidationGroupCode, or ConsolidationSetCode; derive ConsolidationSetCode from the same exact name alias when code is absent | resolve_consolidation_group_or_set_by_ldg | Consolidation Group and Consolidation Set are the same business object for payroll processing | Provide one group or set name or code alias for the selected LDG; never request ConsolidationSetCode separately | ConsolidationSetId, ConsolidationSetName, ConsolidationSetCode |
| payroll_definition_lookup_values | Payroll Definition lookup codes | Conditional | A mapped CutoffBaseDate, CutoffDayType, FixedDate, DatePaidOffset, or PeriodTypeCode is supplied as a lookup name or value | Lookup | Supplied LookupType and exact lookup name or value | resolve_payroll_definition_lookup_code | The supported lookup mappings are PAY_BASE_DATE to CutoffBaseDate, PAY_BASE_OFFSET to CutoffDayType, HRC_YES_NO to FixedDate and AllowNegativePaymentsFlag, PAY_DATE_OFFSET to DatePaidOffset, and PAY_PROC_PERIOD_TYPE to PeriodTypeCode | Supply the exact mapped LookupType and lookup name or value | Matched actual Code and Meaning |
| allow_negative_payments | Allow Negative Payments lookup value | Conditional | AllowNegativePaymentsFlag is supplied for PayrollDefinition | Lookup | Exact supplied lookup name or value | resolve_allow_negative_payments_lookup_code | HRC_YES_NO resolves the actual Code required by AllowNegativePaymentsFlag | Supply the exact Code or Meaning without normalization | AllowNegativePaymentsFlag and matched Meaning |
| period_type | Legislation-supported period type | Yes | PayrollDefinition is prepared or calendar design changes | Lookup | Supplied PeriodTypeCode and resolved legislation code | resolve_period_type_by_legislation | Period types and fixed-date support vary by legislation and release | Provide the intended pay frequency or exact period-type code | PeriodTypeCode and supported calendar pattern |
| default_payment_method | Effective non-EFT default OPM | Yes | PayrollDefinition is prepared | Lookup | Resolved LDG, EffectiveDate, and one OPM name, base name, ID, or code; derive OrganizationPaymentMethodCode from the same exact supplied name or base-name alias when code is absent | resolve_organization_payment_method_by_ldg_and_date | The OPM must exist before the definition and EFT is not a valid default design | Provide an eligible non-EFT OPM name, base name, ID, or code and effective date; never request OrganizationPaymentMethodCode separately | OrgPaymentMethodId, OrganizationPaymentMethodCode candidate, payment type, category, effective range |
| valid_payment_method | Effective eligible OPM relationship | Conditional | ValidPaymentMethod is prepared | Lookup | Resolved LDG, EffectiveDate, and one OPM name, base name, ID, or code; derive OrganizationPaymentMethodCode from the same exact supplied name or base-name alias when code is absent | resolve_organization_payment_method_by_ldg_and_date | The child range must fit within both the payroll and OPM ranges | Provide the OPM name, base name, ID, or code and intended child effective range; never request OrganizationPaymentMethodCode separately | OrgPaymentMethodId, OrganizationPaymentMethodCode candidate, OPM effective range |
| existing_payroll_definition | Existing definition identity and immutable effective boundaries | Conditional | PayrollDefinition is updated or its calendar is extended | Lookup | LegislativeDataGroupId, PayrollName, and SysEffectiveDate | resolve_payroll_definition_by_ldg_and_effective_date | The first start date, last end date, supported update key, and PayrollId must be resolved in the requested LDG and effective date | Supply exact payroll name, LDG ID, and effective date | PayrollId, first effective start date, last effective end date, current NumberOfYears |
| generated_payroll_time_period | Existing generated period identified by user keys | Conditional | A future PayrollTimePeriod is adjusted | Blocked | Target export and generated calendar evidence | | Application-generated source keys must not be invented | Supply the target-confirmed user key values for the generated period | PayrollCode, LDG reference, PeriodCategory, StartDate, supported adjustable dates |
| authorized_hdl_handoff | Authorized HCM Data Loader workflow | Conditional | A live upload, import, or load is requested | Blocked | Approved target environment, Data Exchange access, exact preview, and explicit approval | | These authoring resources validate guidance but do not authorize or perform a Fusion mutation | Hand the validated DAT contract to an authorized HDL workflow only after preview and approval | Environment, approved archive identity, operation, business effect, approval evidence |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Supplied target evidence establishes the dependency and applicable effective dates | Continue without creating related setup. |
| Lookup | One named read-only resolver must establish the reference | Run only the documented lookup; never create a dependency from this task. |
| Blocked | Target metadata, exact identity, effective-range evidence, authorization, preview, or approval is missing | No; resolve the blocker first. |
| Unsupported | Supplied evidence does not establish the requested action, field, or localization contract | No; stop without inventing behavior. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PD.RESOLVE_DEPENDENCIES | decision | 2 | resolve_dependency | ready->PD.RESOLVE_REFERENCES;blocked->PD.HANDLE_ERROR;unsupported->PD.HANDLE_ERROR | PD.VALIDATE_INPUT | stop | Validated Payroll Definitions request |

## Sources

- Developer-provided PayrollDefinition-HDL.md, accessed 2026-08-13.
- Developer-provided PayrollDVO source, accessed 2026-08-14.
- Oracle Fusion Cloud HCM, Payroll Definitions: https://docs.oracle.com/en/cloud/saas/human-resources/25b/faipk/payroll-definitions.html
- Oracle Fusion Cloud HCM, Examples of Loading Payroll Definitions and Time Periods: https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/examples-of-loading-payroll-definitions-and-time-periods.html

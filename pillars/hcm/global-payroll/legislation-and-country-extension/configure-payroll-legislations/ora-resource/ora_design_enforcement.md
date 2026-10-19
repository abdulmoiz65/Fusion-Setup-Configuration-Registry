# Configure Payroll Legislations Design Enforcement

## Evidence Matrix

| Claim or Contract | Source | Source Type | Evidence Status | Release or Date | Limitation |
|---|---|---|---|---|---|
| Task-level FSM contract | Configure Payroll Legislations FSM template package and metadata | Target-environment FSM template | Observed | Fusion release 11.13.26.10.0; exported 2026-08-12 | Does not prove which business records or values are valid. |
| FSM-only configuration route | User implementation direction | Authoring policy | Confirmed | 2026-08-13 | REST is not an execution route for this task. |
| Immutable import approval | User implementation direction and core.data-loader | Implementation policy | Confirmed | 2026-08-13 | Applies immediately before the first import-side effect. |

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Use the selected task | Keep ObjectShortName PAY_CONFIGURE_PAYROLL_LEGISLATION and do not substitute a different task package. |
| 2 | Preserve the FSM contract | Use only the observed metadata XML, filenames, headers, data types, and metadata-defined ordering. |
| 3 | Preserve source values | Do not infer, clone, transform, filter, rename, or replace configuration values; use only the user-supplied source and documented defaults when their explicit Add condition applies. |
| 4 | Use FSM only | Do not use REST calls, REST fields, or REST mutations. |
| 5 | Apply the import gate | Use core.data-loader to validate a final immutable ZIP, show its SHA-256, and wait for the standalone approval before upload or initiation. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A package targets this setup task | Error | | ObjectShortName, metadata, or files identify another task | Rebuild from the Configure Payroll Legislations FSM template | Yes |
| A CSV is included | Error | | Filename, header order, column set, or declared type differs from the template | Correct the package without inventing fields | Yes |
| A populated value is prepared | Error | | No explicit functional source supports the value, other than the documented defaults | Obtain the user-supplied functional decision or source archive before packaging | Yes |
| HCM-product defaults are applied | Error | | Add is not explicit, LegislationCode is missing, user-supplied HCM-product rows exist, or a defaulted row changes a value other than LegislationCode | Preserve user rows or apply exactly the confirmed one-row baseline with a user-supplied LegislationCode | Yes |
| Relationship-type mapping defaults are applied | Error | | Add is not explicit, LegislationCode is missing, user-supplied mapping rows exist, any of the nine mapping values is altered, or ViewInstanceName/GroupingKey do not match the documented defaults | Preserve user rows or apply exactly the confirmed default mapping set | Yes |
| Payroll-relationship-rule defaults are applied | Error | | Add is not explicit, LegislationCode is missing, user-supplied payroll-relationship-rule rows exist, or a defaulted RuleMode or RuleType value differs from the confirmed eight-row baseline | Preserve user rows or apply exactly the confirmed eight-row baseline with a user-supplied LegislationCode | Yes |
| Balance-dimension defaults are applied | Error | | Add is not explicit, LegislationCode is missing, user-supplied balance-dimension rows exist, the baseline differs from the documented 365-row SHA-256, or a defaulted row changes a value other than LegislationCode or the final GroupingKey component | Preserve user rows or apply exactly the confirmed baseline with LegislationCode-derived keys | Yes |
| Balance-type defaults are applied | Error | | Add is not explicit, LegislationCode or CurrencyCode is missing, user-supplied balance-type rows exist, a defaulted row changes a value other than LegislationCode, its GroupingKey legislation component, or a marked CurrencyCode cell, or one of the four confirmed blank CurrencyCode cells is populated | Preserve user rows or apply exactly the confirmed 28-row baseline with the documented input substitutions | Yes |
| Component-group defaults are applied | Error | | Add is not explicit, LegislationCode is missing, user-supplied component-group rows exist, or a defaulted row changes a value other than LegislationCode or its GroupingKey legislation component | Preserve user rows or apply exactly the confirmed six-row baseline with LegislationCode-derived keys | Yes |
| Element-classification defaults are applied | Error | | Add is not explicit, LegislationCode is missing, user-supplied element-classification rows exist, or a defaulted row changes a value other than LegislationCode or the final GroupingKey component | Preserve user rows or apply exactly the confirmed 119-row baseline with LegislationCode-derived keys | Yes |
| Payment-type defaults are applied | Error | | Add is not explicit, LegislationCode is missing, user-supplied payment-type rows exist, or a defaulted row changes a value other than LegislationCode or its GroupingKey legislation component | Preserve user rows or apply exactly the confirmed four-row baseline with LegislationCode-derived keys | Yes |
| A package is prepared | Error | | An attempt is made to derive a business operation or to transform supplied rows | Preserve the supplied FSM content; request explicit functional direction for any change | Yes |
| A REST route or lookup is proposed | Error | | Any REST request is selected for this task | Use FSM only | No |
| An import is requested | Error | | The archive is not final and immutable, has not passed core.data-loader and Task Hook checks, its SHA-256 has not been shown, or current approval is absent | Complete the required validation and wait for exactly approve | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CPL.ENFORCE_FSM_CONTRACT | step | 4 | design_enforcement | compliant->CPL.COMPLETE;blocked->RETURN_ISSUES | CPL.APPLY_DEFAULTS | stop | Always |

# Manage Secondary Ledgers Input Validation

This task creates an in-process secondary accounting representation beneath one exact primary ledger. It establishes structural identity and the disabled relationship shell; ledger options and completed primary-to-secondary mapping remain later lifecycle steps.

## Intake Policy

| Input Class | Policy |
|---|---|
| Definitely mandatory user input | Source primary ledger, secondary ledger name, chart of accounts, accounting calendar, currency, and data conversion level are collected explicitly. No resolver or default may replace the business choice. |
| Optional desired-state input | AccountingMethodName is never required for FSCR creation. Every new secondary is authored with Standard Accrual; another explicitly requested method is retained only for a post-create manual-change handoff. |
| Optional user input | Description is optional. Do not collect ledger-option families in this task. |
| Resolver-derived | IDs, codes, period set, accounted period type, and chart structure metadata come only from exact authoritative matches. Physical FirstLedgerPeriodName must be explicit or independently authoritative and is then validated against the complete period LOV result. |
| Downstream First Opened Period | A period supplied for secondary Specify Ledger Options remains handoff-only in this task. Never copy, substitute, or leak it into the Manage Secondary Ledgers physical FirstLedgerPeriodName field. |
| Export-derived or inherited | Source-primary aliases and the three documented inherited policy flags come from the validated scoped export. |
| Controlled role default | A current-release default is usable only for the same new-secondary role and package shape. |
| Intentional blank | A documented blank remains blank; it is not converted to N, zero, or a copied primary value. |
| Service owned | Generated identifiers, short name, audit values, process values, and manifest identity are never user intake. |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Source primary ledger | SourcePrimaryLedgerName or SourcePrimaryLedgerId | Block preview and request the primary ledger | Resolve exactly one ledger whose category is PRIMARY in the selected accounting configuration | Always | resolve_source_primary_ledger |
| Secondary ledger name | SecondaryLedgerName | Block preview and request a name | User supplies the business name; availability is checked separately | Always | check_ledger_name_availability |
| Chart of accounts | ChartOfAccountsName or source-ledger ChartOfAccountsId as StructureInstanceNumber | Block preview and request the accounting chart of accounts | Resolve exactly one enabled chart by returned Name or StructureInstanceNumber; never substitute StructureInstanceId | Always | resolve_enabled_chart_of_accounts |
| Accounting calendar | AccountingCalendarName | Block preview and request an accounting calendar | Resolve exactly one UserPeriodSetName whose CalendarTypeCode is ACCOUNTING; this LOV has no enabled flag | Always | resolve_accounting_calendar |
| Physical ledger period | FirstLedgerPeriodName for the secondary create shell, distinct from the later secondary-options opening-period handoff | Block preview unless exact independently authoritative same-role export evidence already supplies it | Validate the value against one EnteredPeriodName in the fully paged PeriodSetNameId result after local PeriodType filtering; never select from response order | Always | resolve_secondary_first_ledger_period |
| Currency | CurrencyCode or CurrencyName | Block preview and request an active monetary currency | Resolve exactly one enabled currency whose CurrencyFlag is Y | Always | resolve_monetary_currency |
| Data conversion level | DataConversionLevel | Block preview and request one supported level | Accept the closed local enumeration only | Always |  |
| Accounting Method policy | Optional AccountingMethodName desired-state receipt; physical method fields are not user intake | Never block creation because the method was omitted | Author Standard Accrual as STANDARD_ACCRUAL, S, and blank language for every new secondary. If another method is named, retain it for a post-create secondary Specify Ledger Options UI handoff | Always | resolve_accounting_method_evidence |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Source primary identifier is present | Exactly one PRIMARY ledger and its exact export aliases must agree | Continue with inherited-value and compatibility checks | read_source_primary_export |
| SecondaryLedgerName is present | Zero exact matches across ledger and reporting-currency relationship names is required | Continue only when the broader namespace is clear | check_ledger_name_availability |
| A chart of accounts is selected | A current populated COA task export for the exact selected structure instance must identify the GL key flexfield, exactly one balancing role, at most one management role, segment columns, and value sets | Populate only the exact documented export-join metadata; never use REST describe metadata, a closing-segment-only LOV, or an assumed SEGMENT1 position | resolve_coa_structure_roles |
| An accounting calendar is selected | The full exact eligible period set plus an explicit physical FirstLedgerPeriodName or independently authoritative same-role export value must resolve | Validate the value against EnteredPeriodName and PeriodType. Never select the first response row or sort labels; the later secondary-options task still requires user confirmation of its first opened period | resolve_secondary_first_ledger_period |
| DataConversionLevel is Adjustment Only or ADJUST | Secondary COA, calendar, period set, accounted period type, and currency must equal the source primary values | Block and show every mismatch | read_source_primary_export |
| Secondary COA differs from primary | Current task can create the in-process shell but later mapping readiness is required | Record a blocking dependency for Complete Primary to Secondary Ledger Mapping before review | read_source_primary_export |
| Secondary currency differs from primary | Current task can create the in-process shell but a later exact conversion-rate policy is required | Record a blocking mapping dependency; do not choose Corporate or any rate type | read_source_primary_export |
| Secondary calendar differs from primary | Operational compatibility must be reviewed; no separate calendar-mapping field is proven | Block unsupported assumptions and require a reviewed design | read_source_primary_export |
| A source package is proposed | Exact scope, release, environment, members, aliases, headers, and manifest must validate | Use the package only after all checks pass | inspect_task_package |
| AccountingMethodName is omitted or names Standard Accrual | Continue without asking for method details | Populate STANDARD_ACCRUAL, S, and blank SlaDescriptionLanguage in both secondary aliases | resolve_accounting_method_evidence |
| AccountingMethodName explicitly names another method | Continue structural creation using the controlled Standard Accrual tuple | Retain the exact desired display name, create a manual secondary-options handoff, and require same-scope re-export before Review and Submit | resolve_accounting_method_evidence |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Free-text normalization | Retain the raw decoded text exactly, including leading and trailing whitespace, internal whitespace, case, punctuation, and Unicode. Use an all-Unicode-whitespace check only to classify missing input; do not silently trim, collapse, or case-fold the value sent to Oracle | SecondaryLedgerName or Description is supplied |  |
| Secondary name length | Reject a raw name longer than 30 Oracle characters and identify SecondaryLedgerName | Always |  |
| Secondary name uniqueness | Require zero exact raw-name matches in the broader ledger and reporting-currency relationship namespace; never treat an authorization or client failure as availability | Always | check_ledger_name_availability |
| Description length and blank handling | Reject more than 240 Oracle characters; an omitted or whitespace-only description becomes an intentional blank | Description is supplied |  |
| Closed conversion enumeration | Map Balance to BALANCE, Journal to JOURNAL, Subledger to SUBLEDGER, and Adjustment Only to ADJUST; reject every other label or code without a REST lookup | Always |  |
| Accounting Method physical fields | Reject user-supplied code, type, or language as unsupported direct intake; the controlled create tuple is FSCR-owned | Any physical method field is supplied by the user | resolve_accounting_method_evidence |
| Standard Accrual controlled tuple | Require code STANDARD_ACCRUAL, type S, and blank language on every new FSCR-created secondary, regardless of conversion level or omitted method input | Always | resolve_accounting_method_evidence |
| Alternative method boundary | Preserve another exact AccountingMethodName only as desired-state evidence; do not lookup or directly author its tuple under open boundary GL-01 | A non-Standard-Accrual method is requested | resolve_accounting_method_evidence |
| Adjustment Only compatibility | Reject any COA, calendar, period set, accounted period type, or currency difference from the source primary | DataConversionLevel is Adjustment Only or ADJUST | read_source_primary_export |
| Unknown fields | Reject undocumented fields, aliases, or guessed identifiers and name the unsupported input | User supplies a field outside this contract |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MSL-010-VALIDATE-INPUT | decision | 10 | validate_input | valid->MSL-020-RESOLVE-REFERENCES;invalid->MSL-070-HANDLE-ERROR | none | stop | Always |

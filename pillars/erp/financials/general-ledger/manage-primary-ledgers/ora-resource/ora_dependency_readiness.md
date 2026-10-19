# Manage Primary Ledgers Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Environment and request identity | Bind one target environment, Fusion release, project, exact ledger create request, and one immutable task-local run identity before any live lookup or export |
| 2 | Ledger namespace | Run the complete exact ledgersLOV lookup first. Zero exact matches permits reference resolution; any exact match blocks the request as a duplicate before an export job or package is prepared |
| 3 | Chart of accounts identity | Resolve exactly one enabled chart of accounts by Name and retain returned Name as ChartOfAccountsName plus StructureInstanceId, StructureInstanceNumber, and StructureInstanceCode |
| 4 | Accounting calendar and periods | Resolve exactly one ACCOUNTING calendar by UserPeriodSetName, map returned PeriodType to AccountedPeriodType, retrieve the complete eligible-period set, and validate an explicit physical first-period choice or independently authoritative same-role export value |
| 5 | Currency | Resolve exactly one enabled, currently active monetary currency by exact CurrencyCode |
| 6 | Chart-of-accounts semantic roles | Search the project export inventory for a current same-environment and same-release populated GL_MANAGE_CHARTS_OF_ACCOUNTS_STRUCTURE_INSTANCES export containing the exact resolved StructureInstanceCode. Reuse it when valid; otherwise present the exact export operation and obtain explicit approval immediately before routing exactly one new populated task export. Resolve exactly one balancing segment and zero or one management segment through the documented four-member joins |
| 7 | Accounting method | Apply the controlled Standard Accrual tuple for every new FSCR-created primary ledger. If another method was explicitly requested, retain it only as a post-create manual-change handoff and do not alter the create tuple |
| 8 | Manage Primary Ledgers template | Only after sequences 1 through 7 pass, present the exact environment, GL_MANAGE_PRIMARY_LEDGERS, template-only mode, and purpose; obtain explicit approval immediately before routing exactly one export for the current authoring attempt. Validate the resulting header-only ten-CSV package and ASM_SETUP_CSV_METADATA.xml before editing |
| 9 | Smallest-delta and alias readiness | Add only the two root rows and one logical PRIMARY row in both 133-column aliases, preserve all other members and metadata, and prove alias parity and true-empty serialization before preview |
| 10 | Preview, approval, import, and verification | Present an immutable semantic preview, obtain explicit approval for its exact environment and fingerprint, route one import through core.data-loader, monitor it, and verify by identical-scope populated re-export before declaring this task complete |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| mpl_name | Available primary-ledger name | Yes | Always | Verify | Fully paginated authoritative ledger LOV | find_primary_ledger_name_conflict | A duplicate must stop the task before either export role creates a process | Provide a different exact name when any exact match exists | NameAvailability |
| mpl_coa | Chart of accounts identity | Yes | Always | Lookup | Fusion chart-of-accounts LOV for exact enabled identity only | resolve_chart_of_accounts_exact | The role export must be matched to one exact selected structure instance | Correct an invalid or ambiguous chart-of-accounts identity before export acquisition | ChartOfAccountsName, StructureInstanceId, StructureInstanceNumber, StructureInstanceCode |
| mpl_calendar | Accounting calendar | Yes | Always | Lookup | Fusion accounting-calendar LOV | resolve_accounting_calendar_exact | The ledger requires an ACCOUNTING calendar and its returned period set and period type; the LOV has no enabled flag | Select one exact accounting calendar | AccountingCalendarName, UserPeriodSetName, CalendarId, PeriodSetName, AccountedPeriodType |
| mpl_periods | Eligible accounting periods and physical first period | Yes | Always | Lookup | Fusion accounting-period LOV queried by PeriodSetNameId and filtered locally by PeriodType | list_eligible_accounting_periods | The create row requires physical period identity while the later opening decision remains user owned | Supply exact physical FirstLedgerPeriodName or independently authoritative same-role export evidence, then validate it against EnteredPeriodName; never use response order | FirstLedgerPeriodName, EligibleAccountingPeriods |
| mpl_currency | Ledger currency | Yes | Always | Lookup | Fusion currency LOV | resolve_monetary_currency_exact | The ledger requires one exact active monetary currency | Select one exact active monetary currency | CurrencyCode |
| mpl_coa_roles | Chart-of-accounts role derivation | Yes | After mpl_coa resolves | Verify | Reusable current populated GL_MANAGE_CHARTS_OF_ACCOUNTS_STRUCTURE_INSTANCES export or one new routed populated export when no candidate qualifies | derive_chart_of_accounts_roles | GL_BALANCING and optional GL_MANAGEMENT columns and instance value sets are owned by the selected CoA export and cannot be inferred from REST describe metadata, segment names, sequence, or DefaultValueSetCode | Supply the exact CoA; FSCR either reuses one qualifying export or submits one named task export and reports exact member or composite-key defects | StructureInstanceCode, StructureCode, KeyFlexfieldCode, ApplicationId, BalSegColumnName, BalSegValueSetCode, optional MgtSegColumnName and MgtSegValueSetCode, role evidence, export receipt |
| mpl_method | Controlled accounting method | Yes | Always for a new FSCR-created primary ledger | Verify | Developer-approved Standard Accrual authoring policy plus optional exact alternative AccountingMethodName desired-state receipt | resolve_accounting_method_evidence | FSCR creation has one deterministic supported method tuple and does not directly author arbitrary methods | Do not provide technical method fields. When a different method is desired, state its exact display name for the post-create Specify Ledger Options UI handoff | CSV: SlaAccountingMethodCode, SlaAccountingMethodType, SlaDescriptionLanguage. Non-CSV: EffectiveAccountingMethodName, optional RequestedAccountingMethodName, MethodChangeUIHandoffRequired |
| mpl_package | Current template-only Manage Primary Ledgers carrier | Yes | After mpl_name, mpl_coa, mpl_calendar, mpl_periods, mpl_currency, mpl_coa_roles, and mpl_method are satisfied | Verify | Exactly one current-attempt routed template-only GL_MANAGE_PRIMARY_LEDGERS export result | select_validated_general_ledger_package | The exact header-only task template is the only supported carrier for new ledger rows | Do not supply a populated ledger package or another task's template; reconcile an already accepted current-attempt export before requesting another | Package path, export receipt, member inventory, header and alias fingerprints, metadata identity, zero data-row proof |
| mpl_aliases | Symmetric primary aliases | Yes | Before preview and after re-export | Verify | The two 133-column primary alias members in the validated package | verify_primary_alias_parity | Both aliases represent one logical PRIMARY row and must not diverge | Correct the smallest delta until both aliases have one semantically identical scoped row | Alias row counts, semantic diff, alias-only preservation result |

## Downstream Ledger-Options Handoff

| Supplied With Ledger Request | Manage Primary Ledgers Treatment | Handoff Condition |
|---|---|---|
| Retained earnings account or another primary-ledger option | Preserve the exact user statement as a non-CSV dependent-task receipt. Do not resolve, validate, create, or serialize the account in this task, and keep RetEarnCcidSegments blank in the primary-shell package | Release the receipt to the primary-ledger Specify Ledger Options workflow only after the Manage Primary Ledgers import reaches terminal success and identical-scope re-export verifies the new ledger shell |
| First Opened Period | Preserve only as a dependent-task receipt. Never substitute it for the resolver-derived physical FirstLedgerPeriodName | Release only after verified primary-shell creation |
| Non-Standard accounting method | Create the primary shell with Standard Accrual and preserve the exact requested display name as the documented manual options-task handoff | Require the later manual change and same-scope re-export before Review and Submit readiness |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact required value and current evidence already exist | Continue without creating dependency setup |
| Lookup | A documented read-only resolver can obtain the authoritative value | Yes, read-only lookup only |
| Verify | A local package or export must be validated or compared | Yes, local verification only |
| Routed export | A required task package is absent after prerequisites pass | Yes, only after presenting the exact environment, task, mode, and purpose and obtaining explicit export-operation approval immediately before shared.setup-export.task-level-export; never through an ad hoc call |
| Blocked | Required identity, package, evidence, privilege, or unambiguous match is missing | No; request correction or the exact routed acquisition gate |
| UI handoff | Supported baseline can continue but an optional configuration must be completed in the named Oracle UI task | No direct CSV customization; re-export after UI completion |
| Not required | Conditional dependency does not apply to the selected outcome | Continue while preserving the intentional blank or existing value |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPL.CHECK_DEPENDENCIES | decision | 30 | resolve_dependency | ready->MPL.APPLY_DEFAULTS;blocked->MPL.HANDLE_ERROR | MPL.RESOLVE_REFERENCES | stop | After exact live references and conditional CoA role evidence resolve, require the current template-only carrier and every other dependency before deriving a proposed package delta. |

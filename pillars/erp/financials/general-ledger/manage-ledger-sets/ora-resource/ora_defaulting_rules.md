# Manage Ledger Sets Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Classification | None (blank) | Create and classification omitted | No |  |
| Description | Blank | Create and description omitted | No |  |
| Default Ledger | Blank | Create and no default requested | No |  |
| Optional DFF values | Blank only if current deployed metadata permits | Create and optional segment omitted | No | inspect_ledger_set_evidence |
| Any existing field | Preserve current value | Update and field omitted | No | inspect_ledger_set_evidence |
| Assignments | Preserve current members; require explicit additions/removals | Update and membership delta omitted | No | inspect_ledger_set_evidence |
| ObjectTypeCode | S | Create a ledger set and current task metadata confirms the field | No | inspect_ledger_set_package |
| ShortName | Proposed Name, without truncation | Create, unset ShortName, Name is at most 20 characters, the independent short-name precheck finds no conflict | No; a supplied valid short name takes precedence | find_ledger_set_by_exact_short_name |
| AccessSetName | New set Name | Create under MLS_FSM_CREATE_V1 | No; never copy the source set identity | resolve_ledger_set_create_profile |
| Technical header fields | Packaged MLS_FSM_CREATE_V1 initialization values | Create and the current template supports the packaged field/type contract | No; alternate technical behavior needs its own supported profile | resolve_ledger_set_create_profile |
| LedgerCategoryCode, AlcLedgerTypeCode | NONE | Create under the compatible packaged field/type contract | No; technical fields are not ordinary business options | resolve_ledger_set_create_profile |
| LeLedgerTypeCode | U | Create under the compatible packaged field/type contract | No | resolve_ledger_set_create_profile |
| CurrencyCode, FirstLedgerPeriodName | X | Create under the compatible packaged field/type contract | No; classified currency is handled separately | resolve_ledger_set_create_profile |
| SuspenseAllowedFlag, AllowIntercompanyPostFlag, TrackRoundingImbalanceFlag, EnableAverageBalancesFlag, EnableBudgetaryControlFlag, RequireBudgetJournalsFlag, EnableJeApprovalFlag, EnableAutomaticTaxFlag, ConsolidationLedgerFlag, TranslateEodFlag, TranslateQatdFlag, TranslateYatdFlag, AutomaticallyCreatedFlag, EnableReconciliationFlag, CreateJeFlag | N | Create under the compatible packaged field/type contract | No; do not inherit a member ledger's accounting settings | resolve_ledger_set_create_profile |
| LedgerAttributes | S | Create under the compatible packaged field/type contract | No | resolve_ledger_set_create_profile |
| BalSegValueOptionCode, MgtSegValueOptionCode | I | Create under the compatible packaged field/type contract | No | resolve_ledger_set_create_profile |
| FutureEnterablePeriodsLimit | 0 | Create under the compatible packaged field/type contract | No | resolve_ledger_set_create_profile |
| KeyFlexfieldCode, ApplicationShortName | GL#, GL | Create and current task metadata agrees with GL flexfield/application identity | No | resolve_ledger_set_create_profile |
| StructureInstanceCode | Exact selected COA instance code returned by the declared chart lookup | Create and selected COA agrees with every effective member | No; resolve a changed selection again | resolve_ledger_set_chart_of_accounts |
| PeriodSetName, UserPeriodSetName | Exact internal and display names returned by the declared calendar lookup | Create and calendar/period tuple agrees with every effective member | No; resolve a changed selection again | resolve_ledger_set_accounting_calendar |
| BalSegColumnName | Structural column returned for the selected COA through the declared member lookup | Candidate requires this field and member evidence agrees | No; do not assume SEGMENT1 | resolve_ledger_set_balancing_segment_column |
| Other segment metadata | Allowlisted shared structural values from the fresh primary-ledger-scoped export; management and descriptor fields follow their explicit policies | Candidate requires fields not exposed by the declared LOVs | No; a COA export is conditional on a named required gap | resolve_ledger_set_structural_profile |
| Audit fields | Empty cells under the packaged omission rule | Create; do not copy source who-column values | No | resolve_ledger_set_create_profile |
| Inapplicable technical columns and unused assignment fields | Empty cells for the explicitly named base-profile fields | Create, current field/types agree, and no requested or known required field needs a value | No; supported omission is not proof of an individual Oracle default | resolve_ledger_set_create_profile |

## Packaged Explicit Create Contract

MLS_FSM_CREATE_V1 is the built-in FSCR authoring profile. The Standard Defaults table supplies its 27 explicit initialization fields. It is available to every new project without a previous run, exported ledger-set row, tenant-specific profile receipt or controlled-test exception. Resolve tenant-dependent COA/calendar/member fields afresh; do not inherit ledger accounting options.

This contract defines what FSCR prepares. It does not claim Oracle automatically defaults empty CSV cells or that every target release has been tested. Compare actual field names and XML types with the current template. A new project/environment/COA is not itself a mismatch; changed field/type contracts, known required-field differences and unsupported requested operations are concrete blockers.

Acceptance of the packaged initialization, scoped structural values and named omissions together supports that combined preparation pattern. It does not prove that each populated field is necessary or that each blank has an independent Oracle default. Keep the explicit initialization contract intact unless authoritative metadata or a separately qualified contract supports a change; do not reduce it merely because an import succeeded.

## Header Omission Rules

| Field Group | Fields | Create Handling |
|---|---|---|
| Audit | CreatedBy, CreationDate, LastUpdatedBy, LastUpdateDate, LastUpdateLogin | Empty; never copy source audit values. |
| Display descriptors | BalSegDescription, MgtSegDescription | Empty in the base authoring profile. No description input or historical structure profile is required. Do not map these from a segment Name, Description or value-set code without an established field mapping. A current contract or server error requiring one creates a specific mapping issue, not a reason to guess. |
| Ledger-only status and translation | CompletionStatusCode, LatestOpenedPeriodName, LatestEncumbranceYear, DailyTranslationRateType, PeriodAverageRateType, PeriodEndRateType, BudgetPeriodAvgRateType, BudgetPeriodEndRateType, TransactionCalendarName | Empty for a set; member-ledger options are not inherited. |
| Subledger and tracking | SlaAccountingMethodCode, SlaAccountingMethodType, SlaDescriptionLanguage, SlaSequencingFlag, SlaBalByLedgerCurrFlag, EnableSecondaryTrackFlag, EnableRevalSsTrackFlag, SlaLedgerCashBasisFlag | Empty for a set. |
| Other ledger configuration | CompleteFlag, UssglOptionCode, ValidateJournalRefDate, JrnlsGroupByDateFlag, RevalFromPriLgrCurr, AutorevAfterOpenPrdFlag, PriorPrdNotificationFlag, PopUpStatAccountFlag, ThresholdAmount, NumberOfProcessors, ProcessingUnitSize, ReleaseUpgradeFrom, CriteriaSetName, LedgerName, LedgerConfigName | Empty for a set. |
| Ledger account combinations | CumTransCcidSegments, ResEncumCcidSegments, NetIncomeCcidSegments, RoundingCcidSegments, SlaEntCurBalSusSegments, SlaLedgerCurBalSusSegments, IntercoGainLossSegments, RetEarnCcidSegments, CrossLgrClrAccSegments | Empty; do not copy any member's account combinations. |
| Header DFF | AttributeCategory, Attribute1 through Attribute15, AttributeNumber1 through AttributeNumber5, AttributeDate1 through AttributeDate5 | Empty when omitted and current deployment has no required segment; populate only requested/required deployed mappings. |

## Structure and Assignment Rules

| Field Group | Fields | Create Handling |
|---|---|---|
| Chart and calendar | StructureInstanceCode, PeriodSetName, UserPeriodSetName | Resolve exact codes/display keys through the declared live lookups; period type is compatibility evidence. |
| Balancing role | BalSegColumnName, BalSegValueSetCode | Extract the nonblank pair from the exact PRIMARY row in the fresh ledger-scoped export and cross-check the member lookup; no fixed column or value set. Conditional COA role joins resolve a named required gap. |
| Management role | MgtSegColumnName, MgtSegValueSetCode | Populate only a coherent pair with current selected-chart role evidence. Otherwise empty under the base authoring profile; a primary's default column alone is not proof of a management role. Blank cells do not establish role absence. Conditional COA joins are needed only if current contract/request requires unresolved role values. |
| Assignment identity | GL_LEDGER_SET_DEF.Name, LedgerName, ObjectTypeCode | Supply the new parent Name and every requested direct member's exact resolved Name and L/S type. |
| Assignment audit | CreatedBy, CreationDate, LastUpdatedBy, LastUpdateDate, LastUpdateLogin | Empty. |
| Assignment dates/status | StartDate, EndDate, StatusCode | Empty for ordinary new membership; a requested date/status needs its own supported operation contract. |
| Assignment DFF | AttributeCategory, Attribute1 through Attribute15 | Empty unless requested or required by current deployment. |

All current columns must belong to a documented business, identity, initialization, reference, role, audit, DFF or omission group. Reject an unclassified new column or incompatible type with its exact name rather than asking for a separate qualified profile. Name-based ShortName derivation uses the supplied Name unchanged only when at most 20 characters and the independent precheck passes. For a longer Name or conflict, request a distinct ShortName; never truncate. AccessSetName is the new Name. No other set's generated identities are reused.

If Oracle rejects a supplied value or an omission, inspect the detailed row report, reconcile actual state, correct the named mapping and obtain approval for new bytes. Do not automatically retry or characterize the base profile as universally verified. The known server-required initialization columns are explicitly supplied; descriptor and unresolved management-field omissions remain disclosed authoring policies rather than proven individual importer defaults. They do not mandate another export before an ordinary base-profile preparation.

Oracle's table documentation describes inapplicable ledger-set columns but does not specify this complete FSM CSV omission contract: [GL_LEDGERS](https://docs.oracle.com/en/cloud/saas/financials/26c/oedmf/glledgers-28674.html).

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MLS.APPLY_DEFAULTS | step | 40 | apply_default | prepared->MLS.ENFORCE_DESIGN;blocked->MLS.HANDLE_ERROR | MLS.CHECK_DEPENDENCIES | stop | For create apply packaged explicit initialization, checked new identities, allowlisted scoped structural values and named omission rules; preserve omitted update values and never overwrite supplied business choices. |

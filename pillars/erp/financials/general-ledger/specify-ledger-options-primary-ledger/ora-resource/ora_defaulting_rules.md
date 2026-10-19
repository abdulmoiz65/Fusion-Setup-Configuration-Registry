# Specify Ledger Options Primary-Ledger Defaulting Rules

## Population Classes

| Population Class | Policy |
|---|---|
| Required user input | Primary-ledger scope and retained earnings for a controlled new-primary save are never defaulted |
| Conditional user input | First period, posting-cutoff timezone, custom reversal criteria, and optional-family inputs are requested only when their trigger applies. Journal Description Language is not user intake for the supported new-ledger baseline; English is controlled resolver-derived. A non-Standard AccountingMethodName is optional desired-state input for a UI handoff |
| Resolver-derived | Canonical ledger identity, account-combination ID as evidence, ordered account segments, the export-compatible multiline segment vector, account semantics, period membership, and evidence-backed method fields come from documented resolvers |
| Export-derived or inherited | Existing option values, headers, alias-only columns, multiline encoding, and service-owned values are preserved from the current scoped export |
| Controlled role default | A value may be proposed only for the same Fusion release and matching proven primary-ledger role; preview must label its class and no user choice is replaced |
| Intentional blank | Omitted optional accounts, create-time SlaDescriptionLanguage before any options save, cutoff timezone and date while cutoff is disabled, and TaxDefaultLeTrans may remain blank under the documented baseline. `GL-781444` proves the method language cannot remain blank in the assigned-method options save |
| Service owned | IDs, audit columns, process state, lifecycle state, and generated values remain preserved and are not authored by this task |

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| PrimaryLedgerName | No default | Every task invocation | No | resolve_primary_ledger_scope_exact |
| RetEarnCcidSegments | No business default; resolver-derived quoted 30-slot LF-delimited and LF-terminated segment vector from the exact user-selected account, using the validated package-derived vector shape | Controlled new-primary options save under the validated 133-column contract | No; the returned _CODE_COMBINATION_ID is used as the resolved CodeCombinationId and identity evidence only, while the hyphen-delimited display is never written here | resolve_retained_earnings_account |
| CumTransCcidSegments, ResEncumCcidSegments, RoundingCcidSegments, SlaEntCurBalSusSegments, SlaLedgerCurBalSusSegments, IntercoGainLossSegments, CrossLgrClrAccSegments, SuspenseAccountCcidSegments | Preserve existing; otherwise intentional blank | Corresponding posting-account option family is not explicitly requested | No; when requested require EnabledFlag Y, DetailPostingAllowedFlag Y, SummaryFlag N, effective dates, any family-defined AccountType, and the generic unique dynamic-segment mapping | read_primary_options_export |
| NetIncomeCcidSegments | Preserve existing; otherwise intentional blank | Average-balances family is not explicitly requested | No; when requested use direct LOV fields only for enablement, effectivity, DetailPostingAllowedFlag, SummaryFlag, and AccountType. Balance-enabled semantics require separately authoritative family evidence or a UI handoff because BalanceEnabledFlag is not exposed | read_primary_options_export |
| FirstLedgerPeriodName | No default | Operational or open readiness is requested | No | resolve_first_open_period_exact |
| FutureEnterablePeriodsLimit | Preserve existing; otherwise propose 1 | Existing ledger, or same-release matching new primary role with user review | No | read_primary_options_export |
| SlaAccountingMethodCode, SlaAccountingMethodType, SlaDescriptionLanguage | Preserve existing | Existing ledger outside the newly FSCR-created flow; never overwrite an established method merely by opening options | No | read_primary_options_export |
| SlaAccountingMethodCode | STANDARD_ACCRUAL | Newly FSCR-created primary ledger, whether the method was omitted, Standard Accrual was supplied, or another desired method was supplied | No for FSCR authoring | resolve_accounting_method_evidence |
| SlaAccountingMethodType | S | Newly FSCR-created primary ledger | No for FSCR authoring | resolve_accounting_method_evidence |
| SlaDescriptionLanguage | Controlled English business default; exact code returned by the unique enabled English base-language row from languagesLOV | Newly FSCR-created primary options save with assigned Standard Accrual and blank carrier language | No for the supported baseline. Never hardcode EN or US; write the authoritative returned code | resolve_method_language_exact |
| Non-CSV handoff receipt: RequestedAccountingMethodName and MethodChangeUIHandoffRequired | Exact requested alternative and Y | User explicitly names another method | Never populate these receipt labels as CSV fields; user changes the method manually after creation | resolve_accounting_method_evidence |
| NumberOfProcessors | 1 | Same-release package and matching new primary-ledger role | No |  |
| ProcessingUnitSize | 5000 | Same-release package and matching new primary-ledger role | No |  |
| ProjectsImplementedTrans | false | Same-release package and matching new primary-ledger role | No |  |
| CreateJeFlag | Y | Same-release package and matching new primary-ledger role | No |  |
| AutorevAfterOpenPrdFlag | Y | Same-release package and matching new primary-ledger role; this does not imply custom criteria | No |  |
| EnfSeqDateCorrelationCode | N | Same-release package and matching primary-ledger role | No |  |
| SuspenseAllowedFlag, AllowIntercompanyPostFlag, TrackRoundingImbalanceFlag, EnableAverageBalancesFlag | Preserve existing; otherwise N | Family not explicitly requested and same-release matching disabled baseline applies | No | read_primary_options_export |
| EnableBudgetaryControlFlag, RequireBudgetJournalsFlag, EnableJeApprovalFlag, EnableAutomaticTaxFlag | Preserve existing; otherwise N | Family not explicitly requested and same-release matching disabled baseline applies | No | read_primary_options_export |
| ConsolidationLedgerFlag, TranslateEodFlag, TranslateQatdFlag, TranslateYatdFlag, AutomaticallyCreatedFlag | Preserve existing; otherwise N | Family not explicitly requested and same-release matching disabled baseline applies | No | read_primary_options_export |
| SlaBalByLedgerCurrFlag, EnableReconciliationFlag, SlaLedgerCashBasisFlag, UssglOptionCode | Preserve existing; otherwise N | Family not explicitly requested and same-release matching disabled baseline applies | No | read_primary_options_export |
| ValidateJournalRefDate, JrnlsGroupByDateFlag, PriorPrdNotificationFlag, PopUpStatAccountFlag | Preserve existing; otherwise N | Family not explicitly requested and same-release matching disabled baseline applies | No | read_primary_options_export |
| SequencingModeCode, NetClosingBalFlag, IncomeStmtAdbStatusCode, BalanceMjeByCurrencyFlag, SingleCurrencyJournalFlag | Preserve existing; otherwise N | Family not explicitly requested and same-release matching disabled baseline applies | No | read_primary_options_export |
| PostingCutoffFlag | Preserve existing; otherwise N | Posting cutoff not explicitly requested and same-release matching disabled baseline applies | No | read_primary_options_export |
| PostingCutoffTimezoneCode, PostingCutoffDate | Preserve existing; otherwise blank | PostingCutoffFlag is N | No | read_primary_options_export |
| RevalFromPriLgrCurr and other optional rate, threshold, strict-close, calendar, criteria, tax-helper, SLA-helper, and DFF fields | Preserve existing; otherwise intentional blank | Corresponding family was not explicitly requested | No; exact same-role evidence or UI handoff is required for a requested change | read_primary_options_export |
| Attribute1 through Attribute15 and AttributeCategory | Preserve existing; otherwise intentional blank | DFF context is not deployed and explicitly requested | No; author only with exact deployed-context evidence plus explicit user intent | read_primary_options_export |
| CriteriaSetName | Preserve existing; otherwise blank | Custom reversal criteria were not explicitly requested | No | read_primary_options_export |
| TaxDefaultLeTrans | Preserve existing; otherwise blank | Automatic-tax family is disabled or supported evidence leaves it blank | No | read_primary_options_export |
| Optional account segment fields | Preserve existing; otherwise blank | Corresponding optional account-backed family was not explicitly requested | No | read_primary_options_export |
| IDs, short name, audit columns, process state, lifecycle state, and alias-only fields | Preserve exported value | Always | No | read_primary_options_export |

## Default Safety Rules

| Situation | What Happens |
|---|---|
| Existing scoped ledger | Preserve every field not explicitly approved for change; never reset an existing option to a baseline value |
| Release or primary role differs from controlled evidence | Do not apply a controlled default; preserve export or block for evidence |
| FutureEnterablePeriodsLimit omitted on a matching new primary | Show 1 as a controlled proposal, not a mandatory question or guessed business choice; any accepted proposal remains subject to preview approval |
| Optional family not requested | Preserve existing behavior or the proven disabled baseline without collecting family questions |
| Optional customization requires UI | Keep the safe baseline, identify the exact UI handoff, and block Review and Submit readiness until same-scope re-export verifies completion |
| Any default changes after preview | Invalidate approval and regenerate the semantic diff |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SLOP.APPLY_DEFAULTS | step | 40 | apply_default | prepared->SLOP.ENFORCE_DESIGN;blocked->SLOP.HANDLE_ERROR | SLOP.CHECK_DEPENDENCIES | stop | Produce the smallest primary-options delta using the documented population classes and triggered optional-family policy. |

# Specify Ledger Options Secondary-Ledger Defaulting Rules

This task defaults only technical or explicitly proven baseline behavior. It never silently accepts a create-time value for First Opened Period, Number of Future Enterable Periods, or Retained Earnings Account; all three are mandatory user confirmations in this context.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| FirstLedgerPeriodName | No default; exact eligible user-confirmed period | Always for this task | No | resolve_first_open_period |
| FutureEnterablePeriodsLimit | No default; exact user-confirmed integer 0 through 999 | Always for this task | No |  |
| RetEarnCcidSegments | No business default; resolver-derived quoted 30-slot actual-LF-delimited and LF-terminated segment vector from the exact user-confirmed account, using the validated package-derived vector shape | Always for this task under the validated 133-column contract | No; the returned _CODE_COMBINATION_ID is used as the resolved CodeCombinationId and identity evidence only, while the hyphen-delimited display is never written here | resolve_ledger_role_account |
| CumTransCcidSegments, ResEncumCcidSegments, RoundingCcidSegments, SlaEntCurBalSusSegments, SlaLedgerCurBalSusSegments, IntercoGainLossSegments, CrossLgrClrAccSegments, SuspenseAccountCcidSegments | Preserve existing or intentional blank | Corresponding posting-account option family is not explicitly requested | No; when requested require EnabledFlag Y, DetailPostingAllowedFlag Y, SummaryFlag N, effective dates, any family-defined AccountType, and the generic unique dynamic-segment mapping | read_secondary_options_export |
| NetIncomeCcidSegments | Preserve existing or intentional blank | Average-balances family is not explicitly requested | No; direct LOV evidence covers enablement, effectivity, DetailPostingAllowedFlag, SummaryFlag, and AccountType only. Balance-enabled semantics require separately authoritative family evidence or a UI handoff because BalanceEnabledFlag is not exposed | read_secondary_options_export |
| Existing option values | Preserve exact scoped export value | Field is not owned by confirmed user intent | No | read_secondary_options_export |
| Inherited SequencingModeCode, SingleCurrencyJournalFlag, BalanceMjeByCurrencyFlag | Preserve exact secondary export values | Always | No | read_secondary_options_export |
| SlaAccountingMethodCode | STANDARD_ACCRUAL | Newly FSCR-created secondary at any conversion level | No for FSCR authoring | resolve_accounting_method_evidence |
| SlaAccountingMethodType | S | Newly FSCR-created secondary at any conversion level | No for FSCR authoring | resolve_accounting_method_evidence |
| SlaDescriptionLanguage | Controlled English business default; exact code returned by the unique enabled English base-language row from languagesLOV | Newly FSCR-created secondary options save with assigned Standard Accrual and blank carrier language | No for the supported baseline. Never hardcode EN or US; write the authoritative returned code | resolve_method_language_exact |
| Existing accounting-method fields | Preserve exact scoped export value | Existing secondary outside the newly FSCR-created flow | No | read_secondary_options_export |
| Non-CSV handoff receipt: RequestedAccountingMethodName and MethodChangeUIHandoffRequired | Exact requested alternative and Y | User explicitly names another method | Never populate these receipt labels as CSV fields; complete the method change manually after creation | resolve_accounting_method_evidence |
| AutorevAfterOpenPrdFlag | Preserve current export; Y is compatible with a blank criteria set | No custom reversal criteria requested | No | read_secondary_options_export |
| CriteriaSetName | Preserve existing or intentional blank | Custom reversal criteria not explicitly requested | No | read_secondary_options_export |
| PostingCutoffFlag, PostingCutoffTimezoneCode, PostingCutoffDate | N, intentional blank, intentional blank | New controlled baseline or explicit cutoff request awaits UI completion | No direct override in baseline |  |
| SuspenseAllowedFlag, AllowIntercompanyPostFlag, TrackRoundingImbalanceFlag, EnableAverageBalancesFlag, EnableBudgetaryControlFlag, RequireBudgetJournalsFlag, EnableJeApprovalFlag, EnableAutomaticTaxFlag | Preserve existing on edit; N for each field only on a same-release matching new-role baseline when the family is not requested | Optional family is outside confirmed intent | No | read_secondary_options_export |
| ConsolidationLedgerFlag, TranslateEodFlag, TranslateQatdFlag, TranslateYatdFlag, SlaBalByLedgerCurrFlag, EnableReconciliationFlag, SlaLedgerCashBasisFlag, UssglOptionCode | Preserve existing on edit; N for each field only on a same-release matching new-role baseline when the family is not requested | Optional family is outside confirmed intent | No | read_secondary_options_export |
| ValidateJournalRefDate, JrnlsGroupByDateFlag, PriorPrdNotificationFlag, PopUpStatAccountFlag, NetClosingBalFlag, IncomeStmtAdbStatusCode | Preserve existing on edit; N for each field only on a same-release matching new-role baseline when the family is not requested | Optional family is outside confirmed intent | No | read_secondary_options_export |
| Optional-family account fields | Preserve existing or intentional blank | Corresponding feature is not explicitly requested | No | read_secondary_options_export |
| TaxDefaultLeTrans | Preserve existing or intentional blank | Automatic tax is absent or exact role evidence allows blank | No | read_legal_entity_bsv_export |
| RevalFromPriLgrCurr and other optional rate, threshold, strict-close, calendar, criteria, tax-helper, SLA-helper, and DFF fields | Preserve existing or intentional blank | Corresponding family is not explicitly requested | No; exact same-role evidence or UI handoff is required for a requested change | read_secondary_options_export |
| Attribute1 through Attribute15 and AttributeCategory | Preserve existing or intentional blank | DFF context is not deployed and explicitly requested | No; author only with exact deployed-context evidence plus explicit user intent | read_secondary_options_export |
| Relationship, journal-rule, BSV, root, and configuration-detail values | Preserve exact parent-primary-scoped populated export values | Always | No | acquire_primary_scoped_options_export |
| IDs, short name, audit fields, process fields, status receipts | Preserve existing or leave service owned | Always | No | read_secondary_options_export |

## Population Classes

| Population Class | Rule |
|---|---|
| Mandatory user confirmation | Record the proposed and confirmed values separately; populate only the confirmed value. |
| Conditional user input | Collect only after the user explicitly triggers the feature or SLA condition. Journal Description Language is resolver-derived English for the supported baseline, not user intake. |
| Resolver derived | Retain the exact account ID as evidence and populate the physical account field from the same eligible record's ordered segments using the package-derived multiline vector contract. |
| Controlled method policy | Retain Standard Accrual for the new-ledger flow and treat another requested method only as a manual UI handoff. |
| Export derived or inherited | Preserve the exact value from the fresh populated export scoped by the secondary's parent PrimaryLedgerId unless this task owns an approved change. |
| Controlled role default | Use only for the same release, secondary conversion role, and package shape; do not extrapolate. |
| Intentional blank | Keep blank where the product contract permits it; never coerce every blank flag to N. |
| Service owned | Do not author generated identity, audit, process, or status values. |

## Optional Family Population Policy

| Family | Baseline Behavior | Triggered Behavior |
|---|---|---|
| Suspense, rounding, entered-currency balancing | Preserve on edit or disabled same-role baseline | Require exact role-valid posting account; use UI handoff if the full same-role contract is not proven. |
| Intercompany | Preserve on edit or disabled baseline | Require external intercompany setup and exact role evidence; ledger flag alone is insufficient. |
| Average balances | Preserve on edit or disabled baseline | Require a role-valid Net Income Account and Transaction Calendar when applicable. Use LOV flags for enablement, effectivity, nonposting, summary, and account type; require separately authoritative evidence for balance-enabled semantics or use the UI handoff. |
| Budgetary control and budget journals | Preserve on edit or disabled baseline | Require owning-task readiness; use UI handoff for unsupported direct completion. |
| Automatic tax | Preserve on edit or disabled baseline | Require exact legal entity and BSV evidence; never invent internal ID and do not force TaxDefaultLeTrans when exact evidence permits blank. |
| Translation and revaluation | Preserve on edit or disabled baseline | Require CTA posting account plus appropriate rate and period readiness. |
| Sequencing | Preserve inherited and existing values | Do not overwrite inherited fields without a separately supported override contract. |
| Automatic reversal | Preserve export; AutorevAfterOpenPrdFlag Y may coexist with blank criteria | Ask for Reversal Criteria Set only for explicit custom criteria intent. |
| Approval and reconciliation | Preserve on edit or disabled baseline | Require the external workflow or reconciliation setup before enabling. |
| Posting cutoff | N with blank timezone and date | Import baseline, configure in UI, and re-export; never author Y with blank timezone or assume UTC. |
| SLA cash basis and USSGL | Preserve on edit or disabled baseline | Applicable only to supported Subledger design with exact SLA evidence; otherwise UI handoff. |

## CSV Field Population

| Package Member | Relevant Population Behavior |
|---|---|
| GL_PRIMARY_LEDGER.csv | Update FirstLedgerPeriodName, FutureEnterablePeriodsLimit, the derived 30-slot actual-LF-delimited and LF-terminated RetEarnCcidSegments vector, retain the controlled Standard Accrual fields for the new-ledger flow, and update only explicitly supported option fields on the exact SECONDARY row. |
| GL_SECONDARY_LEDGER.csv | Mirror the exact same secondary-row values, including the byte-identical quoted multiline vector; any semantic or serialization mismatch blocks. |
| GL_LEDGER.csv and ORA_GL_PRIMARY_LEDGER_CONFIG.csv | Preserve root aliases unchanged. |
| ORA_GL_JOURNAL_CONFIG_DETAIL.csv | Preserve dependency closure; never synthesize workflow status or setup-step receipts. |
| ORA_LEGAL_ENTITY_BAL_SEG_VAL_DEF.csv and GL_LEDGER_SEG_VAL_ASSIGNMENT.csv | Preserve unchanged; use as read-only dependency evidence when applicable. |
| ORA_GL_LEDGER_RELATIONSHIP.csv, ORA_GL_JOUNAL_CONVERSION_RULES.csv, ORA_PRIMARY_BALANCING_SEGMENT_VALUE_CONVERSION_RULES.csv | Preserve relationship, mapping, rule, and conversion state unchanged. |
| ASM_SETUP_CSV_METADATA.xml | Preserve the export-generated manifest and business-object field contract. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SLOS-040-APPLY-DEFAULTS | step | 40 | apply_default | applied->SLOS-050-ENFORCE-DESIGN;failed->SLOS-070-HANDLE-ERROR | SLOS-030-RESOLVE-DEPENDENCIES | stop | Always |

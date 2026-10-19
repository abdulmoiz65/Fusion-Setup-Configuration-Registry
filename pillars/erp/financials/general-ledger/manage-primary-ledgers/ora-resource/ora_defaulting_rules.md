# Manage Primary Ledgers Defaulting Rules

## Population Classes

| Population Class | Policy |
|---|---|
| Required user input | Name, chart of accounts, accounting calendar, and currency remain mandatory business choices and never receive guessed defaults |
| Conditional user input | A non-Standard-Accrual AccountingMethodName is optional desired-state input used only to create a post-create manual-change handoff. First-period and ledger-option decisions are handed to their owning task |
| Resolver-derived | IDs, codes, period set, period type, structure instance, flexfield identity, and segment-role fields come only from authoritative resolver output |
| Export-derived or inherited | Existing rows, package headers, metadata, alias-only columns, and unrelated data are preserved exactly from the validated same-environment, same-release baseline |
| Controlled role default | Apply only when the source package is from the same Fusion release, the new row has the matching proven primary-ledger role, and the preview identifies the value as a controlled default |
| Intentional blank | Optional omitted values remain blank; blank is not missing when the documented in-process or disabled baseline permits it |
| Service owned | Generated short names, identifiers, audit columns, process values, and lifecycle state remain blank on create when generation is supported and are verified by re-export |

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Name | No default | New primary ledger | No |  |
| ChartOfAccountsName, StructureInstanceId, StructureInstanceNumber, and StructureInstanceCode | Exact chartOfAccountsLOV output; map ChartOfAccountsName from returned Name | New primary ledger after exact resolution | No; do not invent ChartOfAccountsId or substitute StructureInstanceId for StructureInstanceNumber | resolve_chart_of_accounts_exact |
| StructureInstanceCode, StructureCode, KeyFlexfieldCode, ApplicationId | Exact selected structure-instance export row | New primary ledger after the populated CoA export proves the exact selected instance | No | derive_chart_of_accounts_roles |
| Balancing SegmentCode, segment Name, and SequenceNumber | Resolver evidence only | The qualified-label export assigns exactly one GL_BALANCING role | No; retain in the preview evidence and never populate a ledger field merely from the name or sequence | derive_chart_of_accounts_roles |
| BalSegColumnName | ColumnName from the exact enabled balancing structure-segment row | The GL_BALANCING SegmentCode rejoins through KeyFlexfieldCode, ApplicationId, StructureCode, and SegmentCode | No; never infer SEGMENT1 or derive it from SequenceNumber | derive_chart_of_accounts_roles |
| BalSegValueSetCode | ValueSetCode from the exact balancing structure-instance-segment row | The same GL_BALANCING SegmentCode rejoins through KeyFlexfieldCode, ApplicationId, StructureInstanceCode, and SegmentCode | No; never substitute DefaultValueSetCode | derive_chart_of_accounts_roles |
| Management SegmentCode, segment Name, and SequenceNumber | Resolver evidence only | Exactly one GL_MANAGEMENT assignment exists | No; retain in the preview evidence only | derive_chart_of_accounts_roles |
| MgtSegColumnName | ColumnName from the exact enabled management structure-segment row, otherwise true blank | Exactly one GL_MANAGEMENT assignment exists, otherwise none exists | No; zero assignments means blank and more than one blocks | derive_chart_of_accounts_roles |
| MgtSegValueSetCode | ValueSetCode from the exact management structure-instance-segment row, otherwise true blank | Exactly one GL_MANAGEMENT assignment exists, otherwise none exists | No; never substitute DefaultValueSetCode and never invent a management segment | derive_chart_of_accounts_roles |
| ApplicationShortName | GL | The populated CoA export proves KeyFlexfieldCode GL# and the selected GL application identity | No | derive_chart_of_accounts_roles |
| UserPeriodSetName, PeriodSetName, AccountedPeriodType | Resolver output from exact accounting calendar | New primary ledger after exact accounting-calendar resolution | No | resolve_accounting_calendar_exact |
| FirstLedgerPeriodName | Exact explicit physical first-period choice or independently authoritative same-role export evidence, validated against EnteredPeriodName and PeriodType from the complete period LOV result | New primary ledger after the complete period set resolves | No; response order and label sorting are not authority, and this physical create value remains distinct from a later options-task opening decision | list_eligible_accounting_periods |
| CurrencyCode | Resolver output | New primary ledger after exact active monetary-currency resolution | No | resolve_monetary_currency_exact |
| Description | Blank | User omits the optional description | No |  |
| Attribute1 through Attribute15 and AttributeCategory | Blank | DFF context is not deployed and explicitly requested | No; preserve on edit and author only with exact deployed-context evidence plus explicit user intent |  |
| EffectiveAccountingMethodName | Standard Accrual | Every new FSCR-created primary ledger, whether the method is omitted, Standard Accrual is supplied, or another desired method is supplied | No for creation | resolve_accounting_method_evidence |
| SlaAccountingMethodCode | STANDARD_ACCRUAL | Every new FSCR-created primary ledger | No for creation | resolve_accounting_method_evidence |
| SlaAccountingMethodType | S | Every new FSCR-created primary ledger | No for creation | resolve_accounting_method_evidence |
| SlaDescriptionLanguage | Blank | Every new FSCR-created primary ledger using the controlled Standard Accrual tuple | No for creation | resolve_accounting_method_evidence |
| Non-CSV handoff receipt: RequestedAccountingMethodName and MethodChangeUIHandoffRequired | Exact requested alternative and Y | User explicitly names a method other than Standard Accrual or STANDARD_ACCRUAL | Never populate these receipt labels as CSV fields; complete the change manually after creation | resolve_accounting_method_evidence |
| AcctgEnvironmentCode | NONE | Same-release matching fresh primary-root role only | No; preserve existing root values and do not generalize across roles |  |
| LedgerCategoryCode | PRIMARY | New row has the proven primary-ledger role | No |  |
| AlcLedgerTypeCode | NONE | Same-release matching new primary physical role before reporting-currency relationships exist | No; later reporting setup may change source state to SOURCE |  |
| ObjectTypeCode | L | Same-release package and matching new primary-ledger role | No |  |
| LeLedgerTypeCode | L | Same-release package and matching normal-ledger role | No |  |
| LedgerAttributes | L | Same-release package and matching new primary-ledger role | No |  |
| BalSegValueOptionCode and MgtSegValueOptionCode | A | Same-release matching all-values primary design | No; an explicit reviewed assignment design owns any different value and child rows | derive_chart_of_accounts_roles |
| NumberOfProcessors | 1 | Same-release package and matching new primary-ledger role | No |  |
| ProcessingUnitSize | 5000 | Same-release package and matching new primary-ledger role | No |  |
| ProjectsImplementedTrans | false | Same-release package and matching new primary-ledger role | No |  |
| CreateJeFlag | Y | Same-release package and matching new primary-ledger role | No |  |
| AutorevAfterOpenPrdFlag | Y | Same-release package and matching new primary-ledger role | No |  |
| FutureEnterablePeriodsLimit | 1, proposed for options review | Same-release package and matching new primary-ledger role; final ownership remains Specify Ledger Options | No |  |
| EnfSeqDateCorrelationCode | N | Same-release package and matching new primary-ledger role | No |  |
| SuspenseAllowedFlag, AllowIntercompanyPostFlag, TrackRoundingImbalanceFlag, EnableAverageBalancesFlag | N | Same-release package and matching disabled baseline for an unrequested optional family | No |  |
| EnableBudgetaryControlFlag, RequireBudgetJournalsFlag, EnableJeApprovalFlag, EnableAutomaticTaxFlag | N | Same-release package and matching disabled baseline for an unrequested optional family | No |  |
| ConsolidationLedgerFlag, TranslateEodFlag, TranslateQatdFlag, TranslateYatdFlag, AutomaticallyCreatedFlag | N | Same-release package and matching disabled baseline for an unrequested optional family | No |  |
| SlaBalByLedgerCurrFlag, EnableReconciliationFlag, SlaLedgerCashBasisFlag, UssglOptionCode | N | Same-release package and matching disabled baseline for an unrequested optional family | No |  |
| ValidateJournalRefDate, JrnlsGroupByDateFlag, PriorPrdNotificationFlag, PopUpStatAccountFlag | N | Same-release package and matching disabled baseline for an unrequested optional family | No |  |
| SequencingModeCode, NetClosingBalFlag, IncomeStmtAdbStatusCode, BalanceMjeByCurrencyFlag, SingleCurrencyJournalFlag | N | Same-release package and matching disabled baseline for an unrequested optional family | No |  |
| PostingCutoffFlag | N | Same-release package and matching disabled baseline | No |  |
| PostingCutoffTimezoneCode, PostingCutoffDate | True empty CSV fields | PostingCutoffFlag is N | No; serialize each value as an empty field between delimiters, never as whitespace, a line break, `\\n`, `null`, `None`, or another textual placeholder |  |
| RevalFromPriLgrCurr and other optional rate, threshold, strict-close, calendar, criteria, tax-helper, SLA-helper, and DFF fields | Blank | Matching new primary role and the optional feature is not requested | No; preserve on edit and use exact same-role/UI evidence when requested |  |
| CumTransCcidSegments, ResEncumCcidSegments, NetIncomeCcidSegments, RoundingCcidSegments, SlaEntCurBalSusSegments, SlaLedgerCurBalSusSegments, IntercoGainLossSegments, RetEarnCcidSegments, CrossLgrClrAccSegments, SuspenseAccountCcidSegments | Blank | Initial primary-ledger creation, including when the same user request also supplies a retained-earnings account or another options choice | No; preserve those choices only as non-CSV handoff receipts because primary Specify Ledger Options owns their validation and serialization |  |
| ShortName, LedgerId, relationship IDs, audit columns, status columns, process IDs | Blank for service generation | New row and the exact package contract supports service generation | No |  |
| Every field of an existing scoped or unrelated row | Preserve exported value | Updating or carrying a package baseline | No |  |

## Default Safety Rules

| Situation | What Happens |
|---|---|
| Release or role does not exactly match the controlled evidence | Do not apply a controlled constant; preserve an export value or block for authoritative evidence |
| User supplied a mandatory business choice | Never replace it with a role default; validate and resolve the exact choice. Accounting method is the explicit controlled exception defined by this policy |
| User omitted AccountingMethodName or supplied Standard Accrual | Apply STANDARD_ACCRUAL, S, and blank language without asking for technical fields |
| User supplied another AccountingMethodName | Preserve it as a desired-state receipt, apply Standard Accrual to the create package, and record the post-create manual-change handoff |
| Optional family was not requested | Keep the exact existing value for an existing ledger or use only the proven disabled baseline for a matching new row |
| An intentional blank is written to CSV | Emit a true zero-character CSV value. Reject whitespace, embedded control characters, escaped control text such as `\\n`, and textual null sentinels such as `null` or `None` before checksumming or preview |
| Service-generated field remains blank in the proposed row | Show it as service owned in preview and verify its returned value by same-scope re-export |
| A default changes after preview | Invalidate approval and regenerate the semantic preview before import |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPL.APPLY_DEFAULTS | step | 40 | apply_default | prepared->MPL.ENFORCE_DESIGN;blocked->MPL.HANDLE_ERROR | MPL.CHECK_DEPENDENCIES | stop | Build the smallest proposed primary-ledger row delta using only the documented population classes. |

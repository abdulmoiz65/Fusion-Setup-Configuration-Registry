# Specify Ledger Options Secondary-Ledger Dependency Readiness

This task updates only the exact secondary physical row. Relationship, mapping, journal-rule, legal-entity, BSV, and configuration-detail members are dependency closure unless a product-generated receipt appears in a re-export.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Exact secondary and owning primary | Resolve one exact SECONDARY, then resolve its one authoritative parent PRIMARY from the Manage Secondary Ledgers relationship receipt or package before any options export. |
| 2 | Primary-scoped populated carrier | Run GL_SPECIFY_LEDGER_OPTIONS in populated data mode with GL_PRIMARY_LEDGER and PRIMARY_LEDGER_ID equal to the resolved parent PrimaryLedgerId. Reject template-only, unscoped, wrong-parent, or unrelated-ledger output. |
| 3 | Current secondary row | Reconcile the target SECONDARY row in both 133-column aliases from that scoped export and capture existing, inherited, blank, and service-owned values. |
| 4 | Mandatory option references | Resolve the exact period; query accountCombinationsLOV using StructureInstanceNumber with no fields projection, map dynamic keys generically, and require an exact enabled/effective AccountType O, DetailPostingAllowedFlag Y, SummaryFlag N CCID without a retained-earnings export; then confirm period, future count, and account. If absent, pause for routed FBDI creation and re-query. |
| 5 | Method and conditional options | Preserve controlled Standard Accrual, resolve the controlled English journal-description-language default, and establish the required UI handoff for a requested alternative or explicitly triggered option. |
| 6 | Smallest symmetric delta | Update only the owning SECONDARY row in both aliases and preserve all other package content. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| secondary_parent | Exact primary owning the target secondary | Yes | Always | Verify | Authoritative Manage Secondary Ledgers relationship receipt or package row, reconciled with any user-supplied parent | resolve_secondary_primary_parent | The export scope is always a primary ledger ID, even when the requested option row is secondary | Supply the primary-secondary pair when no durable relationship receipt exists; never infer the parent from shared accounting dimensions | SourcePrimaryLedgerId, SourcePrimaryLedgerName when available, SecondaryLedgerId, relationship identity |
| task_package | Parent-primary-scoped Specify Ledger Options export | Yes | Always | Lookup | Fresh populated GL_SPECIFY_LEDGER_OPTIONS task export with the exact parent PrimaryLedgerId criterion | acquire_primary_scoped_options_export | The parent-scoped export is both the current-state source and the only edit carrier for the secondary; template-only and project-owned create packages cannot supply current option values | Resolve the parent first, then reject header-only, unscoped, wrong-task, wrong-environment, wrong-parent, or unrelated-ledger output | Package release and scope, fingerprint, members, headers, aliases, manifest, SourcePrimaryLedgerId |
| secondary_scope | Exact secondary under exact primary | Yes | Always | Lookup | Authorized ledgersLOV, parent relationship evidence, chartOfAccountsLOV, and both physical aliases | resolve_secondary_ledger_scope | Same Oracle label is used for primary and secondary contexts, so task scope and the secondary COA structure number must be explicit | Supply the exact secondary and its parent or relationship evidence | SecondaryLedgerId, SecondaryLedgerName, SourcePrimaryLedgerId, StructureInstanceCode, StructureInstanceNumber, conversion level |
| secondary_export | Current option row in both aliases | Yes | Always | Verify | Exact SECONDARY logical row in both aliases from the fresh parent-primary-scoped populated export | read_secondary_options_export | Mandatory confirmations and preserve-on-edit require the actual current Fusion values | Block if aliases differ, the row is absent or duplicated, parent linkage is wrong, or unrelated rows are present | Existing exported values, inherited values, intentional blanks, service-owned values, alias parity |
| first_open_period | Eligible first period | Yes | Always | Lookup and user confirmation | accountingPeriodsLOV queried only by PeriodSetNameId, completely paged, then filtered locally by PeriodType and user-selected EnteredPeriodName | resolve_first_open_period | The UI requires a real calendar period for this in-process secondary | Select and confirm one exact eligible period; do not use response order | FirstLedgerPeriodName |
| retained_earnings | Retained Earnings Account and existing CCID | Yes | Always | Lookup and user confirmation | accountCombinationsLOV scoped by _CHART_OF_ACCOUNTS_ID equal to the secondary StructureInstanceNumber, no fields projection, complete pagination, generic unique dynamic-key mapping, exact local segment comparison, and fixed semantic-flag checks | resolve_ledger_role_account | The exact AccountType O, DetailPostingAllowedFlag Y, SummaryFlag N combination must resolve before preview; no value-set or other export is part of this lookup | Select and confirm the account. If zero exact eligible rows return, pause while the router prepares and, after its own immutable preview and approval, runs Import Account Combinations for GL_MANAGE_ACCOUNT_COMBINATIONS; then re-query | Existing _CODE_COMBINATION_ID identity evidence, enablement/effectivity and semantic flags, ordered segments, RetEarnCcidSegments |
| retained_earnings_create | Missing retained-earnings account combination | Conditional | resolve_ledger_role_account returns zero exact rows | Blocked | Separate GL_MANAGE_ACCOUNT_COMBINATIONS task in Financial Reporting Structures using Import Account Combinations FBDI through core.data-loader |  | Specify Ledger Options does not create combinations. The FBDI row uses the exact StructureInstanceCode and SEGMENT1 through SEGMENTn values and is separately previewed and approved | Complete the routed FBDI workflow, require terminal success, then rerun accountCombinationsLOV; an import request ID alone is insufficient | Immutable FBDI artifact and approval receipt, terminal import result, re-query receipt, resolved _CODE_COMBINATION_ID |
| future_periods | Number of Future Enterable Periods | Yes | Always | User confirmation | Explicit integer 0 through 999 |  | It is UI mandatory in this secondary context and cannot be silently accepted from the create default | Confirm or supply the count | FutureEnterablePeriodsLimit |
| accounting_method | Controlled Accounting Method and SLA readiness | Yes | Newly FSCR-created secondary | Verify | Current symmetric export plus the controlled Standard Accrual policy and optional requested-alternative receipt | resolve_accounting_method_evidence | FSCR does not leave the method blank or directly author arbitrary methods; Subledger retains any separate SLA-readiness requirement | Do not supply technical method fields. If another method is desired, state its exact display name for the manual post-create change | CSV: SlaAccountingMethodCode; SlaAccountingMethodType; SlaDescriptionLanguage. Non-CSV receipts: EffectiveAccountingMethodName; RequestedAccountingMethodName when different; MethodChangeUIHandoffRequired |
| method_language | Journal Description Language | Yes | Assigned-method secondary options row has blank SlaDescriptionLanguage | Lookup | English business intent plus exact enabled languages LOV | resolve_method_language_exact | Fusion rejects blank language with GL-781444, so the supported baseline resolves English without user intake | No input is needed when one enabled English base-language row resolves; resolve only genuine environment ambiguity | Resolver-derived nonblank SlaDescriptionLanguage and English evidence |
| role_accounts | Triggered option-family accounts | Conditional | Translation, suspense, rounding, entered-currency balancing, average balances, or another account-bearing family is explicitly requested | Lookup | Exact account-combination LOV scoped to secondary COA | resolve_ledger_role_account | Enabled feature paths require role-valid accounts | Provide each account only for the requested feature | Role-specific CcidSegments values |
| tax_prerequisites | Legal entity and balancing-segment assignment | Conditional | Automatic tax is explicitly requested | Verify | Exact legal-entity and BSV dependency export | read_legal_entity_bsv_export | Tax cannot use an invented internal legal-entity ID | Complete prerequisite setup or use UI handoff | Existing legal entity and BSV identity; TaxDefaultLeTrans only if exact evidence supports it |
| external_optional_setup | Intercompany, budgetary control, approval, rate, sequencing, or other external setup | Conditional | Corresponding family is explicitly requested | Blocked pending exact setup or UI completion | Exact dependency export or reviewed UI receipt | read_secondary_options_export | Ledger-row flags alone do not establish external policy | Configure the dependency in its owning task or UI, re-export, then revalidate | Readiness flag and UI handoff |

## Required Package Members

| Member | Population Policy |
|---|---|
| GL_LEDGER.csv | Preserve the parent-scoped export's dependency-closure root row unchanged. |
| ORA_GL_PRIMARY_LEDGER_CONFIG.csv | Preserve duplicate root alias unchanged. |
| GL_PRIMARY_LEDGER.csv | Update only the exact SECONDARY row and mirror the same option values in GL_SECONDARY_LEDGER.csv. |
| GL_SECONDARY_LEDGER.csv | Update the duplicate exact SECONDARY row; semantic inequality blocks. |
| ORA_GL_JOURNAL_CONFIG_DETAIL.csv | Preserve dependency closure. Accept a Fusion-generated setup-step or status receipt only from export; do not synthesize it. |
| ORA_LEGAL_ENTITY_BAL_SEG_VAL_DEF.csv | Preserve unchanged; it is dependency evidence for explicitly requested automatic tax. |
| GL_LEDGER_SEG_VAL_ASSIGNMENT.csv | Preserve unchanged. |
| ORA_GL_LEDGER_RELATIONSHIP.csv | Preserve relationship and mapping state unchanged. |
| ORA_GL_JOUNAL_CONVERSION_RULES.csv | Preserve all rule and parent-key values unchanged; the product filename spelling is intentional. |
| ORA_PRIMARY_BALANCING_SEGMENT_VALUE_CONVERSION_RULES.csv | Preserve all conversion or replication rows unchanged. |
| ASM_SETUP_CSV_METADATA.xml | Preserve the scoped export-generated manifest and never author process identity, status, request, release, or timestamp fields. |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact scope, value, semantics, and explicit confirmation agree | Read-only lookup only |
| Lookup | Supported alternate key is present | Read-only lookup only |
| Preserve | Optional family is not requested or an existing non-owned field remains unchanged | No create |
| UI handoff | Optional feature is requested but direct exact CSV authoring is outside supported scope | No direct create; re-export after UI |
| Blocked | Mandatory value, exact scope, dependency, confirmation, privilege, or package evidence is missing or ambiguous | No |

## Scoped Export Request Contract

The request property order is part of this task-specific scope contract. Build
and serialize the payload in this exact order: `TaskCode`,
`SetupTaskCSVExportCriteria`, then `SetupTaskCSVExportProcess`. Reject the
preview before export if `SetupTaskCSVExportProcess` precedes
`SetupTaskCSVExportCriteria`; Fusion may otherwise complete an overbroad export
that does not preserve the resolved parent-primary scope for the secondary
ledger.

| Request Field | Required Value | Derivation |
|---|---|---|
| TaskCode | GL_SPECIFY_LEDGER_OPTIONS | Exact setup-task code for Specify Ledger Options |
| SetupTaskCSVExportCriteria.TaskCode | GL_SPECIFY_LEDGER_OPTIONS | Must equal the parent TaskCode |
| SetupTaskCSVExportCriteria.BusinessObjectCode | GL_PRIMARY_LEDGER | The scope object remains the primary ledger for a secondary-options request |
| SetupTaskCSVExportCriteria.AttributeSet | Set1 | Exact task scope attribute set |
| SetupTaskCSVExportCriteria.AttributeName | PRIMARY_LEDGER_ID | Exact primary-ledger scope attribute |
| SetupTaskCSVExportCriteria.AttributeValue | Resolved SourcePrimaryLedgerId rendered as a string | Output of resolve_secondary_primary_parent; never use SecondaryLedgerId |
| SetupTaskCSVExportProcess.TaskCode | GL_SPECIFY_LEDGER_OPTIONS | Must equal the parent TaskCode |

The shared task-level exporter constructs the request object from this contract. Criteria are valid only for a populated task-data export; template-only mode is a preflight error. A live export creates a Fusion process and follows the shared export workflow's process monitoring and persistence rules.

## Missing Combination FBDI Handoff Contract

| Item | Required Contract |
|---|---|
| Owning setup task | GL_MANAGE_ACCOUNT_COMBINATIONS, Manage Account Combinations, Financial Reporting Structures |
| Import route | core.data-loader using the current Import Account Combinations FBDI template and UCM account fin/generalLedger/import; this is not an FSM setup-task CSV import because the catalog CSV export/import flags for GL_MANAGE_ACCOUNT_COMBINATIONS are N |
| Interface member | GL_BULK_COMBINATIONS_INT in the generated FBDI ZIP; preserve the current template column order and control-file contract |
| Exact row identity | STRUCTURE_INSTANCE_CODE from the secondary's resolved COA, plus SEGMENT1 through SEGMENTn populated in physical COA order; leave unused trailing segment columns blank |
| Create attributes | ENABLED_FLAG Y and DETAIL_POSTING_ALLOWED_FLAG Y for the reviewed retained-earnings create intent; populate START_DATE_ACTIVE only from explicit effective-date intent or the reviewed workflow default. Preserve optional end date, alternate account, DFF, and PRESERVE_FLAG as blank unless explicitly requested and validated |
| Service-owned or internal fields | Do not supply CODE_COMBINATION_ID, CONCAT_SEGS, STATUS, ERROR_MESSAGE, REQUEST_ID, or LOAD_REQUEST_ID as business input; use the current template's generated group and row mechanics |
| Validation | Validate the immutable ZIP through core.data-loader and the task handoff, including exact secondary COA, segment count/order, current template, UCM route, and duplicate prevention |
| Approval and execution | Present the Data Loader immutable preview and use its single authoritative approval workflow before upload or initiation. Run Load Interface File for Import with Import Account Combinations, then Import Account Combinations, and require terminal success |
| Resume proof | Re-run resolve_ledger_role_account and require exactly one full-vector enabled/effective AccountType O, DetailPostingAllowedFlag Y, SummaryFlag N row and its returned _CODE_COMBINATION_ID before rebuilding the Specify Ledger Options preview |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SLOS-030-RESOLVE-DEPENDENCIES | decision | 30 | resolve_dependency | ready->SLOS-040-APPLY-DEFAULTS;blocked->SLOS-070-HANDLE-ERROR | SLOS-020-RESOLVE-REFERENCES | stop | Always |

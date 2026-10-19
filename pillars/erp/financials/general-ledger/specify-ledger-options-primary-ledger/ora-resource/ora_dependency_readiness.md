# Specify Ledger Options Primary-Ledger Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Environment and primary identity | Bind the selected environment and release to one exact PRIMARY ledger, its PrimaryLedgerId, enabled chart StructureInstanceCode, and StructureInstanceNumber |
| 2 | Scoped populated carrier | Run GL_SPECIFY_LEDGER_OPTIONS as a populated data export scoped by GL_PRIMARY_LEDGER and PRIMARY_LEDGER_ID equal to the resolved PrimaryLedgerId; validate the returned package and use it as the edit carrier |
| 3 | Retained earnings | Query accountCombinationsLOV directly with _CHART_OF_ACCOUNTS_ID equal to StructureInstanceNumber and no fields projection, map the complete dynamic segment attributes uniquely from exported SegmentCode, Name, and ColumnName, then resolve exactly one enabled/effective, detail-postable, nonsummary AccountType O CCID. Do not trigger a retained-earnings export. If absent, pause for routed GL_MANAGE_ACCOUNT_COMBINATIONS FBDI and re-query after terminal success |
| 4 | Period readiness | Only for operational or open readiness, retrieve the complete exact period set and resolve the user's chosen FirstLedgerPeriodName |
| 5 | Method policy | Confirm a newly FSCR-created ledger retains Standard Accrual, resolve the controlled English journal-description-language default to Fusion's exact enabled code, and record any explicitly requested alternative method as a post-create manual-change handoff |
| 6 | Opt-in families | For each explicitly requested family, prove required account or external setup; otherwise preserve the baseline and create a named UI handoff |
| 7 | Alias and package readiness | Confirm the smallest delta updates the same PRIMARY logical row in both 133-column aliases and no other package member |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| slop_package | Primary-scoped Specify Ledger Options export | Yes | Always | Lookup | Fresh populated GL_SPECIFY_LEDGER_OPTIONS task export with the exact primary-ledger criterion | acquire_primary_scoped_options_export | The scoped export is both the current-state source and the only edit carrier; template-only and project-owned create packages can be historical evidence but cannot supply current option values | Resolve the exact primary before export. Reject header-only, unscoped, wrong-task, wrong-environment, or unrelated-ledger output | Scoped package path and fingerprint, member inventory, headers, aliases, metadata identity, PrimaryLedgerId |
| slop_primary | Exact primary-ledger scope and COA structure number | Yes | Always | Lookup | Fusion ledgersLOV followed by chartOfAccountsLOV | resolve_primary_ledger_scope_exact | This contextual resource must never update a secondary or another primary ledger, and accountCombinationsLOV requires the structure number rather than StructureInstanceId | Provide the exact primary-ledger name and resolve any ambiguity | PrimaryLedgerId, PrimaryLedgerName, StructureInstanceCode, StructureInstanceNumber, accounting dimensions |
| slop_current | Current primary options rows | Yes | Always | Verify | Exact PRIMARY logical row in both aliases from the fresh primary-scoped populated export | read_primary_options_export | Preserve-on-edit and the smallest-delta rule require the actual current Fusion values | Block if either alias is missing, duplicated, divergent, stale, or contains an unrelated ledger | Current exported values, alias parity, serialization contract, service-owned values |
| slop_retained | Retained earnings account and existing CCID | Yes | Controlled new-primary options save | Lookup | accountCombinationsLOV scoped by _CHART_OF_ACCOUNTS_ID equal to StructureInstanceNumber, with no fields projection, complete pagination, generic unique dynamic-key mapping, exact local segment comparison, and fixed semantic-flag checks | resolve_retained_earnings_account | An existing enabled/effective AccountType O, DetailPostingAllowedFlag Y, SummaryFlag N combination must resolve before preview; no value-set or other export is part of this lookup | Supply the exact account. If zero exact eligible rows return, pause while the router prepares and, after its own immutable preview and approval, runs Import Account Combinations for GL_MANAGE_ACCOUNT_COMBINATIONS; then re-query | Existing _CODE_COMBINATION_ID as identity evidence, enablement/effectivity and semantic flags, ordered segments, RetEarnCcidSegments |
| slop_retained_create | Missing retained-earnings account combination | Conditional | resolve_retained_earnings_account returns zero exact rows | Blocked | Separate GL_MANAGE_ACCOUNT_COMBINATIONS task in Financial Reporting Structures using Import Account Combinations FBDI through core.data-loader |  | Specify Ledger Options does not create combinations. The FBDI row uses the exact StructureInstanceCode and SEGMENT1 through SEGMENTn values and is separately previewed and approved | Complete the routed FBDI workflow, require terminal success, then rerun accountCombinationsLOV; an import request ID alone is insufficient | Immutable FBDI artifact and approval receipt, terminal import result, re-query receipt, resolved _CODE_COMBINATION_ID |
| slop_period | First period | Conditional | Operational or open readiness is requested | Lookup | Fusion accounting-period LOV scoped by exported period set and type | resolve_first_open_period_exact | Period selection is a mandatory business decision for the requested readiness outcome | Choose one exact eligible period; do not ask the system to choose | FirstLedgerPeriodName and period evidence |
| slop_method | Controlled accounting method | Yes | Newly FSCR-created primary-ledger flow | Verify | Current symmetric options export plus the controlled Standard Accrual authoring policy and optional requested-alternative receipt | resolve_accounting_method_evidence | The new-ledger path must not silently become blank or directly author an arbitrary method | Do not supply technical fields. If another method is desired, provide its display name for the manual post-create change | CSV: SlaAccountingMethodCode; SlaAccountingMethodType; SlaDescriptionLanguage. Non-CSV receipts: EffectiveAccountingMethodName; RequestedAccountingMethodName when different; MethodChangeUIHandoffRequired |
| slop_language | Journal Description Language | Yes | The assigned-method options row has blank SlaDescriptionLanguage | Lookup | English business intent plus exact enabled languages LOV | resolve_method_language_exact | Fusion rejects blank language with GL-781444, so the supported baseline resolves English without user intake | No input is needed when one enabled English base-language row resolves. Resolve an environment ambiguity only when zero or multiple eligible English rows exist | Resolver-derived nonblank SlaDescriptionLanguage and English language evidence |
| slop_option_account | Optional account-backed family | Conditional | User explicitly requests CTA, reserve-for-encumbrance, rounding, suspense, intercompany, SLA suspense, or net-income behavior | Lookup | Fusion account-combination LOV scoped to the primary chart of accounts | resolve_optional_ledger_account_role | Each account must satisfy its family-specific semantic role | Supply the exact account or accept the named UI handoff | Account segment value and role evidence |
| slop_tax | Automatic-tax external setup | Conditional | User explicitly requests automatic tax | Verify | Current authoritative legal-entity and balancing-segment-value assignment exports | verify_automatic_tax_prerequisites | Automatic tax depends on external assignments and opaque IDs must not be fabricated | Complete or correct the external setup, then use the automatic-tax UI handoff | Verified legal-entity and balancing-segment-value scope |
| slop_aliases | Symmetric primary aliases | Yes | Before preview and after re-export | Verify | Scoped rows in both 133-column primary aliases | verify_primary_options_alias_parity | One logical options row must remain semantically identical in both aliases | Correct alias divergence before approval | Row counts, common-field diff, alias-only preservation result |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact current value and evidence already satisfy the rule | Continue without changing the value |
| Lookup | A documented read-only Fusion resolver can obtain and verify the authoritative value | Yes, read-only lookup only |
| Verify | A local export or package must be matched or compared | Yes, local verification only |
| Blocked | A required input, exact identity, semantic predicate, package, or privilege is missing | No; correct the blocker before preview |
| UI handoff | Baseline CSV authoring is supported but the requested optional customization is outside safe direct CSV scope | No direct customization; complete the named UI task and re-export |
| Not required | A conditional period, tax, or optional-family dependency was not triggered | Continue without asking a baseline question; method still follows the controlled Standard Accrual policy for a new FSCR-created ledger |

## Scoped Export Request Contract

The request property order is part of this task-specific scope contract. Build
and serialize the payload in this exact order: `TaskCode`,
`SetupTaskCSVExportCriteria`, then `SetupTaskCSVExportProcess`. Reject the
preview before export if `SetupTaskCSVExportProcess` precedes
`SetupTaskCSVExportCriteria`; Fusion may otherwise complete an overbroad export
that does not preserve the resolved primary-ledger scope.

| Request Field | Required Value | Derivation |
|---|---|---|
| TaskCode | GL_SPECIFY_LEDGER_OPTIONS | Exact setup-task code for Specify Ledger Options |
| SetupTaskCSVExportCriteria.TaskCode | GL_SPECIFY_LEDGER_OPTIONS | Must equal the parent TaskCode |
| SetupTaskCSVExportCriteria.BusinessObjectCode | GL_PRIMARY_LEDGER | Primary-ledger scope business object |
| SetupTaskCSVExportCriteria.AttributeSet | Set1 | Exact task scope attribute set |
| SetupTaskCSVExportCriteria.AttributeName | PRIMARY_LEDGER_ID | Exact primary-ledger scope attribute |
| SetupTaskCSVExportCriteria.AttributeValue | Resolved PrimaryLedgerId rendered as a string | Output of resolve_primary_ledger_scope_exact; never use a ledger name or secondary LedgerId |
| SetupTaskCSVExportProcess.TaskCode | GL_SPECIFY_LEDGER_OPTIONS | Must equal the parent TaskCode |

The shared task-level exporter constructs the request object from this contract. Criteria are valid only for a populated task-data export; template-only mode is a preflight error. A live export creates a Fusion process and follows the shared export workflow's process monitoring and persistence rules.

## Missing Combination FBDI Handoff Contract

| Item | Required Contract |
|---|---|
| Owning setup task | GL_MANAGE_ACCOUNT_COMBINATIONS, Manage Account Combinations, Financial Reporting Structures |
| Import route | core.data-loader using the current Import Account Combinations FBDI template and UCM account fin/generalLedger/import; this is not an FSM setup-task CSV import because the catalog CSV export/import flags for GL_MANAGE_ACCOUNT_COMBINATIONS are N |
| Interface member | GL_BULK_COMBINATIONS_INT in the generated FBDI ZIP; preserve the current template column order and control-file contract |
| Exact row identity | STRUCTURE_INSTANCE_CODE from the resolved COA, plus SEGMENT1 through SEGMENTn populated in physical COA order; leave unused trailing segment columns blank |
| Create attributes | ENABLED_FLAG Y and DETAIL_POSTING_ALLOWED_FLAG Y for the reviewed retained-earnings create intent; populate START_DATE_ACTIVE only from explicit effective-date intent or the reviewed workflow default. Preserve optional end date, alternate account, DFF, and PRESERVE_FLAG as blank unless explicitly requested and validated |
| Service-owned or internal fields | Do not supply CODE_COMBINATION_ID, CONCAT_SEGS, STATUS, ERROR_MESSAGE, REQUEST_ID, or LOAD_REQUEST_ID as business input; use the current template's generated group and row mechanics |
| Validation | Validate the immutable ZIP through core.data-loader and the task handoff, including exact COA, segment count/order, current template, UCM route, and duplicate prevention |
| Approval and execution | Present the Data Loader immutable preview and use its single authoritative approval workflow before upload or initiation. Run Load Interface File for Import with Import Account Combinations, then Import Account Combinations, and require terminal success |
| Resume proof | Re-run resolve_retained_earnings_account and require exactly one full-vector enabled/effective AccountType O, DetailPostingAllowedFlag Y, SummaryFlag N row and its returned _CODE_COMBINATION_ID before rebuilding the Specify Ledger Options preview |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SLOP.CHECK_DEPENDENCIES | decision | 30 | resolve_dependency | ready->SLOP.APPLY_DEFAULTS;blocked->SLOP.HANDLE_ERROR | SLOP.RESOLVE_REFERENCES | stop | After scoped reference resolution and before deriving the proposed options-row delta. |

# Specify Ledger Options Secondary-Ledger Design Enforcement

The safe baseline completes mandatory secondary ledger options while preserving conversion-specific inheritance. Optional families are opt-in and may require Oracle UI completion; no unsupported option is promoted to baseline intake.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Resolve exact secondary and parent scope | Prove one secondary belongs to one authoritative primary, then acquire a fresh populated GL_SPECIFY_LEDGER_OPTIONS export scoped by that parent's PrimaryLedgerId and reconcile both physical aliases. |
| 2 | Confirm mandatory choices | Obtain explicit confirmation for First Opened Period, future-enterable count, and Retained Earnings Account. |
| 3 | Validate conversion-specific policy | Preserve controlled Standard Accrual, resolve the controlled English journal-description-language default, and enforce any separate SLA readiness required for Subledger. |
| 4 | Evaluate opt-in features | Ask only for explicitly requested families and validate every triggered dependency or create a UI handoff. |
| 5 | Build symmetric smallest delta | Update only the exact SECONDARY row in both aliases; preserve every other member and row. |
| 6 | Preview, approve, import, verify | Bind approval to the exact diff, monitor once, and prove results by identical-scope re-export. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Always | Error | acquire_primary_scoped_options_export | Ledger is not exactly one SECONDARY; its parent PRIMARY is missing or ambiguous; StructureInstanceNumber disagrees with the secondary ledger chart identifier; export criteria use SecondaryLedgerId or anything other than GL_PRIMARY_LEDGER and PRIMARY_LEDGER_ID; or alias rows disagree | Resolve the exact relationship first and reacquire the fresh populated export using the parent PrimaryLedgerId | No |
| Always | Error | resolve_first_open_period | FirstLedgerPeriodName is unconfirmed, absent, ambiguous, or outside the secondary period set and type | Select and explicitly confirm one exact eligible period | Yes, by user input |
| Always | Error |  | FutureEnterablePeriodsLimit is unconfirmed or outside integer range 0 through 999 | Supply and explicitly confirm the count | Yes, by user input |
| Always | Error | resolve_ledger_role_account | Retained earnings is unconfirmed; account shape does not match the resolved secondary COA; accountCombinationsLOV is not scoped by StructureInstanceNumber, includes a fields projection, or is incompletely paged; dynamic-key mapping is incomplete/colliding; zero or many full-vector matches result; or EnabledFlag, effectivity, AccountType O, DetailPostingAllowedFlag Y, or SummaryFlag N fails | Do not trigger a retained-earnings export. Correct the account or response-contract gap. For zero exact eligible rows, pause for the separately previewed and approved GL_MANAGE_ACCOUNT_COMBINATIONS Import Account Combinations FBDI workflow, then re-query before a fresh options preview | Yes, by corrected input or routed FBDI creation |
| Every retained-earnings delta | Error | resolve_ledger_role_account | `RetEarnCcidSegments` contains a CodeCombinationId, hyphen display, literal escape, CRLF, wrong slot count, missing terminal LF, reordered segment, or alias-divergent bytes | Rebuild the quoted 30-slot actual-LF-delimited and LF-terminated vector from authoritative ordered segments under the validated 133-column contract | Yes, before approval |
| Newly FSCR-created secondary options at any conversion level | Error | resolve_accounting_method_evidence | Either alias lacks STANDARD_ACCRUAL and S, language is blank/not the authoritative enabled code for the controlled English default, or an alternative tuple is proposed directly | Restore Standard Accrual code/type and resolve English through languagesLOV into both aliases; write EN only if returned by Fusion | Yes, before approval |
| Conversion level is Subledger | Error | resolve_accounting_method_evidence | Applicable SLA readiness is absent after the controlled method tuple is present | Complete required SLA setup without changing the FSCR method policy | Yes, by authoritative input |
| User explicitly requests another accounting method | Warning | resolve_accounting_method_evidence | The manual post-create handoff is absent or the alternative tuple is directly authored | Keep Standard Accrual, record the exact desired method, then require manual UI change and re-export | No direct alternative-method fix |
| A posting-account family is explicitly requested | Error | resolve_ledger_role_account | Account is disabled or ineffective, DetailPostingAllowedFlag is not Y, SummaryFlag is not N, COA or full segment vector is wrong, dynamic-key mapping is incomplete/colliding, or a family-defined AccountType is wrong | Select a role-valid posting account | Yes, by user input |
| Average balances is explicitly requested | Error | resolve_ledger_role_account | Net income account fails enabled/effective, DetailPostingAllowedFlag N, SummaryFlag N, or family-defined AccountType checks; separately authoritative balance-enabled evidence is absent; or required Transaction Calendar is absent | Complete exact average-balance dependencies or use UI handoff; do not infer BalanceEnabledFlag from this LOV | Yes, by reviewed design |
| Automatic reversal remains baseline | Error |  | Reversal Criteria Set is made mandatory only because AutorevAfterOpenPrdFlag is Y | Keep criteria blank unless custom criteria was explicitly requested | Yes, before approval |
| Automatic tax is explicitly requested | Error | read_legal_entity_bsv_export | Legal entity or BSV prerequisite is absent, an internal ID is invented, or unsupported tax defaults are synthesized | Complete dependencies in their owning task or use UI handoff | No direct fix here |
| Posting cutoff is explicitly requested | Error before Review and Submit |  | Direct CSV enables cutoff without exact timezone contract, or assumes UTC | Keep N and blanks in baseline, configure in UI, re-export, and revalidate | No direct fix here |
| Optional family is not explicitly requested | Error | read_secondary_options_export | Baseline asks for, enables, or overwrites the family | Preserve existing export or controlled disabled baseline | Yes, before approval |
| Inherited field is present | Error | read_secondary_options_export | SequencingModeCode, SingleCurrencyJournalFlag, BalanceMjeByCurrencyFlag, or another inherited value is overwritten without a supported override | Restore exact export value | Yes, before approval |
| Package delta is prepared | Error | acquire_primary_scoped_options_export | Any root, relationship, journal rule, BSV, mapping, unrelated ledger, header, order, or manifest business contract changes | Rebuild the smallest secondary-row-only symmetric delta from the parent-primary-scoped populated carrier | Yes, before approval |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_secondary_primary_parent | Before export | Exact parent PrimaryLedgerId and authoritative relationship evidence for the target secondary | ora_reference_lookups.md |
| acquire_primary_scoped_options_export | Before any options-row read or edit | Exact populated parent-primary export criterion, scoped package identity, members, aliases, headers, and metadata | ora_reference_lookups.md |
| resolve_secondary_ledger_scope | Always | Exact secondary, source primary, category, StructureInstanceCode, StructureInstanceNumber, and accounting dimensions | ora_reference_lookups.md |
| read_secondary_options_export | Always | Both aliases, conversion level, existing options, inheritance, and preserved values | ora_reference_lookups.md |
| resolve_first_open_period | Always | Exact eligible period identity and secondary period context | ora_reference_lookups.md |
| resolve_ledger_role_account | Retained earnings and every explicitly triggered account role | Exact combination, COA, effectiveness, DetailPostingAllowedFlag, SummaryFlag, and applicable AccountType; BalanceEnabledFlag is unavailable and must not be inferred | ora_reference_lookups.md |
| resolve_accounting_method_evidence | Every newly FSCR-created secondary-options flow | Controlled Standard Accrual tuple, optional requested-alternative receipt, and UI-handoff-required flag | ora_reference_lookups.md |
| read_legal_entity_bsv_export | Automatic tax intent | Existing legal entity and effective BSV assignment | ora_reference_lookups.md |

## Preview and Verification Contract

| Gate | Required Evidence |
|---|---|
| Preview identity | Environment, release, exact task context, source primary, secondary, conversion level, and current alias identity. |
| Mandatory confirmations | Proposed and explicitly confirmed FirstLedgerPeriodName, FutureEnterablePeriodsLimit, and RetEarnCcidSegments. |
| Package diff | Exact changed members, row adds or updates or deletes, symmetric alias field deltas, field source class, warnings, and UI handoffs. For account vectors show business display and role evidence separately from a safe serialization summary: segment count, 30-slot count, actual-LF and terminal-LF checks, and alias parity; do not flatten the field. Checksums are runtime evidence only, never reusable defaults. |
| Approval | Explicit accountable approval bound to the exact preview fingerprint; any material change invalidates it. |
| Import | One submission by the authorized task CSV executor; the Task Node graph itself supplies no write authority. |
| Monitoring | External process or object identity, last status, elapsed wait, sanitized errors, and safe resume stage. |
| Re-export | Re-run the same parent PRIMARY_LEDGER_ID-scoped export and prove mandatory values, alias equality, preserved inheritance and optional families, unchanged relationships and rules, generated service fields, and expected in-process status. Manifest-only change is insufficient. |
| Verification export isolation | Treat the post-import export as verification proof only and never as the carrier for the already-approved import. If Fusion ignores the parent scope, stage the unfiltered package only in transient untracked storage, exact-filter the selected secondary plus its exact primary-parent and relationship rows, persist only the filtered comparison, and discard the unfiltered package and every unrelated row. Never reuse the unfiltered package as design input or an import carrier. Fail closed on identity, parent linkage, cardinality, or alias ambiguity; compare semantic parity and classify service-generated differences without copying them into the immutable candidate. |

## UI and Lifecycle Handoffs

| Boundary | Required Handoff |
|---|---|
| Unsupported optional family | Import the supported baseline, configure the explicit feature in Specify Ledger Options UI, re-export identical scope, and revalidate before Review and Submit. |
| Posting cutoff | Keep PostingCutoffFlag N and timezone and date blank in CSV; configure the exact timezone in UI. |
| Intercompany, budgetary control, approval, reconciliation, or external SLA policy | Complete the feature in its owning setup or UI and re-export. |
| Accounting method other than Standard Accrual | Keep the FSCR-authored Standard Accrual tuple, change the desired method manually in this secondary-ledger options context, and re-export before Review and Submit. |
| Custom reversal criteria | Use the UI unless a separately reviewed exact same-role CSV contract exists; AutoReverse Y alone is not a trigger. |
| Mapping or relationship changes | Use Complete Primary to Secondary Ledger Mapping; this task must not mutate relationship or rules. |
| Review and Submit | Stop at read-only readiness. Do not activate, submit, enable conversion, or open periods. |

## Boundary Register

| Boundary ID | Status | Effect in This Task |
|---|---|---|
| TBD-GL-01 | Open; outside the FSCR create path | FSCR authors Standard Accrual only. A different requested method is completed manually here and verified by re-export, so the missing arbitrary-method resolver does not block ledger creation. |
| TBD-GL-07 | Open | Review and Submit has no separately reviewed writable contract; this task stops before any submission or activation mutation. |
| GL-03 | Closed | Reporting-level physical shapes are documented and do not alter this secondary-options scope. |
| GL-09 | Closed | Optional families are opt-in, preserved on edit, disabled for matching new baseline, and otherwise handed to UI. |
| GL-12 | Closed | Posting cutoff uses disabled CSV baseline and UI configuration with re-export. |
| GL-13 | Closed | Controlled journal-rule scope is documented; this task preserves all relationship rules and custom intent remains a mapping-UI handoff. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SLOS-050-ENFORCE-DESIGN | decision | 50 | design_enforcement | ready->SLOS-060-EXECUTION-GATE;blocked->SLOS-070-HANDLE-ERROR | SLOS-040-APPLY-DEFAULTS | stop | Always |

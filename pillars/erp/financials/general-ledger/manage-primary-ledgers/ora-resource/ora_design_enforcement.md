# Manage Primary Ledgers Design Enforcement

## Lifecycle Position and Outcome

| Topic | Contract |
|---|---|
| Lifecycle position | Establishes and verifies the primary-ledger shell after prerequisite chart of accounts, calendar, and currency exist. Primary Specify Ledger Options may consume retained-earnings or other option receipts only after this task reaches terminal import success and identical-scope re-export verification |
| Business outcome | One new primary-ledger root and one logical PRIMARY detail row exist in the validated GL setup package without activating the accounting configuration |
| Design advisory | Confirm enterprise accounting intent, reporting currency, calendar-period model, and chart-of-accounts segment roles; do not ask a baseline accounting-method or optional ledger-option question |
| Supported baseline | New primary-ledger shell with exact mandatory business inputs, optional description, and the controlled Standard Accrual tuple STANDARD_ACCRUAL, S, blank language. A different desired method is a post-create manual Specify Ledger Options handoff |
| Excluded mutation | No ledger options save, relationship creation, conversion-rule creation, balancing-value conversion, activation, submission, conversion enablement, or period opening |

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm exact task scope | Require GL_MANAGE_PRIMARY_LEDGERS and one primary-ledger create request in the selected environment and release |
| 2 | Block duplicates first | Complete the exact fully paginated ledgersLOV check. Any exact match ends the create path before a CoA or template export is submitted |
| 3 | Resolve base references | Resolve exactly one enabled chart of accounts, one ACCOUNTING calendar by UserPeriodSetName with complete periods, and one active monetary currency |
| 4 | Resolve CoA semantic roles | Reuse a qualifying current populated GL_MANAGE_CHARTS_OF_ACCOUNTS_STRUCTURE_INSTANCES export or, after exact export-operation disclosure and explicit approval, route exactly one new populated export. Apply the exact four-member joins and resolve one balancing role plus zero or one management role |
| 5 | Enforce controlled method | Apply the developer-approved Standard Accrual tuple without asking for technical method fields; preserve a different desired method only as a dependent manual-change receipt |
| 6 | Acquire the task template | After all prior gates pass, present the exact environment, task, template-only mode, and purpose; obtain explicit export-operation approval; then route exactly one GL_MANAGE_PRIMARY_LEDGERS export for the current authoring attempt. Reconcile an already accepted current-attempt request before any resubmission |
| 7 | Enforce template shape | Require the ten header-only CSV members, ASM_SETUP_CSV_METADATA.xml, exact member names, headers, column order, both 133-column aliases, metadata, and safe serialization |
| 8 | Enforce smallest delta | Add one GL_LEDGER root, one ORA_GL_PRIMARY_LEDGER_CONFIG root, and the same logical PRIMARY row to both aliases; leave every other member header-only |
| 9 | Preview and approval | Produce a semantic member and field preview with export and resolver receipts, bind explicit approval to the exact immutable package fingerprint, and invalidate approval on any byte or meaning change |
| 10 | Import once | Route one approved package through core.data-loader and never automatically replay an accepted, failed, timed-out, or uncertain submission |
| 11 | Verify | Monitor to terminal status and re-export identical scope to verify generated fields, alias parity, business values, and absence of unintended changes |
| 12 | Release dependent receipts | Only after verified success, release retained earnings, First Opened Period, non-Standard method, and other option receipts to the owning primary Specify Ledger Options workflow |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Creating a primary ledger | Error | find_primary_ledger_name_conflict | Name is missing, longer than 30 characters, or conflicts exactly in the broader ledger namespace | Obtain a valid exact unique name from the user | Yes, before preview |
| Resolving the chart of accounts | Error | resolve_chart_of_accounts_exact | Chart of accounts is missing, ambiguous, or disabled, or its exact StructureInstanceCode is absent | Select one exact enabled chart of accounts before searching for reusable role evidence | Yes, before export acquisition |
| Resolving chart-of-accounts semantic roles | Error | derive_chart_of_accounts_roles | No current populated GL_MANAGE_CHARTS_OF_ACCOUNTS_STRUCTURE_INSTANCES export contains the exact selected StructureInstanceCode, and one cannot be acquired; or the exact composite-key joins do not yield one GL_BALANCING role and zero or one GL_MANAGEMENT role with nonblank ColumnName and instance ValueSetCode | Reuse one qualifying export or route one new populated task export, and correct the exact member, key, cardinality, column, or instance-value-set defect | Yes, before preview |
| Creating a primary ledger | Error | resolve_accounting_calendar_exact | Calendar is missing, ambiguous, disabled, or not type ACCOUNTING | Select one exact enabled accounting calendar | Yes, before preview |
| Preparing the period handoff | Error | list_eligible_accounting_periods | The complete exact eligible-period set is unavailable, has partial pagination, or lacks an explicit or independently authoritative physical FirstLedgerPeriodName | Refresh the periods lookup, preserve adjustment periods, and obtain an authoritative physical selection; do not use response order | Yes, before preview |
| Creating a primary ledger | Error | resolve_monetary_currency_exact | Currency is missing, ambiguous, inactive, disabled, or nonmonetary | Select one exact active monetary currency | Yes, before preview |
| Creating a primary ledger | Error | resolve_accounting_method_evidence | Either PRIMARY alias does not contain STANDARD_ACCRUAL, S, and blank language, or a user-supplied alternative tuple is proposed for direct creation | Rebuild both aliases with the controlled Standard Accrual tuple | Yes, before preview |
| User explicitly requests another accounting method | Warning | resolve_accounting_method_evidence | The desired method is directly authored during creation or the required post-create manual-change handoff is not recorded | Create and verify the ledger as Standard Accrual, then instruct the user to change the method manually in Specify Ledger Options and re-export the same scope | No direct alternative-method fix in FSCR |
| Authoring the PRIMARY logical row | Error | verify_primary_alias_parity | Either 133-column alias is missing the row, has a duplicate, or common fields differ | Apply the same semantic PRIMARY row to GL_PRIMARY_LEDGER.csv and GL_SECONDARY_LEDGER.csv | Yes, before preview |
| Acquiring the populated CoA export | Error | derive_chart_of_accounts_roles | A second POST is proposed while a prior GL_MANAGE_CHARTS_OF_ACCOUNTS_STRUCTURE_INSTANCES export may have been accepted, is still polling, or already produced a result | Reconcile the process identifier, persisted artifact, and terminal status first; submit a new export only when the routed workflow proves no accepted request exists and no qualifying artifact is available | Yes, before another CoA export |
| Acquiring the Primary Ledger template | Error | select_validated_general_ledger_package | A second POST is proposed while a prior template-only GL_MANAGE_PRIMARY_LEDGERS export may have been accepted, is still polling, or already produced a result | Reconcile the process identifier, persisted artifact, and terminal status first; submit a new export only when the routed workflow proves no accepted request exists and the current-attempt template is absent | Yes, before another template export |
| Authoring package members | Error | select_validated_general_ledger_package | The candidate is populated rather than template-only, or header, order, alias, manifest, serialization, or nonowning members would change outside the four-row delta | Rebase on the exact current template-only package and preserve the physical shape | Yes, before preview |
| Serializing any intentional blank | Error | select_validated_general_ledger_package | A blank-designated cell contains whitespace, a control character, escaped control text such as `\\n`, or a textual null sentinel such as `null` or `None` | Rebuild the candidate so the cell is a true zero-character CSV field, then regenerate the package and preview fingerprints | Yes, before preview; any package change requires fresh approval |
| A retained-earnings account or any optional ledger option is supplied | Warning |  | This task would resolve, validate, create, or serialize the account or option before primary-shell verification | Preserve the exact business statement as a non-CSV dependent-task receipt and leave its fields blank; release it only after verified primary-ledger creation | No in this task |
| Review and Submit is requested | Error |  | This task would author lifecycle state or submit or activate the configuration | Stop at verified package state; TBD-GL-07 keeps Review and Submit mutation blocked | No |

## EO and Bean-Equivalent Rules

| Rule Family | Equivalent Enforcement |
|---|---|
| Required-attribute validation | Name, chart of accounts, accounting calendar, and currency are nonnull user choices; accounting method is always populated by the controlled FSCR create policy |
| Length validation | Name is at most 30 characters and optional Description is at most 240 characters before any resolver or package mutation |
| Namespace validation | A successful fully paginated authoritative read must return zero exact conflicts before either export role or package preparation begins |
| Chart validation | One enabled chart of accounts and one current populated exact structure-instance export are required. Qualified-label assignment identifies role SegmentCode, structure-segment supplies ColumnName, and structure-instance-segment supplies ValueSetCode; physical position and instance value sets are never inferred |
| Calendar validation | One exact ACCOUNTING calendar is required; accountingCalendarsLOV has no EnabledFlag. PeriodSetName and PeriodType are resolver outputs, PeriodType maps to AccountedPeriodType, and the complete period set retains adjustment periods |
| Currency validation | One exact enabled currently active monetary currency with CurrencyFlag Y is required |
| Method validation | Every new FSCR-created primary row uses STANDARD_ACCRUAL, S, and blank language in both aliases. An alternative display name is desired-state evidence for a later manual UI change, not a create-time tuple |
| Alias validation | Both 133-column aliases contain exactly one proposed PRIMARY logical row with equal common fields and preserved alias-only columns |
| Service ownership | ShortName, IDs, audit, process, status, and lifecycle fields are not copied from another ledger and remain service-owned where generation is supported |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| select_validated_general_ledger_package | Before reading or changing any package member | Validated package identity, member shape, aliases, headers, metadata | ora_reference_lookups.md |
| find_primary_ledger_name_conflict | Every create request | Name availability in the broader ledger namespace | ora_reference_lookups.md |
| resolve_chart_of_accounts_exact | Every create request | Exact chart-of-accounts identity and structure instance | ora_reference_lookups.md |
| derive_chart_of_accounts_roles | Every create request | Exact COA export receipt plus GL flexfield identity and balancing and management segment role outputs | ora_reference_lookups.md |
| resolve_accounting_calendar_exact | Every create request | AccountingCalendarName and UserPeriodSetName, CalendarId, PeriodSetName, AccountedPeriodType from PeriodType | ora_reference_lookups.md |
| list_eligible_accounting_periods | Every create request | Explicit or independently authoritative physical FirstLedgerPeriodName validated against EnteredPeriodName, plus complete EligibleAccountingPeriods for downstream options readiness | ora_reference_lookups.md |
| resolve_monetary_currency_exact | Every create request | Exact CurrencyCode | ora_reference_lookups.md |
| resolve_accounting_method_evidence | Every new FSCR-created primary ledger | Controlled Standard Accrual tuple, optional requested alternative receipt, and UI-handoff-required flag | ora_reference_lookups.md |
| verify_primary_alias_parity | Before preview and after re-export | Row cardinality and semantic alias diff | ora_reference_lookups.md |

## Package Member Impact

| Package Member | Population Behavior |
|---|---|
| GL_LEDGER.csv | Add exactly one selected primary-ledger root row; populate user, resolver, controlled, intentional-blank, and service-owned fields by class; preserve every unrelated row |
| ORA_GL_PRIMARY_LEDGER_CONFIG.csv | Add the matching primary-configuration root row using the same exact business identity; preserve every unrelated row |
| GL_PRIMARY_LEDGER.csv | Add exactly one PRIMARY logical detail row using the exported 133-column header and serialization contract |
| GL_SECONDARY_LEDGER.csv | Add the same PRIMARY logical detail row under the second exported 133-column alias; preserve every unrelated row |
| ORA_GL_JOURNAL_CONFIG_DETAIL.csv | Preserve dependency-closure workflow rows; do not synthesize SetupStep, NextAction, Status, legal-entity, timezone, tax, or audit receipts |
| ORA_LEGAL_ENTITY_BAL_SEG_VAL_DEF.csv | Preserve header and all rows; do not invent automatic-tax legal-entity associations |
| GL_LEDGER_SEG_VAL_ASSIGNMENT.csv | Preserve header and all rows; do not create balancing-value assignments |
| ORA_GL_LEDGER_RELATIONSHIP.csv | Preserve header and all rows; do not create a primary-secondary relationship |
| ORA_GL_JOUNAL_CONVERSION_RULES.csv | Preserve the product-spelled member name, header, and all rows; do not create journal conversion rules |
| ORA_PRIMARY_BALANCING_SEGMENT_VALUE_CONVERSION_RULES.csv | Preserve header and all rows; do not create balancing-value conversion or replication rules |
| ASM_SETUP_CSV_METADATA.xml | Preserve exact metadata structure and update only through the authorized package workflow; never hand-invent or omit the manifest |

## Field Population Contract

| Field Family | Owning Members | Population Behavior |
|---|---|---|
| Ledger business identity | GL_LEDGER.csv, ORA_GL_PRIMARY_LEDGER_CONFIG.csv, both PRIMARY aliases | Populate exact user Name and optional Description consistently; never silently normalize or derive the name |
| Chart of accounts | Root rows and both PRIMARY aliases where their exported headers define the fields | Populate authoritative chart identity and structure instance. Use the GL_BALANCING label's exact SegmentCode to source BalSegColumnName from the structure-segment member and BalSegValueSetCode from the structure-instance-segment member. Apply the same mapping for the optional single GL_MANAGEMENT role; when absent, keep both management fields truly blank. Never use SequenceNumber or DefaultValueSetCode as substitutes |
| Calendar | Root rows and both PRIMARY aliases where defined | Copy UserPeriodSetName, PeriodSetName, and AccountedPeriodType from the exact calendar resolution; populate physical FirstLedgerPeriodName only from explicit input or independently authoritative same-role export evidence after EnteredPeriodName/PeriodType validation. Never use the first LOV row or label sorting; pass the full eligible set downstream |
| Options-task First Opened Period | No Manage Primary Ledgers member | Keep the user-selected opening period in the dependency handoff only. It must not override or populate the physical FirstLedgerPeriodName in the primary-shell create package, even when both values use the same CSV header in different lifecycle contexts |
| Currency | Root rows and both PRIMARY aliases where defined | Populate the exact resolved monetary CurrencyCode |
| Accounting method | Both PRIMARY aliases where defined | Always populate SlaAccountingMethodCode STANDARD_ACCRUAL, SlaAccountingMethodType S, and blank SlaDescriptionLanguage for a new FSCR-created ledger. Preserve a different requested display name only in the handoff record; never place its tuple in the create package |
| Ledger role and controlled constants | Root rows and both PRIMARY aliases where defined | Apply only same-release matching-role constants documented in ora_defaulting_rules.md |
| Primary ledger options | Both PRIMARY aliases | Leave unrequested option accounts and option-specific values blank or at the proven disabled baseline for the subsequent options task |
| Disabled posting cutoff | Both PRIMARY aliases where defined | Populate PostingCutoffFlag as N and serialize PostingCutoffTimezoneCode and PostingCutoffDate as true empty CSV fields. Never write whitespace, an actual or escaped line break such as `\\n`, or a textual null sentinel |
| Short name, numeric IDs, audit, process, and lifecycle state | Every owning member where defined | Leave blank on create only when service generation is supported; never copy another ledger's values; verify generated results by re-export |
| Alias-only and unknown exported columns | Each PRIMARY alias | Preserve header-defined values from the validated baseline; do not synthesize an undocumented mapping |

## Package Workflow Gates

| Gate | Required Evidence |
|---|---|
| Duplicate preflight | Exact ledger Name, complete ledgersLOV pagination, zero exact matches, environment identity, and lookup receipt. Failure or ambiguity is not availability |
| CoA role export acquisition | Exact selected StructureInstanceCode, searched export inventory, qualifying reuse decision or exact operation disclosure and approval bound to one routed GL_MANAGE_CHARTS_OF_ACCOUNTS_STRUCTURE_INSTANCES populated export, ProcessId, terminal status, package metadata, seven CSV members, and populated selected-instance rows |
| CoA role derivation | One selected instance row, exact composite joins across the four owning CSV members, one GL_BALANCING assignment, zero or one GL_MANAGEMENT assignment, exact ColumnName and instance ValueSetCode for every role, and blocker details for any discarded candidate |
| Primary template acquisition | Exact environment, GL_MANAGE_PRIMARY_LEDGERS, template-only mode, purpose, explicit export-operation approval, one current-attempt export receipt, ProcessId, terminal status, selected artifact, release, and proof that any earlier accepted same-attempt request was reconciled rather than duplicated |
| Task-manifest identity | The package metadata must prove the exact GL_MANAGE_PRIMARY_LEDGERS task identity and task-level template provenance. A functional-area or offering package is not relevant merely because it contains similarly named members |
| Shape validation | Exact ten header-only CSV members plus ASM_SETUP_CSV_METADATA.xml, exact case-sensitive names, headers, column order, both 133-column aliases, metadata, and serialization |
| Four-row delta | Exactly one added row in GL_LEDGER.csv, ORA_GL_PRIMARY_LEDGER_CONFIG.csv, GL_PRIMARY_LEDGER.csv, and GL_SECONDARY_LEDGER.csv; zero added, updated, or deleted rows in all other CSV members |
| Blank serialization validation | Parse every authored CSV member and prove each intentional blank has zero characters; reject whitespace, control characters, escaped control text, and textual null sentinels before preview |
| Preview | Environment, release, exact task, selected CoA data-export receipt, selected Primary template-export receipt, member checksums, row adds, updates and deletes, field-level old and new values, exact CoA join evidence, population class, intentional blanks, service-owned fields, warnings, dependent-task receipts, and open TBD scope; no credential or token material |
| Approval | Explicit accountable approval bound to the exact preview fingerprint, selected environment, release, scope, and package artifact; any material change invalidates it |
| Import | One authorized core.data-loader submission after approval; capture task code and sanitized process or request identity; never automatically replay |
| Monitoring | Poll to a terminal state with bounded elapsed time; on timeout disclose last status and safe next-check path; on failure retrieve and persist available ProcessLog and status evidence |
| Re-export verification | Export identical scope and compare semantic business values, alias parity, generated IDs and short name, defaults, row counts, relationships, rules, and unintended changes; metadata-only change is not proof |
| Verification export isolation | If Fusion cannot filter the populated identical-task export at source, download it only to transient untracked storage, exact-filter the new ledger and its parent-linked rows there, persist only that filtered evidence, and discard the unfiltered package and all unrelated rows. Fail closed on identity, linkage, cardinality, or alias ambiguity; never reuse verification data as design input or a default source |

## TBD and UI Boundary Register

| Item | State | Runtime Consequence |
|---|---|---|
| TBD-GL-01 arbitrary accounting-method resolver | Open; outside the FSCR create path | FSCR does not directly author arbitrary accounting methods. Every new ledger is created with Standard Accrual; a different requested method becomes a named post-create Specify Ledger Options UI handoff and must be verified by re-export before Review and Submit |
| TBD-GL-07 writable Review and Submit contract | Open | Always blocks this task from submission, activation, conversion enablement, period opening, or lifecycle-state authoring |
| GL-03 reporting-ledger package shapes | Closed | Documented package shapes resolve the reporting-shape question; no environment-specific experiment identity is reused here |
| GL-09 optional ledger-option scope | Closed | Optional families are opt-in and are not baseline questions in this task |
| GL-12 posting-cutoff authoring | Closed by baseline and UI handoff | Disabled baseline is supported; enabled customization belongs to the named UI flow and requires re-export |
| GL-13 journal conversion rules | Closed by supported scope and UI handoff | This task creates no relationship or conversion rules; supported rule scope is owned downstream |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPL.ENFORCE_DESIGN | decision | 50 | design_enforcement | pass->MPL.EXECUTION_GATE;blocked->MPL.HANDLE_ERROR | MPL.APPLY_DEFAULTS | stop | Before presenting a package preview or requesting import approval. |

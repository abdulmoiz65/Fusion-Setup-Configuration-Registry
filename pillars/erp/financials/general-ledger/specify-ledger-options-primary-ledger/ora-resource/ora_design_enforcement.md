# Specify Ledger Options Primary-Ledger Design Enforcement

## Lifecycle Position and Outcome

| Topic | Contract |
|---|---|
| Lifecycle position | Configures the owning PRIMARY detail row after Manage Primary Ledgers establishes the shell and before secondary-ledger setup, primary-secondary mapping, and Review and Submit readiness |
| Business outcome | The selected primary's mandatory retained-earnings option and only the explicitly requested supported options are verified in both PRIMARY aliases without submitting or activating the accounting configuration |
| Design advisory | Confirm operational readiness, account-role design, method intent, and explicit opt-in families; keep the conversation focused on triggered choices rather than presenting every optional family as a questionnaire |
| Supported CSV baseline | Controlled basic save centered on RetEarnCcidSegments, optional first period and future-period override when triggered, evidence-backed method fields, preserved existing fields, and matching disabled defaults |
| Excluded mutation | No submission, activation, conversion enablement, period opening, relationship authoring, secondary authoring, or unsafe optional-family customization |

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm primary context and acquire the carrier | Resolve exactly one PRIMARY ledger, build the GL_PRIMARY_LEDGER and PRIMARY_LEDGER_ID criterion from its PrimaryLedgerId, and acquire one fresh populated GL_SPECIFY_LEDGER_OPTIONS export containing its current logical options row in both aliases |
| 2 | Enforce mandatory save fields | For a controlled new-primary save, require the exact user-selected retained-earnings account, query accountCombinationsLOV directly by StructureInstanceNumber without another export, and require one exact enabled/effective AccountType O, DetailPostingAllowedFlag Y, SummaryFlag N CCID after generic dynamic-key mapping. If absent, complete the separately approved Manage Account Combinations FBDI workflow and re-query before continuing |
| 3 | Enforce triggered decisions | Require FirstLedgerPeriodName only for operational or open readiness, method only for method-ready intent, and optional-family inputs only after explicit opt-in |
| 4 | Enforce baseline boundaries | Preserve existing values; use only same-release matching-role defaults; route unsupported optional customizations to named UI handoffs |
| 5 | Enforce package shape | Update the owning PRIMARY row symmetrically in both aliases while preserving every member, header, row, alias-only field, multiline value, and metadata contract |
| 6 | Preview and approval handoff | Show the exact semantic delta, UI handoffs, and readiness blockers; bind approval before one authorized import |
| 7 | Verify | Monitor import, re-export identical scope, and verify option values, alias parity, UI completions, and no unintended changes |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every invocation | Error | acquire_primary_scoped_options_export | Ledger is absent, ambiguous, not PRIMARY; StructureInstanceNumber disagrees with the ledger chart identifier; export criteria do not use GL_PRIMARY_LEDGER and PRIMARY_LEDGER_ID; or the populated export lacks one current symmetric options row | Correct the scope or reacquire the exact scoped populated export before changing options | Yes, before preview |
| Controlled new-primary options save | Error | resolve_retained_earnings_account | Retained earnings is missing; account shape does not match the resolved COA; accountCombinationsLOV is not scoped by StructureInstanceNumber, includes a fields projection, or is incompletely paged; dynamic-key mapping is incomplete/colliding; zero or many exact segment matches result; or EnabledFlag, effectivity, AccountType O, DetailPostingAllowedFlag Y, or SummaryFlag N fails | Do not trigger a retained-earnings export. Correct the account or response-contract gap. For zero exact eligible rows, pause for separately previewed and approved GL_MANAGE_ACCOUNT_COMBINATIONS Import Account Combinations FBDI, then re-query before a fresh options preview | Yes, by corrected input or routed FBDI creation before a fresh preview |
| Operational or open readiness | Error | resolve_first_open_period_exact | FirstLedgerPeriodName is missing or not exactly in the complete eligible set | Ask the user to choose one exact returned period; do not choose for them | Yes, before preview |
| User overrides future-enterable periods | Error |  | Value is not an integer from 0 through 999 | Correct the value; omission remains optional | Yes, before preview |
| Newly FSCR-created primary-ledger options flow | Error | resolve_accounting_method_evidence | Either PRIMARY alias does not retain STANDARD_ACCRUAL and S, SlaDescriptionLanguage is blank or not the authoritative enabled code for the controlled English default, or an alternative method tuple is proposed directly | Restore Standard Accrual code/type and resolve English through languagesLOV into both aliases; write EN only if Fusion returns EN | Yes, before preview |
| User explicitly requests another accounting method | Warning | resolve_accounting_method_evidence | The manual post-create Specify Ledger Options handoff is absent or the alternative is placed in the CSV delta | Keep Standard Accrual in FSCR, record the exact desired method, then require manual UI change and re-export | No direct alternative-method fix |
| Account-backed option family is requested | Error | resolve_optional_ledger_account_role | Account is missing, ambiguous, or fails its exact requested role predicates | Correct the account; if direct field mapping is unsupported, retain baseline and use the named UI handoff | Yes, before preview or in UI |
| Auto-reverse after open period is Y | Error |  | A criteria set is treated as mandatory even though custom criteria were not requested | Do not ask for or invent a criteria set unless custom reversal criteria are explicitly requested | Yes, before preview |
| Custom reversal criteria is requested | Error |  | Exact safe direct CSV contract is absent or CriteriaSetName is missing | Retain baseline and complete custom reversal criteria in Specify Ledger Options UI, then re-export | No direct CSV fix |
| Posting cutoff is not requested | Error |  | Baseline is not PostingCutoffFlag N with blank timezone and date for a matching new role, or existing values are overwritten | Preserve existing values or use the disabled matching-role baseline | Yes, before preview |
| Posting cutoff is requested | Error |  | PostingCutoffFlag would be Y with blank timezone, or a timezone is guessed, or unsupported direct authoring is attempted | Complete posting cutoff in Specify Ledger Options UI; PostingCutoffDate may remain blank only where the UI permits it; re-export | No direct CSV fix |
| Automatic tax is requested | Error | verify_automatic_tax_prerequisites | External legal-entity or balancing-value prerequisites are unproven, an internal ID is invented, or unsupported direct authoring is attempted | Complete prerequisite setup and Configure Automatic Tax Options in the UI; allow TaxDefaultLeTrans to remain blank when the verified UI result does | No direct CSV fix |
| Any optional family is not requested | Error |  | The workflow asks baseline questions, changes an existing value, or enables the family | Preserve existing behavior or the proven disabled baseline | Yes, before preview |
| Any UI handoff remains incomplete | Error |  | Review and Submit readiness is claimed before same-scope re-export verifies the UI change | Complete the named UI flow and re-export before readiness review | No direct CSV fix |
| Any package delta is proposed | Error | verify_primary_options_alias_parity | A nonowning member changes, an alias diverges, a row is deleted, or multiline serialization changes unexpectedly | Rebuild the smallest symmetric alias delta from a validated package | Yes, before preview |
| Review and Submit mutation is requested | Error |  | Lifecycle state, submission, activation, conversion enablement, or period opening would be authored | Stop with TBD-GL-07 and hand off to read-only Review and Submit readiness | No |

## EO and Bean-Equivalent Rules

| Rule Family | Equivalent Enforcement |
|---|---|
| Required-attribute validation | Retained earnings is nonnull for the controlled new-primary save; FirstLedgerPeriodName and method are nonnull only under their documented triggers |
| Account-combination validation | Each account must have the resolved COA segment count and physical order. Query accountCombinationsLOV with _CHART_OF_ACCOUNTS_ID equal to StructureInstanceNumber, omit fields, page until hasMore is false, and uniquely map dynamic attributes from exported SegmentCode, Name, and ColumnName without relying on tenant names or JSON order. Retained earnings requires one enabled/effective AccountType O, DetailPostingAllowedFlag Y, SummaryFlag N exact row; one such row supplies _CODE_COMBINATION_ID as identity evidence. Zero routes separately gated GL_MANAGE_ACCOUNT_COMBINATIONS FBDI and a mandatory post-success re-query. The options CSV stores the validated package-sized actual-LF-delimited, LF-terminated segment vector, not the CCID |
| Range validation | FutureEnterablePeriodsLimit is an integer from 0 through 999 |
| Method validation | A newly FSCR-created primary retains STANDARD_ACCRUAL and S. Create-time blank language is not carried through the options save: default business intent to English and resolve the unique enabled English base-language code through languagesLOV. A different requested method display name is handoff evidence only and never a directly authored tuple |
| Posting-cutoff validation | PostingCutoffFlag Y requires a supported nonblank timezone; date nullability follows the verified UI contract; no UTC assumption |
| Reversal validation | AutorevAfterOpenPrdFlag Y alone does not require a criteria set; custom criteria does |
| Tax validation | External legal-entity and balancing-value assignments must exist before automatic-tax UI completion; internal identifiers are resolver or service outputs only |
| Alias validation | Both 133-column aliases contain exactly one scoped PRIMARY row and every common field is semantically equal |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| acquire_primary_scoped_options_export | Before any package read or edit | Exact populated export criterion, scoped package identity, members, aliases, headers, metadata | ora_reference_lookups.md |
| resolve_primary_ledger_scope_exact | Every invocation | Exact PRIMARY identity and accounting dimensions | ora_reference_lookups.md |
| read_primary_options_export | Every invocation | Current options, calendar scope, method tuple, alias parity, serialization | ora_reference_lookups.md |
| resolve_retained_earnings_account | Controlled new-primary options save | RetEarnCcidSegments and all retained-earnings role predicates | ora_reference_lookups.md |
| resolve_first_open_period_exact | Operational or open readiness | Exact user-selected EnteredPeriodName matched locally within the complete PeriodSetNameId result and AccountedPeriodType | ora_reference_lookups.md |
| resolve_accounting_method_evidence | Every newly FSCR-created primary-ledger options flow | Controlled Standard Accrual tuple, optional requested-alternative receipt, and UI-handoff-required flag | ora_reference_lookups.md |
| resolve_optional_ledger_account_role | A supported account-backed family is explicitly requested | Exact account value and role-semantic evidence | ora_reference_lookups.md |
| verify_automatic_tax_prerequisites | Automatic tax is explicitly requested | Legal-entity and balancing-segment-value prerequisite evidence | ora_reference_lookups.md |
| verify_primary_options_alias_parity | Before preview and after re-export | Row cardinality and semantic alias diff | ora_reference_lookups.md |

## Package Member Impact

| Package Member | Population Behavior |
|---|---|
| GL_LEDGER.csv | Preserve header and all values; primary business identity is scope only and is not re-authored by this options task |
| ORA_GL_PRIMARY_LEDGER_CONFIG.csv | Preserve header and all values; do not recreate the primary root |
| GL_PRIMARY_LEDGER.csv | Update exactly one scoped PRIMARY row using the exported 133-column header; minimally populate RetEarnCcidSegments for the controlled basic save and only other explicitly approved supported option fields |
| GL_SECONDARY_LEDGER.csv | Update the same scoped PRIMARY logical row under the second 133-column alias; preserve every SECONDARY and unrelated row |
| ORA_GL_JOURNAL_CONFIG_DETAIL.csv | Preserve dependency-closure workflow rows; never synthesize or update SetupStep, NextAction, Status, legal-entity, timezone, tax, or audit receipts |
| ORA_LEGAL_ENTITY_BAL_SEG_VAL_DEF.csv | Preserve; automatic-tax legal-entity or balancing-value customization uses the named UI handoff unless a separately reviewed contract exists |
| GL_LEDGER_SEG_VAL_ASSIGNMENT.csv | Preserve; do not create balancing-value assignments in this task |
| ORA_GL_LEDGER_RELATIONSHIP.csv | Preserve; do not create or update a primary-secondary relationship |
| ORA_GL_JOUNAL_CONVERSION_RULES.csv | Preserve the product-spelled member name, header, and rows; do not synthesize conversion rules |
| ORA_PRIMARY_BALANCING_SEGMENT_VALUE_CONVERSION_RULES.csv | Preserve header and rows; do not author conversion or replication rules |
| ASM_SETUP_CSV_METADATA.xml | Preserve exact package metadata structure and update only through the authorized package workflow |

## Field Population Contract

| Field Family | Population Behavior |
|---|---|
| RetEarnCcidSegments | Mandatory derived physical value for the controlled new-primary options save: take the exact user-selected account's resolved segments in authoritative COA order, serialize them as one quoted 30-slot actual-LF-delimited field with empty unused slots and a terminal LF under the validated 133-column contract, and write identically to both PRIMARY aliases. Do not store the resolver's CodeCombinationId or the hyphen-delimited display string |
| FirstLedgerPeriodName | Exact user-selected eligible period only when operational or open readiness is requested; no guessed default |
| FutureEnterablePeriodsLimit | Preserve existing; accept optional user integer 0 through 999; for a matching new role only, 1 may be proposed and previewed |
| SlaAccountingMethodCode, SlaAccountingMethodType, SlaDescriptionLanguage | Preserve existing for unrelated established ledgers; for the newly FSCR-created options flow require STANDARD_ACCRUAL, S, and the exact languagesLOV code for the controlled English default until any requested alternative is completed manually and verified by re-export. Never hardcode EN or US |
| Retained-earnings, CTA, reserve, rounding, suspense, intercompany, SLA-suspense, and net-income account segment fields | Populate only the exact requested supported role output; otherwise preserve existing or intentional blank and use the relevant UI handoff |
| Optional-family flags | Preserve existing; for a matching new role use only documented disabled defaults when the family was not requested; never silently enable |
| AutorevAfterOpenPrdFlag and custom reversal criteria | A proven Y default does not imply criteria; preserve criteria unless a supported explicit custom request is completed through UI and re-exported |
| PostingCutoffFlag, PostingCutoffTimezoneCode, PostingCutoffDate | Preserve existing; matching new disabled baseline is N, blank, blank; enabled customization is UI-owned and timezone is never guessed |
| Automatic-tax fields including TaxDefaultLeTrans | Preserve existing or disabled baseline; never fabricate legal-entity identifiers; verified UI completion may legitimately re-export a blank TaxDefaultLeTrans |
| IDs, audit, status, process, lifecycle, alias-only, and undocumented fields | Preserve exact exported values; never populate from user input or another ledger |

## Optional Family UI Handoffs

| Triggered Family | Supported Baseline | Named Handoff | Verification Boundary |
|---|---|---|---|
| Suspense or SLA suspense | Preserve existing or disabled baseline; direct account only when exact supported field contract is proven | Specify Ledger Options account sections | Same-scope re-export verifies flags and account semantics |
| Rounding or entered-currency balancing | Preserve existing or disabled baseline | Specify Ledger Options balancing and rounding sections | Re-export verifies exact account fields and flags |
| Intercompany | Preserve existing or disabled baseline | Specify Ledger Options intercompany section and any prerequisite intercompany setup | Re-export verifies the selected accounts and behavior |
| Average daily balances | Preserve existing or disabled baseline | Specify Ledger Options average-balances section | Re-export verifies enabled state and net-income role where applicable |
| Budgetary control or budget journals | Preserve existing or disabled baseline | Specify Ledger Options budgetary controls and prerequisite budget setup | Re-export verifies flags and reserve-for-encumbrance role where applicable |
| Automatic tax | Preserve existing or disabled baseline | Configure Automatic Tax Options after legal-entity and balancing-value prerequisites | Re-export verifies tax flags and returned service-owned values |
| Translation | Preserve existing or disabled baseline | Specify Ledger Options translation section | Re-export verifies translation flags and CTA role where applicable |
| Sequencing | Preserve existing or N matching-role baseline | Specify Ledger Options sequencing section | Re-export verifies exact sequencing fields |
| Custom reversal criteria | Preserve current criteria or blank; AutorevAfterOpenPrdFlag Y alone is sufficient for baseline | Specify Ledger Options journal-reversal section | Re-export verifies the selected criteria set |
| Journal approval or reconciliation | Preserve existing or disabled baseline | Specify Ledger Options journal-processing sections | Re-export verifies exact flags |
| Posting cutoff | N with blank timezone and date for a matching new role | Specify Ledger Options posting-cutoff section | Re-export verifies nonblank timezone when enabled and exact returned date nullability |
| SLA cash basis or USSGL | Preserve existing or disabled baseline | Specify Ledger Options subledger-accounting sections | Re-export verifies exact flags and any dependent setup |
| Accounting method other than Standard Accrual | Keep STANDARD_ACCRUAL, S, and the resolver-derived English language code in the FSCR-authored options package | Specify Ledger Options accounting-method section after the new ledger is created and verified | Same-scope re-export verifies the manually selected method tuple and language before Review and Submit |

## Package Workflow Gates

| Gate | Required Evidence |
|---|---|
| Acquisition | Selected environment, release, exact PRIMARY ledger, resolved PrimaryLedgerId, and one fresh populated GL_SPECIFY_LEDGER_OPTIONS data export scoped with BusinessObjectCode GL_PRIMARY_LEDGER, AttributeSet Set1, AttributeName PRIMARY_LEDGER_ID, and AttributeValue equal to that PrimaryLedgerId. This scoped export is the sole current-state carrier. Template-only and project-owned create packages are not carriers. No unrelated populated row may enter the candidate |
| Shape validation | Exact ten CSV members plus ASM_SETUP_CSV_METADATA.xml, exact names, headers, order, aliases, header-only members, metadata, and unrelated rows. Parse every populated account segment vector as one quoted CSV field; require actual LF separators, terminal LF, package-derived slot count (30 for the validated 133-column contract), ordered segment round-trip, and symmetric alias bytes |
| Preview | Exact member checksums, row adds, updates and deletes, field-level old and new values, population class, role-semantic evidence, intentional blanks, preserved values, warnings, UI handoffs, and open-item scope |
| Approval | Explicit accountable approval bound to the current preview fingerprint, environment, release, primary scope, and package artifact; any change invalidates approval |
| Import | One authorized core.data-loader submission after approval; no blind replay |
| Monitoring | Terminal process state or bounded timeout with last status and safe next-check path; retrieve available ProcessLog on failure |
| Re-export verification | Identical scope semantic diff of both aliases, requested options, generated values, UI handoffs, relationships, rules, row counts, and unintended changes; metadata-only change is not proof |
| Verification export isolation | Re-run the same PRIMARY_LEDGER_ID-scoped task export after import. Treat the post-import result as verification proof only and never as the carrier for the already-approved import. If Fusion ignores the scope, stage the unfiltered package only in transient untracked storage, exact-filter the selected primary, persist only the filtered comparison, and discard the unfiltered package and every unrelated row. Fail closed on identity, cardinality, or alias ambiguity; compare semantic parity and classify service-generated differences without copying them into the immutable candidate |

## TBD and UI Boundary Register

| Item | State | Runtime Consequence |
|---|---|---|
| TBD-GL-01 arbitrary accounting-method resolver | Open; outside the FSCR create path | FSCR authors Standard Accrual only. A different requested method is completed manually in Specify Ledger Options and verified by re-export; creation is not blocked by the missing arbitrary-method resolver |
| TBD-GL-07 writable Review and Submit contract | Open | Always blocks submission, activation, conversion enablement, period opening, and lifecycle-state authoring |
| GL-03 reporting-ledger package shapes | Closed | Package-shape evidence resolves the reporting-shape question; no environment experiment identity is reused |
| GL-09 optional ledger-option scope | Closed | Every optional family is opt-in, not a baseline questionnaire |
| GL-12 posting-cutoff authoring | Closed by baseline and UI handoff | N with blank timezone and date is the matching new-role baseline; enabled customization is UI-owned and re-exported |
| GL-13 journal conversion rules | Closed by supported scope and UI handoff | This task preserves conversion-rule members and never synthesizes unsupported rules |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SLOP.ENFORCE_DESIGN | decision | 50 | design_enforcement | pass->SLOP.EXECUTION_GATE;blocked->SLOP.HANDLE_ERROR | SLOP.APPLY_DEFAULTS | stop | Before presenting the primary-options package preview or requesting import approval. |

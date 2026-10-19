# Wage Basis Rules Input Validation

## Task and Scope

Payroll Calculation Information (PAY_MANAGE_PAYROLL_DEDUCTIONS) owns this
Wage Basis Rules contract. It replaces the relevant legacy UI functionality,
not every feature of the old task. Component Group Rules continues to delegate
to Payroll Components; do not move its routing here. The generated manifest's
CSV flag does not establish a Wage Basis Rules mutation contract. Select native
Taxability Rule through core/data-loader for the operations below.

## Operation Profiles

| Operation | Supported business effect | Boundary |
|---|---|---|
| read | Review exact rules and their history | GET-only; no archive |
| create | New dated rule for each selected component/secondary combination | Native TaxabilityRule MERGE with business user keys; duplicate preflight required |
| update | Change inclusion on a new effective boundary, preserving the predecessor | Complete-identity MERGE, PURGE_FUTURE_CHANGES N; current supported shape splits the last open-ended slice |
| correct | Change inclusion in the selected existing slice without changing its dates | Complete-identity MERGE at exactly that slice's start and end, PURGE_FUTURE_CHANGES N |
| delete_record_and_history | Remove the logical rule and every historical/future slice | Complete-identity DELETE; explicit whole-history intent is mandatory |
| reconcile | Verify a previously submitted supported operation | Read-only; tied to original approved request and baseline |
| end_date | Pending future development | Tested MERGE variants retained future applicability; do not prepare a load |
| delete_record | Pending future development | Native DELETE removed all history, not one selected dated change; do not substitute it |
| override_predefined | Pending future development | UI source alone is not an approved native write contract |

TaxabilityRule is a standalone date-effective BO, with no child records. UI
rows can aggregate several independent component rules. Explicit Select All
Secondary Classifications expands the current eligible set; never infer this
choice or use the visible UI item count as the physical row count.

## Conversational Intake

Apply this contract to the current request and its follow-up answers, including
business values supplied through the invoking workflow. Collect business intent,
not HDL syntax. A supplied value awaiting Fusion validation is not a missing
answer. Conversation state collecting means input is still being resolved; it
does not mean a failed load or permission to prepare an incomplete archive.

### Input Kinds

| Input Kind | Business Requirements | User Guidance |
|---|---|---|
| Fusion choice | LDG, component group, reference level, primary and secondary classifications, active context values, payroll components, existing rule and history version | Ask to select from Fusion using business labels and eligible choices from the owning resolver. Treat an explicitly supplied name or code as the user's selection to validate, not as a reason to ask for the same selection again. |
| Fixed choice | Operation when unclear, Included or Excluded per component, explicit all/none secondary scope, whole-history deletion intent | Ask to select one applicable business choice; do not present these as Fusion LOVs or silently infer all, none, inclusion or destructive intent. Eligibility and operation limits remain those of Required Groups and the owning design rules. |
| User-entered date | Effective as-of date, Create start or Update boundary when needed | Ask for an unambiguous full-year date, suggesting YYYY-MM-DD. Accept other unambiguous full-year dates under Field Validation; do not ask the user to supply the native DAT date format. Existing history versions are Fusion choices, not dates to invent. |
| Declared default | Conditional values defined in ora_defaulting_rules.md | Do not ask for an already applicable default; disclose its business effect in the complete core preview. Never replace an explicit user value or introduce a new default. |
| Internally derived or core-owned | Surrogate/foreign IDs, context storage codes and HDL mappings, legislation, returned links, DAT encodings, verified environment/security context and artifact/approval state | Resolve through the owning lookup or core workflow. Never ask for internal IDs, URLs, tokens, P/N codes or HDL directives. If the configured target is unresolved, ask only for a business environment choice through core. |

Lookup mechanics remain in ora_reference_lookups.md and dependency order in
ora_dependency_readiness.md. This intake contract authorizes no additional
external call, lookup shortcut, default, operation or approval step. Keep
internal IDs out of conversational prompts, choices and business summaries.

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Every initial request or changed operation | Classify intent before collecting operation-specific fields | Infer the operation when explicit. Otherwise ask only the business distinction needed. Consult Operation Profiles and ora_design_enforcement.md before further collection; do not offer a pending operation as available. | |
| The request explicitly asks for a pending operation or an unsupported field shape | UNSUPPORTED or WBR_OPERATION_PENDING, not incomplete intake | Use ora_error_handling.md to explain the current boundary immediately. Do not collect more mutation details, discard the unsupported part or substitute another operation. Conditions discoverable only from current reads remain subject to the later design gate. | |
| Business values are supplied in the current request or its follow-up answers | Retain user intent; eligibility may still be unresolved | Ingest all supplied values together, including per-component inclusion decisions. Validate through their existing Required Groups resolvers without asking the user to re-enter them. Do not import selections, IDs, approvals or example values from a previous operation. | |
| Required business input is absent or user intent is ambiguous | Remain collecting; discovery or NEEDS_INPUT | If intent is supported and resolving supplied parent values or retrieving the next choice list requires declared lookups, use the discover outcome through dependency and reference nodes. If a user-entered prerequisite or intent clarification is needed first, return needs_input and ask only that question. Never prepare an archive or approval preview while required input is unresolved. | |
| The user answers some or all pending questions | Resume collecting or finish intake | Validate the answer's input kind and retain accepted values in this operation. Follow the existing dependency invalidation rules for changed values. Ask only the next unresolved requirement, not the entire questionnaire. A compact batch is allowed only for independent questions; a partial batch answer does not restart that batch. | |
| A supplied value is invalid, ambiguous or conflicts with another supplied value | Clarification needed; unaffected accepted input remains available | Use ora_error_handling.md to explain the specific business issue and ask for a correction or disambiguation. An unresolved system mapping, unavailable lookup or auth failure is a blocker, not a demand that the user supply an internal key. | |
| All applicable business inputs have been supplied | Intake complete, not approval or Fusion success | Advance through the declared dependency, lookup, defaulting and design checks without a redundant confirmation of every field. Only core's existing preparation and approval workflow may request mutation approval after the full contract passes. | |
| A selection request requires live choices not yet retrieved | Discovery, not an implicit selection | Keep the original requested operation while the declared reference node resolves choices. Follow Lookup Execution Rules in ora_reference_lookups.md for searchable bounded lists; a search term or a one-row search result is not user selection. | |

While collecting, end each response with the next direct, actionable business
question, not only a progress list or "ask me for the next step." Do not ask
another intake question when input is complete, the requested read is complete,
the user cancels or pauses, a real blocker requires owner action, or the workflow
is awaiting core approval. Route diagnostics and safe continuation through
ora_error_handling.md; collecting never bypasses a technical or approval gate.

## Secondary Classification Intent

Normalize intent before resolving the secondary field. These are input states,
not four different HDL shapes; lookup authority remains with
find_wbr_classifications in ora_reference_lookups.md.

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Missing secondary selection | Keep unresolved, not blank-key or all. After the primary/date scope is known, ask which secondary to select, or offer explicit all or none only when applicable. An empty eligible list does not silently resolve the omission. | Secondary not supplied | find_wbr_classifications |
| Explicit named secondary selection | Retain the supplied selection and resolve it within the current primary/LDG/date scope. Invalid or ambiguous matches require a targeted question, not replacement by another choice or all. | A secondary business label was selected | find_wbr_classifications |
| Explicit none | Represent an intentional null secondary only after the current scope's optional-secondary contract is established. A missing label, empty list or unselected dropdown is not explicit none. | User requests no secondary classification | find_wbr_classifications |
| Explicit all | Resolve the entire eligible secondary set, not the current search page. If no eligible secondaries exist, ask whether none is intended only if eligible; otherwise report the scope/contract issue. Never create zero rows and report success or silently turn all into none. | User selects all eligible secondary classifications | find_wbr_classifications |
| Contradictory secondary instructions | Ask whether named selection, none or all is intended, preserving unrelated answers. Do not choose whichever instruction appeared first or last unless the user clearly corrected it. | More than one incompatible mode supplied | |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Intent and environment | operation, environmentAlias, project/task context | NEEDS_INPUT | Resolve one supported business operation and configured target; ambiguous delete requires clarification | Always | |
| Legislative scope | LegislativeDataGroupName | NEEDS_INPUT | Select an exact current LDG name | Every fresh operation | find_wbr_ldg |
| Component group | ComponentGroupName | NEEDS_INPUT | Resolve the group from the current LDG's choices before requesting reference levels | Discovery/Create or when target identity needs clarification | find_wbr_group |
| Reference level | ReferenceLevel | NEEDS_INPUT | Select from the current group's reference levels, including explicit No References when offered | Discovery/Create or when target identity needs clarification | find_wbr_reference_level |
| Classification | PrimaryClassification, SecondaryClassification selection or explicit all/none | NEEDS_INPUT | Establish the applicable date, resolve primary, then apply Secondary Classification Intent; do not infer none or all | Fresh target selection/Create | find_wbr_classifications |
| Context | Ordered business values for active levels | NEEDS_INPUT | Resolve all required cascading context levels and both HDL/REST representations | Reference level has active contexts | find_wbr_context_values |
| Components and inclusion | PayrollComponent selections, Included or Excluded per component | NEEDS_INPUT | Create resolves requested components and decisions; Update/Correct reuse the selected existing rule's component and collect only its new decision | Create, Update, Correct | find_wbr_components |
| Effective dates | Explicit Create start for each component, Update boundary, or existing Correction slice | NEEDS_INPUT | Reuse an explicit common Create start where no component-specific start was supplied; otherwise ask only for unresolved dates. Existing operations select the applicable history version. | Mutation except whole-history Delete | read_wbr_history |
| Lookup date | Explicit applicable business date or unambiguously selected history version date | NEEDS_INPUT | Follow the operation-specific date roles in ora_dependency_readiness.md before a date-sensitive lookup; do not ask again for an already supplied date | Whenever primary/secondary classification choices need resolution | |
| Existing target | Complete business identity and selected version where applicable | NEEDS_INPUT | Follow Existing-Rule Maintenance Intake; reuse supplied identity, read history and ask only unresolved target/version questions | Update, Correct, Delete, exact read | read_wbr_history |
| Whole-history intent | Explicit delete_record_and_history request | NEEDS_INPUT | Explain every version is removed and obtain explicit scope before preparation | Delete | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Business dates | Parse real unambiguous calendar dates; normalized internal/read dates are YYYY-MM-DD, native DAT dates are YYYY/MM/DD; reject invalid dates | All dates | |
| Inclusion | Included maps to P and Excluded maps to N; no default if omitted | Create, Update, Correct | |
| DAT cells | Reject pipe, CR, LF or NUL inside a value; report current encoding limitation rather than invalidating a legitimate business label | Mutation | |
| Unexpected fields | Reject rather than silently dropping them; REST ContextValueN, effectiveOf, object version and UI-only Select All are never DAT columns | Mutation | |
| Context cardinality | Preserve six ordered slots; never shift later levels into blanks; no invented zero context | Mutation | find_wbr_context_values |
| No References with conflicting values | If the current request explicitly supplies context values alongside No References, ask which scope is intended rather than silently discarding those values. Previously cached context selections are invalidated when the reference level changes. | Conflicting reference/context input | |
| Record identity | Surrogate/foreign keys are operation-local lookup outputs, never ordinary user input or cross-environment defaults | Mutation | read_wbr_history |
| Secondary selection | Never silently use all or choose the first; keep collecting on a meaningful omission | Create | find_wbr_classifications |
| Fan-out count | Apply Create Component Rows; count every resolved component/secondary combination, including Excluded rows and intentional null-secondary alternatives; reject duplicate identities | Create | |
| Existing-rule action count | One logical rule per Update, Correct or Delete archive; other requested rules become separately reviewed operations | Existing-rule mutation | |
| Date range | Update boundary must fall strictly after the selected last slice start and within its range; Correction dates equal selected physical range | Update, Correct | read_wbr_history |

## Existing-Rule Maintenance Intake

Start with the requested effect and the existing rule, not a fresh Create
questionnaire. Identity and version evidence come from the declared lookup
workflow; user-facing choices remain business labels and full-year dates.
The lifecycle policy and exact before/after effects belong to
ora_design_enforcement.md; native shapes remain in Native DAT Contract.

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Maintenance intent | Reuse an explicit Update, Correct or Delete Record and History request. If the user says only maintain or change and the intended dated effect is unclear, ask whether to introduce a change from a new date or correct an existing version in place. Do not select an operation merely because its inputs are easier to obtain. | Unclear lifecycle effect | |
| Supplied or selected rule | Retain the supplied LDG, component, classification and reference/context business identity, including a rule selected during this request. Let the existing resolvers verify it and retrieve full history; ask only for a still-missing discriminator required by that route. Do not request internal IDs or reselect known Create fields. | Every maintenance request | read_wbr_history |
| Multiple or absent targets | Present available business distinctions when several logical identities match; ask which rule is intended. A component or an aggregate UI row alone may cover several rules. No exact match is NOT_FOUND, not permission to create or substitute a similar rule. | Target selection unresolved | read_wbr_history |
| Update input | Collect the requested Included or Excluded state and full-year effective boundary, reusing either if supplied. Read the selected rule's history as soon as its lookup prerequisites are ready; do not wait for missing change inputs or ask for a new Create start, end, secondary scope or component list. | Update | read_wbr_history |
| Correct version | Reuse a version explicitly selected in this request, an exact existing start/period, or a supplied as-of date that uniquely identifies a returned version. Otherwise present history and ask which existing version to correct; do not default to the latest or today's version. Translate a qualifying as-of date to the selected version's actual start, never a new boundary. | Correct | read_wbr_history |
| Correct input | Ask only for the requested Included or Excluded state if missing. Retain the selected version's actual start and end under ora_defaulting_rules.md; do not request replacement dates. If the request also changes dates or asks for a new version, clarify the conflicting effect before preparation rather than silently converting Correct into Update. | Correct | |
| Ambiguous delete | A bare delete, remove this rule or an unqualified yes does not establish whole-history intent. Ask whether every version or only a dated version is meant, explaining that single-version Delete is pending. A yes counts only when it answers a clear question naming this rule and removal of all historical and future versions. | Deletion scope not explicit | |
| Explicit Delete Record and History | Retain the explicit scope without asking for it repeatedly. Retrieve the complete history and disclose every version to be removed under the design/disclosure rules. Do not collect a new inclusion, start or end; derive native identity dates under ora_defaulting_rules.md. Scope clarification is not execution approval; core still owns approval. | Explicit whole-history intent | read_wbr_history |
| Date-qualified deletion | If the request restricts deletion to a version or period, apply the pending-operation boundary. If it is unclear whether a date identifies the rule or limits deletion, ask that distinction; never treat the qualifier as permission to remove all history. | Deletion includes dates | |
| Multiple maintenance targets | Keep each requested logical rule separately identified. The current contract prepares one logical rule per operation; do not apply a selected row's action to other components, secondary classifications or jurisdictions, or carry Create all-secondary expansion into maintenance. | More than one potential or requested rule | |
| Partial answers and changed selection | Preserve accepted business intent while collecting and ask only the next unresolved input. Apply Selection Changes and Revalidation when the target, version, operation, boundary or decision changes. No incomplete maintenance request reaches artifact preparation or approval. | Maintenance follow-up | |

## Create Component Rows

Retain a business row per selected component within the resolved LDG, group,
reference/context and primary-classification scope. These are conversational
selections, not a new transport schema. Resolve them before core preparation;
only core produces the archive using Native DAT Contract below.

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Component-row intent | Retain the component selection, explicit Included or Excluded decision, and explicit applicable start date. A request to include A and B and exclude C supplies three decisions, not two rules and a removal. Never drop an Excluded selection. | Each Create component | find_wbr_components |
| Common versus component start | Apply Common Create start propagation in ora_defaulting_rules.md during intake, before date-sensitive lookups, retaining the source of each date as common instruction or component-specific instruction. Ask about contradictory dates only when the user's intent is unclear. | Create with common or row-specific dates | |
| Incomplete component row | Ask only for the missing inclusion decision or start for the named component, preserving completed rows and scope. A supplied decision or date awaiting validation is not missing. Keep collecting; no archive or approval preview. | At least one unresolved component row | |
| Date-scoped classification selection | Resolve the primary and requested secondary selection for every distinct component start through the existing date-sensitive resolver. A named secondary must be eligible in every combination where requested; an ineligible selection needs clarification, not silent omission. | Create rows with one or more dates | find_wbr_classifications |
| Explicit all expansion | For each component, pair it with every member of the completely retrieved eligible secondary set at its start date. Ignore any display search/page restriction. Count the sum of these set sizes across components; when all share the same set, this is component count times secondary count. Copy that component's decision and start to each combination. | Explicit all-secondary intent | find_wbr_classifications |
| Named and none expansion | Pair each component with the explicitly selected eligible secondary or secondaries. Explicit eligible none is one intentional null-secondary alternative per component, not an empty set or zero rules. Missing intent, empty all or partially retrieved all remains unresolved. | Named or explicit none intent | find_wbr_classifications |
| Native and readback context representations | Retain the established HDL business helper key separately from the REST stored value for each ordered active slot. Native ContextN cells use the helper keys; REST ContextValueN expectations use the corresponding stored values. Do not copy a displayed label or numeric REST value into native cells without mapping evidence. Inactive gaps remain blank and No References omits native context columns. | Resolved context scope | find_wbr_context_values |
| Exact expected rows | Derive the ordered native expected rows and independent REST identity/date expectations from the same resolved business combinations before comparing with core's prepared DAT. Do not derive expected values by copying the DAT under test. Included and Excluded both contribute one row per combination; open-ended/date serialization follows ora_defaulting_rules.md. | Completed Create selection | |
| Repeated logical identity | Identify repeated resolved LDG/component/primary/secondary/ordered-context identities, including different labels resolving to the same identity. Different start dates or inclusion choices do not make a repeated identity a new Create. Apply the conflict gate in ora_design_enforcement.md; do not silently deduplicate. | Expanded Create rows | |

No internal IDs, native context encodings or dates in loader syntax are user
questions. If a mapping cannot be established, report the resolver blocker;
do not ask the user to invent a key. A numeric-looking helper key is valid when
current mapping evidence establishes it; numeric appearance alone is not a
reason to substitute or reject it.

## Create Acceptance Cases

These are offline conversation and contract-review cases. A passing helper
check does not establish live eligibility, complete lookup pagination or user
approval; those remain workflow gates.

| Scenario | Expected Result |
|---|---|
| One secondary, Include A and B, Exclude C, common start 01-Feb-2026 | Three native rows and three readback expectations: two Included and one Excluded, all starting 2026/02/01 in DAT; no repeated inclusion/date questions |
| Same three components with explicit all and two eligible secondaries | Six rules: four Included and two Excluded; enumerate both secondary choices and count exclusions in the business summary |
| A starts 01-Feb-2026 and B starts 01-Mar-2026; explicit all resolves two and three eligible secondaries respectively | Five rules with their respective component dates and eligible sets; do not reuse one date's classification evidence for the other |
| Explicit eligible none with three components versus missing secondary | None produces three null-secondary rules; missing remains collecting and never silently becomes none |
| One component lacks inclusion or start | Ask only for that component's unresolved value; preserve other answers and do not prepare an archive or approval preview |
| Same logical combination repeated with different dates, inclusion or aliases | Block Create as a conflict; never merge instructions, drop a row or turn the request into Update |
| Supplied finite end, unmapped active context, or incomplete all-secondary retrieval | No Create approval: explain the pending finite-end contract or the specific unresolved mapping/discovery prerequisite |
| Complete resolved scope and rows with no history conflicts | Supply the complete business summary and exact expected rows to core's existing preparation/Task Hook/approval workflow; no extra task-owned confirmation |

## Discovery Acceptance Cases

These are offline conversation-review cases, not claims of live tenant results.
Use synthetic choices and follow the declared graph; no Fusion call is needed
to review the expected intake behavior.

| Scenario | Expected Result |
|---|---|
| Complete prompt supplies scope, classification, components and 01-Feb-2026 | Reuse the date and every supplied selection; validate classifications for that date rather than today; no repeated questionnaire |
| Applicable classification date is absent | Ask for the date before any classification lookup; independent LDG/group discovery need not be discarded |
| No References is selected and its metadata has no active contexts | Skip all context questions and context-value calls; retain empty ordered slots; do not ask for State/County/City |
| The same prompt explicitly supplies No References and a City | Ask which reference scope is intended; do not silently omit the supplied City or replace No References |
| User supplies a State, County and City together | Resolve the parent chain in order and reuse each unique eligible selection; an ambiguous City asks only for the necessary business distinction |
| A LOV has 21 choices and a text search leaves 23 matches in a larger LOV | Ask for a term for the large set; present at most 20 matches per page with continuation, not truncated-as-complete results |
| A search leaves one match versus an explicit exact business selection | Ask for selection after search; validate the explicit exact selection without asking again |
| Missing secondary, explicit none, explicit all, or all while a text filter is active | Keep the modes distinct; none requires eligibility, all uses the full scoped set and never just filtered matches; missing remains a question |
| An empty or partially retrieved secondary list | Empty does not imply none or successful all; partial retrieval blocks completeness claims |
| Two eligible records share a label or a customer-defined label is selected | Disambiguate using business fields; accept eligible customer-defined selections under the same mapping rules; never choose the first, expose IDs or force sample values |
| State changes while County and City were already selected | Invalidate and re-resolve descendant candidates and rule baselines; ask only for ineligible or ambiguous replacements, retaining unrelated answers |
| Date, LDG, group or reference level changes | Apply Selection Changes and Revalidation; discard stale evidence and displayed page ordinals, preserve unaffected business input and invalidate any prepared approval |
| Discovery finishes retrieving choices but the user has not selected | Return needs_input through the existing intake-resume path; do not reach defaulting, archive validation or approval |

## Native DAT Contract

Core prepares exactly one TaxabilityRule.dat member. This task validates its
bytes and returns Task Hook findings; it does not implement another loader.
Use one METADATA section, no COMMENT, no child sections, no extra members and
equal field counts on every data/header line, preserving trailing empty cells.

| Profile | Directive | Instruction | Ordered attributes after TaxabilityRule |
|---|---|---|---|
| create | None | MERGE | EffectiveStartDate, LegislativeDataGroupName, PayrollComponent, PrimaryClassification, SecondaryClassification, zero to six ordered ContextN fields, UsageType |
| update or correct | SET PURGE_FUTURE_CHANGES N | MERGE | TaxabilityRulesId, EffectiveStartDate, EffectiveEndDate, ClassificationId, SecondaryClassificationId, DeductionTypeId, LegislativeDataGroupId, Context1, Context2, Context3, Context4, Context5, Context6, UsageType |
| delete_record_and_history | None | DELETE | TaxabilityRulesId, EffectiveStartDate, EffectiveEndDate, ClassificationId, SecondaryClassificationId, DeductionTypeId, LegislativeDataGroupId, Context1, Context2, Context3, Context4, Context5, Context6 |

For Create, include context columns through the highest active slot, filling
only metadata-inactive intervening slots with blanks. With No References omit
all ContextN columns. A missing secondary is an intentional empty key only
after the lookup and explicit selection rules pass. The current Create profile
omits end date and expects the live open-ended default; a requested finite end
date requires a separately proven shape, not silently ignoring the request.

For Update/Correct/Delete use the existing surrogate ID plus all foreign
identity fields and all six HDL context slots. ID alone previously failed the
functional-reference resolver. Update retains the selected open-ended end;
Correct retains both physical dates. Delete carries dates of the selected
existing version for identity, but those dates DO NOT limit its destructive
scope: all versions are removed. None of these profiles authors a source key.

## Offline Contract Check

The task-local helper scripts/wbr_contract.py is read-only and supplemental:
it checks exact DAT field shape/count/date syntax and compares normalized
timelines. It never resolves a Fusion identity, grants approval, submits data,
or replaces current core schema validation. Run its validate-dat command
against the final supplied DAT plus the exact expected rows derived by the
governed plan; successful parsing alone is not semantic validation. Follow
ora_error_handling.md for reconciliation and helper usage.

## Task Nodes

Rule ID inventory: WBR.VALIDATE_INPUT, WBR.RESOLVE_DEPENDENCIES,
WBR.RESOLVE_REFERENCES, WBR.CHECK_PREPARATION, WBR.APPLY_DEFAULTS, WBR.VALIDATE_NATIVE_CONTRACT,
WBR.ENFORCE_DESIGN, WBR.EXECUTION_GATE, WBR.HANDLE_ERROR,
WBR.READY_FOR_CONFIRMATION, WBR.DONE_READ_ONLY, WBR.RETURN_ISSUES.

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WBR.VALIDATE_INPUT | decision | 1 | validate_input | valid->WBR.RESOLVE_DEPENDENCIES;discover->WBR.RESOLVE_DEPENDENCIES;needs_input->WBR.HANDLE_ERROR;unsupported->WBR.HANDLE_ERROR;invalid->WBR.HANDLE_ERROR | none | stop | Apply Conversational Intake, Dependency-Aware Validation and the applicable Existing-Rule Maintenance Intake or Create Component Rows; valid means complete supplied input, not resolved eligibility; discover permits only declared prerequisite/choice reads while collecting; needs_input asks a missing prerequisite; unsupported stops further mutation intake |

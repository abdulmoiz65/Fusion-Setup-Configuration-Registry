# Wage Basis Rules Error Handling and Reconciliation

## Error Situations

| Situation | What Should Happen |
|---|---|
| Missing or ambiguous business selection | Report NEEDS_INPUT, not a failed Fusion operation. Follow Conversational Intake in ora_input_validation.md; retain accepted values and ask the next unresolved business question with current eligible labels when available. |
| Invalid or conflicting user-entered value | Explain the specific business issue and request only its correction; preserve unrelated accepted input. For an ambiguous or invalid date, suggest an unambiguous full-year date rather than asking for DAT syntax. |
| A supplied business value is awaiting lookup validation | Do not ask for it again merely because its ID is unresolved. Use its owning declared resolver; a blocked lookup requires the relevant technical next action, not an internal-ID question. |
| Maintenance target or Correct version remains ambiguous | Show the available business distinctions or verified dated history and ask only which rule/version is intended. Retain new inclusion and other accepted answers; do not default to the latest version or restart Create intake. |
| Maintenance request conflicts with retrieved history | Explain the specific period or current inclusion that differs from the request. Do not silently switch components, versions or operations to make the request fit. Unchanged inclusion is NO_CHANGE; an unsupported Update boundary needs clarification or the pending-shape response. |
| Deletion scope is ambiguous | Ask whether all history or a single dated version is meant, stating that single-version Delete is pending. Neither an unqualified yes nor a date alone establishes whole-history intent; a clearly contextual answer may resolve it. No preparation while unresolved. |
| Native date parser rejects ISO dates | Report INPUT_VALIDATION; TaxabilityRule DAT requires YYYY/MM/DD. Correct bytes through core, then repeat validation/approval; no replay |
| PrimaryClassificationHelper.Validation fails | Check complete classification, secondary, component, LDG and context identity; surrogate ID alone was insufficient |
| Context resolver rejects a numeric REST code | Check route-specific HDL helper keys versus REST stored codes; retain business selection and resolve the mapping |
| DAT row/header counts differ | Preserve empty trailing cells and count them. Three remaining blank attributes require three separators after the last populated value, not four |
| Loader reports success but state differs | CONTRACT_INCOMPLETE, not business success. Preserve partial successes; do not resubmit the whole archive |
| Core returns auth, HTTP, process failure or timeout | Use core's sanitized diagnostic and original request identifiers; do not invent success from missing output |
| Write response is uncertain | OUTCOME_UNKNOWN; reconcile original request through core status and declared GETs. No automatic mutation replay |
| Explicit End Date or selected-version Delete requested | WBR_OPERATION_PENDING as soon as intent is known, before collecting further mutation details. Explain that whole-history deletion is not a substitute. For an ambiguous "delete," clarify the intended scope rather than assuming either operation. |
| Another unsupported operation or field shape is explicit in the request | Explain the current limitation before further mutation intake, using the boundaries in ora_design_enforcement.md. Do not drop a requested finite end date or offer another write as equivalent; offer a read-only review without starting it automatically. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| NEEDS_INPUT | Missing or ambiguous business choice during intake | Preserve collecting and ask only the unresolved business question; no incomplete archive or approval preview |
| INPUT_VALIDATION | Invalid supplied input shape, date, encoding or field count | Ask for the specific business correction while collecting, or have core correct a malformed prepared artifact; ordinary omissions are NEEDS_INPUT |
| NO_CHANGE | Requested inclusion already matches the selected applicable version | Report the existing business state and that no change was prepared or submitted; a different request needs fresh validation, not an automatic substitute operation |
| CATALOG_MISMATCH | Missing/changed template, mismatched aliases, unresolved mapping or incomplete pagination | Repair authoritative contract/evidence before planning |
| AUTH_AUTHZ | Unusable session or insufficient privilege | Ask authorized owner to refresh/grant access; honor no-OAuth instructions |
| TRANSPORT_ENVIRONMENT or FUSION_API | Connection/host mismatch, HTTP failure or invalid response | Preserve sanitized error and ECID through core; do not treat as absence |
| PROCESS_FAILED or PROCESS_TIMEOUT | Core reports failed or unfinished original load | Inspect core status/detail; no new dispatch |
| ARTIFACT_PERSISTENCE or APPROVAL_BLOCKER | Immutable artifact/envelope absent, changed or unapproved | Stop before upload and rebuild/reapprove through core |
| CONTRACT_INCOMPLETE | Successful load fails exact business reconciliation | Show expected versus observed business effect and escalate; no automatic corrective write |
| WBR_OPERATION_PENDING or UNSUPPORTED | Requested lifecycle effect/field shape is not delivered | Record future work and offer supported read-only review |

## Intake Return and Resume

WBR.HANDLE_ERROR also discloses nonfailure NEEDS_INPUT results. Follow its
existing transition to WBR.RETURN_ISSUES and return missing requirements plus
the next actionable question to the caller, preserving conversation state
collecting. Use MISSING if the invoking execution guide requires that terminal
status; do not represent it as a failed load or a completed business operation.

After an answer, the caller re-enters WBR.VALIDATE_INPUT with the accepted
business values and the new answer for the same operation. Do not add a graph
cycle, skip prerequisites, automatically retry a failed lookup or replay a
mutation. Apply
the input contract again; lookup evidence must still satisfy its current scope.
An auth/contract/transport blocker remains blocked until its own recovery
conditions pass, and an uncertain write still requires reconciliation.

## Preparation Continuation After Intake

When the user accepts a plan for separate supported operations, retain that
intent and advance each operation independently through its declared read-only
preflights, lookups and local preparation to the next genuine workflow gate.
For example, after agreement to Create one missing component rule and Correct
another existing rule, complete the applicable checks and prepare a separate
core-governed preview for each. A progress update such as "live metadata
preflight is next" does not by itself end the turn or require the user to say
"continue." Do not repeat accepted business questions or treat agreement to
the plan as approval to upload or initiate either load.

Pause only when an operation needs a missing or ambiguous business choice, a
declared preflight is blocked or conflicts with current evidence, or core's
authoritative preparation or approval workflow requires a return to the user.
At a task-owned pause, state which operations are ready, blocked or still
being prepared and the specific next action; use core's authoritative report
unchanged when it owns the return. Retain each operation's independent
identity, artifact and approval. Do not bypass a core terminal response,
retry a failed lookup, submit a load or poll status to keep work moving.

## Reconciliation Rules

These rules apply only after authoritative loader success and a requested
business verification. Loader status alone, an aggregate UI count or an empty
filtered query is insufficient. Resolve all-history and independent physical
reads through ora_reference_lookups.md, retaining the original approval-bound
business identity and before-state. Compare every context, including nulls,
and verify the unaffected baseline. History with unresolved two-digit years is
not suitable for a success decision.

| Operation | Required outcome |
|---|---|
| create | Intended loader row count loaded, zero failed; exactly one new logical rule for each requested component/secondary combination, correct start and open end, inclusion and stored contexts; no extra or accidental blank-context rule; previously observed siblings unchanged |
| update | Same logical identity; selected prior slice ends boundary minus one day with old inclusion, new slice starts at boundary with requested inclusion and original open end; earlier history unchanged; physical reads on prior day, boundary and following day agree |
| correct | Same identity, same number of slices and same start/end dates; only selected slice inclusion changes; predecessor/future slices and other components unchanged |
| delete_record_and_history | Complete exact history empty; independent ID and full-business-identity physical reads empty at every former slice start and representative later date; other component rules unchanged |

An Update removing earlier history, a Correction creating a new slice, or a
Delete leaving any selected-rule version is CONTRACT_INCOMPLETE. Finite end
plus a surviving future slice is failed End Date semantics even if loader
status is success. That operation remains unavailable.

## Offline Helper Contract

Run from repository root (the commands are local and perform no Fusion calls):

```text
python -B pillars/hcm/global-payroll/calculation-cards-and-calculation-values/payroll-calculation-information/scripts/wbr_contract.py --help
python -B -m unittest discover -s pillars/hcm/global-payroll/calculation-cards-and-calculation-values/payroll-calculation-information/tests -v
```

`validate-dat --operation <profile> --dat <approved-input> --expected <rows-json>`
reads the supplied DAT and a JSON array of exact expected native-field
dictionaries from the governed plan. It checks syntax/shape and exact expected
values, not live lookup authority. It never echoes row values.

`reconcile --evidence <normalized-json>` consumes operation, before, after,
change, complete and loader_success. Each slice has the exact physical identity
fields, six ContextValueN slots, ISO EffectiveStartDate/EffectiveEndDate and
UsageType. The change selects target_id plus date/usage for Update, target_id
plus start/usage for Correct, target_id plus whole_history=true for Delete,
or rows containing expected Create identity/dates/usage (without a new ID).
The caller must collect the complete baseline/after-state for the same scoped
family, including siblings, and set complete=true only after all mandated
queries/pagination succeed. The helper cannot authenticate that assertion or
replace independent physical reads. Invalid/missing evidence fails closed;
output is counts/classification only. Protected evidence remains governed by
core/project handling and is not a reusable fixture.

## QA Scenarios

| Scenario | Expected result |
|---|---|
| Complete supported Create prompt with LDG, start date, group, reference level, classifications, all active contexts and per-component inclusion | Reuse every supplied business value and advance to the existing validation path; do not repeat selection questions or treat intake completion as approval |
| Only inclusion is missing for one named component | Ask whether that component is Included or Excluded; retain the other rows and do not ask for UsageType or internal IDs |
| User answers only the LDG after being asked for LDG and start date | Retain the LDG and ask only for the missing start date; do not repeat the batch or stop with a progress-only message |
| User supplies 01-Feb-2026, an invalid date, or an ambiguous numeric date | Accept the unambiguous full-year date; for the others ask only for a valid unambiguous date; do not ask the user to format an HDL cell |
| Supplied component name has more than one eligible match | Present available business-label distinctions and ask which match is intended; do not choose the first or request a surrogate key |
| Business choices are complete but context mapping or authentication is blocked | Explain the technical blocker and safe next action; do not ask the user to replace a valid selection with internal codes |
| User accepts separate Create and Correct operations after a history conflict | Continue each operation's declared read-only preflight and local preparation to its own core preview or genuine blocker; a progress-only "preflight is next" message does not require a new "continue" instruction. Neither operation inherits the other's artifact or approval. |
| Finite-end Create is explicitly requested | Explain the current unsupported shape before collecting more mutation inputs; no silent open-ended replacement |
| User says only "delete this rule" | Clarify whether one version or the entire history is intended; do not assume the supported destructive interpretation |
| New rule, two included components | Two exact new physical rules after governed load and readback |
| Include two components and exclude a third | Three rules, not two; resolve the prompt/expected-count mismatch before approval |
| Missing secondary where eligible choices exist | Prompt for it, with no prepared/submitted write |
| Customer-defined valid live label | Accept unique eligible selection when native mapping resolves; never force a fixture label |
| Effective Update | Prior period preserved and new boundary/inclusion exact |
| Correct one dated version | No added/deleted slices or date changes |
| Existing rule was selected and user supplies Excluded from 01-Jul-2026 | Reuse business identity, retrieve complete history, validate the boundary and new inclusion; do not repeat Create scope questions |
| Update inclusion is supplied but its boundary is missing | Retrieve history when its binds are ready, then ask only for the change's effective date; no default to today or an old Create date |
| Correct has a selected version but no new inclusion | Show that version's dates/current inclusion and ask only Included or Excluded; retain both existing dates |
| Correct supplies an as-of date inside exactly one returned version | Select that existing version, retaining its actual start/end; do not split at the as-of date |
| Correct names no version while several versions exist | Present full-year history and request a version; no implicit latest selection or new-date question |
| Update versus Correct on an Included version starting 01-Jan-2026 with no end | Update to Excluded from 01-Jul creates Jan-Jun Included plus Jul-onward Excluded; Correct that original version to Excluded retains 01-Jan and the original end with no new version |
| A generic delete or a date-qualified deletion is followed by an unclear yes | Remain collecting until whole-history scope or the pending single-version intent is explicit; do not prepare DELETE |
| Explicit whole-history Delete on a rule with past and future versions | Reuse supplied intent, disclose all versions/count, derive native anchor dates without asking for a deletion date, and use core approval once |
| Multiple component rules share an aggregate UI row, or only context/secondary differs | Select the exact logical rule; all other identities remain outside the operation and unchanged in reconciliation |
| Requested inclusion already matches the applicable version | NO_CHANGE; no new archive, no submission and no false mutation-success claim |
| End Date | Pending-operation response; zero write |
| Delete only a later version | Pending-operation response; zero whole-history DELETE |
| Explicit Delete Record and History | Destructive scope disclosed before approval; every target version absent and siblings preserved |
| Malformed trailing delimiter or ISO DAT date | Offline/native-contract validation blocks before approval |
| Partial page, lost response, failed load or stale artifact | No success and no automatic replay |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input/lookup failure | Business selection, safe reason and next action; no raw IDs |
| Approval/initiation/status | Core/data-loader's complete authoritative report, without a competing task-local report or approval step |
| Separate reconciliation | Business expected/observed dates and inclusion, verified versus failed outcome, pending operations and safe next action |
| Destructive intent clarification | All historical and future versions of the selected logical rule will be removed; selected DAT dates do not limit deletion |
| Existing-rule maintenance preview | Selected logical rule in business terms, all before/after periods and inclusion, version counts and unaffected scope; whole-history Delete explicitly includes every historical and future version. Supply these facts through core's authoritative report, not a second approval prompt. |

No task node uploads, initiates, polls or calls a direct product mutation.
After accepted initiation, follow core's current later-status workflow; do not
add automatic polling. Do not inspect, print or persist tokens, cookies, secret
properties or session-cache contents. A success terminal for validation is not
evidence of a Fusion write. Reconciliation never authorizes another mutation.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WBR.EXECUTION_GATE | decision | 8 | execution_gate | controlled_plan_ready->WBR.READY_FOR_CONFIRMATION;read_only_ready->WBR.DONE_READ_ONLY;blocked->WBR.HANDLE_ERROR | none | stop | Mutation must have completed input/dependency/reference/preparation/default/contract/design nodes; read must have completed its applicable lookup path; reconciliation must meet the exact outcome rules |
| WBR.HANDLE_ERROR | step | 9 | error_handler | disclosed->WBR.RETURN_ISSUES | none | continue | Disclose NEEDS_INPUT without marking a failed operation, or handle a failed, blocked or unsupported request; follow Intake Return and Resume |
| WBR.READY_FOR_CONFIRMATION | terminal | 10 | terminal | none | WBR.EXECUTION_GATE | continue | Exact artifact passed Task Hook; return to core approval lifecycle, not mutation success |
| WBR.DONE_READ_ONLY | terminal | 11 | terminal | none | WBR.EXECUTION_GATE | continue | Requested read or exact business reconciliation completed |
| WBR.RETURN_ISSUES | terminal | 12 | terminal | none | none | continue | Return sanitized blockers or unresolved input and one safe next action; NEEDS_INPUT preserves collecting and resumes through WBR.VALIDATE_INPUT after the answer |

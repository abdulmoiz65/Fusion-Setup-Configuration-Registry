# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Identity/immutable header invalid | Stop with set/name/type/ID and exact conflicting field |
| Reference/subtype dependency invalid | Stop with line key, field, supplied value, match/effective/dependency result |
| REFERENCE_UNRESOLVED | Warning, blocking=false: preserve proven representation; show skipped check and next evidence; continue all supported checks and preview without waiver |
| UI-only control lacks CSV mapping | Record unresolved/nonblocking and explicitly not applied; never invent a field |
| Supported REST lookup fails | Classify auth/authz, transport/environment, API or pagination failure as error; do not mislabel missing authority or claim validation complete |
| Duplicate/overlapping/invalid line | Stop with canonical key, intervals, value/UOM, and precedence impact |
| Active-use/delete conflict | Stop with stable ID, operation, protected fields, and consumer counts |
| REST/FSM execution fails | Report route, target, request/package checksum, item/member/row, HTTP/Oracle error; no retry/fallback |
| REST Invalid attribute | Classify as a request-contract failure; preserve exact rejected method/path/subtype/field. Compare header versus child request schemas and target metadata. Do not conclude that the field is globally unwritable or force FSM without evaluating a corrected REST contract. |
| Header created but child failed | Record partial success and returned parent ID, independently read back header and lines, and stop. Do not re-POST the header, silently delete it, or call the schedule complete. A recovery preview must cover only the remaining verified delta. |
| UI autocomplete incident | Classify transport/environment or Fusion API failure with the actual field and diagnostic. The observed Computers incident occurred in Expenditure Type; do not turn it into a resource membership rule or retry a dispatched write |
| Person/Nonlabor unordered input supplies both amounts | Report the conflicting Rate and Markup values and require the intended amount; do not invent UI entry order or silently discard a supplied value |
| From Date default authority missing | needs_input for only the affected new line; preserve explicit dates and continue independent supported checks |
| Delete unavailable or disabled for a line | Report selected row, action availability and supported eligibility evidence; do not infer the reason from toolbar placement or attempt a different route |

## Observed UI Messages

These are messages actually observed in the 2026-10-14 UI tests, not a promise that another subtype, release or import adapter emits the same text. Input predicates are owned by ora_input_validation.md and design predicates by ora_design_enforcement.md. Offline findings must be labeled FSCR validation results; retain Oracle codes only as observed reference messages unless returned by the selected operation. Preserve multiple returned messages rather than reducing them to one generic error.

| Condition | Message | Evidence Scope |
|---|---|---|
| Rate and Markup both blank | You must supply either a rate or markup percentage. (PJF-2235533) | Resource Class, Person and tested Nonlabor UI lines |
| Nonlabor Rate Required unchecked and no Markup | You must provide a markup percent value for the provided expenditure type. (PJF-2235133) | Observed alongside PJF-2235533; Rate input unavailable |
| Job Set absent | You must provide a job set for a job rate schedule. (PJF-2235114) | Job header |
| Job line Rate absent | Error: A value is required. / You must enter a value. | Generic inline required errors; no PJF code captured |
| Project Role line Rate absent | You must provide a value for the Rate attribute. | Project Role modal; no code captured |
| From Date after To Date | Error: You must enter a from date that's on or before the to date. | Resource Class date test; equality accepted |
| Same Resource Class key with overlapping ranges | A rate with an overlapping date range already exists for this resource class. (PJF-2235677) / Revise at least one of the date ranges to remove the overlap. | Inclusive endpoint overlap observed for Resource Class only |
| Header Delete with at least one child line | You can't delete this rate schedule because it contains one or more rate schedule lines. (PJF-2235397) | Persisted disposable Job header; no deletion occurred |
| Attempted Project Role text did not resolve | Error: Autocompletion failed / Please select an item from suggestions | One unresolved text attempt; suggestion selection recovered; not a prohibition on all typed names |
| Expenditure Type autocomplete application incident | An application error occurred. See the incident log for more information. | Incident 13 observed; environmental diagnostic, not a business rejection |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Identity/date/value failure | Correct input |
| Dependency | Required mutation baseline/capability/use/package missing | Complete affected mutation dependency; continue independent supported checks |
| REFERENCE_UNRESOLVED | Unsupported LOV authority or unverified eligibility parity | Warning, blocking=false; preserve supported representation and continue without waiver |
| Conflict | Immutable/overlap/dependency/use conflict | Correct or preserve |
| Unsupported | No complete route or forbidden fallback | Stop |
| Approval blocker | Preview absent/changed/declined | Stop |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation | Target, route, set/name/type/ID, immutable fields, subtype keys, interval/value/reference/use findings |
| Preview | REST method/URL/payload or FSM members, stable IDs, before/after lines, precedence/copy/delete impact, checksum |
| Result | Route-specific HTTP/Data Loader status, expected/observed header and child counts, target/checksum, errors and independent read-back comparison of every requested field; a successful process/header alone is insufficient |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Ambiguous/capability/reference/use unknown | Do not guess; distinguish nonblocking LOV-authority warning from mutation capability/use gates |
| Duplicate/overlap or active-use destructive conflict | Do not write |
| Route incomplete/changed after approval | Do not split/fallback |
| Preview/approval absent | Do not execute |
| Failure | Do not retry/claim success |

After a failed POST, independently check exact set/name/type identity and any relevant child lines before preparing a correction. Preserve the consumed preview and failure receipt. A corrected endpoint, field set, staged call sequence, or FSM route requires a new immutable preview/checksum and fresh approval; it is not a retry under the old approval.

## Regression Review Cases

| Case | Expected result |
|---|---|
| Root Resource Class POST contains ResourceClassName based only on a GET line and public schema | Block before preview: target root-field write evidence missing |
| Target rejects root ResourceClassName, while documented child uses that field | Diagnose endpoint-specific mismatch; discover child contract, not blanket field prohibition or automatic FSM fallback |
| Header and Resource Class child have exact supported request fields and references | Allow a complete two-call preview with returned-ID binding; no mutation until approval |
| Generic child metadata describes Job fields only | Block Resource Class line readiness as unknown; do not use Job attributes or assume other subtypes |
| Child fails after header succeeds | Report partial success and reconcile; no duplicate header submission |
| Failed flat-create approval is supplied for a corrected two-call create | Reject approval reuse; require the new preview checksum |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RATE.EXECUTION_GATE | decision | 9 | execution_gate | ready->RATE.RETURN_SUCCESS;warning->RATE.RETURN_SUCCESS;not_ready->RATE.RETURN_ISSUES;declined->RATE.RETURN_REFUSAL | RATE.ENFORCE_DESIGN | stop | Return supported validation with warnings; writes still require route-specific approval and other mutation gates |
| RATE.RETURN_SUCCESS | terminal | 10 | terminal | none | RATE.EXECUTION_GATE | continue | Supported validation complete, with explicit warnings if any; do not claim skipped checks passed or a Fusion write occurred |
| RATE.RETURN_ISSUES | terminal | 11 | terminal | none | none | continue | Correctable issue |
| RATE.RETURN_REFUSAL | terminal | 12 | terminal | none | none | continue | Unsupported/unsafe/declined action |

For warning outcomes, retain resolver, CSV field, proven representation, skipped membership/eligibility check and next evidence required. Natural-language input is not itself an error; ask only for actual ambiguity or a missing canonical representation needed for supported payload construction. Terminal success means the supported validation path completed, not that all memberships were verified.

For independent verification, read the complete selected set/name/type scope with all child pages and compare canonical identities, dates, optional qualifiers, UOM and amounts to the immutable candidate. In the UI, reopen and search via QBE before declaring a fixture absent; the initial visible page is not a complete baseline. QBE returned all five test headers; independent detailed read-back was captured for Job and Resource Class. Person, Nonlabor and Project Role header persistence was observed, but complete child re-verification must still be performed for a future execution claim.

## Evidence Limits

| Behavior | Required Treatment |
|---|---|
| Default date clock/timezone | UI default observed; source clock unresolved; use ora_defaulting_rules.md authority gate |
| Header required-field omission messages | Required asterisks visible; individual omission messages not all tested; do not invent message text |
| Empty-header and actual line deletion | Not executed; require supported operation and eligibility evidence; no invented success, cascade or absence-of-use proof |
| Why Delete is unavailable for particular lines | Unresolved user observation; availability is not proof of the cause |
| Numeric zero/sign/precision/range | Presence is distinct from eligibility; validate evidenced route metadata, not guessed limits |
| Used transactional history protections | Not tested in UI; preserve evidenced consumer/policy protection, never infer from date alone |
| REST/FSM parity with UI | Separate operation-specific contract; UI evidence alone cannot prove writable shape or import errors |

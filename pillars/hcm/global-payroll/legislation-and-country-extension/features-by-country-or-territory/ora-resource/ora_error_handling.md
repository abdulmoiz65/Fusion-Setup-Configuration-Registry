# Features by Country or Territory Error Handling

This file owns task-specific execution gates, outcome interpretation, verification,
diagnostics, and retry boundaries. The source document's proposed clarifications
were accepted for this initialization; its open decisions and unexecuted tests
remain open. The task graph returns rule results to its caller. It contains no
Fusion write action and does not replace core.data-loader.

## Execution Phases and Handoff

| Phase | What Must Happen | Result Meaning |
|---|---|---|
| Preparation or Search | Run the input, applicable lookup, dependency, default, and design rules for the requested scope | Return validated facts, candidates, decisions, and blockers; no mutation has occurred |
| Final pre-approval validation | The routed core.data-loader workflow prepares and validates the exact immutable archive and invokes Task Hook; evaluate these task rules on that artifact before approval feedback | A passed task check is one preflight result, not upload approval or load success |
| Submission | Return control to core.data-loader for its own exact-artifact approval, integrity checks, upload, and initiation | Do not implement a write, OAuth flow, loader adapter, or alternate import route in these resources |
| Later status and verification | When the active workflow selects a status or verification step and load results are available, run the applicable read-only rules using the submitted target plan and baseline | Distinguish processing results from verified business postconditions for each target |

## Execution Gates

| Gate | What Must Be Shown |
|---|---|
| Authoring readiness | Current compiled registry, matching Markdown sources and task identity, normal planner result, and all missing contract fields; an initial registry containing reachable unresolved contracts is incomplete |
| Workflow preflight | Selected environment identity, operation, required read/write privileges, effective catalog flags, registered BO and current template, source and destination paths, payload/ZIP shape, and applicable core.data-loader checks |
| Business plan | Exact resolved targets, requested operation and per-row action, branch-specific values, excluded/protected/unchanged/blocked groups, and defaults awaiting confirmation; unresolved decisions cannot become write rows |
| Empty or canceled plan | Report not submitted or no change required; do not generate an empty DAT, upload, or submit a load |
| Baseline freshness | Perform any required reread during final pre-approval validation; rebuild and revalidate if the baseline differs. A reread does not provide an atomic concurrency guarantee |
| Approval owner | Use core.data-loader and, where applicable, core.runbook approval for the exact environment, operation, and immutable artifact. Do not add a second task-specific approval of the same load |
| After approval | Follow the core.data-loader integrity-only submission boundary. Do not rerun lookups, rebuild the archive, refresh metadata, or repeat Task Hook merely to submit. A material artifact/context change invalidates the approved plan and returns to fresh validation and approval |
| Initiation accepted | Return the governing Data Loader initiation result immediately. Do not automatically poll or claim completed loading or verified business success |
| Status or verification selected later | Inspect actual loader results through its declared workflow, then obtain complete target-identity reads through ora_reference_lookups.md; evaluate the postconditions below |
| Missing workflow step | Stop and disclose the missing route, contract, or evidence. Do not substitute browser navigation, direct REST mutation, SQL execution, BO registration repair, or another import utility |
| Known uncertain earlier mutation | Reconcile status and present state before any new action. Do not replay or silently change the operation |

## Verification Postconditions

| Operation | Required Evidence | Failure Interpretation |
|---|---|---|
| Search | Complete successful reads for the requested scope, resolved business presentation, and disclosed coverage limitations | Failed, malformed, or incomplete reads are unknown; they are not empty search results |
| Create | Exactly one record for each submitted target, matching all ten planned business fields in ora_defaulting_rules.md, including SeededStatus | Report missing target, duplicate identity, incorrect field, or unavailable comparison field separately |
| Update | Exact existing composite identity remains; each requested change matches the desired value and every untouched business field matches the approved baseline | Distinguish unintended business changes from server-managed audit/version changes |
| Delete | Each submitted exact target is absent after a complete successful identity-based read | A still-present target failed verification; a failed/truncated read is unknown. A target already missing in preflight was not deleted by this run |
| UPSERT | Apply Create checks to POST targets and Update checks to PATCH targets independently, including exact preserved values in the shared full profile | A matching count alone proves neither target identity nor correct values; retain successful, failed, and unknown rows separately |

## Outcome Classification

These labels describe task outcomes, not asserted Fusion API status enum values.

| Outcome | When Used | What Must Not Be Claimed |
|---|---|---|
| Not submitted | Invalid, ambiguous, protected, blocked, excluded, canceled, or empty candidate set | No claim that an excluded or missing target was changed |
| No change required | An existing record already satisfies a request under a confirmed comparison policy and no PATCH was submitted | Do not use unresolved null/PER equivalence to infer this outcome |
| Load succeeded, verification pending | Actual processing succeeded but the required business post-read is missing or incomplete | No verified-success claim |
| Verified success | The submitted row's postcondition is confirmed by complete evidence | Do not generalize one verified row to the whole file |
| Failed | A known processing or business validation failure is established | Do not infer file-wide rollback or failed adjacent rows |
| Outcome unknown | Timeout, interrupted processing/read, incomplete result, or missing evidence prevents classification | Neither success nor confirmed failure |

## Error Situations

| Situation | What Should Happen |
|---|---|
| Invalid or ambiguous lookup input | Group affected inputs and return candidates or correction requirements. Apply the design policy for explicit exclusion; never silently discard or choose a match |
| Read/authentication/authorization/transport failure, missing items, malformed response, or incomplete pagination | Mark the result unknown, retain the affected phase, and stop dependent absence, eligibility, or verification conclusions |
| Unsupported attribute, missing concrete Update change, or conflicting target/value/action | Return the input or design finding and obtain one unambiguous request; do not execute a reduced interpretation and claim completion of the original request |
| Protected or unknown Delete eligibility | Apply ora_design_enforcement.md before submission and explain protected versus unknown state accurately |
| HZ-120124: You must enter a valid address style for the territory code. | Report the affected target/style, use resolve_address_style_by_territory to obtain valid options through the declared read step, and rebuild validation after correction. Do not hard-code the recorded AF result as a universal rule |
| REST surrogate ID LegislationApplicationKey could not be resolved from user keys for PATCH logical line id <logical-line-id> | Check exact current identity and supplied ApplicationId/LegislationCode against the deployed BO derivation through core.data-loader preflight/diagnostics. Do not invent a surrogate or modify registration automatically |
| Direct surrogate input was rejected as not a whole number | Preserve the documented internal derivation route. Do not retry the unsupported composite-string input or assume its datatype contract changed |
| URL request parameter ParameterKeys cannot be used in this context. | Correct request construction using the owning lookup contract: finder arguments belong inside finder, not as outer parameters |
| Loader failure or partial processing | Preserve successful, failed, and unknown row outcomes and actionable errors. Direct POST/PATCH/DELETE is never a fallback |
| Verification discrepancy | Name the actual missing, duplicated, incorrect, unexpectedly changed, or unverifiable business result per target |
| Process timeout | Stop waiting at the governing workflow limit. Report environment, operation, task/job, available ProcessId or request ID, last status, elapsed wait, and the declared next-check path without starting another load |
| Failed Fusion job | Retrieve available status and ProcessLog/error detail only through the selected workflow; retain sanitized diagnostics, partial successes, and an errors array/nonzero failure result |
| Artifact persistence failure | Stop before relying on an unavailable or unsafe artifact. Report the failed destination or integrity check and repair the workspace issue before a new approval-bound action |
| Open decision or incomplete authoring contract | Return the decision ID and owning source field; leave it unresolved for a later authoring update. Initialization is not a readiness waiver |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | Missing, malformed, unsupported, conflicting, or ambiguous inputs | Correct or explicitly resolve the affected input; rerun validation |
| catalog mismatch | Effective task flags, BO identity, profile, or deployed template disagree | Resolve the exact catalog/metadata mismatch in the owning workflow |
| auth/authz | The declared read or loader route lacks valid identity or privileges | Use its declared authentication recovery; an eligible cached-token 401/403 refresh is allowed at most once, never as automatic mutation replay |
| transport/environment | Host/environment identity, connectivity, or complete-read evidence fails | Confirm the selected environment and read outcome before dependent decisions |
| Fusion API | A returned API or business diagnostic rejects the request | Preserve the exact diagnostic internally and present the actionable business correction |
| process timeout | The selected workflow reaches its polling deadline | Stop, retain external correlation and last status, and give a later check path |
| process failed | Actual import/load/job or verification failure is known | Preserve successful rows and errors; reconcile before any proposed retry |
| artifact persistence | Required source, archive, diagnostic, or state cannot be stored/read safely | Resolve path/integrity/storage failure before continuing |
| approval blocker | Required scoped approval, immutable artifact, workflow step, or authoring contract is absent | Return the blocker to the owning workflow; do not substitute an execution route |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| User-facing result | Business names and resolved labels, operation, actual per-target outcome, actionable error, and one safe next step; use the governing Data Loader report conventions |
| Runtime diagnostics | Under the selected project workspace, retain redacted status, stage, failure class, message, recommended action, environment reference, artifact references, and permitted external correlation IDs |
| Protection of evidence | Never copy HAR sessions, hosts, cookies, authorization headers, tokens, credentials, private keys, customer payloads, or production-sensitive values into tracked resources or project artifacts |
| Evidence provenance | Source-recorded execution, locally inspected fixture shape, historical HAR observation, newly accepted requirement, and unexecuted test remain distinct |
| Completion handoff | Return task code/name, phase, terminal rule, completed path/outcomes, validated facts, blockers, verified side effects, safe next action, and resume context to the invoking validator |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Unknown prior POST/PATCH/DELETE or loader result | No automatic mutation/import/job retry without idempotency evidence or explicit approval under the selected workflow; inspect prior results and current state first |
| A POST might already have succeeded | Do not resubmit blindly or silently convert it to PATCH. Recompute the proposed action after reconciliation |
| Mixed file failure | Do not assume atomicity, rollback, row execution order, or successful-row compensation |
| Compensation is proposed | Do not delete successful records unless separately authorized and eligible under the Delete contract |
| Direct REST or database access appears possible | Do not bypass core.data-loader or run the documented surrogate SQL at runtime |
| Raw code or a label is unavailable | Do not invent translations, seeded-state meanings, LOV choices, or unknown DDF mappings |
| Runtime decision remains open | Do not resolve D01-D10 from a successful adjacent example or an existing registry |
| Authoring initialization completes | Do not claim current deployment, live mutation, tested locale/concurrency, or complete execution readiness |

## Validation Backlog

The following source tests are retained for later authorized validation. None was
executed in Fusion during initialization; ZIP inspection validates fixture shape
only. Synthetic tests do not replace missing Fusion contract evidence.

| Test ID | Priority | Required Follow-up | Acceptance Evidence |
|---|---|---|---|
| T01 | High | Mixed UPSERT post-read | Created targets match their plans; updated target matches changed and preserved values |
| T02 | High | Partial Update with deliberate nondefault untouched fields | The other two mutable values remain unchanged |
| T03 | High | Omitted values in both UPSERT branches | Defaults apply only to new records; existing records preserve omissions |
| T04 | High | Small-page filtered and LOV queries | Later-page matches affect ambiguity, absence, and verification correctly |
| T05 | High if template changes | Validate proposed template exclusions and regenerate | Internal surrogate derivation and all three profiles still work; no registration change is part of this initialization |
| T06 | High for complete extension search | Resolve D01 and test null/PER search, selection, reset, and no-op semantics | Approved representations are found without unintended normalization |
| T07 | Medium | Create invalid territory/style and Update valid style transition | Target-specific validation blocks the invalid value and permits an evidenced valid transition |
| T08 | Medium | Authorized predefined-record Update | Permitted editable changes and preserved identity/protection are demonstrated |
| T09 | High | Controlled mixed-row failure and separately approved retry | Committed, failed, and unknown rows are distinguished; no blind repeat or assumed rollback |
| T10 | High | Failed auth/read and malformed/incomplete response | No false missing, invalid, or deleted classification |
| T11 | High; synthetic permitted | Duplicate aliases, conflicting/disjoint values, invalid/ambiguous groups, all excluded, cancel, and unknown protection | At most one authorized row per exact target; blocked, empty, and canceled requests do not write |
| T12 | Medium | Non-English session and differing conversation language | Actual backend label/locale behavior is observed without changing internal codes |
| T13 | Medium | Intervening change between plan and submission | Approved stale-baseline policy detects/replans or discloses the concurrency limitation |
| T14 | Medium | Apostrophes, accents, pipe/newline text, query and URL boundaries | Supported escaping preserves literal values and DAT column structure |
| T15 | Medium | Multiple Update with distinct target-specific values | Global and per-record values remain associated with the intended exact target |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FBCT.CHECK_EXECUTION_BOUNDARY | decision | 60 | execution_gate | ready->FBCT.COMPLETE;blocked->FBCT.HANDLE_ISSUES | FBCT.ENFORCE_DESIGN | stop | Evaluate only the selected phase and its applicable readiness, handoff, or verification gate; never perform a write |
| FBCT.COMPLETE | terminal | 70 | terminal | none | FBCT.CHECK_EXECUTION_BOUNDARY | continue | Return accumulated task-rule results for the selected phase; a preparation pass is not load success |
| FBCT.HANDLE_ISSUES | step | 80 | error_handler | reported->RETURN_ISSUES | none | stop | Any failed input, lookup, dependency, default, design, readiness, processing, or verification gate |
| RETURN_ISSUES | terminal | 90 | terminal | none | none | continue | Return classified issues and safe resume information without an undeclared action |

# Enterprise Shifts Error Handling

## Source Basis

- Enterprise Shifts Rest Describe, Confluence page 21451526148, version 3
- Enterprise Shifts Test Technical Design Document for FSCIR, Confluence page 21452837175, version 4
- User-Facing Value Resolution Policy, user-provided authoring source, received 11 August 2026
- Enterprise Shifts UI does not provide shift deletion, user confirmation, 11 August 2026
- Enterprise Shift name, field-value precedence, and default-origin display rules, user-provided, received 19 August 2026
- Automatic final Data Loader completion and read-back verification, user-provided, received 19 August 2026
- Dependent-workflow handoff and final-result disclosure policy, user-provided, received 19 August 2026
- Active-workflow-context inspection policy, user-provided, received 19 August 2026
- Generalized dependent-flow resume prompt policy, user-provided, received 19 August 2026
- Always poll Enterprise Shifts loads automatically after approval, user-provided, received 20 August 2026
- Terminal Enterprise Shifts result must include a business-only summary after success or error, user-provided, received 10 September 2026

## Error Situations

| Situation | What Should Happen |
|---|---|
| One or more required inputs or positive work duration are missing or invalid | Stop before lookup or preview and request all unresolved required inputs together by their verified user-facing labels or business purposes; do not request optional fields |
| Shift name, item identity, or category lookup returns zero or many matches | Stop and describe the unresolved or ambiguous business selection without exposing lookup values, record keys, request paths, or internal field names |
| Time serialization, time-zone interpretation, or 15-minute behavior is unverified | Stop and request controlled target evidence; do not copy an example as a production contract |
| Complete Summary cannot be generated entirely from verified structured fields | Stop before provider-owned approval. Do not substitute warnings, diagnostics, technical notes, or unverified values for the required business-only summary. |
| Fusion returns o:errorDetails | Preserve the first redacted detail and available correlation identifiers; leave the candidate uncommitted |
| Update has no changed fields | Return no-change and do not invoke PATCH |
| Create, update, upsert, action, or batch outcome is uncertain | Stop before retry and reconcile through a read-only item or finder request |
| An approved asynchronous request reaches failure, timeout, partial success, or an uncertain terminal result | Return a business-only terminal result with the Shift Name, business-friendly outcome, known completed and failed counts when available, and one safe resume or investigation action. Do not report final success, end with a generic Data Loader status table, or retry the submission automatically |
| A terminal success result does not have one matching Enterprise Shift read-back, or the read-back differs from approved values | Report the verification mismatch in business terms, retain the comparison evidence, and do not retry the submission automatically |
| A verified Enterprise Shift is a documented prerequisite for another workflow | Prompt: Would you like to resume {parent workflow}? Identify that the dependent workflow has not started. On confirmation, return its retained identity and safe resume stage; do not start, preview, approve, submit, create, update, import, or load the dependent workflow from Enterprise Shifts. |
| A verified Enterprise Shift has no documented parent workflow | Return the standalone verified Shift summary and do not show a resume prompt. |
| A prerequisite with a documented dependent workflow fails, times out, is partial or uncertain, or has a verification mismatch | Do not offer dependent-workflow continuation; preserve the last known result and give one safe investigation or resume action |
| An Enterprise Shift request starts while another workflow is active | Inspect the active workflow context and its applicable task resources before treating the Shift as standalone. Retain and disclose a parent handoff only when one current parent explicitly documents Enterprise Shifts as a prerequisite; otherwise continue standalone or stop on ambiguity. |
| A 400, 401, 403, 404, 409, 412, 429, or 5xx response occurs | Classify the observed response without claiming that undocumented statuses are guaranteed for this resource |
| Advanced-search filters, sort, or response members are needed beyond documented fields | Stop and retain the unexpanded object contract as unresolved |
| An internal value has no verified display mapping | Stop recommendation generation, mark the selection unresolved or incomplete, and request the displayed label or relevant lookup information without repeating the raw value |
| A supplied internal value conflicts with a supplied display label | Report inconsistent selection information without exposing the internal value |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required, length, type, duration, offset, day, or read-only-field rule fails | Correct the exact input and rerun validation |
| Lookup gap | Shift, category, or lookup contract is zero, many, unavailable, or TBD | Correct source values or supply the missing source-backed contract |
| Auth or authz | Authentication or authorization fails | Refresh an approved cached token once for a read if applicable, then stop |
| Transport or environment | Target or network fails before a side effect | Retry only bounded idempotent reads |
| Fusion API | Fusion rejects a request or returns a business or concurrency conflict | Preserve redacted error evidence and do not replay |
| Approval blocker | Exact preview, writable executor, or current approval is absent | Complete the separate runbook gate |
| Unsupported operation | Shift deletion, unsafe upsert, undocumented batch action, or invented custom-action shape is requested | Reject the unsupported operation and use only a supported source-backed path |
| Uncertain side effect | A mutation timed out or its response was lost | Reconcile with read-only retrieval before considering another write |
| User-facing value resolution | A selected value or field cannot be mapped to verified business terminology | Return an unresolved business-language result and do not recommend from the unresolved value |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation | Task business name, affected user-facing fields, business-language failed checks, lookup blockers, and unresolved source contracts; keep task codes and internal field names private |
| Preview handoff | Target environment, operation in business terms, resolved business identity, final business values with each system-populated documented default labeled Default, sanitized category evidence, current-record comparison, and approval receipt without raw internal identifiers |
| Final completion | A successful result uses the Complete Summary and Defaults Applied sections from verified saved Enterprise Shift details, including system-populated documented defaults labeled Default. A failed, timed-out, partial, uncertain, or mismatched result uses the Shift Name, business-friendly outcome, known completed and failed counts when available, and one safe next action. Never end either result with a generic Data Loader status table. |
| Dependent-workflow handoff | When the active workflow context verifies one documented parent workflow and the Enterprise Shift is verified, show: Would you like to resume {parent workflow}? State that the dependent workflow has not started. On confirmation, return resume_requested with the retained parent identity and safe resume stage; do not imply that the dependent object was prepared, approved, or submitted. When no documented parent exists, omit this disclosure and show only the standalone Shift result. |
| Failure | Stage, business-language failure class, HTTP status when useful, sanitized Fusion detail, and safe next action; keep methods, paths, correlation identifiers, service aliases, and internal values private unless a separate restricted technical diagnostic is explicitly requested |
| Verification | Resolved business identity, persisted user-facing values from a read, unchanged unrelated business fields, documented defaults labeled Default only when system-populated, and whether any side effect remains uncertain |
| Unresolved selection | State that the selected value could not be resolved to a business label; do not display the value, guess a meaning, or expose a code-to-label mapping |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing exact time, lookup, upsert, or concurrency contract | Do not infer, fabricate, or silently default it |
| Category meaning is supplied | Do not submit Meaning as ShiftCategory without resolving the exact LookupCode |
| Mutation lacks current approval | Do not construct or submit the write from these resource files |
| Mutation fails or times out | Do not automatically retry POST, PATCH, custom action, or batch |
| Asynchronous completion is failed, timed out, partial, uncertain, or mismatched | Do not automatically retry upload, initiation, create, update, import, or load |
| An active workflow context is absent, ambiguous, stale, conflicting, or does not document Enterprise Shifts as a prerequisite | Do not present a dependent-workflow message or infer a handoff from business-use wording |
| A verified Enterprise Shift is standalone | Do not show a resume prompt or a dependent-workflow message |
| A verified Enterprise Shift is a prerequisite for one active documented parent workflow | Do not automatically submit, create, update, import, or load the dependent workflow; rebuild its preview when the verified Shift changes its approved values, then obtain its separate current explicit approval |
| Delete is requested | Do not offer or attempt deletion because the Enterprise Shifts UI does not provide that action |
| Advanced-search action is requested in batch | Do not include it because live describe reports batchEnabled false |
| A user-facing response contains an internal value | Do not send it; resolve and sanitize the response first |
| A label would be inferred rather than verified | Do not remove prefixes, replace underscores, change capitalization, expand abbreviations, or infer from a similar value |
| A technical URL is included | Do not include a real record key; use a descriptive placeholder |
| A recommendation depends on an unresolved value | Do not recommend; return an unresolved or incomplete result |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ES.EXECUTION_GATE | decision | 60 | execution_gate | ready->ES.WAIT_FOR_FINAL_COMPLETION;blocked->ES.HANDLE_ERROR | ES.ENFORCE_DESIGN | stop | Before handing validated facts to a separate writable runbook and automatic final-completion verification |
| ES.HANDLE_ERROR | step | 70 | error_handler | handled->ES.RETURN_ISSUES | none | stop | Any validation, lookup, dependency, default, design, or handoff failure |
| ES.RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| ES.READY | terminal | 90 | terminal | none | ES.WAIT_FOR_FINAL_COMPLETION | stop | An approved asynchronous request reached terminal success and its Enterprise Shift read-back matched the approved configuration. When one documented parent workflow is retained, prompt the user to resume that named workflow and return resume_requested only after confirmation; otherwise return the standalone verified Shift summary. |

# Supplier Qualification Questions Error Handling

Classify failures, preserve the request artifact, and stop before another execution attempt. This guidance does not retry or call Fusion.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Task checks pass and the selected Data Loader session is ready to build its preview | Return ready_for_preview without requiring an existing preview or user approval. This result completes task validation only; it does not authorize upload, initiation, or a question REST write |
| No supported execution workflow is selected, or validation or lifecycle checks remain unresolved | Return handoff_blocked and stop before preview; do not substitute a direct REST write or another executor |
| Data Loader has returned its final validation preview | Wait for contextual user approval of that preview, then approve only the same retained session and preview ID through core.data-loader. That workflow owns the execution approval; do not add a second task approval or reuse approval from another session |
| Required field or paired code/display value is missing | Report the missing fields and return the request for correction |
| QuestionId lookup returns no resource | Stop the update, revision, delete, activation, inactivation, or status PATCH path and ask for a valid identifier |
| Question name is duplicated | Stop preparation and require a unique Question name |
| A supplied meaning or code value does not match its fixed common lookup type | Stop preparation and identify the attribute pair and lookup type that requires correction |
| A supplied meaning and code resolve to different lookup records | Stop preparation and require a matching pair or only one authoritative value |
| A conditional Input Box, preferred response, supplier-attribute, scoring, or acceptable-response rule fails | Identify the controlling question type, response type, responder type, mapping, or scoring method and return the request for correction |
| A lifecycle status PATCH is ineligible | Stop and explain the required current status and permitted target status; do not substitute a different action or target status |
| Fusion rejects an inactivation PATCH for an Active question because the operation is Draft-only | Classify as a lifecycle blocker, retain redacted error evidence, and stop; do not retry or substitute another lifecycle action without a separately documented path, new preview, and approval |
| A lifecycle status PATCH lacks a selected authorized executor or immutable request artifact | Stop before execution and retain the validated lifecycle evidence for the approved execution workflow |
| A save requires a new revision or confirmation | Preserve the pending change and request the documented revision, propagation, or inactivation confirmation |
| A translation create/delete or attachment update is requested | Stop; the functional rules prohibit that action in the relevant edit state |
| Fusion rejects a request | Persist the redacted response details, target environment, method, path, and request identifier when available; do not retry automatically |
| Authentication or authorization fails | Classify the failure as auth/authz and stop; refresh a cached token only once when the active workflow permits it |
| Transport failure or timeout occurs | Classify the failure as transport/environment or process timeout, retain elapsed time and request context, and use the approved next-check path |
| A live request needs to be changed after preview | Invalidate the preview and obtain a new explicit approval for the immutable request artifact |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | Required REST field, limit, flag, encoding, or code/value pair is invalid | Correct the source data and rerun validation only |
| auth/authz | Fusion rejects the caller identity or privilege | Verify role and privilege prerequisites; do not change data |
| transport/environment | Fusion endpoint cannot be reached | Record environment and transport detail, then use the approved retry or next-check path |
| Fusion API | Fusion returns an API validation or processing failure | Preserve redacted response diagnostics and correct the request before another approved attempt |
| approval blocker | The selected execution workflow has not received approval bound to its current preview | Stop before the live operation; absence of approval during task validation does not block creation of that workflow's preview |
| lifecycle blocker | Question status or revision does not permit the requested edit, activation, inactivation, or draft delete | Use the permitted lifecycle path |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before a lifecycle status PATCH | Exact target environment, PATCH method, question resource path, target status, operation, and immutable request artifact |
| After Fusion API failure | Failure class, redacted message, environment, method, path, external request identifier when available, and recommended next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A create, update, revision, delete, activation, inactivation, or status PATCH lacks explicit approval | Do not invoke the REST endpoint |
| A REST request fails | Do not retry a POST, PATCH, DELETE, or revise action without idempotency or explicit approval |
| Credentials, tokens, or sensitive payload values appear in diagnostics | Do not persist or expose them |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SUPQ.GATE | decision | 5 | execution_gate | ready_for_preview->SUPQ.READY;handoff_blocked->SUPQ.BLOCKED | SUPQ.DESIGN | stop | Create preparation, or existing-question preparation after SUPQ.QUESTION_LOOKUP succeeds: verify completed task checks and a supported selected execution workflow; a preview and execution approval are not required at this stage |
| SUPQ.READY | terminal | 6 | terminal | none | SUPQ.GATE | stop | Task validation passed and the selected workflow may build its preview; execution approval remains pending in that workflow, and this terminal authorizes no Fusion write |
| SUPQ.BLOCKED | terminal | 7 | terminal | none | none | stop | A validation, lookup, design, preview, approval, or execution gate blocks progress |

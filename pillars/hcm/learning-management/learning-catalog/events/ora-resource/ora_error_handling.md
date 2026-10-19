# Events Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| One input row is missing identity or contains an unsupported operation | Mark only that row blocked, show the exact issue, and continue read-only evaluation of unrelated rows |
| A Draft omits activation-only schedule, capacity, or resource data | Return Draft With Activation Gaps, preserve ORA_DRAFT, and do not describe it as an error or activation-ready result |
| A supplied schedule, dependency, field, or lifecycle value is invalid | Stop that row before preview and name the failing field, resolver, or transition |
| Instructor, classroom, course, or supplier lookup is empty, ambiguous, inactive, unavailable, or insufficient | Stop the affected active-schedule row and return sanitized exact-match, status, availability, or capacity evidence |
| Provider validation contract is absent or validateProviderUser fails or is indeterminate | Stop only provider-backed webinar setup; do not infer payload fields, success semantics, or a requirement for a fixed meeting URL |
| An ad hoc resource is requested | Stop only that row until an approved global identity and availability provider exists |
| Preview or current-state fingerprint is stale | Invalidate the affected row approval, refresh its event and resources, and rebuild its preview |
| A write or action result is uncertain | Do not retry; reconcile by safe reads and report the row indeterminate when evidence remains inconclusive |
| A documented child operation returns an asynchronous tracker and polling times out | Stop polling and return the operation, sanitized process identifier, last status, elapsed time, and safe next check; do not infer asynchronous parent processing |
| Readback differs from the approved preview | Report the exact row as partial or failed verification without claiming success |
| An earlier row has an uncertain outcome | Stop later writes that depend on it; unrelated independently approved rows may proceed only when their evidence remains fresh |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| DRAFT_WITH_ACTIVATION_GAPS | Draft creation is valid but activation-only evidence is intentionally incomplete | Create only after approval, then complete and separately approve activation later |
| MISSING | Required row input, approval, provider contract, lookup, or exact identity is absent | Supply or resolve the named blocker |
| AMBIGUOUS | A finder or provider result is not exactly one expected match | Provide a stronger business key and rerun the row |
| UNSUPPORTED | Finalize, parent delete, exposed upsert, unresolved ad hoc resource, or another operation has no approved route | Select a supported operation or defer the affected row |
| STALE | Event, activity, enrollment, resource, target, operation, or payload evidence changed after preview | Refresh, rebuild preview, and approve again |
| PARTIAL | A side effect occurred but one or more approved assertions failed readback | Preserve verified state and require a new plan; do not retry automatically |
| INDETERMINATE | The outcome cannot be proven after safe reconciliation | Escalate with sanitized identifiers; do not replay the write |
| FAILED | Validation, execution, polling, or verification conclusively failed | Review sanitized diagnostics before a separately planned attempt |
| ALL_GOOD | Every assertion for that row is freshly verified | Return the completed row result and run record |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before preview | Row key, target alias, operation, event or create identity, applicable activation gaps, dependencies, and blockers |
| Preview | Exact selected row set, parent and child intent, schedule and learner impacts, resources, lifecycle transition, concurrency limitation, expected readback, and immutable fingerprint |
| Approval | Whether fresh explicit approval matches the exact selected-row fingerprint |
| Before submit | Fresh state and resource comparison; any changed evidence invalidates only affected row approval |
| After submit | Sanitized request or process identifier when returned, verified side effects, readback differences, result category, and one safe next action per row |
| On mixed input | Ready, Draft-with-gaps, blocked, no-change, executed, and verification results remain visibly separated by stable row key |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Approval is absent, stale, or applies to a different row set | Do not call event or activity POST, PATCH, DELETE, or copy |
| An incomplete Draft is requested | Do not reject it merely for activation-only omissions and do not activate it |
| An ad hoc resource provider is absent | Do not invent a resource endpoint, identity, quantity, conflict result, or status |
| Provider validation payload or result semantics are opaque | Do not invent request members, infer success from HTTP status, or reuse another provider's contract |
| Finalize or parent-event delete is requested | Do not infer an action from lifecycle, deletion-reason, or keep-completions fields |
| Upsert appears in Describe metadata | Do not expose it; preserve explicit create-versus-update planning and approval |
| No documented tracker was returned | Do not poll or claim asynchronous Event processing |
| A write outcome is uncertain or partial | Do not replay, compensate, or delete automatically |
| Multiple rows are selected | Do not claim atomicity or let one row's approval, state, or result stand for another |
| Diagnostics are recorded | Do not persist tokens, credentials, environment hostnames, raw payloads, or sensitive response bodies |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EVT.EXECUTION_GATE | decision | 6 | execution_gate | authorized->EVT.EVALUATE_RESULT;validation_only->EVT.EVALUATE_RESULT;blocked->EVT.HANDLE_ERROR | EVT.ENFORCE_DESIGN | stop | A row has complete validation-only evidence or an immutable approved mutation preview and fresh fingerprint |
| EVT.HANDLE_ERROR | step | 8 | error_handler | disclosed->EVT.RETURN_ISSUES | none | stop | A row is blocked, stale, unsupported, failed, partial, or indeterminate at any stage |
| EVT.RETURN_SUCCESS | terminal | 9 | terminal | none | EVT.EVALUATE_RESULT | stop | The requested validation-only or mutation result is verified for all completed rows |
| EVT.RETURN_ISSUES | terminal | 10 | terminal | none | EVT.HANDLE_ERROR | stop | One or more row-scoped issues require disclosure or follow-up |

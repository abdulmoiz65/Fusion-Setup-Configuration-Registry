# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Input is invalid | Stop before preview and identify the invalid field |
| Environment cannot be resolved | Stop before Fusion execution and request the exact target |
| Fusion rejects authentication or privilege | Allow only the core cached-token refresh retry, then stop and report auth or authorization failure |
| Submission response has no requestId | Treat the outcome as uncertain and do not resubmit |
| Polling times out | Preserve the requestId and last status and offer to resume tracking |
| Parent process fails | Retrieve available full status and ECID, persist redacted diagnostics, and stop |
| Process succeeds but no locations are geocoded | Treat this as a functional result requiring log review, not as proof of transport failure |
| Artifact persistence fails | Preserve the external requestId in the response and report the persistence failure separately |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Optional parameter, date pair, polling value, or mode is invalid | Correct input and preview again |
| auth_or_authorization | OAuth or Run Geocode Loader access is rejected | Correct credentials or privilege before retrying |
| transport_or_environment | Host, DNS, TLS, or selected environment fails | Correct environment connectivity and check existing request status before retry |
| fusion_api_error | Scheduler REST rejects or returns an invalid response | Preserve the response and do not automatically repeat POST |
| process_timeout | Request remains nonterminal after the polling window | Resume the same requestId |
| process_failed | ESS reaches a terminal unsuccessful status | Review full status and process log; any replacement submission requires a new direct run request |
| artifact_persistence | Project output cannot be saved safely | Report the external requestId and correct the project path |
| execution_intent_blocker | The request does not clearly authorize a new submission | Ask one short intent question and stop without side effects |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Execution summary | Environment, filter scope, monitoring behavior, effective defaults, regeneration warning, and side effect |
| Submission success | requestId and whether polling has reached a terminal state |
| Timeout | Environment, job definition, requestId, last status, elapsed wait, and resume path |
| Process failure | Environment, requestId, last status, ECID when available, failure class, and recommended action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Direct execution intent is missing or stale | Do not submit |
| A POST response is uncertain | Do not retry or create a replacement request |
| Polling times out | Do not resubmit |
| A requestId is supplied for tracking | Do not create a new request |
| A secret or token appears in diagnostics | Do not print or persist it |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GEOCODE.BLOCKED | terminal | 10 | terminal | none | none | continue | A prerequisite, environment, or approval-independent readiness gate blocks execution |
| GEOCODE.REFUSED | terminal | 11 | terminal | none | none | continue | The request is advisory, hypothetical, or does not authorize live execution |
| GEOCODE.FAILED | terminal | 12 | terminal | none | none | continue | Input, authentication, transport, Fusion API, ESS process, or persistence handling fails |

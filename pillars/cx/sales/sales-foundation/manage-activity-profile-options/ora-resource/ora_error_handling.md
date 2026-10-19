# Activity Profile Options Error Handling and Execution Gate

## Error Situations

| Situation | Classification | Required Response |
|---|---|---|
| Missing or malformed operation, scope key, expected state, proposed value, or preview | input_validation | Stop and identify the exact field |
| Current or configured request is answered from documentation or defaults | incomplete_workflow | Normalize to Inventory or Review and execute the environment workflow |
| Environment identity disagrees with project or REST host | transport_environment | Stop before external calls and report the sanitized mismatch |
| Inventory or Review export fails or times out | process_failed_or_timeout | Preserve ProcessId and last status; continue exact live reads and disclose the reconciliation gap |
| Documented or live option is absent from export | reconciliation_warning | Continue exact Apps Common reads; never block CRUD or build a synthetic FSM package |
| Live definition, level, or required child cannot be read | fusion_api_or_privilege | Stop mutation and report the exact read failure |
| Cached token is rejected | auth_expired_or_invalid | Allow only the shared client's documented cached-token refresh behavior |
| Mutation privilege is missing | authorization_or_privilege | Stop and report FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV |
| Activity reminder channel or impact acknowledgement is missing | input_validation | Return the exact dependency evidence and stop before preview |
| More than one exact scope or dependency row resolves | catalog_or_metadata_mismatch | Stop; do not choose a row or issue a write |
| Expected state differs from latest live state | stale_state | Invalidate preview and approval; rebuild from a fresh read |
| POST is proposed for an existing row, or PATCH or DELETE for an absent row | execution_route_violation | Reclassify from exact current state and produce a new preview |
| Parent definition, audit fields, level metadata, or unrelated fields are writable in the request | input_validation | Reject and rebuild the minimal child-value request |
| Preview approval is vague, stale, or not digest-bound | approval_blocker | Stop and obtain approval for the complete immutable preview |
| Apps Common POST, PATCH, or DELETE returns an error | fusion_api_error | Preserve method, sanitized path, HTTP status, request ID or ECID, and server message; do not retry |
| Mutation outcome is uncertain | indeterminate_write | Read the exact child item before considering a new preview; never replay automatically |
| Exact post-write verification disagrees | verification_mismatch | Report the mismatch and stop; do not issue compensation |
| BulkSet row fails after earlier successes | partial_bulk_completion | Stop immediately, list verified successes and failed or unattempted rows, and require a new request for remaining changes |
| FSM ZIP, Data Loader, setup import, browser write, curl, Upsert-Mode, or task-local HTTP code is proposed | execution_route_violation | Stop and route configured-value CRUD only through core.fusion-api.apps-common |
| Effective profile value is absent | not_execution_failure | Report effective verification unavailable; do not undo configured success |
| Inventory or Review lacks complete candidate and child evidence | incomplete_workflow | Resume at ACTIVITY_PROFILE.LOOKUP_PROFILE or return the classified attempted-call failure |
| Artifact cannot be persisted | artifact_persistence | Preserve safe diagnostics in a temporary path and report the intended project path |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| READY_REVIEW | Reconciled Inventory or exact Review has complete live evidence | Return the read-only result with no mutation authorized |
| READY_APPS_COMMON | Exact immutable CRUD preview is complete and awaits or holds matching approval | Execute once only after all gates and immediate stale-state read |
| BLOCKED | Required identity, dependency, privilege, preview, or approval is missing | Resolve the missing condition; do not write |
| FAILED | Read, write, validation, verification, persistence, or graph contract failed | Disclose the classified failure and safe next action |
| PARTIAL | BulkSet stopped after earlier verified successes | Report verified, failed, and unattempted rows; require a new request for the remainder |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Mutation preview | Environment, task code, exact profile code, level and scope key, normalized operation, method, relative endpoint, current state, proposed stored value and meaning or delete fallback, Activity dependencies, minimal body or bodyless delete, verification plan, and PreviewSha256 |
| Mutation result | Matching approval, HTTP outcome, request ID or ECID when present, and exact post-write child verification |
| Inventory | Documented and export-only candidates, attempted, resolved, not-found, and error counts, unresolved codes, complete configured Site, Product, and User rows or absence, level flags, and timestamps |
| Review | Exact code, export attempt, definition, complete child rows or absence, level flags, and timestamps |
| Failure | Classification, sanitized evidence, affected target or row, verified earlier side effects, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Documentation or export-only evidence | Do not present it as current configured state or use it to select a mutation method |
| User or Product value is absent | Do not infer it from Site, defaults, export, or profileValues |
| Profile definition or metadata change | Do not mutate parent definitions, SQL validation, level metadata, descriptions, application or module identifiers, or audit columns |
| Ambiguous identity | Do not fuzzy-match codes, users, applications, channels, or stored values |
| Missing or stale approval | Do not call Apps Common POST, PATCH, or DELETE |
| Profile-value CRUD | Do not use FSM, Data Loader, shared setup import, setupTaskCSVImports, UCM, browser automation, direct curl, Upsert-Mode, or task-local HTTP |
| Write error or uncertain outcome | Do not retry, compensate, or replay without a new exact read, preview, and approval |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACTIVITY_PROFILE.EXECUTION_GATE | step | 6 | execution_gate | review_ready->ACTIVITY_PROFILE.READY_REVIEW;apps_common_ready->ACTIVITY_PROFILE.READY_APPS_COMMON;blocked->ACTIVITY_PROFILE.RETURN_ISSUES | ACTIVITY_PROFILE.DESIGN | stop | Route Inventory or Review to read-only output after completeness gates, or Set, Remove, and BulkSet to an exact immutable Apps Common CRUD preview; block missing approval, stale state, ambiguous identity, unsupported fields, unresolved Activity dependencies, or any FSM or Data Loader route |
| ACTIVITY_PROFILE.READY_REVIEW | terminal | 7 | terminal | none | ACTIVITY_PROFILE.EXECUTION_GATE | continue | Environment-backed reconciled Inventory or exact Review is ready with no mutation authorized |
| ACTIVITY_PROFILE.READY_APPS_COMMON | terminal | 8 | terminal | none | ACTIVITY_PROFILE.EXECUTION_GATE | continue | Exact Apps Common child-value CRUD preview is ready for standalone digest-bound approval and one non-retried execution followed by exact verification |
| ACTIVITY_PROFILE.RETURN_ISSUES | terminal | 9 | terminal | none | none | continue | Any validation, dependency, lookup, design, approval, execution-route, write, or verification gate fails safely |

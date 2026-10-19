# Error Handling and Execution Gate

## Error Situations

| Situation | Classification | Required Response |
|---|---|---|
| Missing or malformed operation, scope key, expected state, proposed value, or preview | input_validation | Stop and identify the exact field |
| Current/configured request is answered from documentation or defaults | incomplete_workflow | Normalize to Inventory or Review and execute the environment workflow |
| Environment access is denied without an attempted declared route | incomplete_workflow | Attempt the selected export or Apps Common read route before classifying failure |
| Environment identity disagrees with project or REST host | transport_environment | Stop before external calls and report the sanitized mismatch |
| Catalog task or CSV support differs from generated metadata | catalog_or_metadata_mismatch | Report exact catalog evidence; do not reinterpret the task identity |
| Inventory/Review export fails or times out | process_failed_or_timeout | Preserve ProcessId and last status; continue exact live reads and disclose the reconciliation gap |
| Documented/live option is absent from export | reconciliation_warning | Continue exact Apps Common reads; never block CRUD or build a synthetic FSM package |
| Live definition or required child cannot be read | fusion_api_or_privilege | Stop mutation and report the exact read failure |
| Cached token is rejected | auth_expired_or_invalid | Allow only the shared client's documented cached-token refresh behavior |
| Mutation privilege is missing | authorization_or_privilege | Stop and report FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV |
| Conditional dependency is missing or ambiguous | input_validation | Return exact lookup evidence; never guess a code or ID |
| More than one exact scope row resolves | catalog_or_metadata_mismatch | Stop; do not choose a row or issue a write |
| Expected state differs from latest live state | stale_state | Invalidate preview and approval; rebuild from a fresh read |
| POST is proposed for an existing row, or PATCH/DELETE for an absent row | execution_route_violation | Reclassify from exact current state and produce a new preview |
| Parent definition, audit fields, level metadata, or unrelated fields are writable in the request | input_validation | Reject and rebuild the minimal child-value request |
| Preview approval is vague, stale, or not digest-bound | approval_blocker | Stop and obtain approval for the complete immutable preview |
| Apps Common POST/PATCH/DELETE returns an error | fusion_api_error | Preserve method, sanitized path, HTTP status, request ID/ECID, and server message; do not retry |
| Mutation outcome is uncertain | indeterminate_write | Read the exact child item before considering a new preview; never replay automatically |
| Exact post-write verification disagrees | verification_mismatch | Report the mismatch and stop; do not issue compensation |
| BulkSet row fails after earlier successes | partial_bulk_completion | Stop immediately, list verified successes and failed/unattempted rows, and require a new request for remaining changes |
| FSM ZIP, Data Loader, setup import, browser write, curl, or task-local HTTP code is proposed | execution_route_violation | Stop and route configured-value CRUD only through core.fusion-api.apps-common |
| Effective profile value is absent | not_execution_failure | Report effective verification unavailable; do not undo configured success |
| Inventory or Review lacks complete candidate/child evidence | incomplete_workflow | Resume at SPO.LOOKUP_PROFILE or return the classified attempted-call failure |
| Artifact cannot be persisted | artifact_persistence | Preserve safe diagnostics in a temporary path and report intended project path |

## Disclosure Rules

Every mutation preview and result must identify environment, task code, exact
profile code, level and scope key, normalized CRUD operation, method, relative
endpoint, exact current state, proposed stored value and meaning or delete
fallback, dependencies, minimal body or bodyless delete, preview digest,
approval state, HTTP outcome, and exact post-write verification.

Every Inventory result must disclose documented/export-only candidate lists,
attempted/resolved/not-found/error counts, unresolved/error codes, conversion-
option canary status, and configured Site/User/Product rows plus level flags.
Every Review result must disclose the exact code, export attempt, definition,
complete child rows or absence, level flags, and timestamps.

Redact tokens, authorization headers, credentials, secrets, user GUIDs when not
required for review, and sensitive values.

## Refusal Rules

- Do not create or modify task-local, core, or shared scripts.
- Do not answer environment-backed Inventory or Review from documentation or
  export alone.
- Do not infer User or Product values from Site, defaults, or profileValues.
- Do not mutate profile definitions, SQL validation, level metadata,
  descriptions, or audit columns.
- Do not fuzzy-match codes, users, applications, templates, rules, maps, roles,
  or lookup values.
- Do not use Upsert-Mode for normal CRUD when an exact read can choose POST or
  PATCH deterministically.
- Do not call Apps Common POST, PATCH, or DELETE without the complete digest-
  bound approval and immediate stale-state read.
- Do not use FSM, Data Loader, shared setup import, setupTaskCSVImports, UCM,
  browser automation, direct curl, or task-local HTTP for profile-value CRUD.
- Do not retry or compensate for a mutation without a new read, preview, and
  approval.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SPO.EXECUTION_GATE | step | 6 | execution_gate | review_ready->SPO.READY_REVIEW;apps_common_ready->SPO.READY_APPS_COMMON;blocked->SPO.RETURN_ISSUES | SPO.DESIGN | stop | Route Inventory/Review to read-only output after completeness gates, or Set/Remove/BulkSet to an exact immutable Apps Common CRUD preview; block missing approval, stale state, ambiguous identity, unsupported field changes, or any FSM/Data Loader route |
| SPO.READY_REVIEW | terminal | 7 | terminal | none | SPO.EXECUTION_GATE | continue | Environment-backed reconciled Inventory or exact Review is ready with no mutation authorized |
| SPO.READY_APPS_COMMON | terminal | 8 | terminal | none | SPO.EXECUTION_GATE | continue | Exact Apps Common child-value CRUD preview is ready for standalone digest-bound approval and one non-retried execution followed by exact verification |
| SPO.RETURN_ISSUES | terminal | 9 | terminal | none | none | continue | Any validation, dependency, lookup, design, approval, execution-route, write, or verification gate fails safely |

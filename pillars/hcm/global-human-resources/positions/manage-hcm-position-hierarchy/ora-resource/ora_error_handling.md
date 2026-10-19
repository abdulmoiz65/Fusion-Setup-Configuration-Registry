# Manage HCM Position Hierarchy Error Handling

## Purpose

Defines task-specific failure classification, disclosure, reconciliation, and retry boundaries.

## Error Situations

| Error ID | Situation | Result Category | What Should Happen |
|---|---|---|---|
| POSH-01 | A Position or relationship is missing or ambiguous | Input validation | Stop and request one exact selector |
| POSH-01A | A Position or relationship is outside the effective range | Input validation | Stop and request a valid effective range |
| POSH-01B | Cached authentication remains invalid after one permitted refresh | Authentication | Stop and require reauthentication |
| POSH-01C | A required REST, Position-security, hierarchy, or Data Loader privilege is denied | Authorization | Stop and report the missing access without changing routes |
| POSH-01D | The declared Fusion environment cannot be reached | Transport/environment | Stop and report the environment and failed stage |
| POSH-02 | The hierarchy read is incomplete, cyclic, orphaned, duplicated, or has multiple parents | Fusion API | Stop without rendering a misleading hierarchy or authoring a workbook |
| POSH-03 | Position Hierarchy live metadata is missing, ambiguous, or differs from the workbook | Catalog mismatch | Stop and regenerate the template through Core Data Loader |
| POSH-03A | Position Hierarchy UCM template lacks METADATA&#124;PositionHierarchy or its data header | Catalog mismatch | Stop and refresh the live template through Core Data Loader |
| POSH-04 | A new child or duplicate lacks Position.xlsx or PositionHierarchy.xlsx | Artifact persistence | Stop before preview and rebuild the complete combined source set |
| POSH-04A | Position.xlsx and PositionHierarchy.xlsx use different Business Unit or Position code values | Input validation | Stop before preview and correct the combined source set |
| POSH-05 | Delete targets a Position with incumbents or child Positions | Input validation | Stop and report the dependency class without exposing restricted incumbent data |
| POSH-06 | XLSX contains guessed or mismatched IDs, an unverified relationship identifier, partial source keys, unsupported fields, or extra relationship rows | Input validation | Stop before preview and correct the complete workbook |
| POSH-07 | The immutable preview or standalone approval is missing or stale | Approval blocker | Stop before upload; changed state or source bytes require a new preview and approval |
| POSH-08 | Data Loader reaches a failed or completed-with-errors status | Process failed | Preserve the process diagnostics and stop |
| POSH-08A | Data Loader completes with partial row failures | Process failed | Preserve successful rows and row errors, then reconcile every affected Position |
| POSH-08B | Data Loader does not reach a terminal status within the allowed wait | Process timeout | Stop polling and report the process identifier, last status, and elapsed wait |
| POSH-08C | The submission outcome cannot be confirmed | Process failed | Refresh affected relationships before considering any retry |
| POSH-09 | The load completes but fresh REST reads do not prove every assertion | Verification failed | Return failed with expected and observed parents; do not report success |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A selector, date, mode, key, dependency, or combined Position source value is absent or invalid | Correct the input and restart resolution |
| Catalog mismatch | Task mode, business object, or live metadata no longer matches the contract | Restore the contract and regenerate the source |
| Authentication | Cached authentication remains invalid after one permitted refresh | Stop and require reauthentication through the authorized authentication owner |
| Authorization | A required Fusion privilege is denied | Restore the required access; do not change routes |
| Transport/environment | The declared Fusion environment cannot be reached | Restore connectivity before continuing |
| Fusion API | A read is rejected or its response cannot construct a valid graph | Preserve sanitized diagnostics and correct the request or contract |
| Artifact persistence | A required Position or Position Hierarchy workbook is unavailable | Rebuild and preserve the complete combined source set |
| Process failed | Data Loader reports failed, partial, or uncertain rows | Retrieve errors, reconcile every affected Position, and require a new correction plan |
| Process timeout | Data Loader does not reach a terminal result in the allowed wait | Report identifiers and last status; use only the status-check path later |
| Approval blocker | Exact source preview is unapproved or its fingerprint changed | Preview the current immutable source and obtain standalone approval |
| Verification failed | Fresh effective hierarchy does not match the approved assertions | Report observed state and stop without automatic replay |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before approval | Environment, operation, effective range, affected Positions, parent changes, move mode, workbook fingerprint, row count, and verification assertions |
| Loader failure | Data set, status, total, loaded and failed counts, actionable row diagnostics, and one safe next action when available |
| Uncertain or partial result | Expected and freshly observed parent for every affected Position without assuming rollback or completion |
| Combined create partial result | Whether the Position and hierarchy edge exist, each object loader status, and the safe correction path |
| Final success | Refreshed hierarchy, effective range, previous and resulting parent, affected children, pagination completeness, and verification outcome |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A direct REST write is available | Do not use it; retain the Core Data Loader route |
| A Position must be created or deleted | Do not use Position Hierarchy; delegate to Manage Positions |
| Relationship removal is requested | Do not delete the underlying Position or bypass the effective-date rule |
| Physical DELETE is requested | Use it only when the requested date equals the confirmed earliest relationship start; require immutable destructive preview and do not mix MERGE and DELETE for one record |
| A mutation result is uncertain | Do not retry or switch to REST, FSM, browser, or another loader route |
| Combined create is partial | Do not automatically delete or replay the Position |
| A URL names another environment | Do not change the authenticated target environment from the URL |
| Diagnostics are returned | Do not expose credentials, tokens, raw payloads, restricted incumbent data, or protected identifiers |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POSH.POSITION_ROUTE | decision | 3 | execution_gate | position_only->POSH.DONE_POSITION;hierarchy_required->POSH.ANCESTOR;blocked->POSH.ERROR | POSH.DEFAULTS | stop | Delegate a Position create or edit without a parent relationship add or change to Manage Positions; otherwise continue hierarchy processing |
| POSH.ROUTE | decision | 10 | execution_gate | read_complete->POSH.DONE_READ;loader_ready->POSH.DONE_LOADER;blocked->POSH.ERROR | POSH.DESIGN | stop | Select read completion or the declared Core Data Loader stage and enforce preview, approval, and verification boundaries |
| POSH.ERROR | step | 11 | error_handler | stopped->POSH.BLOCKED | none | stop | A prior node returns invalid, missing, ambiguous, blocked, failed, partial, timed-out, uncertain, stale, or unverified |
| POSH.DONE_READ | terminal | 12 | terminal | none | POSH.ROUTE | continue | A complete validated hierarchy was rendered from the selected ancestor |
| POSH.DONE_LOADER | terminal | 13 | terminal | none | POSH.ROUTE | continue | The exact mutation plan is ready for its declared Core Data Loader stage or completed with fresh verification |
| POSH.BLOCKED | terminal | 14 | terminal | none | none | stop | The request cannot safely continue without corrected input, access, metadata, source, approval, or reconciliation |
| POSH.DONE_POSITION | terminal | 15 | terminal | none | POSH.POSITION_ROUTE | continue | Manage Positions owns the create or edit with no parent relationship change |

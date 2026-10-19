# Inventory ABC Analysis Error Handling

## Error Handling Rules

| Situation | What Happens |
|---|---|
| A supplied code or friendly lookup value has no exact match | Stop before Data Loader handoff and request a valid display value or canonical code |
| A supplied code or friendly lookup value is ambiguous | Stop before Data Loader handoff; do not select a candidate automatically |
| Code and friendly values resolve to different rows | Stop and request values that identify one authoritative lookup row |
| A user-settable business date is not YYYY-MM-DD | Stop before Data Loader handoff and identify the field and required zero-padded format |
| A required per-run BO metadata preflight fails or a registered BO is unavailable | Stop before Data Loader handoff; record the selected environment identifier, BO name, result, and sanitized diagnostic in the task validation artifact and skill-run record; do not fall back to direct REST write guidance |
| Data Loader rejects prepared data | Preserve the Data Loader status, row identity, failure class, and sanitized message; Data Loader and Fusion own backend validation |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Lookup no match | An exact display-value lookup returns no item | Provide a valid display value or canonical code |
| Lookup ambiguity | An exact display-value lookup returns multiple items | Provide a more precise value or canonical code |
| Conflicting input | Friendly and canonical inputs resolve to different values | Provide one authoritative representation |
| Date format | A user-settable business date does not exactly match YYYY-MM-DD | Provide the date in YYYY-MM-DD format |
| BO visibility preflight | The selected environment does not expose a required BO or the read-only metadata check fails | Verify registration and selected-environment access, then run a new preflight before retrying |
| Data Loader validation | Data Loader or Fusion rejects prepared data | Correct the source data using the reported diagnostic |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Lookup is missing, ambiguous, or conflicting | Do not fuzzy-match, guess, or select the first candidate |
| Data Loader reports an uncertain failure | Do not resubmit until status and read-only verification clarify the outcome |
| Metadata is unavailable | Do not create direct REST POST, PATCH, or DELETE guidance as a fallback |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ABC.DATA_LOADER_HANDOFF | decision | 60 | execution_gate | ready->ABC.DONE;blocked->ABC.HANDLE_ERROR;failure->ABC.HANDLE_ERROR | ABC.RESOLVE_COMPILE_TYPE | stop | Before handing validated data to core.data-loader for abcClasses, abcClassifications, and abcAssignmentGroups |
| ABC.HANDLE_ERROR | step | 70 | error_handler | handled->ABC.RETURN_ISSUES | none | stop | Any approved lookup, readiness, defaulting, or Data Loader issue |
| ABC.RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| ABC.DONE | terminal | 90 | terminal | none | ABC.DATA_LOADER_HANDOFF | stop | Local rules passed; Data Loader owns final validation and execution |

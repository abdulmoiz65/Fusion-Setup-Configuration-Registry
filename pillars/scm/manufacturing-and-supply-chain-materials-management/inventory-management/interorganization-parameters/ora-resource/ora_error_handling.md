# Interorganization Parameters Error Handling

## Error Handling Rules

| Situation | What Happens |
|---|---|
| A supplied code or friendly lookup value has no exact match | Stop before Data Loader handoff and request a valid LookupCode or Meaning |
| A supplied code or friendly lookup value is ambiguous | Stop before Data Loader handoff; do not select a candidate automatically |
| Code and friendly values resolve to different rows | Stop and request values that identify one authoritative lookup row |
| A required per-run BO metadata preflight fails or a registered BO is unavailable | Stop before Data Loader handoff; record the selected environment identifier, BO name, result, and sanitized diagnostic in the task validation artifact and skill-run record; do not fall back to direct REST write guidance |
| Data Loader rejects prepared data | Preserve the Data Loader status, row identity, failure class, and sanitized message; Data Loader and Fusion own backend validation |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Lookup no match | An exact code-or-meaning lookup returns no item | Provide a valid LookupCode or Meaning |
| Lookup ambiguity | An exact code-or-meaning lookup returns multiple items | Provide a more precise value |
| Conflicting input | Code and friendly input resolve to different values | Provide one authoritative representation or a consistent pair |
| BO visibility preflight | The selected environment does not expose interOrganizationParameters or the read-only metadata check fails | Verify registration and selected-environment access, then run a new preflight before retrying |
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
| IOP.DATA_LOADER_HANDOFF | decision | 80 | execution_gate | ready->IOP.DONE;blocked->IOP.HANDLE_ERROR;failure->IOP.HANDLE_ERROR | IOP.RESOLVE_EXPENSE_CANCEL_BACKORDERS | stop | Before handing validated data to core.data-loader for interOrganizationParameters |
| IOP.HANDLE_ERROR | step | 90 | error_handler | handled->IOP.RETURN_ISSUES | none | stop | Any approved lookup, readiness, or Data Loader issue |
| IOP.RETURN_ISSUES | terminal | 100 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| IOP.DONE | terminal | 110 | terminal | none | IOP.DATA_LOADER_HANDOFF | stop | Local rules passed; Data Loader owns final validation and execution |

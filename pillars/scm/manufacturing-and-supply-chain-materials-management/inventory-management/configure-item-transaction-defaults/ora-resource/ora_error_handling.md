# Configure Item Transaction Defaults Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| DefaultType or DefaultTypeMeaning does not resolve to exactly one Item Transaction Defaults standard-lookup row | Stop before Data Loader handoff and show the supplied value, resolver name, path, match count, and correction needed |
| DefaultType and DefaultTypeMeaning resolve to different LookupCode/Meaning rows | Stop before Data Loader handoff and ask for one authoritative matching value |
| Item Transaction Defaults metadata is unavailable | Stop and report a Data Loader availability issue; do not fall back to direct REST write guidance |
| Data Loader rejects a prepared row | Preserve the Data Loader status, row identity, failure class, and sanitized message; Data Loader and Fusion own backend validation |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Lookup readiness | Default Type is not found, ambiguous, inaccessible, or supplied values resolve to different rows | Provide an exact `INV_ITEM_TXN_DEFAULTS_TYPE` Meaning or matching LookupCode |
| Data Loader availability | Business-object metadata cannot be read | Verify BO registration and target-environment access before retrying |
| Data Loader validation | Data Loader or Fusion rejects prepared data | Correct source data from the returned diagnostic |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Default Type lookup failure | Supplied DefaultTypeMeaning, supplied DefaultType when present, resolver name, standard-lookup path, match count, and correction needed |
| Data Loader handoff | Task code, task name, business object, and resolved DefaultTypeMeaning and LookupCode when applicable |
| Data Loader failure | Data Loader request or process identifier when available, failed row identifier, sanitized message, stage, and recommended next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Default Type lookup is ambiguous | Do not choose the first candidate, fuzzy-match, or use contains matching |
| BO/Data Loader route is unavailable | Do not use task-local REST POST or PATCH guidance as a fallback |
| Data Loader outcome is uncertain | Do not resubmit until status and read-only verification clarify the outcome |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ITD.DATA_LOADER_HANDOFF | decision | 50 | execution_gate | ready->ITD.DONE;blocked->ITD.HANDLE_ERROR;failure->ITD.HANDLE_ERROR | ITD.CHECK_READINESS | stop | Before handing normalized data to core.data-loader for Item Transaction Defaults |
| ITD.HANDLE_ERROR | step | 60 | error_handler | handled->ITD.RETURN_ISSUES | none | stop | Any local validation, lookup, readiness, or Data Loader issue |
| ITD.RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| ITD.DONE | terminal | 80 | terminal | none | ITD.DATA_LOADER_HANDOFF | stop | Local task rules passed and Data Loader owns final validation and execution |

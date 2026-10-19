# Material Statuses Error Handling

## Error Handling Rules

| Situation | What Happens |
|---|---|
| A documented 1/2 field has an unsupported value | Stop before Data Loader handoff and identify the field, supplied value, and accepted friendly values |
| A documented 1/2 field has multiple or conflicting supplied values | Stop before Data Loader handoff; do not choose a value automatically |
| Data Loader rejects the prepared row | Preserve the Data Loader status, row identity, failure class, and sanitized message; Data Loader and Fusion own backend validation |
| A future metadata request fails | Stop and report the BO registration evidence and metadata failure; do not fall back to direct REST write guidance |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input normalization | A supplied value does not exactly match a documented friendly or canonical value | Provide one accepted value |
| Conflicting input | More than one supplied value maps to different canonical values | Provide one authoritative value |
| Data Loader availability | Business-object metadata is unavailable | Verify registration and environment access before retrying |
| Data Loader validation | Data Loader or Fusion rejects prepared data | Correct the source data using the reported diagnostic |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Normalization input is unsupported or conflicting | Do not fuzzy-match, guess, or select a value |
| Data Loader reports an uncertain failure | Do not resubmit until status and read-only verification clarify the outcome |
| Metadata is unavailable | Do not create direct REST POST, PATCH, or DELETE guidance as a fallback |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MSTAT.DATA_LOADER_HANDOFF | decision | 30 | execution_gate | ready->MSTAT.DONE;blocked->MSTAT.HANDLE_ERROR;failure->MSTAT.HANDLE_ERROR | MSTAT.CHECK_READINESS | stop | Before handing normalized data to core.data-loader for inventoryMaterialStatuses |
| MSTAT.HANDLE_ERROR | step | 40 | error_handler | handled->MSTAT.RETURN_ISSUES | none | stop | Any normalization, dependency, or Data Loader issue |
| MSTAT.RETURN_ISSUES | terminal | 50 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| MSTAT.DONE | terminal | 60 | terminal | none | MSTAT.DATA_LOADER_HANDOFF | stop | Local normalization and readiness rules passed; Data Loader owns final validation and execution |

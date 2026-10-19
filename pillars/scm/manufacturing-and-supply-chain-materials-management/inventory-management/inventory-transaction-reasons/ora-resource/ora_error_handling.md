# Inventory Transaction Reasons Error Handling

## Source Evidence

| Source | Used For |
|---|---|
| Implementation owner confirmation | Data Loader owns execution through the registered inventoryTransactionReasonsV2 business object |
| Redwood inventoryTransactionReasonsV2 layout and LOV action chains | Type and Context are standard lookup controls; Context is enabled only when ReasonType equals 1 |
| Data Loader sample generation | Live metadata sample generation for inventoryTransactionReasonsV2 succeeded and produced editable, attribute-details, and key-fields workbooks |
| Implementation owner approved rule | EnableDate and DisableDate use YYYY-MM-DD, are not before the current date, and DisableDate is not before EnableDate |

## Error Situations

| Situation | What Should Happen |
|---|---|
| A Type or Context display value has no exact match, has multiple matches, or is inaccessible | Stop and show the supplied value, resolver name, lookup source, exact-match count, and correction needed |
| ReasonType and ReasonTypeMeaning, or ReasonContextCode and ReasonContext, identify different LOV rows | Stop and request one authoritative value or matching code and display value |
| ReasonContext or ReasonContextCode is supplied while ReasonType is not 1 | Stop and require ReasonType 1 or removal of the Context value |
| EnableDate or DisableDate is not YYYY-MM-DD | Stop and request the date in YYYY-MM-DD format |
| EnableDate or DisableDate is before the current date | Stop and request a date on or after the current date |
| DisableDate is before EnableDate | Stop and request a DisableDate on or after EnableDate |
| Data Loader metadata for inventoryTransactionReasonsV2 is unavailable in a future environment | Stop and report the BO registration confirmation and failed metadata retrieval; do not fall back to direct REST write guidance |
| Data Loader rejects the prepared row | Preserve Data Loader status, row identity, failure class, and sanitized message; let Data Loader and Fusion own backend validation |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Lookup readiness | Type or Context does not resolve to one exact standard lookup row | Provide a valid display value or implementation code |
| Conflicting input | Supplied code and display value identify different lookup rows | Keep one authoritative value or make the pair match |
| UI-only condition | Context is supplied for a Type other than 1 | Use ReasonType 1 or omit Context |
| Date validation | A supplied date is not YYYY-MM-DD, is before the current date, or DisableDate is before EnableDate | Correct the supplied date values before retrying |
| Data Loader availability | A future Data Loader metadata request cannot retrieve the registered BO | Verify registration, environment access, sample support, mandatory attributes, and key attributes before retrying |
| Data Loader validation | Data Loader or Fusion rejects a prepared row | Show Data Loader diagnostics and correct the source data |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Type or Context lookup failure | Supplied display value and code when present, resolver name, lookup source, exact-match count, and correction needed |
| UI-only condition failure | Supplied ReasonType and Context value, plus the requirement that Context is enabled only for ReasonType 1 |
| Date validation failure | Supplied EnableDate and DisableDate, expected YYYY-MM-DD format, current-date comparison, and date-order correction needed |
| Data Loader handoff | Task code, task name, business object inventoryTransactionReasonsV2, resolved lookup values, and Data Loader visibility status |
| Data Loader failure | Data Loader request or process identifier when available, failed row identity, sanitized message, stage, and recommended next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Type or Context lookup is ambiguous | Do not choose the first candidate, fuzzy-match, or use a contains match as the final result |
| Data Loader metadata is not visible | Do not send data or create direct REST POST or PATCH guidance as a fallback |
| A retry follows an uncertain Data Loader failure | Do not resubmit until Data Loader status and read-only verification clarify the outcome |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ITR.DATA_LOADER_HANDOFF | decision | 50 | execution_gate | ready->ITR.DONE;blocked->ITR.HANDLE_ERROR;failure->ITR.HANDLE_ERROR | ITR.CHECK_DEPENDENCIES | stop | Before handing resolved data to core.data-loader for inventoryTransactionReasonsV2 |
| ITR.HANDLE_ERROR | step | 60 | error_handler | handled->ITR.RETURN_ISSUES | none | stop | Any validation, lookup, dependency, or Data Loader handoff issue |
| ITR.RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| ITR.DONE | terminal | 80 | terminal | none | ITR.DATA_LOADER_HANDOFF | stop | Local task rules passed and Data Loader owns final validation and execution |

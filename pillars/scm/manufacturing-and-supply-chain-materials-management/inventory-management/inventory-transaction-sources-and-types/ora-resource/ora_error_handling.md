# Inventory Transaction Sources and Types Error Handling

## Source Evidence

| Source | Used For |
|---|---|
| Implementation owner confirmation | Data Loader owns execution through registered business object inventoryTransactionSources |
| Implementation owner validation decision | Local errors are limited to friendly-value normalization, existing source context, Transaction Action and Value Set resolution, and Data Loader or business-object handoff diagnosis |

## Error Situations

| Situation | What Should Happen |
|---|---|
| LocationRequired contains a value other than blank, Y, N, Yes, or No | Stop before Data Loader handoff and ask for Y, N, Yes, No, or blank |
| EnableStatusControl contains a value other than blank, 1, 2, Y, N, Yes, or No | Stop before Data Loader handoff and ask for 1, 2, Yes, No, Y, N, or blank |
| AllowProjectTransactions contains a value other than blank, 1, 2, Y, N, Yes, or No | Stop before Data Loader handoff and ask for 1, 2, Yes, No, Y, N, or blank |
| Existing transaction source name is not found, ambiguous, or inaccessible | Stop and show the supplied TransactionSourceTypeName, resolver name, lookup path, match count, and safe corrective guidance |
| Transaction Action is not found, ambiguous, inaccessible, or conflicts with TransactionActionId | Stop and show the supplied Transaction Action or TransactionActionName, supplied TransactionActionId if any, TransactionSourceTypeId if available, whether this is an existing-source or new-source create flow, selected action lookup group when known, case-insensitive exact action LOV match count, and safe corrective guidance |
| Value Set is not found, disabled, ambiguous, inaccessible, or conflicts with DescriptiveFlexContext | Stop and show the supplied Value Set, supplied DescriptiveFlexContext if any, INV_TRANSACTION_SOURCES context match count, and safe corrective guidance |
| Data Loader or registered business object rejects the prepared row | Preserve the Data Loader status, row identity, failure class, sanitized message, and business-object context; do not duplicate the backend validation locally |
| Data Loader business object inventoryTransactionSources is unavailable | Stop and report a Data Loader readiness issue; do not fall back to direct REST write guidance |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input normalization | Friendly control value cannot be normalized | Correct the exact value and rerun task validation |
| Lookup readiness | Existing transaction source cannot resolve to one TransactionSourceTypeId, Transaction Action cannot resolve by trim plus case-insensitive exact match to exactly one TransactionActionId, or Value Set cannot resolve to exactly one usable DescriptiveFlexContext | Provide a valid display value, exact implementation field value, or clear existing-source versus new-source create context |
| Conflicting input | Transaction Action and TransactionActionId, or Value Set and DescriptiveFlexContext, identify different lookup rows after the resolver's comparison rules | Keep one authoritative value or make them match |
| Data Loader validation | Data Loader or BO validation rejects the prepared row | Show Data Loader diagnostics and let Data Loader or Fusion own the field-level validation |
| Data Loader availability | The registered BO is not visible or loader metadata cannot be read | Verify BO registration and environment access before retrying |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Local validation failure | Field name, supplied value, accepted values, normalized value when available, and row identifier |
| Existing source lookup failure | Supplied TransactionSourceTypeName, resolver name, lookup path, match count, and correction needed |
| Transaction Action lookup failure | Supplied Transaction Action or TransactionActionName, supplied TransactionActionId if present, TransactionSourceTypeId if available, existing-source or new-source create context, resolver name, lookup path, source-specific lookup group when known, case-insensitive exact match count, and correction needed |
| Value Set lookup failure | Supplied Value Set, supplied DescriptiveFlexContext if present, resolver name, lookup path, match count, EnabledFlag state when available, and correction needed |
| Data Loader handoff | Task code, task name, business object inventoryTransactionSources, normalized local values, and whether TransactionActionId and DescriptiveFlexContext were resolved or blank |
| Data Loader failure | Data Loader request or process identifier when available, failed row identifier, sanitized message, stage, and recommended next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Backend validation fails | Do not recreate server-side validation rules in ora_input_validation.md unless a future sourced UI-only or pre-loader rule is approved |
| Transaction Action lookup is ambiguous | Do not choose the first candidate, fuzzy-match an action, or use contains matching |
| Value Set lookup is ambiguous | Do not choose the first candidate or fuzzy-match a context |
| BO/Data Loader path is unavailable | Do not use task-local direct REST POST or PATCH guidance as a fallback |
| User asks to retry after uncertain loader failure | Do not resubmit until Data Loader status and read-only verification clarify the outcome |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TST.DATA_LOADER_HANDOFF | decision | 60 | execution_gate | ready->TST.DONE;blocked->TST.HANDLE_ERROR;failure->TST.HANDLE_ERROR | TST.CHECK_DEPENDENCIES | stop | Before handing normalized data to core.data-loader for inventoryTransactionSources |
| TST.HANDLE_ERROR | step | 70 | error_handler | handled->TST.RETURN_ISSUES | none | stop | Any local normalization, existing source readiness, Transaction Action readiness, Value Set readiness, or Data Loader handoff issue |
| TST.RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| TST.DONE | terminal | 90 | terminal | none | TST.DATA_LOADER_HANDOFF | stop | Local task rules passed and Data Loader owns final validation and execution |

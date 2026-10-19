# Inventory Document Output Preferences Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| UI-form validation fails | Stop preparation and identify the missing or invalid field. |
| A resolver returns no match, multiple matches, or conflicting supplied code and display value | Stop preparation and request a precise supported value. |
| Fusion returns an error response | Surface the returned business detail when available; otherwise report the HTTP status and text. Stop before retry. |
| A Data Loader validation, preview, or execution error occurs | Delegate diagnosis to core.data-loader and do not retry a mutation automatically. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A lookup is unresolved or ambiguous | Do not guess, fuzzy-match, select the first result, or bypass the lookup. |
| A REST write is requested through this resource | Do not create direct POST, PATCH, DELETE, payload, or approval guidance. |
| An execution error is uncertain | Do not replay the request. Reconcile through the declared Data Loader workflow. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IDOP.HANDLE_ERROR | decision | 40 | error_handler | handled->IDOP.STOP | none | stop | A validation, lookup, Data Loader, or Fusion error occurs |
| IDOP.COMPLETE | terminal | 50 | terminal | none | IDOP.APPLY_DEFAULT | stop | Input and applicable lookups/defaults completed |
| IDOP.STOP | terminal | 60 | terminal | none | none | stop | A blocking error occurs |

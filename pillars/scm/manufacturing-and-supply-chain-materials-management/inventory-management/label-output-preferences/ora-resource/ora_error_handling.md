# Label Output Preferences Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Label UI form validation fails | Stop preparation and identify the field rejected by the form. |
| A header, organization, or subinventory lookup has no exact match or is ambiguous | Stop preparation and request a precise supported value. |
| Fusion returns an error response | Surface the returned business detail when available and stop before retry. |
| A Data Loader validation, preview, or execution error occurs | Delegate diagnosis to core.data-loader and do not retry a mutation automatically. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A VBC service identifier is the only lookup evidence | Do not guess a REST path, create a resolver, or select a value from an undocumented service. |
| A REST write is requested through this resource | Do not create direct POST, PATCH, DELETE, payload, or approval guidance. |
| An execution error is uncertain | Do not replay the request; reconcile through the declared Data Loader workflow. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LOP.HANDLE_ERROR | decision | 30 | error_handler | handled->LOP.STOP | none | stop | A validation, lookup, Data Loader, or Fusion error occurs |
| LOP.COMPLETE | terminal | 40 | terminal | none | LOP.RESOLVE_LOOKUPS | stop | Input validation and applicable lookups completed without a blocking error |
| LOP.STOP | terminal | 50 | terminal | none | none | stop | A blocking error occurs |

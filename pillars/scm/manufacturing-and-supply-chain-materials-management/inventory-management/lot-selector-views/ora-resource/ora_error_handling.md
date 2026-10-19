# Lot Selector Views Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Application or Task Flow lookup has no exact match, more than one exact match, or conflicting code and display input | Stop before Data Loader handoff and request one unambiguous value. |
| A supplied Default, Display Columns, or Filter Chip representation is unsupported | Stop before Data Loader handoff; request the documented active or Boolean form. |
| Current inventorySearchViews metadata preflight fails or is unavailable | Classify as a metadata readiness blocker; do not substitute direct REST execution. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Friendly value normalization or exact lookup matching fails. | Correct the input and restart task validation. |
| Catalog mismatch | Current Data Loader metadata cannot represent inventorySearchViews. | Stop and reconcile BO registration or metadata; do not retry a load. |
| Auth/authz | The configured environment cannot read required metadata or lookup values. | Refresh authentication once, then stop on a second failure. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LSV.DATA_LOADER_HANDOFF | decision | 60 | execution_gate | ready->LSV.DONE;blocked->LSV.HANDLE_ERROR;failure->LSV.HANDLE_ERROR | LSV.CHECK_METADATA | stop | Before handing normalized data to core.data-loader. |
| LSV.HANDLE_ERROR | step | 90 | error_handler | handled->LSV.RETURN_ISSUES | none | stop | Any lookup, normalization, metadata, or handoff issue. |
| LSV.RETURN_ISSUES | terminal | 100 | terminal | none | none | stop | A blocking issue was classified and disclosed. |
| LSV.DONE | terminal | 110 | terminal | none | LSV.DATA_LOADER_HANDOFF | stop | Local rules passed; core.data-loader owns final validation and execution. |

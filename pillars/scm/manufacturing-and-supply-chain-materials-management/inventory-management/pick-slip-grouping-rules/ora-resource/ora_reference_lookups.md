# Pick Slip Grouping Rules Reference Lookups

## Local Resolver Boundary

No task-local read-only lookup is defined for this task.

| Input | Handoff behavior |
|---|---|
| GroupByCatalogCode | Pass the supplied trimmed value directly as `GroupByCatalogCode`. Do not resolve a catalog name to an ID and do not send `GroupByCatalogId`. |

Data Loader and Fusion own any server-side lookup, existence, or compatibility validation.

# Performance Document Types Reference Lookups

Apply this task guidance using current target metadata and the declared execution route.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| get_document_type_by_id | Updating Status, DateFrom, or DateTo | DocumentTypeId | /latest/talentPerformanceDocumentTypes/{DocumentTypeId} | DocumentTypeId, Status, DateFrom, DateTo, InUseFlag | PrimaryKey row finder matches the supplied DocumentTypeId. | Current Status, DateFrom, DateTo, InUseFlag | On no match, stop as an invalid identity. The PrimaryKey finder returns one record; otherwise stop as ambiguous. |
| resolve_document_type_status | Status is supplied | Status | ACTIVE_INACTIVE lookup| Code | Exact active/inactive status code | Validated Status | No match: stop as invalid. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A constrained update needs current state | Perform only the documented GET by DocumentTypeId before evaluating the update. |
| The lookup returns InUseFlag=Y | Do not permit a Status change; use the current state when evaluating date constraints. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PERFORMANCE_DOCUMENT_TYPES.LOOKUP_CURRENT | decision | 20 | reference_lookup | found->PERFORMANCE_DOCUMENT_TYPES.DEPENDENCIES;not_found->PERFORMANCE_DOCUMENT_TYPES.STOP_DEPENDENCY;not_applicable->PERFORMANCE_DOCUMENT_TYPES.DEPENDENCIES | PERFORMANCE_DOCUMENT_TYPES.VALIDATE | stop | Updating Status, DateFrom, or DateTo. For a create, the lookup is not applicable and processing continues to dependency validation. |

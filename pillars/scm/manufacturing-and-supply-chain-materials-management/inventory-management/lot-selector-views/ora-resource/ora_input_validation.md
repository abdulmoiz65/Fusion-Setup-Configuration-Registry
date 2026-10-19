# Lot Selector Views Input Validation

## Scope Boundary

| Boundary | What Happens |
|---|---|
| Local ownership | Normalize only the approved Application, Task Flow, Default, Display Columns, and Filter Chip representations before Data Loader handoff. |
| Backend ownership | Data Loader and Fusion own required fields, uniqueness, lengths, server-side domains, child keys, and final field enforcement. |
| Execution | Do not create direct REST write guidance; core.data-loader owns governed load preparation and execution. |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Application identity | Application or ApplicationCode | Stop | Supply an Application display value, LookupCode, or both. | A view is created or its application is changed. | resolve_inventory_search_view_application |
| Task Flow identity | Task Flow or TaskFlow | Stop | Supply a Task Flow display value, LookupCode, or both. | A view is created or its task flow is changed. | resolve_inventory_search_view_task_flow |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Application normalization | Resolve a supplied display value, LookupCode, or both to ApplicationCode. Both supplied representations must identify the same row. | Before Data Loader handoff. | resolve_inventory_search_view_application |
| Task Flow normalization | Resolve a supplied display value, LookupCode, or both to TaskFlow. Both supplied representations must identify the same row. | Before Data Loader handoff. | resolve_inventory_search_view_task_flow |
| Default normalization | Convert active to true and a blank Default representation to false. Preserve explicit true or false Boolean values. | Default is supplied or normalized for a view. |  |
| Display Columns normalization | Accept true or false Boolean values. For the Redwood existing-child update route, emit Y or N; for a new child and the Data Loader BO route, emit the Boolean value. | Display Columns is supplied. |  |
| Filter Chip normalization | Accept true or false Boolean values. For the Redwood existing-child update route, emit Y or N; for a new child and the Data Loader BO route, emit the Boolean value. | Filter Chip is supplied. |  |
| Unsupported friendly representation | Reject values other than the documented active or Boolean forms; do not infer yes, no, y, or n aliases. | Default, Display Columns, or Filter Chip is supplied. |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LSV.NORMALIZE_INPUT | step | 20 | validate_input | valid->LSV.RESOLVE_APPLICATION;invalid->LSV.HANDLE_ERROR | LSV.APPLY_ENTITY_DEFAULT | stop | Before Data Loader task validation or import preparation. |

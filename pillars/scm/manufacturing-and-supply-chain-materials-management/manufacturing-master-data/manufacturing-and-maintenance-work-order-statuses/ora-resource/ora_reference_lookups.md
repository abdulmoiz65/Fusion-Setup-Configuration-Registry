# Reference Lookups

Read-only lookups support validation only. They do not authorize a direct REST write, import, or FSM operation; `core.data-loader` remains the only import orchestrator.

Source: Oracle Fusion Cloud SCM, *How You Manage Work Order Statuses*; `workOrderStatuses_rest_rules_summary.txt` supplied by the developer.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| confirm_work_order_statuses_loader_object | A REST Data Loader operation is requested | Business Object: workOrderStatuses | Core Data Loader managed read-only Data Loader metadata retrieval | Registered business object identity and supported operation metadata | Match the exact registered Business Object workOrderStatuses and the requested operation | Confirmed Business Object and supported operation | Stop and ask the user; do not invent a substitute REST Business Object or route. |
| resolve_work_order_status_by_id | An update, deactivate, or delete identifies a status by ID | WoStatusId | /fscmRestApi/resources/11.13.18.05/workOrderStatuses/{WoStatusId} | WoStatusId, WoStatusCode, WoStatusName, WoSystemStatusCode, SeededFlag, InactiveDate | Match the exact WoStatusId | Existing identity and protection state | Stop when no status exists. |
| resolve_work_order_status_by_code | A create supplies WoStatusCode | WoStatusCode | /fscmRestApi/resources/11.13.18.05/workOrderStatuses with FilterByStatusCode | WoStatusId, WoStatusCode | Match the exact supplied code | Duplicate-status-code finding | Stop if a different row has the code. |
| resolve_work_order_status_by_name | A create or rename supplies WoStatusName | WoStatusName | /fscmRestApi/resources/11.13.18.05/workOrderStatuses | WoStatusId, WoStatusName | Match the exact supplied name | Duplicate-status-name finding | Stop if a different row has the name or if the result is ambiguous. |
| resolve_work_order_system_status | A create supplies WoSystemStatusCode | Lookup type ORA_WIE_WO_SYSTEM_STATUS and WoSystemStatusCode | Core Data Loader managed read-only lookup metadata retrieval | Valid lookup code and meaning | Match the exact lookup code | Validated WoSystemStatusCode and meaning | Stop when the code is absent or invalid; do not use an ORA_-prefixed display variant. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Read-only verification is needed | Use the documented lookup through the selected core workflow; do not substitute a direct import or write call. |
| A REST collection query does not prove an active-status filter | Do not assume inactive statuses are excluded; apply the documented InactiveDate rule explicitly. |
| A status delete is requested | Use Data Loader validation to verify the status is user-defined and not referenced by a work order header or status history before approval. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WOSTATUS.LOOKUPS | decision | 3 | reference_lookup | resolved->WOSTATUS.DEPENDENCIES;unresolved->WOSTATUS.BLOCKED | WOSTATUS.APPLY_DEFAULTS | stop | Read-only business-object, identity, duplicate, and system-status validation is required. |

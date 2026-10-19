# Design Enforcement

Source: Oracle Fusion Cloud SCM, *How You Manage Work Order Statuses*; `workOrderStatuses_rest_rules_summary.txt` supplied by the developer.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm object and operation | Confirm the registered workOrderStatuses Data Loader Business Object and requested operation. |
| 2 | Confirm business values | Validate unique code, unique name, and the associated system-status lookup code. |
| 3 | Enforce lifecycle restrictions | Treat code and system status as immutable; protect seeded statuses and validate future dating. |
| 4 | Enforce route and approval | Use Core Data Loader, validate the immutable artifact, and obtain explicit approval before any live import. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Creating a user-defined status | Error | resolve_work_order_status_by_code | A duplicate code exists | Use a unique status code that makes the related system status understandable | Yes |
| Creating or renaming a status | Error | resolve_work_order_status_by_name | A duplicate name exists | Use a unique, meaningful name that makes the system-status relationship clear | Yes |
| Creating a status | Error | resolve_work_order_system_status | The system status is invalid or is PENDING_APPROVAL for a user-defined status | Use a valid ORA_WIE_WO_SYSTEM_STATUS lookup code other than PENDING_APPROVAL for user-defined creation | Yes |
| Updating a status | Error | resolve_work_order_status_by_id | WoStatusCode or WoSystemStatusCode would change | Preserve those immutable fields; for user-defined statuses limit changes to Name, Description, or a valid future InactiveDate | Yes |
| Updating a seeded or predefined status | Error | resolve_work_order_status_by_id | The request changes code, system status, or inactive date | Do not change the protected fields; any name or description change requires an explicit business decision | Yes |
| Deleting a status | Error | resolve_work_order_status_by_id | The status is seeded or referenced by a work order header or status history | Retain the status or remove permitted dependencies through their own approved workflows | No |
| Importing any status data | Error | confirm_work_order_statuses_loader_object | REST metadata does not confirm the object and operation, the source is not validated, the immutable artifact changes, or approval is absent | Use REST through Core Data Loader; use FSM only after REST is proven unavailable and the immutable FSM artifact is explicitly approved | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| confirm_work_order_statuses_loader_object | Any REST Data Loader import | Registered object identity and supported operation | ora_reference_lookups.md |
| resolve_work_order_status_by_code | Creating a status | Existing status code result | ora_reference_lookups.md |
| resolve_work_order_status_by_name | Creating or renaming a status | Existing status name result | ora_reference_lookups.md |
| resolve_work_order_system_status | Creating a status | Exact valid lookup code and meaning | ora_reference_lookups.md |
| resolve_work_order_status_by_id | Updating, deactivating, or deleting a status | Existing identity, SeededFlag, and protection state | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WOSTATUS.DESIGN | decision | 5 | design_enforcement | compliant->WOSTATUS.ROUTE;blocked->WOSTATUS.BLOCKED | WOSTATUS.DEPENDENCIES | stop | A work order status request passes input, lookup, and dependency validation. |

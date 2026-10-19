# Design Enforcement

Sources: Oracle Fusion Cloud SCM, *Redwood: Group Work Orders to Perform Mass Actions*; `workOrderGroups_rest_rules_summary.txt` supplied by the developer.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm object and operation | Confirm the registered workOrderGroups Data Loader Business Object and requested operation. |
| 2 | Confirm group identity | Validate unique code and name in the organization and source context. |
| 3 | Confirm assignment eligibility | Validate the work order’s status, group assignment, organization, and work method. |
| 4 | Enforce import route and approval | Use Core Data Loader, validate the immutable artifact, and obtain explicit approval before any live import. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Creating or updating a group | Error | resolve_work_order_group_by_code | A duplicate GroupCode exists for the same organization and source | Use a unique group code | Yes |
| Creating or updating a group | Error | resolve_work_order_group_by_name | A duplicate GroupName exists for the same organization and source | Use a unique group name meaningful to its intended work-order grouping | Yes |
| Creating a group | Error | resolve_work_order_group_source | GroupSource is invalid | Use a valid ORA_WIE_SOURCE code; use the default ORA_MANUFACTURING only when it is the intended source | Yes |
| Updating a group | Error | resolve_work_order_group_by_id | GroupSource or OrganizationId would change | Preserve the insert-only fields | Yes |
| Adding a work order to a group | Error | resolve_work_order_for_group | The work order is pending approval, completed, canceled, closed, already grouped, in another organization, or has a work method inconsistent with the group source | Select an eligible unassigned work order with the same organization and a compatible work method | Yes |
| Adding to an inactive group | Error | resolve_work_order_group_by_id | The group is inactive for assignment | Reactivate the group or select an active group | Yes |
| Deleting a group | Error | resolve_work_order_group_by_id | The group has one or more child assignments | Delete child assignments first through the approved Data Loader workflow | Yes |
| Importing any group or assignment data | Error | confirm_work_order_groups_loader_object | REST metadata does not confirm the object and operation, the source is not validated, the immutable artifact changes, or approval is absent | Use REST through Core Data Loader; use FSM only after REST is proven unavailable and the immutable FSM artifact is explicitly approved | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| confirm_work_order_groups_loader_object | Any REST Data Loader import | Registered object identity and supported operation | ora_reference_lookups.md |
| resolve_work_order_group_by_code | Creating or updating a group | Existing composite code-key result | ora_reference_lookups.md |
| resolve_work_order_group_by_name | Creating or updating a group | Existing composite name-key result | ora_reference_lookups.md |
| resolve_work_order_group_source | Creating a group | Exact valid group-source lookup code | ora_reference_lookups.md |
| resolve_work_order_group_by_id | Updating, assigning to, inactivating, or deleting a group | Existing identity, organization, source, active state, and child assignment result | ora_reference_lookups.md |
| resolve_work_order_for_group | Adding a work order to a group | Work-order identity, status, organization, method, and existing assignment | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WOGROUP.DESIGN | decision | 5 | design_enforcement | compliant->WOGROUP.ROUTE;blocked->WOGROUP.BLOCKED | WOGROUP.DEPENDENCIES | stop | A work order group request passes input, lookup, and dependency validation. |

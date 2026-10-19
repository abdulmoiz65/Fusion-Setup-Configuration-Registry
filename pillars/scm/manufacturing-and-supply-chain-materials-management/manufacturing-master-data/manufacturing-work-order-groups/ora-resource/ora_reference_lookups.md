# Reference Lookups

Read-only lookups support validation only. They do not authorize a direct REST write, import, or FSM operation; `core.data-loader` remains the only import orchestrator.

Sources: Oracle Fusion Cloud SCM, *Redwood: Group Work Orders to Perform Mass Actions*; `workOrderGroups_rest_rules_summary.txt` supplied by the developer.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| confirm_work_order_groups_loader_object | A REST Data Loader operation is requested | Business Object: workOrderGroups | Core Data Loader managed read-only Data Loader metadata retrieval | Registered business object identity and supported operation metadata | Match the exact registered Business Object workOrderGroups and the requested operation | Confirmed Business Object and supported operation | Stop and ask the user; do not invent a substitute REST Business Object or route. |
| resolve_work_order_group_by_id | A group update, deactivation, delete, or child assignment identifies a parent group | WoGroupId | /fscmRestApi/resources/11.13.18.05/workOrderGroups/{WoGroupId} | WoGroupId, GroupCode, GroupName, GroupSource, OrganizationId, InactiveDate | Match the exact WoGroupId | Existing group identity, source, organization, and active state | Stop when no group exists. |
| resolve_work_order_group_by_code | A group create or update supplies GroupCode | GroupCode, OrganizationId, GroupSource | /fscmRestApi/resources/11.13.18.05/workOrderGroups | WoGroupId, GroupCode, OrganizationId, GroupSource | Match the exact OrganizationId, GroupSource, and GroupCode | Duplicate-group-code finding | Stop if a different row has the same composite business key. |
| resolve_work_order_group_by_name | A group create or update supplies GroupName | GroupName, OrganizationId, GroupSource | /fscmRestApi/resources/11.13.18.05/workOrderGroups | WoGroupId, GroupName, OrganizationId, GroupSource | Match the exact OrganizationId, GroupSource, and GroupName | Duplicate-group-name finding | Stop if a different row has the same composite business key or the result is ambiguous. |
| resolve_work_order_group_source | A group create supplies GroupSource | Lookup type ORA_WIE_SOURCE and GroupSource | Core Data Loader managed read-only lookup metadata retrieval | Valid lookup code and meaning | Match the exact lookup code | Validated GroupSource | Stop when the value is absent or invalid. |
| resolve_work_order_group_organization | A group create supplies OrganizationId or OrganizationCode | OrganizationId or OrganizationCode | Core Data Loader managed read-only organization metadata retrieval | OrganizationId, OrganizationCode, organization identity | Match the exact supplied identifier | Validated OrganizationId and OrganizationCode | Stop when the organization is absent, inaccessible, or ambiguous. |
| resolve_work_order_for_group | A child assignment supplies WorkOrderId or WorkOrderNumber | WorkOrderId, or WorkOrderNumber plus group OrganizationId | Core Data Loader managed read-only work-order metadata retrieval | WorkOrderId, WorkOrderNumber, OrganizationId, work method, system status, existing group assignment | Match exact WorkOrderId, or exact WorkOrderNumber plus group OrganizationId | Validated work-order identity and assignment eligibility | Stop when no unique same-organization work order is resolved or it cannot be assigned. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Work order groups need to be searched or acted on by group | Create the group and add its work orders before relying on group search or mass actions. |
| More than one candidate is returned | Stop and ask for an exact identifier. |
| No candidate is returned | Stop and ask for a valid identifier. |
| A direct REST resource is documented | Use it only for read-only lookup under the selected Core Data Loader workflow; do not use it for direct import execution. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WOGROUP.LOOKUPS | decision | 3 | reference_lookup | resolved->WOGROUP.DEPENDENCIES;unresolved->WOGROUP.BLOCKED | WOGROUP.APPLY_DEFAULTS | stop | Read-only business-object, group, organization, work-order, uniqueness, and source validation is required. |

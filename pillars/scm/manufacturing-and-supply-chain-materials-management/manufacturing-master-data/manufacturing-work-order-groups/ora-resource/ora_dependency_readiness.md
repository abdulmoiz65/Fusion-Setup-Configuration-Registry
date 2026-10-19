# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Feature and access | The no-enablement feature is available and the actor has the required Manage or View Work Order Groups privilege for the selected operation. |
| 2 | Registered Data Loader object | Confirm workOrderGroups and the requested REST operation through read-only Core Data Loader metadata. |
| 3 | Group organization and source | Resolve the group organization and valid source before creating or assigning work orders. |
| 4 | Work order eligibility | Resolve the selected work order, its status, work method, organization, and existing assignment before adding it to a group. |
| 5 | Delete readiness | Remove every child assignment before requesting deletion of the parent group. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| feature_access | Feature availability and role access | Yes | Any group operation | Verify | Oracle readiness guidance and target environment access |  | No enablement step is required, but Manage Work Order Groups or View Work Order Groups access is required for the selected activity | Obtain the required privilege before the operation | Requested operation, privilege evidence |
| registered_loader_object | Registered workOrderGroups Business Object | Yes | Any REST Data Loader import | Verify | Core Data Loader read-only metadata | confirm_work_order_groups_loader_object | The requested operation must use the confirmed registered object | Stop and provide the confirmed object or request an approved FSM fallback after REST is proven unavailable | Business Object, supported operation |
| group_organization | Valid group organization | Yes | Create or update a group; add a work order | Verify | Organization metadata | resolve_work_order_group_organization | Groups and child assignments require a valid matching organization | Supply a valid OrganizationId or OrganizationCode | OrganizationId, OrganizationCode |
| group_source | Valid group source | Yes | Create a group | Verify | ORA_WIE_SOURCE lookup | resolve_work_order_group_source | Group source controls eligible work-order methods | Use a valid source such as ORA_MANUFACTURING or ORA_MAINTENANCE | GroupSource |
| work_order_eligibility | Eligible unassigned same-organization work order | Yes | Add a work order to a group | Verify | Work order and group metadata | resolve_work_order_for_group | Ineligible statuses, an existing group assignment, organization mismatch, or source-method mismatch block assignment | Supply an eligible work order or remove it from its existing group through its approved workflow | WorkOrderId, WorkOrderNumber, OrganizationId, status, work method |
| parent_delete_readiness | Parent group has no child assignments | Yes | Delete a group | Verify | workOrderGroups child-assignment validation | resolve_work_order_group_by_id | A group with any child assignment cannot be deleted | Delete all child assignments first through the approved Data Loader workflow | WoGroupId, child-assignment result |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| satisfied | Every applicable access, object, organization, source, work-order, and delete prerequisite is confirmed | Read-only lookup only; no import is authorized here. |
| blocked | A required privilege, object, organization, source, work order, or delete prerequisite is missing, invalid, protected, or ambiguous | Read-only verification only; stop before preview. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WOGROUP.DEPENDENCIES | decision | 4 | resolve_dependency | ready->WOGROUP.DESIGN;blocked->WOGROUP.BLOCKED | WOGROUP.LOOKUPS | stop | Applicable work order group dependencies are evaluated. |

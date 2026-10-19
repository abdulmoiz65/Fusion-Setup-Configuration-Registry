# Input Validation

Sources: Oracle Fusion Cloud SCM, *Redwood: Group Work Orders to Perform Mass Actions*; `workOrderGroups_rest_rules_summary.txt` supplied by the developer.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Group create identity | GroupCode; GroupName; OrganizationId or OrganizationCode | Block preview | Supply all required business fields | Creating a work order group | resolve_work_order_group_organization |
| Group update or delete identity | WoGroupId or one unique existing group identity | Block preview | Select exactly one group | Updating, inactivating, or deleting a group | resolve_work_order_group_by_id |
| Work order assignment | WorkOrderId, or WorkOrderNumber with the parent group organization | Block child preview | Supply an exact work-order identity in the same organization | Adding a work order to a group | resolve_work_order_for_group |
| Optional group fields | GroupSource; GroupDescription; InactiveDate; documented DFF values | Accept omitted values | Omit a field unless the intended change requires it | Group create or update |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| GroupCode | Require a nonblank value of 30 characters or fewer and reject a duplicate within OrganizationId plus GroupSource | Create or update | resolve_work_order_group_by_code |
| GroupName | Require a nonblank value of 120 characters or fewer and reject a duplicate within OrganizationId plus GroupSource | Create or update | resolve_work_order_group_by_name |
| GroupSource | Accept a valid ORA_WIE_SOURCE lookup code of 30 characters or fewer; default only to ORA_MANUFACTURING | Create | resolve_work_order_group_source |
| Organization | Require an existing OrganizationId or resolvable OrganizationCode | Create | resolve_work_order_group_organization |
| InactiveDate | Require a date later than the current database date when the validation applies | Create or update when supplied |  |
| Insert-only header fields | Reject a change to GroupSource or OrganizationId after creation | Update |  |
| Child assignment fields | Do not repoint WorkOrderId or change child OrganizationId on an existing assignment | Child update |  |
| System-managed fields | Do not supply group or detail IDs, audit fields, status, or ObjectVersionNumber on create unless the live Data Loader contract expressly requires them | Create |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WOGROUP.VALIDATE_INPUT | decision | 1 | validate_input | valid->WOGROUP.APPLY_DEFAULTS;invalid->WOGROUP.BLOCKED | none | stop | A work order group header, assignment, update, deactivation, or delete request is prepared. |

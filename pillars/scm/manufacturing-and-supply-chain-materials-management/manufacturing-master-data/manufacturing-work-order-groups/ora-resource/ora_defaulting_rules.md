# Defaulting Rules

Source: `workOrderGroups_rest_rules_summary.txt` supplied by the developer.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| GroupSource | ORA_MANUFACTURING | Creating a group and GroupSource is omitted | Yes |  |
| OrganizationId | Resolved from OrganizationCode | Creating a group with a valid OrganizationCode and no OrganizationId | Yes | resolve_work_order_group_organization |
| Child OrganizationId | Parent work order group OrganizationId | Creating a child assignment under an existing parent group | No | resolve_work_order_group_by_id |
| WorkOrderId | Resolved from WorkOrderNumber plus the group OrganizationId | Creating a child assignment with WorkOrderNumber and no WorkOrderId | Yes | resolve_work_order_for_group |
| Group and detail identifiers; audit and version fields | Fusion-managed infrastructure values | Creating or updating headers or assignments | No |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WOGROUP.APPLY_DEFAULTS | step | 2 | apply_default | applied->WOGROUP.LOOKUPS | WOGROUP.VALIDATE_INPUT | stop | A valid work order group request is being prepared. |

# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Item status identity | Status Code and Status Name | Reject the record and return the missing field names | Provide both required values | A status record is supplied for validation | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Status Code required | Reject when Status Code is blank or absent | A status record is supplied | |
| Status Code length | Reject when Status Code exceeds 10 characters | Status Code is supplied | |
| Status Code spaces | Reject when Status Code contains a space | Status Code is supplied | |
| Status Name required | Reject when Status Name is blank or absent | A status record is supplied | |
| Status Name length | Reject when Status Name exceeds 240 characters | Status Name is supplied | |
| Status Description length | Reject when Status Description exceeds 240 characters | Status Description is supplied | |
| Operational attribute display name required | Reject when AttrDispName is blank or absent | One or more operational attributes are provided for update or lookup | resolve_item_operational_attribute |
| Status-controlled attribute values | Reject when any supplied status-controlled attribute is not Y or N | A status-controlled attribute is supplied | |
| Inventory Item prerequisite | Reject when `STOCK_ENABLED_FLAG` or `BUILD_IN_WIP_FLAG` is `Y` and the immutable source does not also set `INVENTORY_ITEM_FLAG` to `Y`, or the fresh exported baseline does not evidence `INVENTORY_ITEM_FLAG` as `Y` for the same Item Status Code. Set Inventory Item to `Y` first, obtain a fresh exported baseline, then prepare and validate the dependent update. | Stocked or Build in WIP is set to `Y` | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IST.VALIDATE-INPUT | step | 10 | validate_input | valid->IST.VALIDATE_INVENTORY_PREREQUISITE;invalid->RETURN_ISSUES | none | stop | A Manage Item Statuses record is supplied for validation |
| IST.VALIDATE_INVENTORY_PREREQUISITE | step | 15 | validate_input | valid->IST.DEFAULT_STATUS_CONTROL;invalid->RETURN_ISSUES | IST.VALIDATE-INPUT | stop | Stocked or Build in WIP is set to Y |

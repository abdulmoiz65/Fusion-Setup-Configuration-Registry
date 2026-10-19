# Input Validation

Source: Oracle Fusion Cloud SCM, *How You Manage Work Order Statuses*; `workOrderStatuses_rest_rules_summary.txt` supplied by the developer.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Create identity | WoStatusCode; WoStatusName; WoSystemStatusCode | Block preview | Supply all three business fields | Creating a user-defined work order status |  |
| Update identity | WoStatusId or one unique existing status identity; requested mutable fields | Block preview | Select exactly one existing status and provide only supported changes | Updating or deactivating a status | resolve_work_order_status_by_id |
| Delete identity | WoStatusId or one unique existing status identity | Block preview | Select exactly one existing status | Deleting a status | resolve_work_order_status_by_id |
| Optional business fields | WoStatusDescription; InactiveDate | Accept omitted values | Omit the field when it is not required by the intended change | Create or user-defined update |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| WoStatusCode | Require a nonblank value of 30 characters or fewer and reject an existing code | Create | resolve_work_order_status_by_code |
| WoStatusName | Require a nonblank value of 120 characters or fewer and reject an existing name | Create or rename | resolve_work_order_status_by_name |
| WoStatusDescription | Accept a value of 240 characters or fewer | Create or update |  |
| WoSystemStatusCode | Require a nonblank value of 30 characters or fewer from lookup type ORA_WIE_WO_SYSTEM_STATUS; use the lookup code, not an ORA_-prefixed display variant | Create | resolve_work_order_system_status |
| PENDING_APPROVAL | Reject PENDING_APPROVAL for a user-defined create | Create |  |
| InactiveDate | Require a date strictly later than the current database date | Create or user-defined update when supplied |  |
| System-managed fields | Do not supply WoStatusId, SeededFlag, audit fields, or ObjectVersionNumber on create unless the live Data Loader contract expressly requires them | Create |  |
| Immutable fields | Reject a requested change to WoStatusCode or WoSystemStatusCode after creation | Update |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WOSTATUS.VALIDATE_INPUT | decision | 1 | validate_input | valid->WOSTATUS.APPLY_DEFAULTS;invalid->WOSTATUS.BLOCKED | none | stop | A work order status create, update, deactivate, or delete request is prepared. |

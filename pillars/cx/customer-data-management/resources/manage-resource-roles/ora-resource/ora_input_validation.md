# Manage Resource Roles Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve |
|---|---|---|---|
| Role identity | Role Name and Role Code | Block | Provide both values |
| Role classification | Role Type or RoleTypeCode and Orientation | Block | Provide a role type that exists as an exact `LookupCode` in the `JTF_RS_ROLE_TYPE` standard lookup, and a documented orientation. |

## Field Validation

| Check | What Happens |
|---|---|
| Role Type | Require a nonblank Role Type or RoleTypeCode that exactly matches an existing `LookupCode` in the `JTF_RS_ROLE_TYPE` standard lookup. |
| Orientation | Require Member for an individual, Manager for a managerial, or Administrator for an administrative resource |
| Requested operation | Route only a read request to Resource Roles REST GET, and only a create/update FSM CSV request to `shared.setup-import.task-level-import`. Block REST create/update/delete and FSM delete. |

If the role type is not found, block the role operation. Direct the user to
`cx.customer-data-management.resources.manage-resource-role-lookups` (Manage
Resource Role Lookups) to create or activate the required lookup code through
the approved lookup workflow, then repeat this validation.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRR.VALIDATE | decision | 2 | validate_input | valid->MRR.ROLE_TYPE_LOOKUP;invalid->MRR.BLOCKED | MRR.COLLECT | stop | Role inputs are collected |

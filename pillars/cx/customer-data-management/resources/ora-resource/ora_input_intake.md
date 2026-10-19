# Manage Resource Roles Input Intake

## Accepted Input Formats

| Task Code | Task Name | Input Format | What Must Be Provided | Applies To |
|---|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Interactive role definition | Role Name, Role Code, Role Type, and Orientation | Each resource role to create |

## Dependency Inputs

| Task Code | Task Name | Field | Mandatory | Purpose | Send in Request Body? | Lookup Rule |
|---|---|---|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Role Name | Yes | Identify the resource role | No | Not documented |
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Role Code | Yes | Supply the organization role code | No | Not documented |
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Role Type | Yes | Classify the role | No | Use Service |
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Orientation | Yes | Classify responsibility | No | Use Member, Manager, or Administrator |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | MRR.COLLECT | step | 1 | collect_input | valid->MRR.VALIDATE;missing->MRR.BLOCKED | none | stop | A resource role is requested |

# Manage Resource Roles Input Validation

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve |
|---|---|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Role identity | Role Name and Role Code | Block | Provide both values |
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Role classification | Role Type and Orientation | Block | Select Service and a documented orientation |

## Field Validation

| Task Code | Task Name | Check | What Happens |
|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Role Type | Require Service |
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Orientation | Require Member for an individual, Manager for a managerial, or Administrator for an administrative resource |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | MRR.VALIDATE | decision | 2 | validate_input | valid->MRR.DEPENDENCIES;invalid->MRR.BLOCKED | MRR.COLLECT | stop | Role inputs are collected |

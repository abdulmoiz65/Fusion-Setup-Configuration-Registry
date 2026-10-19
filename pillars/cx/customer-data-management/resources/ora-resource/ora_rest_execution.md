# Manage Resource Roles Execution Contract

## Runtime Sources

| Task Code | Task Name | Source | Purpose |
|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Supplied Oracle Manage Resource Roles documentation | Define the documented UI creation steps and identify the missing REST contract |

## Execution Contract

| Task Code | Task Name | Situation | What Happens |
|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Runtime execution is requested | Block because the supplied source documents only the Setup and Maintenance UI flow and no writable REST contract |
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Manual setup is performed | Navigate to Setup and Maintenance, open Users and Security, select Manage Resource Roles, create the role, enter the documented fields, and save and close |

## Endpoint

| Task Code | Task Name | Action | Method | Path |
|---|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Create resource role | TBD | TBD — no REST endpoint is documented in the supplied source |

## Preview Pattern

| Task Code | Task Name | Step | Requirement |
|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Review role definition | Confirm name, code, Service role type, and orientation before manual save |

## Live Pattern

| Task Code | Task Name | Step | Requirement |
|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Execute through REST | Not available until an approved Oracle REST contract is supplied |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | MRR.RUNTIME_CONTRACT | decision | 6 | approval_gate | blocked->MRR.BLOCKED | MRR.ENFORCE | stop | Runtime execution is requested without a documented REST contract |

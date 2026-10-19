# Manage Resource Roles Error Handling

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Required role inputs are incomplete or invalid | Stop and request corrected values |
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Required role and type association is not verified | Stop before adding users or assigning work |
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Runtime REST execution is requested | Stop and request approved Oracle endpoint and request-contract guidance |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | No writable REST contract is supplied | Do not invent an endpoint, payload, or REST execution behavior |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | MRR.BLOCKED | terminal | 7 | terminal | none | none | stop | Any validation, dependency, design, or execution-contract blocker occurs |

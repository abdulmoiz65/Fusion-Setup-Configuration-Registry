# Manage Resource Roles Design Advisory

## Guidance Sources

| Task Code | Task Name | Source Mode | Allowed Sources | When Used |
|---|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Oracle documentation | Supplied Manage Resource Roles documentation | When defining a Field Service resource role |

## Guidance Topics

| Task Code | Task Name | Topic | Advisory Level | What To Explain | Do Not Include |
|---|---|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Resource role versus job role | Required context | Resource roles manage Field Service resource types; job roles control access | Unsupported equivalence between role types |
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | Role orientation | Required context | Member is individual, Manager is managerial, and Administrator is administrative | Undocumented orientations |

## Output Rules

| Task Code | Task Name | Situation | What Happens |
|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | A job triggers automatic resource-role assignment | Direct the user to Manage Users; do not treat the job as a replacement for a resource role |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | MRR.ADVISORY | step | 4 | design_advisory | reviewed->MRR.ENFORCE | MRR.DEPENDENCIES | stop | Resource-role design is ready for review |

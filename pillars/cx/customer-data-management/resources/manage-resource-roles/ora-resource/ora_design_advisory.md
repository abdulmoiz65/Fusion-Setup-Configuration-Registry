# Manage Resource Roles Design Advisory

## Guidance Sources

| Source Mode | Allowed Sources | When Used |
|---|---|---|
| Oracle documentation | Supplied Manage Resource Roles documentation | When defining a Field Service resource role |

## Guidance Topics

| Topic | Advisory Level | What To Explain | Do Not Include |
|---|---|---|---|
| Resource role versus job role | Required context | Resource roles manage Field Service resource types; job roles control access | Unsupported equivalence between role types |
| Role orientation | Required context | Member is individual, Manager is managerial, and Administrator is administrative | Undocumented orientations |

## Output Rules

| Situation | What Happens |
|---|---|
| A job triggers automatic role assignment | Direct the user to Manage Users; do not treat the job as a replacement for a resource role |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRR.ADVISORY | step | 5 | design_advisory | reviewed->MRR.ENFORCE | MRR.DEPENDENCIES | stop | Resource-role design is ready for review |

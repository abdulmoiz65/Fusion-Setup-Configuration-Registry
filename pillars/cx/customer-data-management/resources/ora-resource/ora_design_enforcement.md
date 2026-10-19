# Manage Resource Roles Design Enforcement

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | 1 | Establish roles and types | Create and associate all needed resource roles and resource types before adding users |

## Design Rules

| Task Code | Task Name | Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | MRR-ROLE-TYPE-ASSOCIATION | Before adding users | Blocker | Manual UI verification | A required role or resource type is not created and associated | Complete role and type associations first | Yes |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| HZ_MANAGE_RESOURCE_ROLES | Manage Resource Roles | MRR.ENFORCE | decision | 5 | design_enforcement | passed->MRR.RUNTIME_CONTRACT;blocked->MRR.BLOCKED | MRR.ADVISORY | stop | Resource-role design is reviewed |

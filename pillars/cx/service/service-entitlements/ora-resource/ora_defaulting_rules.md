# Defaulting Rules

## Standard Defaults

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | MilestoneType | ORA_SVC_NO_REPEAT | Operation is create and MilestoneType is omitted | No |  |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | AllowAgentCompletionFlag | false | Operation is create and AllowAgentCompletionFlag is omitted | No |  |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | AllowDueDateOverrideFlag | false | Operation is create and AllowDueDateOverrideFlag is omitted | No |  |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | DeletedFlag | false | Operation is create and DeletedFlag is omitted | No |  |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | DisabledFlag | false | Operation is create and DisabledFlag is omitted | No |  |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | BusinessUnitName | Default business unit selected in Setup and Maintenance | Operation is create in a non-BU-specific request | Yes |  |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | SVCMILESTONE.DEFAULTS | step | 2 | apply_default | ok->SVCMILESTONE.LOOKUP;failure->SVCMILESTONE.FAILED | SVCMILESTONE.VALIDATE | stop | Create or update preview after required input validation |

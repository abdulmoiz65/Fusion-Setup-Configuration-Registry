# Design Enforcement

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | 1 | Confirm milestone type behavior | The implementation owner must choose whether the milestone can be reopened, can be repeated, or cannot be repeated |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | 2 | Confirm service request conditions | Start, pause, and completion criteria must be documented before preview |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | 3 | Confirm BU scope | BU-specific milestones must be configured for every BU that intends to track them |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | 4 | Confirm coverage application | The coverage level that will apply the milestone to service requests must be identified |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Milestone type is omitted on create | Error |  | The milestone repeat or reopen behavior is not explicitly selected or defaulted | Use ORA_SVC_NO_REPEAT only when the business confirms the milestone must not reopen or repeat | Yes |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Start, pause, or completion criteria are missing | Error |  | The milestone cannot be evaluated against service requests | Provide static, field-based, or object-function criteria with human-readable labels | Yes |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Multiple condition rows are configured for one criteria section | Warning |  | The reviewer has not acknowledged that all rows must evaluate true together | Show the combined AND behavior in preview | Yes |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Business Units feature is enabled | Error |  | The request does not identify the BU that will track the milestone | Create or update one milestone configuration per BU that must track it | Yes |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | BU feature is enabled and no milestone is configured for a service request BU | Error |  | Service requests for that BU will not receive milestones | Configure milestones for the assigned BU or confirm the BU should not track milestones | Yes |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Agent due-date override or agent completion is enabled | Warning |  | Audit and operational ownership were not reviewed | Confirm whether due-date audit and agent completion behavior match the service policy | Yes |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Subscription coverages are used for entitlements | Warning |  | Coverage precedence was not reviewed | Confirm that subscription or contract coverage overrides customer-level and global defaults as expected | Yes |

## Design Lookup Requirements

| Task Code | Task Name | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | find_milestone_by_alt_key | Duplicate create, update, or delete preview | MilestoneConfigId, MilestoneCode, ObjectName, BUOrgId, DisabledFlag | ora_reference_lookups.md |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | get_milestone_by_id | Existing milestone comparison by primary key | MilestoneConfigId, MilestoneCode, ObjectName, BUOrgId, MilestoneType, DisabledFlag | ora_reference_lookups.md |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | SVCMILESTONE.DESIGN | step | 5 | design_enforcement | ok->SVCMILESTONE.READY;failure->SVCMILESTONE.FAILED | SVCMILESTONE.DEPENDENCIES | stop | Before milestone configuration preview is treated as ready |

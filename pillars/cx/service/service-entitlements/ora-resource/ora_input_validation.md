# Input Validation

## Required Groups

| Task Code | Task Name | Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Milestone create identity | MilestoneCode, ObjectName, MilestoneType | Block preview | Ask for the milestone code, service object name, and milestone type before create preview | Operation is create |  |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Milestone update or delete identity | MilestoneConfigId or MilestoneCode plus ObjectName plus optional BUOrgId | Block preview | Ask for a milestone configuration identifier or the alternate key needed to find exactly one milestone | Operation is update or delete | find_milestone_by_alt_key |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Display and condition details | MilestoneLabel, StartCondition, StartConditionLabel, PauseCondition, PauseConditionLabel, StopCondition, StopConditionLabel | Continue for optional values | Omit optional fields unless supplied by the implementation owner | Operation is create or update |  |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Threshold and behavior controls | ThresholdCode, AllowDueDateOverrideFlag, AllowAgentCompletionFlag, TzPreferenceCd, DisabledFlag | Continue for optional values | Apply documented defaults for omitted boolean controls and require supplied threshold or time-zone values to match configured setup | Operation is create or update |  |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Multiple business unit scope | BUOrgId or BusinessUnitName | Block preview when BU-specific milestones are requested | Ask for the business unit identifier or name for each BU that tracks the milestone | Business Units feature is enabled and the request is BU-specific |  |

## Dependency-Aware Validation

| Task Code | Task Name | Applies When | Result | Next Action | Resolver |
|---|---|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Alternate-key lookup finds an existing milestone and operation is create | Blocked | Switch to update or choose a milestone code, object name, and BU scope that do not already exist | find_milestone_by_alt_key |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Lookup finds no milestone and operation is update or delete | Blocked | Switch to create or provide an existing MilestoneConfigId | find_milestone_by_alt_key |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Request includes both MilestoneConfigId and alternate key fields | Satisfied | Prefer MilestoneConfigId for item lookup and disclose any alternate-key mismatch before preview | get_milestone_by_id |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | BU-specific request omits BUOrgId and BusinessUnitName | Blocked | Ask for the business unit because milestones must be defined per BU when the BU feature is enabled |  |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Request uses a static condition such as Immediate or Never | Satisfied | Do not require operator or value fields for that condition row |  |

## Field Validation

| Task Code | Task Name | Check | What Happens | Applies When | Resolver |
|---|---|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | MilestoneCode length exceeds 255 characters | Reject before preview | MilestoneCode is supplied |  |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | MilestoneLabel length exceeds 255 characters | Reject before preview | MilestoneLabel is supplied |  |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | ObjectName length exceeds 255 characters | Reject before preview | ObjectName is supplied |  |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | StartCondition, PauseCondition, StopCondition, or matching label exceeds 1000 characters | Reject before preview | Any condition or label is supplied |  |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | AllowDueDateOverrideFlag, AllowAgentCompletionFlag, DisabledFlag, or DeletedFlag is not boolean | Reject before preview | Boolean control is supplied |  |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | MilestoneType is omitted on create | Apply documented default ORA_SVC_NO_REPEAT before preview | Operation is create |  |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Condition row combines multiple condition rows | Disclose that multiple condition rows are evaluated together with AND | Start, pause, or completion condition has more than one row |  |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | SVCMILESTONE.VALIDATE | step | 1 | validate_input | ok->SVCMILESTONE.DEFAULTS;failure->SVCMILESTONE.FAILED | none | stop | Every milestone configuration request |

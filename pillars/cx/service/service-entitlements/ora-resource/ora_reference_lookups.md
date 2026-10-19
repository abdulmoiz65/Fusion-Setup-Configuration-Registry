# Reference Lookups

## Live Lookups

| Task Code | Task Name | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | find_milestone_by_alt_key | MilestoneConfigId is missing and MilestoneCode plus ObjectName are supplied | MilestoneCode, ObjectName, optional BUOrgId | /crmRestApi/resources/11.13.18.05/milestones?finder=MilestoneConfigVOAltKey;BUOrgId={BUOrgId},MilestoneCode={MilestoneCode},ObjectName={ObjectName}&fields=MilestoneConfigId,MilestoneCode,ObjectName,BUOrgId,BusinessUnitName,MilestoneLabel,DisabledFlag&onlyData=true | MilestoneConfigId, MilestoneCode, ObjectName, BUOrgId, BusinessUnitName, MilestoneLabel, DisabledFlag | Match exactly one milestone by alternate key; omit BUOrgId only for non-BU-specific requests | MilestoneConfigId: MilestoneConfigId; BusinessUnitName: BusinessUnitName; DisabledFlag: DisabledFlag | If no match, route create requests forward and block update or delete; if many matches, stop and ask for MilestoneConfigId or BUOrgId |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | get_milestone_by_id | MilestoneConfigId is supplied | MilestoneConfigId | /crmRestApi/resources/11.13.18.05/milestones/{MilestoneConfigId}?fields=MilestoneConfigId,MilestoneCode,ObjectName,BUOrgId,BusinessUnitName,MilestoneLabel,MilestoneType,ThresholdCode,StartCondition,PauseCondition,StopCondition,DisabledFlag&onlyData=true | MilestoneConfigId, MilestoneCode, ObjectName, BUOrgId, BusinessUnitName, MilestoneLabel, MilestoneType, ThresholdCode, StartCondition, PauseCondition, StopCondition, DisabledFlag | Match the item returned for the supplied MilestoneConfigId | Existing milestone fields for preview comparison | If no match, block update or delete and ask for a valid MilestoneConfigId |

## Lookup Execution Rules

| Task Code | Task Name | Situation | What Happens |
|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Request uses alternate-key lookup with Business Units enabled | Require BUOrgId when the same milestone code and object name can exist for more than one BU |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Request asks only to view the milestone configuration | Run the lookup and return the milestone fields without preparing a write |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Lookup response contains read-only fields | Use read-only fields for comparison and disclosure only; never send them in a create or update body |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | SVCMILESTONE.LOOKUP | step | 3 | reference_lookup | found->SVCMILESTONE.DEPENDENCIES;not_found->SVCMILESTONE.DEPENDENCIES;failure->SVCMILESTONE.FAILED | SVCMILESTONE.DEFAULTS | stop | MilestoneConfigId or alternate key is available |

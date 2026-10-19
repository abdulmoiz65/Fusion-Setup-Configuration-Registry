# Error Handling

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Required milestone identity is missing | Stop and ask for the missing MilestoneConfigId or alternate key fields |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Alternate-key lookup returns more than one milestone | Stop and ask for MilestoneConfigId or BUOrgId |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Matrix result column is not confirmed | Stop before preview and ask the implementation owner to confirm the milestone and threshold result columns |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Oracle rejects a create, update, or delete request | Show the operation, milestone identity, endpoint path, and Oracle error payload; stop before retry |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Documentation lookup is needed to explain a live Oracle error | Ask before looking up additional documentation |

## Error Classifications

| Task Code | Task Name | Result Category | When Used | Next Action |
|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | input validation | Required field, field length, boolean shape, or condition contract is invalid | Ask for corrected input |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | dependency readiness | Matrix class, default BU, BU scope, or coverage plan is missing | Resolve the prerequisite before preview |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | fusion api | Milestone REST lookup or live write returns an Oracle error | Preserve the request identifiers and stop before retry |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | approval blocker | The request would create, update, or delete milestone configuration without explicit approval | Return the preview and wait for approval |

## Disclosure Rules

| Task Code | Task Name | Gate | What Must Be Shown |
|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Before preview | Operation, milestone identity, BU scope, condition summary, defaults applied, and lookup result |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Before live change | HTTP method, REST path, path parameters, request body fields, and expected response shape |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | After live failure | Oracle status, error code or message, request path, milestone identity, and whether any partial update is known |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Live create, update, or delete has not been approved | Do not call POST, PATCH, or DELETE |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Milestone identity is ambiguous | Do not choose one record from multiple lookup results |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | BU feature is enabled but BU scope is missing | Do not create a global-looking milestone as a substitute for BU-specific setup |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | Oracle error occurs during live execution | Do not retry or search documentation automatically |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | SVCMILESTONE.READY | terminal | 6 | terminal | none | SVCMILESTONE.DESIGN | stop | Milestone configuration guidance is ready for preview handoff |
| ORA_SVC_MANAGE_MILESTONE_CONFIG | Manage Service Milestone Configuration | SVCMILESTONE.FAILED | terminal | 7 | terminal | none | none | stop | Any validation, lookup, dependency, or design gate fails |

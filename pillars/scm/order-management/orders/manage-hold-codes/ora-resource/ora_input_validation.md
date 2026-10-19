# Manage Hold Codes Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Hold identity | HoldCode and HoldName | Stop before source generation | Provide both values | Every create | |
| Reference set | SetCode | Stop before source generation | Provide a set code; do not provide SetId or SetName as a substitute | Every create or update that changes the set | resolve_hold_reference_set |
| Task-specific mapping | Exact TaskTypeName | Stop before source generation | Provide at least one eligible task | GeneralHoldFlag is false | resolve_hold_task_definition |
| Role mapping | Exact RoleName for each restricted apply or release action | Stop before source generation | Provide the role name for each requested action | ApplyHoldRoleEligibility or ReleaseHoldRoleEligibility is R | resolve_hold_role |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Hold identity uniqueness inputs | Require a nonblank HoldCode and the supplied or defaulted OrchestrationApplicationId before the uniqueness check. | Every create or update | check_hold_code_uniqueness |
| Date ordering | Reject an end date earlier than the effective start date. | An EffectiveEndDate is supplied | |
| Generic and task-specific flags | A generic hold has no task mapping. A task-specific hold has at least one eligible task and does not use Pause. | Every create or mapping change | resolve_hold_task_definition |
| Role eligibility | Accept A for all roles or R for role-restricted access. Require corresponding access-role mappings for R. | Every create or eligibility change | resolve_hold_role |
| Create identifier | Omit HoldCodeId from a new parent record; the business object generates it. | Every create | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HOLD_CODES.VALIDATE_INPUT | step | 10 | validate_input | valid->HOLD_CODES.APPLY_DEFAULTS;invalid->RETURN_ISSUES | none | stop | Before preparing a Manage Hold Codes source or preview. |

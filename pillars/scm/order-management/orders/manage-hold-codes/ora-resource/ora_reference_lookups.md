# Manage Hold Codes Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_hold_reference_set | Before creating or updating a hold set assignment | SetCode | /fscmRestApi/resources/11.13.18.05/omSetIdSetsLOV with finder=IntentFinder;Intent=DOO_MANAGE_ORCHESTRATION_HOLD_CODE_DEFINITION_DATA | SetCode, SetId, SetName | Prefer one case-sensitive SetCode match; otherwise accept exactly one case-insensitive SetCode match and retain its canonical casing. | Canonical SetCode, SetId, SetName | Stop on no match, multiple case-insensitive matches, or unavailable lookup. |
| check_hold_code_uniqueness | Before creating or selecting an existing hold | HoldCode, OrchestrationApplicationId | /fscmRestApi/resources/11.13.18.05/omHoldDefinitions | HoldCode, OrchestrationApplicationId, HoldCodeId | For create, require no exact HoldCode and OrchestrationApplicationId match. For update, require exactly the intended existing match. | Existing-hold identity or uniqueness result | Stop on missing, ambiguous, or unavailable result. |
| resolve_hold_task_definition | Before preparing a task-specific mapping | Exact TaskTypeName | /fscmRestApi/resources/11.13.18.05/omHoldTaskDefinitions | CheckHoldsFlag, ServiceCode, ServiceId, ServiceName, TaskTypeId, TaskTypeName | Require exactly one exact TaskTypeName and positive numeric ServiceId and TaskTypeId. | ServiceId, ServiceName, TaskTypeId, TaskTypeName | Stop on no match, multiple matches, inactive mapping, or nonnumeric identifier. |
| resolve_hold_role | Before preparing a restricted access-role record | Exact RoleName | /hcmRestApi/resources/11.13.18.05/rolesLOV | RoleName, RoleId | Require exactly one exact RoleName and a positive numeric RoleId. | RoleName, RoleId | Stop on no match, multiple matches, nonnumeric ID, or unavailable lookup. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup returns more pages | Follow pagination before evaluating the match rule. |
| A role, task, set, or hold identity is shown to a user | Show the resolved business name alongside its identifier. |
| A lookup fails | Stop before source generation, preview, upload, or mutation; retain only redacted diagnostics. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HOLD_CODES.RESOLVE_SET | step | 30 | reference_lookup | resolved->HOLD_CODES.CHECK_UNIQUENESS;unresolved->RETURN_ISSUES;failure->RETURN_ISSUES | HOLD_CODES.APPLY_DEFAULTS | stop | A hold request has passed input validation and defaulting. |
| HOLD_CODES.CHECK_UNIQUENESS | step | 40 | reference_lookup | unique-or-identified->HOLD_CODES.ENFORCE_DESIGN;ambiguous-or-conflict->RETURN_ISSUES;failure->RETURN_ISSUES | HOLD_CODES.RESOLVE_SET | stop | Before creating or updating a hold definition. |

# Manage Hold Codes Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate identity and dates | Confirm required values and logical effective dates. |
| 2 | Resolve dependencies | Use the documented set, identity, task, and role resolvers as applicable. |
| 3 | Enforce hold design | Apply generic-versus-task-specific, role, and system-hold constraints. |
| 4 | Prepare immutable source | Use the current Data Loader template and its permitted relationships. |
| 5 | Gate execution | Obtain the separate approval required immediately before upload. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every create | Error | check_hold_code_uniqueness | The exact HoldCode and OrchestrationApplicationId combination already exists. | Choose a unique code or select the intended existing hold for update. | Yes |
| A task-specific hold is requested | Error | resolve_hold_task_definition | No eligible task exists, the mapping is ambiguous, or Pause is selected. | Provide one eligible exact task type. | Yes |
| Restricted apply or release eligibility is requested | Error | resolve_hold_role | A requested action has no exact resolved role mapping. | Provide the exact role name for each action. | Yes |
| A role-specific mapping is prepared | Error | resolve_hold_role | The source lacks a corresponding role mapping or attempts to use a guessed role ID. | Use the resolved numeric RoleId and correct action flags. | Yes |
| Every create | Error | | SystemFlag is true, a HoldCodeId is preallocated, or a backend-generated parent ID is invented for child linkage. | Set SystemFlag to false, omit HoldCodeId, and use only template-supported child linkage. | Yes |
| A delete is requested | Error | check_hold_code_uniqueness | The hold is applied to sales orders, is a system hold, or its required child identities are not enumerated. | Stop and use the existing-hold read-only baseline before a Data Loader delete. | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| check_hold_code_uniqueness | Before every create or existing-hold update | Exact hold and application identity or no-match evidence | ora_reference_lookups.md |
| resolve_hold_task_definition | Before every task-specific mapping | Service and task identifiers with exact names | ora_reference_lookups.md |
| resolve_hold_role | Before every restricted action mapping | Exact RoleName and numeric RoleId | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HOLD_CODES.ENFORCE_DESIGN | step | 50 | design_enforcement | compliant->HOLD_CODES.APPROVAL_GATE;noncompliant->RETURN_ISSUES | HOLD_CODES.CHECK_UNIQUENESS | stop | A hold request has resolved its mandatory identity and set lookups. |

# Manage Hold Codes Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Reference set | Resolve the requested SetCode before source generation. |
| 2 | Hold identity | Confirm the HoldCode and OrchestrationApplicationId combination is valid for the requested operation. |
| 3 | Task mapping | Resolve the task and service identifiers when the hold is task-specific. |
| 4 | Role mappings | Resolve every role identifier when eligibility is restricted. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| reference_set | Order Management reference set | Yes | Every create or set update | Lookup | Read-only Fusion lookup | resolve_hold_reference_set | The hold must use an authoritative set identity. | Provide SetCode only. | SetCode, SetId, SetName |
| hold_identity | Hold-code and application identity | Yes | Every create or update | Verify | Read-only Fusion lookup | check_hold_code_uniqueness | The same hold code can exist only for a different application. | Provide HoldCode; application defaults to 10008 only when omitted. | Existing-hold identity or uniqueness evidence |
| task_mapping | Eligible task and service mapping | Conditional | GeneralHoldFlag is false | Lookup | Read-only Fusion lookup | resolve_hold_task_definition | Task-specific holds require an eligible task mapping. | Provide the exact task type name. | ServiceId, ServiceName, TaskTypeId, TaskTypeName |
| access_role | Apply or release role | Conditional | ApplyHoldRoleEligibility or ReleaseHoldRoleEligibility is R | Lookup | Read-only Fusion lookup | resolve_hold_role | Restricted eligibility requires valid role mappings. | Provide each exact role name and action. | RoleId, RoleName |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The authoritative identifier is already resolved for this unchanged request. | No |
| Lookup | A documented read-only resolver can obtain the missing identifier. | Yes |
| Blocked | The value is missing, ambiguous, or cannot be resolved. | No |

# Performance Roles Design Enforcement

Sources: Performance Roles REST contract and Performance Roles Frontend Validations.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate writable fields | Validate names, dates, role type, status, conditional manager type, and matrix flag. |
| 2 | Resolve existing target | Resolve RoleId and current state for update or delete. |
| 3 | Enforce type-specific rules | Apply manager and participant field restrictions. |
| 4 | Enforce in-use restrictions | Reject protected-field changes for an in-use role. |
| 5 | Gate execution | Require exact validated identity, authorization, and current approval before mutation. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every create | Blocker | | RoleName, DateFrom, or DateTo is missing; the name exceeds 240 characters; or the date range is invalid. | Supply valid required values. | Yes |
| Every create | Blocker | | RoleType is neither MANAGER nor PARTICIPANT, or is WORKER. | Use MANAGER or PARTICIPANT. | Yes |
| Every create or update | Blocker | | Status is not a valid ACTIVE_INACTIVE lookup code. | Use a valid status code. | Yes |
| RoleType is MANAGER | Blocker | | ManagerType is absent or invalid, or MatrixManagerRoleFlag is supplied. | Supply a valid ManagerType and omit MatrixManagerRoleFlag. | Yes |
| RoleType is PARTICIPANT | Blocker | | ManagerType is supplied. | Omit ManagerType. | Yes |
| Update | Blocker | find_performance_role_by_id | RoleType change is requested. | Keep RoleType unchanged because it is insert-only. | No |
| In-use manager role update | Blocker | find_performance_role_by_id | DateFrom, DateTo, or ManagerType changes. | Do not change the protected field. | No |
| In-use participant role update | Blocker | find_performance_role_by_id | MatrixManagerRoleFlag changes. | Do not change MatrixManagerRoleFlag. | No |
| Any mutation | Blocker | | Authorization is missing or the REST entity returns HRC:::HRC_ATOM_NOAUTH. | Use an authorized caller. | Yes |
| Any mutation | Blocker | | Request includes RoleId, BusinessGroupId, ObjectVersionNumber, StatusMeaning, RoleTypeMeaning, or InUseFlag as a writable business field. | Remove read-only or hidden fields from the request. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_performance_role_by_id | Updating or deleting a role, or checking in-use restrictions. | RoleId, RoleType, DateFrom, DateTo, ManagerType, MatrixManagerRoleFlag, InUseFlag. | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PERFORMANCE_ROLES.ENFORCE | decision | 50 | design_enforcement | passed->PERFORMANCE_ROLES.EXECUTION_GATE;blocked->PERFORMANCE_ROLES.STOP_DESIGN | PERFORMANCE_ROLES.DEPENDENCIES | stop | The validated role request requires design and authorization enforcement. |

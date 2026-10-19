# Performance Roles Dependency Readiness

Sources: Performance Roles REST contract and Performance Roles Frontend Validations.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Request validation | Validate the writable request fields and conditional rules. |
| 2 | Existing role resolution | Resolve RoleId before an update or delete. |
| 3 | Authorization | The caller must have the manage-performance-roles permission enforced by the REST entity. |
| 4 | Execution approval | Bind a mutation approval to the exact validated target and operation. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PERFORMANCE_ROLES.TARGET_ROLE | Existing Performance Role | Yes | Update or delete | Lookup | talentPerformanceRoles resource | find_performance_role_by_id | Singleton update and delete endpoints require RoleId. | Resolve and review the exact target role before mutation. | RoleId, RoleName, RoleType, DateFrom, DateTo, Status, InUseFlag |
| PERFORMANCE_ROLES.MANAGE_PERMISSION | Manage Performance Roles permission | Yes | Create, update, or delete | Verify | REST entity authorization | | The REST entity requires the manage-performance-roles permission. | Use an authorized caller; stop on HRC:::HRC_ATOM_NOAUTH. | Authorization result |
| PERFORMANCE_ROLES.IN_USE_RESTRICTIONS | In-use role state | Conditional | A protected field is changed | Lookup | Singleton role response | find_performance_role_by_id | In-use manager and participant roles have protected-field restrictions. | Do not submit a change to a protected field when InUseFlag is Y. | InUseFlag, RoleType, current dates, ManagerType, MatrixManagerRoleFlag |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Lookup | An existing role or its in-use state must be resolved. | Yes, read-only lookup only. |
| Verify | Authorization is enforced by the REST entity. | No |
| Blocked | A required identity, permission, or protected-field condition fails. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PERFORMANCE_ROLES.DEPENDENCIES | decision | 40 | resolve_dependency | ready->PERFORMANCE_ROLES.ENFORCE;blocked->PERFORMANCE_ROLES.STOP_DEPENDENCY | PERFORMANCE_ROLES.RESOLVE_TARGET | stop | Target identity, authorization, and in-use restrictions are evaluated. |

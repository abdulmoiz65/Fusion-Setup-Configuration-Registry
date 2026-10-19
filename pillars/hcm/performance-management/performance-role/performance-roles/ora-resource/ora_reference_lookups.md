# Performance Roles Reference Lookups

Source: Performance Roles REST contract.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_performance_roles_by_name | A role name needs duplicate checking or an update/delete target must be selected. | RoleName query; optional RoleType, Status, InUseFlag, DateFrom, DateTo filters. | POST /latest/talentPerformanceRoles/action/findByAdvancedSearchQuery using application/vnd.oracle.adf.action+json | RoleId, RoleName, RoleDescription, DateFrom, DateTo, Status, RoleType, ManagerType, MatrixManagerRoleFlag, InUseFlag | Query applies to RoleName; filters are limited to RoleType, Status, InUseFlag, DateFrom, and DateTo. | RoleId and current role state. | No match: continue only for a create request. Many matches: stop and select an exact RoleId. |
| find_performance_role_by_id | An update or delete request provides RoleId. | RoleId | GET /latest/talentPerformanceRoles/{RoleId} | RoleId, RoleName, RoleDescription, DateFrom, DateTo, Status, RoleType, ManagerType, MatrixManagerRoleFlag, InUseFlag | PrimaryKey singleton finder uses RoleId. | Current role state and RoleId. | No match: stop; do not substitute another role. Many matches: not applicable to a primary-key finder. |
| resolve_role_status | Status is supplied | Status | ACTIVE_INACTIVE lookup| Code | Exact active/inactive status code | Validated Status | No match: stop as invalid. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A read-only lookup returns an exact role | Use its RoleId and current state only for the declared request. |
| A lookup fails or returns an unsupported response | Stop before a mutation; preserve the sanitized diagnostic. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PERFORMANCE_ROLES.RESOLVE_TARGET | decision | 30 | reference_lookup | resolved->PERFORMANCE_ROLES.DEPENDENCIES;unresolved->PERFORMANCE_ROLES.STOP_DEPENDENCY | PERFORMANCE_ROLES.DEFAULTS | stop | A duplicate check, update, or delete target must be resolved. |

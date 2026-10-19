# Performance Roles Input Validation

Sources: Performance Roles REST contract and Performance Roles Frontend Validations.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Create identity | RoleName, DateFrom, DateTo, RoleType | Stop before create. | Provide all required role values. | Creating a role | |
| Existing-role identity | RoleId | Stop before update or delete. | Resolve the exact role by RoleId. | Updating or deleting a role | find_performance_role_by_id |
| Manager-role details | ManagerType | Stop before create or update. | Provide a valid supervisor-type code. | RoleType is MANAGER | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An update or delete names an existing role | Lookup | Resolve the RoleId before choosing the singleton endpoint. | find_performance_roles_by_name |
| An update or delete supplies RoleId | Lookup | Retrieve the singleton role and validate its current state before the change. | find_performance_role_by_id |
| The role is in use and a participant MatrixManagerRoleFlag change is requested | Blocked | Do not change MatrixManagerRoleFlag. | |
| The role is in use and a manager date or ManagerType change is requested | Blocked | Do not change the protected values. | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| RoleName | Require a nonempty value of at most 240 characters. | Create or update | |
| RoleDescription | Accept an optional value of at most 4000 characters. | Create or update | |
| DateFrom and DateTo | Require both values and require DateFrom to be on or before DateTo. | Create or update | |
| RoleType | Accept only MANAGER or PARTICIPANT. Do not accept WORKER. | Create | |
| Status | Accept a valid ACTIVE_INACTIVE lookup code. | Create or update | |
| ManagerType | Require a valid PER_SUPERVISOR_TYPE lookup code for MANAGER; reject or omit it for PARTICIPANT. | Create or update | |
| MatrixManagerRoleFlag | Accept only Boolean semantics; reject it for MANAGER. | Create or update | |
| RoleId, BusinessGroupId, ObjectVersionNumber, StatusMeaning, RoleTypeMeaning, InUseFlag | Reject as client-writable business fields. | Create or update | |
| RoleType on update | Reject a RoleType change because RoleType is insert-only. | Update | |

| FSM CSV escaping | When creating or regenerating a CSV member, write headers and ordinary values without double quotes. Add double quotes only for an individual value containing a comma, double quote, carriage return, or line feed; double embedded quotes. Reject blanket-quoted CSV members. | FSM CSV import is prepared or revalidated | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PERFORMANCE_ROLES.VALIDATE | decision | 10 | validate_input | valid->PERFORMANCE_ROLES.DEFAULTS;invalid->PERFORMANCE_ROLES.STOP_INVALID | none | stop | A Performance Role create, update, or delete request is prepared. |

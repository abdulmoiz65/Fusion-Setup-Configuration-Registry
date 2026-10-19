# Performance Roles Defaulting Rules

Sources: Performance Roles REST contract and Performance Roles Frontend Validations.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Status | A | A new performance role has no supplied status. | Yes | |
| DateFrom | Current date | A new performance role has no supplied DateFrom. | Yes | |
| DateTo | 4712-12-31 | A new performance rolehas no supplied DateTo. | Yes | |
| RoleType | PARTICIPANT | RoleType is omitted on create. | Yes | |
| ManagerType | LINE_MANAGER | RoleType is MANAGER and ManagerType is omitted during create. | Yes | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PERFORMANCE_ROLES.DEFAULTS | step | 20 | apply_default | complete->PERFORMANCE_ROLES.RESOLVE_TARGET | PERFORMANCE_ROLES.VALIDATE | stop | Input validation passed and create defaults may apply. |

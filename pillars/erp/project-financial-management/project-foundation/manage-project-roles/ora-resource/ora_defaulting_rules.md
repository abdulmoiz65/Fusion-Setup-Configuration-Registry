# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Omitted base/child group | Preserve current rows | Update | No | find_project_role |
| EndDateActive (ToDate alias) | Blank, open-ended | Create | No |  |
| StartDateActive (FromDate alias) | No default | Create; missing value blocks | No |  |
| Enterprise Role | No implicit association | Create | No | resolve_active_enterprise_role |
| Qualifications | Empty | Create and PM implemented | No | resolve_role_children |
| Seeded/read-only fields | Preserve source values; explicit change is refused by design | Update | No | find_project_role |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PROLE.APPLY_DEFAULTS | step | 2 | apply_default | applied->PROLE.FIND_ROLE;failure->PROLE.RETURN_ISSUES | PROLE.VALIDATE_INPUT | stop | Valid input |

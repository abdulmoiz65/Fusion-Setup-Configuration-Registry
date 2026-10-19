# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Existing structure control values | Preserve the exported ActiveFlag, ModuleId, and ObjectStatus values | Updating an existing country row | No, unless the approved design explicitly changes the value | |
| First-time country controls | Use only values supplied by the task-native template and approved design | No exported row exists | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GHS.DEFAULTS | decision | 30 | apply_default | applied->GHS.ENFORCE;issues->GHS.DESIGN_ISSUES | GHS.READINESS | stop | A valid country structure package is being prepared |

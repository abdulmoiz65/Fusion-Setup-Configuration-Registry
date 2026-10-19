# Learning Paths Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| learningItemType | ORA_SPECIALIZATION | Create omits type | No; preserve a supported explicit value | |
| learningItemStatus | ORA_DRAFT | FDD Draft creation is requested | No; send ORA_DRAFT explicitly and validate it instead of accepting the target ORA_ACTIVE default | resolve_learning_path_lifecycle_values |
| learningItemVisibility | PUBLIC | Create omits visibility and the user approves Public visibility | No; never widen visibility silently | |
| Activation behavior | Separate operation | Every create or update | No | |
| Dependency graph | No implicit edges | No predecessor edges are supplied | No; never invent prerequisite ordering | |
| Batch failure scope | Block only the affected row or grouped path | Some rows are invalid | No; preserve valid independent rows for preview | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LPT.APPLY_DEFAULTS | decision | 4 | apply_default | applied->LPT.ENFORCE_DESIGN;preserved->LPT.ENFORCE_DESIGN;blocked->LPT.HANDLE_ERROR | LPT.RESOLVE_REFERENCE | stop | Validated rows omit only a documented safe default |

# Courses Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| learningItemType | ORA_COURSE | Create omits type | No; preserve a supported explicit value | |
| learningItemStatus | ORA_DRAFT | FDD Draft creation is requested | No; send ORA_DRAFT explicitly and validate it rather than accepting the target ORA_ACTIVE default | resolve_course_lifecycle_values |
| learningItemVisibility | PUBLIC | Create omits visibility and the user approves Public visibility | No; never widen visibility silently | |
| Activation behavior | Separate operation | Every create or update | No | |
| Batch failure scope | Block only the affected row | Some rows are invalid | No; preserve valid independent rows for preview | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CRS.APPLY_DEFAULTS | decision | 4 | apply_default | applied->CRS.ENFORCE_DESIGN;preserved->CRS.ENFORCE_DESIGN;blocked->CRS.HANDLE_ERROR | CRS.RESOLVE_REFERENCE | stop | Validated Course rows omit only a documented safe default |

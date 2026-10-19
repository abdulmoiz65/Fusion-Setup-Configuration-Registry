# Manage Classrooms Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Description | Exact user-provided Title | Description is missing and the user explicitly accepts the one-time warning and chooses to continue | No |  |

An explicit Skip means omit an optional field; it is not a default. Never default the classroom count, Bulk intent, Excel-or-DAT choice, Title, Location, Owner, Data Loader keys, Set, Capacity, Contact, Training Supplier, Status, DFF context or segments, or advanced source-reference fields. Never assume COMMON, Active, or any person role.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CL.APPLY_DEFAULTS | decision | 4 | apply_default | applied->CL.ENFORCE_DESIGN;not_applicable->CL.ENFORCE_DESIGN;blocked->CL.BLOCKED;failure->CL.FAILED | CL.CHECK_DEPENDENCIES | stop | Apply only the explicitly accepted Description default; preserve all other values and Skip decisions |

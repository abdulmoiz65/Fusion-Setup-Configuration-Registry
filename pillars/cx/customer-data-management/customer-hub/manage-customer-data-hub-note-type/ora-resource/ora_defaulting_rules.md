# Defaulting Rules

## Standard Defaults
| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| TaskCode | ZCH_MANAGE_DUPLICATE_RESOLUTION_REQUEST_NOTE_TYPE | Export or import | Yes |  |
| Lookup type/category | ZMM_NOTE_TYPE / standardLookups | REST operation | No | resolve_customer_data_hub_note_type |
| Upsert | Disabled | Create | No |  |
| Mutation values | No default | Missing field | No; stop |  |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NT.DEFAULTS | step | 25 | apply_default | applied->NT.DEPENDENCIES;failure->NT.ERROR | NT.LOOKUP | stop | Apply exact parent and safe defaults. |

# Defaulting Rules

## Standard Defaults
| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| TaskCode | ZCH_MANAGE_DUPLICATE_RESOLUTION_REQUEST_NOTE_TYPE_MAPPING | Export or import | Yes |  |
| REST method | GET | Mapping REST request | No | resolve_note_type_mapping |
| Resource | /crmRestApi/resources/11.13.18.05/noteTypes | Mapping REST read | No | resolve_note_type_mapping |
| SourceObjectCode | NOTE | Mapping REST read when SourceObjectCode is omitted | Yes; only NOTE, ZCH_DUP_IDNT_BATCH, or ZCH_DUP_RES_REQUEST are accepted | resolve_note_type_mapping |
| Mutation route | None | POST, PATCH, DELETE, or PUT requested | No; refuse |  |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NTM.DEFAULTS | step | 25 | apply_default | applied->NTM.DEPENDENCIES;failure->NTM.ERROR | NTM.LOOKUP | stop | Apply GET-only and exact task defaults. |

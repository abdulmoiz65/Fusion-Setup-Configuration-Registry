# Input Validation

## Required Groups
| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Read mapping | Environment; optional exact SourceObjectCode limited to NOTE, ZCH_DUP_IDNT_BATCH, or ZCH_DUP_RES_REQUEST; optional exact MappedLookupCode | Stop on unsupported source object or ambiguity | Omit SourceObjectCode to default to NOTE; otherwise use the documented noteTypes GET/finder for one supported source object | Read | resolve_note_type_mapping |
| Import | Immutable ZIP/hash, exact task identity, Task Hook envelope, and approval | Stop before upload | Route through Core Data Loader | Import |  |

## Field Validation
| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| REST method | Permit GET only | REST request | resolve_note_type_mapping |
| SourceObjectCode | Default an omitted value to NOTE; reject values other than NOTE, ZCH_DUP_IDNT_BATCH, or ZCH_DUP_RES_REQUEST | Mapping read | resolve_note_type_mapping |
| Finder | Use NoteTypeFinder with exact BindSourceObjectCode after applying the NOTE default or validating a supported source object | Object-scoped read | resolve_note_type_mapping |
| Mutation | Reject POST, PATCH, DELETE, and PUT because live describe exposes no mutation action | Mutation | resolve_note_type_mapping |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NTM.VALIDATE | step | 10 | validate_input | valid->NTM.LOOKUP;invalid->NTM.ERROR | none | stop | Before mapping read or setup-data routing. |

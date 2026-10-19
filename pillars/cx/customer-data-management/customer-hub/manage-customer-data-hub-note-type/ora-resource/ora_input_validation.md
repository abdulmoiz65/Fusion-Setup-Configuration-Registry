# Input Validation

## Required Groups
| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Read | Environment and optional exact LookupCode | Stop on ambiguity | GET ZMM_NOTE_TYPE or exact code | Read | resolve_customer_data_hub_note_type |
| Mutation | Environment, operation, LookupCode, and changed values | Stop before preview | GET exact type/code and code describe | Create, update, deactivate, or delete | resolve_customer_data_hub_note_type |
| Import | Immutable ZIP/hash, exact task identity, Task Hook envelope, and approval | Stop before upload | Route through Core Data Loader | Import |  |

## Field Validation
| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Parent | Require exact Standard lookup ZMM_NOTE_TYPE at Extensible level | Any REST operation | resolve_customer_data_hub_note_type |
| Identity and seed | Reject type/code rename, ORA_ custom code, silent upsert, and destructive changes to seeded or unknown-origin codes | Mutation | resolve_customer_data_hub_note_type |
| Writable fields | Intersect Extensible rules, seed evidence, and current describe | Mutation | resolve_customer_data_hub_note_type |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NT.VALIDATE | step | 10 | validate_input | valid->NT.LOOKUP;invalid->NT.ERROR | none | stop | Before lookup resolution or setup-data routing. |

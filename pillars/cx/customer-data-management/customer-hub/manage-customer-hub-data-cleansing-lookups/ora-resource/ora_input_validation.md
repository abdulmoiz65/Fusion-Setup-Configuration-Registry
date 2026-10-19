# Input Validation

## Required Groups
| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Read | Environment, exact LookupType, and optional LookupCode | Stop | GET an exact task member | Read | resolve_data_cleansing_lookup |
| Meaning update | Environment, LookupType, LookupCode, and Meaning | Stop before preview | GET exact state and code describe | Update | resolve_data_cleansing_lookup |
| Import | Immutable ZIP/hash, exact task identity, Task Hook envelope, and approval | Stop before upload | Route through Core Data Loader | Import |  |

## Field Validation
| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Membership | Require an exact member of the 10-type inventory in ora_reference_lookups.md | Read or update | resolve_data_cleansing_lookup |
| System restriction | Reject create/delete and every change except Meaning | Update | resolve_data_cleansing_lookup |
| Current evidence | Require System level, exact code, seed evidence, and Meaning writable in current describe | Update | resolve_data_cleansing_lookup |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DCL.VALIDATE | step | 10 | validate_input | valid->DCL.LOOKUP;invalid->DCL.ERROR | none | stop | Before lookup resolution or setup-data routing. |

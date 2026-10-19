# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Read | Environment, exact LookupType, and optional LookupCode | Stop on ambiguity | Select an exact task member and GET current state | Read | resolve_duplicate_management_lookup |
| Mutation | Environment, LookupType, operation, exact code identity, and proposed fields | Stop before preview | GET exact type/code and code describe | Create, update, deactivate, or delete | resolve_duplicate_management_lookup |
| Import | Immutable ZIP/hash, environment, exact task identity, Task Hook envelope, and approval | Stop before upload | Route through Core Data Loader | Import |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Membership | Require an exact member of the 17-type inventory in ora_reference_lookups.md | Read or mutation | resolve_duplicate_management_lookup |
| System restriction | For the 15 System types, reject create/delete and every change except current-describe-supported Meaning | Mutation | resolve_duplicate_management_lookup |
| Extensible restriction | For ZCH_MATCH_OBJ_ORGANIZATION and ZCH_MATCH_OBJ_PERSON, protect seeded or unknown-origin codes; allow only the documented custom-code fields and lifecycle | Mutation | resolve_duplicate_management_lookup |
| Current evidence | Require exact configuration level, code identity/origin, current values, links, and current code describe | Mutation | resolve_duplicate_management_lookup |
| Mutation envelope | Require immutable method, exact URL, redacted payload, expected effect, target environment, approval, and one-request limit | Mutation | resolve_duplicate_management_lookup |
| FSM archive | Require exactly task ZCH_MANAGE_CUSTOMER_HUB_LOOKUPS | Import |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DML.VALIDATE | step | 10 | validate_input | valid->DML.LOOKUP;invalid->DML.ERROR | none | stop | Before lookup resolution or setup-data routing. |

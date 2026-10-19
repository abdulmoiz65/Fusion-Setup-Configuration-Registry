# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Read | Environment and optional exact LookupType or meaning | Stop on ambiguity | Resolve one environment and exact task membership | Read | resolve_data_quality_lookup_type |
| Create or update | Environment, LookupType, LookupCode, and named values | Stop before preview | GET exact type/code and current describe | Mutation | resolve_data_quality_lookup_type |
| Import | Immutable ZIP, SHA-256, environment, exact metadata task identity, Task Hook envelope, and approval | Stop before upload | Preserve bytes and route through Core Data Loader | Import |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Membership | Require one of the closed 21 lookup types; never infer from prefix, module, or meaning | Read or mutation | resolve_data_quality_lookup_type |
| Identity and seed | Reject identity changes, `ORA_` custom codes, silent upsert, and destructive treatment of seeded or unknown-origin codes | Mutation | resolve_data_quality_lookup_type |
| Writable fields | Intersect configuration-level rules, `CreatedBy` seed evidence, and current REST describe | Mutation | resolve_data_quality_lookup_type |
| FSM archive | Require one safe readable unencrypted `ASM_SETUP_CSV_METADATA.xml` and exactly one task identity equal to `ZCQ_MANAGE_DATA_QUALITY_LOOKUPS` | Import |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DQL.VALIDATE | step | 10 | validate_input | valid->DQL.LOOKUP;invalid->DQL.ERROR | none | stop | Before lookup resolution, export, validation, or import routing. |

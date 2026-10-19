# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Read | Environment and optional exact LookupType or meaning | Stop on ambiguity | Resolve one environment and exact task membership | Read | resolve_customer_hub_common_lookup_type |
| Mutation | Environment, LookupType, LookupCode, and named values | Stop before preview | GET exact type/code and current describe | Create, update, or delete | resolve_customer_hub_common_lookup_type |
| Import | Immutable ZIP/hash, environment, exact metadata identity, Task Hook envelope, and approval | Stop before upload | Preserve bytes and route through Core Data Loader | Import |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Membership | Require one of the closed 6 lookup types; never infer membership | Read or mutation | resolve_customer_hub_common_lookup_type |
| Identity and seed | Reject identity changes, `ORA_` custom codes, silent upsert, and destructive treatment of seeded or unknown-origin codes | Mutation | resolve_customer_hub_common_lookup_type |
| Writable fields | Intersect configuration level, `CreatedBy` seed evidence, and current REST describe | Mutation | resolve_customer_hub_common_lookup_type |
| FSM archive | Require one safe `ASM_SETUP_CSV_METADATA.xml` with exactly task `ZCH_MANAGE_CUSTOMER_HUB_COMMON_LOOKUPS` | Import |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CHC.VALIDATE | step | 10 | validate_input | valid->CHC.LOOKUP;invalid->CHC.ERROR | none | stop | Before lookup resolution or setup-data routing. |

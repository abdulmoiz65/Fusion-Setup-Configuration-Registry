# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Read | Environment and optional exact LookupType or meaning | Stop only on ambiguous environment or type | Resolve one environment and require exact task membership | Read | resolve_customer_center_lookup |
| Create | Environment, LookupType, LookupCode, Meaning | Stop before preview | GET type and duplicate, then validate level, seed status, and describe | Create | resolve_customer_center_lookup |
| Update or delete | Environment, LookupType, LookupCode, named fields | Stop before preview | GET exact current code and retain only supported named changes | Mutation | resolve_customer_center_lookup |
| Import | Immutable ZIP, hash, environment, metadata member, exact task identity, Data Loader approval, Task Hook validation envelope, and Task Hook validation contract | Stop before preview | Preserve the ZIP, require task identity ZCM_MANAGE_CUSTOMER_CENTER_LOOKUPS, and obtain Data Loader's approval-bound `Task Hook validation envelope` | Import |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Task membership | Require one of the eight exact baseline types; never infer from ZCA or ZMM prefix, module, or meaning | Read or mutation | resolve_customer_center_lookup |
| LookupCode | Require stable uppercase code of 30 or fewer characters, no spaces, no ORA_ prefix, and no duplicate | Create | resolve_customer_center_lookup |
| Meaning and description | Require nonempty Meaning of 80 or fewer characters; Description at most 240 when describe permits | Create or update |  |
| Dates and EnabledFlag | Require supported REST format, end not before start, and Y or N only | Named fields supplied |  |
| Identity and upsert | Reject identity, category, module, security, configuration, or seed changes and reject upsert | Mutation | resolve_customer_center_lookup |
| FSM archive | Require one safe readable unencrypted member with exact basename ASM_SETUP_CSV_METADATA.xml | Import |  |
| FSM task identity | Parse metadata without rewriting the archive and require exactly one task identity equal to ZCM_MANAGE_CUSTOMER_CENTER_LOOKUPS | Import |  |
| Task-local route selection | Reject any endpoint, adapter, routing field, or retry policy selected by this task skill | Import |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CC.VALIDATE | step | 1 | validate_input | valid->CC.DEFAULT_SCOPE;invalid->CC.RETURN_ISSUES | none | stop | Before lookup resolution, validation, export, or import routing. |

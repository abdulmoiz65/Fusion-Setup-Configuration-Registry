# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Read | Environment and optional exact LookupType or meaning | Stop only on ambiguous environment or type | Resolve one environment and require task-membership evidence for a named type | Read | resolve_task_lookup_target |
| Create | Environment, LookupType, LookupCode, Meaning | Stop before preview | GET type and exact duplicate, then validate category, level, seed status, and describe | Create | resolve_task_lookup_target |
| Update or delete | Environment, LookupType, LookupCode, named fields | Stop before preview | GET exact current code and retain only supported named changes | Mutation | resolve_task_lookup_target |
| Import | Immutable ZIP, hash, environment, metadata member, exact task identity, Data Loader approval, Task Hook validation envelope, and Task Hook validation contract | Stop before preview | Preserve the ZIP, require task identity HZ_MANAGE_CONTACT_LOOKUPS, and obtain Data Loader's approval-bound `Task Hook validation envelope` | Import |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Task membership | Require authoritative attribution to HZ_MANAGE_CONTACT_LOOKUPS; never infer from prefix, module, or meaning | Read or mutation | resolve_task_lookup_target |
| LookupCode | Require a stable uppercase code of 30 or fewer characters, no spaces, no ORA_ prefix, and no duplicate | Create | resolve_task_lookup_target |
| Meaning and description | Require nonempty Meaning of 80 or fewer characters; Description at most 240 when describe permits | Create or update |  |
| Dates and EnabledFlag | Require supported REST format, end not before start, and Y or N only | Named fields supplied |  |
| Identity and upsert | Reject identity/category/module/seed changes and reject Upsert-Mode true | Mutation | resolve_task_lookup_target |
| FSM archive | Require one safe readable unencrypted member with exact basename ASM_SETUP_CSV_METADATA.xml | Import |  |
| FSM task identity | Parse metadata without rewriting the archive and require exactly one task identity equal to HZ_MANAGE_CONTACT_LOOKUPS | Import |  |
| Task-local route selection | Reject any endpoint, adapter, routing field, or retry policy selected by this task skill | Import |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CL.VALIDATE | step | 1 | validate_input | valid->CL.DEFAULT_SCOPE;invalid->CL.RETURN_ISSUES | none | stop | Before lookup resolution, validation, export, or import routing. |

# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Read | Environment and optional exact LookupType or meaning | Stop only on ambiguous environment or type | Resolve one environment and require task-membership evidence for a named type | Read | resolve_task_lookup_target |
| Update | Environment, LookupType, optional LookupCode, and named allowlisted fields | Stop before preview | GET the exact current type/code and retain only supported named changes | Mutation | resolve_task_lookup_target |
| Import | Immutable ZIP, hash, environment, metadata member, exact task identity, Data Loader approval, Task Hook validation envelope, and Task Hook validation contract | Stop before preview | Preserve the ZIP, require task identity HZ_MANAGE_PARTY_USAGE_LOOKUPS, and obtain Data Loader's approval-bound `Task Hook validation envelope` | Import |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Task membership | Require authoritative attribution to HZ_MANAGE_PARTY_USAGE_LOOKUPS; never infer from prefix, module, or meaning | Read or mutation | resolve_task_lookup_target |
| Create or delete | Reject because every confirmed task member is System | Mutation | resolve_task_lookup_target |
| System update intersection | Accept only Meaning and require current REST describe to mark it updatable | PATCH | resolve_task_lookup_target |
| Protected fields | Reject Description, DisplaySequence, EnabledFlag, StartDateActive, EndDateActive, Tag, ModuleId, RestAccessSecured, CustomizationLevel, category, seed, and identity changes | Mutation | resolve_task_lookup_target |
| Identity and upsert | Reject LookupType or LookupCode identity changes and reject Upsert-Mode true | Mutation | resolve_task_lookup_target |
| FSM archive | Require one safe readable unencrypted member with exact basename ASM_SETUP_CSV_METADATA.xml | Import |  |
| FSM task identity | Parse metadata without rewriting the archive and require exactly one task identity equal to HZ_MANAGE_PARTY_USAGE_LOOKUPS | Import |  |
| Task-local route selection | Reject any endpoint, adapter, routing field, or retry policy selected by this task skill | Import |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PU.VALIDATE | step | 1 | validate_input | valid->PU.DEFAULT_SCOPE;invalid->PU.RETURN_ISSUES | none | stop | Before lookup resolution, validation, export, or import routing. |

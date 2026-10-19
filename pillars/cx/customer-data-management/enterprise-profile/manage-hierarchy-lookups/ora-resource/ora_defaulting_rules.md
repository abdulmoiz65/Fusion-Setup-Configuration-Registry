# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Read scope | PARTY_HIERARCHY_TYPE and HZ_TREE_STATUS | User generally asks for hierarchy lookups | Yes | resolve_hierarchy_lookup_target |
| Read expansion | lookupCodes | Reading a lookup type | No | resolve_hierarchy_lookup_target |
| Mutation LookupType | No default | A mutation omits the exact lookup type | No; stop and ask |  |
| EnabledFlag | No default | Create omits enabled state | No; preserve the missing value for the executor to resolve from its supported contract |  |
| StartDateActive | No default | Create omits a date | No; do not invent a date |  |
| Import gate | core.data-loader source review plus a current Task Hook validation envelope and separate immutable-preview approval | Import is requested | No |  |
| Import execution route | Current Task Hook validation envelope bound to the exact archive SHA-256 | Exact-task FSM ZIP import is requested | No; stop with approval_blocker when absent |  |
| Import execution owner | `core.data-loader`, after a current Task Hook validation envelope and separate explicit approval | Exact-task FSM ZIP import is requested | No; stop with approval_blocker when unavailable |  |
| Task-local import route selection | Forbidden | Exact-task FSM ZIP import is requested | No |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HL.DEFAULT_SCOPE | step | 2 | apply_default | lookup_or_mutation->HL.LOOKUP_TARGET;import->HL.DEPENDENCY_READINESS;failure->HL.RETURN_ISSUES | HL.VALIDATE | stop | Apply only the documented general-read scope and exact task-level FSM import routing; never default a mutation identity, payload value, or generic-loader fallback. |

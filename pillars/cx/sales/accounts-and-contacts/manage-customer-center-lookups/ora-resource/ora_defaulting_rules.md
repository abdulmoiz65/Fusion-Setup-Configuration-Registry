# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| TaskCode | ZCM_MANAGE_CUSTOMER_CENTER_LOOKUPS | Export or import | Yes; exact task identity is mandatory |  |
| Read expansion | lookupCodes | Reading an exact confirmed Standard type | No | resolve_customer_center_lookup |
| Mutation identity or values | No default | Mutation omits required target or value | No; stop |  |
| Import gate | core.data-loader source review plus a current Task Hook validation envelope and separate immutable-preview approval | Import | No |  |
| Import execution route | Current Task Hook validation envelope bound to the exact archive SHA-256 | Exact-task FSM ZIP | No; stop with approval_blocker when absent |  |
| Import execution owner | core.data-loader after a current Task Hook validation envelope is verified | Exact-task FSM ZIP | No; fail approval_blocker when unavailable |  |
| Task-local import route selection | Forbidden | Exact-task FSM ZIP | No |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CC.DEFAULT_SCOPE | step | 2 | apply_default | lookup_or_mutation->CC.LOOKUP_TARGET;import->CC.DEPENDENCY_READINESS;failure->CC.RETURN_ISSUES | CC.VALIDATE | stop | Apply exact task identity and safe routing; never default lookup identity, values, or task-local import fallback. |

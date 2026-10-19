# Dependency Readiness

## Dependency Rules
| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| DCL.ENV | Fusion environment | Yes | Live operation | Satisfied | Exactly one environment |  | Prevent cross-environment work | Select target | Environment identity |
| DCL.CURRENT | Current task lookup | Yes | Read or update | Lookup | Exact GET and describe | resolve_data_cleansing_lookup | Prevent inferred payload | Supply exact type/code | Category, level, seed, fields |
| DCL.LOADER | Core Data Loader Task Hook | Yes | Import | Blocked until proven | Envelope bound to ZIP hash |  | Prevent bypass | Build immutable preview | Envelope and hash |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DCL.DEPENDENCIES | decision | 30 | resolve_dependency | satisfied->DCL.ENFORCE;blocked->DCL.ERROR | DCL.DEFAULTS | stop | Before update or import readiness. |

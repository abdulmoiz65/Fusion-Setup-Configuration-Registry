# Dependency Readiness

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| DML.ENV | Fusion environment | Yes | Live operation | Satisfied | Exactly one configured environment |  | Prevent cross-environment work | Select one target | Environment identity |
| DML.CURRENT | Current task lookup | Yes | Read or mutation | Lookup | Exact GET and code describe | resolve_duplicate_management_lookup | Prevent inferred scope or payload | Supply exact type/code | Category, level, seed, fields |
| DML.LOADER | Core Data Loader Task Hook | Yes | Import | Blocked until proven | Approval envelope bound to ZIP SHA-256 |  | Prevent route bypass | Build immutable preview | Envelope and hash |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DML.DEPENDENCIES | decision | 30 | resolve_dependency | satisfied->DML.ENFORCE;blocked->DML.ERROR | DML.DEFAULTS | stop | Before update or import readiness. |

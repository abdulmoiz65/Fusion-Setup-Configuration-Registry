# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Fusion environment | Resolve exactly one target. |
| 2 | Task membership and current state | Resolve exact type/code, Standard category, configuration level, and seed evidence. |
| 3 | Current describe | Prove the named method and fields are supported. |
| 4 | Shared owner | Use the shared REST client for manual operations or shared exporter, validators, and Core Data Loader for setup data. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| DQL.ENV | Fusion environment | Yes | Live operation | Satisfied | Exactly one configured environment |  | Prevent cross-environment work | Select one target | Environment identity |
| DQL.CURRENT | Current task lookup | Yes | Read or mutation | Lookup | Exact-task inventory plus exact GET | resolve_data_quality_lookup_type | Prevent inferred scope | Supply an exact type/code | Category, level, seed, fields |
| DQL.LOADER | Core Data Loader Task Hook | Yes | Import | Blocked until proven | Approval-bound envelope for exact ZIP SHA-256 |  | Prevent route bypass | Rebuild immutable preview when stale | Envelope and archive hash |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DQL.DEPENDENCIES | decision | 30 | resolve_dependency | satisfied->DQL.ENFORCE;blocked->DQL.ERROR | DQL.DEFAULTS | stop | Before mutation or import readiness. |

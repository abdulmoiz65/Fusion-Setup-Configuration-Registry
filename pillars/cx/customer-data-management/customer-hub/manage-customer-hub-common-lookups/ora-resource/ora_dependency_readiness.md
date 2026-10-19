# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Fusion environment | Resolve exactly one target. |
| 2 | Current lookup contract | Resolve membership, Standard category, configuration level, seed evidence, and describe. |
| 3 | Owning executor | Use the shared REST client, exporter/validators, or Core Data Loader as applicable. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CHC.ENV | Fusion environment | Yes | Live operation | Satisfied | Exactly one configured environment |  | Prevent cross-environment work | Select one target | Environment identity |
| CHC.CURRENT | Current task lookup | Yes | Read or mutation | Lookup | Task inventory plus exact GET | resolve_customer_hub_common_lookup_type | Prevent inferred scope | Supply exact type/code | Category, level, seed, fields |
| CHC.LOADER | Core Data Loader Task Hook | Yes | Import | Blocked until proven | Envelope bound to exact ZIP SHA-256 |  | Prevent route bypass | Rebuild immutable preview if stale | Envelope and hash |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CHC.DEPENDENCIES | decision | 30 | resolve_dependency | satisfied->CHC.ENFORCE;blocked->CHC.ERROR | CHC.DEFAULTS | stop | Before mutation or import readiness. |

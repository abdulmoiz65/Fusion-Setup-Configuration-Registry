# Dependency Readiness

## Dependency Rules
| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| NT.ENV | Fusion environment | Yes | Live operation | Satisfied | Exactly one environment |  | Prevent cross-environment work | Select target | Environment identity |
| NT.CURRENT | ZMM_NOTE_TYPE current state | Yes | REST operation | Lookup | Exact GET and describe | resolve_customer_data_hub_note_type | Protect scope and seeded data | Supply exact operation/code | Level, seed, fields |
| NT.LOADER | Core Data Loader Task Hook | Yes | Import | Blocked until proven | Envelope bound to ZIP hash |  | Prevent bypass | Build immutable preview | Envelope and hash |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NT.DEPENDENCIES | decision | 30 | resolve_dependency | satisfied->NT.ENFORCE;blocked->NT.ERROR | NT.DEFAULTS | stop | Before mutation or import readiness. |

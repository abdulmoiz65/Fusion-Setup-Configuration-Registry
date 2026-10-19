# Dependency Readiness

## Dependency Rules
| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| NTM.ENV | Fusion environment | Yes | Live read | Satisfied | Exactly one environment |  | Prevent cross-environment results | Select target | Environment identity |
| NTM.CURRENT | noteTypes read contract | Yes | Live read | Lookup | Current GET and describe | resolve_note_type_mapping | Enforce GET-only boundary and supported mapping scope | Omit SourceObjectCode to list NOTE mappings, or provide exactly one of NOTE, ZCH_DUP_IDNT_BATCH, or ZCH_DUP_RES_REQUEST; provide an exact MappedLookupCode only when needed | Effective mappings |
| NTM.LOADER | Core Data Loader Task Hook | Yes | Import | Blocked until proven | Envelope bound to ZIP hash |  | Prevent bypass | Build immutable preview | Envelope and hash |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NTM.DEPENDENCIES | decision | 30 | resolve_dependency | satisfied->NTM.ENFORCE;blocked->NTM.ERROR | NTM.DEFAULTS | stop | Before read or import readiness. |

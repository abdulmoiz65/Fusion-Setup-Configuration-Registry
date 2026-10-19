# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Fusion target | Resolve exactly one configured environment. |
| 2 | Task membership and current state | Confirm HZ_MANAGE_IMPORT_LOOKUPS, exact lookup category/type/code, configuration level, and seeded evidence. |
| 3 | Describe contract | Prove the named fields and method are currently supported. |
| 4 | Shared executor | Use Apps Common/REST client for permitted manual work or shared exporter/validators/core.data-loader for setup data. |
| 5 | Core Data Loader Task Hook handoff | After the final immutable archive is prepared and before upload, require Core Data Loader Task Hook validation and an envelope bound to that exact archive SHA-256. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| IL.ENV | Fusion environment | Yes | Live read or side effect | Satisfied | Exactly one configured environment |  | Prevent cross-environment execution | Select one target | Environment identity |
| IL.CURRENT | Current task-scoped lookup | Yes | Read or mutation | Lookup | Authoritative task attribution plus exact GET | resolve_task_lookup_target | Prevent inferred scope and silent upsert | Supply exact type/code or unambiguous confirmed request | Category, level, code, seed state, fields |
| IL.DESCRIBE | Current writable contract | Yes | Mutation | Blocked until proven | Current describe metadata |  | Prevent unsupported payloads | Refresh describe and restrict to named writable fields | Method, endpoint, fields, types, nullability |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IL.DEPENDENCY_READINESS | decision | 4 | resolve_dependency | satisfied->IL.DESIGN_GATE;blocked->IL.RETURN_ISSUES | IL.DEFAULT_SCOPE | stop | Before a mutation preview or exact-task FSM import preview. |

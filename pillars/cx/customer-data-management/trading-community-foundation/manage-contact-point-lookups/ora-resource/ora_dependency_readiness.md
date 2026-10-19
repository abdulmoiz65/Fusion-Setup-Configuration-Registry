# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Fusion target | Resolve exactly one configured environment. |
| 2 | Task membership and current state | Confirm HZ_MANAGE_CONTACT_POINT_LOOKUPS, exact lookup category/type/code, configuration level, and seeded evidence. |
| 3 | Describe contract | Prove the named fields and method are currently supported. |
| 4 | Shared executor | Use Apps Common/REST client for permitted manual work or shared exporter/validators/core.data-loader for setup data. |
| 5 | Core Data Loader Task Hook handoff | After the final immutable archive is prepared and before upload, require Core Data Loader Task Hook validation and an envelope bound to that exact archive SHA-256. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CP.ENV | Fusion environment | Yes | Live read or side effect | Satisfied | Exactly one configured environment |  | Prevent cross-environment execution | Select one target | Environment identity |
| CP.CURRENT | Current task-scoped lookup | Yes | Read or mutation | Lookup | Authoritative task attribution plus exact GET | resolve_task_lookup_target | Prevent inferred scope and silent upsert | Supply exact type/code or unambiguous confirmed request | Category, level, code, seed state, fields |
| CP.DESCRIBE | Current writable contract | Yes | Mutation | Blocked until proven | Current Standard lookup describe plus configuration and seed rules |  | Prevent unsupported or overbroad payloads | Refresh describe and intersect it with exact level and seeded-origin restrictions | Method, endpoint, permitted fields, types, nullability |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CP.DEPENDENCY_READINESS | decision | 4 | resolve_dependency | satisfied->CP.DESIGN_GATE;blocked->CP.RETURN_ISSUES | CP.DEFAULT_SCOPE | stop | Before a mutation preview or exact-task FSM import preview. |

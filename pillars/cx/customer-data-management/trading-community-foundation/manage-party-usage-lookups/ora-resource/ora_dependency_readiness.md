# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Fusion target | Resolve exactly one configured environment. |
| 2 | Task membership and current state | Confirm HZ_MANAGE_PARTY_USAGE_LOOKUPS, exact lookup category/type/code, configuration level, and seeded evidence. |
| 3 | Describe contract | Prove the named fields and method are currently supported. |
| 4 | Shared executor | Use Apps Common/REST client for permitted manual work or shared exporter/validators/core.data-loader for setup data. |
| 5 | Core Data Loader Task Hook handoff | After the final immutable archive is prepared and before upload, require Core Data Loader Task Hook validation and an envelope bound to that exact archive SHA-256. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PU.ENV | Fusion environment | Yes | Live read or side effect | Satisfied | Exactly one configured environment |  | Prevent cross-environment execution | Select one target | Environment identity |
| PU.CURRENT | Current task-scoped lookup | Yes | Read or mutation | Lookup | Authoritative task attribution plus exact GET | resolve_task_lookup_target | Prevent inferred scope and silent upsert | Supply exact type/code or unambiguous confirmed request | Category, level, code, seed state, fields |
| PU.DESCRIBE | Current writable contract | Yes | Mutation | Blocked until proven | Current Standard lookup describe plus System configuration rules |  | Prevent generic REST exposure from bypassing System restrictions | Refresh describe and require Meaning as the sole permitted field | Method, endpoint, Meaning type and nullability |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PU.DEPENDENCY_READINESS | decision | 4 | resolve_dependency | satisfied->PU.DESIGN_GATE;blocked->PU.RETURN_ISSUES | PU.DEFAULT_SCOPE | stop | Before a mutation preview or exact-task FSM import preview. |

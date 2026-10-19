# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Fusion target | Resolve exactly one configured environment. |
| 2 | Task membership and current state | Confirm ZCM_MANAGE_CUSTOMER_CENTER_LOOKUPS, exact Standard type/code, level, and seeded evidence. |
| 3 | Describe contract | Prove the named fields and method are currently supported. |
| 4 | Shared executor | Use Apps Common/REST client for manual work or shared exporter, validators, and core.data-loader for setup data. |
| 5 | Core Data Loader Task Hook handoff | After the final immutable archive is prepared and before upload, require Core Data Loader Task Hook validation and an envelope bound to that exact archive SHA-256. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CC.ENV | Fusion environment | Yes | Live read or side effect | Satisfied | Exactly one configured environment |  | Prevent cross-environment execution | Select one target | Environment identity |
| CC.CURRENT | Current task-scoped lookup | Yes | Read or mutation | Lookup | Supplied task inventory plus exact GET | resolve_customer_center_lookup | Prevent inferred scope and silent upsert | Supply exact type/code or unambiguous request | Category, level, code, seed state, fields |
| CC.DESCRIBE | Current writable contract | Yes | Mutation | Blocked until proven | Current describe metadata |  | Prevent unsupported payloads | Refresh describe and restrict to named fields | Method, endpoint, fields, types, nullability |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CC.DEPENDENCY_READINESS | decision | 4 | resolve_dependency | satisfied->CC.DESIGN_GATE;blocked->CC.RETURN_ISSUES | CC.DEFAULT_SCOPE | stop | Before a mutation preview or exact-task FSM import preview. |

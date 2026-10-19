# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Fusion target | Resolve exactly one configured environment. |
| 2 | Current lookup state | Resolve the exact task-scoped lookup type and code when applicable. |
| 3 | Existing hierarchy type | For PARTY_HIERARCHY_TYPE creation, require authoritative evidence that Manage Tree Structures already created the proposed hierarchy type. |
| 4 | Executor metadata | Before a mutation, the authorized executor must use current writable-field metadata and an immutable preview. |
| 5 | Core Data Loader Task Hook handoff | After the final immutable archive is prepared and before upload, require a current Task Hook validation envelope bound to that exact archive SHA-256. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| HL.ENV | Fusion environment | Yes | Every live operation | Satisfied | Exactly one configured environment |  | Prevent cross-environment reads and writes | Configure or select one target environment | Environment identity |
| HL.CURRENT | Current lookup state | Yes | Every read or mutation | Lookup | Standard Lookups REST | resolve_hierarchy_lookup_target | Protect System and seeded values and prevent silent upsert | Supply an exact type or unambiguous task-scoped request | Configuration level and current code state |
| HL.HIERARCHY | Existing hierarchy type | Yes | Create PARTY_HIERARCHY_TYPE code | Blocked until supplied | Oracle-documented Manage Tree Structures completion evidence supplied by the caller |  | Oracle requires creating the hierarchy type first and then adding it to Party Hierarchy Type | Supply evidence that identifies exactly one completed hierarchy type; no undocumented endpoint may be inferred | Verified hierarchy type identity, evidence source, and exact proposed lookup code |
| HL.EXECUTOR | Supported write or import executor | Yes | Mutation or import | Blocked until proven | Task SKILL.md route and Task Hook validation envelope |  | Prevent task-local writes or import-route selection | Use the shared lookup transport for a supported mutation; for an FSM ZIP require Core Data Loader, its current Task Hook envelope, exact archive SHA-256 binding, and separate approval | Executor, immutable artifact hash, Task Hook envelope, approval fingerprint, and Core Data Loader evidence |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The dependency is verified | Yes |
| Lookup | A documented read-only resolver must run | Lookup only until it returns exactly one match |
| Blocked | Required authority, evidence, metadata, or approval is missing | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HL.DEPENDENCY_READINESS | decision | 4 | resolve_dependency | satisfied->HL.DESIGN_GATE;blocked->HL.RETURN_ISSUES | HL.DEFAULT_SCOPE | stop | Before previewing creation of a PARTY_HIERARCHY_TYPE custom code or importing a task-scoped FSM archive. |

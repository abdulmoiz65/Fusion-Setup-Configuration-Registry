# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Scope | Confirm the request is lookup maintenance, not hierarchy definition, version, node, or data maintenance. |
| 2 | Current state | Resolve the exact lookup type and code. |
| 3 | Permission | Enforce configuration level and seeded-code protection. |
| 4 | Dependency | For create, require authoritative hierarchy-type verification. |
| 5 | Execution boundary | Permit only a supported executor with an immutable preview and explicit mutation approval. |
| 6 | Core Data Loader boundary | For an exact-task FSM ZIP, require a current Task Hook validation envelope bound to the exact archive SHA-256 before Core Data Loader upload or initiation; prohibit task-local route selection. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| New PARTY_HIERARCHY_TYPE code | Error |  | Authoritative evidence does not identify exactly one existing hierarchy type | Define or verify it in its owning setup before adding the lookup code | Yes |
| Any named lookup-code mutation | Error | resolve_hierarchy_lookup_target | System configuration, seeded identity, unsupported field, reserved prefix, or ambiguous target | Select an eligible custom code and only currently supported fields | Yes |
| Hierarchy definition, version, node, or data change | Error |  | Request is outside lookup scope | Route to the owning hierarchy-management task | Yes |
| HZ_TREE_STATUS create, enable, disable, date, tag, or delete | Error | resolve_hierarchy_lookup_target | Any prohibited state change is requested | Keep seeded ACTIVE and INACTIVE status codes unchanged | No |
| HZ_TREE_STATUS meaning or translation change | Error | resolve_hierarchy_lookup_target | Exact current rules and metadata do not permit the named wording field | Restrict the request to an explicitly supported wording change | Yes |
| PARTY_HIERARCHY_TYPE tag or module update | Error | resolve_hierarchy_lookup_target | Extensible configuration doesn't permit the requested field | Restrict the request to a permitted custom-code field | No |
| Create request enables upsert | Error | resolve_hierarchy_lookup_target | Upsert-Mode is true or the executor can't prove create-only behavior | Use create-only behavior and stop on an existing exact code | Yes |
| FSM ZIP metadata task mismatch | Error |  | Metadata is missing, ambiguous, or not exactly `HZ_MANAGE_HIERARCHY_LOOKUPS` | Use an immutable export for the exact setup task | Yes |
| Task-local import route selection | Error |  | This task skill selects an endpoint, adapter, routing field, or retry behavior | Stop with approval_blocker and restart through Core Data Loader | No |
| Missing or stale Task Hook validation | Error |  | The envelope or exact archive SHA-256 binding is missing, stale, changed, or reconstructed locally | Stop with approval_blocker and rebuild the immutable Data Loader preview | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_hierarchy_lookup_target | Every read or named mutation | Exact type, configuration level, code state, and seeded evidence | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HL.DESIGN_GATE | decision | 5 | design_enforcement | pass->HL.EXECUTION_GATE;fail->HL.RETURN_ISSUES | HL.DEFAULT_SCOPE | stop | After lookup and applicable dependency or adapter resolution, before reporting read readiness or previewing a mutation or import. |

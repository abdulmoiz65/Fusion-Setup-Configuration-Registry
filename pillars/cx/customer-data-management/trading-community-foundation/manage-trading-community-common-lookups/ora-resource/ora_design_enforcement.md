# Design Enforcement

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any task lookup request | Error | resolve_task_lookup_target | Exact membership in HZ_MANAGE_TRADING_COMMUNITY_COMMON_LOOKUPS is not authoritative | Supply official task attribution or current exact-task metadata; never infer | Yes |
| Any lookup update | Error | resolve_task_lookup_target | Named field is absent from current REST describe or disallowed by configuration level or seeded origin | Intersect the exact level, seed rules, and current describe | Yes |
| Seeded-code destructive change | Error | resolve_task_lookup_target | Delete, identity change, or custom-code treatment targets a code whose CreatedBy is SEED_DATA_FROM_APPLICATION or whose origin is unknown | Select a proven custom code or a non-destructive field permitted at that level | Yes |
| Seed classification | Error | resolve_task_lookup_target | LastUpdatedBy is used to classify a code as custom | Use CreatedBy for seeded origin; LastUpdatedBy is audit only | Yes |
| Custom code create | Error | resolve_task_lookup_target | Code starts ORA_, already exists, or upsert is enabled | Use a nonreserved unique code and create-only behavior | Yes |
| Any mutation | Error | resolve_task_lookup_target | Category, identity, level, seed state, named field, describe, preview, or approval is missing | Complete exact preflight and regenerate preview | Yes |
| FSM ZIP metadata | Error |  | Missing, unsafe, duplicate, unreadable, encrypted, ambiguous, or not exactly HZ_MANAGE_TRADING_COMMUNITY_COMMON_LOOKUPS | Use an unchanged exact-task export | Yes |
| Task Hook authorization | Error |  | `Task Hook validation envelope` or exact archive SHA-256 binding is missing, stale, changed, or reconstructed locally | Stop with approval_blocker and rebuild the Data Loader immutable preview | Yes |
| FSM Task Hook validation contract | Error |  | The envelope is missing, stale, bound to different bytes, or a task-local route was selected | Stop with approval_blocker; rerun Core Data Loader validation and do not substitute a route | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_task_lookup_target | Read or manual mutation | Exact task membership, category, type/code, level, seed state, links, and describe fields | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCC.DESIGN_GATE | decision | 5 | design_enforcement | pass->TCC.EXECUTION_GATE;fail->TCC.RETURN_ISSUES | TCC.DEFAULT_SCOPE | stop | Before returning read readiness or previewing a mutation, export, or import. |

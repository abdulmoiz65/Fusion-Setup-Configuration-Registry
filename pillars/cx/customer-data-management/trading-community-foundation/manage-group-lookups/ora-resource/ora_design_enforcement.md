# Design Enforcement

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any task lookup request | Error | resolve_task_lookup_target | Exact membership in HZ_MANAGE_GROUP_LOOKUPS is not authoritative | Supply official task attribution or current exact-task metadata; never infer | Yes |
| Configuration-level mutation | Error | resolve_task_lookup_target | Request exceeds HZ_HOUSEHOLD_DFLT_NAMES Extensible or the seven User member rules | Restrict the request to the member's current level and describe contract | Yes |
| System lookup mutation | Error | resolve_task_lookup_target | Request exceeds an exact wording field permitted by current rules and describe | Keep System code protected | No |
| Extensible seeded code | Error | resolve_task_lookup_target | CreatedBy is SEED_DATA_FROM_APPLICATION or seeded origin cannot be disproved | Select a proven custom code | Yes |
| Custom code create | Error | resolve_task_lookup_target | Code starts ORA_, already exists, or upsert is enabled | Use a nonreserved unique code and create-only behavior | Yes |
| Any mutation | Error | resolve_task_lookup_target | Category, identity, level, seed state, named field, describe, preview, or approval is missing | Complete exact preflight and regenerate preview | Yes |
| FSM ZIP metadata | Error |  | Missing, unsafe, duplicate, unreadable, encrypted, ambiguous, or not exactly HZ_MANAGE_GROUP_LOOKUPS | Use an unchanged exact-task export | Yes |
| Task Hook authorization | Error |  | `Task Hook validation envelope` or exact archive SHA-256 binding is missing, stale, changed, or reconstructed locally | Stop with approval_blocker and rebuild the Data Loader immutable preview | Yes |
| FSM Task Hook validation contract | Error |  | The envelope is missing, stale, bound to different bytes, or a task-local route was selected | Stop with approval_blocker; rerun Core Data Loader validation and do not substitute a route | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_task_lookup_target | Read or manual mutation | Exact task membership, category, type/code, level, seed state, links, and describe fields | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GL.DESIGN_GATE | decision | 5 | design_enforcement | pass->GL.EXECUTION_GATE;fail->GL.RETURN_ISSUES | GL.DEFAULT_SCOPE | stop | Before returning read readiness or previewing a mutation, export, or import. |

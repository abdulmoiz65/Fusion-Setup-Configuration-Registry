# Design Enforcement

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any task lookup request | Error | resolve_customer_center_lookup | Exact membership in ZCM_MANAGE_CUSTOMER_CENTER_LOOKUPS is not authoritative | Use one of the eight confirmed types; never infer | Yes |
| Configuration-level mutation | Error | resolve_customer_center_lookup | Request exceeds the seven User rules or ZMM_NOTE_TYPE Extensible rules | Restrict to current level and describe contract | Yes |
| Extensible seeded code | Error | resolve_customer_center_lookup | CreatedBy is SEED_DATA_FROM_APPLICATION or custom origin cannot be proven | Select a proven custom code | Yes |
| Custom code create | Error | resolve_customer_center_lookup | Code starts ORA_, already exists, or upsert is enabled | Use a nonreserved unique code and create-only behavior | Yes |
| Any mutation | Error | resolve_customer_center_lookup | Category, identity, level, seed state, field, describe, preview, or approval is missing | Complete exact preflight and regenerate preview | Yes |
| FSM ZIP metadata | Error |  | Missing, unsafe, duplicate, unreadable, encrypted, ambiguous, or not exactly ZCM_MANAGE_CUSTOMER_CENTER_LOOKUPS | Use an unchanged exact-task export | Yes |
| Task Hook authorization | Error |  | `Task Hook validation envelope` or exact archive SHA-256 binding is missing, stale, changed, or reconstructed locally | Stop with approval_blocker and rebuild the Data Loader immutable preview | Yes |
| FSM Task Hook validation contract | Error |  | The envelope is missing, stale, bound to different bytes, or a task-local route was selected | Stop with approval_blocker; rerun Core Data Loader validation and do not substitute a route | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_customer_center_lookup | Read or manual mutation | Exact membership, Standard category, type/code, level, seed state, links, and describe fields | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CC.DESIGN_GATE | decision | 5 | design_enforcement | pass->CC.EXECUTION_GATE;fail->CC.RETURN_ISSUES | CC.DEFAULT_SCOPE | stop | Before returning read readiness or previewing a mutation, export, or import. |

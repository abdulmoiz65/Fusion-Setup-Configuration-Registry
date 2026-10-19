# Design Enforcement

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any request | Error | resolve_customer_hub_common_lookup_type | Exact membership or Standard category is not proven | Reconcile authority; never infer | Yes |
| Mutation | Error | resolve_customer_hub_common_lookup_type | Level, seed state, describe, preview, or approval is missing | Complete exact preflight | Yes |
| Create | Error | resolve_customer_hub_common_lookup_type | Code starts `ORA_`, exists, or upsert is enabled | Use unique nonreserved create-only code | Yes |
| Seeded code | Error | resolve_customer_hub_common_lookup_type | Destructive or identity change targets seeded/unknown origin | Select proven custom code or permitted wording field | Yes |
| FSM ZIP | Error |  | Metadata/hash/envelope is unsafe, changed, ambiguous, or wrong task | Rebuild immutable Core Data Loader preview | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_customer_hub_common_lookup_type | Read or mutation | Membership, category, type/code, level, seed, values, describe | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CHC.ENFORCE | decision | 40 | design_enforcement | pass->CHC.READY;fail->CHC.ERROR | CHC.DEPENDENCIES | stop | Before read readiness or mutation/export/import preview. |

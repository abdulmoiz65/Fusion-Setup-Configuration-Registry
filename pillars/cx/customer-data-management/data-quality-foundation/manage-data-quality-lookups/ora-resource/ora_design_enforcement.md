# Design Enforcement

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any request | Error | resolve_data_quality_lookup_type | Exact task membership or Standard category is not proven | Reconcile authoritative task evidence; never infer | Yes |
| Mutation | Error | resolve_data_quality_lookup_type | Configuration level, seed state, current describe, preview, or approval is missing | Complete exact preflight and regenerate preview | Yes |
| Create | Error | resolve_data_quality_lookup_type | Code starts `ORA_`, already exists, or upsert is enabled | Use a unique nonreserved custom code | Yes |
| Seeded code | Error | resolve_data_quality_lookup_type | Delete, identity change, or custom treatment targets seeded or unknown origin | Select a proven custom code or allowed non-destructive field | Yes |
| FSM ZIP | Error |  | Metadata is unsafe, ambiguous, changed, or not exactly `ZCQ_MANAGE_DATA_QUALITY_LOOKUPS`; Task Hook/hash binding is absent | Rebuild the immutable Core Data Loader preview | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_data_quality_lookup_type | Read or mutation | Exact membership, category, type/code, level, seed state, current values, and describe fields | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DQL.ENFORCE | decision | 40 | design_enforcement | pass->DQL.READY;fail->DQL.ERROR | DQL.DEPENDENCIES | stop | Before read readiness or mutation, export, or import preview. |

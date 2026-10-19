# Manage Worker Unions Design Enforcement

## Purpose

Defines the final blocking gates before routing.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm identity | Resolve one target or confirm create availability |
| 2 | Confirm EFF completion | Resolve every requested context, segment, value, and information code |
| 3 | Confirm mutation shape | Require the Organization, Worker Union classification, and requested OrgInformation rows |
| 4 | Decide readiness | Continue only when no blocker remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| IDENTITY | Every request | Blocking | find_manage_worker_unions | Identity is absent, ambiguous, or duplicated | Supply one exact unique identity | Input fix |
| CLASSIFICATION | A mutation is requested | Blocking | resolve_worker_union_components | The Organization or `ORA_PER_UNION` classification row is unsupported or incomplete | Correct the component mapping | Input fix |
| EFF_PARENT | OrgInformation is supplied | Blocking | resolve_worker_union_classification | One effective `ORA_PER_UNION` classification parent is not resolved | Resolve the classification parent | Lookup fix |
| EFF_SHAPE | OrgInformation is supplied | Blocking | resolve_worker_union_eff_context | A requested context, segment, discriminator, or multirow key is incomplete | Complete every requested EFF row | Lookup fix |
| EFF_VALUE | A supplied EFF segment with no task-specific resolver declares a value set | Blocking | resolve_worker_union_eff_segment_value | Its typed stored value is unresolved or mapped to the wrong target | Resolve one compatible stored value | Lookup fix |
| BARGAINING_UNIT | Associated Bargaining Units is supplied | Blocking | resolve_worker_union_bargaining_unit | Its typed stored value is unresolved or mapped to the wrong target | Resolve or create and re-resolve one compatible value | Lookup fix |
| INFORMATION_CODE | An Additional Information code is supplied | Blocking | validate_worker_union_information_code | Its uniqueness is not proven | Validate the supplied code | Lookup fix |
| DATE_EFFECTIVE_SPLIT_DELETE | delete-effective-split is requested | Blocking | resolve_worker_union_delete_history | Source uses HDL DELETE, omits `SET PURGE_FUTURE_CHANGES Y` or an operation-required classification association, would remove the logical first split, or does not exactly bound future splits to remove | Use an Organization MERGE row with the confirmed retained EffectiveStartDate and inclusive EffectiveEndDate, plus at least one OrgUnitClassification association; omit OrgInformation and non-key attributes | Source rebuild |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_manage_worker_unions | Every request | Exact identity, availability, and current values | ora_reference_lookups.md |
| resolve_worker_union_components | A mutation is requested | Organization and Worker Union classification mappings | ora_reference_lookups.md |
| resolve_worker_union_classification | OrgInformation is supplied | Worker Union classification identity and category | ora_reference_lookups.md |
| resolve_worker_union_eff_context | OrgInformation is supplied | Context, segment, type, target, cardinality, and multirow contract | ora_reference_lookups.md |
| resolve_worker_union_eff_segment_value | A value-set-backed EFF segment has no task-specific resolver | Typed stored value for the declared target | ora_reference_lookups.md |
| resolve_worker_union_bargaining_unit | Associated Bargaining Units is supplied | Typed stored bargaining-unit value | ora_reference_lookups.md |
| validate_worker_union_information_code | An Additional Information code is supplied | Uniqueness evidence | ora_reference_lookups.md |
| resolve_worker_union_delete_history | delete-effective-split | Confirmed retained start, inclusive deletion end, and preserved predecessor values | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocker is satisfied | Continue to routing |
| not_required | No design rule applies | Continue unchanged |
| blocked | A blocker remains | Stop and correct it |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UNION.DESIGN | decision | 8 | design_enforcement | passed->UNION.ROUTE;not_required->UNION.ROUTE;blocked->UNION.ERROR | UNION.DEFAULTS | stop | After validation, dependency resolution, and defaulting |

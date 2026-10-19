# Manage Divisions Design Enforcement

## Purpose

Defines the blocking design gates for Manage Divisions.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm identity | Resolve one target or confirm create availability |
| 2 | Validate EFF value | Resolve each supplied value through its declared segment contract |
| 3 | Validate mutation structure | Require Organization, classification, and applicable EFF shape |
| 4 | Decide readiness | Continue only when no blocker remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| IDENTITY | Every request | Blocking | find_manage_divisions | Identity is absent, ambiguous, or duplicated | Supply one exact unique identity | Input fix |
| CLASSIFICATION | Create, edit, or inactivate | Blocking |  | ClassificationCode is not `HCM_DIVISION` | Correct the classification row | Input fix |
| MODIFIED_OBJECTS_ONLY | Create, edit, or inactivate | Blocking |  | XLSX or DAT contains OrgInformation when the user did not explicitly request an Organization Information/EFF change | Remove the OrgInformation worksheet and its Data Loader Map row; retain only Organization and OrgUnitClassification | Source rebuild |
| EFF_SHAPE | An OrgInformation row is supplied | Blocking | resolve_division_eff_context | Its category, context discriminator, context value, or multirow unique key is incomplete | Correct the EFF row | Input fix |
| EFF_VALUE | A supplied EFF segment declares a value set | Blocking | resolve_division_eff_segment_value | Its stored value is missing, ambiguous, type-incompatible, or mapped to the wrong target attribute | Resolve one compatible stored value | Lookup fix |
| DATE_EFFECTIVE_SPLIT_DELETE | delete-effective-split is requested | Blocking | resolve_division_delete_history | Source uses HDL DELETE, omits `SET PURGE_FUTURE_CHANGES Y` or an operation-required classification association, would remove the logical first split, or does not exactly bound future splits to remove | Use an Organization MERGE row with the confirmed retained EffectiveStartDate and inclusive EffectiveEndDate, plus at least one operation-required `OrgUnitClassification` association; omit OrgInformation and non-key attributes | Source rebuild |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_manage_divisions | Every request | Exact identity, availability, and current values | ora_reference_lookups.md |
| resolve_division_delete_history | delete-effective-split | Confirmed retained start, inclusive deletion end, and preserved predecessor values | ora_reference_lookups.md |
| resolve_division_eff_context | A Division EFF context or segment is requested or supplied | Context, segment, target attribute, type, cardinality, and value-set contract | ora_reference_lookups.md |
| resolve_division_eff_segment_value | A supplied EFF segment declares a value set | One typed stored value for the declared target attribute | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every blocker is satisfied | Continue to routing |
| not_required | No rule applies | Continue unchanged |
| blocked | A blocker remains | Stop and correct it |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DIV.DESIGN | decision | 8 | design_enforcement | passed->DIV.ROUTE;not_required->DIV.ROUTE;blocked->DIV.ERROR | DIV.DEFAULTS | stop | After validation, dependencies, and defaulting |

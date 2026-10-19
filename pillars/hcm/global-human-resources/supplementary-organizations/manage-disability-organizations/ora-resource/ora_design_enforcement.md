# Manage Disability Organizations Design Enforcement

## Purpose

Defines the blocking design gates for Manage Disability Organizations.

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
| IDENTITY | Every request | Blocking | find_manage_disability_organizations | Identity is absent, ambiguous, or duplicated | Supply one exact unique identity | Input fix |
| CLASSIFICATION | Create, edit, or inactivate | Blocking |  | ClassificationCode is not `HCM_DISABILITY_ORGANIZATION` | Correct the classification row | Input fix |
| EFF_SHAPE | An OrgInformation row is supplied | Blocking | resolve_disability_organization_eff_context | Its category, context discriminator, context value, or multirow unique key is incomplete | Correct the EFF row | Input fix |
| EFF_VALUE | A supplied EFF segment declares a value set | Blocking | resolve_disability_organization_eff_segment_value | Its stored value is missing, ambiguous, type-incompatible, or mapped to the wrong target attribute | Resolve one compatible stored value | Lookup fix |
| DATE_EFFECTIVE_SPLIT_DELETE | Date-effective delete | Blocking | resolve_disability_organization_delete_history | Source uses HDL `DELETE`, omits `SET PURGE_FUTURE_CHANGES Y` or the retained-predecessor classification association, would remove the first row, or does not exactly bound future splits | Use reviewed retained-predecessor `Organization` and `OrgUnitClassification` `MERGE` rows with the confirmed final deletion end | Source rebuild |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_manage_disability_organizations | Every request | Exact identity, availability, and current values | ora_reference_lookups.md |
| resolve_disability_organization_delete_history | Date-effective delete | Complete history, one current row, effective range, and internal eligibility | ora_reference_lookups.md |
| resolve_disability_organization_eff_context | A Disability Organization EFF context or segment is requested or supplied | Context, segment, target attribute, type, cardinality, and value-set contract | ora_reference_lookups.md |
| resolve_disability_organization_eff_segment_value | A supplied Disability Organization EFF segment declares a value set | One typed stored value for the declared target attribute | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every blocker is satisfied | Continue to routing |
| not_required | No rule applies | Continue unchanged |
| blocked | A blocker remains | Stop and correct it |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DISORG.DESIGN | decision | 8 | design_enforcement | passed->DISORG.ROUTE;not_required->DISORG.ROUTE;blocked->DISORG.ERROR | DISORG.DEFAULTS | stop | After validation, dependencies, and defaulting |

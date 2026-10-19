# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Retrieve existing class units | Run find_units_of_measure_by_class using the supplied UOMClass. |
| 2 | Evaluate base-unit and conversion design | Only when the class exists, confirm the base UOM is the smallest unit and each non-base UOM has an effective standard or intraclass conversion to the base UOM of at least 1. |
| 3 | Resolve a blocker | Correct the proposed setup, or obtain explicit user approval to bypass the blocker. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Operation is Create or Update and the supplied UOMClass has existing units | Blocker | find_units_of_measure_by_class | The base UOM is not the smallest unit, or a non-base UOM has no effective standard or intraclass conversion to the base UOM that is at least 1 | Choose the smallest unit as the base UOM and express every non-base UOM as at least 1 base unit to avoid fractional conversion results and decimal dust in partial-quantity transactions | Yes, or bypass only with explicit user approval |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_units_of_measure_by_class | The supplied UOMClass already exists | UOMCode, BaseUnitFlag, StandardConversion, BaseUOMCode, intraclass conversion, inverse-conversion flag | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UOM.ENFORCE-CONVERSION-DESIGN | decision | 30 | design_enforcement | compliant->UOM.DONE-CLASS-COMPLIANT;bypass_requested->UOM.GATE-BYPASS-APPROVAL;blocked->UOM.HANDLE-DESIGN-BLOCKER | UOM.LOOKUP-CLASS | stop | Operation is Create or Update and the supplied UOMClass has existing units |

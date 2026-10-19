# Design Enforcement

## Source

- Oracle Fusion Cloud SCM, Valuation Units, https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/valuation-units.html

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm valuation structure | Confirm the costing attributes and valuation-unit creation mode. |
| 2 | Select design approach | Use automatic generation unless a manual grouping is required to share a common cost. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A resolved valuation structure uses Auto mode | Blocking | resolve_valuation_structure | A manual source conflicts with the structure's automatic-generation design | Use the automatically generated valuation unit, or obtain an approved design change | Yes |
| A manual valuation unit is proposed and the mode was resolved | Warning | resolve_valuation_structure | The business need to group entities and share a common cost is not documented | Prefer automatic generation because it requires less manual intervention | Yes |
| A manual valuation unit includes details and the mode was resolved | Blocking | resolve_valuation_structure | The segment combinations do not conform to the confirmed costing attributes | Correct the segment values | Yes |
| Internal IDs are supplied directly | Info |  | No additional ID lookup is required | Validate the source against the current live Data Loader template | Yes |
| Details are added after a master is created | Blocking | resolve_valuation_unit_master | A matching parent row and the resolved ValuationUnitId are absent | Resolve exactly one master and regenerate the Data Loader source from the current template | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_valuation_structure | Before manual creation when ValuationStructureCode is supplied | Valuation structure mode and costing attributes | ora_reference_lookups.md |
| resolve_valuation_unit_master | Before adding details after a master is created | One nonblank ValuationUnitId | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VU.ENFORCE_CREATE_DESIGN | decision | 9 | design_enforcement | compliant->VU.DONE_CREATE;blocked->VU.HANDLE_ISSUE | VU.ROUTE_OPERATION | stop | A master is created, with or without details, after input and lookup review. |
| VU.ENFORCE_EXISTING_MASTER_DETAILS | decision | 10 | design_enforcement | compliant->VU.DONE_EXISTING_MASTER_DETAILS;blocked->VU.HANDLE_ISSUE | VU.RESOLVE_VALUATION_UNIT_MASTER | stop | Details are added after an existing master is resolved. |

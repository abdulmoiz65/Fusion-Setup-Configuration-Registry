# Dependency Readiness

## Source

- Oracle Fusion Cloud SCM, Valuation Units, https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/valuation-units.html

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| cost_organization | Cost organization | Yes | Creating a valuation unit | Lookup | CostOrganizationId or user-provided name or code | resolve_cost_organization | CostOrganizationId is mandatory for a valuation-unit master | Provide an ID, name, or code | CostOrganizationId |
| cost_book | Cost book | Yes | Creating a valuation unit | Lookup | CostBookId or user-provided CostBookCode | resolve_cost_book | CostBookId is scoped by the cost organization | Provide an ID or code | CostBookId |
| valuation_structure | Valuation structure and costing attributes | Yes | Creating a valuation unit | Lookup | ValuationStructureId or user-provided ValuationStructureCode | resolve_valuation_structure | A valuation unit is defined by the costing attributes in its corresponding valuation structure | Provide an ID or code | ValuationStructureId, SetId, SetName, and ValStructureModeCode |
| structure_instance | Structure instance number | Yes | A detail is supplied | Lookup | ValuationStructureId | resolve_structure_instance_number | The ADF combination validator requires the structure instance number | Derive it from the valuation structure | StructureInstanceNumber |
| segment_combination | Detail segment combination | Yes | Creating a manual valuation unit or adding details | Verify | SegmentValues and StructureInstanceNumber | validate_valuation_unit_segment_combination | A manual valuation unit requires at least one valid segment association | Correct the segment value when validation fails | Validated SegmentValues and ValuationUnitCombinationId |
| valuation_unit_master | Existing valuation unit master | Yes | Adding details after the master is created | Lookup | ValuationUnitCode | resolve_valuation_unit_master | The child uses the master's ValuationUnitId as its parent key | Provide the master code and resolve exactly one parent before detail preparation | ValuationUnitId |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Input validation | A required identifier or segment value is missing | No |
| Dependency readiness | A valuation structure, cost context, or Data Loader relationship is unconfirmed | No |
| Data Loader validation | The generated source does not conform to live metadata | No |

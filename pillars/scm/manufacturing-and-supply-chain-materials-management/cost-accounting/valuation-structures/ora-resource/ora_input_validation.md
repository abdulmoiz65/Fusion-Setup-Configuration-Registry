# Input Validation

## Source

| Source | Location | Used For |
|---|---|---|
| Oracle Valuation Structures | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/valuation-structures-and-valuation-units.html | Costing attributes, types, cost-method limits, and immutability after transactions |
| Oracle Valuation Structure Rules | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/valuation-structure-rules.html | Mandatory and optional costing-attribute conflict behavior |
| Oracle Valuation Units | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/valuation-units.html | Valuation-unit generation mode and manual-unit use case |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Valuation structure identity | Valuation structure name | Stop | Provide the business name for the valuation structure | Creating a valuation structure | |
| Valuation structure type | Asset, Expense, or Consigned | Stop | Provide the user-selected type; resolve its exact Oracle type code from the standard lookup | Creating a valuation structure | resolve_valuation_structure_type |
| Cost Valuation Granularity | Exact flexfield structure Name | Stop | Provide the granularity name; resolve the structure using the type-dependent KeyFlexfieldCode | A Cost Valuation Granularity is specified | resolve_cost_valuation_granularity |
| Costing attributes | Cost Organization and the selected additional costing attributes | Stop | Define the Cost Organization attribute and every required cost-segregation attribute | Creating or changing a valuation structure | |
| Valuation-unit mode | Auto, Both auto and manual, or manual behavior | Default to AUTO only when the resolved Valuation Structure Type Code is CONSIGNED; otherwise stop | Provide the user-selected mode, or allow the CONSIGNED default; resolve any supplied mode to its exact Oracle mode code | Creating a valuation structure | resolve_valuation_structure_mode |
| Valuation Structure Set | Exact Set Name | Stop | Provide the set name and resolve its exact SetId and SetCode | A Valuation Structure Set is specified | resolve_valuation_structure_set |
| Cost-profile context | Cost method and intended item cost profile use | Optional | Provide it only when validating a proposed association to an item cost profile; its absence must not stop valuation-structure creation | Associating the valuation structure to an item cost profile | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Cost Organization is included as a costing attribute | Reject the definition when Cost Organization is absent | Always | |
| Valuation structure type is Asset, Expense, or Consigned | Reject any other type or a value that has no exact standard-lookup Meaning match | Creating a valuation structure | resolve_valuation_structure_type |
| Cost Valuation Granularity has an exact type-dependent flexfield-structure match | Reject a granularity with no exact costingFlexFieldStructuresLOV match for the resolved KeyFlexfieldCode and supplied Name | A Cost Valuation Granularity is specified | resolve_cost_valuation_granularity |
| Valuation structure mode has an exact standard-lookup Meaning match | Reject a mode with no exact standard-lookup Meaning match | Creating a valuation structure | resolve_valuation_structure_mode |
| Valuation Structure Set Name has an exact costing-set match | Reject a set name with no exact costingSetsLOV SetName match | A Valuation Structure Set is specified | resolve_valuation_structure_set |
| Costing attributes are compatible with the inventory attributes and do not exceed on-hand granularity | Reject an incompatible or lower-granularity definition | Always | |
| Standard cost or periodic average cost uses only Cost Organization or Cost Organization - Inventory Organization granularity | Reject a more granular definition for either cost method | Validating association to an item cost profile whose cost method is standard cost or periodic average cost | |
| Project or Task is selected only when Project-Driven Supply Chain is opted in and set up | Reject the definition until the required feature setup exists | Project or Task is selected as a costing attribute | |
| An attribute missing on an item is optional, not mandatory | Reject association of the valuation structure to that item when the missing attribute is mandatory | Associating the valuation structure to an item cost profile | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VS.VALIDATE_INPUT | decision | 1 | validate_input | valid->VS.RESOLVE_VALUATION_STRUCTURE_TYPE;invalid->VS.HANDLE_ISSUE | none | stop | Creating or changing a Valuation Structure |

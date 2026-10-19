# Input Validation

## Source

- Oracle Fusion Cloud SCM, [Manage Cost Elements and Analysis Groups](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/manage-cost-elements-and-analysis-groups.html)
- Oracle Fusion Cloud SCM, [How Cost Components, Cost Elements, and Cost Component Groups Work Together](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/how-cost-components-cost-elements-and-cost-component-groups-work.html)

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Cost Element identity | CostElementCode, CostElementType meaning, CostElementSetName; optional CostElementDescription | Stop only when the code, type meaning, or set name is missing; resolve the type meaning and set name before building a payload | Create Cost Element, with or without an association | resolve_cost_element_type | |
| Cost Analysis Group association | Existing Cost Element identity, AnalysisGroupCode, AnalysisCode | Stop | Provide the existing Cost Element and the existing Analysis Group and Analysis Code | Add an association later, or create with an association | |
| Cost Analysis Group association removal | Existing Cost Element identity and the association to remove | Stop | Resolve the exact existing child mapping before preparing the delete row | Remove an association | resolve_element_analysis_group_mapping |
| Profit In Inventory organization | Inventory Organization name | Stop | Provide an unambiguous existing inventory-organization name | Resolved Cost Element Type meaning is Profit In Inventory | resolve_inventory_organization |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| CostElementType is supplied as a user-friendly Meaning, not an arbitrary code | Query CST_COST_ELEMENT_TYPES after excluding RESOURCE_DIRECT, RESOURCE_OVERHEAD, and OUTBOUND_TAX; require exactly one case-insensitive exact Meaning match; serialize its LookupCode as CostElementType and retain the display Meaning only in CostElementTypeMeaning when that workbook column is present | Always | resolve_cost_element_type |
| Data Loader workbook source | Provide parent Cost Element values and, when requested, child Analysis Group association values in the core Data Loader Excel template; core.data-loader generates the import source | Always | |
| CostElementSetName resolves uniquely | Query costingSetsLOV, require exactly one case-insensitive exact SetName match, and pass its SetId as CostElementSetId | Always | resolve_cost_element_set |
| Inventory Organization is mandatory only for Profit In Inventory | Resolve the supplied organization name uniquely and add its OrganizationId to the parent payload | Resolved Cost Element Type meaning is Profit In Inventory | resolve_inventory_organization |
| Inventory Organization is not collected for other types | Do not request or send OrganizationId unless the REST service requires it | Resolved Cost Element Type meaning is not Profit In Inventory | |
| Analysis Group and Analysis Code already exist | Confirm the user declares both values already exist; do not create either prerequisite in this workflow | An association is requested | |
| Profit In Inventory uses the Common Cost Element Set | Stop when the resolved Cost Element Set name is not Common | Resolved Cost Element Type meaning is Profit In Inventory | resolve_cost_element_set |
| Analysis Code is unique within an Analysis Group | Stop when the requested mapping duplicates an Analysis Group and Analysis Code combination for the Cost Element | An association is requested | |
| Combined create parent correlation | Require every new child row to use the same `CostElementCode` and `CostElementSetId` as the new parent; leave child `CostElementId` blank rather than inventing a persistent value | A new Cost Element and child association are in the same source | |
| Association insert action | Require `RestAction` `POST` on every child association row; reject a missing action and reject `CREATE` and `MERGE` | Add an association, either during parent creation or later | |
| Association removal identity | Resolve exactly one existing child mapping and use its ElementAnalysisGroupId with child RestAction `DELETE` | Remove an association | resolve_element_analysis_group_mapping |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A Cost Element only is requested and all parent values resolve | Parent payload contains CostElementCode, resolved CostElementType, and resolved CostElementSetId; include CostElementDescription only when supplied and OrganizationId only when required | Continue to Data Loader preview through core.data-loader | |
| A Cost Element with an association is requested and all parent values resolve | Add one or more nested costAccountingCostElementAnalysisGroups entries with RestAction `POST`, resolved AnalysisGroupId, validated AnalysisGroupCode, and validated AnalysisCode | Continue to Data Loader preview through core.data-loader | |
| A new Cost Element and association are supplied together | Use the Cost Element alternate key (`CostElementCode`, `CostElementSetId`) on both parent and child rows; do not serialize an orphan child with a blank parent context | Provide the parent and child values to core.data-loader for serialization and preview | |
| An association for an existing Cost Element is requested | Prepare the child-resource association through the registered parent business object; do not recreate the Cost Element | Continue to Data Loader preview through core.data-loader | |
| An existing association is removed | Prepare only the child row with CostElementId, resolved ElementAnalysisGroupId, and RestAction `DELETE`; retain the parent Cost Element | Continue to Data Loader preview through core.data-loader | resolve_element_analysis_group_mapping |

## Nested Resource Contract

| Parent Resource | Child Resource | Supported Use |
|---|---|---|
| costAccountingCostElements | costAccountingCostElementAnalysisGroups | Create a Cost Element with one or more Analysis Group and Analysis Code mappings. |
| costAccountingCostElements | costAccountingCostElementAnalysisGroups | Add an Analysis Group and Analysis Code mapping later for an existing Cost Element without recreating the parent. |
| costAccountingCostElements | costAccountingCostElementAnalysisGroups | Remove one exactly resolved Analysis Group and Analysis Code mapping later for an existing Cost Element without deleting the parent. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCE.VALIDATE_INPUT | decision | 1 | validate_input | valid->CCE.RESOLVE_COST_ELEMENT_TYPE;invalid->CCE.HANDLE_ISSUE | none | stop | Create a Cost Element or manage an Analysis Group association |

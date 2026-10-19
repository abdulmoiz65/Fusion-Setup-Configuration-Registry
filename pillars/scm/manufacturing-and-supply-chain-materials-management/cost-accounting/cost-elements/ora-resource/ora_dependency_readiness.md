# Dependency Readiness

## Source

- Oracle Fusion Cloud SCM, [Manage Cost Elements and Analysis Groups](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/manage-cost-elements-and-analysis-groups.html)
- Oracle Fusion Cloud SCM, [How Cost Components, Cost Elements, and Cost Component Groups Work Together](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/how-cost-components-cost-elements-and-cost-component-groups-work.html)

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Cost Element Type | Resolve one eligible CST_COST_ELEMENT_TYPES lookup meaning to LookupCode. |
| 2 | Cost Element Set | Resolve one existing Cost Element Set name to SetId. |
| 3 | Inventory Organization | Resolve one existing organization only when the selected type is Profit In Inventory. |
| 4 | Common Cost Element Set | Confirm the resolved Cost Element Set is Common when the selected type is Profit In Inventory. |
| 5 | Cost Analysis Group and Analysis Code | Ensure both already exist before associating them to a Cost Element. |
| 6 | Existing Analysis Group mapping | Resolve exactly one nested child mapping before removing it from an existing Cost Element. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CCE-COST-ELEMENT-TYPE | Eligible Cost Element Type | Yes | Always | Lookup | Fusion standardLookupsLOV | resolve_cost_element_type | The REST payload must receive the approved lookup code, not an arbitrary user value. | Provide a valid Cost Element Type meaning. | CostElementType from LookupCode |
| CCE-COST-ELEMENT-SET | Existing Cost Element Set | Yes | Always | Lookup | Fusion costingSetsLOV | resolve_cost_element_set | The REST payload requires CostElementSetId. | Provide an unambiguous existing Cost Element Set name. | CostElementSetId from SetId |
| CCE-INVENTORY-ORGANIZATION | Existing Inventory Organization | Conditional | Resolved type meaning is Profit In Inventory | Lookup | Fusion inventoryOrganizations | resolve_inventory_organization | Profit In Inventory requires OrganizationId. | Provide one exact Inventory Organization name. | OrganizationId from OrganizationId |
| CCE-PROFIT-IN-INVENTORY-SET | Common Cost Element Set | Yes | Resolved type meaning is Profit In Inventory | Verify | Resolved CostElementSetName and CostElementSetId | resolve_cost_element_set | A Profit in Inventory Cost Element must be shared across cost organizations through the Common Cost Element Set. | Select Common as the Cost Element Set. | CostElementSetId from the resolved Common set |
| CCE-ANALYSIS-ASSOCIATION | Existing Cost Analysis Group and Analysis Code | Yes | An association is requested | Lookup | Fusion costAccountingCostAnalysisGroups and its costAccountingCostAnalysisCodes child resource | resolve_analysis_group | The workflow must validate the group, derive its AnalysisGroupId, then validate the code under that exact group before associating it. | Provide exact group and code values; do not use a supplied or assumed group ID. | Validated AnalysisGroupCode, AnalysisGroupId, AnalysisCode |
| CCE-ANALYSIS-ASSOCIATION-REMOVE | Existing Cost Element Analysis Group mapping | Yes | Remove an association | Lookup | Nested Fusion costAccountingCostElements child resource | resolve_element_analysis_group_mapping | A child delete requires the exact existing ElementAnalysisGroupId. | Provide the Cost Element and the exact existing Analysis Group and Analysis Code mapping to remove. | ElementAnalysisGroupId, CostElementId |
| CCE-COST-ELEMENT-DELETE | Fusion delete evaluation | Yes | Delete a Cost Element | Verify | Fusion Data Loader delete |  | Do not pre-check child mappings or other references. Fusion evaluates the complete dependency state when processing the parent delete. | Submit a parent delete with the exact CostElementId; resolve any Fusion rejection before a new request. | CostElementId |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | All required lookup results are unique and any requested Analysis Group and Analysis Code already exist | Yes, read-only lookup only |
| Blocked | A required lookup has zero or multiple exact matches | No |
| Blocked | Profit In Inventory is paired with a Cost Element Set other than Common | No |
| Blocked | An association is requested but its Analysis Group or Analysis Code does not already exist | No |
| Ready | An Analysis Group association is being edited or removed; parent Cost Element references do not block a mapping-only change | Yes, perform the child-mapping operation only |
| Blocked | An association removal does not resolve exactly one existing child mapping | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCE.ENFORCE_ASSOCIATION_PREREQUISITES | decision | 5 | resolve_dependency | ready->CCE.PREVIEW_GATE;blocked->CCE.HANDLE_ISSUE | CCE.RESOLVE_INVENTORY_ORGANIZATION | stop | Create a Cost Element or manage an Analysis Group association |

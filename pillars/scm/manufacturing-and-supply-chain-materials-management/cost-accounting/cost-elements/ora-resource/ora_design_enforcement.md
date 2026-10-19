# Design Enforcement

## Source

- Oracle Fusion Cloud SCM, [Manage Cost Elements and Analysis Groups](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/manage-cost-elements-and-analysis-groups.html)
- Oracle Fusion Cloud SCM, [How Cost Components, Cost Elements, and Cost Component Groups Work Together](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/how-cost-components-cost-elements-and-cost-component-groups-work.html)

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate type | Derive CostElementType from the selected CST_COST_ELEMENT_TYPES Meaning. |
| 2 | Validate set | Derive CostElementSetId from the supplied Cost Element Set name. |
| 3 | Apply conditional organization rule | Require and resolve OrganizationId only for Profit In Inventory. |
| 4 | Apply Profit In Inventory set rule | Require the Common Cost Element Set for Profit In Inventory. |
| 5 | Validate association prerequisites | Associate only an already existing Cost Analysis Group and Analysis Code. |
| 6 | Enforce Cost Element immutability | Do not change the Cost Element code, type, or Cost Element Set after creation. |
| 7 | Apply lifecycle controls | Allow mapping-only edits or removals; submit a parent Cost Element delete without independently checking or removing Analysis Group child mappings or other references. Fusion evaluates the complete dependency state. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Always | Error | resolve_cost_element_type | CostElementType is supplied as a code, is excluded, or does not have exactly one matching Meaning | Select an eligible user-friendly Cost Element Type meaning and use its resolved LookupCode. | Yes |
| Always | Error | resolve_cost_element_set | CostElementSetName does not resolve to exactly one SetId | Correct the Cost Element Set name before payload preparation. | Yes |
| Resolved type meaning is Profit In Inventory | Error | resolve_inventory_organization | Inventory Organization is omitted or does not uniquely resolve | Provide a unique existing Inventory Organization name; include the resolved OrganizationId. | Yes |
| Resolved type meaning is Profit In Inventory | Error | resolve_cost_element_set | CostElementSetName is not Common | Select the Common Cost Element Set so the Cost Element can be shared across cost organizations. | Yes |
| An association is requested | Error | | Analysis Group or Analysis Code is not already configured | Create the prerequisite setup separately, then return to this association workflow. | Yes |
| An association is requested | Error | | The requested Analysis Group and Analysis Code combination duplicates an existing mapping | Use a distinct existing Analysis Code within the Analysis Group, or do not create a duplicate mapping. | Yes |
| A request changes an existing Cost Element | Error | | The request changes CostElementCode, CostElementType, or CostElementSetId | Keep these parent values unchanged; create a separate Cost Element if a different immutable value is needed. | No |
| A request edits or removes an Analysis Group association | Allowed | | None solely because the parent Cost Element is referenced through a Cost Component Group or Cost Profile | Apply the change to the child mapping only; do not modify or delete the parent Cost Element. | Yes |
| A request deletes a Cost Element | Allowed | | None | Prepare the parent delete without pre-checking child mappings or other references. Fusion evaluates the complete dependency state during the Data Loader delete. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_cost_element_type | Always | Meaning, LookupCode | ora_reference_lookups.md |
| resolve_cost_element_set | Always | SetName, SetId | ora_reference_lookups.md |
| resolve_inventory_organization | Resolved type meaning is Profit In Inventory | OrganizationName, OrganizationId | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCE.PREVIEW_GATE | decision | 6 | design_enforcement | compliant->CCE.READY_FOR_DATA_LOADER;blocked->CCE.HANDLE_ISSUE | CCE.ENFORCE_ASSOCIATION_PREREQUISITES | stop | Before core.data-loader prepares an immutable preview |

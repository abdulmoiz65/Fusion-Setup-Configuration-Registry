# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Item Cost Profile identity | Cost Organization Name, Cost Book Code, Item Number | Stop | Request every missing user-friendly value; do not accept internal IDs as substitutes for this input contract | Create or Delete | |
| Cost Profile assignment | Expense Cost Profile and/or Asset Cost Profile and/or Consigned Cost Profile | Stop | Request at least one complete Cost Profile Code | Create only | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Cost Organization Name is supplied as a complete value | Resolve case-insensitively and continue only when exactly one returned CostOrganizationName equals the supplied value; map `CostOrganizationId` for downstream binds | Always | resolve_cost_organization_exact |
| Cost Organization Name is missing | Stop validation before any Cost Book, Item, or Cost Profile lookup | Always | |
| Cost Book Code is supplied as a complete value | Resolve case-insensitively within the resolved Cost Organization and continue only when exactly one returned CostBookCode equals the supplied value | Always | resolve_cost_book_exact |
| Item Number is supplied as a complete value | Resolve case-insensitively within the resolved Cost Organization through the environment-resolved Costing Items LOV route, require CostingEnabledFlag=true, and continue only when exactly one returned Item equals the supplied value | Always | resolve_costing_item_exact |
| Expense Cost Profile Code is complete | Resolve case-insensitively using the EXPENSE lookup and continue only when exactly one returned CostProfileCode equals the supplied value | Expense Cost Profile is supplied | resolve_expense_cost_profile_exact |
| Asset Cost Profile Code is complete | Resolve case-insensitively using the ASSET lookup and continue only when exactly one returned CostProfileCode equals the supplied value | Asset Cost Profile is supplied | resolve_asset_cost_profile_exact |
| Consigned Cost Profile Code is complete | Resolve case-insensitively using the CONSIGNED lookup and continue only when exactly one returned CostProfileCode equals the supplied value | Consigned Cost Profile is supplied | resolve_consigned_cost_profile_exact |
| At least one Cost Profile Code is supplied | Continue only when one or more profile-code inputs are present | Create only | |
| One value is supplied for each selected profile type | Accept no more than one Expense, one Asset, and one Consigned Cost Profile Code in an Item Cost Profile request | Always | |
| Delete identity is supplied as complete friendly values | Require Cost Organization Name, Cost Book Code, and Item Number; do not request ItemCostProfileId from the end user | Delete an Item Cost Profile | prepare_delete_loader_source |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Required values are present | Resolve Cost Organization before every other value | Continue only after one CostOrganizationId is resolved | resolve_cost_organization_exact |
| Cost Organization is resolved | Resolve a non-Periodic Average Cost Book using its CostOrganizationId finder bind | Continue only after one CostBookId is resolved | resolve_cost_book_exact |
| Cost Book is resolved | Resolve Costing Enabled Item using its CostOrganizationId finder bind | Continue only after one InventoryItemId and InventoryOrgId are resolved | resolve_costing_item_exact |
| Expense Cost Profile is supplied | Resolve only the Expense profile; absence of Asset or Consigned profile is not an error | Continue only after one ExpenseCostProfileId is resolved | resolve_expense_cost_profile_exact |
| Asset Cost Profile is supplied | Resolve only the Asset profile; absence of Expense or Consigned profile is not an error | Continue only after one AssetCostProfileId is resolved | resolve_asset_cost_profile_exact |
| Consigned Cost Profile is supplied | Resolve only the Consigned profile; absence of Expense or Asset profile is not an error | Continue only after one ConsignedCostProfileId is resolved | resolve_consigned_cost_profile_exact |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ICP.VALIDATE_INPUT | decision | 1 | validate_input | create_valid->ICP.RESOLVE_COST_ORGANIZATION;delete_valid->ICP.DELETE_LOADER_SOURCE;invalid->ICP.HANDLE_ISSUE | none | stop | Create or Delete an Item Cost Profile |

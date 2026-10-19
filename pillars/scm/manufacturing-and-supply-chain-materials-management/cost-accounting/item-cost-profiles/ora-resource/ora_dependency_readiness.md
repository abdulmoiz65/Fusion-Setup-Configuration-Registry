# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Cost Organization | Validate one exact Cost Organization Name and map its returned `CostOrganizationId` before validating the Cost Book, Item, and Cost Profiles. |
| 2 | Cost Book | Validate one exact non-Periodic Average Cost Book Code for the selected Cost Organization. |
| 3 | Item | Validate one exact Costing Enabled Item Number for the selected Cost Organization. |
| 4 | Cost Profiles | Resolve each supplied profile type to its respective CostProfileId; the Cost Organization set and Common set are the eligible profile sources. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| ICP.COST_ORGANIZATION | Cost Organization | Yes | Always | Lookup | Cost Organization Name | resolve_cost_organization_exact | Scopes Cost Book, Item, and Cost Profile validation through its returned CostOrganizationId | Provide a valid unique complete Cost Organization Name | Validated CostOrganizationId |
| ICP.COST_BOOK | Cost Book | Yes | Always | Lookup | Cost Book Code and selected CostOrganizationId | resolve_cost_book_exact | Must belong to the selected Cost Organization and have PeriodicAverageFlag=false | Provide a valid unique complete non-Periodic Average Cost Book Code | Validated Cost Book |
| ICP.ITEM | Costing Enabled Item | Yes | Always | Lookup | Item Number and selected CostOrganizationId | resolve_costing_item_exact | Item Cost Profiles require an item enabled for costing in the selected Cost Organization; resolves the generic route first and retains a verified same-environment route only when needed | Provide a valid unique complete Costing Enabled Item Number | Validated Costing Enabled Item |
| ICP.EXPENSE_PROFILE | Expense Cost Profile | Conditional | Expense Cost Profile is supplied | Lookup | Expense Cost Profile Code and CostOrgId | resolve_expense_cost_profile_exact | Assigns the supplied Expense profile from the Cost Organization or Common set | Provide its complete unique non-Periodic Average code | ExpenseCostProfileId |
| ICP.ASSET_PROFILE | Asset Cost Profile | Conditional | Asset Cost Profile is supplied | Lookup | Asset Cost Profile Code and CostOrgId | resolve_asset_cost_profile_exact | Assigns the supplied Asset profile from the Cost Organization or Common set | Provide its complete unique non-Periodic Average code | AssetCostProfileId |
| ICP.CONSIGNED_PROFILE | Consigned Cost Profile | Conditional | Consigned Cost Profile is supplied | Lookup | Consigned Cost Profile Code and CostOrgId | resolve_consigned_cost_profile_exact | Assigns the supplied Consigned profile from the Cost Organization or Common set | Provide its complete unique code | ConsignedCostProfileId |
| ICP.DELETE_LOADER_SOURCE | Item Cost Profile deletion source | Yes | Delete an Item Cost Profile | Data Loader preflight | Cost Organization Name, Cost Book Code, Item Number | prepare_delete_loader_source | Validates the complete delete-oriented source through the registered Data Loader business-object contract; no direct REST identity lookup is permitted | Provide complete unique friendly values and correct the source if validation is blocked | Validated immutable delete-oriented source |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | An exact unique result resolves every applicable dependency; continue to payload design enforcement | Yes |
| Blocked | A required value is missing, no exact result is found, or more than one exact result exists; stop and ask the user for a valid unique value | Lookup only |

# Default Cost Profiles Dependency Readiness

Source: [Oracle Fusion Cloud SCM 26c: Set Up a Default Cost Profile](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/set-up-a-default-cost-profile.html).

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Cost organization | Resolve the specified cost organization before resolving a cost book or a type-specific cost profile. |
| 2 | Cost book | Resolve a cost book only when a cost-book assignment is selected. |
| 3 | Item category | Resolve an item category only when a category assignment is selected. |
| 4 | Cost profiles | Resolve each supplied type-specific cost profile using the resolved cost organization. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| DCP.COST_ORGANIZATION | Cost organization | Yes | A cost book or a type-specific cost profile is supplied | Lookup | Fusion costOrganizationsLOV exact-name lookup | resolve_cost_organization_by_exact_name | The resolved CostOrganizationId is required by the cost-book and cost-profile contracts | Provide one exact Cost Organization Name | CostOrgId |
| DCP.COST_BOOK | Cost book | Yes | Cost-book assignment is selected | Lookup | Fusion costOrgBooksLOV exact cost-book-code lookup by resolved CostOrganizationId | resolve_cost_book_by_cost_organization | The default profile can be assigned at cost-book level; its PeriodicAverageFlag is required for periodic-average profile enforcement | Provide one exact Cost Book Code for the resolved cost organization | CostBookId, PeriodicAverageFlag |
| DCP.ITEM_CATEGORY_BY_CODE | Item category by code | Yes | Category assignment is selected and Item Category Code is supplied | Lookup | Fusion allItemCategoriesLOV exact-code lookup | resolve_item_category_by_exact_code | The default profile can be assigned at item-category level | Provide one exact Item Category Code | ItemCategoryId, ItemCategoryCode, ItemCategoryName |
| DCP.ITEM_CATEGORY_BY_NAME | Item category by name | Yes | Category assignment is selected and Item Category Name is supplied | Lookup | Fusion allItemCategoriesLOV exact-name lookup | resolve_item_category_by_exact_name | The default profile can be assigned at item-category level | Provide one exact Item Category Name | ItemCategoryId, ItemCategoryCode, ItemCategoryName |
| DCP.PROFILE_CREATION | New-item profile creation | Yes | Always | Lookup | Fusion standardLookupsLOV exact lookup | resolve_profile_creation_code_by_exact_meaning | The default profile requires a resolved profile-creation code | Provide one exact standard-lookup Meaning; the current developer-selected value is Auto | ProfileCreationCode |
| DCP.ASSET_COST_PROFILE | Asset cost profile | Yes | An Asset Cost Profile Code is supplied | Lookup | Fusion costProfileDetails SearchBySetAccess lookup | resolve_asset_cost_profile_by_exact_code | The resolved profile is used for AssetCostProfileId and its CostMethodCode is evaluated against the resolved cost-book flag | Provide one exact Asset Cost Profile Code | AssetCostProfileId, AssetCostMethodCode |
| DCP.EXPENSE_COST_PROFILE | Expense cost profile | Yes | An Expense Cost Profile Code is supplied | Lookup | Fusion costProfileDetails SearchBySetAccess lookup | resolve_expense_cost_profile_by_exact_code | The resolved profile is used for ExpenseCostProfileId and its CostMethodCode is evaluated against the resolved cost-book flag | Provide one exact Expense Cost Profile Code | ExpenseCostProfileId, ExpenseCostMethodCode |
| DCP.CONSIGNED_COST_PROFILE | Consigned cost profile | Yes | A Consigned Cost Profile Code is supplied | Lookup | Fusion costProfileDetails SearchBySetAccess lookup | resolve_consigned_cost_profile_by_exact_code | The resolved profile is used for ConsignedCostProfileId and its CostMethodCode is evaluated against the resolved cost-book flag | Provide one exact Consigned Cost Profile Code | ConsignedCostProfileId, ConsignedCostMethodCode |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Lookup | A read-only REST contract resolves the required attribute | Yes; only the documented lookup may run |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|

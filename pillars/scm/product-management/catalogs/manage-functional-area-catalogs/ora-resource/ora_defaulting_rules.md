# Defaulting Rules

## Functional-area values are user-provided

When `HierarchyEnabled` is omitted, default it from the current `itemCatalogs/describe` metadata: `HierarchyEnabledFlag.defaultValue=true`, mapped to `EGP_CATALOG.csv.HierarchyEnabled=Y`. Preserve any explicitly supplied normalized value. A supplied public Oracle Functional Area Catalog Rules document reference may be retained as validation evidence; its absence is recorded as `not_provided` and does not block.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Catalog Code | Supplied Catalog Name | Catalog Code is blank and Catalog Name is nonblank | No | |
| Catalog Name | Supplied Catalog Code | Catalog Name is blank and Catalog Code is nonblank | No | |
| EGP_CATALOG.csv.CategorySetName | Resolved Catalog Name | A non-omitted catalog row is prepared for the FSM package | No | |
| EGP_CATALOG.csv.ControlLevel | 1 | ControlLevel and its REST/UI aliases are blank | No | |
| EGP_CATALOG.csv.MultItemCatAssignFlag | N | MultItemCatAssignFlag and its REST/UI aliases are blank, and no default functional-area assignment is requested | No | |
| EGP_CATALOG.csv.HierarchyEnabled | Y | HierarchyEnabled and its aliases are blank | No | itemCatalogs/describe `HierarchyEnabledFlag.defaultValue=true` |
| EGP_CATALOG.csv.CatalogContentCode | LEAF_ITEMS | CatalogContentCode and its REST/UI aliases are blank for a non-omitted catalog row | No | resolve_catalog_content_code |
| DefaultCategoryRequired | Yes | A default Category Code or Category Name is supplied for a functional-area assignment and no conflicting explicit value is supplied | No | |
| EGP_CATEGORY.csv.StartDateActive | Today's date | StartDateActive is blank and the user confirms today's date | No | |
| Category Code | Supplied Category Name | Category Code is blank and Category Name is nonblank | No | |
| Category Name | Supplied Category Code | Category Name is blank and Category Code is nonblank | No | |
| EGP_CATEGORY.csv.SummaryFlag | Y | SummaryFlag is blank or not provided | No | |
| EGP_CATEGORY.csv.SupplierEnabledFlag | Y | SupplierEnabledFlag is blank or not provided | No | |
| EGP_CATALOG.csv.ValidateFlag | Y | ValidateFlag is blank or not provided | No | |

## FSM CSV Mapping

| Source Value | FSM CSV Target | Applies When | Required Result |
|---|---|---|---|
| Resolved Catalog Code | EGP_CATALOG.csv.CatalogCode | A non-omitted catalog row is prepared | Nonblank value equal to the resolved Catalog Code |
| Resolved Catalog Name | EGP_CATALOG.csv.CategorySetName | A non-omitted catalog row is prepared | Nonblank value equal to the resolved Catalog Name; when Catalog Name was defaulted from Catalog Code, write that same approved value here |
| REST Describe default | EGP_CATALOG.csv.ControlLevel | ControlLevel and its REST/UI aliases are blank | `1` |
| REST Describe default | EGP_CATALOG.csv.MultItemCatAssignFlag | MultItemCatAssignFlag and its REST/UI aliases are blank, and no default functional-area assignment is requested | `N` |
| Per-row resolved catalog-content lookup code | EGP_CATALOG.csv.CatalogContentCode | A non-omitted catalog row is prepared | Nonblank value equal to the exact enabled, effective `EGP_CATALOG_CONTENT_CODE` LookupCode resolved for that row from the one complete cached lookup receipt |
| Canonical user-provided category-content code | EGP_CATEGORY.csv.CategoryContentCode | A category row is prepared and CategoryContentCode or its REST/UI alias is supplied | Exact canonical `ITEM_ONLY` or `MIXED` value |
| REST Describe default or user-provided value | EGP_CATALOG.csv.HierarchyEnabled | A catalog row is prepared | Explicit normalized value, otherwise `Y` from `HierarchyEnabledFlag.defaultValue=true` |
| User-provided functional-area value | EGP_CATALOG.csv.MultItemCatAssignFlag | A catalog is created or assigned to a resolved functional area | Exact user-provided `MultItemCatAssignFlag` value |
| Default Category Code or Name | DefaultCategoryRequired validation evidence | A default category is supplied for a functional-area assignment | Record inferred value `Yes`; this is not an FSM CSV column |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CATALOGS.DEFAULT-CATALOG-IDENTITY | step | 14 | apply_default | defaulted->CATALOGS.RESOLVE-CATALOG-CONTENT-CODE;invalid->RETURN_ISSUES | CATALOGS.CANONICALIZE-INPUT | stop | A catalog or category record supplies an identity value, or a category or functional-area assignment supplies a catalog reference |
| CATALOGS.MAP-CATALOG-IDENTITY-TO-FSM-CSV | step | 16 | apply_default | functional_area_assignment->CATALOGS.RESOLVE-FUNCTIONAL-AREA-ID;no_functional_area_assignment->CATALOGS.VERIFY-REFERENCED-BASELINE-CATALOG;missing->RETURN_ISSUES | CATALOGS.RESOLVE-CATALOG-CONTENT-CODE | stop | A non-omitted EGP_CATALOG.csv row is prepared for an FSM package |

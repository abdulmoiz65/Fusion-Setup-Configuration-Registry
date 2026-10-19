# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| MultItemCatAssignFlag | N | A default catalog is assigned to Sales | No | |
| DefaultCategoryRequired | No | A default catalog is assigned to Sales | No | |
| EGP_CATALOG.csv.CatalogContentCode | ALL_ITEMS | A catalog row is independently included in the delegated package for the Sales request | No | |
| EGP_CATALOG.csv.HierarchyEnabled | Y | A catalog row is independently included in the delegated package for the Sales request | No | |
| EGP_CATALOG.csv.ControlLevel | 1 | A catalog row is independently included in the delegated package for the Sales request | No | |
| EGP_CATEGORY.csv.CategoryContentCode | MIXED | A category row is independently included in the delegated package for the Sales request | No | |

The supplied Sales Functional Area Rule screenshot is the authority for these defaults. The assignment-only CSV row carries FunctionalAreaId and CatalogCode; it must not add catalog or category rows solely to restate a Sales policy value.

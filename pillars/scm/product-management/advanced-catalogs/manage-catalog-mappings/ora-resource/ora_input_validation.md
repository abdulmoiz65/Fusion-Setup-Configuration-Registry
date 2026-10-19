# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Catalog category mapping headers | EGP_CATALOG_CATEGORY_MAPPING.csv with CatgMapName, SourceCatalogCode, and TargetCatalogCode | Stop validation and report the missing file or column. | Provide the exported mapping-header CSV with the exact required columns. | A Manage Catalog Mappings CSV validation is requested. | |
| Catalog category mapping details | ORA_ITEM_CATEGORY_MAPPING_DETAIL.csv with EGP_CATALOG_CATEGORY_MAPPING.CatgMapName, SourceCategoryCode, and TargetCategoryCode | Stop validation and report the missing file or column. | Provide the exported mapping-detail CSV with the exact required columns. | A Manage Catalog Mappings CSV validation is requested. | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Mapping-detail header join | For every detail row, use EGP_CATALOG_CATEGORY_MAPPING.CatgMapName to find exactly one EGP_CATALOG_CATEGORY_MAPPING.csv row whose CatgMapName is an exact, case-sensitive match. Reject the detail row when the match is missing or duplicated. | A mapping-detail row is supplied. | |
| Parent-to-child cardinality | Treat EGP_CATALOG_CATEGORY_MAPPING.csv.CatgMapName as the parent key and ORA_ITEM_CATEGORY_MAPPING_DETAIL.csv.EGP_CATALOG_CATEGORY_MAPPING.CatgMapName as its child key. One mapping-header row may match many detail rows; repeated child keys are valid and must not be rejected. | A mapping-detail row is supplied. | |
| Per-detail-row lookup context | Create one immutable validation context for each detail row: detail-row identity, CatgMapName, matched SourceCatalogCode, SourceCategoryCode, matched TargetCatalogCode, and TargetCategoryCode. A context may use values only from its own matched header and detail row. | The exact header join succeeds for a mapping-detail row. | |
| Source catalog/category values | Reject the detail row when its matched header has a blank SourceCatalogCode or the detail row has a blank SourceCategoryCode. | A mapping-detail row is supplied. | |
| Target catalog/category values | Reject the detail row when its matched header has a blank TargetCatalogCode or the detail row has a blank TargetCategoryCode. | A mapping-detail row is supplied. | |

## Binding Contract

For every immutable detail-row context, bind only these pairs:

| Lookup Branch | Catalog Value | Category or Item-Class Value | Prohibited Substitution |
|---|---|---|---|
| Source category | Matched SourceCatalogCode | Detail-row SourceCategoryCode | Do not use TargetCatalogCode or TargetCategoryCode. |
| Non-ROOT_ICC target category | Matched TargetCatalogCode | Detail-row TargetCategoryCode | Do not use SourceCatalogCode or SourceCategoryCode. |
| ROOT_ICC target item class | ROOT_ICC TargetCatalogCode | Detail-row TargetCategoryCode | Do not call itemCategories or substitute source values. |

For example, the `Test 3` detail row binds `AK_CATSET` with `ASSEMBLY.DESKTOP300100058588702` for the source lookup, then binds `Code_1100000311` with `Electrical and Electronic Equip Comp` for the target lookup.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCM.VALIDATE_CSV_CONTRACT | step | 10 | validate_input | valid->MCM.RESOLVE_SOURCE_CATEGORIES;invalid->RETURN_ISSUES | none | stop | Validate all CSV contracts and build one immutable context for every mapping-detail row. |

# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_source_category_by_catalog | For every immutable detail-row context after CSV contract validation | That context's matched SourceCatalogCode; that context's SourceCategoryCode | /fscmRestApi/resources/11.13.18.05/itemCategories?q=CatalogCode='{SourceCatalogCode}'%20AND%20CategoryCode='{SourceCategoryCode}' | CategoryCode and CatalogCode returned by itemCategories | Build the q expression with uppercase AND between the catalog and category predicates, URL-encode it exactly once with spaces as %20, and require exactly one returned category whose CatalogCode and CategoryCode exactly equal that context's SourceCatalogCode and SourceCategoryCode. Never substitute target values. | Per-row source lookup result with detail-row identity and CatgMapName | Zero results: record that the given source category may not belong to the given source catalog. Multiple results: record an ambiguous source category result. Read failure: record the sanitized diagnostic. Continue independent row validation. |
| resolve_target_category_by_catalog | For every immutable detail-row context whose TargetCatalogCode is not ROOT_ICC | That context's matched TargetCatalogCode; that context's TargetCategoryCode | /fscmRestApi/resources/11.13.18.05/itemCategories?q=CatalogCode='{TargetCatalogCode}'%20AND%20CategoryCode='{TargetCategoryCode}' | CategoryCode and CatalogCode returned by itemCategories | Build the q expression with uppercase AND between the catalog and category predicates, URL-encode it exactly once with spaces as %20, and require exactly one returned category whose CatalogCode and CategoryCode exactly equal that context's TargetCatalogCode and TargetCategoryCode. Never substitute source values. | Per-row target lookup result with detail-row identity and CatgMapName | Zero results: record that the given target category may not belong to the given target catalog. Multiple results: record an ambiguous target category result. Read failure: record the sanitized diagnostic. Continue independent row validation. |
| resolve_target_item_class | For every immutable detail-row context whose TargetCatalogCode is ROOT_ICC | That context's TargetCategoryCode | /fscmRestApi/resources/11.13.18.05/itemClasses?q=ItemClassCode='{TargetCategoryCode}' | ItemClassCode returned by itemClasses | URL-encode only the context's TargetCategoryCode and require exactly one returned ItemClassCode that exactly equals it. Do not call itemCategories or substitute source values for this branch. | Per-row ROOT_ICC lookup result with detail-row identity and CatgMapName | Zero results: record that the supplied target category value does not resolve as an item class for ROOT_ICC. Multiple results: record an ambiguous item-class result. Read failure: record the sanitized diagnostic. Continue independent row validation. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Source category lookup returns no result | Record the row-level failure that the given source category may not belong to the given source catalog; continue independent rows and block only in aggregate. |
| Non-ROOT_ICC target category lookup returns no result | Record the row-level failure that the given target category may not belong to the given target catalog; continue independent rows and block only in aggregate. |
| ROOT_ICC target lookup returns no result | Record the row-level failure that the supplied target category value does not resolve as an item class for ROOT_ICC; continue independent rows and block only in aggregate. |
| TargetCatalogCode is ROOT_ICC | Skip resolve_target_category_by_catalog and validate TargetCategoryCode only with resolve_target_item_class. |
| itemCategories query is constructed | Combine CatalogCode and CategoryCode predicates in one q expression using uppercase AND with one space on either side. Encode spaces as %20 in the URL, not HTML entities such as &nbsp; or &#32;. Apply this to both source-category and non-ROOT_ICC target-category lookups. |
| Encoded itemCategories URL is passed to the shared REST client | Construct the raw q expression from the immutable row context, percent-encode it once with spaces as %20, then pass the resource path plus encoded query as the endpoint. Do not also pass q through --query, which would encode percent signs again. The displayed URL templates show the AND separator encoding; substituted values and other query characters must also be encoded once. |
| itemCategories or itemClasses lookup is sent | Send REST-Framework-Version: 9 on every GET as required by the core.data-loader request policy. Oracle documents the header and its server-selected default behavior; FSCR core policy fixes the value at 9. |

## Documentation Sources

| Source | Authority | Verified Contract | Location |
|---|---|---|---|
| Oracle Fusion Cloud SCM 26B, Get all categories | Official Oracle documentation | GET itemCategories collection path; CatalogCode and CategoryCode are queryable | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/fasrp/op-itemcategories-get.html |
| Oracle Fusion Cloud SCM 26B, Get all item classes | Official Oracle documentation | GET itemClasses collection path; ItemClassCode is queryable and returned by the resource | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/fasrp/op-itemclasses-get.html |
| Developer-provided query requirement, 2026-09-24 | Explicit resource-authoring request | itemCategories uses one q expression with uppercase AND between predicates and URL percent-encoding with spaces as %20 | User instruction in the resource-authoring conversation |
| FSCR core.data-loader request policy | Repository execution policy | Every delegated Fusion REST request sends REST-Framework-Version: 9 | core/data-loader/SKILL.md |

Documentation contracts were verified on 2026-09-24. The AND query and %20 space-encoding requirement was supplied by the developer on 2026-09-24 and has not yet been verified against the live environment. Lookup values remain exact task inputs and must be URL-encoded by the delegated REST client before sending the request.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCM.RESOLVE_SOURCE_CATEGORIES | step | 20 | reference_lookup | evaluated->MCM.RESOLVE_TARGET_CATEGORIES | MCM.VALIDATE_CSV_CONTRACT | continue | Evaluate source-category membership for every immutable detail-row context and retain all row findings. |
| MCM.RESOLVE_TARGET_CATEGORIES | step | 30 | reference_lookup | evaluated->MCM.RESOLVE_ROOT_ITEM_CLASSES;not-applicable->MCM.RESOLVE_ROOT_ITEM_CLASSES | MCM.RESOLVE_SOURCE_CATEGORIES | continue | Evaluate every non-ROOT_ICC target category using only its context's target catalog and target category. |
| MCM.RESOLVE_ROOT_ITEM_CLASSES | step | 40 | reference_lookup | evaluated->MCM.AGGREGATE_VALIDATION_OUTCOMES;not-applicable->MCM.AGGREGATE_VALIDATION_OUTCOMES | MCM.RESOLVE_TARGET_CATEGORIES | continue | Evaluate every ROOT_ICC target as an item class using only its context's target category. |
| MCM.AGGREGATE_VALIDATION_OUTCOMES | decision | 50 | evaluate_result | passed->MCM.RETURN_SUCCESS;blocked->RETURN_ISSUES | MCM.RESOLVE_ROOT_ITEM_CLASSES | stop | Aggregate all CSV-contract, source, target, ROOT_ICC, ambiguity, and read-failure findings after every applicable row branch completes. |

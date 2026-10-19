# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required mapping CSV file or column is absent | Stop before any Fusion lookup and identify the missing file or exact column. |
| A mapping-detail CatgMapName has no matching header or has multiple matching headers | Record the detail-row identity and CatgMapName; require exactly one exact mapping-header match. Do not reject repeated child rows for a valid parent header. |
| Source-category lookup returns no result | Record the detail-row identity, CatgMapName, source catalog, and source category; state that the given source category may not belong to the given source catalog. |
| Non-ROOT_ICC target-category lookup returns no result | Record the detail-row identity, CatgMapName, target catalog, and target category; state that the given target category may not belong to the given target catalog. |
| ROOT_ICC item-class lookup returns no result | Record the detail-row identity, CatgMapName, and target category; state that the supplied target category value does not resolve as an item class for ROOT_ICC. |
| A lookup returns multiple results or cannot be read | Record the row-level ambiguity or sanitized transport, authorization, or Fusion API diagnostic. |
| Any row-level validation finding exists | Complete all independent detail-row branches, return every finding together, and block preview, upload, and import. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| INPUT | A required CSV, required column, required catalog/category value, or exact CatgMapName join is missing or ambiguous | Correct the CSV input and restart validation. |
| SOURCE_CATEGORY | SourceCategoryCode does not resolve exactly in its SourceCatalogCode | Correct the source category or catalog; the given source category may not belong to the given source catalog. |
| TARGET_CATEGORY | TargetCategoryCode does not resolve exactly in a non-ROOT_ICC TargetCatalogCode | Correct the target category or catalog; the given target category may not belong to the given target catalog. |
| TARGET_ITEM_CLASS | TargetCategoryCode does not resolve exactly as an item class when TargetCatalogCode is ROOT_ICC | Correct the target category value to an exact item-class code and restart validation. |
| LOOKUP | A read-only lookup is ambiguous or fails to read | Resolve the ambiguity or diagnostic and restart validation. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| CSV contract validation fails | The affected file, row, column, CatgMapName, and corrective action. |
| Source or target lookup fails | The affected catalog code, category value, lookup branch, zero-result or ambiguity state, and corrective action without exposing credentials. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| CSV validation or a category/item-class lookup fails | Do not continue to preview, prepare an import artifact, or submit setup data for the affected row. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCM.RETURN_SUCCESS | terminal | 60 | terminal | none | MCM.AGGREGATE_VALIDATION_OUTCOMES | stop | Every applicable source, target-category, and ROOT_ICC item-class lookup resolves exactly for every mapping-detail row. |
| RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | CSV-contract validation failed directly, or one or more read-only lookup findings were aggregated for Manage Catalog Mappings. |

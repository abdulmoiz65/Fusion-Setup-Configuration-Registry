# Specify Supplier News Content Defaulting Rules

## Defaulting Rules

| Default | When Applied | Override Behavior | What Happens | Resolver |
|---|---|---|---|---|
| Retain existing supplier news content | The supplied SupplierNewsContent is unchanged | A different explicit SupplierNewsContent replaces the retained value through the supplierNewsContent Data Loader REST artifact | Do not prepare a content update for an unchanged value | resolve_supplier_news_content |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | What Happens |
|---|---|---|---|---|---|---|---|---|
| POZ.SNC.APPLY_NO_CHANGE_DEFAULT | step | 20 | apply_default | applied->POZ.SNC.LOOKUP_CURRENT_NEWS | POZ.SNC.VALIDATE_INPUT | stop | After input validation | Retain the existing value when the supplied supplier news content is unchanged |

# Lot Selector Views Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EntityName | Lots | EntityName is omitted for an inventorySearchViews row. | No. Preserve an explicit EntityName. |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LSV.APPLY_ENTITY_DEFAULT | step | 10 | apply_default | applied->LSV.NORMALIZE_INPUT;skipped->LSV.NORMALIZE_INPUT | none | stop | EntityName is omitted or explicitly supplied. |

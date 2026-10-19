# Performance Document Types Defaulting Rules

Apply this task guidance using current target metadata and the declared execution route.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Status | A | A new document type has no supplied status. | Yes | |
| DateFrom | Current date | A new document type has no supplied DateFrom. | Yes | |
| DateTo | 4712-12-31 | A new document type has no supplied DateTo. | Yes | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PERFORMANCE_DOCUMENT_TYPES.DEFAULTS | step | 40 | apply_default | applied->PERFORMANCE_DOCUMENT_TYPES.ENFORCE | PERFORMANCE_DOCUMENT_TYPES.DEPENDENCIES | stop | A new document type omits a documented defaulted field. |

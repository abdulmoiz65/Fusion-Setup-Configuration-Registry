# Inventory Document Output Preferences Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| AttachShippingDocumentFlag | false | The field is blank | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IDOP.APPLY_DEFAULT | step | 30 | apply_default | applied->IDOP.COMPLETE;not_required->IDOP.COMPLETE | IDOP.RESOLVE_LOOKUPS | stop | AttachShippingDocumentFlag is blank or supplied |

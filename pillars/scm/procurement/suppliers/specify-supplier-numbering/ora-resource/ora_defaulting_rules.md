# Specify Supplier Numbering Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| NextSupplierNumber | 10001 | The approved `supplierNumberingInitializeSetup` Data Loader POST establishes a missing row and no replacement next supplier number is supplied | Yes | find_supplier_numbering_row |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SN.APPLY_INITIAL_DEFAULT | step | 62 | apply_default | applied->SN.CREATE_GATE;blocked->SN.HANDLE_ERROR | SN.ENFORCE_CREATE | stop | An initialized row has no requested replacement next supplier number |

# Attachment Category Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ApplicationId | 1 | ApplicationId is not supplied for Product Model | No | |
| ModuleId | 47110F64AC8308E2E040449823C60DB6 | ModuleId is not supplied for Product Model | Yes | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| APPLY_PRODUCT_MODEL_DEFAULTS | step | 20 | apply_default | defaulted->RETURN_SUCCESS;preserved->RETURN_SUCCESS | VALIDATE_ATTACHMENT_CATEGORY_INPUTS | stop | After category availability and input validation pass |

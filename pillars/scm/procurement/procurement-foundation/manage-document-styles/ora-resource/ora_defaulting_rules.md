# Client-Side Defaulting Rules

Apply these local derivations after input validation and before any later Data Loader preparation. They do not inspect Fusion state, invoke a REST endpoint, or replace the downstream business-object contract.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| QuantityPurchaseBasisEnabledFlag | true | Purchase Basis is Quantity | Yes | |
| AmountPurchaseBasisEnabledFlag | true | Purchase Basis is Amount | Yes | |
| LineTypeCode | Copy the supplied Line Type input | A nonblank Line Type input is supplied | Yes | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MDS.APPLY_DEFAULTS | step | 20 | apply_default | completed->MDS.COMPLETE | MDS.VALIDATE_INPUT | stop | A Manage Document Styles record passes local input validation |

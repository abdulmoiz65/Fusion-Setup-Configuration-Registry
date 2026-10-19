# Cost Profiles Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Referenced RMA Cost Code | SO_COST | Always; this is the only supported option | No | |
| Quantity Depletion Method Code | NOT_APPLICABLE | Cost Method Code is PERIODIC_AVERAGE | No | |
| Quantity Depletion Method Code | FIFO | Cost Method Code is not PERIODIC_AVERAGE | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CP.APPLY_REFERENCED_RMA_COST_DEFAULT | step | 27 | apply_default | defaulted->CP.APPLY_QUANTITY_DEPLETION_METHOD_DEFAULT | CP.RESOLVE_REFERENCED_RMA_COST | stop | After the referenced-RMA Meaning is resolved |
| CP.APPLY_QUANTITY_DEPLETION_METHOD_DEFAULT | step | 28 | apply_default | defaulted->CP.RESOLVE_VALUATION_STRUCTURE_ID | CP.APPLY_REFERENCED_RMA_COST_DEFAULT | stop | After Cost Method Code is resolved |

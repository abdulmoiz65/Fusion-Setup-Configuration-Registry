# Defaulting Rules

## Standard Defaults
| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| TaskCode | ZCH_MANAGE_CUSTOMER_HUB_DATA_CLEANSING_LOOKUPS | Export or import | Yes |  |
| Lookup category | standardLookups | Confirmed member | No | resolve_data_cleansing_lookup |
| Mutation fields | Meaning only | System code update | No | resolve_data_cleansing_lookup |
| Import owner | core.data-loader with Task Hook envelope | Import | No |  |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DCL.DEFAULTS | step | 25 | apply_default | applied->DCL.DEPENDENCIES;failure->DCL.ERROR | DCL.LOOKUP | stop | Apply exact task and safe routing defaults. |

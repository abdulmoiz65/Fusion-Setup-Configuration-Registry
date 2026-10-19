# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| TaskCode | ZCH_MANAGE_CUSTOMER_HUB_COMMON_LOOKUPS | Export or import | Yes; exact identity is mandatory |  |
| Lookup category | standardLookups | Confirmed task member | No; stop if current GET disagrees | resolve_customer_hub_common_lookup_type |
| Mutation identity or values | No default | Required value omitted | No; stop |  |
| Import owner | core.data-loader with current Task Hook envelope | Import | No |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CHC.DEFAULTS | step | 25 | apply_default | applied->CHC.DEPENDENCIES;failure->CHC.ERROR | CHC.LOOKUP | stop | Apply only exact task identity and safe routing defaults. |

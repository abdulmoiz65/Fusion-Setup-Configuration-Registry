# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| TaskCode | ZCQ_MANAGE_DATA_QUALITY_LOOKUPS | Export or import | Yes; exact task identity is mandatory |  |
| Lookup category | standardLookups | Confirmed task member | No; stop if current GET disagrees | resolve_data_quality_lookup_type |
| Mutation identity or values | No default | Required value is omitted | No; stop |  |
| Import owner | core.data-loader with current Task Hook envelope | Import | No |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DQL.DEFAULTS | step | 25 | apply_default | applied->DQL.DEPENDENCIES;failure->DQL.ERROR | DQL.LOOKUP | stop | Apply only exact task identity and safe routing defaults. |

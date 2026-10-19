# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| TaskCode | ZCH_MANAGE_CUSTOMER_HUB_LOOKUPS | Export or import | Yes; exact identity is mandatory |  |
| Lookup category | standardLookups | Confirmed task member | No; stop if current GET disagrees | resolve_duplicate_management_lookup |
| System mutation fields | Meaning only | System code update | No | resolve_duplicate_management_lookup |
| Extensible mutation fields | Meaning, Description, DisplaySequence; EnabledFlag and active dates only for proven custom codes | Extensible code update | No | resolve_duplicate_management_lookup |
| Upsert | Disabled | Create or update | No | resolve_duplicate_management_lookup |
| Import owner | core.data-loader with Task Hook envelope | Import | No |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DML.DEFAULTS | step | 25 | apply_default | applied->DML.DEPENDENCIES;failure->DML.ERROR | DML.LOOKUP | stop | Apply exact task and safe routing defaults. |

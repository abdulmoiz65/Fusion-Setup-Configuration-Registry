# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Reference Designator Range Indicator | ORA_NONE (None) | No special-character range behavior is requested | Yes | resolve_rd_range_indicator_lookup_value |
| Quantity Related | Enabled | New engineering or commercial item structures use the setup default | Yes | |
| Enable Lifecycle Validation / LifecycleValidationFlag | 2 (false; unchecked) | No value is supplied. User inputs `false`, `N`, and `No` normalize to this value. | Yes | |
| Use Primary for Expansion | false (unchecked) | No value is supplied | Yes | |
| Internal Name | Display Name | No internal name is supplied | Yes | |
| Description | Empty | No description is supplied | Yes | |

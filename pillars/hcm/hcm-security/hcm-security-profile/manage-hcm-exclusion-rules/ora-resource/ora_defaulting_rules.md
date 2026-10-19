# HCM Exclusion Rules Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Enabled Flag | Y | No value is supplied for a new row | No | |
| Name | Derive from the functional definition | No Name is supplied for a new rule | No | |
| Unavailable optional CSV value | Empty field | An optional exclusion-rule CSV value is not available | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HCMEX.APPLY_DEFAULTS | step | 20 | apply_default | applied->HCMEX.RESOLVE_REFERENCES;skipped->HCMEX.RESOLVE_REFERENCES | HCMEX.VALIDATE_INPUT | stop | Defaults are evaluated for a new HCM exclusion-rule row |

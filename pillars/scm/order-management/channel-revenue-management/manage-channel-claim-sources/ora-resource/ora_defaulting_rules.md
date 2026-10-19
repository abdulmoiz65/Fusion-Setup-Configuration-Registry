# Manage Channel Claim Sources Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EnabledFlag | false | Create parent only and omitted | No | |
| settlementMethods.EnabledFlag | false | Create child only and omitted | No | |
| settlementMethods.DefaultFlag | false | Create child only and omitted | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CJMCS.APPLY_DEFAULTS | step | 6 | apply_default | applied->CJMCS.VALIDATE_CHANGES;unchanged->CJMCS.VALIDATE_CHANGES | CJMCS.VALIDATE_DESIGN | stop | Create applies only omitted documented defaults; create_child applies child defaults only and never defaults parent values; every update returns unchanged and preserves all omitted flags |

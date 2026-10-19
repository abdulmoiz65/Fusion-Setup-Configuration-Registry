# Defaulting rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Include Payroll Time Type | Y | The value is omitted | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| TDL.DDTA.APPLY_DEFAULT | step | 20 | apply_default | defaulted->TDL.DDTA.RESOLVE_LDG;provided->TDL.DDTA.RESOLVE_LDG | TDL.DDTA.VALIDATE_INPUTS | stop | Every validated ESS request |

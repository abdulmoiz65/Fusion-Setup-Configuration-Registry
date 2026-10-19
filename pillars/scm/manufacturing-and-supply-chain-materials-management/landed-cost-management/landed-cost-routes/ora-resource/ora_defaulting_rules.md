# Landed Cost Routes Defaulting Rules

Source: User-supplied Landed Cost Routes rule.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Route availability / InactiveFlag | Active; internally false, translated to N for the stored Data Loader value | The business user does not state an active or inactive status | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LANDED_COST_ROUTES.DEFAULT_INACTIVE_FLAG | step | 20 | apply_default | default-applied->LANDED_COST_ROUTES.RESOLVE_ROUTE_ID;default-failed->RETURN_ISSUES | LANDED_COST_ROUTES.VALIDATE_INPUT | stop | Default an unstated business route availability to Active before preparing a Landed Cost Routes Data Loader request. |

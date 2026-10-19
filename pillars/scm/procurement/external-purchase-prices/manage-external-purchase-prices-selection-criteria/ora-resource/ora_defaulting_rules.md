# Selection Criteria Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| LowestPriceFlag | false | A planned criterion omits the lowest-price preference | No | |

Oracle's REST field definition gives `false` as the default. Apply it only as a planning and review aid when the preference is omitted. When the preference is explicit, take the `not_applicable` path and preserve that value. This resource does not apply the value to Fusion or construct a write request.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPPSEL.APPLY_DEFAULTS | step | 40 | apply_default | applied->EPPSEL.ENFORCE_DESIGN;not_applicable->EPPSEL.ENFORCE_DESIGN;blocked->EPPSEL.HANDLE_ERROR | EPPSEL.CHECK_DEPENDENCIES | stop | Reviewing a planned or resolved criterion; apply false only when LowestPriceFlag is omitted |

## Oracle Source

- [Oracle Procurement 26D: REST endpoints](https://docs.oracle.com/en/cloud/saas/procurement/26d/fapra/rest-endpoints.html) — current selection-criteria resource path.
- [Oracle Procurement 25D: Get all selection criteria](https://docs.oracle.com/en/cloud/saas/procurement/25d/fapra/op-externalpurchasepricesselectioncriteria-get.html) — available field detail states that `LowestPriceFlag` is Boolean and defaults to `false`.

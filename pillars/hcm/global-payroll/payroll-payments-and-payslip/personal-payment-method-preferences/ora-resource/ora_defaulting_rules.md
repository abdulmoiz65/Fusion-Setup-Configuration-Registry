# Personal Payment Method Preferences Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Payment amount type | B (Both) | No amount type is selected | Yes | |

The Oracle functional guidance states that the Payment Amount Type system default is Both. The supplied source does not document defaults for any other REST attribute; do not invent them.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PPMP.APPLY_DEFAULTS | step | 7 | apply_default | applied->PPMP.ENFORCE_DESIGN | none | stop | A documented default applies after its selected read-only branch succeeds |

## Sources

- Oracle Fusion Cloud HCM, Configure Payment Method Preferences: https://docs.oracle.com/en/cloud/saas/human-resources/25a/faipb/configure-payment-method-preferences.html

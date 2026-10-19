# Manage Resource Role Descriptive Flexfields Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Context value source | Context codes | No context value set is specified | Yes |  |
| Context usage | Optional | A descriptive flexfield is configured without a context requirement | Yes |  |

## Defaulting Rules

When no value set is specified for a context segment, the permitted context
values are the configured context codes. Do not apply a segment initial value,
BI label, display property, or context requirement unless the requester has
supplied it or the approved DFF configuration provides it.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRRDFF.APPLY_DEFAULTS | step | 2 | apply_default | applied->MRRDFF.DESIGN_GUARD;not-applicable->MRRDFF.DESIGN_GUARD | MRRDFF.VALIDATE_INPUT | stop | A permitted context default applies |

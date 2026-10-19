# Defaulting Rules

## Defaults

| Field(s) | Default value | Applies when | Explicit request | Handling |
|---|---|---|---|---|
| AP_TERM_HEADER.EnabledFlag | `Y` | Create a payment-term header and the request omits or leaves EnabledFlag blank | Explicit value wins | Apply as an explicit candidate value |
| AP_TERM_HEADER.Type | `STD` | Create a payment-term header and the request omits or leaves Type blank | Only an explicit `STD` value is accepted | Apply as an explicit candidate value; reject every other nonblank value |
| AP_TERM_HEADER.StartDateActive | Package-builder system date, serialized `YYYY/MM/DD` | Create a payment-term header and the request omits or leaves StartDateActive blank | Explicit value wins | Apply as an explicit candidate value |

## Defaulting Boundary

These defaults are applied by the offline adapter as explicit candidate values
and recorded in `explicitDefaults`; they do not depend on UI, REST, or FSM-side
default application. `StartDateActive` uses the package-builder system date at
normalization time. Type is constrained to `STD`; an explicit nonblank Type
must therefore also be `STD`.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DEFAULT.APPLY | step | 50 | apply_default | success->DESIGN.ENFORCE | LOOKUP.SET | stop | A new AP_TERM_HEADER omits EnabledFlag, Type, or StartDateActive |

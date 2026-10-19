# Manage Channel Claim Reasons Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| BuySideFlag | false | BuySideFlag is omitted from a create candidate | No | |
| SellSideFlag | false | SellSideFlag is omitted from a create candidate | No | |

No default is assumed for ClaimReason, ClaimReasonCode, SetCode, SetName, dates, or description.

For updates, apply no defaults at all. Omitted fields remain unchanged; never add false side flags, today's date, empty descriptions, or current values to fill an update payload. The defaulting node returns unchanged for every update and for a create with no missing defaulted fields.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CJMCR.APPLY_DOCUMENTED_DEFAULTS | step | 4 | apply_default | applied->CJMCR.FIND_BY_CODE;unchanged->CJMCR.FIND_BY_CODE | CJMCR.FIND_REFERENCE_DATA_SET | stop | Apply documented defaults only to create candidates; return unchanged for updates or when no create default applies |

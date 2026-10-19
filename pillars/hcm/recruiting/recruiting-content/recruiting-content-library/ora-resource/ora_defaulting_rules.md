# Recruiting Content Library Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| CaptureInteraction | N | Importing a description record when the task-supported source applies the documented default. | No | |
| VersionStartDate seconds | 00 | A user supplies VersionStartDate as yyyy/MM/dd HH:mm. Append :00 once to produce the base serialized import format yyyy/MM/dd HH:mm:ss; an optional .fffffffff fractional-second suffix remains valid when supplied in a correctly formatted value. | No | |
| VersionStartDate | Current timestamp explicitly formatted as yyyy/MM/dd HH:mm:ss and retained as an opaque string | A requester asks for a description version to start immediately. Write the same canonical value to the description-version and description-version translation CSVs; do not parse, coerce, or re-serialize it. | No | |
| IsFileBased | true for ORA_OFFER_LETTER_TEMPLATE and ORA_PROV_OFFER_LETTER_TEMPLATE; otherwise false | Importing a description record. Derive the value from DescriptionTypeCode; do not ask the user to provide it. | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RCL.DEFAULT | step | 40 | apply_default | applied->RCL.DESIGN | RCL.READINESS | stop | A validated description record uses the documented CaptureInteraction default, a user supplies a minute-precision VersionStartDate, a requester asks for an immediate version start, or IsFileBased is derived from DescriptionTypeCode. |

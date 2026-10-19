# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| limit | 100 | User omits limit for the public documented collection GET | No | |
| offset | 0 | User omits offset for the public documented collection GET | No | |
| active | true | User explicitly requests enablement and does not provide active | No | |
| active | false | User explicitly requests a disabled create or update | No | |
| timeStart | 00:00 | User explicitly states 12AM | No | |
| timeEnd | 12:00 | User explicitly states 12PM | No | |

`isAllDay` is a response-only field for this direct REST contract and has no
workbook input or write-payload default. Design-evidence fields have no
execution defaults and are never part of the Time Slots write payload.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TS.DEFAULTS | step | 3 | apply_default | ready->TS.LOOKUP;blocked->TS.DESIGN_BLOCKED | TS.DEPENDENCIES | stop | Time Slots defaults or time normalization are required before lookup and design enforcement. |

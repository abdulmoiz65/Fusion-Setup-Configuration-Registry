# Time Allocations Defaulting Rules

## Source Basis

- Developer-provided Time Allocation UI Skeleton.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Effective Start Date | Current Date | A start date is not supplied | Yes | |
| Effective End Date | 12/31/4712 | Always; the field is read-only | No | |
| Source Processing Sequence | Source-table row number | A Source row is added without a processing sequence | Yes | |
| Hours Processing Sequence | Hours-table row number | A hours row is added without a processing sequence | Yes | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TAL.APPLY_DEFAULTS | step | 20 | apply_default | defaulted->TAL.ENFORCE_DESIGN;not_applicable->TAL.ENFORCE_DESIGN | TAL.VALIDATE_INPUT | stop | A valid Time Allocations request is prepared |

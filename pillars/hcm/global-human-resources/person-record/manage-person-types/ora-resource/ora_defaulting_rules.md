# Manage Person Types Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Person Types. This file does not own input validation, lookup mechanics,
design policy, payload construction, or execution routing.

## Defaulting Precedence

| Priority | Condition | Required Action | Outcome |
|---|---|---|---|
| 1 | A valid explicit value is supplied and user override is allowed | Preserve the supplied value | preserved |
| 2 | An edit omits a field that must retain its current value | Preserve the freshly read current value | preserved |
| 3 | Exactly one Standard Defaults row applies | Apply that default | applied |
| 4 | No defaulting or preservation rule applies | Make no change | not_required |
| 5 | A required resolver is unresolved, ambiguous, or failed | Apply no value and stop | blocked |
| 6 | Multiple conflicting default rows apply to the same field | Apply no value and stop | blocked |
| 7 | A supplied value conflicts with a non-overridable default | Apply no value and stop | blocked |

## Standard Defaults

| Field | Default Value | Applies When | Can User Override? | Resolver | If Unavailable or Invalid |
|---|---|---|---|---|---|

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Operation | A mutation is not explicit | Do not infer it; exploratory intent may remain read-only | not_required |
| Omitted edit value | An edit omits an existing reviewed XLSX value | Preserve the fresh reviewed value | preserved |
| Effective end date | The value is omitted | Do not default it; render a stored 4712-12-31 as End Of Time only for presentation | not_required |
| Identity, reference, or runtime ID | Current resolution succeeds | Preserve it only for the current run; never reuse a prior value | preserved |
| Identity, reference, or runtime ID | Current resolution fails | Apply no value and stop | blocked |
| Approval | Exact current approval is present | Preserve it only for the approved immutable preview | preserved |
| Approval | Exact current approval is absent | Never infer it from authentication or prior activity | blocked |
| Source data | The source is missing, stale, or ambiguous | Stop preparation; do not create an inferred mapping | blocked |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PT.DEFAULTS | decision | 4 | apply_default | applied->PT.ENFORCE;preserved->PT.ENFORCE;not_required->PT.ENFORCE;blocked->PT.ERROR | PT.READ | stop | After validation, current-state reads, and required resolvers are complete |

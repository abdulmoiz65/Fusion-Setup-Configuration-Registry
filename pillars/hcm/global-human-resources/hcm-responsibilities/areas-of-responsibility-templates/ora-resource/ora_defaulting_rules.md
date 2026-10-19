# Areas of Responsibility Templates Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Areas of Responsibility Templates. This file does not own input validation,
lookup mechanics, design policy, payload construction, or execution routing.

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
| List status | Active | No status filter is supplied | Yes |  | Block when Active is not supported by the current registered object |
| List limit | 25 | Every collection page | Yes |  | Block an explicit unbounded or invalid limit |
| List offset | 0 | The initial collection page omits offset | No |  | Block when the initial offset is invalid |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Omitted edit value | An edit omits an existing value | Preserve the fresh current value | preserved |
| Template identity, mutation field, scope, criterion, representative, date, or approval | The value is omitted | Never infer or default it | not_required |
| Explicit validated list value | A supported bounded value is supplied | Preserve it instead of applying the list default | preserved |
| Registered-object mismatch | A proposed value is unsupported | Stop and report catalog mismatch; do not substitute another value | blocked |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AORT.DEFAULTS | decision | 5 | apply_default | applied->AORT.ENFORCE;preserved->AORT.ENFORCE;not_required->AORT.ENFORCE;blocked->AORT.ERROR | AORT.READ | stop | After validation, current-state reads, and required resolvers are complete |

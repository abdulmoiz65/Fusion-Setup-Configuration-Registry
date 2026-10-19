# Manage Legislative Data Groups Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Legislative Data Groups. This file does not own input validation, lookup
mechanics, design policy, payload construction, or execution routing.

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
| Omitted edit value | An edit omits an existing value | Preserve the fresh current value | preserved |
| Legislation | The value is omitted | Never infer it from a display label; require exactly one resolved legislation when mandatory | not_required |
| Explicit resolved legislation | A legislation resolves exactly | Preserve the resolved stored value | preserved |
| Zap delete | A delete is requested | Do not default dates, country, currency, child rows, EFF rows, or source-system keys; retain only the fresh internal LegislativeDataGroupId locator | not_required |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LDG.DEFAULTS | decision | 5 | apply_default | applied->LDG.DESIGN;preserved->LDG.DESIGN;not_required->LDG.DESIGN;blocked->LDG.ERROR | LDG.DEPENDENCIES | stop | After validation, current-state reads, and required resolvers are complete |

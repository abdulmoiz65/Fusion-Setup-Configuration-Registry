# Manage Action Reasons Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Action Reasons. This file does not own input validation, lookup
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
| Effective end date | Registered-object system End-of-Time default | A standalone create omits the end date and the registered object confirms support | Yes |  | Block when the registered object does not confirm the default and no explicit supported value is supplied |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Operation | A mutation is requested | Never infer the mutation; normalize only explicit intent | not_required |
| Omitted edit value | An edit omits an existing value | Preserve the fresh current value; absence is not deletion | preserved |
| Action, Country, role, or association | A usage association omits the value | Do not infer it; resolve only an explicitly supplied value | not_required |
| Association policy | An Action Reason association is requested | Associate only after both the Action and Action Reason are available; stop when either object is unavailable | blocked |
| Unsupported default | The registered object does not support the proposed value | Do not substitute another value | blocked |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AR.DEFAULTS | decision | 5 | apply_default | applied->AR.ENFORCE;preserved->AR.ENFORCE;not_required->AR.ENFORCE;blocked->AR.ERROR | AR.READ | stop | After validation, current-state reads, and required resolvers are complete |

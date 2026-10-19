# Manage Actions Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Actions. This file does not own input validation, lookup mechanics,
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
| Registered mapping shape | Current registered-object-supported mapping shape | An action-reason role mapping is prepared | No |  | Block when the current registered mapping shape is unavailable |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Operation | A mutation is requested | Never infer the mutation; normalize only explicit intent | not_required |
| Effective end date or Country | The value is omitted | Do not infer or default the value | not_required |
| Omitted action or association value | An edit omits an existing value | Preserve the fresh current value; absence is not deletion | preserved |
| Type, ViewInstanceName, generated ID, or GroupingKey | An action-reason role mapping is prepared | Do not default these values | not_required |
| Action policy | An Action Reason association is requested | Require the Action Reason's separate configuration and one Action Type | blocked |
| Unsupported default | The registered object does not support the proposed value | Do not substitute another value | blocked |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACT.DEFAULTS | decision | 5 | apply_default | applied->ACT.ENFORCE;preserved->ACT.ENFORCE;not_required->ACT.ENFORCE;blocked->ACT.ERROR | ACT.READ | stop | After validation, current-state reads, and required resolvers are complete |

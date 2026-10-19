# Manage Assignment Status Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Assignment Status. This file does not own input validation, lookup
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
| DefaultFlag | Stored code for the meaning No in the YES_NO Common Lookup | Create omits DefaultFlag | Yes | resolve_default_flag | Block when exactly one enabled compatible value cannot be resolved |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Omitted edit field | An edit omits an exported value | Preserve the fresh exported value; absence is not a change request | preserved |
| Status classification or legislation | The value is omitted | Never infer it from a display label | not_required |
| Explicit valid DefaultFlag | Create or edit supplies the value | Preserve the exact resolved stored value | preserved |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AS.DEFAULTS | decision | 4 | apply_default | applied->AS.ENFORCE;preserved->AS.ENFORCE;not_required->AS.ENFORCE;blocked->AS.ERROR | AS.READ | stop | After validation, current-state reads, and required resolvers are complete |

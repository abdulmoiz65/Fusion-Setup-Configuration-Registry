# Manage Person Name Styles Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Person Name Styles. This file does not own input validation, lookup
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
| Generated parent and child IDs | Blank | Create rows | No |  | Block when the current contract does not confirm Fusion-generated identifiers |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| LegislationCode | The value is omitted | Never infer a country or legislation from the style name | not_required |
| Omitted edit value or translation | An edit omits an existing exported value | Preserve the fresh exported value; absence is not removal or addition | preserved |
| Prompt | A create or edit supplies a prompt | Preserve the supplied value and verify the stored result because Fusion can normalize it | preserved |
| Prompt | The value is omitted | Never infer or default it | not_required |
| Response-generated ID | Every create | Never reuse an ID from a prior response | not_required |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PNS.DEFAULTS | decision | 4 | apply_default | applied->PNS.ENFORCE;preserved->PNS.ENFORCE;not_required->PNS.ENFORCE;blocked->PNS.ERROR | PNS.READ | stop | After validation, current-state reads, and required resolvers are complete |

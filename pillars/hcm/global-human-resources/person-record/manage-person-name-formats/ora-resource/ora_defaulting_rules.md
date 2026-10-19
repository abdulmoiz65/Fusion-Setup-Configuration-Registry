# Manage Person Name Formats Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Person Name Formats. This file does not own input validation, lookup
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
| Omitted edit value | An edit omits an existing reviewed XLSX value | Preserve the fresh reviewed value | preserved |
| Business decision, identifier, effective date, reference, unsupported value, or approval | The value is omitted | Never infer or default it | not_required |
| Source data | The source is missing, stale, or ambiguous | Stop preparation and require current unambiguous source data | blocked |
| Format versus style behavior | Every request | Use formats only for display sequence and styles only for captured components | not_required |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PNF.DEFAULTS | decision | 4 | apply_default | applied->PNF.ENFORCE;preserved->PNF.ENFORCE;not_required->PNF.ENFORCE;blocked->PNF.ERROR | PNF.READ | stop | After validation, current-state reads, and required resolvers are complete |

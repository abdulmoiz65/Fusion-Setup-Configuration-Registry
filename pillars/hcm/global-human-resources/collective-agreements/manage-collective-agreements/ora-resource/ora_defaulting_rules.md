# Manage Collective Agreements Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Collective Agreements. This file does not own input validation, lookup
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
| Effective date | Current task-context date | A read request omits its date | Yes |  | Block when the current task-context date is unavailable or invalid |
| EFF_CATEGORY_CODE | PER_COL_EIT | A collectiveAgreementsEFF row is authored | No |  | Block a conflicting value |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Operation | A mutation is requested | Never infer the mutation; normalize only explicit intent | not_required |
| Create, edit, or delete effective date | The mutation omits its effective date | Do not apply the read-only current-date default | blocked |
| Status | A status is omitted | Use only an explicit value or a registered-object default; otherwise apply no value | not_required |
| Country, legislation, or reference | A value is omitted | Do not infer it from another agreement; omit it only when the registered object permits omission | not_required |
| Effective end date | An end date is omitted | Do not send a synthetic end date | not_required |
| Omitted edit field or row | An edit omits an existing value or row | Preserve the fresh current value; absence is not deletion | preserved |
| Name or identification code | Every operation | Preserve exact explicit values; never generate them from a sample | preserved |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CA.DEFAULTS | decision | 5 | apply_default | applied->CA.ENFORCE;preserved->CA.ENFORCE;not_required->CA.ENFORCE;blocked->CA.ERROR | CA.READ | stop | After validation, current-state reads, and required resolvers are complete |

## Date-effective Split Preservation

Never default a split, predecessor, successor, or end date. For a bounded middle-split purge, set the retained predecessor EffectiveEndDate only to the final selected split former end date, preserve every other split boundary, and serialize both DAT dates as `YYYY/MM/DD`.


## Corrected HDL Split-Deletion Contract (Supersedes Earlier Examples)

Use exactly one `SET PURGE_FUTURE_CHANGES Y` directive and one retained-predecessor `MERGE` row, with DAT dates in `YYYY/MM/DD`. The retained predecessor start and final selected end bound the contiguous removal. Reject HDL DELETE, mixed instructions, ISO DAT dates, first/only split deletion, and any REST mutation.

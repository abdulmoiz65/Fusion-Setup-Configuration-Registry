# Manage HCM Position Hierarchy Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage HCM Position Hierarchy. This file does not own input validation, lookup
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
| View as-of date | Today's date in YYYY-MM-DD | view_hierarchy has no explicit date | Yes |  | Block when the task-context date is unavailable or invalid |
| Relationship effective end date | Earliest effective-row end date shared by the child and parent; display 4712/12/31 as End Of Time | Creating or changing a relationship omits a shorter valid end date | Yes | resolve_position_hierarchy_members | Block when the shared effective range cannot be resolved exactly |
| PositionHierarchyId and GUID | Blank when confirmed user keys are used | Every Position Hierarchy workbook using confirmed user keys | No | inspect_position_hierarchy_loader_contract | Block when the loader contract does not confirm that the identifiers may be blank |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Mutation effective date | Any mutation omits the date | Never infer or default it | blocked |
| Move mode | move_position omits the mode | Never infer or default it | blocked |
| SourceSystemOwner and SourceSystemId | Neither source-key value is supplied | Do not derive either value; apply neither value | not_required |
| SourceSystemOwner and SourceSystemId | Both source-key values are supplied and valid | Preserve the explicit pair | preserved |
| SourceSystemOwner and SourceSystemId | Only one source-key value is supplied | Do not default the other value; require an explicit valid pair | blocked |
| Omitted edit value | An edit omits an existing relationship value | Preserve the fresh current value | preserved |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POSH.DEFAULTS | decision | 2 | apply_default | applied->POSH.POSITION_ROUTE;preserved->POSH.POSITION_ROUTE;not_required->POSH.POSITION_ROUTE;blocked->POSH.ERROR | POSH.INPUT | stop | After validation, current-state reads, and required resolvers are complete |

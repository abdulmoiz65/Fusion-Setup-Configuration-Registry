# Manage Locations Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Locations. This file does not own input validation, lookup mechanics,
design policy, payload construction, or execution routing.

## Defaulting Precedence

| Priority | Condition | Required Action | Outcome |
|---|---|---|---|
| 1 | A valid explicit value is supplied and user override is allowed | Preserve the supplied value | preserved |
| 2 | An edit omits a field that must retain its current value and no Standard Defaults row applies | Preserve the freshly read current value | preserved |
| 3 | Exactly one Standard Defaults row applies | Apply that default | applied |
| 4 | No defaulting or preservation rule applies | Make no change | not_required |
| 5 | A required resolver is unresolved, ambiguous, or failed | Apply no value and stop | blocked |
| 6 | Multiple conflicting default rows apply to the same field | Apply no value and stop | blocked |
| 7 | A supplied value conflicts with a non-overridable default | Apply no value and stop | blocked |

## Metadata Default Gate

Before applying any Standard Defaults row, confirm that current operation-specific Data Loader metadata exposes the field and confirms the value as an accepted default or required constant. If an optional default is not confirmed, omit the field; if current metadata marks the field required and no valid value resolves, ask only for that required value and block authoring. A fixed technical discriminator may be retained only when this task contract requires it to identify the exact business-object section; never promote an example value to a default.

## Standard Defaults

| Field | Default Value | Applies When | Can User Override? | Resolver | If Unavailable or Invalid |
|---|---|---|---|---|---|
| ActiveStatus | A | An included Location row omits ActiveStatus | Yes |  | Block when an explicit value is invalid |
| SetCode | COMMON | An included Location row omits both SetId and SetCode | Yes |  | Block when an explicit set is invalid |
| EFF_CATEGORY_CODE | HCM_LOC | A LocationExtraInfo row is authored | No |  | Block a conflicting value |
| EFF_CATEGORY_CODE | HCM_LOC_LEG | A LocationLegislative row is authored | No |  | Block a conflicting value |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Omitted edit value | An edit omits an existing value and no Standard Defaults row applies | Preserve the fresh current value | preserved |
| ActionReasonCode on date-effective edit | An edit uses a new EffectiveStartDate | Never preserve, copy, or default the prior or create reason. Leave it absent unless the user explicitly supplies an update reason; resolve only that supplied value. | not_required |
| Date-effective delete range | A delete is requested | Never default from a requested date alone; derive the retained start and deletion end only from complete fresh LocationHistoryDef evidence | blocked |
| Country-specific MAIN address field | A required address value is missing | Do not default it; require the exact value established by resolve_location_address_contract | blocked |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LOC.DEFAULTS | decision | 6 | apply_default | applied->LOC.DESIGN;preserved->LOC.DESIGN;not_required->LOC.DESIGN;blocked->LOC.ERROR | LOC.DEPENDENCIES | stop | After validation, current-state reads, and required resolvers are complete |

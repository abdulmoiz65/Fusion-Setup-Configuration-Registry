# Manage Positions Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Positions. This file does not own input validation, lookup mechanics,
design policy, payload construction, or execution routing.

Shared reuse: `core.data-loader` owns loader artifact and execution behavior; these defaults apply before its handoff.

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
| ActiveStatus | A | An included Position row omits ActiveStatus | Yes |  | Block when an explicit value is invalid |
| EffectiveStartDate | Target Position EffectiveStartDate | A child row is copied to a new Position | Yes, when the supplied date remains within the target Position range |  | Block a child date before the target Position start or after its end |
| DateEvaluated | Later of the source DateEvaluated and target Position EffectiveStartDate | A PositionEvaluation row is copied | Yes, when the supplied date remains within the target Position range |  | Block a date before the target Position start or after its end |
| EFF_CATEGORY_CODE | POS_EIT | A PositionExtraInfo row is authored | No |  | Block a conflicting value |
| EFF_CATEGORY_CODE | POS_LEG | A PositionLegislative row is authored | No |  | Block a conflicting value |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Omitted edit value | An edit omits an existing value and no Standard Defaults row applies | Preserve the fresh value read from the applicable Position section | preserved |
| BusinessUnitName, DepartmentName, JobCode, or LocationCode | The reference is omitted | Never infer it; every supplied value must resolve exactly through its documented resolver | not_required |
| PositionCode | Automatic code generation is confirmed and the value is omitted | Leave it omitted for the loader to generate | not_required |
| ActionReasonCode | An effective-dated edit or update is authored | Do not copy, default, or preserve a create/correct action reason. Leave it absent unless the user explicitly supplies an update-appropriate action reason. | not_required |
| Explicit resolved workforce reference | A supplied reference resolves exactly | Preserve the resolved value | preserved |
| Omitted child section or field | The user did not request that child section or field | Do not add it and do not copy a value from another section | not_required |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POS.DEFAULTS | decision | 11 | apply_default | applied->POS.DESIGN;preserved->POS.DESIGN;not_required->POS.DESIGN;blocked->POS.ERROR | POS.DEPENDENCIES | stop | After validation, current-state reads, and required resolvers are complete |

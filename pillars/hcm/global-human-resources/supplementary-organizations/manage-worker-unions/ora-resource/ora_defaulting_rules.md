# Manage Worker Unions Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Worker Unions. This file does not own input validation, lookup mechanics,
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

## Metadata Default Gate

Before applying any Standard Defaults row, confirm that current operation-specific Data Loader metadata exposes the field and confirms the value as an accepted default or required constant. If an optional default is not confirmed, omit the field; if current metadata marks the field required and no valid value resolves, ask only for that required value and block authoring. A fixed technical discriminator may be retained only when this task contract requires it to identify the exact business-object section; never promote an example value to a default.

## Standard Defaults

| Field | Default Value | Applies When | Can User Override? | Resolver | If Unavailable or Invalid |
|---|---|---|---|---|---|
| ClassificationName | Worker Union | An Organization, OrgUnitClassification, or OrgInformation row is built | No |  | Block when ClassificationCode is not ORA_PER_UNION |
| EFF_CATEGORY_CODE | ORA_PER_UNION | An OrgInformation row is built | No | resolve_worker_union_classification | Block when the resolved classification is not ORA_PER_UNION |
| Status | A | An included OrgUnitClassification row omits Status | Yes |  | Block when an explicit value is invalid |
| EffectiveEndDate | 4712-12-31 | A Worker Union is created | No |  | Apply as the open-ended internal date; never request it from the user. |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| EffectiveStartDate | A mutation omits the date | Require an explicit supported date | blocked |
| EffectiveEndDate | A Worker Union create omits the date | Apply the open-ended default internally; do not ask the user for it | applied |
| Set | A Set is supplied | Treat Set as not applicable and reject the supplied value | blocked |
| Set | A Set is omitted | Apply no value because Set is not applicable | not_required |
| Omitted edit field | An edit omits an existing value and no Standard Defaults row applies | Preserve the fresh current value; change only explicitly requested fields | preserved |
| Additional Information context, segment, or code | The requested value and its metadata resolve exactly | Preserve the resolved typed value | preserved |
| Additional Information context, segment, or code | A required value or its metadata is missing, ambiguous, or invalid | Apply no value and stop; never infer it | blocked |
| Associated Bargaining Unit | The association is omitted | Never infer the association | not_required |
| Date-effective split deletion range | delete-effective-split is requested | Never default the retained EffectiveStartDate or deletion EffectiveEndDate; use only freshly resolved boundaries and omit non-key attributes | not_required |
| Classification, context, segment, value-set value, or unrelated Organization child row | The value is omitted | Never infer or default it | not_required |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UNION.DEFAULTS | decision | 7 | apply_default | applied->UNION.DESIGN;preserved->UNION.DESIGN;not_required->UNION.DESIGN;blocked->UNION.ERROR | UNION.DEPENDENCIES | stop | After validation, current-state reads, and required resolvers are complete |

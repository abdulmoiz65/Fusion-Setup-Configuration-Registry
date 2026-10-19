# Manage Enterprise HCM Information Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Enterprise HCM Information. This file does not own input validation,
lookup mechanics, design policy, payload construction, or execution routing.

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
| EFF_CATEGORY_CODE | ENTERPRISE | An OrgInformation row is built | No | resolve_enterprise_classification | Block when the resolved classification is not ENTERPRISE |
| Status | A | An included OrgUnitClassification row omits Status | Yes |  | Block when an explicit value is invalid |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Omitted edit value | An edit omits an existing value and no Standard Defaults row applies | Preserve the fresh current value | preserved |
| Existing OrgInformation identity or SequenceNumber | An existing context row is edited | Preserve the freshly read value; never invent or default it | preserved |
| Enterprise context or segment value | The value is omitted | Never infer it; require the configured value or one exact resolved value-set value when mandatory | not_required |
| Explicit resolved value | A context or segment value resolves exactly | Preserve the resolved value | preserved |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ENT.DEFAULTS | decision | 9 | apply_default | applied->ENT.DESIGN;preserved->ENT.DESIGN;not_required->ENT.DESIGN;blocked->ENT.ERROR | ENT.DEPENDENCIES | stop | After validation, current-state reads, and required resolvers are complete |

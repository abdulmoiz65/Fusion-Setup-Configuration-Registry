# Manage Disability Organizations Defaulting Rules

## Purpose

Defines safe defaults and preservation rules for Manage Disability Organizations.

## Defaulting Precedence

| Priority | Condition | Required Action | Outcome |
|---|---|---|---|
| 1 | A valid explicit value is supplied and override is allowed | Preserve it | preserved |
| 2 | An edit omits an existing value | Preserve the fresh value | preserved |
| 3 | Exactly one standard default applies | Apply it | applied |
| 4 | No rule applies | Make no change | not_required |
| 5 | Required evidence is unresolved or conflicting | Apply no value and stop | blocked |

## Metadata Default Gate

Before applying any Standard Defaults row, confirm that current operation-specific Data Loader metadata exposes the field and confirms the value as an accepted default or required constant. If an optional default is not confirmed, omit the field; if current metadata marks the field required and no valid value resolves, ask only for that required value and block authoring. A fixed technical discriminator may be retained only when this task contract requires it to identify the exact business-object section; never promote an example value to a default.

## Standard Defaults

| Field | Default Value | Applies When | Can User Override? | Resolver | If Unavailable or Invalid |
|---|---|---|---|---|---|
| ClassificationName | Disability Organization | An Organization, OrgUnitClassification, or OrgInformation row is built | No |  | Block when ClassificationCode is not HCM_DISABILITY_ORGANIZATION |
| EFF_CATEGORY_CODE | HCM_DISABILITY_ORGANIZATION | An OrgInformation row is built | No |  | Block when the loader contract does not support the classification category |
| Status | A | An included OrgUnitClassification row omits Status | Yes |  | Block when an explicit value is invalid |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Omitted edit value | edit omits an existing value and no Standard Defaults row applies | Preserve the fresh value | preserved |
| Related organization value | The value is omitted | Do not infer it | not_required |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DISORG.DEFAULTS | decision | 7 | apply_default | applied->DISORG.DESIGN;preserved->DISORG.DESIGN;not_required->DISORG.DESIGN;blocked->DISORG.ERROR | DISORG.DEPENDENCIES | stop | After validation and dependency resolution |

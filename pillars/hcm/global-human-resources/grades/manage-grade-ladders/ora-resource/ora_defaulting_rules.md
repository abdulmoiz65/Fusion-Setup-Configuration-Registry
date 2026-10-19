# Manage Grade Ladders Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Grade Ladders. This file does not own input validation, lookup mechanics,
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
| ActiveStatus | A | An included GradeLadder row omits ActiveStatus | Yes |  | Block when an explicit value is invalid |
| GradeSetCode | COMMON | Create omits Grade Set | Yes |  | Block when an explicit value is invalid |
| GradeType | STEP | Every create | No |  | Block an explicit different value |
| CurrencyCode | Resolved LDG DefaultCurrencyCode | A new rate omits currency | Yes | resolve_grade_ladder_currency | Block when the LDG currency cannot be resolved or an explicit value is invalid |
| AnnualizationFactor | ANNUAL=1, QUARTER=4, MONTHLY=12, HOURLY=2080 | A new rate resolves one of these frequencies and omits the factor | Yes | resolve_grade_ladder_lookup_codes | Block when frequency is unresolved or has no listed factor; reset and recalculate after a frequency change |
| Grade placement | End of ladder in supplied order | Placement is omitted | Yes |  | Block when the supplied grade order is unavailable or ambiguous |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| UpdateSalaryFlag | Every request | Do not default, preserve, or add it to the loader source | not_required |
| Omitted edit value | An edit omits an existing value and no Standard Defaults row applies | Preserve the fresh current value | preserved |
| Date-effective split deletion range | delete-effective-split is requested | Never default the retained EffectiveStartDate or deletion EffectiveEndDate; use only freshly resolved boundaries and omit non-key attributes | not_required |
| Rate amount or Grade | The value is omitted | Never infer or default it | not_required |
| Explicit valid value | A supported value is supplied | Preserve it after validation | preserved |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GLAD.DEFAULTS | decision | 4 | apply_default | applied->GLAD.ENFORCE;preserved->GLAD.ENFORCE;not_required->GLAD.ENFORCE;blocked->GLAD.ERROR | GLAD.READ | stop | After validation, current-state reads, and required resolvers are complete |

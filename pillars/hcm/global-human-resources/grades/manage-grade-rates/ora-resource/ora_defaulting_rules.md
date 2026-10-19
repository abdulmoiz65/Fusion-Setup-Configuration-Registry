# Manage Grade Rates Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Grade Rates. This file does not own input validation, lookup mechanics,
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
| AnnualizationFactor | ANNUAL=1, MONTHLY=12, HOURLY=2080 | Create or frequency change omits the factor after exact frequency resolution | Yes | resolve_grade_rate_lookup_codes | Block when frequency is unresolved or has no listed factor; reset and recalculate after a frequency change |
| ActiveStatus | A | An included GradeRate row omits ActiveStatus | Yes |  | Block when an explicit value is invalid |
| CurrencyCode | Resolved LDG DefaultCurrencyCode | Create omits currency | Yes | resolve_grade_rate_ldg | Block when currency is omitted and the LDG default cannot be resolved |
| MidValue | Arithmetic midpoint of Minimum and Maximum, rounded to two decimal places | Both bounds are numeric and MidValue is omitted | Yes |  | Make no change when either bound is omitted; block when a supplied bound is nonnumeric or the midpoint cannot be calculated |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Omitted edit value | An edit omits an existing value and no Standard Defaults row applies | Preserve the fresh current value, including LegislativeDataGroupId | preserved |
| LegislativeDataGroup, LegislativeDataGroupId, RateType, RateFrequency, GradeRateName, Value, or grade | The value is omitted | Never infer or default it | not_required |
| Explicit valid value | A supported value is supplied | Preserve it after validation | preserved |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GRAT.DEFAULTS | decision | 4 | apply_default | applied->GRAT.ENFORCE;preserved->GRAT.ENFORCE;not_required->GRAT.ENFORCE;blocked->GRAT.ERROR | GRAT.READ | stop | After validation, current-state reads, and required resolvers are complete |

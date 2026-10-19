# Manage Job Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Job. This file does not own input validation, lookup mechanics, design
policy, payload construction, or execution routing.

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
| ActiveStatus | A | An included Job row omits ActiveStatus | Yes |  | Block when an explicit value is invalid |
| SetCode | COMMON | An included Job row omits both SetId and SetCode | Yes |  | Block when an explicit set is invalid |
| EFF_CATEGORY_CODE | JOB_LEG | A JobLegislative row is included because that object is modified | No |  | Block when the workbook contract does not support the JobLegislative category |
| EFF_CATEGORY_CODE | JOB_EIT | A JobExtraInfo row is included because that object is modified | No |  | Block when the workbook contract does not support the JobExtraInfo category |
| Included Job EFF child identity fields | Resolved base-Job linkage, context identity, effective boundary, and fixed/default values declared by the current child template and describe | A new Job includes JobLegislative or JobExtraInfo | No | read_job_eff_context | Block when a required identity value is unresolved or the metadata does not confirm a proposed default |
| StandardWorkingHours | Enterprise Work Day Information value | Create omits StandardWorkingHours and current metadata confirms the field as required or defaultable | Yes | resolve_job_workday_defaults | Block only when current metadata marks it required and the Enterprise value cannot be resolved; otherwise omit |
| StandardWorkingFrequency | Enterprise Work Day Information value | Create omits StandardWorkingFrequency and current metadata confirms the field as required or defaultable | Yes | resolve_job_workday_defaults | Block only when current metadata marks it required and the Enterprise value cannot be resolved; otherwise omit |
| StandardAnnualWorkingDuration | Enterprise Work Day Information value | Create omits StandardAnnualWorkingDuration and current metadata confirms the field as required or defaultable | Yes | resolve_job_workday_defaults | Block only when current metadata marks it required and the Enterprise value cannot be resolved; otherwise omit |
| AnnualWorkingDurationUnits | Enterprise Work Day Information value | Create omits AnnualWorkingDurationUnits and current metadata confirms the field as required or defaultable | Yes | resolve_job_workday_defaults | Block only when current metadata marks it required and the Enterprise value cannot be resolved; otherwise omit |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Omitted edit value | An edit omits an existing value and no Standard Defaults row applies | Preserve the fresh current value | preserved |
| Date-effective split deletion range | delete-effective-split is requested | Never default the retained EffectiveStartDate or deletion EffectiveEndDate; use only freshly resolved boundaries and omit non-key attributes | not_required |
| Omitted history value | A later create-history row omits an attribute | Inherit it from the immediately preceding row; require mandatory create values on the earliest row | preserved |
| Job family or subfamily | The value is omitted | Never infer it from display text; require one exactly resolved allowed value when mandatory | not_required |
| Explicit resolved reference | A reference resolves exactly | Preserve the resolved value | preserved |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JOB.DEFAULTS | decision | 5 | apply_default | applied->JOB.DESIGN;preserved->JOB.DESIGN;not_required->JOB.DESIGN;blocked->JOB.ERROR | JOB.DEPENDENCIES | stop | After validation, current-state reads, and required resolvers are complete |

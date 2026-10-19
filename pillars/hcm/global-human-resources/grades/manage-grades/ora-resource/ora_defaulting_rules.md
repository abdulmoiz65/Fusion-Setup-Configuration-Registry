# Manage Grades Defaulting Rules

## Purpose

Defines safe defaults and preservation rules for Manage Grades.

## Defaulting Precedence

| Priority | Condition | Required Action | Outcome |
|---|---|---|---|
| 1 | A valid explicit value is supplied and override is allowed | Preserve it | preserved |
| 2 | An edit omits an existing value and no standard default applies | Preserve the freshly read value | preserved |
| 3 | Exactly one standard default applies | Apply it | applied |
| 4 | No rule applies | Make no change | not_required |
| 5 | Required evidence is unresolved or conflicting | Apply no value and stop | blocked |

## Standard Defaults

| Field | Default Value | Applies When | Can User Override? | Resolver | If Unavailable or Invalid |
|---|---|---|---|---|---|
| ActiveStatus | A | An included Grade row omits ActiveStatus | Yes |  | Block when an explicit value is invalid |
| SetCode | COMMON | An included Grade row omits both SetId and SetCode | Yes |  | Block when an explicit set is invalid |
| EFF_CATEGORY_CODE | GRADE_LEG | A GradeLegislative row is authored | No |  | Block a conflicting value |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Omitted edit value | edit omits an existing value and no Standard Defaults row applies | Preserve the fresh current value | preserved |
| Date-effective split deletion range | delete with mode effective-split | Never default the retained EffectiveStartDate or deletion EffectiveEndDate; use only freshly resolved boundaries and omit non-key attributes | not_required |
| GradeCode or GradeName | The value is omitted on create | Do not infer it | not_required |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GRD.DEFAULTS | decision | 5 | apply_default | applied->GRD.DESIGN;preserved->GRD.DESIGN;not_required->GRD.DESIGN;blocked->GRD.ERROR | GRD.DEPENDENCIES | stop | After validation, current-state reads, and required resolvers are complete |

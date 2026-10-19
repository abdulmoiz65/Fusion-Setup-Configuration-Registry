# Manage Grades Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Manage Grades.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, inactivate, delete, or delete-effective-split | Block | Provide one supported operation. Treat delete-effective-split as delete with mode effective-split. | Every request |  |
| Delete mode | zap or effective-split | Block | State whether to purge the complete logical Grade or delete one dated split | delete targets the Grade parent |  |
| Existing grade selector | Exact GradeId, GradeCode, or GradeName | Block | Provide one exact selector | get, edit, inactivate, or delete | find_manage_grades |
| Create identity | GradeCode and GradeName | Block | Provide the complete Grade identity | create |  |
| Effective context | Explicit EffectiveStartDate | Block | Provide one valid date for the logical object | Every mutation |  |
| Edit changes | At least one supported change | Block | Provide the intended change | edit |  |
| Effective-split deletion range | Exact existing Grade, retained EffectiveStartDate, and last deleted EffectiveEndDate | Block | Resolve the complete affected history and provide the inclusive deletion range | delete with mode effective-split | resolve_grade_split_deletion_range |
| Delete confirmation | Explicit confirmation of the displayed zap purge or effective-split range | Block loader handoff | Show the destructive scope and request confirmation | delete |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The target does not resolve exactly | Missing | Provide one exact Grade selector | find_manage_grades |
| A create identity already exists | Invalid | Supply a unique Grade identity | find_manage_grades |
| The reference-data set is unresolved | Invalid | Correct the Set | resolve_grade_set |
| A supplied Action Reason is unresolved | Invalid | Correct the Action Reason | resolve_grade_action_reason |
| Delete mode is absent or ambiguous | Invalid | Choose zap or effective-split; never infer purge intent from the word delete |  |
| The selected effective-split row is absent, ambiguous, or marked FirstSplitFlag=true, or no immediately preceding row exists | Invalid | Choose one exact non-first EffectiveStartDate | resolve_grade_split_deletion_range |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Loader Boolean value | For an included attribute declared by current loader metadata as Boolean or Flag, write true or Yes as Y and false or No as N; preserve Y or N; do not add an omitted attribute or change REST read values | A Data Loader mutation includes the attribute |  |
| Date format | Normalize an unambiguous date to the loader format; reject an invalid date | A date is supplied |  |
| Logical-object effective date | Apply the supplied EffectiveStartDate to the Grade row and every included child row | Every mutation |  |
| Active status | Accept only the loader-supported active or inactive value | Status is supplied |  |
| Effective alignment | Reject an end date before the start date | An effective range is supplied |  |
| Grade deletion key | Use GradeId or both GradeCode and SetCode; reject GradeCode alone | A Grade delete artifact is authored | find_manage_grades |
| Zap delete | Author one Grade `DELETE` data row using the freshly resolved GradeId or GradeCode and SetCode. Do not author `MERGE`, child rows, or `SET PURGE_FUTURE_CHANGES Y` for the same logical Grade in that file. | delete with mode zap | find_manage_grades |
| Date-effective split deletion | Allow removal of one or more noninitial future splits only with `SET PURGE_FUTURE_CHANGES Y` and a Grade `MERGE` row. Set EffectiveStartDate to the immediately preceding history row's EffectiveStartDate and EffectiveEndDate to the selected row's EffectiveEndDate. Include only the resolved GradeId or GradeCode and SetCode plus these boundaries. Reject HDL `DELETE`, first-row deletion, and an unbounded or misaligned range. | delete with mode effective-split | resolve_grade_split_deletion_range |
| Legislative EFF context | Require the generated `FLEX:PER_GRADES_LEG_EFF` discriminator to contain the deployed context code | A GradeLegislative EFF row is supplied |  |
| GradeLegislative child identity | Require a complete parent Grade reference and one complete child key selected by Core Data Loader from the live key-field contract; context, category, and segments do not replace the child key | Every included GradeLegislative row |  |
| Multirow EFF identity | Require every flexfield segment marked as a unique key for the context; reject incomplete or duplicate combinations | A multirow GradeLegislative context is supplied |  |
| Mutation source scope | Keep the Grade worksheet, map entry, and base row for create, edit, or inactivate; include GradeLegislative and GradeStep only when explicitly modified. For zap, keep one Grade `DELETE` row with the resolved GradeId or GradeCode and SetCode. For effective-split, keep only the resolved Grade key, retained EffectiveStartDate, inclusive EffectiveEndDate, and the one supported purge directive. Omit child rows and non-key attributes for either delete mode. | create, edit, inactivate, or delete |  |
| Supported fields | Reject response-only, audit, and unregistered loader fields | A mutation value is supplied |  |
| Verification boundary | Do not treat source generation or load acceptance as business verification | Every mutation |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GRD.VALIDATE | decision | 1 | validate_input | valid->GRD.READ;missing->GRD.ERROR;invalid->GRD.ERROR;unsupported->GRD.ERROR | none | stop | Every Manage Grades request |

# Manage Grade Ladders Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Manage Grade Ladders.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, or delete-effective-split | Block | Provide one supported operation | Every request |  |
| Existing ladder selector | Exact GradeLadderId or Name | Block | Provide one exact selector | get, edit, or delete-effective-split | find_manage_grade_ladders |
| Create identity | Name and optional GradeSetCode | Block when Name is missing; default omitted GradeSetCode | Provide Name | create |  |
| Effective context | Explicit EffectiveStartDate | Block | Provide one valid date for the logical object | Every mutation |  |
| Edit changes | Exact ladder and at least one supported change | Block | Provide the target and intended change | edit | find_manage_grade_ladders |
| Delete-effective-split target | Exact ladder, retained EffectiveStartDate, and inclusive deletion EffectiveEndDate | Block | Provide the bounded future range | delete-effective-split | resolve_grade_ladder_split_deletion_range |
| Grade rows | Exact Grade and optional placement sequence | Block | Provide each requested Grade | Grades are supplied | resolve_grade_ladder_grade |
| Rate definition | Rate Name, Legislative Data Group, Rate Type, Frequency, Annualization Factor, and Currency | Block | Provide or resolve every required rate value | A rate row is supplied | resolve_grade_ladder_ldg |
| Rate values | One numeric value or explicit blank for every Rate by Grade Step combination | Block | Complete the rate-value matrix | Rates and grades are supplied | resolve_grade_ladder_steps |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A Grade is unresolved, inactive, ineffective, incompatible with GradeType, or outside the explicit or defaulted Grade Set or COMMON | Invalid | Correct the Grade, GradeType, or Grade Set | resolve_grade_ladder_grade |
| A required Grade step collection is missing, duplicated, or unordered | Invalid | Correct the Grade steps before ladder authoring | resolve_grade_ladder_steps |
| A Legislative Data Group does not resolve exactly once | Invalid | Correct the Legislative Data Group | resolve_grade_ladder_ldg |
| A supplied currency does not resolve exactly once | Invalid | Correct the currency | resolve_grade_ladder_currency |
| A Rate by Grade Step combination is missing or duplicated | Invalid | Complete the matrix with one numeric value or explicit blank per combination | resolve_grade_ladder_steps |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Loader Boolean value | For an included attribute declared by current loader metadata as Boolean or Flag, write true or Yes as Y and false or No as N; preserve Y or N; do not add an omitted attribute or change REST read values | A Data Loader mutation includes the attribute |  |
| Grade type | Require the STEP default and reject a different value | create |  |
| Grade Set | Require an explicit validated GradeSetCode or the COMMON default before source preparation | create |  |
| Logical-object effective date | Apply the supplied EffectiveStartDate to the GradeLadder row and every included child row | Every mutation |  |
| Grade compatibility | Require each Grade to be an active effective STEP Grade in the explicit or defaulted Grade Set or COMMON | A Grade is supplied | resolve_grade_ladder_grade |
| Grade steps | Require a nonempty ordered Step collection, Step count, and ceiling Step for each Grade | A Grade is supplied | resolve_grade_ladder_steps |
| Grade ordering | Require supplied sequences to be unique positive integers | Grade sequences are supplied |  |
| Rate ordering | Preserve supplied Rate-row order | Multiple Rates are supplied |  |
| Rate children | Omit StepRate and StepRateValue when no Rate is supplied; when Rates exist without Grades, include only StepRate rows | create |  |
| Rate-step matrix | When Rates and Grades exist, require exactly one numeric value or explicit blank for every Rate by Grade Step combination | create | resolve_grade_ladder_steps |
| Grade Set edit | Reject a Grade Set change when the resolved ladder contains Grades | edit changes Grade Set | find_manage_grade_ladders |
| Existing rate LDG | Reject an in-place Legislative Data Group change on an existing rate | edit changes an existing rate | resolve_grade_ladder_ldg |
| Date-effective split deletion | Allow removal of one or more noninitial future splits only with a `GradeLadder` `MERGE` row and `SET PURGE_FUTURE_CHANGES Y` when the current generated Grade Ladder loader contract preserves that directive. Require EffectiveStartDate to identify the last record to retain and EffectiveEndDate to identify the last record to delete. Reject HDL `DELETE`, logical-record or first-row deletion, an unsupported `RestAction`, an unavailable directive contract, and an unbounded or misaligned range. | delete-effective-split | resolve_grade_ladder_split_deletion_range |
| Effective-split deletion portability | Treat source rows, resolved identifiers, history evidence, immutable archives, preflight envelopes, and approvals as environment-specific. Re-resolve and regenerate them in the target environment; only the allowlisted directive contract is reusable. | delete-effective-split | resolve_grade_ladder_split_deletion_range |
| Mutation source scope | Keep the GradeLadder worksheet, map entry, and base row for every mutation; include GradesInLadder, StepRate, and StepRateValue only when supplied or modified | create, edit, or delete |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GLAD.VALIDATE | decision | 1 | validate_input | valid->GLAD.DEPENDENCIES;missing->GLAD.ERROR;invalid->GLAD.ERROR;unsupported->GLAD.ERROR | none | stop | Every Manage Grade Ladders request |

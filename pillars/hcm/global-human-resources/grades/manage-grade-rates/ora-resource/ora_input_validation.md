# Manage Grade Rates Input Validation

## Purpose

Defines required inputs, conditional requirements, field checks, and validation routing for Manage Grade Rates.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | get, create, edit, delete, or delete-effective-split | Block | Provide one supported operation | Every request |  |
| Existing rate selector | Exact RateId or GradeRateName | Block | Provide one exact selector | get, edit, or delete | find_manage_grade_rates |
| Create identity | GradeRateName, Legislative Data Group, Rate Type, and Frequency | Block | Provide every identity value | create | resolve_grade_rate_ldg |
| Effective context | Explicit EffectiveStartDate | Block | Provide one valid date for the logical object | Every mutation |  |
| Edit changes | Exact rate and at least one supported change | Block | Provide the target and intended change | edit | find_manage_grade_rates |
| Delete target | Exact current rate | Block | Provide one exact selector | delete | find_manage_grade_rates |
| Effective-split deletion range | Exact existing Grade Rate, retained EffectiveStartDate, and last deleted EffectiveEndDate | Block | Resolve the complete affected history and provide the inclusive deletion range | delete-effective-split | resolve_grade_rate_split_deletion_range |
| Rate value | Grade name or GradeCode, optional SetCode, with Value; Minimum and Maximum; or all three amounts | Block | Provide the Grade business value and a valid amount shape. SetCode is required only when the Grade lookup is ambiguous. RateObjectId is never requested from the end user. | A rate-value row is supplied | resolve_grade_rate_grade |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A Grade does not resolve to one active effective match | Invalid | Correct the Grade or effective context | resolve_grade_rate_grade |
| RateObjectId is supplied as end-user input | Invalid | Discard the unverified internal value and resolve the Grade name or GradeCode with SetCode when needed | resolve_grade_rate_grade |
| A lookup meaning or code does not resolve to one enabled effective LookupCode | Invalid | Correct the lookup value | resolve_grade_rate_lookup_codes |
| A Legislative Data Group is unresolved, ineffective, or ambiguous | Invalid | Correct the Legislative Data Group | resolve_grade_rate_ldg |
| The supplied or defaulted currency is disabled, ineffective, or ambiguous | Invalid | Correct the currency | resolve_grade_rate_currency |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Loader Boolean value | For an included attribute declared by current loader metadata as Boolean or Flag, write true or Yes as Y and false or No as N; preserve Y or N; do not add an omitted attribute or change REST read values | A Data Loader mutation includes the attribute |  |
| Amount shape | Reject an incomplete range; accept Value alone, Minimum and Maximum together, or all three amounts | A rate-value row is supplied |  |
| Logical-object effective date | Apply the supplied EffectiveStartDate to the GradeRate row and every included GradeRateValue row | Every mutation |  |
| Range ordering | Require Minimum less than or equal to MidValue and Value when present, and each less than or equal to Maximum | A range is supplied |  |
| Duplicate grade | Reject duplicate GradeId rows in one effective rate | Multiple rate-value rows are supplied | resolve_grade_rate_grade |
| Grade Rate identity | Require the populated GradeRate row to contain one complete parent key selected by Core Data Loader; when it selects the user key, populate GradeRateName and LegislativeDataGroup with the resolved LDG name | Every mutation |  |
| Child identity | Require exact parent-key parity with the populated GradeRate row and use resolved GradeCode with SetCode as the GradeRateValue Grade key by default. RateObjectId is an internal key: never request it from the end user, and populate it only from the freshly resolved GradeId when Core Data Loader explicitly selects the internal-ID alternative. | Every included GradeRateValue row | resolve_grade_rate_grade |
| Existing LDG | Preserve Legislative Data Group and reject an in-place change | Edit | resolve_grade_rate_ldg |
| Date-effective split deletion | Allow deletion of one or more noninitial future effective splits only with `SET PURGE_FUTURE_CHANGES Y` and a `Grade Rate` `MERGE` row. Require EffectiveStartDate to identify the last record to retain and EffectiveEndDate to identify the last record to delete. Reject HDL DELETE, first-row deletion, an unbounded or misaligned range, and authored GradeRateValue rows. | delete-effective-split | resolve_grade_rate_split_deletion_range |
| Currency | Preserve an explicit CurrencyCode after exact validation; default from the resolved LDG only on create, and preserve the current value on edit unless a supported change is requested and validated | Create or edit | resolve_grade_rate_currency |
| Prepared artifact | Compare the populated workbook and generated DAT key fields with the validated values and preview summary; stop on any difference | Before approval |  |
| Mutation source scope | Keep the GradeRate worksheet, map entry, and base row for every mutation. Include GradeRateValue only when explicitly modified, except that a delete-effective-split must omit all GradeRateValue rows and rely on the reviewed parent purge. | Create, edit, delete, or delete-effective-split |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GRAT.VALIDATE | decision | 1 | validate_input | valid->GRAT.DEPENDENCIES;missing->GRAT.ERROR;invalid->GRAT.ERROR;unsupported->GRAT.ERROR | none | stop | Every Manage Grade Rates request |

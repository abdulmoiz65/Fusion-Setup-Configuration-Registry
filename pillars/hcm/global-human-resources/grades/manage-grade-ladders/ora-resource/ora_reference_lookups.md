# Manage Grade Ladders Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_manage_grade_ladders | A row search, exact target lookup, or create uniqueness check is requested | GradeLadderId, exact Name, or user-supplied name fragment | /hcmRestApi/resources/{version}/gradeLaddersV2 | GradeLadderId, Name, GradeType, GradeSetId, ActiveStatus, EffectiveStartDate, EffectiveEndDate, and item link | To find rows by name fragment, pass q=Name like '%<name-fragment>%' without hardcoding the fragment and return all matches. For a single-row request, require one exact identifier or Name match. For create, require zero exact Name matches. | Resolved business identity, effective context, current values, and item link when available | Return zero or all matches for a row search. For single-row resolution, stop on zero or multiple exact matches. For create, zero means the identity is available; one or more exact matches stop duplicate creation. |
| resolve_grade_ladder_ldg | A rate row is supplied | Legislative Data Group name or ID | /hcmRestApi/resources/{version}/legislativeDataGroupsLOV | Name, LegislativeDataGroupId, LegislationCode, DefaultCurrencyCode | Exactly one effective match | Name -> LegislativeDataGroupName, LegislativeDataGroupId, LegislationCode, and DefaultCurrencyCode | Stop on zero or multiple matches |
| resolve_grade_ladder_currency | A rate row supplies currency or uses the resolved LDG default | Currency code or name | /fscmRestApi/resources/{version}/currenciesLOV | CurrencyCode, Name | Exactly one currency match | CurrencyCode, Name | Stop on zero or multiple matches |
| resolve_grade_ladder_grade | A Grade is supplied | Grade name or code, effective date, and explicit or defaulted Grade Set | /hcmRestApi/resources/{version}/gradesV2 | GradeId, GradeCode, Name, GradeType, SetId, SetName, ActiveStatus, EffectiveStartDate, EffectiveEndDate, and item link | Exactly one active effective STEP Grade in the explicit or defaulted Grade Set or COMMON | GradeId, GradeCode, Name, SetId, SetName, and item link | Stop on zero or multiple matches, inactive status, wrong type, or wrong set |
| resolve_grade_ladder_steps | A STEP Grade is resolved | Returned Grade item link and effective date | Server-returned gradeSteps link from the resolved gradesV2 item | GradeStepId, StepName, GradeStepSequence, CeilingStepFlag | Return the complete ordered collection with exactly one ceiling Step | Ordered GradeStepId values, GradeStepsCount, and the ceiling GradeStepId as GradeCeilingStepId | Stop on missing, duplicate, unordered, or multiple ceiling Steps |
| resolve_grade_ladder_lookup_codes | Status, rate type, or frequency requires a stored lookup code | Supplied meaning or code, LDG legislation when applicable, and effective date | hcm.global-human-resources.global-human-resources-common.manage-common-lookups | LookupCode and Meaning | Require one enabled effective ACTIVE_INACTIVE status, GRADE_PAY_RATE_TYPE RateType, or declared RateFrequency code | LookupCode and Meaning | Stop on zero, multiple, disabled, or out-of-range results |
| resolve_grade_ladder_split_deletion_range | Date-effective split deletion is requested | Exact GradeLadderId or Name, retained EffectiveStartDate, and requested last deleted EffectiveEndDate | Complete current Grade Ladder effective history through /hcmRestApi/resources/{version}/gradeLaddersV2 and the current generated Grade Ladder loader contract | Grade Ladder identity, effective ranges, and retained predecessor values | Require one logical Grade Ladder; verify the retained start exists, the requested end aligns to a later existing row, at least one later row would be removed, and the current contract preserves `SET PURGE_FUTURE_CHANGES Y` | Confirmed retained start, inclusive deletion end, and predecessor values | Stop for a logical first-row deletion, missing or unbounded range, misalignment, ambiguous history, or unavailable directive |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup requires authentication | Use core.auth.fusion-oauth-authentication. |
| A read or mutation precheck runs | Execute applicable reference_lookup nodes through core.fusion-api.rest-api-client before source preparation; do not use core.data-loader, core.data-loader.task-rest, or ora_rest_execution.md for the read. |
| An existing date-effective target or reference is resolved as of a requested date | Accept the row when EffectiveStartDate ≤ requested date ≤ EffectiveEndDate; do not require equal start dates. |
| A date-effective split deletion is requested | Read the complete current Grade Ladder history before source preparation; use the verified retained predecessor and inclusive last-deleted boundary only when the current generated loader contract preserves `SET PURGE_FUTURE_CHANGES Y`. State that complete Grade Ladder deletion is unsupported; present only the retained effective start and inclusive deletion end. Keep internal eligibility and identifiers hidden. |
| Grade Steps are required | Read the exact Grade from gradesV2 for the effective date without onlyData=true, follow its returned item link, then follow its returned gradeSteps link; never construct the child URL from GradeId or use gradesLov. |
| An exact target or reference is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A collection is requested | Use bounded limit and offset pagination and follow hasMore or the next page only to the declared bound. |
| Any lookup runs | Keep it read-only; mutations use core.data-loader. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GLAD.READ | decision | 3 | reference_lookup | resolved->GLAD.DEFAULTS;list_returned->GLAD.DEFAULTS;create_available->GLAD.DEFAULTS;not_found->GLAD.ERROR;duplicate->GLAD.ERROR;ambiguous->GLAD.ERROR;failed->GLAD.ERROR | GLAD.DEPENDENCIES | stop | Read is requested, an exact target is required before a mutation, a uniqueness check is required before create, or an applicable reference must resolve |

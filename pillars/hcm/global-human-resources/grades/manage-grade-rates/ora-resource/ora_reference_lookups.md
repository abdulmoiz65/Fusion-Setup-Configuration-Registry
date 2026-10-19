# Manage Grade Rates Reference Lookups

## Purpose

Defines deterministic, read-only reference resolution for this task.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_manage_grade_rates | A row search, exact target lookup, or create uniqueness check is requested | RateId, exact GradeRateName, or user-supplied name fragment | /hcmRestApi/resources/{version}/gradeRatesV2 | RateId, GradeRateName, CurrencyCode, RateFrequency, RateType, ActiveStatus, EffectiveStartDate, EffectiveEndDate, and item link | To find rows by name fragment, pass q=GradeRateName like '%<name-fragment>%' without hardcoding the fragment and return all matches. For a single-row request, require one exact identifier or name match. For create, require zero exact name matches. | Resolved business identity, effective context, current values, and item link when available | Return zero or all matches for a row search. For single-row resolution, stop on zero or multiple exact matches. For create, zero means the identity is available; one or more exact matches stop duplicate creation. |
| resolve_grade_rate_split_deletion_range | A delete-effective-split request is supplied | Exact GradeRateName or RateId, retained EffectiveStartDate, and requested last deleted EffectiveEndDate | /hcmRestApi/resources/{version}/gradeRatesV2 | RateId, GradeRateName, LegislativeDataGroup, effective start and end dates, and current values | Require one logical Grade Rate. Confirm that the retained start is an existing row start, the requested end aligns to the end of an existing later row, and at least one later effective split is removed. | Confirmed retained start, inclusive deletion end, preserved predecessor values, and the future `GradeRateValue` rows to reconcile | Stop when no later split exists to remove, the range is empty, the requested end does not align to an existing row end, the range would remove the logical first split, or the target is ambiguous. |
| resolve_grade_rate_ldg | Create requires an LDG or edit needs the current LDG | Legislative Data Group name or ID and effective date | /hcmRestApi/resources/{version}/legislativeDataGroupsLOV | Name, LegislativeDataGroupId, LegislationCode, DefaultCurrencyCode | Exactly one effective match; require DefaultCurrencyCode only when create omits CurrencyCode | Name -> LegislativeDataGroup, LegislativeDataGroupId, LegislationCode, and DefaultCurrencyCode when available | Stop on zero, multiple, ineffective, or missing required default-currency matches |
| resolve_grade_rate_currency | Currency is supplied or create omits it | Supplied CurrencyCode; otherwise resolved LDG DefaultCurrencyCode | /fscmRestApi/resources/{version}/currenciesLOV | CurrencyCode, Name, EnabledFlag, StartDateActive, EndDateActive | Exactly one enabled effective currency matching the selected code | CurrencyCode and Name | Stop on zero, multiple, disabled, or ineffective matches |
| resolve_grade_rate_grade | A rate-value row supplies a Grade name or code | Grade name or GradeCode, optional SetCode, and effective date | /hcmRestApi/resources/{version}/gradesLov | GradeId, GradeCode, Name, SetCode, SetId, ActiveStatus | Require exactly one active effective Grade. When a name or code matches multiple Grade Sets, require SetCode and repeat the lookup. | GradeCode -> GradeRateValue.GradeCode; SetCode -> GradeRateValue.SetCode; retain GradeId internally and map GradeId -> RateObjectId only when Core Data Loader selects the internal-ID alternative | Stop on zero matches or inactive status. On multiple matches, request SetCode; never request RateObjectId. |
| resolve_grade_rate_lookup_codes | Status, rate type, or frequency requires a stored lookup code | Supplied meaning or code, LDG legislation, and effective date | hcm.global-human-resources.global-human-resources-common.manage-common-lookups | LookupCode and Meaning | Require exactly one enabled effective result | LookupCode and Meaning | Stop on zero, multiple, disabled, or out-of-range results |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A lookup requires authentication | Use core.auth.fusion-oauth-authentication. |
| A read or mutation precheck runs | Execute applicable reference_lookup nodes through core.fusion-api.rest-api-client before source preparation; do not use core.data-loader, core.data-loader.task-rest, or ora_rest_execution.md for the read. |
| Complete details are requested | Resolve the exact Grade Rate item without a restrictive field projection, follow the server-returned child link that current response/describe identifies for Grade Rate values, paginate every parent and value collection, and return the current Grade Rate plus all GradeRateValue business fields after the task's WHO/ID filtering. Never construct the child path. |
| An existing date-effective target or reference is resolved as of a requested date | Accept the row when EffectiveStartDate ≤ requested date ≤ EffectiveEndDate; do not require equal start dates. |
| A delete-effective-split request is resolved | Read the complete effective history and the `GradeRateValue` rows for the requested future segment; do not infer retained or deletion boundaries from a display name. |
| An exact target or reference is required | Accept exactly one eligible result; stop on zero or multiple results. |
| A collection is requested | Use bounded limit and offset pagination and follow hasMore or the next page only to the declared bound. |
| Currency is required | Preserve and validate an explicit CurrencyCode; only create may use and validate the resolved LDG DefaultCurrencyCode. |
| A GradeRateValue key is prepared | Prefer the resolved GradeCode and SetCode user-key alternative. RateObjectId is internal: never request or accept it as an end-user business input; populate it only from the freshly resolved GradeId when Core Data Loader explicitly selects the internal-ID alternative. |
| Any lookup runs | Keep it read-only; mutations use core.data-loader. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GRAT.READ | decision | 3 | reference_lookup | resolved->GRAT.DEFAULTS;list_returned->GRAT.DEFAULTS;create_available->GRAT.DEFAULTS;not_found->GRAT.ERROR;duplicate->GRAT.ERROR;ambiguous->GRAT.ERROR;failed->GRAT.ERROR | GRAT.DEPENDENCIES | stop | Read is requested, an exact target is required before a mutation, a uniqueness check is required before create, or an applicable reference must resolve |

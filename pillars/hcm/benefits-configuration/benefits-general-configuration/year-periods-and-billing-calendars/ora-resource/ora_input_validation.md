# Benefit Year Periods HDL Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | A declared create, update, delete, or validation-only intent | Stop before preview | Provide the intended operation | Every request | |
| HDL source | A nonempty source for the registered benefitYearPeriods object | Stop before preview | Provide the exact DAT or loader artifact | Every import or validation request | |
| Task and target context | Task code BEN_MANAGE_PROGRAMS_PLAN_YEARS and the target environment | Stop before a side effect | Select the target through the routed workflow | Every import request | |
| Current metadata validation | A successful core.data-loader validation of the exact artifact | Stop before approval | Validate the source against current Data Loader metadata | Every import request | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A benefitYearPeriods row supplies PeriodTypeMeaning | Validate that row's value through the selected commonLookupsLOV resolver | Record valid, invalid, ambiguous, or unverified_forbidden per row and field | |
| The PeriodTypeMeaning lookup returns 403 | Do not fail field validation or mark the meaning invalid; record unverified_forbidden | Continue independent checks; retain the unverified status for load readiness | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Business object | Reject a source whose top-level object is not benefitYearPeriods | Every request | |
| Unsupported CSV route | Reject CSV export or import as a replacement route because catalog support is N | Every request proposing CSV | |
| HDL contract | Reject missing, malformed, changed, or unvalidated source content | Every import request | |
| Benefit year period dates | Reject a populated StartDate, EndDate, LimitationYearStartDate, or LimitationYearEndDate unless it is a valid calendar date formatted exactly YYYY-MM-DD; do not silently reformat an ambiguous value | Every benefitYearPeriods record that supplies any listed date | |
| Period type foreign key | Reject a `PeriodType` display label or inferred code. The current live contract marks `PeriodType` as a foreign key and provides `PeriodTypeMeaning` as its user-key alternative; require a target-validated key form and exact lookup value. | Every benefitYearPeriods record that supplies a period type | |
| PeriodTypeMeaning lookup | When supplied, require one exact Meaning match through commonLookupsLOV with LookupTypeFinder;LookupType=BEN_PERD_TYP; preserve the supplied meaning | Every benefitYearPeriods row that supplies PeriodTypeMeaning | |
| Required operation | Reject a source that omits `RestAction`; current live metadata marks it mandatory. | Every import request | |
| Attribute and operation contract | Require current Data Loader metadata to validate attributes, keys, dates, hierarchy, and the requested operation; do not infer any of them | Every import request | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_YR.VALIDATE_REQUEST | decision | 10 | validate_input | valid->BEN_YR.CHECK_READINESS;invalid->BEN_YR.HANDLE_ISSUE | none | stop | Validate task scope, target context, object identity, and exact HDL source |

# Benefit Year Periods Reference Lookup

## Conditional Period Type Meaning Check

Run this read-only check for each `benefitYearPeriods` row that supplies
`PeriodTypeMeaning`, only when the active project workflow selects reference
validation through `core.fusion-api.rest-api-client`. Use the selected
environment and `REST-Framework-Version: 9`. This check validates the
supplied meaning without changing it, inferring a `PeriodType` code, or
authorizing an HDL load.

| Resolver | Supplied field | Read-only Fusion request | Exact-match rule | Result |
|---|---|---|---|---|
| resolve_period_type | `benefitYearPeriods.PeriodTypeMeaning` | `GET /fscmRestApi/resources/11.13.18.05/commonLookupsLOV?finder=LookupTypeFinder;LookupType=BEN_PERD_TYP` | Require one distinct row with `LookupType=BEN_PERD_TYP` and `Meaning` exactly equal to the supplied value. | Validation status only; preserve `PeriodTypeMeaning`. |

Send only the declared `LookupTypeFinder` request, without a `q` predicate.
Read all response pages and compare returned `Meaning` exactly, including
case, within `BEN_PERD_TYP`. Zero exact matches means `invalid`; multiple
distinct exact matches mean `ambiguous`; one means `valid`. Do not choose the
first candidate or substitute `LookupCode` for the user-key meaning. If
`PeriodTypeMeaning` is omitted, skip this lookup without an error; the
current Data Loader metadata still governs any supplied `PeriodType` code.

An HTTP 403 records `unverified_forbidden` for only the affected row and
field. Do not fail field validation, mark the meaning invalid, or stop other
independent checks. It does not prove the meaning valid: resolve access or
use another workflow-approved authoritative check before live load. A 401
may use the selected client's permitted one-time cached-token refresh;
classify a remaining denial as auth/authz. Classify other failures separately,
without treating them as no matches. If no read-only route is active, record
a workflow blocker; do not call REST directly or silently mark the meaning valid.

Oracle REST contract: [commonLookupsLOV](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-commonlookupslov-get.html).

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_YR.LOOKUP_PERIOD_TYPE | decision | 25 | reference_lookup | matched->BEN_YR.ENFORCE_DESIGN;skipped->BEN_YR.ENFORCE_DESIGN;forbidden->BEN_YR.ENFORCE_DESIGN;invalid->BEN_YR.HANDLE_ISSUE | BEN_YR.CHECK_READINESS | continue | Validate each supplied benefitYearPeriods.PeriodTypeMeaning through BEN_PERD_TYP; 403 records unverified_forbidden |

# Benefit Self-Service Configuration Reference Lookups

## Conditional Meaning Checks

Apply these read-only checks only when a `benefitSelfServiceConfigurations` row
supplies the corresponding field and the current Data Loader sample confirms
that exact attribute. Do not infer `SelfServiceEnrollmentPathMeaning` from
another HDL object's schema; use it in this skill only if the current
`benefitSelfServiceConfigurations` sample exposes it. Otherwise report the
mapping mismatch and omit the field from the DAT. Run selected checks through
`core.fusion-api.rest-api-client` against the selected environment only when
the active project workflow selects reference validation. Send
`REST-Framework-Version: 9`. Each check validates the supplied meaning; it
does not change the value, choose an HDL code, or authorize a load.

| Resolver | Supplied field | Read-only Fusion request | Exact-match rule | Result |
|---|---|---|---|---|
| resolve_unrestricted_processing_type | `benefitSelfServiceConfigurations.AllowUnrestrictedProcessingTypeMeaning` | `GET /fscmRestApi/resources/11.13.18.05/commonLookupsLOV?finder=LookupTypeFinder;LookupType=BEN_ALLOW_SS_UNRST_PROCG` | Require one distinct row with `LookupType=BEN_ALLOW_SS_UNRST_PROCG` and `Meaning` exactly equal to the supplied value. | Validation status only; preserve `AllowUnrestrictedProcessingTypeMeaning`. |
| resolve_enrollment_path | `benefitSelfServiceConfigurations.SelfServiceEnrollmentPathMeaning`, only if confirmed in current HDL sample | `GET /fscmRestApi/resources/11.13.18.05/commonLookupsLOV?finder=LookupTypeFinder;LookupType=ORA_BEN_SS_PATH_SELECTION` | Require one distinct row with `LookupType=ORA_BEN_SS_PATH_SELECTION` and `Meaning` exactly equal to the supplied value. | Validation status only; preserve `SelfServiceEnrollmentPathMeaning`. |

Send only the declared `LookupTypeFinder` request, without a `q` predicate.
Read all response pages and compare returned `Meaning` exactly, including
case, within the requested lookup type. Zero exact matches means `invalid`;
multiple distinct exact matches mean `ambiguous`; one means `valid`. Do not
select the first candidate or replace the meaning with a code. If a field
is omitted, skip its check without an error.

An HTTP 403 records `unverified_forbidden` for only the affected row and
field. Do not fail field validation, mark the value invalid, or stop other
independent checks. It is not evidence of a valid value: resolve access or
use another workflow-approved authoritative check before live load. A 401
may use the selected client's permitted one-time cached-token refresh;
classify a remaining denial as auth/authz. Classify other failures separately,
without treating them as no matches. If no read-only route is active, record
a workflow blocker; do not call REST directly or silently mark the value valid.

Oracle REST contract: [commonLookupsLOV](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-commonlookupslov-get.html).

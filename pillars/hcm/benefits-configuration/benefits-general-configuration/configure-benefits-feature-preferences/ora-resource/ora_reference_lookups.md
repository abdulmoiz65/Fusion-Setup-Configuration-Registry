# Benefits Feature Preferences Reference Lookups

## Conditional Update Checks

Apply these read-only checks only to supplied fields in
`benefitFeaturePreferences` Update preferences rows. The fixed parameterless
`initializeBenefitFeaturePreferences` Create preferences DAT has no user
preference values: skip all four lookups for that operation. Use the selected
environment and `core.fusion-api.rest-api-client` only when the active project
workflow selects reference validation. Send `REST-Framework-Version: 9`.
These checks validate the user's meaning or legislation value without
changing it, inventing a code, or authorizing an HDL load.

| Resolver | Supplied field | Read-only Fusion request | Exact-match rule | Result |
|---|---|---|---|---|
| resolve_feature_type | `benefitFeaturePreferences.FeatureTypeMeaning` | `GET /fscmRestApi/resources/11.13.18.05/commonLookupsLOV?finder=LookupTypeFinder;LookupType=ORA_BEN_FP_FEATURE_TYPE` | Require one distinct row with `LookupType=ORA_BEN_FP_FEATURE_TYPE` and `Meaning` exactly equal to the supplied value. | Validation status only; preserve FeatureTypeMeaning. |
| resolve_preference_status | `benefitFeaturePreferences.PreferenceStatusMeaning` | `GET /fscmRestApi/resources/11.13.18.05/commonLookupsLOV?finder=LookupTypeFinder;LookupType=ORA_BEN_FP_PREF_STATUS` | Require one distinct row with `LookupType=ORA_BEN_FP_PREF_STATUS` and `Meaning` exactly equal to the supplied value. | Validation status only; preserve PreferenceStatusMeaning. |
| resolve_applicability | `benefitFeaturePreferences.ApplicabilityMeaning` | `GET /fscmRestApi/resources/11.13.18.05/commonLookupsLOV?finder=LookupTypeFinder;LookupType=ORA_BEN_FP_APPLICABILITY` | Require one distinct row with `LookupType=ORA_BEN_FP_APPLICABILITY` and `Meaning` exactly equal to the supplied value. | Validation status only; preserve ApplicabilityMeaning. |
| resolve_legislation | `benefitFeaturePreferences.Legislation` | `GET /fscmRestApi/resources/11.13.18.05/territoriesLOV?q=TerritoryShortName='<Legislation>'` | Require one distinct returned row whose `TerritoryShortName` exactly equals the supplied Legislation. | Validation status only; preserve Legislation. |

For `commonLookupsLOV`, send only the declared `LookupTypeFinder` request,
without a `q` predicate, and compare returned `Meaning` exactly, including
case, within the requested lookup type. For `territoriesLOV`, send the supplied
Legislation in the `q=TerritoryShortName` equality predicate. URL-encode the
complete query parameter, escape apostrophes using the endpoint's documented
query syntax, and compare the returned `TerritoryShortName` again for exact
equality. Read all result pages before deciding zero (`invalid`), one
(`valid`), or multiple distinct exact matches (`ambiguous`). Do not select the
first candidate or replace a meaning or territory name with a code.

Skip a lookup when its field is omitted. An HTTP 403 records
`unverified_forbidden` for only the affected row and field: do not fail field
validation, mark the value invalid, or stop the remaining independent checks.
It is not evidence of a valid value. Resolve access or use another
workflow-approved authoritative check before a live load. A 401 may use the
selected client's permitted one-time cached-token refresh; classify a
remaining denial as auth/authz. Classify other request failures separately;
do not turn them into no matches. Without an active read-only lookup route,
record a workflow blocker and do not call REST directly or silently mark a
value valid.

Oracle REST contracts: [commonLookupsLOV](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-commonlookupslov-get.html) and [territoriesLOV](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-servername-fscmrestapi-resources-11.13.18.05-territorieslov-get.html).

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_PREF.LOOKUP_FEATURE_TYPE | decision | 12 | reference_lookup | matched->BEN_PREF.LOOKUP_STATUS;skipped->BEN_PREF.LOOKUP_STATUS;forbidden->BEN_PREF.LOOKUP_STATUS;invalid->BEN_PREF.HANDLE_ISSUE | BEN_PREF.VALIDATE_REQUEST | continue | For Update only, validate supplied FeatureTypeMeaning through ORA_BEN_FP_FEATURE_TYPE; 403 records unverified_forbidden |
| BEN_PREF.LOOKUP_STATUS | decision | 14 | reference_lookup | matched->BEN_PREF.LOOKUP_APPLICABILITY;skipped->BEN_PREF.LOOKUP_APPLICABILITY;forbidden->BEN_PREF.LOOKUP_APPLICABILITY;invalid->BEN_PREF.HANDLE_ISSUE | BEN_PREF.LOOKUP_FEATURE_TYPE | continue | For Update only, validate supplied PreferenceStatusMeaning through ORA_BEN_FP_PREF_STATUS; 403 records unverified_forbidden |
| BEN_PREF.LOOKUP_APPLICABILITY | decision | 16 | reference_lookup | matched->BEN_PREF.LOOKUP_LEGISLATION;skipped->BEN_PREF.LOOKUP_LEGISLATION;forbidden->BEN_PREF.LOOKUP_LEGISLATION;invalid->BEN_PREF.HANDLE_ISSUE | BEN_PREF.LOOKUP_STATUS | continue | For Update only, validate supplied ApplicabilityMeaning through ORA_BEN_FP_APPLICABILITY; 403 records unverified_forbidden |
| BEN_PREF.LOOKUP_LEGISLATION | decision | 18 | reference_lookup | matched->BEN_PREF.GATE_EXECUTION;skipped->BEN_PREF.GATE_EXECUTION;forbidden->BEN_PREF.GATE_EXECUTION;invalid->BEN_PREF.HANDLE_ISSUE | BEN_PREF.LOOKUP_APPLICABILITY | continue | For Update only, validate supplied Legislation against territoriesLOV TerritoryShortName; 403 records unverified_forbidden |

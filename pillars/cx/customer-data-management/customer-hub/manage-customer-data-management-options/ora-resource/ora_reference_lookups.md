# Reference Lookups

Resolve the exact live profile definition, SITE record, and lookup-backed stored value. These reads do not authorize a change.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| read_cdm_option_definition | A supported option is viewed, changed, defaulted, or found in a changed FSM row | Exact ProfileOptionName and SITE | GET /fscmRestApi/resources/11.13.18.05/profileOptions/{ProfileOptionName}; GET its child/profileOptionLevels; GET its child/siteProfileOptionValues through core.fusion-api.apps-common | ProfileOptionName, ApplicationId, SqlValidation, LevelName, EnabledFlag, UpdateableFlag, LevelValue, ProfileOptionValue | Require one exact inventory definition, one enabled SITE level, and at most one configured SITE record | ApplicationId, SqlValidation, SITE eligibility, SITE key, current stored value | Stop with catalog_mismatch or input_validation; do not choose another code or level |
| resolve_cdm_option_lookup_code | SqlValidation for a requested categorical option names exactly one lookup type | Exact lookup type and requested stored value | GET /fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}/child/lookupCodes through core.fusion-api.apps-common | LookupCode, Meaning, EnabledFlag, StartDateActive, EndDateActive | Require one exact active LookupCode equal to the requested stored value | Confirmed stored code and UI meaning | Stop before preview; do not substitute the UI label, another active code, or a stale code |

## Lookup Type Mapping

| Profile Option Code | Lookup Type |
|---|---|
| ORA_ZCQ_ENABLE_REALTIME_KEYGEN | YES_NO |
| ORA_ZCQ_CONVERTER_FINEST_LOGGING | YES_NO |
| ORA_ZCH_MERGE_SCOPE | ORA_ZCH_MERGE_SCOPE_LOOKUP |
| ZCH_REQUEST_NOTIFICATIONS | ORA_ZCH_NOTIFICATION_OPTION |
| ZCA_MERGE_REQUEST | YES_NO |
| ZCH_DEDUP_REQUEST_TYPE_OPTION | ZCH_DEDUP_REQUEST_TYPE_OPTION |
| ORA_ZCH_DS_MERGE_REQUESTS | ZCH_EUM_REQUEST_OPTION |
| ZCH_USER_MERGE_REQUESTS | ZCH_EUM_REQUEST_OPTION |
| ZCH_AGREEMENT_TYPE | ORA_ZCH_AGREEMENT_LOOKUP |
| ZCH_SETATTRIBUTE_TYPE | ORA_ZCH_SETATTRIBUTE_LOOKUP |
| ZCH_ENABLE_SURVIVORSHIP | ZCH_YES_NO |
| ORA_ZCH_SETMASTER_TYPE | ORA_ZCH_SETMASTER_LOOKUP |
| ORA_ZCH_MERGE_IDENTICAL | YES_NO |
| ZCH_GROOVY_RULE | YES_NO |
| ORA_ZCH_LINK_SETMAIN_TYPE | ORA_ZCH_LINK_SETMAIN_LOOKUP |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| SqlValidation names one supported lookup type | Resolve the requested stored value against that lookup before preview |
| SqlValidation is blank for a documented numeric or boolean option | Apply the closed local type rule and require live definition and SITE eligibility; do not invent a lookup |
| Live lookup meanings differ from documentation | Show the live meaning, classify the discrepancy, and block until ownership is resolved |
| A documented profile is omitted from an otherwise successful FSM export | Confirm it through the live definition and report export_content_discrepancy; never synthesize an FSM row |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CDMO.READ_PROFILE_OPTION | step | 2 | reference_lookup | resolved->CDMO.RESOLVE_STORED_VALUE;unresolved->CDMO.ERROR | CDMO.VALIDATE_CONTEXT | stop | Before preview whenever an option definition, SITE eligibility, current value, or CSV identity must be verified |
| CDMO.RESOLVE_STORED_VALUE | decision | 3 | reference_lookup | resolved->CDMO.DEPENDENCY_READINESS;not_applicable->CDMO.DEPENDENCY_READINESS;unresolved->CDMO.ERROR | CDMO.READ_PROFILE_OPTION | stop | Resolve a lookup-backed categorical value; take not_applicable only for a documented numeric or blank contract |

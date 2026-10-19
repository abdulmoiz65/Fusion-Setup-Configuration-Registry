# Manage Resource Profile Options Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_profile_option_definition | Every changed profile value after input validation | Exact ProfileOptionName | GET /fscmRestApi/resources/11.13.18.05/profileOptions/<ProfileOptionName> through core.fusion-api.apps-common | ProfileOptionName, SqlValidation, definition status | Require one exact ProfileOptionName | SqlValidation and definition facts | Stop and report that the profile option is unresolved |
| resolve_profile_option_level | Every changed profile value after definition resolution | Resolved ProfileOptionName, level, and scope key | GET /fscmRestApi/resources/11.13.18.05/profileOptions/<ProfileOptionName>/child/profileOptionLevels and GET the matching site, product, or user profile-value child through core.fusion-api.apps-common | LevelName, EnabledFlag, UpdateableFlag, LevelValue, ProfileOptionValue | Require one exact requested level and scope key | Enabled flag, updatable flag, current value, and scope key | Stop and report that the level or scope is unresolved |
| resolve_profile_option_lookup_type | Every changed profile value after definition resolution | SqlValidation returned by resolve_profile_option_definition | Extract one LOOKUP_TYPE literal from the resolved SqlValidation response; no additional REST request | Resolved lookup type | Require exactly one LOOKUP_TYPE literal using the supported LOOKUP_TYPE = '<lookup type>' or LOOKUP_TYPE='<lookup type>' form | Resolved lookup type | Stop and report that the validation contract is unresolved |
| resolve_profile_option_lookup_code | Every changed profile value after lookup type resolution | Resolved lookup type and requested ProfileOptionValue | GET /fscmRestApi/resources/11.13.18.05/standardLookups/<resolved lookup type>?expand=lookupCodes through core.fusion-api.apps-common | LookupCode, EnabledFlag, StartDateActive, EndDateActive | Require one exact LookupCode equal to requested ProfileOptionValue | Matched code, enabled flag, start date, and end date | Stop and report that the requested code is unresolved |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| SqlValidation contains exactly one supported LOOKUP_TYPE literal | Resolve that lookup type before resolving the requested code |
| SqlValidation is blank, contains no lookup type, contains more than one lookup type, or uses an unsupported expression | Block the import preview and report the unresolved validation contract |
| Requested lookup code is disabled, not yet active, or end-dated | Block the import preview and request an enabled effective code |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RPO.RESOLVE_PROFILE | step | 2 | reference_lookup | resolved->RPO.RESOLVE_LEVEL;unresolved->RPO.RETURN_ISSUES | RPO.VALIDATE_INPUT | stop | Every changed profile value |
| RPO.RESOLVE_LEVEL | step | 3 | reference_lookup | resolved->RPO.RESOLVE_LOOKUP_TYPE;unresolved->RPO.RETURN_ISSUES | RPO.RESOLVE_PROFILE | stop | Every changed profile value |
| RPO.RESOLVE_CODE | step | 5 | reference_lookup | resolved->RPO.ENFORCE_VALUE;unresolved->RPO.RETURN_ISSUES | RPO.RESOLVE_LOOKUP_TYPE | stop | Every changed profile value |

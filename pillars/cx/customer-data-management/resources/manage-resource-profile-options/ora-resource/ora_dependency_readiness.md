# Manage Resource Profile Options Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Profile definition | Resolve the live profile definition for every changed value |
| 2 | Profile level and current value | Resolve the same live level and scope before preview |
| 3 | Lookup type | Extract one exact standard lookup type from the resolved SqlValidation |
| 4 | Requested lookup code | Resolve and validate the requested code in the extracted lookup |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| RPO.PROFILE | Profile definition | Yes | Every changed profile value | Lookup | GET /fscmRestApi/resources/11.13.18.05/profileOptions/<ProfileOptionName> through core.fusion-api.apps-common | resolve_profile_option_definition | SqlValidation identifies the allowed-value lookup authority | Supply an exact profile option name | SqlValidation and profile definition facts |
| RPO.LEVEL | Profile level and current value | Yes | Every changed profile value | Lookup | GET profileOptionLevels and the matching site, product, or user child value through core.fusion-api.apps-common | resolve_profile_option_level | The selected level and scope must exist, be enabled, and be updatable | Supply the exact level and scope key | Level enabled flag, updatable flag, current value, and scope key |
| RPO.LOOKUP_TYPE | Standard lookup type | Yes | Every changed profile value | Verify | Extract exactly one LOOKUP_TYPE literal from the resolved SqlValidation using the supported LOOKUP_TYPE = '<lookup type>' or LOOKUP_TYPE='<lookup type>' form | resolve_profile_option_lookup_type | The requested value must be checked against the profile definition's own lookup | Use a profile option whose SqlValidation has one exact supported lookup reference | Resolved lookup type |
| RPO.CODE | Requested lookup code | Yes | Every changed profile value | Lookup | GET /fscmRestApi/resources/11.13.18.05/standardLookups/<resolved lookup type>?expand=lookupCodes through core.fusion-api.apps-common | resolve_profile_option_lookup_code | The requested code must be enabled and effective in the resolved lookup | Supply an enabled lookup code | Matched code, enabled flag, start date, and end date |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | Definition, level, SqlValidation lookup type, and requested code resolve exactly | Yes |
| Blocked | Definition, level, lookup expression, code, enabled state, or effective date is unresolved | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RPO.RESOLVE_LOOKUP_TYPE | step | 4 | resolve_dependency | resolved->RPO.RESOLVE_CODE;blocked->RPO.RETURN_ISSUES | RPO.RESOLVE_LEVEL | stop | Every changed profile value |

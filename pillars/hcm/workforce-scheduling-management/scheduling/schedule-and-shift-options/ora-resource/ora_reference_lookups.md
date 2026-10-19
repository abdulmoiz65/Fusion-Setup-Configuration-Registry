# Schedule and Shift Options Reference Lookups

## Source Basis

- Schedule and Shift Options Technical Design Document for FSCR, Confluence page 21805560036
- Workforce Scheduling Common Applications provider-dependency contract, user-provided

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_current_schedule_common_setups | Any update request | Selected ParameterCode and displayed setup-option name | GET {FA_HOST}/hcmRestApi/resources/11.13.18.05/scheduleCommonSetups?onlyData=true | SetupParamId, ParameterCode, ParameterName, ParameterValue, ValueType | Require exactly one returned row matching the selected ParameterCode and setup-option identity | SetupParamId, current ParameterValue, ValueType | Stop when no exact row or more than one matching row is returned |
| resolve_content_type | CONTENT_TYPE is updated | Selected ContentTypeName or ContentTypeId | GET {FA_HOST}/hcmRestApi/resources/11.13.18.05/contentTypesLOV?q={encoded-q}&orderBy=ContentTypeName&onlyData=true | ContentTypeId, ContentTypeName | Restrict to the documented fixed IDs 103, 104, and 109; then require one exact provider result | ParameterValue as a comma-delimited selection of ContentTypeId values | Stop when a selected value is absent or ambiguous |
| resolve_setup_option_common_lookup | RESPONSIBILITY_TYPE, SKILL_TYPE, WORKER_SEARCH_FIELDS, PARTIAL_SHIFT_SWAP, or FLEX_DURATION_SWAP is updated | Exact lookupType and selected Meaning | Invoke hcm.workforce-scheduling-management.workforce-scheduling-common.manage-common-lookups through core.fusion-api.apps-common.lookups manage-lookups, passing lookupType only and never LookupCode | Provider-returned LookupType, LookupCode, Meaning, active/selectable state, and provider validation evidence | Pass one documented lookupType unchanged: PER_RESPONSIBILITY_TYPES for RESPONSIBILITY_TYPE; ORA_HTS_JOB_PROFILE_TYPES for SKILL_TYPE; ORA_HTS_ASSIGN_WORKER_LOV for WORKER_SEARCH_FIELDS; ORA_HTS_PARTIAL_SHIFT_SWAP for PARTIAL_SHIFT_SWAP; ORA_HTS_FLEX_DURATION_SWAP for FLEX_DURATION_SWAP. Require one exact active selectable Meaning match. | ParameterValue from the provider-returned LookupCode | Stop for a provider gap, no match, or many matches; do not construct a Common Lookup request in this consumer. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A current setup-option row is selected | Resolve its immutable SetupParamId before any preview or update handoff. |
| A lookup-backed parameter is updated | Delegate through hcm.workforce-scheduling-management.workforce-scheduling-common.manage-common-lookups with its documented exact lookupType, then use one provider-returned LookupCode. |
| The Common Lookup provider returns a gap or ambiguity | Stop and disclose the provider evidence; do not call or construct a Common Lookup REST request from this consumer. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Resolver |
|---|---|---|---|---|---|---|---|---|
| SSO.LOOKUP.CURRENT | step | 3 | reference_lookup | resolved->SSO.LOOKUP.CONTENT_TYPE;no_match->SSO.ERROR;many_matches->SSO.ERROR | SSO.DEPENDENCIES | stop | Any update request | resolve_current_schedule_common_setups |
| SSO.LOOKUP.CONTENT_TYPE | step | 4 | reference_lookup | resolved->SSO.LOOKUP.COMMON;not_applicable->SSO.LOOKUP.COMMON;no_match->SSO.ERROR;many_matches->SSO.ERROR | SSO.LOOKUP.CURRENT | stop | CONTENT_TYPE is updated | resolve_content_type |
| SSO.LOOKUP.COMMON | step | 5 | reference_lookup | resolved->SSO.DEFAULTS;not_applicable->SSO.DEFAULTS;provider_gap->SSO.ERROR;no_match->SSO.ERROR;many_matches->SSO.ERROR | SSO.LOOKUP.CONTENT_TYPE | stop | A Common Lookup-backed parameter is updated | resolve_setup_option_common_lookup |

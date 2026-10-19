# Check-In Templates Reference Lookups

## Lookup Operation Notes

- Updating or deleting a template uses `find_check_in_template_by_id` to read
  its current lifecycle state.
- A review-period mode switch reads the complete review-period child collection
  before a batch-delete operation; stop if a required child key is missing or
  ambiguous.


## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_check_in_template_by_id | Updating or deleting a template | CheckInTemplateId | /latest/talentCheckInTemplates/{CheckInTemplateId} | CheckInTemplateId, Name, TemplateTypeCode, InUseFlag, Status, DateFrom, DateTo | Exact CheckInTemplateId | Current template state | No match: stop as missing. |
| resolve_check_in_template_status | Status is supplied | Status and LookupType=ACTIVE_INACTIVE | core.fusion-api.apps-common.lookups via /fscmRestApi/resources/11.13.18.05 selected lookup view | LookupCode, Meaning | Resolve the lookup category through the core skill, then match LookupCode exactly | Validated Status | No match: stop as invalid. |
| resolve_check_in_template_type | A template is created | Supplied TemplateTypeCode or inferred Touchpoints business meaning, and LookupType=ORA_HRA_CHECK_IN_TYPE | core.fusion-api.apps-common.lookups via /fscmRestApi/resources/11.13.18.05 selected lookup view | LookupCode, Meaning | Resolve the lookup category through the core skill. Match a supplied LookupCode exactly, or select the unique active meaning that represents Touchpoints for a monthly/quarterly recurring request. | Validated type | Stop if invalid, ambiguous, or no active Touchpoints type exists. |
| resolve_review_period | Specific review-period mode is used | ReviewPeriodId, ReviewPeriodName, or DateFrom for current-period intent | /hcmRestApi/resources/latest/reviewPeriodsLOV with StatusCode='A' | ReviewPeriodId, ReviewPeriodName, StartDate, EndDate, StatusCode | Match an exact active name or identifier; for current-period intent, select the unique active period whose start and end dates contain DateFrom. | ReviewPeriodId | Stop if invalid, ambiguous, duplicate for template, or no active period contains DateFrom. |
| resolve_role_questionnaire | Questionnaire fields are supplied | WorkerQuestionnaireId or ManagerQuestionnaireId | /hcmRestApi/resources/latest/questionnairesLOV with Status='A' and SubscriberId='1' | Id, subscriber code, scored status | Role-specific exact match | Valid questionnaire pairing and scored state | Stop if unavailable to role. |
| resolve_check_in_eligibility_profile | Eligibility Profile fields are supplied | EligibilityProfileId or name | /hcmRestApi/resources/latest/eligibilityProfilesLOV with StatCd='A' and AsmtToUseCd='APS' and ProfileType='PRTP' | EligyPrflId, Name, Description, StatCd | Exact match | EligibilityProfileId, RequiredFlag=false, TalentObjectType=CHECKIN | Stop if invalid. |
| resolve_manager_type | TeamSyncFlag is false | AllManagerTypesCode, ManagerTypes, LookupType=ORA_HRA_ALL_MANAGER_TYPES, and LookupType=PER_SUPERVISOR_TYPE | core.fusion-api.apps-common.lookups via /fscmRestApi/resources/11.13.18.05 selected lookup views | LookupCode, Meaning | Resolve each lookup category through the core skill. AllManagerTypesCode must be exactly `ORA_HRA_ALL_MANAGER_TYPES` or `ORA_HRA_SPECIFIC_MANAGER_TYPES`. When specific-manager-types is selected, split ManagerTypes on commas and match every nonblank code exactly against `PER_SUPERVISOR_TYPE`. | Validated AllManagerTypesCode and normalized comma-delimited ManagerTypes | Stop when the code is null or invalid, ManagerTypes is populated for all-manager-types, specific-manager-types has no ManagerTypes, or any comma-delimited manager type fails the `PER_SUPERVISOR_TYPE` lookup. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A REST read uses a template ID | Use only the documented GET endpoint and exact identity match. |
| Describe metadata is insufficient to resolve a lookup value | Stop and obtain the authoritative lookup request contract; do not infer a write or alternate endpoint. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| CHECKIN.RESOLVE_REFERENCES | step | 30 | reference_lookup | resolved->CHECKIN.APPLY_DEFAULTS;unresolved->CHECKIN.HANDLE_LOOKUP_ERROR | CHECKIN.CHECK_DEPENDENCIES | stop | A declared dependency has Lookup status |

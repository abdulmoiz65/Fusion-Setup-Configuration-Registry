# Check-In Templates Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Business scope | Extract the workforce population, manager participants, stated permissions, discussion topics, cadence, questionnaire intent, and related operational requirements. Apply safe defaults and identify only genuine business choices. |
| 2 | Template identity | Resolve the existing template by ID before update or delete. |
| 3 | Reference values | Resolve supplied status, type, review period, manager type, eligibility profile, and questionnaire values when applicable. |
| 4 | Lifecycle state | Confirm InUseFlag before applying update or delete restrictions. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CHECKIN.TEMPLATE_IDENTITY | Existing check-in template | Yes | Updating or deleting | Lookup | talentCheckInTemplates REST resource | find_check_in_template_by_id | Update and delete operate on the generated template identity. | Supply CheckInTemplateId and resolve its current lifecycle state. | CheckInTemplateId, InUseFlag, TemplateTypeCode, current values |
| CHECKIN.STATUS_CODE | Active/inactive status | Yes | Status is supplied | Lookup | Active/inactive lookup through template REST data | resolve_check_in_template_status | Status must be a valid active/inactive code. | Supply a valid status code. | Status |
| CHECKIN.TEMPLATE_TYPE | Check-in template type | Yes | Creating a template | Lookup | ORA_HRA_CHECK_IN_TYPE lookup through template REST data | resolve_check_in_template_type | Template type is required on create and controls applicability. | Supply a valid create-only template type. | TemplateTypeCode |
| CHECKIN.BUSINESS_SCOPE | Business population, participants, cadence, and discussion intent | Yes | Creating or materially changing a template | Intake | Business request or requirements document |  | These decisions determine eligibility, manager types, questionnaire handling, and the template type. | Infer stated requirements and safe defaults first. Ask only when the source explicitly conflicts, names an unsupported outcome, or leaves a material business choice unresolved; do not require Fusion object names. | intended population, line/project/other managers, recurring or annual-process use, questionnaire roles when selected |
| CHECKIN.REVIEW_PERIOD | Review period | Conditional | The request names the current or a specific review period | Lookup | ReviewPeriodPVO through reviewPeriods REST child | resolve_review_period | ReviewPeriodId is a required child reference in specific-period mode. | Resolve the period active on DateFrom for current, or distinct valid stated periods. | ReviewPeriodId, ReviewPeriodName |
| CHECKIN.QUESTIONNAIRE | Role-appropriate questionnaire | Conditional | QuestionnaireFlag is Y | Lookup | Worker or manager questionnaire search VO | resolve_role_questionnaire | Questionnaire IDs must be available to their specified role; scoring and score visibility must satisfy the documented dependent-field rules. | Resolve valid role-appropriate selections only after the requester elects to configure structured questions. | Questionnaire ID, subscriber code, WkrQstnrScoringFlag, MgrQstnrScoringFlag |
| CHECKIN.ELIGIBILITY_PROFILE | Eligibility profile | Conditional | Eligibility profiles are supplied or the business request names a restricted population | Lookup | Profiles REST child | resolve_check_in_eligibility_profile | Profile rows must be valid, distinct, and CHECKIN scoped. A restricted workforce must not be broadened by default. | Resolve the profile that represents the named population. If none exists, mark eligibility association as an activation/import prerequisite while retaining the safe blueprint. | Profile ID, TalentObjectType, RequiredFlag |
| CHECKIN.MANAGER_TYPE | Manager type | Conditional | TeamSyncFlag is false | Lookup | `PER_SUPERVISOR_TYPE` lookup data for specific manager types | resolve_manager_type | AllManagerTypesCode is required and controls ManagerTypes child consistency. | Use `ORA_HRA_ALL_MANAGER_TYPES` with ManagerTypes null only when the request explicitly includes all manager types. Use `ORA_HRA_SPECIFIC_MANAGER_TYPES` with a comma-delimited list of one or more manager types, each resolved against `PER_SUPERVISOR_TYPE`, when roles are named. | AllManagerTypesCode, ManagerTypes |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required template state or reference value resolves uniquely and meets its documented contract. | Yes |
| Missing | A required identifier or reference value has no match. | Yes |
| Ambiguous | A supplied selector resolves to more than one result where one is required. | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| CHECKIN.CHECK_DEPENDENCIES | step | 20 | resolve_dependency | ready->CHECKIN.RESOLVE_REFERENCES;missing->CHECKIN.HANDLE_DEPENDENCY_ERROR | CHECKIN.VALIDATE_INPUT | stop | A request supplies or depends on a template identity or reference value |

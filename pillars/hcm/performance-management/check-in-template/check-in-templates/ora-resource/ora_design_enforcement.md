# Check-In Templates Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate payload ownership | Reject generated, derived, and non-updateable fields from write payloads. |
| 2 | Enforce type and lifecycle state | Apply Team Sync, Touchpoints, Performance, and in-use template rules. |
| 3 | Enforce uniqueness | Enforce unique template names, one active Team Sync template, and one default Performance or Touchpoints template. |
| 4 | Enforce dependent-field invariants | Re-evaluate every applicable dependent-field rule after normalization. A contradictory supplied value, including one explicitly requested as a bypass, blocks the run. |
| 5 | Enforce child consistency | Apply review-period, manager-type, eligibility-profile, questionnaire, scoring, goal, topic, and transcript relationships. |
| 6 | Gate mutation | Require authorization and an exact target identity before create, update, or delete. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Business request names a restricted population | Blocker | resolve_check_in_eligibility_profile | Activation or import would use all workers, an unrelated profile, or no profile instead of a profile that represents the requested population. | Resolve or create the appropriate restricted-population profile before activation or import. Allow a clearly marked, non-activated blueprint to retain all other safe configuration. | Yes |
| Business request names line, project, or other specific manager roles | Blocker | resolve_manager_type | The payload uses all manager types or omits a stated manager role. | Resolve and set the stated specific manager types; ask only if their permissions differ or the business wording is ambiguous. | Yes |
| Business request explicitly selects structured questions or questionnaires | Blocker | resolve_role_questionnaire | QuestionnaireFlag is Y but participant roles or a role-valid questionnaire are missing. | Confirm who completes the questionnaire and cross-role visibility, then resolve a role-valid questionnaire. Do not block an optional questionnaire that remains off. | Yes |
| Business request includes monthly or quarterly cadence | Blocker | resolve_check_in_template_type | The resolved type is not Touchpoints and the source does not explicitly state annual-performance-process-only intent or another conflicting purpose. | Resolve the Touchpoints type. Do not ask a cadence-only request to choose a template type. | Yes |
| Business request requires performance goals, development goals, or general discussion | Blocker |  | The corresponding discussion-topic flags are absent or disabled. | Enable the stated topic flags and, when active goals must be available, enable the applicable goal auto-population behavior. | Yes |
| Request does not explicitly require nudges | Blocker |  | NudgesFlag is enabled solely by a default. | Set NudgesFlag to N unless the requester explicitly requests nudges. | Yes |
| Request states current review period | Blocker | resolve_review_period | AllReviewPeriodsFlag is Y or the resolved period is not active on DateFrom. | Use specific-period mode and the active period on DateFrom. | Yes |
| Request requires Outlook calendar behavior | Blocker |  | The blueprint silently selects ICS or claims that the template configures Outlook integration. | Ask whether the desired behavior is automated meeting creation/updates or ICS download, then record the corresponding related work item. | Yes |
| Creating or updating | Blocker |  | Name isn't unique, exceeds 400 characters, or Comments exceeds 4000 characters. | Use a unique valid name and compliant text lengths. | Yes |
| Creating Team Sync | Blocker | find_check_in_template_by_id | More than one active Team Sync template would exist. | Retain only one active Team Sync template. | Yes |
| Setting a default template | Blocker |  | More than one default Performance or Touchpoints template would exist. | Retain one default template for each applicable type. | Yes |
| Updating an in-use template | Blocker | find_check_in_template_by_id | The change affects questionnaire ID/display, DateFrom, Status, or Performance goal flags prohibited by entity validation. | Limit the change to fields allowed for the current in-use type and state. | Yes |
| Team Sync | Blocker |  | Payload retains fields that are not applicable to Team Sync. | Remove or normalize non-Team-Sync fields and apply maximumEndDate. | Yes |
| Touchpoints | Blocker |  | DisplayGeneralTopicFlag is changed, or TopicsPriorCheckInsFlag is enabled without OpenTopicsNoOfMonths. | Remove the irrelevant change or provide the required month value. | Yes |
| Questionnaire configuration | Blocker | resolve_role_questionnaire | QuestionnaireFlag is Y with neither questionnaire, or a supplied questionnaire is invalid for its role. | Supply role-valid questionnaire selections; dependent scoring and visibility fields are normalized by the defaulting rules. | Yes |
| Any dependent-field rule applies | Blocker |  | A normalized payload violates a required dependent value, or the request asks to retain a contradictory value by bypassing the rule. | Apply the required reset and re-evaluate all dependent-field rules. If any invariant remains unsatisfied, stop before preview, approval, import, or mutation; no request or approval can waive the rule. | Yes, only by making the payload compliant |
| Review periods | Blocker | resolve_review_period | Specific periods have no valid child or AllReviewPeriodsFlag is true with stale child rows. | Supply valid distinct children only for specific-period mode. | Yes |
| Manager types | Blocker | resolve_manager_type | AllManagerTypesCode is null or unsupported; `ORA_HRA_ALL_MANAGER_TYPES` has populated ManagerTypes; `ORA_HRA_SPECIFIC_MANAGER_TYPES` has null, empty, malformed, duplicate, or invalid ManagerTypes; or the selection conflicts with stated business participants. | Use `ORA_HRA_ALL_MANAGER_TYPES` only with ManagerTypes null. Use `ORA_HRA_SPECIFIC_MANAGER_TYPES` only with a comma-delimited list of one or more valid `PER_SUPERVISOR_TYPE` codes. | Yes |
| Eligibility | Blocker | resolve_check_in_eligibility_profile | Performance template has no eligibility profile, profiles are duplicate/non-CHECKIN scoped, or eligibility conflicts with a stated restricted workforce. | Supply at least one valid distinct CHECKIN profile that represents the requested population. | Yes |
| Delete | Blocker | find_check_in_template_by_id | Template is in use or caller lacks manage permission. | Do not delete; resolve lifecycle state or authorization first. | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_check_in_template_type | Creating a template or cadence requires a process-type decision | TemplateTypeCode and the confirmed recurring or annual-process intent | ora_reference_lookups.md |
| find_check_in_template_by_id | Updating, deleting, or checking in-use state | CheckInTemplateId, InUseFlag, TemplateTypeCode, current values | ora_reference_lookups.md |
| resolve_role_questionnaire | Questionnaire display or scoring is configured | Questionnaire ID, role availability, ScoredFlag | ora_reference_lookups.md |
| resolve_review_period | Specific review periods are configured | ReviewPeriodId, ReviewPeriodName | ora_reference_lookups.md |
| resolve_manager_type | TeamSyncFlag is false | AllManagerTypesCode, ManagerTypes | ora_reference_lookups.md |
| resolve_check_in_eligibility_profile | Eligibility profiles are configured | Profile ID, TalentObjectType, RequiredFlag | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| CHECKIN.ENFORCE_DEPENDENT_FIELD_INVARIANTS | step | 50 | design_enforcement | compliant->CHECKIN.ENFORCE_DESIGN;blocked->CHECKIN.HANDLE_DESIGN_ERROR | CHECKIN.APPLY_DEFAULTS | stop | Any Check-In Templates request for which a documented dependent-field rule applies |
| CHECKIN.ENFORCE_DESIGN | step | 60 | design_enforcement | compliant->CHECKIN.SUCCESS;blocked->CHECKIN.HANDLE_DESIGN_ERROR | CHECKIN.ENFORCE_DEPENDENT_FIELD_INVARIANTS | stop | Any Check-In Templates REST request covered by the supplied contract |

# Check-In Templates Defaulting Rules

## Create Defaults

Apply these values only when creating a Check-In Template and the input omits the field. An explicit requester value takes precedence unless a dependency rule below requires normalization.

| Field | Default Value |
|---|---|
| StatusCode | `A` |
| AllManagerTypesCode | `ORA_HRA_ALL_MANAGER_TYPES` |
| AllReviewPeriodsFlag | `Y` only when the request does not name the current or a specific review period |
| IncludeInPerfDocFlag | `Y` |
| ManagerCanCreateFlag | `Y` |
| ManagerCanDeleteFlag | `Y` |
| TemplateTypeCode | Resolved Touchpoints type when recurring monthly or quarterly intent is stated; otherwise resolve the type from the stated purpose |
| WorkerCanCreateFlag | `Y` |
| WorkerCanDeleteFlag | `Y` |
| NudgesFlag | `N` |
| AnytimeFeedbackFlag | `N` |
| CompetencyFlag | `N` |
| DevGoalsAutoPopulateFlag | `N` |
| DevelopedSkillFlag | `N` |
| DevelopingSkillFlag | `N` |
| DevelopmentGoalsFlag | `N` |
| GeneralDiscussionTopicFlag | `N` |
| PerfGoalsAutoPopulateFlag | `N` |
| PerformanceGoalsFlag | `N` |
| QuestionnaireFlag | `N` |
| RequestedFeedbackFlag | `N` |

## Business-Intent Defaults

Apply these defaults from an explicit business requirement. They are not
generic create defaults.

| Business Signal | Required Result |
|---|---|
| Request names the current review period | Set AllReviewPeriodsFlag to N and resolve the one period active on DateFrom. |
| Request names one or more review periods | Set AllReviewPeriodsFlag to N and resolve the stated distinct periods. |
| Request omits effective dates | Set DateFrom to the request date and DateTo to the supported far-future end date. Disclose both values in the blueprint. |
| Request includes monthly or quarterly recurring check-ins | Resolve the Touchpoints template type; do not create a cadence field or ask a type question unless the source explicitly conflicts. |
| Request requires performance goals, development goals, or general discussion | Enable the corresponding topic flags. Enable goal auto-population only when the request says active goals should be available in the check-in. |
| Request says a questionnaire may be required or treats it as optional | Keep QuestionnaireFlag N unless the requester elects to configure structured questions. |
| Request does not mention nudges | Keep NudgesFlag N. |

## Dependent-Field Rules

These are non-bypassable data invariants, not optional defaults. Apply them after create defaults and whenever the controlling field is supplied or changed, including when a request, approval, import artifact, or instruction explicitly asks to bypass them. A dependent reset overrides a contradictory supplied value. After normalization, reject the payload if any required dependent value is still inconsistent; do not preview, approve, import, or mutate the template.

| Controlling Condition | Required Dependent Values |
|---|---|
| `WkrQstnrScoringFlag = N` | `MgrCanViewWkrScoresFlag = N`; `WkrCanViewWkrScoresFlag = N` |
| `MgrQstnrScoringFlag = N` | `MgrCanViewMgrScoresFlag = N`; `WkrCanViewMgrScoresFlag = N` |
| `QuestionnaireFlag = N` | `MgrQstnrSubscriberCode = null`; `WkrQstnrSubscriberCode = null`; `HideMgrQstnrUntilMgrMarksAsDoneFlag = N`; `HideWkrQstnrUntilWkrMarksAsDoneFlag = N`; `MgrCanViewMgrScoresFlag = N`; `MgrCanViewWkrQstnrFlag = N`; `MgrCanViewWkrScoresFlag = N`; `MgrQstnrScoringFlag = N`; `WkrCanViewMgrQstnrFlag = N`; `WkrCanViewMgrScoresFlag = N`; `WkrCanViewWkrScoresFlag = N`; `WkrQstnrScoringFlag = N` |
| `PerformanceGoalsFlag = N` | `PerfGoalsAutoPopulateFlag = N` |
| `DevelopmentGoalsFlag = N` | `DevGoalsAutoPopulateFlag = N` |
| `TopicsPriorCheckInsFlag = N` | `OpenTopicsNoOfMonths = null` |
| `MgrCanViewWkrQstnrFlag = N` | `HideWkrQstnrUntilWkrMarksAsDoneFlag = N` |
| `WkrCanViewMgrQstnrFlag = N` | `HideMgrQstnrUntilMgrMarksAsDoneFlag = N` |
| `AllowTranscriptFlag = N` | `StoreTranscriptFlag = N`; `ShowConsentForTranscriptFlag = N` |
| `AllManagerTypesCode = ORA_HRA_ALL_MANAGER_TYPES` | `ManagerTypes = null` |
| `AllManagerTypesCode = ORA_HRA_SPECIFIC_MANAGER_TYPES` | `ManagerTypes` must contain one or more comma-delimited manager-type codes, each resolved from `PER_SUPERVISOR_TYPE` |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| CHECKIN.APPLY_DEFAULTS | step | 40 | apply_default | applied->CHECKIN.ENFORCE_DEPENDENT_FIELD_INVARIANTS;invalid->CHECKIN.HANDLE_INPUT_ERROR | CHECKIN.RESOLVE_REFERENCES | stop | A documented default or dependent-field reset applies |

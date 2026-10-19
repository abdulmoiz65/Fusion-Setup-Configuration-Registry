# Schedule Generation Profile Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Basic Details | Name, ScheduleProfileCode, ActiveStartDate | Stop | Provide all required Basic Details fields | Always | |
| Schedule | CycleInWeeks, StartDate, GenerationWindowEnds | Stop | Provide the required schedule values | Always | |
| Self-scheduling rotation enablement | SelfScheduledOpens, SelfScheduledEnds, and at least one selfSchedulingRotations child row | Stop | Provide both self-scheduling window values and at least one rotation row, or disable self-scheduling rotations | SelfSchedRotationEnabledFlag is true | |
| Staffing row | DepartmentId, TimezoneCode | Stop | Resolve department and time zone | A staffing or float-pool row is supplied | resolve_staffing_department |
| Person filter row | JobPositionMemberType and JobId or PositionId | Stop | Select a Job or Position and resolve its ID | A person filter is supplied | resolve_job_or_position |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Start Date equals Active Start Date | Reject conflicting values | Always | |
| Date format | Accept profile and child date values only in YYYY-MM-DD format | A date value is supplied | |
| Boolean serialization | Always convert every Boolean value to the exact lowercase literal true or false before generating a REST payload, workbook, DAT file, or upload archive. Never emit Python-style True or False values. | Any Boolean field is supplied or preserved in generated output | |
| Update baseline | Reject an update payload that was not constructed from a fresh resolve_current_schedule_profile result. Require the current parent ID and preserve every updated existing child's REST ID and surrogate user code. | Any update is requested | resolve_current_schedule_profile |
| Create duplicate check | Before requesting approval or creating a new profile, require `find_identical_schedule_profile_configuration` to compare the complete resolved and defaulted create configuration with current profiles and their populated child collections. Stop for an exact configuration match until the user explicitly chooses whether to create a separate profile. Do not run this check for an explicit duplicate operation. | Any create operation | find_identical_schedule_profile_configuration |
| Generation and self-scheduling windows | Reject GenerationWindowOpens, GenerationWindowEnds, SelfScheduledOpens, or SelfScheduledEnds when the value is less than 0 | Any generation or self-scheduling window value is supplied | |
| Draft or Submit action maps to status | Set IsDraftFlag to true for Draft; set IsDraftFlag to false for Submit or active mode | A create or update action includes a save mode | |
| Method Type requires auto-generation | Reject MethodTypeCode when AutoGenerateScheduleFlag is not true | MethodTypeCode is supplied | resolve_method_type |
| Notification reminder offset requires notification | Reject editable reminder offset when EmailNotificationFlag is not true | EmailNotificationDaysOffset is supplied | |
| Grace period mapping | Map Number of Minutes unchanged to GracePeriod. It is the minutes before and after scheduled start and end times that do not create time-card exceptions. | Grace period is supplied | |
| Start period, minutes before mapping | Map Number of Minutes Before unchanged to StartEarlyPeriod. | Start period, before value is supplied | |
| Start period, before violation mapping | Map Violation Type to StartEarlyViolationType. | Start period, before violation type is supplied | resolve_violation_type |
| Start period, minutes after mapping | Map Number of Minutes After unchanged to StartLatePeriod. | Start period, after value is supplied | |
| Start period, after violation mapping | Map Violation Type to StartLateViolationType. | Start period, after violation type is supplied | resolve_violation_type |
| End period, minutes before mapping | Map Number of Minutes Before unchanged to EndEarlyPeriod. | End period, before value is supplied | |
| End period, before violation mapping | Map Violation Type to EndEarlyViolationType. | End period, before violation type is supplied | resolve_violation_type |
| End period, minutes after mapping | Map Number of Minutes After unchanged to EndLatePeriod. | End period, after value is supplied | |
| End period, after violation mapping | Map Violation Type to EndLateViolationType. | End period, after violation type is supplied | resolve_violation_type |
| Shift-deviation period minute values | Accept non-negative whole-minute values for GracePeriod, StartEarlyPeriod, StartLatePeriod, EndEarlyPeriod, and EndLatePeriod. | Any mapped period value is supplied | |
| Allowed time-deviation requirement | Reject DeviationAllowTimeFlag=true when both DeviationAllowStartMinutes and DeviationAllowEndMinutes are blank. These allowance fields are independent of the Grace, Start period, and End period UI mappings. | DeviationAllowTimeFlag is true | |
| Coverage equals one day | Reject rows whose IntervalInMinutes times NumberOfIntervals do not total 1,440 minutes | Coverage intervals are supplied | |
| Include or Exclude code is resolved | Reject an unresolved IncludeExcludeRuleCode | Person filters are supplied | resolve_include_exclude_rule |
| Float-pool self-scheduling flag | Accept a Boolean IncludeFloatPoolForSelfSchedulingFlag; omit it when no value is supplied | Float-pool self-scheduling is configured | |
| Self-scheduling rotation requirements | Reject SelfSchedRotationEnabledFlag=true unless both SelfScheduledOpens and SelfScheduledEnds are supplied, each is 0 or greater, and at least one selfSchedulingRotations child row is included | SelfSchedRotationEnabledFlag is true | resolve_rotation_type |
| Rotation rows require enablement | Reject selfSchedulingRotations child rows when SelfSchedRotationEnabledFlag is not true | Any selfSchedulingRotations child row is supplied | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SGP.VALIDATE | step | 1 | validate_input | valid->SGP.DEPENDENCIES;invalid->SGP.ERROR | none | stop | Always |

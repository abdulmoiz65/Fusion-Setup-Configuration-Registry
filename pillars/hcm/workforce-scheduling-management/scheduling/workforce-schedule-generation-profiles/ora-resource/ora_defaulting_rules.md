# Schedule Generation Profile Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| StartDate | ActiveStartDate | StartDate is not supplied | No | |
| StartOfWorkWeekCode | Weekday derived from StartDate | StartDate is supplied | No | resolve_start_day |
| Weekend flags | Saturday and Sunday true; Monday through Friday false | No weekend selection is supplied | Yes | |
| DayStartTime | 00:00:00 | DayStartTime is not supplied | Yes | |
| profileCoverageIntervals | Create one child row: StartTime 00:00:00; Interval Length 4 hours mapped to IntervalInMinutes 240; NumberOfIntervals 6; StopTime derived as StartTime plus Interval Length times Number of Intervals, resulting in next-day 00:00 | No coverage rows are supplied during profile creation | Yes | |
| EmailNotificationDaysOffset | 7 | EmailNotificationFlag is true and no offset is supplied | Yes | |
| SelfSchedRotationEnabledFlag | false | No self-scheduling rotation selection is supplied | Yes | |
| SelfSchedRotationType | ORA_HTS_ROTATION_STATIC | A self-scheduling rotation type is enabled and no type is supplied | Yes | resolve_rotation_type |

## Complete Summary Default Reporting

Include a default in Defaults Applied only when this task actually applied it. Preserve every user-provided business value as a selected value and never label it as a default.

## Default Coverage-Interval Construction

When no coverage rows are supplied during profile creation, materialize one profileCoverageIntervals child record. Send StartTime 00:00:00, IntervalInMinutes 240, and NumberOfIntervals 6. StopTime is derived and read-only; do not require user input for it. The resulting end time is next-day 00:00.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SGP.DEFAULTS | step | 16 | apply_default | applied->SGP.DESIGN;not_applicable->SGP.DESIGN | SGP.LOOKUP.VIOLATION_TYPE | stop | After applicable reference resolution |

# Manage Facility Shifts input validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Shift identity | Name | Stop before preview | Ask for the shift name only. Do not ask for ShiftId; Fusion generates it and Name is the user-key alternative. | Creating a shift | |
| Time shift definition | ShiftTypeCode = TIME; ShiftDetailTypeCode = FLEX, PUNCH, or NONE; StartTime; EndTime; Duration; DurationUnit = DAYS, HOURS, MINUTES, or WEEKS | Stop before preview | Request the missing business value using the listed business field name. | Shift type is time | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Shift name | Accept Name as the user-provided identity. Do not collect ShiftId, HCMScheduleShiftId, or any other identifier from the user. | Creating a shift | |
| Start and end time format | Require each time in hh:mm AM or PM format, for example 09:00 AM and 05:00 PM. | StartTime or EndTime is supplied | |
| Duration unit values | Accept only DAYS, HOURS, MINUTES, or WEEKS. | DurationUnit is supplied | |
| Shift type values | Accept only TIME, DURATION, or ELAPSED. | ShiftTypeCode is supplied | |
| Time-shift detail values | For a TIME shift, require FLEX, PUNCH, or NONE. | ShiftTypeCode = TIME | |
| Duration consistency | Validate that supplied Duration agrees with the stated start and end times before preview. | StartTime, EndTime, and Duration are supplied | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SHIFT.VALIDATE_INPUT | step | 10 | validate_input | passed->SHIFT.DONE;failed->RETURN_ISSUES | none | stop | Creating or validating a facility shift |

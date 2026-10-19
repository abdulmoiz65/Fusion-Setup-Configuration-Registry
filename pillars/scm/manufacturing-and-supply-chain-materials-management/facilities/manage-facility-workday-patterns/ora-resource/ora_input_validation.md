# Manage Facility Workday Patterns input validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Pattern identity | Name | Stop before preview | Ask for the pattern name only. Do not request PatternId or another system-generated identifier. | Creating or validating a workday pattern | |
| Pattern definition | PatternTypeCode; LengthInDays | Stop before preview | Ask for the missing business value. | Creating or validating a workday pattern | |
| Shift associations | ShiftName for every associated shift; StartDay; EndDay | Stop before preview | Ask for each missing shift name or day value. Do not request ShiftId, PatternId, or PatternDetailId. | One or more shifts are associated with a pattern | resolve_shift_by_exact_name |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Pattern name | Accept Name as the user-provided identity. Do not collect PatternId or another system-generated identifier. | Creating or validating a workday pattern | |
| Shift name | Accept ShiftName as the user-provided association value. Do not collect ShiftId, PatternId, or PatternDetailId from the user. | A shift association is supplied | resolve_shift_by_exact_name |
| Shift-name uniqueness | Require each ShiftName once for the same pattern-day association unless the user explicitly supplies distinct day ranges. | More than one shift association is supplied | |
| Pattern type | Accept TIME, DURATION, or ELAPSED. | PatternTypeCode is supplied | |
| Pattern length | Require a positive whole number of days. | LengthInDays is supplied | |
| Pattern-day range | Require StartDay and EndDay to be positive whole numbers; require StartDay to be less than or equal to EndDay and within LengthInDays. | A shift association is supplied | |
| Date format | When a date attribute is supplied, require YYYY/MM/DD. Do not accept locale-dependent date text. | A date attribute is supplied by the selected loader schema | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WORKDAY_PATTERN.VALIDATE_INPUT | step | 10 | validate_input | passed->WORKDAY_PATTERN.DONE;failed->RETURN_ISSUES | none | stop | Creating or validating a facility workday pattern |

# Manage Facility Shifts error handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Missing shift name | Stop before preview and request the Name. Do not request any system-generated identifier. |
| Invalid time format | Stop before preview and request the time again in hh:mm AM or PM format. |
| Invalid duration unit, shift type, or shift detail type | Stop before preview and present the accepted values documented in input validation. |
| Duration conflicts with start and end times | Stop before preview and ask for corrected business values. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| User has provided a shift name | Do not request ShiftId, HCMScheduleShiftId, or another system-generated identifier. |
| Input validation fails | Do not create a preview, archive, upload, or load. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SHIFT.DONE | terminal | 20 | terminal | none | SHIFT.VALIDATE_INPUT | stop | Input validation passed |
| RETURN_ISSUES | terminal | 30 | terminal | none | none | stop | Input validation failed |

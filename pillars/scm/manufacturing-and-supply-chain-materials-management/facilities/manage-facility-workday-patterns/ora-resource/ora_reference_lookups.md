# Manage Facility Workday Patterns reference lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_shift_by_exact_name | A shift association is supplied | ShiftName | Data Loader workdayPatterns metadata contract | ShiftName | Match the supplied shift name exactly once | Validated ShiftName association | Stop before preview and ask for the shift name only. Do not ask the user for ShiftId or another identifier. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A user supplies a shift name | Resolve and validate the association by exact ShiftName through the selected Data Loader workflow. |
| A shift name cannot be resolved or is ambiguous | Stop before preview. Request a corrected shift name; never request an ID from the user. |

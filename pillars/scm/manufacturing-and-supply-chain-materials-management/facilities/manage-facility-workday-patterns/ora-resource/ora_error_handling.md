# Manage Facility Workday Patterns error handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Missing shift name | Stop before preview and request the ShiftName. Do not request ShiftId, PatternId, or PatternDetailId. |
| Shift name is unresolved or ambiguous | Stop before preview and ask for the corrected business name only. |
| Invalid date format | Stop before preview and request the date in YYYY/MM/DD format. |
| Invalid pattern-day range | Stop before preview and request StartDay and EndDay within the pattern length. |
| Fusion reports a loader error | Preserve the returned diagnostic, stop before retry, correct the source, revalidate the immutable archive, and require fresh approval. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A user provides a name | Do not request a system-generated ID as a substitute for Pattern Name or Shift Name. |
| Validation or lookup fails | Do not create a preview, archive, upload, or load. |
| A load fails | Do not replay the archive until the source or live metadata contract has been corrected, fresh validation passes, and the user approves the new exact archive. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WORKDAY_PATTERN.DONE | terminal | 20 | terminal | none | WORKDAY_PATTERN.VALIDATE_INPUT | stop | Input validation passed |
| RETURN_ISSUES | terminal | 30 | terminal | none | none | stop | Input validation failed |

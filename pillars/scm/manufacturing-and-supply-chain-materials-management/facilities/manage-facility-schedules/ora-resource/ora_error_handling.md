# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Fusion rejects EffectiveFromDate or EffectiveToDate because the value is not YYYY-MM-DD | Stop, show the affected date field, correct it to YYYY-MM-DD, create a new immutable preview, and obtain fresh approval before submission. |
| The backend cannot resolve PatternName to PatternId | Stop, disclose the lookup result, and ask only for a corrected or more specific pattern name. |
| Fusion reports PatternId is required | Treat this as a backend name-resolution failure; do not ask the user for PatternId or invent one. Stop before retry until the backend resolver is available or the user supplies a corrected PatternName. |
| A source value, preview, or backend behavior changes after approval | Invalidate the prior approval and require a new immutable preview and explicit approval. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A date is missing, out of range, or not YYYY-MM-DD | Correct the user-supplied date values and rebuild the preview. |
| Lookup resolution | PatternName has no match, many matches, or cannot be resolved by the backend | Ask for a corrected or more specific PatternName; never ask for PatternId. |
| Approval blocker | The payload or backend behavior changes after preview | Create a new immutable preview and request approval. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Date validation failure | The exact date field and the required YYYY-MM-DD format |
| Pattern lookup failure | The supplied PatternName, the resolution result, and the request for a corrected name only |
| Retry gate | That prior approval is invalid and a newly validated immutable payload requires approval |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| PatternId is unavailable or a lookup fails | Do not ask the user for PatternId, guess an ID, or substitute a similar pattern. |
| Date validation fails | Do not submit or retry the existing archive. |
| A preview is stale | Do not reuse its approval for a changed payload or changed backend behavior. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FAC_SCH.HANDLE_ISSUE | step | 4 | error_handler | disclosed->RETURN_ISSUES | none | stop | Prior node reports invalid, unresolved, ambiguous, blocked, or failed |
| FAC_SCH.DONE | terminal | 5 | terminal | none | FAC_SCH.ENFORCE_NAME_INPUT | stop | Create schedule passed all documented validation and name-resolution gates |
| RETURN_ISSUES | terminal | 6 | terminal | none | none | stop | Error disclosure complete |

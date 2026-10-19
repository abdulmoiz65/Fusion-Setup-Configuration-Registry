# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required identity or numbering inputs are missing | Stop the affected row and request only the missing values. |
| The surrogate user key derivation query has no match | Route the row to POST; do not create a synthetic DocumentNumberId. |
| The surrogate user key derivation query has many matches | Stop the affected row and resolve the duplicate identity before preview. |
| The intended operation conflicts with the lookup result | Stop the affected row and correct the operation: POST without DocumentNumberId, PATCH with the derived DocumentNumberId. |
| Data Loader preview or live processing returns an error | Preserve the affected row and the sanitized error details; stop before retrying or changing the operation. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required input or approval is absent | Collect the missing fact or approval and revalidate. |
| FAILED | The lookup is ambiguous, the determinant source is wrong, or Data Loader reports an error | Correct the recorded row and rerun preview; do not retry a live mutation automatically. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview failure | Affected row, validated Document Type, selected determinant-name source, lookup outcome, and proposed POST or PATCH route. |
| Live failure | Affected row, selected operation, derived DocumentNumberId when present, sanitized failure response, and the safe next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| DocumentNumberId is absent | Do not PATCH or invent an identifier. |
| DocumentNumberId exists | Do not POST a duplicate row. |
| Lookup is ambiguous or live processing is uncertain | Do not automatically retry, switch methods, or perform a direct REST write. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PDN.DONE_POST_ROUTE | terminal | 40 | terminal | none | PDN.ENFORCE_OPERATION_ROUTE | stop | The design gate selects POST |
| PDN.DONE_PATCH_ROUTE | terminal | 50 | terminal | none | PDN.ENFORCE_OPERATION_ROUTE | stop | The design gate selects PATCH |
| RETURN_ISSUES | terminal | 60 | terminal | none | none | stop | Any validation, lookup, or design gate blocks the row |

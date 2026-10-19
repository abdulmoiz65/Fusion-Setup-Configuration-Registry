# Content Type Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A completed same-task export baseline is unavailable, invalid, or has unclear required relationships | Stop before execution and obtain a completed export of the Redwood task. Inspect its metadata, CSV headers, identities, and parent-child relationships before preparing a package. |
| A visibility lookup has no documented request contract | Stop before applying restricted visibility and obtain the authoritative lookup contract. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| The exported baseline is unavailable or a required parent relationship is unclear | Do not construct or import a package from guessed member names, CSV columns, identifiers, or relationships. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CONTENT_TYPES_REDWOOD.BASELINE_CONTRACT | decision | 1 | execution_gate | ready->CONTENT_TYPES_REDWOOD.COMPLETE;unavailable_or_unclear->CONTENT_TYPES_REDWOOD.BLOCKED | none | stop | A content type create or update is requested |
| CONTENT_TYPES_REDWOOD.COMPLETE | terminal | 2 | terminal | none | CONTENT_TYPES_REDWOOD.BASELINE_CONTRACT | stop | The baseline package structure and required relationships are clear and all required validation passes |
| CONTENT_TYPES_REDWOOD.BLOCKED | terminal | 3 | terminal | none | CONTENT_TYPES_REDWOOD.BASELINE_CONTRACT | stop | The baseline is unavailable or a required package relationship remains unclear |

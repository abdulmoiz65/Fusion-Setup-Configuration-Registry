# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required class or base-UOM value is missing or exceeds the documented length | Stop and return the precise correction. |
| ClassCode or ClassName has a uniquely high-confidence probable spelling error | Stop before live lookup, preview, or write; show the original value, closest candidate, and edit distance, then require the user to confirm or replace the value. |
| ClassCode or ClassName is an individual UOM, matches the base UOM after normalization, or is a decorated form of it | Stop and direct the user to provide the broader UOM class/dimension. Do not infer a replacement. |
| The semantic role of the class label is uncertain | Stop and ask the user to identify the intended UOM class/dimension. |
| Exact class-code lookup fails or returns multiple matches | Stop before preview. Do not select a class or retry automatically. |
| The exact class code already exists | Stop creation and present the existing class identity. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Existing, ambiguous, or unresolved class identity | Do not create a duplicate class, substitute a different class, or retry a write automatically. |
| Probable typo | Do not silently correct the code or name, submit the existing approval archive, or treat the suggestion as user approval. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UMC.HANDLE_ISSUE | step | 5 | error_handler | disclosed->RETURN_ISSUES | none | stop | Prior node reports invalid, individual-unit, uncertain, ambiguous, existing, or failed |
| UMC.DONE | terminal | 6 | terminal | none | UMC.ENFORCE | stop | Creation passed all documented gates |
| RETURN_ISSUES | terminal | 7 | terminal | none | none | stop | Error disclosure complete |

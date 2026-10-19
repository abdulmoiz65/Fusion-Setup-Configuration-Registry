# Work Skills Design Validation Outcomes

## Error Situations

| Situation | What Should Happen |
|---|---|
| Workbook structure is incomplete | Stop before preview and identify the missing worksheet, column, or condition value |
| A design rule blocks | Stop before preview, identify the failing Work Skills rule, affected skill or condition where supplied, and the permitted correction |
| Routing or optimization evidence is absent for an advanced design | Stop before preview; do not claim end-to-end eligibility or optimization validation from workbook data alone |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| RETURN_ISSUES | Rule ID, blocking condition, affected workbook data when available, recommendation, and whether correction is allowed before preview |
| RETURN_READY_FOR_PREVIEW | The completed validation path and explicit statement that a separate preview and approval are required before any live change |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| RETURN_ISSUES | terminal | 11 | terminal | none | none | stop | A validation rule blocks or required workbook input is invalid |
| RETURN_READY_FOR_PREVIEW | terminal | 12 | terminal | none | WS.ADVANCED_VALIDATION | stop | All applicable design rules pass |

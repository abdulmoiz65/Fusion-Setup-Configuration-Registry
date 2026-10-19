# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| The registered BO template lacks rule-name, effective-start-date, or pricing-basis fields | Stop. Correct and publish the BO registration, then obtain a fresh template before preparing another load. |
| Fusion rejects a prepared load or reports a payload parse failure | Stop before retry. Retrieve the Data Loader error details and correct the identified contract or source issue. |
| The pricing-basis field contract is not documented | Stop. Do not infer a payload from an earlier test or a similarly named resource. |
| A supplied effective date is not ISO YYYY-MM-DD | Stop before preparing or retrying the load. Correct every supplied date-bearing source field to YYYY-MM-DD, then rebuild and revalidate the archive. |
| A basis-changing PATCH completes but AccountingTransferPriceBasis remains null | Read the persisted basis flags. If none is selected, correct the Data Loader source to use Y or N values with exactly one accounting-basis flag set to Y; omit derived fields, rebuild the archive, and obtain new approval before retrying. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Registration or metadata blocker | The live template omits fields needed for the requested rule | Correct the BO attribute registration and regenerate the template. |
| Contract blocker | The exact selected-basis field combination is unknown | Obtain authorized source material and update the task resource. |
| Fusion load failure | Fusion rejects an approved Data Loader submission | Retrieve the error details; do not retry the same load without correction and a new approval. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before source preparation | The confirmed template fields and any registration or contract blocker. |
| After a failed load | The actionable Fusion error and the corrected next step, without credentials or tokens. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TPR.HANDLE_ISSUE | step | 40 | error_handler | handled->TPR.DONE_ISSUES | none | stop | Any validation, readiness, or design rule returns a blocker |
| TPR.DONE_READY | terminal | 50 | terminal | none | TPR.ENFORCE_DESIGN | stop | Validation and design enforcement pass |
| TPR.DONE_UPDATE_READY | terminal | 55 | terminal | none | TPR.ENFORCE_UPDATE_DESIGN | stop | Update validation, target resolution, and design enforcement pass |
| TPR.DONE_ISSUES | terminal | 60 | terminal | none | TPR.HANDLE_ISSUE | stop | An issue has been classified and disclosed |

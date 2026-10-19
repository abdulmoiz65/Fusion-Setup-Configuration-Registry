# Resource Types Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Workbook input is missing, ambiguous, or invalid | Stop before preview, identify the affected worksheet, label, or conflicting selection, and request correction. |
| A Resource Type design rule blocks preview | Return the rule ID, blocking condition, and permitted correction; do not release the preview. |
| REST execution contract is incomplete | Stop before mutation and request the endpoint, API version, method, payload mapping, identity rule, preview contract, and read-back query. |
| A REST mutation result is uncertain | Do not retry automatically; require documented read-back reconciliation before any further mutation. |
| A PUT succeeds but its GET verification fails | Stop the sequence immediately, preserve a redacted partial-failure record, and do not send any remaining PUT. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Workbook intake is missing or invalid | Correct the workbook and rerun validation. |
| design_enforcement | An RT rule blocks the proposed model | Correct the model before preview. |
| execution_contract_missing | REST behavior is not documented | Supply the missing contract; do not infer it. |
| mutation_uncertain | A REST mutation outcome cannot be verified | Reconcile with documented read-only verification; do not replay the mutation. |
| partial_execution | A request failed or verification failed after an earlier request may have applied | Stop; read back the affected object; prepare an approved recovery or continuation preview. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A design rule blocks preview | Do not bypass the rule or replace it with a generic recommendation. |
| REST contract is incomplete | Do not construct an endpoint, payload, browser workflow, or substitute import route. |
| A write outcome is uncertain | Do not automatically POST, PATCH, PUT, or DELETE again. |
| A partial execution is detected | Do not send later requests, auto-rollback, or reuse the prior approval checksum. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RT.RETURN_SUCCESS | terminal | 12 | terminal | none | RT.CHECK_CONTRACTOR_SEPARATION | stop | The applicable Resource Type design rules pass |
| RT.RETURN_ISSUES | terminal | 13 | terminal | none | none | stop | Workbook validation or design enforcement returns a blocker |

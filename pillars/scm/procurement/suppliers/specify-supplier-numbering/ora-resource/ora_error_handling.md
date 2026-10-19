# Specify Supplier Numbering Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| The Supplier Numbering row is missing | Prepare the approved minimal `supplierNumberingInitializeSetup` Data Loader POST artifact, submit it once after approval, then re-read and validate the resulting row |
| The row lookup is zero, multiple, or has a non-supplier identity | Stop and disclose the sanitized lookup result; do not select a row or construct a substitute execution route |
| The requested value is at or below the current maximum | Stop unless the current explicit rollback approval and collision evidence apply |
| Initialization, Data Loader update, or verification fails | Preserve redacted outcome evidence; reconcile with a fresh read before considering another submission |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Requested number is missing, nonnumeric, zero, or over 18 digits | Correct the requested value |
| Row readiness | Supplier Numbering row is absent or ambiguous | Use the approved `supplierNumberingInitializeSetup` Data Loader POST artifact or resolve duplicate state |
| Rollback safety | Requested number is at or below the current maximum without required evidence | Obtain explicit approval and collision evidence |
| Execution processing | An initialization or Data Loader update outcome that is failed or uncertain | Stop before retry and reconcile through a fresh read |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Supplier Numbering mutation | Do not bypass the approved Data Loader workflow |
| Missing row | Do not hand-author a payload or use a substitute execution route |
| Uncertain processing result | Do not resubmit until read-only reconciliation establishes the current row state |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SN.CREATE_GATE | step | 70 | execution_gate | ready->SN.DONE_CREATED;not_ready->SN.HANDLE_ERROR | SN.APPLY_INITIAL_DEFAULT | stop | Before the `supplierNumberingInitializeSetup` Data Loader POST handoff for a missing row |
| SN.UPDATE_EXISTING_GATE | step | 71 | execution_gate | ready->SN.DONE_EXISTING;not_ready->SN.HANDLE_ERROR | SN.ENFORCE_EXISTING | stop | Before the Data Loader update handoff for an existing row |
| SN.HANDLE_ERROR | step | 80 | error_handler | handled->SN.RETURN_ISSUES | none | stop | Any validation, lookup, initialization, Data Loader update, or verification failure |
| SN.RETURN_ISSUES | terminal | 90 | terminal | none | none | stop | A blocking issue was disclosed |
| SN.DONE_CREATED | terminal | 100 | terminal | none | SN.CREATE_GATE | stop | The approved missing-row `supplierNumberingInitializeSetup` Data Loader POST handoff is ready |
| SN.DONE_EXISTING | terminal | 101 | terminal | none | SN.UPDATE_EXISTING_GATE | stop | The approved existing-row Data Loader update handoff is ready |

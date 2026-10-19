# Specify Supplier News Content Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required content or supplierNewsContent Data Loader REST artifact is missing | Stop and return the missing-input details. |
| A proposed route is not supplierNewsContent Data Loader REST | Stop and return the route blocker. |
| The supplier news content row is missing | Prepare the approved minimal `supplierNewsContentInitializeSetup` Data Loader REST POST artifact, submit it once after approval, then re-read and require exactly one row. |
| Initialization is failed or uncertain | Preserve the redacted outcome evidence, reconcile with a fresh read, and do not retry automatically. |
| A Data Loader REST import result is not available | Do not infer a successful update; obtain the Data Loader result through the selected import workflow. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| The task is ready for import | Do not perform, describe, or imply a direct content update from this task resource. |
| A read operation is needed | Do not model it as an update; any future ADF REST rule must be a read-only reference lookup with a documented request contract. |
| The singleton row is absent | Do not create a row through `supplierNewsContent`; use only the approved `supplierNewsContentInitializeSetup` Data Loader REST POST artifact. |
| A direct creation is requested | Do not create through `supplierNewsContent`, a raw REST `POST`, or another integration route; reject the request and retain only the approved initialization branch. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | What Must Be Shown |
|---|---|---|---|---|---|---|---|---|
| POZ.SNC.DATALOADER_GATE | step | 50 | execution_gate | ready->POZ.SNC.DATALOADER_READY;blocked->POZ.SNC.RETURN_ISSUES | POZ.SNC.ENFORCE_DATALOADER_ROUTE | stop | Before routing the task for import | Confirm that the only planned update route is the task-scoped supplierNewsContent Data Loader REST artifact handled by core.data-loader |
| POZ.SNC.INITIALIZE_GATE | step | 45 | execution_gate | ready->POZ.SNC.INITIALIZATION_READY;blocked->POZ.SNC.RETURN_ISSUES | POZ.SNC.LOOKUP_CURRENT_NEWS | stop | Before the supplierNewsContentInitializeSetup Data Loader REST POST handoff for a missing row | Confirm the minimal initialization artifact is the only planned mutation and requires Data Loader approval |
| POZ.SNC.INITIALIZATION_READY | terminal | 55 | terminal | none | POZ.SNC.INITIALIZE_GATE | stop | The approved missing-row initialization handoff is ready | Return the validated `supplierNewsContentInitializeSetup` Data Loader REST POST artifact; re-read before preparing any update |
| POZ.SNC.DATALOADER_READY | terminal | 60 | terminal | none | POZ.SNC.DATALOADER_GATE | stop | The Data Loader REST handoff is ready | Return the validated task package for the selected Data Loader REST workflow |
| POZ.SNC.RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | Validation, route enforcement, or handoff readiness fails | Return the applicable missing-input or Data Loader REST route blocker |

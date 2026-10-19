# Configure Supplier Notifications Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required notification timing values or the `supplierOptions` Data Loader REST artifact are absent or invalid | Stop and return the missing or invalid information; do not process the artifact. |
| The read-only Supplier Options singleton query returns no row or multiple rows | Stop and return the lookup result; correct the singleton configuration before retrying. |
| The requested configuration is not approved for Data Loader REST processing | Stop and require an approved `supplierOptions` Data Loader REST artifact. |
| A shared supplierOptions artifact includes another task's attribute or a stale row | Stop, re-read the singleton after the preceding task completes, and prepare a new artifact containing only NotifyPriorToExpirationDays and ReminderFrequencyDays. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Missing input | A timing value or `supplierOptions` Data Loader REST artifact is absent. | Supply the missing information and restart validation. |
| Lookup failure | The read-only singleton query fails or does not resolve exactly one row. | Correct the singleton configuration and restart validation. |
| Processing gate blocked | The `supplierOptions` Data Loader REST artifact is not approved. | Approve the artifact and restart validation. |
| Shared singleton conflict | The artifact contains another task's field or the baseline is stale. | Resolve the sequence, refresh the lookup, and rebuild this task's two-field artifact. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before Data Loader REST processing | The validated timing values, resolved singleton row, and approved `supplierOptions` Data Loader REST artifact. |
| On a validation stop | The failed validation or lookup and the required next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Supplier notification timing configuration change | Do not process the change outside the `supplierOptions` Data Loader REST workflow. |
| Shared supplierOptions row | Do not run this task in parallel with Configure Supplier Registration or Configure Supplier Profile Change Request, and do not include their attributes in this task's artifact. |
| Validation, lookup, or approval failure | Do not submit or retry Data Loader processing until the issue is resolved. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POZ.SN.DATALOADER_GATE | step | 50 | execution_gate | ready->POZ.SN.RETURN_READY;blocked->POZ.SN.RETURN_ISSUES;failure->POZ.SN.RETURN_ISSUES | POZ.SN.ENFORCE_DATALOADER_ROUTE | stop | The approved supplier notification timing configuration is ready for `supplierOptions` Data Loader REST processing |
| POZ.SN.RETURN_READY | terminal | 60 | terminal | none | POZ.SN.DATALOADER_GATE | stop | The approved configuration is ready for `supplierOptions` Data Loader REST processing |
| POZ.SN.RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | Input validation, lookup, design enforcement, or processing approval cannot proceed |

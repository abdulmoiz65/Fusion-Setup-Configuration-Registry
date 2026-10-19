# Configure Supplier Notifications Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Data Loader REST artifact | Prepare and approve the task-specific `supplierOptions` notification timing artifact. |
| 2 | Current notification timing | Resolve the existing timing values through the read-only ADF REST lookup. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| approved_dataloader_artifact | Approved `supplierOptions` Data Loader REST artifact | Yes | A supplier notification timing change is requested | Verify | Approved implementation artifact | | Notification timing updates are processed only through Data Loader REST. | Prepare and approve the task-specific `supplierOptions` Data Loader REST artifact before processing. | Approved artifact reference |
| current_notification_timing | Current notification timing | Yes | A supplier notification timing change is requested | Lookup | Read-only ADF REST Supplier Options singleton query | resolve_supplier_notification_timing | The current values provide the configuration baseline for validation and post-load verification. | Query the Supplier Options collection and require exactly one row. | NotifyPriorToExpirationDays, ReminderFrequencyDays |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | The `supplierOptions` Data Loader REST artifact is approved and the notification timing resolves once. | Read-only lookup only; no create or update. |
| Missing dependency | The artifact is absent. | Stop until the task-specific Data Loader REST artifact is prepared. |
| Invalid dependency | The lookup does not resolve exactly one Supplier Options configuration. | Read-only lookup only; stop before Data Loader processing. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POZ.SN.CHECK_DEPENDENCIES | step | 20 | resolve_dependency | ready->POZ.SN.LOOKUP_CURRENT_TIMING;missing->POZ.SN.RETURN_ISSUES;invalid->POZ.SN.RETURN_ISSUES;failure->POZ.SN.RETURN_ISSUES | POZ.SN.VALIDATE_CHANGE_PACKAGE | stop | A supplier notification timing change is requested |

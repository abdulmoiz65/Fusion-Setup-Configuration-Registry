# Configure Supplier Notifications Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Notification timing configuration | NotifyPriorToExpirationDays and ReminderFrequencyDays | Stop preparation | Supply both values in the `supplierOptions` Data Loader REST artifact. | A supplier notification timing change is requested | |
| Data Loader route | Approved `supplierOptions` Data Loader REST artifact for Configure Supplier Notifications | Stop preparation | Prepare the task-specific artifact for Data Loader processing. | A supplier notification timing change is requested | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Expiration notification lead time | Accept NotifyPriorToExpirationDays only as a positive whole number. | A supplier notification timing change is requested | |
| Reminder frequency | Accept ReminderFrequencyDays only as a positive whole number. | A supplier notification timing change is requested | |
| Notification timing pair | Require both notification timing values in the same approved `supplierOptions` Data Loader REST artifact. | A supplier notification timing change is requested | |
| Shared supplierOptions attribute ownership | Accept only NotifyPriorToExpirationDays and ReminderFrequencyDays; reject every Supplier Registration and Supplier Profile Change Request attribute. | A `supplierOptions` Data Loader REST artifact is supplied | resolve_supplier_notification_timing |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POZ.SN.VALIDATE_CHANGE_PACKAGE | step | 10 | validate_input | valid->POZ.SN.CHECK_DEPENDENCIES;missing->POZ.SN.RETURN_ISSUES;invalid->POZ.SN.RETURN_ISSUES | none | stop | A supplier notification timing change is requested |

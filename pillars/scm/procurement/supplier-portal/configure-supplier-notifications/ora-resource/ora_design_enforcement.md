# Configure Supplier Notifications Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate notification timing | Confirm both timing values are positive whole numbers. |
| 2 | Verify current configuration | Confirm the read-only Supplier Options lookup resolves exactly one configuration. |
| 3 | Shared singleton coordination | Require exclusive ownership of NotifyPriorToExpirationDays and ReminderFrequencyDays, serial execution, and a fresh lookup after an earlier shared task completes. |
| 4 | Approve Data Loader REST artifact | Continue only with the approved task-specific `supplierOptions` artifact. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A supplier notification timing change is requested | Blocking | resolve_supplier_notification_timing | Either timing value is absent or is not a positive whole number. | Correct both timing values in the `supplierOptions` Data Loader REST artifact. | Yes |
| A supplier notification timing change is requested | Blocking | resolve_supplier_notification_timing | The Supplier Options singleton query does not resolve exactly one configuration. | Correct the singleton configuration, then rerun the read-only query. | Yes |
| A supplier notification timing change is requested | Blocking | | The change is not represented by an approved `supplierOptions` Data Loader REST artifact. | Prepare and approve the artifact before Data Loader processing. | Yes |
| A shared supplierOptions artifact is prepared | Blocking | resolve_supplier_notification_timing | The artifact contains any registration or profile-change attribute, or was prepared from a row read before an earlier shared task completed. | Re-read the shared singleton and prepare a new artifact containing only NotifyPriorToExpirationDays and ReminderFrequencyDays. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_supplier_notification_timing | Before approval of a supplier notification timing configuration. | NotifyPriorToExpirationDays, ReminderFrequencyDays. | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POZ.SN.ENFORCE_DATALOADER_ROUTE | step | 40 | design_enforcement | compliant->POZ.SN.DATALOADER_GATE;blocked->POZ.SN.RETURN_ISSUES;failure->POZ.SN.RETURN_ISSUES | POZ.SN.LOOKUP_CURRENT_TIMING | stop | A supplier notification timing change is prepared for `supplierOptions` Data Loader REST processing |

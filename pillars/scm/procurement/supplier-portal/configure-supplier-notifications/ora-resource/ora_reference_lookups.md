# Configure Supplier Notifications Reference Lookups

## Live Lookups

| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| POZ.SN.LOOKUP_CURRENT_TIMING | resolve_supplier_notification_timing | A supplier notification timing change is requested. | None. | `core.fusion-api.rest-api-client` GET `/fscmRestApi/resources/11.13.18.05/supplierOptions?onlyData=true&limit=2&fields=SupplierOptionsConfigId,NotifyPriorToExpirationDays,ReminderFrequencyDays`. | SupplierOptionsConfigId, NotifyPriorToExpirationDays, ReminderFrequencyDays. | Return exactly one Supplier Options row; no identifier filter is supplied. | Resolved singleton key, NotifyPriorToExpirationDays, ReminderFrequencyDays. | Stop; correct the singleton configuration before retrying. |

## Shared Collection Ownership

| Collection | This Task Owns | Other Task Ownership | Shared-row Rule |
|---|---|---|---|
| supplierOptions | NotifyPriorToExpirationDays, ReminderFrequencyDays | Configure Supplier Registration owns registration attributes; Configure Supplier Profile Change Request owns InternalChangeBankAccAttachmentsRequiredFlag and SupplierPortalChangeBankAccAttachmentsRequiredFlag | Resolve exactly one shared singleton, run the tasks serially, re-read after an earlier task completes, and include only this task's two timing attributes in the Data Loader REST artifact. |

## Lookup Execution Rules

Run the lookup through `core.fusion-api.rest-api-client` using its standard
Fusion REST client. Request at most two rows so the task can distinguish the
required singleton from an invalid multi-row response. This GET is read-only;
do not use the client for any mutation.

| Situation | What Happens |
|---|---|
| Current notification timing must be verified | Run only the documented read-only ADF REST singleton query. |
| The singleton query resolves one row | Use the returned timing values as validation and post-load-verification evidence for the `supplierOptions` Data Loader REST artifact. |
| Configure Supplier Registration or Configure Supplier Profile Change Request completed first | Re-run the read-only lookup before artifact preparation and retain only NotifyPriorToExpirationDays and ReminderFrequencyDays. |
| The singleton query fails or does not resolve exactly one row | Stop before Data Loader processing; do not substitute another lookup. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POZ.SN.LOOKUP_CURRENT_TIMING | step | 30 | reference_lookup | resolved->POZ.SN.ENFORCE_DATALOADER_ROUTE;not_found->POZ.SN.RETURN_ISSUES;ambiguous->POZ.SN.RETURN_ISSUES;failure->POZ.SN.RETURN_ISSUES | POZ.SN.CHECK_DEPENDENCIES | stop | A supplier notification timing change is requested |

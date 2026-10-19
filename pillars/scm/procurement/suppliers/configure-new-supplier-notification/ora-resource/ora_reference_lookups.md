# Configure New Supplier Notification ADF REST Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_supplier_notification_option | A notification-enable decision is planned, and again after an earlier shared `supplierOptions` task succeeds | None | `core.fusion-api.rest-api-client` GET `/fscmRestApi/resources/11.13.18.05/supplierOptions?onlyData=true&limit=2&fields=SupplierOptionsConfigId,EnableNewSupplierNotificationFlag` | SupplierOptionsConfigId, EnableNewSupplierNotificationFlag | Return exactly one seeded Supplier Options row; no identifier filter is supplied. | Resolved singleton key and current enablement value | Stop on zero rows or multiple rows; do not create a singleton row. |
| resolve_global_supplier_notification | GLOBAL email content is changed | TaxCountryCode = GLOBAL | `core.fusion-api.rest-api-client` GET `/fscmRestApi/resources/11.13.18.05/newSupplierNotification?onlyData=true&limit=2&q=TaxCountryCode%20%3D%20%27GLOBAL%27&fields=NewSupplierNotificationId,TaxCountryCode,EmailSubject,EmailBody` | NewSupplierNotificationId, TaxCountryCode, EmailSubject, EmailBody | Return exactly one GLOBAL notification. | Resolved global notification key and current content | Stop on zero rows or multiple GLOBAL rows; do not create a global notification in this task. |
| inspect_supplier_notification_attachments | Attachments are requested, including post-upload verification | Explicit GLOBAL or two-letter TaxCountryCode; resolve zero/one/many current rows. One is reused, zero non-GLOBAL selects a reviewed create, and many block | Task-specific adapter through core.fusion-api.rest-api-client GET territoriesLOV with q=TerritoryCode='<code>', newSupplierNotification with q=TaxCountryCode='<code>', its collection describe for creation, and the resolved attachment child collection/describe for reuse | Child discriminator, parent linkage, operation support, file-content type/transport, generated and mandatory keys; existing AttachedDocumentId, FileName, Title, UploadedFileContentType and file-content read links when advertised | Use bounded paging; resolve the selected country only. Require POST create and generated IDs for the missing parent and attachment child, with attachment-typed FileContents. Use nested child metadata before parent creation. Reject duplicate adds; replacement/deletion remain out of scope. | Current parent/child identity, live attributes, operation and file transport evidence, verification links | Stop on missing GLOBAL, an ambiguous country, unsupported parent/child create identity, or missing byte transport. Do not substitute HCM metadata or a different supplier resource. |

## Lookup Execution Rules

### Attachment Create Contract Evidence

For the HCM-aligned attachment-add design, inspect the exact resolved supplier
notification child, not `hrDocumentTypes`. Capture collection `create`/`POST`,
`FileContents` with attachment type, and whether `AttachedDocumentId` is
generated. Only map create-capable live fields; potential supplier fields are
`DatatypeCode`, `FileName`, `Title`, `UploadedFileName`,
`UploadedFileContentType`, and `FileContents`. Require the actual describe
contract before using any of them. Resolve the supplied filename across the
necessary child pages to reject duplicate adds. A valid REST contract proves
service capability; the declared task adapter still requires exact-file approval.

| Situation | What Happens |
|---|---|
| The current enablement state is unknown | Resolve the `supplierOptions` singleton through `core.fusion-api.rest-api-client` before preparing its Data Loader REST artifact. |
| Global email content is changed | Resolve the GLOBAL `newSupplierNotification` record through `core.fusion-api.rest-api-client` before preparing its Data Loader REST artifact. |
| A configuration update is requested | Use each read-only result only as validation evidence. Prepare the approved task-specific Data Loader REST artifacts and obtain explicit approval immediately before import. |
| Attachments are requested | Resolve the selected country through territoriesLOV (GLOBAL excepted). Reuse one row; for zero non-GLOBAL matches inspect collection POST create, generated parent identity, and nested attachment create. Include parent and files in one immutable preview and obtain combined approval. Multiple matches or missing GLOBAL block. |
| An attachment upload has completed | Re-read the resolved parent and child collection. Verify the requested add and preservation of unrequested content; use advertised file-content reads to verify bytes where supported. Do not automatically replay an uncertain mutation. |

These ADF REST reads are lookup guidance, not mutation authorization.
Notification enablement and content updates use the supplierOptions and
newSupplierNotification Data Loader business objects through core.data-loader.
Country documents use the declared combined Python adapter through Core OAuth
and REST primitives. The approved immutable preview covers any missing-country
creation and every reviewed file upload. Do not derive import columns from UI artifacts or issue
a direct parent PATCH or use the combined create for email/enablement changes.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| POZ.NSN.LOOKUP_CURRENT_STATE | step | 20 | reference_lookup | resolved->POZ.NSN.DATALOADER_GATE;not_found->POZ.NSN.RETURN_ISSUES;ambiguous->POZ.NSN.RETURN_ISSUES;failure->POZ.NSN.RETURN_ISSUES | POZ.NSN.VALIDATE_INPUT | stop | A notification enablement, global content, or document update is requested. |

# Configure New Supplier Notification Functional Rules

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| New supplier notification policy | EnableNewSupplierNotificationFlag in the `supplierOptions` Data Loader artifact | Block the enablement update | Resolve exactly one current Supplier Configuration Options record | Enablement is changed | resolve_supplier_notification_option |
| Global notification content | EmailSubject and EmailBody in the `newSupplierNotification` Data Loader artifact | Block the content update | Resolve the existing `TaxCountryCode = GLOBAL` notification | Email content is changed | resolve_global_supplier_notification |
| Required email content | EmailSubject and EmailBody | Block notification enablement | Supply both subject and body content | EnableNewSupplierNotificationFlag is true | |
| Supplier-facing notification documents | Requested operation, explicit GLOBAL or country scope, actual file and reviewed file metadata for an add or replacement; exact existing child selector for replacement or deletion | Block only the document operation | Resolve the selected country; when a non-GLOBAL row is absent, include its live-contract-validated REST create and all files in one combined preview. Never substitute GLOBAL. Ask only for missing country/file assignments or required create fields. | Supporting documents are explicitly requested | inspect_supplier_notification_attachments |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Notification enablement | Accept a boolean EnableNewSupplierNotificationFlag value in the `supplierOptions` artifact. When true, Fusion sends the email notification to all supplier contacts with valid email addresses when suppliers are registered or promoted to spend-authorized status. | Notification enablement is changed | resolve_supplier_notification_option |
| Notification content | EmailSubject and EmailBody are required when notification is enabled. EmailBody supports rich text. | EnableNewSupplierNotificationFlag is true | |
| Supporting documents | A document may be Global or country-specific. Select the supplier Taxpayer Country first, then Tax Registration Country, and use Global documents when neither country is defined. | Supporting documents are included | |
| Shared supplierOptions ownership | Accept only EnableNewSupplierNotificationFlag in this task's `supplierOptions` artifact; reject every Registration, Profile Change Request, and Configure Supplier Notifications attribute. | A `supplierOptions` update is supplied | resolve_supplier_notification_option |
| Attachment input | Require a readable nonempty file for an add or replacement, preserve the requested filename and title, and determine MIME type from the actual file. Validate every file before the combined preview; reject unsafe paths, missing files, and duplicate batch filenames. Do not require a file for a delete. | A file attachment mutation is requested | |
| Attachment schema | For existing rows inspect the child create contract; for missing non-GLOBAL rows require parent POST create with generated identity and validate the nested attachment contract before any write. Do not copy HCM attributes, invent Title or FileName keys, or ask for a generated AttachedDocumentId. Unsupported create identity blocks the add. | A document artifact is prepared | inspect_supplier_notification_attachments |
| Omitted values | Attachments are optional. Do not require an enablement change, resubmit unchanged email content, or clear existing documents for an attachment-only request. Use current email content as validation evidence when enabling without changing content. | Partial updates are supplied | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | What Happens |
|---|---|---|---|---|---|---|---|---|
| POZ.NSN.VALIDATE_INPUT | step | 10 | validate_input | valid->POZ.NSN.LOOKUP_CURRENT_STATE;invalid->POZ.NSN.RETURN_ISSUES | none | stop | Before configuration or attachment preparation | Validate only requested changes; retain unresolved live-state requirements for the lookup step. For attachment mutations validate the operation, parent scope, file inputs, and existing-child selector as applicable. |

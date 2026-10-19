# Configure New Supplier Notification Functional Error Handling

## Execution Gate

## Public Mutation Approval Gate

| Situation | What Must Be Shown | What Must Not Happen | Next Action |
|---|---|---|---|
| Data Loader REST notification update is requested | Confirm the target environment, validated immutable `supplierOptions` and/or `newSupplierNotification` artifact, and the requested notification values. | Do not PATCH either business object, infer a Data Loader payload from a read-only lookup, or import without explicit approval immediately before submission. | Submit only the approved artifact or artifacts through `core.data-loader`, then verify with the selected read-only lookup. |
| Supporting documents are requested | Include the country, create-or-reuse parent decision, parent fields and all file metadata in one immutable REST preview. Require current child metadata, supported transport, and route-specific approval. The product size limit is guidance, not a mandatory local aggregate-size gate. | Do not treat BO publication as upload validation, reuse a loader approval for REST, copy the HCM adapter, or silently change routes. | Use the combined country-document adapter after one approval; stop if either parent or child contract is unsupported. Report a Fusion size-limit rejection without automatic retry. |

## Error Situations

For an HCM-aligned combined preview, retain the exact environment, country/parent,
endpoint, operation, reviewed file metadata, file/payload hashes, selected
executor fingerprint, and contract evidence. Never include the file bytes in
the user-facing report. A changed approval-bound artifact or execution context
requires a new preview and approval under the selected route's rules. Service
support for REST create without a permitted executor is an execution-route gap,
not an invalid file or a missing user-provided attachment ID.

| Situation | What Should Happen |
|---|---|
| Attachment child or POST create is absent from the live REST contract | Stop the document operation; do not invent an endpoint or use another object's contract. |
| Attachment-type FileContents or generated AttachedDocumentId is unsupported | Stop before preview; do not invent an ID, substitute loader packaging, or use a browser fallback. |
| A same-name attachment already exists | Report the conflict and ask only whether an explicit replacement is intended; resolve that child before a new preview. Never overwrite on an add request. |
| Country creation or a file succeeds but a later upload fails | Report partial success with the retained parent and each file's state. Stop remaining uploads. Reconcile before a new approval for only missing operations; never delete/recreate the parent or resend successful files automatically. |
| Load is accepted but file verification is unavailable | Report submission or completion separately from attachment verification. Retrieve applicable Core status/errors and inspect fresh child state; do not claim that bytes were verified. |
| Diagnostics contain document contents or authentication material | Keep binary/base64 content, credentials, tokens, and full sensitive payloads out of reports and reusable files. Retain only the sanitized failure stage and permitted identifiers. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | What Must Be Shown |
|---|---|---|---|---|---|---|---|---|
| POZ.NSN.DATALOADER_GATE | step | 30 | execution_gate | ready->POZ.NSN.RETURN_READY;blocked->POZ.NSN.RETURN_ISSUES;failure->POZ.NSN.RETURN_ISSUES | POZ.NSN.LOOKUP_CURRENT_STATE | stop | Before configuration or attachment preview | Use Core's approval gate for ordinary configuration and one combined REST approval for country creation plus files. For documents require live parent/child identity, POST create with attachment-type FileContents, validated file inputs, and preservation of unrequested fields. Unsupported file transport blocks documents, not unrelated email-only operations. |
| POZ.NSN.RETURN_READY | terminal | 40 | terminal | none | POZ.NSN.DATALOADER_GATE | stop | The configuration artifact or attachment preview is ready for its approval gate | Return the validated artifact and target-specific approval requirement. |
| POZ.NSN.RETURN_ISSUES | terminal | 50 | terminal | none | none | stop | Functional validation or selected-route readiness fails | Return the applicable validation or execution-blocker message. |

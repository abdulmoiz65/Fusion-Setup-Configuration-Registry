# Manage HCM Extract Definitions Error Handling

Error handling keeps validation, preview, approval, and live Data Loader handoff from replaying uncertain or stale work.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Custom parameter base name, ESS name, or XML tag is missing | Apply task naming rules and validate the result before requesting technical input; report only unresolved business values |
| Parameter names are invalid, exceed live length limits, or collide within the requested parent definition | Stop before preview; identify affected parameters and fields and request a corrected name or valid explicit override |
| Parameter data type is unresolved or ambiguous | Report supplied value and returned candidates; ask for a precise data type before preview |
| A required conditional parameter value or coded override contract is unresolved | Stop before preview and identify the exact conditional requirement or missing declared lookup contract |
| Required information is missing | Ask only for the missing business value and stop before preview |
| Data Loader metadata cannot be resolved | Stop before source generation, validation, packaging, upload, or initiation |
| Extract Delivery Options template lacks usable `METADATA` sections | Stop before preview/upload and report the BO/template contract issue; do not proceed from synthesized component metadata alone |
| Extract Type or Consumer lookup has no exact match and no single unambiguous returned partial match, or has many candidate matches | Report the unresolved or ambiguous value, show candidate values when useful, and ask for a precise value |
| Consumer is generated into `AttributeNineteen` without `resolve_extract_consumer_lov` evidence | Stop before preview and resolve Consumer through the selected extract type's consumer LOV |
| User entity resolution attempts any endpoint other than `extractBlockUserEntitiesLOV` | Stop before preview and resolve through `resolve_extract_block_user_entity_lov` |
| Block threading database item resolution attempts any endpoint other than `extractThreadingDBIsLOV` | Stop before preview and resolve through `resolve_extract_threading_dbi_lov` |
| Data element DBI resolution does not use `userEntityDatabaseItems` filtered by the parent block user entity ID | Stop before preview and resolve through `resolve_user_entity_database_item` |
| `DbiGroupId` is missing for DBI-backed data element creation | Stop before preview and resolve the data element DBI again through `userEntityDatabaseItems` |
| Data element `DataType` is missing or not `N`, `D`, or `T` | Stop before preview and ask for the data type |
| Data element `ShortCode`, `InformationColumn`, generated flags, or `StartDate` are missing or invalid | Stop before preview and regenerate from task-local defaults |
| Final `extractDataElements` DAT contains empty/non-standard template fields | Regenerate the DAT using only the task-standard field set before preview |
| Source validation fails | Stop and show the validation issue, affected source row or artifact, and safe next action |
| Source validation fails and an alternate endpoint or existing-row inference is being considered | Stop before preview; validation is a conformance gate for the task-defined source contract |
| Fusion load fails with an LOV binding error for an optional root attribute | Remove the optional attribute unless its LOV contract and generated value are resolved; regenerate, validate, and preview a fresh artifact before approval |
| Extract block/data group parent definition cannot be resolved | Stop before preview and ask for the parent extract definition identity |
| Fusion load reports a missing parent extract definition identifier for `extractBlocks` | Recheck live `Extract Data Groups` metadata, regenerate the block source using the metadata-supported parent reference attribute, and verify whether the parent extract already exists or is being created in the same artifact |
| Extract Data Groups load or validation reports missing template fields for a scratch block/data group | Reclassify those fields against the live runtime result. If the operation is template/copy-based, require template source context. If the operation is scratch creation, add only proven task-local generation/defaulting behavior; otherwise stop before upload with the exact runtime error |
| Extract record parent definition or block cannot be resolved | Stop before preview and ask for the parent extract definition and block identity |
| Extract record type or process code has no exact match and no single unambiguous returned partial match, or has many candidate matches | Report the unresolved or ambiguous value, show candidate values when useful, and ask for a precise value |
| A requested threading or DBI-bound feature has multiple database item candidates after exact and normalized candidate matching inside `extractThreadingDBIsLOV` | Stop before preview and ask for the precise DBI/database-item selection rather than choosing automatically |
| MultiThreadActType resolves to `O` but Multi DBI is missing or unresolved | Stop before preview and ask for Multi DBI Name or MultiDbiId; resolve it through `extractThreadingDBIsLOV` before generating `MultiDbiId` |
| Upload readiness fails before approval | Stop before requesting approval; fix the ZIP path/name, fingerprint mismatch, uploader envelope shape, or JSON encoding first |
| Upload readiness finds separate ZIPs for DAT files in one live extract creation request | Regenerate one combined ZIP, revalidate the DAT set, and request approval for the combined ZIP fingerprint |
| First-level Data Loader load did not complete successfully | Stop before second-level DAT generation |
| Created extract definition cannot be resolved by `DefinitionName` | Stop before second-level DAT generation and report the unresolved definition name |
| Created extract definition resolves to multiple rows | Stop before second-level DAT generation and ask for disambiguation |
| `generateAllFormulas.dat` is prepared in the first-level ZIP | Remove it from the first-level ZIP and regenerate the preview before approval |
| `compileAllFormulas.dat` is prepared in the first-level ZIP | Remove it from the first-level ZIP and regenerate the preview before approval |
| Second-level ZIP is prepared without current preview and approval | Stop before upload and request approval for the second-level ZIP fingerprint |
| DAT-only path attempts to require XLSX/sample workbook output | Treat XLSX output as optional review support and continue with direct DAT validation when supported |
| DAT-only request reaches ZIP, approval, upload, or initiation preparation | Stop after the validated DAT path and validation result unless the user later asks to proceed toward live creation |
| Live creation request stops at DAT-only validation | Prepare and verify the upload ZIP/readiness preview before asking for approval, unless the user explicitly limited the request to a DAT artifact |
| A one-off source-generation runner is needed | Stop and ask for explicit approval before creating workaround code outside supported Data Loader paths |
| Preview is stale | Revalidate and regenerate the preview before seeking approval |
| Approval is missing or stale | Stop before any Fusion side effect and request approval for the exact current preview and fingerprint |
| Live POST may have reached Fusion but response capture failed | Do not retry automatically; perform read-only recovery/status lookup where available; disclose duplicate-create or duplicate-action risk before any approved retry |
| Fusion job fails after initiation | Retrieve and persist available ProcessLog or status payload through the active workflow and preserve partial successes with errors |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | Missing task identity, operation, required field, source artifact, or parser-compatible encoding | Ask for the missing or corrected input |
| catalog mismatch | Task, business object, discriminator, or metadata contract does not match the selected task | Reroute or re-author before preview |
| auth/authz | Active workflow reaches a read-only or live step but credentials or privileges are not valid | Refresh cached token once for 401 or 403 where permitted, otherwise stop |
| transport/environment | Network, pod, timeout, or environment issue prevents the declared lookup or operation | Report environment, operation, last status, and retry or next-check path |
| Fusion API | Fusion lookup, upload, initiation, or status call returns an application error | Report the redacted error and stop before retry |
| approval blocker | Current approval does not bind to task identity, operation, business object, preview, validation result, and fingerprint | Show the current preview and request explicit approval |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preview gate | Task identity; operation route; selected business object; generated source shape; resolved values; validation result; artifact fingerprint |
| Approval gate | Exact target environment; operation; selected business object; immutable source artifact or payload reference; validation result; artifact fingerprint |
| Upload-readiness gate | Upload ZIP path/name; source artifact path; artifact fingerprint; envelope shape check; JSON encoding check |
| Polling timeout | Environment; operation; TaskCode or job; ProcessId or requestId when available; last status; elapsed wait; next-check or retry path |
| Failed Fusion job | Redacted ProcessLog or status payload reference when available; partial successes; errors array; nonzero status |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Task identity does not match Manage HCM Extract Definitions | Do not validate, preview, package, upload, or initiate |
| Business object is not one of the task-supported Extracts Data Loader objects for its declared phase | Do not proceed with the Data Loader route |
| Source validation is missing or stale | Do not request approval or perform live handoff |
| Approval is missing or stale | Do not upload or initiate |
| Scratch creation has unresolved mandatory or conditional fields | Do not generate the preview as ready |
| Generated source includes unauthorized child rows | Do not include child rows in the source artifact |
| Reusable resources contain credentials or environment-specific identifiers | Do not persist or publish the resource until sanitized |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HCM_EXT_DEF.GATE_PREVIEW | step | 100 | execution_gate | ready->HCM_EXT_DEF.GATE_APPROVAL;blocked->HCM_EXT_DEF.RETURN_ISSUES | HCM_EXT_DEF.ENFORCE_DESIGN | stop | Before approval or Data Loader handoff |
| HCM_EXT_DEF.GATE_APPROVAL | step | 110 | execution_gate | approved->HCM_EXT_DEF.READY_FOR_DATALOADER_HANDOFF;missing->HCM_EXT_DEF.RETURN_ISSUES | HCM_EXT_DEF.GATE_PREVIEW | stop | Before any Fusion upload or initiation |
| HCM_EXT_DEF.READY_FOR_DATALOADER_HANDOFF | terminal | 120 | terminal | none | HCM_EXT_DEF.GATE_APPROVAL | stop | Validation, preview, and approval gates passed |
| HCM_EXT_DEF.RETURN_ISSUES | terminal | 130 | terminal | none | none | stop | Any validation, lookup, dependency, design, preview, approval, or live-readiness issue occurs |

# Sales Note Type Design Enforcement

Apply these documented design gates before presenting a guided change, migration preview, or runtime-availability conclusion.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/sales/oacts/define-notes.html | Categorization goals, object mappings, default-note fallback, and impact of default changes |
| https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-can-i-add-new-note-types.html | Required note-type definition and mapping follow-up |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/overview-of-lookups.html | Code shape, configuration levels, enablement, translations, deletion limits, and session refresh |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/op-notetypes-get.html | Object-context runtime verification fields |
| https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/automate-export-and-import-of-csv-file-packages.html | Task package and import safeguards |

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm operation and identity | Validate the exact task operation, stable code, display values, and effective state. |
| 2 | Confirm editability and impact | Check configuration-level restrictions and whether the row is predefined data. |
| 3 | Confirm business-object visibility | Identify the downstream mapping or accepted Default Note Types behavior. |
| 4 | Confirm migration controls | For CSV work, use the current task package, authorized executor, immutable preview, and exact approval. |
| 5 | Confirm runtime evidence | Treat the Note Types REST result as object-context mapping evidence, not as the base lookup inventory. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Creating or renaming a note type | Error |  | The code contains spaces, the meaning is blank, or the requested meaning does not support a distinct search, filter, or reporting category. | Use a stable underscore-separated code and a concise business-facing meaning and description. | Yes |
| A new note type must appear for one or more business objects | Error |  | No downstream mapping plan identifies the target objects or Default Note Types behavior. | Complete the definition here, then use Manage Sales Note Type Mapping for each target object or approved default-note scope. | Yes |
| Changing a default note type | Error |  | The requester has not accepted that objects without explicit mappings inherit the default-note change. | Review all unmapped object types before approving the change. | Yes |
| Updating dates, enablement, or deleting a row | Error |  | The selected lookup configuration level or predefined-data status does not permit the operation. | Preserve seeded rows and apply only operations allowed by the task page. | Yes when the task page permits it |
| Deactivating a custom note type used by historical notes | Error |  | The requester proposes deletion without reviewing historical and mapping impact. | Prefer an enabled-state or end-date change when history must remain interpretable; treat this as an FSCR safety recommendation, not an Oracle deletion requirement. | Yes |
| Translating a note type | Error |  | The target language is not enabled or TranslatedMeaning is blank. | Use the lookup translation control for an administrator-permitted language and validate the translated UI in a refreshed session. | Yes |
| Importing setup data | Error |  | The package is not current and task-specific, exceeds the documented package constraints, or lacks a matching preview and approval. | Recreate the package from the current task template or export and obtain a new immutable preview. | Yes |
| Runtime lookup returns no exact match | Warning | find_mapped_note_type_for_object | The requester interprets no match as proof that the ZMM_NOTE_TYPE row does not exist. | Review the mapping task and Default Note Types fallback; verify the base lookup in the setup task before changing it. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_mapped_note_type_for_object | ValidateRuntimeAvailability is requested | RuntimeMappedLookupCode, RuntimeMeaning, RuntimeSourceObjectCode | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_NOTE.DESIGN | decision | 5 | design_enforcement | allowed->SALES_NOTE.EXECUTION_GATE;policy_block->SALES_NOTE.FAILED | SALES_NOTE.DEFAULTS | stop | Always |

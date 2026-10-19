# Sales Note Type Mapping Design Enforcement

Apply these documented design gates before presenting a guided mapping change, migration preview, or runtime-availability conclusion.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/sales/oacts/define-notes.html | Tailored object lists, fallback behavior, and default-note impact |
| https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-can-i-add-new-note-types.html | Mapping sequence, mapped lookup value, optional end date, and Default field |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/op-notetypes-get.html | Effective runtime verification boundary |
| https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/automate-export-and-import-of-csv-file-packages.html | Task package and import safeguards |

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm operation and identity | Validate the exact business object, mapped lookup code, Default decision, and optional end date. |
| 2 | Confirm parent setup | Verify that the mapped code already exists and is enabled and effective in ZMM_NOTE_TYPE. |
| 3 | Confirm tailored-list impact | For a first object-specific mapping, obtain an explicit Preserve or Restrict choice, then review the complete resulting list; do not treat inherited values as implicitly approved for copying. |
| 4 | Confirm fallback impact | Before changing Default Note Types, review every business object with no specific mapping. |
| 5 | Confirm migration controls | For CSV work, use the current task package, authorized executor, immutable preview, and exact approval. |
| 6 | Confirm evidence boundary | Treat the Note Types REST result as effective availability, not proof of an explicit setup mapping row. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Creating or updating a mapping | Error | find_active_sales_note_type_code | The mapped lookup code is absent, disabled, or outside its effective dates. | Define or correct the code through Manage Sales Note Type before mapping it. | Yes |
| Creating an object-specific mapping | Error |  | The complete tailored list for the selected business object has not been reviewed. | Include every note type that should remain available after the object-specific mapping is applied. | Yes |
| Creating a first object-specific mapping | Error | find_effective_note_type_for_object | The object has no persisted mapping row and the requester has not explicitly chosen Preserve or Restrict. | Ask whether to retain the current effective list or limit the object to the requested values; do not auto-copy Default Note Types. | Yes |
| Selecting Default Note Types or changing fallback design | Error |  | The affected business objects without specific mappings and their accepted impact are unknown. | Review all fallback consumers and record explicit approval before changing defaults. | Yes |
| Creating or changing a mapping | Error |  | BusinessObjectName, MappedLookupCode, or required DefaultFlag is inferred rather than explicitly selected. | Use the exact setup-page object and code and an explicit Y or N default decision. | Yes |
| End-dating a mapping | Error |  | The requester has not reviewed which values will remain available or whether the object will fall back to Default Note Types. | Review the post-end-date effective list before approval. | Yes |
| Reviewing an exact setup row | Error | find_effective_note_type_for_object | Runtime effective availability is being treated as proof of an explicit mapping or duplicate row. | Inspect the Manage Sales Note Type Mapping page or a current task export for exact setup-row evidence. | Yes |
| Importing setup data | Error |  | The package is not current and task-specific, or lacks a matching preview, target environment, and approval. | Recreate the package from the current task template or export and obtain a new immutable preview. | Yes |
| Runtime lookup returns no exact match | Warning | find_effective_note_type_for_object | The requester interprets no match as proof that the ZMM_NOTE_TYPE code is absent. | Verify the parent lookup separately and review object mapping and Default Note Types behavior. | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_active_sales_note_type_code | A mapped lookup code is supplied | VerifiedLookupCode, VerifiedMeaning, VerifiedEnabledFlag, VerifiedStartDate, VerifiedEndDate | ora_reference_lookups.md |
| find_effective_note_type_for_object | ValidateRuntimeAvailability is requested | RuntimeMappedLookupCode, RuntimeMeaning, RuntimeSourceObjectCode | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NOTE_MAPPING.DESIGN | decision | 6 | design_enforcement | allowed->NOTE_MAPPING.EXECUTION_GATE;policy_block->NOTE_MAPPING.BLOCKED | NOTE_MAPPING.DEFAULTS | stop | Always |

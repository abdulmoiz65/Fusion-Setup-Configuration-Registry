# Sales Note Type Mapping Error Handling and Execution Gate

Stop safely on ambiguous scope, missing lookup setup, unreviewed default impact, stale CSV packages, unsupported direct writes, uncertain import results, or an unselected execution route. This resource prepares an explicitly requested manual UI procedure or an authorized setup-data handoff; it does not itself mutate Fusion.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-can-i-add-new-note-types.html | Guided mapping sequence and supported page fields |
| https://docs.oracle.com/en/cloud/saas/sales/oacts/define-notes.html | Object-specific and Default Note Types behavior |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/api-list-values-note-types.html | Read-only Sales Note Types REST boundary |
| https://docs.oracle.com/en/cloud/saas/sales/oaslm/Sales_Administrator_job_roles.html | Set Up Sales Note access |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-exports.html | Task CSV export boundary |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-template-exports.html | Task CSV template export boundary |
| https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-imports.html | Task CSV import and result boundary |
| https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/automate-export-and-import-of-csv-file-packages.html | Role, task-code, ZIP, and package-editing requirements |

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required operation, business object, mapped code, Default decision, end date, or package input is missing | Stop and request only the missing business value. |
| The mapped lookup code is absent, disabled, or ineffective | Stop and route code creation or correction to Manage Sales Note Type. |
| The selected business object is approximate or ambiguous | Stop and require the exact setup-page object or runtime SourceObjectCode. |
| The supplied UI object or SourceObjectCode is absent from the supported-object catalog | Stop. Do not synthesize a code from the label or Object Metadata; obtain the exact current UI selection or positive runtime evidence, then update the catalog through the documented review process. |
| The selected exact UI business object has no mapping row in the current task export | Treat this as no persisted mapping evidence, not as an invalid object. Reuse the matching `ORA_OBJECT_LOOKUP.csv` parent row when present. When it is absent but the exact selector is catalogued in `ora_supported_object_codes.md`, add the controlled parent row defined by that catalog before adding the child mapping; Fusion skips a child `ZMM_OBJECT_LOOKUP_MAPPING.csv` row whose parent object row is missing. |
| The selected object has no persisted mapping row but inherits Default Note Types | Stop and ask whether to Preserve the current effective list or Restrict the object to the requested values. Do not automatically add inherited values to the object-specific CSV rows. |
| A default mapping change lacks an impact review | Stop because the change can affect every object with no specific mapping. |
| A new mapping causes expected note types to disappear | Review the complete object-specific mapping list; explicit mapping tailors the available values for that object. |
| An ended mapping changes the object's effective list | Review remaining explicit mappings and Default Note Types fallback before concluding that the change failed. |
| The read-only Note Types resource returns no exact match | Report only that effective availability was not verified; do not claim the parent code or explicit setup row is absent. |
| The read-only Note Types resource returns a match | Report effective availability and disclose that the result does not distinguish an explicit mapping from Default Note Types fallback. |
| A direct create, patch, or delete is requested against the CRM Note Types resource | Refuse the mutation because the documented resource is read-only. Use the guided setup task or approved setup-task CSV workflow. |
| A supported mutation does not select a route | Default to the current task-specific package and core Data Loader preview-and-approval workflow; do not initialize browser control. |
| The requester explicitly selects manual UI | Prepare the documented guided procedure only; do not substitute a Data Loader import. |
| The CSV template or export is stale, for another task, or has altered file names or headers | Stop and obtain a current package for ZBS_MANAGE_SALES_NOTE_TYPE_MAPPING. |
| Import approval does not match the exact preview and target environment | Stop and revalidate the changed package before obtaining new approval. |
| Import completes with errors or uncertain status | Retrieve the documented result or process log once, disclose it safely, and stop before retry. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| BLOCKED | Required access, code, scope, impact review, package, privilege, preview, or approval is missing. | Resolve the missing gate; do not perform or request a mutation. |
| FAILED | Validation, lookup, design, or process evidence is invalid or ambiguous. | Disclose the sanitized failure and wait for corrected input or explicit retry instruction. |
| DATA_LOADER_DEFAULT | A supported mutation did not explicitly select manual UI. | Use the current task package and core Data Loader preview-and-approval workflow. |
| UI_GUIDANCE_READY | The requester explicitly selected manual UI and the reviewed plan is ready for an authorized setup user. | Follow the documented Setup and Maintenance procedure. |
| IMPORT_HANDOFF_READY | A current task package has passed validation and has exact approval. | Hand off to core.data-loader and the task-level setup import workflow. |
| REVIEW_COMPLETE | Review, export planning, or runtime availability validation completed without a Fusion mutation. | Return the evidence and any fallback or mapping follow-up. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Guided UI plan | Task code, operation, target environment, business object, mapped lookup code and meaning, DefaultFlag, EndDate, tailored-list impact, and fallback impact. |
| Runtime validation | SourceObjectCode, mapped lookup code, returned meaning, match count, and the explicit-mapping-versus-fallback limitation. |
| CSV import handoff | Exact package identity, task code, file and header validation, target environment, preview fingerprint, approval state, and authorized executor. |
| Failure | Safe task or endpoint identity, response or process status, sanitized result or log, and one safe next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Missing or ambiguous business object | Do not infer the mapping scope from the lookup code or request wording. |
| Missing parent note type | Do not create an undocumented placeholder mapping; route to Manage Sales Note Type. |
| Missing Preserve or Restrict decision for a first object-specific mapping | Do not prepare a UI plan, CSV preview, or import artifact. |
| Unreviewed Default Note Types impact | Do not approve or execute the default change. |
| Direct CRM Note Types write requested | Do not invent a POST, PATCH, or DELETE payload for the read-only resource. |
| Missing current task package or schema | Do not hand-build CSV files or submit an import. |
| Missing or stale approval | Do not execute or request an import. |
| Failed or uncertain mutation | Do not retry automatically or claim success. |

## Documented Guided Setup — Explicit Manual UI Only

1. In Setup and Maintenance, open the Sales offering, Sales Foundation functional area, and `Manage Sales Note Type Mapping` task.
2. Select the exact business object, such as Sales Account, or explicitly select Default Note Types when changing fallback values.
3. Add or select the mapping row and choose the existing code in Mapped Lookup Value.
4. Enter an end date only when the approved design requires one.
5. Set Default to the explicitly approved Y or N value; do not infer it.
6. If this is the first object-specific mapping, ask whether to Preserve the current effective list or Restrict the object to the requested values; review the resulting complete tailored list and Default Note Types impact, then save and close through an authorized setup user.
7. Validate effective availability for the exact source object through the read-only Note Types resource, while preserving the fallback limitation.

## Documented CSV Automation Route

| Sequence | Required Gate | What Must Happen |
|---|---|---|
| 1 | Task package | Export the current template or setup data for ZBS_MANAGE_SALES_NOTE_TYPE_MAPPING. |
| 2 | Package preparation | Preserve the template-derived file names and columns, treat all columns as text when editing, and keep the CSV within Oracle's documented size limit. |
| 3 | Validation | Validate each object, lookup code, Default decision, end date, and fallback-impact rule. For a first object-specific mapping, require the explicit Preserve or Restrict decision and do not invent or auto-copy omitted rows. |
| 4 | Immutable preview | Build a preview for the exact normalized ZIP and target environment. |
| 5 | Approval | Obtain approval bound to that exact preview and authorized executor. |
| 6 | Import handoff | Route the approved package to core.data-loader using task code ZBS_MANAGE_SALES_NOTE_TYPE_MAPPING. |
| 7 | Verification | Retrieve the import result or process log once, review the mapping in the setup task, and validate effective availability for the exact source object. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NOTE_MAPPING.EXECUTION_GATE | decision | 7 | execution_gate | ui_guidance_ready->NOTE_MAPPING.UI_READY;import_handoff_ready->NOTE_MAPPING.IMPORT_READY;review_or_validation_complete->NOTE_MAPPING.REVIEW_COMPLETE;default_data_loader->NOTE_MAPPING.IMPORT_READY;missing_gate->NOTE_MAPPING.BLOCKED;unsupported_direct_write->NOTE_MAPPING.BLOCKED | NOTE_MAPPING.DESIGN | stop | After validation: default supported mutations to Data Loader/FSM import; use manual UI only when explicitly requested. |
| NOTE_MAPPING.UI_READY | terminal | 8 | terminal | none | NOTE_MAPPING.EXECUTION_GATE | stop | The requester explicitly selected manual UI and the reviewed plan is ready for an authorized setup user |
| NOTE_MAPPING.IMPORT_READY | terminal | 9 | terminal | none | NOTE_MAPPING.EXECUTION_GATE | stop | A validated package is ready for the default core.data-loader handoff, or Data Loader/FSM import was explicitly requested |
| NOTE_MAPPING.REVIEW_COMPLETE | terminal | 10 | terminal | none | NOTE_MAPPING.EXECUTION_GATE | stop | Review, export planning, or runtime availability validation completed without mutation |
| NOTE_MAPPING.BLOCKED | terminal | 11 | terminal | none | none | stop | A required access, code, scope, impact, package, preview, approval, or supported-write gate is missing |
| NOTE_MAPPING.FAILED | terminal | 12 | terminal | none | none | stop | Input, dependency, lookup, design, or process evidence is invalid or ambiguous |

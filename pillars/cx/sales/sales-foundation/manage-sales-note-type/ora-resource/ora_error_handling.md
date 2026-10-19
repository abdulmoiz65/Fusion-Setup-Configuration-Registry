# Sales Note Type Error Handling and Execution Gate

Stop safely on ambiguous identity, protected lookup data, missing mapping intent, stale CSV packages, unsupported direct writes, uncertain import results, or an unselected execution route. This resource prepares an explicitly requested manual UI procedure or an authorized setup-data handoff; it does not itself mutate Fusion.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-can-i-add-new-note-types.html | Guided note-type creation and mapping sequence |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/overview-of-lookups.html | Protected lookup operations, enablement, translations, deletion, and session refresh |
| https://docs.oracle.com/en/cloud/saas/sales/faaps/api-list-values-note-types.html | Read-only Note Types REST boundary |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-template-exports.html | Task CSV template export boundary |
| https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-imports.html | Task CSV import and result boundary |
| https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/automate-export-and-import-of-csv-file-packages.html | Role, task-code, ZIP, and package-editing requirements |

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required operation, identity, definition, translation, object context, or package input is missing | Stop and request only the missing business value. |
| The selected row is protected by its configuration level or predefined-data status | Stop the requested update or deletion and disclose the restriction. |
| A new type is saved but not available for the intended object | Review Manage Sales Note Type Mapping and Default Note Types behavior, then refresh the user session before concluding that setup failed. |
| The read-only Note Types resource returns no match | Report only that object-context availability was not verified; do not claim the base lookup is absent. |
| The read-only Note Types resource fails or returns ambiguous matches | Stop and disclose the sanitized request context and status; do not retry automatically. |
| A direct create, patch, or delete is requested against the CRM Note Types resource | Refuse the mutation because the documented resource is read-only. Use the guided setup task or approved setup-task CSV workflow. |
| A supported mutation does not select a route | Default to the current task-specific package and the core Data Loader preview-and-approval workflow; do not initialize browser control. |
| The requester explicitly selects manual UI | Prepare the documented guided procedure only; do not substitute a Data Loader import. |
| The CSV template or export is stale, for another task, or has altered file names or headers | Stop and obtain a current package for ZBS_MANAGE_SALES_NOTE_TYPE. |
| Import approval does not match the exact preview | Stop and revalidate the changed package before obtaining new approval. |
| Import completes with errors or uncertain status | Retrieve the documented result or process log once, disclose it safely, and stop before retry. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| BLOCKED | Required access, editability, mapping intent, template, privilege, preview, or approval is missing. | Resolve the missing gate; do not perform or request a mutation. |
| FAILED | Validation, lookup, design, or process evidence is invalid or ambiguous. | Disclose the sanitized failure and wait for corrected input or explicit retry instruction. |
| DATA_LOADER_DEFAULT | A supported mutation did not explicitly select manual UI. | Use the current task package and core Data Loader preview-and-approval workflow. |
| UI_GUIDANCE_READY | The requester explicitly selected manual guided UI and the reviewed plan is ready for an authorized setup user. | Follow the documented Setup and Maintenance procedure. |
| IMPORT_HANDOFF_READY | A current task package has passed validation and has exact approval. | Hand off to core.data-loader and the task-level setup import workflow. |
| REVIEW_COMPLETE | Review, export planning, or runtime availability validation completed without a Fusion mutation. | Return the evidence and any mapping or session-refresh follow-up. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Guided UI plan | Task code, operation, note-type code, meaning, description, enablement, effective dates, translations, and downstream mapping intent. |
| Runtime validation | Source object code, mapped lookup code, returned meaning, match count, and the limitation that no match does not prove base-row absence. |
| CSV import handoff | Exact package identity, task code, file and header validation, preview fingerprint, approval state, and authorized executor. |
| Failure | Safe task or endpoint identity, response or process status, sanitized result or log, and one safe next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Unknown or protected lookup operation | Do not invent editability or bypass the task page restriction. |
| Object mapping requested in this task | Do not write mapping fields as ZMM_NOTE_TYPE fields; route to Manage Sales Note Type Mapping. |
| Direct CRM Note Types write requested | Do not invent a POST, PATCH, or DELETE payload for the read-only resource. |
| Missing current task package or schema | Do not hand-build CSV files or submit an import. |
| Missing or stale approval | Do not execute or request an import. |
| Failed or uncertain mutation | Do not retry automatically or claim success. |

## Documented Guided Setup — Explicit Manual UI Only

1. In Setup and Maintenance, open the Sales offering, Sales Foundation functional area, and `Manage Sales Note Type` task.
2. For creation, add a row to the `ZMM_NOTE_TYPE` lookup codes table, enter the stable lookup code, select Enable for an immediately usable type, and enter the meaning and description.
3. For an allowed update or deactivation, change only the permitted meaning, enablement, start date, or end date fields after reviewing configuration-level and predefined-data restrictions.
4. For translation, use the lookup-row translation control, select an administrator-permitted language, and enter the translated meaning and optional description.
5. Save and close. If the type must be available for a business object, continue in `Manage Sales Note Type Mapping`, select the object and mapped lookup value, add an end date if required, and set the intended default.
6. Have affected users sign out and sign back in before validating the changed list of values.

## Documented CSV Automation Route

| Sequence | Required Gate | What Must Happen |
|---|---|---|
| 1 | Task package | Export the current template or setup data for ZBS_MANAGE_SALES_NOTE_TYPE. |
| 2 | Package preparation | Preserve the template-derived file names and columns, treat all columns as text when editing, and keep the ZIP within Oracle's documented size limit. |
| 3 | Validation | Validate each requested row, configuration restriction, and effective-date rule without inventing missing schema details. |
| 4 | Immutable preview | Build a preview for the exact normalized ZIP and target environment. |
| 5 | Approval | Obtain approval bound to that exact preview and authorized executor. |
| 6 | Import handoff | Route the approved package to core.data-loader using task code ZBS_MANAGE_SALES_NOTE_TYPE. |
| 7 | Verification | Retrieve the import result or process log once, then verify the lookup in the setup task and object-context availability after mapping and session refresh. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_NOTE.EXECUTION_GATE | decision | 6 | execution_gate | ui_guidance_ready->SALES_NOTE.UI_READY;import_handoff_ready->SALES_NOTE.IMPORT_READY;review_or_validation_complete->SALES_NOTE.REVIEW_COMPLETE;default_data_loader->SALES_NOTE.IMPORT_READY;missing_gate->SALES_NOTE.BLOCKED;unsupported_direct_write->SALES_NOTE.BLOCKED | SALES_NOTE.DESIGN | stop | After validation: default supported mutations to Data Loader/FSM import; use manual UI only when explicitly requested. |
| SALES_NOTE.UI_READY | terminal | 7 | terminal | none | SALES_NOTE.EXECUTION_GATE | stop | The requester explicitly selected manual UI and the reviewed plan is ready for an authorized setup user |
| SALES_NOTE.IMPORT_READY | terminal | 8 | terminal | none | SALES_NOTE.EXECUTION_GATE | stop | A validated package is ready for the default core.data-loader handoff, or Data Loader/FSM import was explicitly requested |
| SALES_NOTE.REVIEW_COMPLETE | terminal | 9 | terminal | none | SALES_NOTE.EXECUTION_GATE | stop | Review, export planning, or runtime availability validation completed without mutation |
| SALES_NOTE.BLOCKED | terminal | 10 | terminal | none | none | stop | A required access, mapping, package, preview, approval, or supported-write gate is missing |
| SALES_NOTE.FAILED | terminal | 11 | terminal | none | none | stop | Input, dependency, lookup, design, or process evidence is invalid or ambiguous |

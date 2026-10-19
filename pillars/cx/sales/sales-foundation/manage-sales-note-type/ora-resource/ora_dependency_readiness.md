# Sales Note Type Dependency Readiness

Resolve setup access, editability, mapping intent, runtime context, and migration prerequisites before the requested note-type workflow continues.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-can-i-add-new-note-types.html | Manage Sales Note Type and Manage Sales Note Type Mapping workflow |
| https://docs.oracle.com/en/cloud/saas/sales/oacts/define-notes.html | Required business-object mapping and default-note fallback behavior |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/overview-of-lookups.html | Configuration levels, predefined-data restrictions, enablement, sign-in refresh, and translations |
| https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/automate-export-and-import-of-csv-file-packages.html | Export/import roles, task code, ZIP handling, and package limits |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-template-exports.html | Current task CSV template export contract |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Task access and editability | Confirm the setup user can open Manage Sales Note Type and that the ZMM_NOTE_TYPE row permits the requested change. |
| 2 | Note-type design | Confirm the stable code, user-facing meaning, description, enablement, effective dates, and translations in scope. |
| 3 | Mapping intent | Confirm whether the type must be mapped to one or more business objects or included among default note types in the separate mapping task. |
| 4 | Runtime validation context | When runtime availability is checked, provide the exact source object code and treat the Note Types REST result as mapping evidence only. |
| 5 | CSV package and authority | For migration or bulk maintenance, obtain the current package for this exact task and confirm the executor has the required setup-data role and task privileges. |
| 6 | Immutable preview | Validate the exact UI plan or CSV package and obtain approval before any authorized mutation workflow. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| setup_access | Manage Sales Note Type access | Yes | Create, Update, Deactivate, Translate, Export, or Import | Satisfied when an authorized setup user can open the task | Executor authorization |  | Oracle directs setup users to this task for ZMM_NOTE_TYPE maintenance. | Confirm task access before preparing a change. | Authorized setup user |
| lookup_editability | Lookup configuration level and predefined-data status | Conditional | Update or Deactivate | Satisfied when the requested operation is permitted for the selected row | Manage Sales Note Type page |  | Configuration level controls which insert, enablement, date, and delete operations are allowed. | Review the selected row before promising a change; do not alter protected seeded data. | Configuration level, predefined-data status |
| object_mapping_intent | Business-object or default-note mapping plan | Conditional | A new type must appear for a business object or as a default note type | Satisfied when the downstream mapping task and affected objects are identified | Implementation design |  | A defined lookup value does not by itself establish object-specific availability. | Identify each target business object and route the follow-up to Manage Sales Note Type Mapping. | SourceObjectCode, DefaultFlag, MappingEndDate |
| runtime_object_context | Source object for runtime availability | Conditional | ValidateRuntimeAvailability | Satisfied when SourceObjectCode is supplied | Request |  | The Note Types resource resolves values in business-object context. | Supply the exact source object code. | SourceObjectCode |
| task_csv_package | Current task-specific CSV package | Conditional | Export or Import | Satisfied when the package is for ZBS_MANAGE_SALES_NOTE_TYPE and its template-derived schema is preserved | Setup task CSV export or template export |  | Oracle setup-data import expects a task-specific ZIP package. | Do not hand-build the file names or columns. | Package path, file names, headers, task code |
| import_authority | Setup-data import role and task privilege | Conditional | Import | Satisfied when the executor has ORA_ASM_FUNCTIONAL_SETUPS_USER_ABSTRACT and task-specific privileges | Executor authorization |  | Oracle requires both the export/import abstract role and task-specific privileges. | Confirm the submitting identity before import handoff. | Authorized executor |
| session_refresh | User session refresh | Conditional | A saved lookup change is not visible | Satisfied after affected users sign out and sign back in | Oracle lookup behavior |  | Oracle documents that lookup changes may require a new user session to take effect. | Refresh the session before classifying the saved setup as ineffective. | Refreshed session evidence |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required access, design, mapping intent, context, package, and approval facts are present. | Proceed to the applicable read-only check or guidance gate. |
| Not Applicable | A conditional dependency does not apply to the selected operation. | Continue. |
| Blocked | Required access, editability, context, package, privilege, preview, or mapping intent is missing. | Stop before change or import handoff. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_NOTE.DEPENDENCIES | step | 2 | resolve_dependency | satisfied->SALES_NOTE.RUNTIME_LOOKUP;blocked->SALES_NOTE.FAILED | SALES_NOTE.VALIDATE | stop | Always |

# Sales Note Type Mapping Dependency Readiness

Resolve setup access, the parent note type, exact business-object scope, default-impact review, and migration prerequisites before mapping guidance or import handoff continues.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-can-i-add-new-note-types.html | Manage Sales Note Type prerequisite and mapping sequence |
| https://docs.oracle.com/en/cloud/saas/sales/oacts/define-notes.html | Business-object mapping, fallback, and default-note impact |
| https://docs.oracle.com/en/cloud/saas/sales/oaslm/Sales_Administrator_job_roles.html | Sales Administrator access through Set Up Sales Note |
| https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/automate-export-and-import-of-csv-file-packages.html | CSV roles, task code, ZIP handling, and task-specific access |
| https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/api-setup-task-csv-template-exports.html | Current task CSV template export contract |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Task access | Confirm the setup user can open Manage Sales Note Type Mapping and has Set Up Sales Note access. |
| 2 | Parent note type | Confirm the exact mapped lookup code already exists and is enabled and effective in ZMM_NOTE_TYPE. |
| 3 | Business-object scope | Select the exact business object or Default Note Types scope; do not infer it from a note-type name. |
| 4 | Mapping and fallback impact | For a first object-specific mapping, obtain the requester's explicit Preserve or Restrict decision before reviewing the resulting tailored list; review all unmapped objects before changing Default Note Types. |
| 5 | CSV package and authority | For migration or bulk maintenance, obtain the current package for this task and confirm the executor has the required setup-data role and task privileges. |
| 6 | Immutable preview | Validate the exact guided plan or CSV package and obtain approval before any authorized mutation workflow. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| setup_access | Manage Sales Note Type Mapping access | Yes | Create, Update, EndDate, Export, or Import | Satisfied when an authorized setup user can open the task | Executor authorization |  | Oracle identifies Set Up Sales Note as the Sales Administrator access that controls sales-note setup. | Confirm the executor can open the mapping task before preparing a change. | Authorized setup user, target environment |
| mapped_note_type | Existing enabled ZMM_NOTE_TYPE code | Yes | Create, Update, EndDate, or ValidateRuntimeAvailability | Satisfied when exactly one enabled and effective code matches | Standard Lookups REST or Manage Sales Note Type | find_active_sales_note_type_code | Oracle requires the lookup code to be created before it is selected as a mapped value. | Create or correct the code through Manage Sales Note Type before mapping it. | LookupCode, Meaning, EnabledFlag, StartDateActive, EndDateActive |
| business_object_scope | Exact mapping scope | Yes | Review, Create, Update, EndDate, or ValidateRuntimeAvailability | Satisfied when the exact UI business object or runtime SourceObjectCode is supplied | Request and Manage Sales Note Type Mapping page |  | Mappings tailor the values by business object, while Default Note Types supplies fallback values. | Select the exact business object or explicitly select Default Note Types. | BusinessObjectName or SourceObjectCode |
| first_mapping_scope | Preserve or restrict inherited values | Conditional | Create when the current task export has no persisted mapping row for the exact object | Satisfied when requester explicitly selects Preserve or Restrict after seeing the current effective values | Requester decision, current task export, and Note Types REST | find_effective_note_type_for_object | The first object-specific mapping replaces fallback values for that object. | Ask whether the existing effective list should be retained. Preserve requires a complete explicit list; Restrict requires explicit confirmation that omitted values will no longer be available. | PreserveEffectiveList, desired complete list, DefaultFlag per row |
| default_impact_review | Default Note Types impact review | Conditional | Default Note Types is changed, or DefaultFlag is changed in a way that affects fallback behavior | Satisfied when every affected unmapped business object has been reviewed | Approved implementation design |  | Oracle states that modifying a default note type affects every business object with no specific mapping. | Review the fallback consumers and record approval before changing the default design. | Affected objects, accepted impact, approver |
| task_csv_package | Current task-specific CSV package | Conditional | Export or Import | Satisfied when the package is for ZBS_MANAGE_SALES_NOTE_TYPE_MAPPING and its template-derived schema is preserved | Setup task CSV export or template export |  | Oracle setup-data import expects a task-specific ZIP package. | Do not hand-build the file names or columns. | Package path, file names, headers, task code |
| import_authority | Setup-data import role and task privilege | Conditional | Import | Satisfied when the executor has ORA_ASM_FUNCTIONAL_SETUPS_USER_ABSTRACT and task-specific privileges | Executor authorization |  | Oracle requires both the export/import abstract role and task-specific access. | Confirm the submitting identity before import handoff. | Authorized executor |
| immutable_preview | Exact preview and approval | Conditional | Create, Update, EndDate, or Import proceeds to an authorized mutation workflow | Satisfied when approval is bound to the exact environment, object, mapped code, default flag, end date, and package when applicable | Approved execution preview |  | A changed object, code, default decision, date, or package changes the business effect. | Recreate the preview and approval after any material change. | Preview fingerprint, approval state |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required access, lookup code, scope, impact review, package, privilege, and approval facts are present. | Proceed to the applicable read-only checks or guidance gate. |
| Not Applicable | A conditional dependency does not apply to the selected operation. | Continue. |
| Blocked | Required access, code, object scope, impact review, package, privilege, preview, or approval is missing. | Stop before change or import handoff. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| NOTE_MAPPING.DEPENDENCIES | step | 2 | resolve_dependency | satisfied->NOTE_MAPPING.BASE_LOOKUP;blocked->NOTE_MAPPING.BLOCKED | NOTE_MAPPING.VALIDATE | stop | Always |

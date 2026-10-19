# Dependency Readiness

The documented task associates a type with one or more activity functions, then optionally maps the type to a subtype. An activity type that is not associated with a function is not visible to users. CSV automation requires a verified task-specific source package: either a template ZIP or a completed data-export ZIP for the exact task. The supplied completed export contains subtype rows only, so its parent activity type must already exist.

Sources: [Associate Activity Type with a Function and Subtype](https://docs.oracle.com/en/cloud/saas/sales/oasal/associate-activity-type-with-a-function-and-subtype.html), [About Activity Type and Subtype](https://docs.oracle.com/en/cloud/saas/sales/oasal/about-activity-type-and-subtype.html), and [Setup Task CSV Template Exports REST Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-template-exports.html).

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Activity type and function association | Select or create the activity type and associate it with the required Appointment, Task, or Call Report functions. |
| 2 | Task CSV source package | For CSV automation, use either a completed template-export ZIP or a verified completed data-export ZIP for this exact task. Extract the CSV, make the allowed subtype-row change, and repackage it as ZIP before preview. |
| 3 | Activity subtype relationship | If a subtype is in scope, select the activity type, add or review the subtype, and select Enabled when adding the subtype. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| activity_type_function_mapping | Existing activity type is associated with the selected activity function | Conditional | review of a type-function association or change_mode is update_type_functions | Verify | Read-only Activity Type Lookups LOV | find_activity_type_by_function | An existing type without a function association is not visible in the UI. | Provide the activity type and function codes, then correct the mapping in the documented task if it is not returned. | activity_type_code: LookupCode; activity_type_name: Meaning; activity_type_enabled: EnabledFlag; activity_type_tag: Tag |
| new_activity_type_definition | New activity type has code, name, enablement, start date, tag, and selected functions | Yes | change_mode is create_type | Verify | Normalized request values |  | A new type needs a complete definition before it can be previewed. | Provide the missing value; do not infer a name, code, start date, or function selection. | activity_type_code; activity_type_name; enabled_flag; start_date; lookup_type_tag; activity_function_codes |
| csv_export_package | Completed task data-export ZIP is available for the selected task | Conditional | change_mode is create_subtype or update_subtype and the user supplies a data-export ZIP | Verify | User-supplied local ZIP explicitly identified as the task data-export source | verify_activity_type_csv_source_package | Oracle permits extracting a downloaded CSV data package, editing its CSV, saving it in a ZIP, and importing it. The supplied package exports ORA_ZMM_ACTIVITY_SUBTYPE only. | Provide a completed export ZIP for ORA_ZMM_MANAGE_ACTIVITY_TYPE_SUBTYPE. Do not use it to create a parent activity type or associate activity functions. | csv_source_zip_path; csv_metadata_object_short_name; csv_metadata_process_status; csv_headers |
| csv_template_package | Completed template ZIP is available for the selected task | Conditional | change_mode is create_subtype or update_subtype and no data-export ZIP is supplied | Verify | Setup task CSV template export REST result | get_activity_type_csv_template_status | The import endpoint requires a ZIP containing the task CSV files. | Wait for a completed template export and provide the downloaded ZIP; do not submit an import while the process is pending. | template_export_process_id: ProcessId; template_export_status: StatusCode; csv_template_zip_path: FileContent |
| activity_subtype_relationship | Supplied subtype belongs to the selected activity type | Conditional | Adding or reviewing a subtype | Verify | Read-only Activity Subtypes LOV | find_activity_subtype_by_type | Activity subtypes are dependent on the selected activity type. | Provide the subtype code. A missing result may be added through the documented task UI; an ambiguous result blocks guidance. | activity_subtype_code: ActivitySubtypeCode; activity_subtype_id: ActivitySubtypeId; activity_type_code: ActivityTypeCode; subtype_enabled: EnabledFlag |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| VERIFIED | The existing relationship is uniquely returned, the new-type definition is complete, or a verified source ZIP is available | Proceed to preview gate |
| NOT_FOUND | A requested new type or subtype is not returned | New type or subtype may proceed only through the documented CSV import or guided UI route |
| PENDING | The selected template-export process has no completed result | Stop before preview; retain the process identifier and wait for its result |
| BLOCKED | The supplied identifiers are missing, ambiguous, conflict with the selected relationship, the source ZIP is not a completed export for this task, or the template result failed | Stop before import |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACTIVITY.DEPENDENCY | step | 3 | resolve_dependency | ready->ACTIVITY.LOOKUP_TYPE;blocked->ACTIVITY.BLOCKED | ACTIVITY.DEFAULT_TAG | stop | Before guided setup, CSV preview, or import routing in the Sales Foundation task. |

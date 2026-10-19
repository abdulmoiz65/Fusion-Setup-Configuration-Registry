# Design Enforcement

Apply these documented design gates before presenting the guided UI procedure or the CSV import preview. They preserve the activity type and subtype relationships required for Sales activity classification.

Sources: [Associate Activity Type with a Function and Subtype](https://docs.oracle.com/en/cloud/saas/sales/oasal/associate-activity-type-with-a-function-and-subtype.html), [About Activity Type and Subtype](https://docs.oracle.com/en/cloud/saas/sales/oasal/about-activity-type-and-subtype.html), and [Add an Activity Subtype Field](https://docs.oracle.com/en/cloud/saas/sales/oasal/add-an-activity-subtype-field.html).

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate requested identifiers | Confirm the type, function, and subtype inputs required for the requested scope. |
| 2 | Verify the current relationships | Use the documented read-only LOVs for the selected type, function, and subtype. |
| 3 | Enforce type and subtype design rules | Require visibility, relationship, enablement, effective-date, and lookup-type tag conditions before guided setup or import preview. When the supplied CSV source package contains only subtype rows, require an existing parent type and limit the import to subtype changes. |
| 4 | Confirm subtype-field availability when in scope | For a subtype-enabled activity experience, enable the field with Application Composer, test the sandbox change, and publish according to business practices. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| change_mode is review or update | Error | find_activity_type_by_function | The selected existing activity type is not associated with at least one selected activity function. | Associate the type with the intended Appointment, Task, or Call Report function in the documented Sales Foundation task. | Yes in the guided task UI or through an approved task CSV import |
| change_mode is create_type | Error |  | The new type lacks a name, code, enabled state, start date, tag, or at least one selected activity function. | Complete the new-type definition before preview. | Yes in the guided task UI |
| Adding or reviewing a subtype | Error | find_activity_subtype_by_type | An existing subtype belongs to a different activity type, or the lookup is ambiguous. | Select the appropriate parent type and use a subtype relationship unique to that type. | Yes in the guided task UI |
| Adding a subtype | Error | find_activity_subtype_by_type | The new subtype is not enabled. | Select Enabled before saving the subtype relationship. | Yes in the guided task UI |
| Adding a new lookup type for all three supplied functions | Error |  | lookup_type_tag is not APPOINTMENT:TASK:CALLREPORT. | Use the documented tag value for the new lookup type. | Yes in the guided task UI |
| CSV import uses a verified package containing only ORA_ZMM_ACTIVITY_SUBTYPE.csv | Error | verify_activity_type_csv_source_package | The request would create a parent activity type, change its function associations, or use a parent code that is not already present. | Limit the CSV change to a unique subtype under an existing parent activity type. Use the guided task UI for parent-type or function-association work. | Yes, by changing the reviewed subtype request or using the guided task UI |
| The business outcome requires users to select subtypes on activity pages or lists | Error |  | The requester has not confirmed that the Subtype field is enabled in Application Composer for the intended activity experience. | Enable the field in an active sandbox, test it, and publish it according to the organization's practices. | Yes with approved Application Composer access |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_activity_type_by_function | Before enforcing visibility of an existing activity type | activity_type_code, activity_function_code, LookupCode, Meaning, EnabledFlag, LookupEnabledFlag, Tag | ora_reference_lookups.md |
| find_activity_subtype_by_type | Before enforcing the supplied subtype-to-type relationship | activity_type_code, activity_subtype_code, ActivitySubtypeCode, ActivityTypeCode, EnabledFlag, Meaning | ora_reference_lookups.md |
| verify_activity_type_csv_source_package | Before enforcing a subtype-only CSV import boundary | csv_source_zip_path, csv_metadata_object_short_name, csv_metadata_process_status, csv_headers, verified_parent_activity_type_code | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACTIVITY.ENFORCE | decision | 6 | design_enforcement | pass->ACTIVITY.VERIFY_CSV_SOURCE;fail->ACTIVITY.BLOCKED | ACTIVITY.LOOKUP_SUBTYPE | stop | Before any attempt to create or change activity type or subtype setup. |

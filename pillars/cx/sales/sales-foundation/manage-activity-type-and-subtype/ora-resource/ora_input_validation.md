# Input Validation

Validate the requested create, review, or update scope before using the Sales Foundation task. This file owns required input shape and presence checks; it does not choose existing activity types, functions, or subtype relationships.

Sources: [About Activity Type and Subtype](https://docs.oracle.com/en/cloud/saas/sales/oasal/about-activity-type-and-subtype.html), [Associate Activity Type with a Function and Subtype](https://docs.oracle.com/en/cloud/saas/sales/oasal/associate-activity-type-with-a-function-and-subtype.html), and [Create a setup task CSV import](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-fscmrestapi-resources-11.13.18.05-setuptaskcsvimports-post.html).

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | change_mode | Stop before lookup or execution routing | Provide create_type, create_subtype, review, update_type_functions, or update_subtype | Always | |
| Activity type | activity_type_code | Stop before lookup or guided setup | Provide the code for the type to create, associate, or review | Always | find_activity_type_by_function |
| New activity type name | activity_type_name | Stop before preview | Provide the display name | change_mode is create_type | |
| Activity functions | activity_function_codes | Stop before lookup or guided setup | Provide one or more selected codes from APPOINTMENT, CALLREPORT, TASK | change_mode is create_type, review of a type-function association, or update_type_functions | find_activity_type_by_function |
| Enablement and effective start | enabled_flag; start_date | Stop before preview | Confirm enablement and a start date | change_mode is create_type or create_subtype | |
| Activity subtype | activity_subtype_code | Stop before subtype guidance | Provide the subtype code to add or review for the selected type | change_mode is create_subtype, review of a subtype, or update_subtype | find_activity_subtype_by_type |
| Subtype enablement | enabled_flag | Stop before guided setup | Confirm that the requested subtype is to be enabled | change_mode is create_subtype | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| An activity subtype is supplied without an activity type | Reject the request because a subtype is dependent on its activity type | A subtype is supplied | |
| No selected activity function is one of APPOINTMENT, CALLREPORT, or TASK | Reject the request because the Sales activity function is unsupported | An activity function is supplied | |
| A new lookup type mapped to all three supplied functions lacks the documented tag | Apply the documented APPOINTMENT:TASK:CALLREPORT default before preview | change_mode is create_type and all three functions are selected | |
| A CSV setup import is requested without a verified task CSV source package | Stop before preview and obtain either a task template ZIP or a completed data-export ZIP for this exact task | change_mode is create_subtype or update_subtype and CSV import is selected | verify_activity_type_csv_source_package |
| A supplied task package is used to create an activity type parent or associate activity functions | Reject that CSV scope: the verified package contains ORA_ZMM_ACTIVITY_SUBTYPE.csv only and has no columns for the parent type name, tag, or function associations | CSV import is selected | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACTIVITY.VALIDATE | step | 1 | validate_input | valid->ACTIVITY.DEFAULT_TAG;invalid->ACTIVITY.BLOCKED | none | stop | Before any lookup, preview, or guided setup for an activity type and subtype mapping. |

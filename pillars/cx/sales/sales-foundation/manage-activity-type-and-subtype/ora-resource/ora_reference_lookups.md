# Reference Lookups

These are read-only Oracle Fusion Sales LOV and Functional Setup Manager calls, plus a user-supplied local package check, used to verify requested relationships and the availability of a task CSV source package. They do not create, update, enable, or associate setup data.

Sources: [Get all activity types](https://docs.oracle.com/en/cloud/saas/sales/faaps/op-activitytypelookupslov-get.html), [Get all activity subtypes](https://docs.oracle.com/en/cloud/saas/sales/faaps/op-activitysubtypeslov-get.html), [Automate Export and Import of CSV File Packages](https://docs.oracle.com/en/cloud/saas/applications-common/26a/oafsm/automate-export-and-import-of-csv-file-packages.html), and [Setup Task CSV Template Exports REST Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-template-exports.html).

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| verify_activity_type_csv_source_package | change_mode is create_subtype or update_subtype and the user supplies a local task data-export ZIP | csv_source_zip_path; archive ASM_SETUP_CSV_METADATA.xml; archive CSV headers; activity_type_code | ZIP contains ASM_SETUP_CSV_METADATA.xml with ObjectShortName ORA_ZMM_MANAGE_ACTIVITY_TYPE_SUBTYPE, ObjectType TASK, ProcessType EXPORT, and ProcessStatus COMPLETED; it contains exactly ORA_ZMM_ACTIVITY_SUBTYPE.csv with headers ActivityTypeCode, ActivitySubtypeCode, Meaning, EnabledFlag, DefaultFlag, StartDateActive, EndDateActive; the parent ActivityTypeCode already occurs in the CSV | csv_metadata_object_short_name; csv_metadata_process_status; csv_headers; verified_parent_activity_type_code; csv_source_zip_path | Any missing, mismatched, incomplete, or ambiguous archive content, or a parent type absent from the source package, blocks preview and import. |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_activity_type_by_function | An activity type and activity function are supplied for review or type-function update | activity_type_code; activity_function_code; current_date | GET /crmRestApi/resources/11.13.18.05/activityTypeLookupsLOV?finder=ByActivityFunctionFinder;Bind_ActivityFunctionCode={activity_function_code},Bind_CurrentDate={current_date}&fields=LookupCode,LookupType,Meaning,EnabledFlag,LookupEnabledFlag,StartDateActive,EndDateActive,Tag&onlyData=true | LookupCode, LookupType, Meaning, EnabledFlag, LookupEnabledFlag, StartDateActive, EndDateActive, Tag | Exactly one returned LookupCode equals activity_type_code | activity_type_code: LookupCode; activity_type_name: Meaning; activity_type_enabled: EnabledFlag; activity_type_tag: Tag | No result permits a new-type candidate only through the documented guided UI route. More than one matching result or a REST failure blocks guidance. |
| find_activity_subtype_by_type | An activity type and subtype are supplied | activity_type_code; activity_subtype_code | GET /crmRestApi/resources/11.13.18.05/activitySubtypesLOV?finder=UniqueTypeSubtype;ActivitySubtypeCode={activity_subtype_code},ActivityTypeCode={activity_type_code}&fields=ActivitySubtypeCode,ActivitySubtypeId,ActivityTypeCode,DefaultFlag,EnabledFlag,EndDateActive,Meaning,StartDateActive&onlyData=true | ActivitySubtypeCode, ActivitySubtypeId, ActivityTypeCode, DefaultFlag, EnabledFlag, EndDateActive, Meaning, StartDateActive | Return zero or one record for the exact subtype and activity-type pair | activity_subtype_code: ActivitySubtypeCode; activity_subtype_id: ActivitySubtypeId; activity_type_code: ActivityTypeCode; subtype_enabled: EnabledFlag; subtype_name: Meaning | No result permits a user-guided add in the documented task UI. More than one result or a REST failure blocks guidance. |
| get_activity_type_csv_template_status | A CSV import is selected and a template-export process identifier is supplied | task_code; template_export_process_id | GET /fscmRestApi/resources/11.13.18.05/setupTaskCSVTemplateExports/{task_code}/child/SetupTaskCSVTemplateExportProcess/{template_export_process_id}; then GET /fscmRestApi/resources/11.13.18.05/setupTaskCSVTemplateExports/{task_code}/child/SetupTaskCSVTemplateExportProcess/{template_export_process_id}/child/SetupTaskCSVTemplateExportProcessResult | ProcessCompletedFlag, ProcessId, StatusCode, FileName | ProcessCompletedFlag is true and exactly one result has StatusCode COMPLETED or COMPLETED_WARNINGS with a template ZIP available | template_export_process_id: ProcessId; template_export_status: StatusCode; csv_template_zip_path: FileContent | A false completion flag or no result is pending and blocks preview. COMPLETED_ERRORS or multiple results blocks import; retrieve the ProcessLog once and do not resubmit automatically. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Activity type lookup returns one matching type for the selected function | Use the returned type details to evaluate the design rules. |
| Activity type lookup returns no matching type | Continue to a documented new-type candidate and use the guided UI route. Do not claim a change was made. |
| Subtype lookup returns one matching relationship | Use the returned subtype details to evaluate the design rules. |
| Subtype lookup returns no matching relationship | Treat the subtype as absent only for a user-guided add in the documented task UI; do not claim it was created. |
| Either LOV call fails or returns an ambiguous result | Stop before guided setup and do not retry automatically. |
| Template-export status is incomplete or has no result | Stop before preview and import. Retain the process identifier and wait for a completed result; do not create another export automatically. |
| A user-supplied completed data-export ZIP matches the task and CSV schema | Treat it as the import source package. Extract it, make only the reviewed subtype-row change, repackage it as a new ZIP, then build an immutable preview. |
| A CSV source package contains only ORA_ZMM_ACTIVITY_SUBTYPE.csv | Permit only subtype-row changes under an existing activity type. Do not use it to create the parent type or its activity-function associations. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ACTIVITY.LOOKUP_TYPE | step | 4 | reference_lookup | matched->ACTIVITY.LOOKUP_SUBTYPE;not_found->ACTIVITY.LOOKUP_SUBTYPE;not_applicable->ACTIVITY.LOOKUP_SUBTYPE;ambiguous->ACTIVITY.BLOCKED;failure->ACTIVITY.FAILED | ACTIVITY.DEPENDENCY | stop | Before mapping the selected activity type to a function or subtype. It is not applicable to a subtype-only CSV import with no activity-function change. |
| ACTIVITY.LOOKUP_SUBTYPE | step | 5 | reference_lookup | found->ACTIVITY.ENFORCE;not_found->ACTIVITY.ENFORCE;not_applicable->ACTIVITY.ENFORCE;ambiguous->ACTIVITY.BLOCKED;failure->ACTIVITY.FAILED | ACTIVITY.LOOKUP_TYPE | stop | Before adding or reviewing a subtype for the selected activity type. |
| ACTIVITY.VERIFY_CSV_SOURCE | step | 7 | reference_lookup | ready->ACTIVITY.EXECUTION_GATE;pending->ACTIVITY.BLOCKED;not_applicable->ACTIVITY.EXECUTION_GATE;failure->ACTIVITY.FAILED | ACTIVITY.ENFORCE | stop | Before a requested CSV setup import is previewed, using either the local data-export-package check or the template-export status lookup. |

# Design Enforcement

Apply these documented gates before presenting guided setup, downstream sales-stage association, or immutable CSV package handoff. They preserve the distinction between a template header, its individual tasks, and the separate sales-stage association that exposes generated tasks to opportunity users.

Sources: [Shared task-template fields and defaults](https://docs.oracle.com/cd/G55130_01/trans/F77858-09/getting-started-with-your-partner-relationship-management-implementation.pdf#page=112), [Add Task Templates to Sales Stages](https://docs.oracle.com/en/cloud/saas/sales/oasal/add-task-templates-to-sales-stages.html), [Export and Import of CSV File Packages](https://docs.oracle.com/en/cloud/saas/applications-common/26b/oafsm/export-and-import-of-csv-file-packages.html), [Create an activity](https://docs.oracle.com/en/cloud/saas/sales/faaps/op-activities-post.html), and the current target-environment task export and import validation for ZBS_MANAGE_SALES_TASK_TEMPLATE on 2026-08-10.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm task ownership | Use Manage Sales Task Templates for the Opportunity template and its individual task definitions. |
| 2 | Enforce template-before-task order | Create or select the template header before adding individual tasks. |
| 3 | Preserve documented scheduling semantics | Treat lead time as the offset from template use to task start, and template duration as the offset from task start to due date. A blank duration creates a task without a due date. |
| 4 | Route sales-stage association | Use Manage Sales Methods and Sales Stages only after the template exists. |
| 5 | Enforce automatic-generation intent | Select Automatically generated when generated tasks must appear for users in the opportunity Activities tab. |
| 6 | Preserve CSV activity identities | Give every ORA_ACTIVITY.csv child row a nonblank, unique ActivityNumber no longer than 64 characters. |
| 7 | Preserve task-specific CSV structure | Derive filenames, headers, and allowed columns from the current export or template; don't invent a schema or a direct Sales Task Template REST payload. |
| 8 | Preserve the Data Loader boundary | Validate and hash the final immutable package, then hand it to Core Data Loader without requesting package approval; Data Loader owns Task Hook preview, later contextual approval, upload, and initiation. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| create_template or update_template | Error | | The template type isn't Opportunity; the user has not explicitly confirmed Common Set or selected a different exact Set ID/Set Code; Common Set was inferred or paired with a supplied non-Common identity; the set fails input validation or cannot be verified in exact selected-target setup/package evidence; the documented setup page cannot select the exact set; or subtype intent is unresolved. | Use Opportunity, ask the explicit Common-vs-different-set question, and preserve one confirmed exact set identity, including a verified zero. Never infer Common Set from its number. Leave subtype blank unless this is explicitly an Assessment template. | Yes in the guided setup task or reviewed task CSV package |
| import_task_csv changes template set | Error | verify_sales_task_template_csv_source_package | The confirmed set is unknown in exact-target package evidence, cross-environment, or differs from the source export or candidate package row. | Reconfirm one exact set, obtain a current exact-target source package, and rebuild the candidate without substituting a set. | Yes before handoff |
| add_template_task or create_template includes tasks | Error | | The header doesn't exist before the individual task, or the task lacks a subject. | Create or select the template first, then add the task with its required subject and reviewed optional values. | Yes in the guided setup task or reviewed task CSV package |
| A task supplies lead time or template duration | Error | | The requester treats lead time as the due-date interval or duration as the start-date offset. | Apply lead time to task start and duration from start to due date; preserve a blank duration when no due date is intended. | Yes before save or package validation |
| associate_to_sales_stage | Error | | The template doesn't exist, the sales method or stage isn't identified, or association is attempted in the wrong setup task. | Complete the template, then use Manage Sales Methods and Sales Stages for the intended stage. | Yes through the documented downstream task |
| Generated tasks must appear automatically in opportunity Activities | Error | | generation_type isn't Automatically generated. | Select Automatically generated; Oracle states that otherwise the associated tasks won't appear to users. | Yes through Manage Sales Methods and Sales Stages |
| import_task_csv contains individual template tasks | Error | verify_sales_task_template_csv_source_package | Any ORA_ACTIVITY.csv row has a blank ActivityNumber, an identifier longer than 64 characters, or a duplicate identifier within the candidate package. | Assign every task row a reviewed, unique activity number before rebuilding and validating the immutable package. | Yes before handoff |
| import_task_csv and csv_source_zip_path is supplied | Error | verify_sales_task_template_csv_source_package | The source or final package is for another task, is incomplete, changes the exported structure, changes outside the reviewed row delta, or lacks exact target/task identity, SHA-256, and persisted Data Loader task-context binding. | Obtain the current exact-task package, preserve its structure, build the reviewed delta, reopen and validate it, then hand it to Core Data Loader with a validated task context and without synthesizing values. | Yes before handoff |
| import_task_csv and template_export_process_id is supplied instead of csv_source_zip_path | Error | get_sales_task_template_csv_template_status | The export is pending or failed, its task code differs, its result has no ZIP, or the final candidate fails immutable package validation. | Wait for the exact-task result, inspect the returned ZIP, build and validate the final package, then hand it to Core Data Loader. | Yes before handoff |
| import_task_csv is ready for Core Data Loader | Error | verify_sales_task_template_csv_source_package | This child requests package approval, creates or reconstructs a Task Hook envelope, or treats package validation as upload authorization. | Hand off the unchanged validated package and evidence only; Core Data Loader creates its Task Hook-bound preview and later requests contextual approval. | Yes before handoff |
| A direct Sales Task Template REST mutation is requested | Error | | No public task-specific create or update REST contract has been established by the reviewed sources. | Use the documented setup UI or approved Functional Setup Manager CSV import route. | Yes by changing the execution route |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_sales_task_template_csv_source_package | A local data-export or template ZIP is supplied for import | csv_source_zip_path, verified_task_code, csv_member_names, csv_headers, source_package_kind | ora_reference_lookups.md |
| get_sales_task_template_csv_template_status | A template-export process identifier is supplied for import | task_code, template_export_process_id, template_export_status, csv_source_zip_path | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_TASK_TEMPLATE.ENFORCE | decision | 5 | design_enforcement | pass->SALES_TASK_TEMPLATE.EXECUTION_GATE;fail->SALES_TASK_TEMPLATE.BLOCKED | SALES_TASK_TEMPLATE.LOOKUP_CSV_SOURCE | stop | Every supported Sales Task Templates request, including review_template and export_task_csv. Apply only design rules relevant to change_mode; nonmutating review/export does not require mutation approval or an import package. When template set is in scope, reject inferred Common Set and wrong, conflicting or cross-environment identity |

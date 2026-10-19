# Dependency Readiness

## FSM Task Identity Policy

Require exact task code/name, selected task `SKILL.md`, target environment, and
immutable archive SHA-256 throughout review, export, package preparation, and
validation.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  `TaskCode`, `TaskName`, offering, and functional area.

The persisted context may come from a project setup-task plan without creating
an Oracle Run Book. Never hand-author, infer, or synthesize it solely to satisfy
Data Loader.

The documented flow creates the task-template header before its individual tasks. A reference-data set is selected for the applicable business unit. If generated tasks must appear for salespeople at an opportunity sales stage, the completed template is associated later through Manage Sales Methods and Sales Stages. CSV automation additionally requires a verified task-specific package.

Sources: [Shared task-template fields and defaults](https://docs.oracle.com/cd/G55130_01/trans/F77858-09/getting-started-with-your-partner-relationship-management-implementation.pdf#page=112), [Add Task Templates to Sales Stages](https://docs.oracle.com/en/cloud/saas/sales/oasal/add-task-templates-to-sales-stages.html), [Export and Import of CSV File Packages](https://docs.oracle.com/en/cloud/saas/applications-common/26b/oafsm/export-and-import-of-csv-file-packages.html), [Create an activity](https://docs.oracle.com/en/cloud/saas/sales/faaps/op-activities-post.html), and the current target-environment task export and import validation for ZBS_MANAGE_SALES_TASK_TEMPLATE on 2026-08-10.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Authorized setup access | An authorized sales administrator or setup user opens the exact Manage Sales Task Templates task. |
| 2 | Template header | Create or identify the Opportunity template with its name, active state, subtype intent, and template set. |
| 3 | Individual template tasks | After the template header exists, add each task definition with a subject and any reviewed optional scheduling or classification values. For CSV import, every ORA_ACTIVITY.csv row also requires its own nonblank activity number. |
| 4 | Opportunity sales-stage association | When automatic stage-specific tasks are required, use Manage Sales Methods and Sales Stages after the template exists and associate it to the intended stage. |
| 5 | Task CSV source package | For bulk setup changes, obtain a completed template-export ZIP or verified completed data-export ZIP for ZBS_MANAGE_SALES_TASK_TEMPLATE before package preparation. |
| 6 | Immutable Data Loader handoff | Validate the final ZIP against the exact target, task identity and persisted Data Loader task context, ASM identity, members, headers, reviewed row delta, and reopened SHA-256, then hand it to Core Data Loader without requesting child-level approval. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| setup_access | Sales administrator or setup-user access is available | Yes | Guided setup or review is requested | Confirm | Request context | | Oracle identifies these roles for the documented procedure. | Sign in with authorized setup access; do not claim the page was changed without it. | authorized_setup_access |
| task_template_header | The named Opportunity task template exists before an individual task or stage association is added | Conditional | add_template_task, update_template, review_template, or associate_to_sales_stage | Confirm | Manage Sales Task Templates page | | Oracle's procedure creates the template first and then its individual tasks; stage association also selects a template created earlier. | Select the exact template in the documented setup page. A missing or ambiguous selection blocks update or association guidance. | template_name; template_type; active_flag; template_subtype; template_set |
| template_set_selection | A reference-data set appropriate for the applicable business unit is selected | Yes | create_template or update_template changes the set | Confirm | Explicit user set decision and Template Set selection on the setup page | | Oracle requires selecting the set to associate with the business unit. | Ask whether Common Set should be used or a different exact Set ID or Set Code should be selected; never infer Common Set when a value was not supplied. | SetSelectionDecision; template_set; SetId; SetCode |
| task_definition_order | The template header exists before an individual task is created | Yes | add_template_task or create_template includes tasks | Confirm | Normalized setup plan | | Oracle documents the template and task creation as separate ordered steps. | Create or select the header first, then add task details. For import_task_csv, assign every task a nonblank unique activity_number no longer than 64 characters. | template_name; activity_number; task_subject |
| sales_stage_owner_task | Sales-stage association is routed to Manage Sales Methods and Sales Stages | Conditional | associate_to_sales_stage | Confirm | Normalized setup plan | | The task-template setup page creates the template; the separate Opportunities task owns stage association. | Complete the template first, then use the specified sales method and sales stage. | sales_method_name; sales_stage_name; generation_type |
| csv_local_source_package | A current task-specific CSV source ZIP is available | Conditional | import_task_csv and csv_source_zip_path is supplied | Verify | User-supplied local ZIP explicitly identified as the source package | verify_sales_task_template_csv_source_package | The import contract requires a ZIP containing the setup-task CSV files. | Supply a completed package for ZBS_MANAGE_SALES_TASK_TEMPLATE and retain its filenames and headers. | task_code; csv_source_zip_path; csv_member_names; csv_headers |
| csv_template_source_package | A completed task CSV template export is available | Conditional | import_task_csv and template_export_process_id is supplied instead of csv_source_zip_path | Verify | Setup task CSV template export result | get_sales_task_template_csv_template_status | The template export provides the task-specific ZIP structure used to enter and upload setup data. | Wait for the existing process to complete and use its returned ZIP. | task_code; template_export_process_id; template_export_status; csv_source_zip_path |
| csv_data_loader_handoff | Final immutable package is bound to exact task identity, persisted Data Loader task context, and validation evidence | Conditional | import_task_csv is ready for execution routing | Verify | Reopened final ZIP and completed task-local package validation | verify_sales_task_template_csv_source_package | Core Data Loader owns Task Hook preview, later contextual approval, upload, and initiation | Bind final path/SHA-256, exact TaskCode/TaskName, ASM/member/header/delta receipt, and the persisted project context TaskContextPath/positive TaskSequence; never hand-author or synthesize task context | final package and task identity; persisted Data Loader task context; package validation result |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| VERIFIED | Required access, ordered setup inputs, set choice, downstream routing, and any CSV source are confirmed | Proceed to the next rule |
| NOT_FOUND | An existing template requested for update, task addition, review, or stage association isn't found by the authorized user | Stop that operation; create a new template only when explicitly requested |
| PENDING | A selected CSV template export has no completed result | Stop before package preparation or handoff and retain the existing process identifier |
| BLOCKED | Access, required predecessor, template selection, set choice, stage identifiers, or task-specific CSV source is missing or ambiguous | Stop before any mutation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_TASK_TEMPLATE.DEPENDENCY | step | 3 | resolve_dependency | ready->SALES_TASK_TEMPLATE.LOOKUP_CSV_SOURCE;blocked->SALES_TASK_TEMPLATE.BLOCKED | SALES_TASK_TEMPLATE.DEFAULTS | stop | Every supported Sales Task Templates request. Resolve only dependencies applicable to change_mode; full-task export requires task/target context, not an existing template, template-set selector, mutation ZIP or Data Loader task context. Block when an applicable required template-set choice is not explicit |

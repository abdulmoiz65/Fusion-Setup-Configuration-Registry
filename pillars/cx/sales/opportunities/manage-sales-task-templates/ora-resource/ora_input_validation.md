# Input Validation

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

Validate the requested template, template-task, sales-stage-association, or CSV-package scope before using the setup task. This file owns input presence and shape checks; it does not claim that a template already exists or that a Fusion change has been made.

Sources: [Shared task-template fields and defaults](https://docs.oracle.com/cd/G55130_01/trans/F77858-09/getting-started-with-your-partner-relationship-management-implementation.pdf#page=112), [Add Task Templates to Sales Stages](https://docs.oracle.com/en/cloud/saas/sales/oasal/add-task-templates-to-sales-stages.html), [Create a setup task CSV import](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-fscmrestapi-resources-11.13.18.05-setuptaskcsvimports-post.html), [Create an activity](https://docs.oracle.com/en/cloud/saas/sales/faaps/op-activities-post.html), and the current target-environment task export and import validation for ZBS_MANAGE_SALES_TASK_TEMPLATE on 2026-08-10.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | change_mode | Stop before defaulting, lookup, or execution routing | Provide create_template, add_template_task, update_template, review_template, associate_to_sales_stage, export_task_csv, or import_task_csv | Always | |
| Task template identity | template_name | Stop before guided setup or package validation | Provide the exact task template name | create_template, add_template_task, update_template, review_template, or associate_to_sales_stage | |
| Template set | SetSelectionDecision plus template_set; exact SetId or SetCode when a different set is selected | Stop before creating or changing the template set | Ask whether Common Set should be used or a different exact Set ID or Set Code should be selected; never infer Common Set from an absent value | create_template or update_template changes the set | |
| Template subtype intent | assessment_template_flag or template_subtype | Stop before creating the template | Confirm Assessment when the template is for assessment; otherwise confirm that the subtype is blank | create_template or update_template | |
| Template task definition | task_subject | Stop before creating the individual template task | Provide the task subject; task_description, lead_time_days, task_type, template_duration_days, and priority are optional | add_template_task or create_template includes a task definition | |
| CSV activity identity | activity_number | Stop before package validation | Provide a nonblank activity number for every ORA_ACTIVITY.csv child row; use a unique value no longer than 64 characters | import_task_csv and the package contains an individual template task | |
| Sales stage association | sales_method_name; sales_stage_name; generation_type | Stop before downstream association guidance | Provide the sales method and stage and use Automatically generated when tasks must appear automatically in opportunity Activities | associate_to_sales_stage | |
| CSV source package | csv_source_zip_path or template_export_process_id | Stop before package validation | Provide a task-specific completed data-export ZIP or completed CSV-template-export process for ZBS_MANAGE_SALES_TASK_TEMPLATE | import_task_csv | |
| Immutable Data Loader handoff | Exact target/release/task identity, TaskCode fixed to ZBS_MANAGE_SALES_TASK_TEMPLATE, exact TaskName, final package path/SHA-256, ASM identity, member inventory, exported headers, reviewed row delta, and validation result; require persisted TaskContextPath plus positive TaskSequence resolved to the exact skill path, TaskCode, TaskName, offering, and functional area | Block Core Data Loader handoff | Complete package preparation, reopen the final ZIP, bind its unchanged bytes to exact task identity, validate the persisted Data Loader task context, and require persisted Data Loader task context | import_task_csv is ready for handoff | verify_sales_task_template_csv_source_package |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| template_name or task_subject is blank after trimming | Reject the request and ask for the missing business value | The corresponding field is required | |
| ConflictId is missing, blank after trimming, or not an integer in any ZMM_TASK_TEMPLATE.csv row | Block package handoff and Data Loader preview with the affected row; ActivityTemplateSetEO requires ConflictId. Accept numeric 0 and CSV text 0 as populated values, preserve them during serialization, and validate the final packaged CSV and captured native CSV cells rather than only the header. | import_task_csv | |
| activity_number is blank after trimming | Reject the candidate before package handoff because the current FSM object requires ActivityNumber for each ORA_ACTIVITY.csv row | import_task_csv | |
| activity_number is longer than 64 characters or repeats within the candidate package | Reject the candidate before package handoff and require a distinct value within the documented identifier length | import_task_csv | |
| template_type is supplied with a value other than Opportunity | Reject the request because this skill owns the Opportunity task-template setup task | create_template or update_template | |
| assessment_template_flag is false but template_subtype is populated | Reject the request and ask whether the template is an Assessment template or should have a blank subtype | create_template or update_template | |
| lead_time_days or template_duration_days is supplied but is not a valid day count accepted by the setup page | Reject the value before guided setup or package validation | A template task includes either value | |
| automatic opportunity visibility is requested but generation_type is not Automatically generated | Reject the association plan and require the documented value | associate_to_sales_stage | |
| template_set is absent and the user has not confirmed Common Set or selected a different exact SetId or SetCode | Stop and ask the explicit Common-vs-different-set question before guided setup or package review | create_template or update_template changes the set | |
| Common Set is inserted from a product default, environment convention, prior example, or implementation assumption without user confirmation | Reject the inferred value and return to set selection; Common Set confirmation does not authorize a mutation | create_template, update_template, or import_task_csv changes the template set | |
| A supplied SetId is not an integer, a supplied SetCode is blank, supplied SetId and SetCode identify different sets, or confirmed Common Set is paired with a non-Common set identity | Reject before guided setup or package review; show the sanitized conflict and request one valid explicit set decision. Validate supplied selectors without requiring both ID and code. Do not reject an integer solely because it is zero: require explicit selection and exact selected-target setup/package evidence, and preserve numeric or CSV text zero without converting it to a blank value | create_template, update_template, or import_task_csv changes the template set | verify_sales_task_template_csv_source_package |
| A template package row's set differs from the confirmed choice, documented setup selection, fresh source export, or selected target environment | Reject the complete candidate package; never substitute Common Set, another environment's set, or a close match | import_task_csv | verify_sales_task_template_csv_source_package |
| A CSV import is requested without a verified current package for this exact setup task | Stop before handoff and obtain a current task template ZIP or completed data-export ZIP | import_task_csv | |
| TaskCode, target/release, TaskName, final package path/SHA-256, ASM/member/header receipt, or reviewed row delta is missing or inconsistent, or a persisted project context lacks exact TaskContextPath/positive TaskSequence | Reject Core Data Loader handoff and rerun validation; missing or inconsistent task context blocks handoff; never hand-author or synthesize task context | import_task_csv | verify_sales_task_template_csv_source_package |
| This child skill requests package approval or requires a Task Hook approval before handoff | Refuse the child approval gate; hand off the validated immutable package so Core Data Loader can create its own Task Hook-bound preview and later request contextual approval | import_task_csv before handoff | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_TASK_TEMPLATE.VALIDATE | step | 1 | validate_input | valid->SALES_TASK_TEMPLATE.DEFAULTS;invalid->SALES_TASK_TEMPLATE.BLOCKED | none | stop | Before any lookup, package validation, guided setup, export, import handoff, or sales-stage association guidance; require an explicit Common Set confirmation or different exact set and reject malformed, unknown, or conflicting set identity whenever template set is in scope. |

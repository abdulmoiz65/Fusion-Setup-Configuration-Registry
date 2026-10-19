# Reference Lookups

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

Use only the documented Functional Setup Manager template-export status call and a local inspection of an explicitly supplied task package. No public read-only Sales Task Template REST resource was identified, so existing templates and reference-data sets remain selections in the documented setup page rather than invented REST lookups.

Sources: [Setup Task CSV Template Exports REST Endpoints](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/api-setup-task-csv-template-exports.html), [Create a setup task CSV template export](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-fscmrestapi-resources-11.13.18.05-setuptaskcsvtemplateexports-post.html), [Export and import task setup data using CSV files](https://docs.oracle.com/en/cloud/saas/applications-common/faqac/export-and-import-task-setup-data-using-csv-files.html), and the completed current target-environment template export for ZBS_MANAGE_SALES_TASK_TEMPLATE on 2026-08-10.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| verify_sales_task_template_csv_source_package | change_mode is import_task_csv and a local ZIP is supplied or prepared | Explicit SetSelectionDecision when template set changes, with user-confirmed Common Set or a different exact SetId/SetCode; source/final ZIP paths and SHA-256; exact target/release/task code/name; ASM metadata; exported members/headers; reviewed row delta; and persisted Data Loader task-context fields | Reject inferred Common Set, then require a readable exact-task source and immutable final ZBS_MANAGE_SALES_TASK_TEMPLATE ZIP with ZMM_TASK_TEMPLATE.csv, ORA_ACTIVITY.csv, one exact ASM metadata file, preserved members/headers, reviewed-only rows, valid ActivityNumber values, reopened SHA-256 equality, and persisted Data Loader task context | SetSelectionDecision and exact set identity when changed; source/final package receipts, SHA-256, task identity, persisted Data Loader task context, member/header evidence, reviewed delta, validation result | Missing set choice, automatically inferred Common Set, wrong-task, incomplete, schema-altered, changed, hash-mismatched evidence, invalid ActivityNumber, or inconsistent persisted Data Loader task context blocks handoff; never hand-author or synthesize task context, guess schema, or request child approval |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| get_sales_task_template_csv_template_status | change_mode is import_task_csv and template_export_process_id is supplied instead of a local data-export ZIP | task_code fixed to ZBS_MANAGE_SALES_TASK_TEMPLATE; template_export_process_id | GET /fscmRestApi/resources/11.13.18.05/setupTaskCSVTemplateExports/{task_code}/child/SetupTaskCSVTemplateExportProcess/{template_export_process_id}; then GET its SetupTaskCSVTemplateExportProcessResult child | TaskCode, ProcessCompletedFlag, ProcessId, StatusCode, FileName, FileContent | TaskCode is exact, ProcessCompletedFlag is true, and exactly one process result is COMPLETED or COMPLETED_WARNINGS with a ZIP in FileContent | template_export_process_id: ProcessId; template_export_status: StatusCode; csv_source_zip_path: FileContent; csv_source_file_name: FileName | An incomplete process or no result is pending. COMPLETED_ERRORS, a task mismatch, multiple matching results, or a request failure blocks import; retrieve ProcessLog once when available and don't resubmit automatically. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| The final local package is verified for the exact task and retains the source structure | Hand the unchanged package and validation receipt to Core Data Loader; this child doesn't build or approve the Task Hook upload preview. |
| The template-export process is complete with a usable ZIP | Download the returned FileContent, inspect the ZIP locally, populate the current template structure, build and reopen the immutable candidate, then hand it to Core Data Loader after validation. |
| The template-export process is pending | Stop before package preparation and handoff; retain the existing process identifier and wait for its result. |
| The source task, ZIP structure, member names, or headers do not match | Block the import; obtain a new current task export or template rather than guessing the schema. |
| An ORA_ACTIVITY.csv child row has a blank ActivityNumber | Block the handoff and assign a reviewed, unique identifier no longer than 64 characters before rebuilding and revalidating the immutable package. |
| An existing task template or reference-data set must be selected | Use the documented Manage Sales Task Templates page with authorized access; do not substitute an undocumented REST endpoint. |
| SetId/SetCode is malformed, conflicts with the explicit choice or source package, confirmed Common Set maps to a non-Common set, or a candidate row uses another target's set | Block guided/package progression, disclose the sanitized mismatch, and require one corrected explicit selection; do not invent a REST lookup or substitute a set. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_TASK_TEMPLATE.LOOKUP_CSV_SOURCE | step | 4 | reference_lookup | ready->SALES_TASK_TEMPLATE.ENFORCE;pending->SALES_TASK_TEMPLATE.BLOCKED;not_applicable->SALES_TASK_TEMPLATE.ENFORCE;failure->SALES_TASK_TEMPLATE.FAILED | SALES_TASK_TEMPLATE.DEPENDENCY | stop | Before package validation or import handoff, including exact set-choice/source-row reconciliation; not applicable to guided UI, review, export, or downstream sales-stage guidance. |

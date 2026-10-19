# Attachment File Formats

## Purpose

Use this reference when a pillar setup-task skill routes an attachment-file-
format task to `core.fusion-api.apps-common.attachments`. This route delegates
manual configuration guidance to `shared.common.manual-tasks`; it does not
implement CSV transport, Fusion REST transport, or UI automation.

Examples include:

| Task code | Task name |
| --- | --- |
| `ORA_FND_APP_DOCUMENT_FILE_FORMATS` | Manage Attachment File Formats |

## Manual Execution Route

1. Obtain the calling pillar task skill's exact task code, task name, offering,
   functional-area, and a positive task sequence. If any identifier is missing
   or conflicts, stop with `input_validation`; do not choose a task by name
   alone.
2. Use `shared.setup-export.task-level-export` to resolve the authoritative
   task code, functional area, and offering from the calling skill metadata,
   live task lookup when available, or
   `knowledge/setup-task-catalog/release/setupTasksAll.json`.
3. Check the resolved task's flags. For `ORA_FND_APP_DOCUMENT_FILE_FORMATS`,
   `ExportImportSupportedFlag=Y` but `CSVExportImportSupportedFlag=N`; that
   means no CSV export or import workflow is selected.
4. Invoke `shared.common.manual-tasks` with:

   - `manual_task_name=Manage Attachment File Formats`
   - the user's exact `approved_configuration_change`
   - the exact `target_environment`
   - task-specific instructions:  [How can I restrict file formats for attachments?](https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/how-can-i-restrict-file-formats-for-attachments.html)

5. The shared skill must provide instructions for the user to make and verify
   the approved configuration in Fusion. It must not open Fusion or perform the
   change on the user's behalf.

## Automation Boundary

`CSVExportImportSupportedFlag` is `N`. Do not reinterpret
`ExportImportSupportedFlag=Y` as proof of an executable export or import route.
No export or import workflow is selected for this task.

Do not route this task through:

- `shared.setup-export.task-level-export`
- `core.data-loader`
- task-level FSM CSV export or import
- UCM, ESS, HDL, FBDI, CX Import, or spreadsheet loaders
- public, private, or inferred REST or SOAP endpoints
- browser automation or direct UI control

Report `manual verification pending` until the user confirms the readback or
safe test result. Never report automated execution success.

## Boundaries

Use only `shared.common.manual-tasks` for attachment-file-format execution
guidance. Do not invoke `setupTaskCSVExports` or `setupTaskCSVImports`
directly, and do not duplicate authentication, CSV transport, or UI execution.
Classify an unsupported route as `catalog_or_metadata_mismatch` and a missing
approved configuration change or target environment as `input_validation`.
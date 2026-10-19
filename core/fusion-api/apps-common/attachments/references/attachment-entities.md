# Attachment Entities

## Purpose

Use this reference when a pillar setup-task skill routes an attachment-entity
task to `core.fusion-api.apps-common.attachments`. This route manages
task-level attachment-entity setup data through the supported CSV export and
FSM CSV import workflows; it does not implement its own Fusion REST transport.

Examples include:

| Task code | Task name |
| --- | --- |
| `FND_MANAGE_ATTACHMENT_ENTITIES` | Manage Attachment Entities |
| `FND_MANAGE_APPLICATIONS_CORE_ATTACHMENT_ENTITIES` | Manage Applications Core Attachment Entities |

## Eligibility Gate

1. Obtain the calling pillar task skill's exact task code, task name, offering,
   functional-area, and a positive task sequence. If any identifier is missing
   or conflicts, stop with `input_validation`; do not choose a task by name
   alone.
2. Use `shared.setup-export.task-level-export` to resolve the authoritative
   task code, functional area, and offering from the calling skill metadata,
   live task lookup when available, or
   `knowledge/setup-task-catalog/release/setupTasksAll.json`.
3. Check the resolved task's `ExportImportSupportedFlag`. If it is not `Y`, do
   not start an attachment-entity setup-data export or import. Report the
   resolved task metadata and that this attachment CSV route is unsupported.
4. The task-level export workflow also enforces its required
   `CSVExportImportSupportedFlag` check before it creates a CSV export. Do not
   bypass that shared-workflow gate.

## Export Attachment-Entity Setup Data

Delegate export to `shared.setup-export.task-level-export`. That shared skill
owns task-code resolution, CSV setup-task export, polling, download, and
project-workspace persistence.

1. Pass the calling attachment-entity task's exact task code or task name,
   offering, and functional-area context.
2. Let the shared skill confirm the exact task and supported flags.
3. Let it export the CSV setup data and persist the ZIP or process log under:

   ```text
   project/{project_id}/exports/{offering}/{functional-area}/{task-name}
   ```

4. Return the exported artifact reference, `ProcessId`, outcome, and
   diagnostics to the calling pillar skill.

Use normal data-export mode for a configuration baseline. Use template/spec
mode only when the caller explicitly requests an attachment-entity CSV template
rather than current setup data.

## Import Attachment-Entity Setup Data

Delegate import only to `core.data-loader` using the FSM CSV Import route.
This is a configuration-changing operation.

1. Resolve the task code, task name, offering, functional area, and positive
   sequence from the calling pillar skill context. Reapply the eligibility gate
   before accepting the import.
2. Require a nonempty, valid ZIP produced for the resolved attachment-entity
   task. It must contain the exact-case member `ASM_SETUP_CSV_METADATA.xml`
   plus the task CSV files. Preserve the ZIP bytes unchanged.
3. Route the request to `core.data-loader` with:

   | Data Loader input | Required value |
   | --- | --- |
   | `requested_operation` | `FSM CSV Import` |
   | `task_context` | Resolved task code, exact task name, and positive sequence (in the Task Hook context) |
   | `data_load_source_or_registered_business_object` | The validated FSM ZIP path |
   | `fusion_environment_context` | Confirmed target Fusion environment |

4. Let Data Loader classify the immutable ZIP as FSM, perform its Task Hook
   validation and approval-preview lifecycle, upload the approved archive, and
   initiate the Fusion import. A standalone approval applies only to the exact
   reviewed archive; do not submit it before that confirmation.
5. Return Data Loader's initiation result and diagnostics to the calling pillar
   skill. Do not poll for status unless the caller explicitly asks for status,
   progress, results, counts, or errors.

## Boundaries

Use only `shared.setup-export.task-level-export` for attachment-entity CSV
export and `core.data-loader` for attachment-entity FSM CSV import. Do not
route imports to `shared.setup-import.task-level-import`, invoke
`setupTaskCSVImports` directly, or duplicate authentication, CSV transport,
Task Hook validation, or Data Loader approval handling. Classify an unsupported
flag as `catalog_or_metadata_mismatch` and an unapproved import as
`approval_blocker`.

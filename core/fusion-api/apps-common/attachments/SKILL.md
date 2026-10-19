---
skill_id: "core.fusion-api.apps-common.attachments"
name: "Apps Common Attachments"
description: "Manages Oracle Fusion attachment-entity and attachment-category setup data through task-level CSV export and the approved Data Loader FSM CSV import workflow, and routes attachment-file-format setup to manual execution guidance."
layer: "core"
pillar: "Core"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "Central platform team"
version: "0.1.0"
inputs: ["fusion_environment_context", "attachment_task_context", "execution_options"]
outputs: ["execution_result", "diagnostics", "audit_summary"]
depends_on: ["shared.setup-export.task-level-export", "core.data-loader", "shared.common.manual-tasks"]
uses_core: []
persists_project_state: false
workspace_outputs: []
applicability:
  industries: ["All"]
  countries: ["All"]
  fusion_releases: ["Current Oracle Fusion Cloud Applications release"]
side_effects: ["May export attachment-entity or attachment-category setup data or submit an approved FSM CSV import through the selected workflow; attachment-file-format tasks provide manual-only guidance."]
required_privileges: ["Fusion privileges required by the selected setup-task export and Data Loader workflows", "Privilege to access the Attachment File Formats Setup and Maintenance task"]
---

# Apps Common Attachments

## Purpose

Manage attachment-related setup tasks routed from pillar setup-task skills
without owning CSV transport. Select the exact task family before acting:

| Attachment task family | Guidance |
| --- | --- |
| Attachment entities | [attachment-entities.md](references/attachment-entities.md) |
| Attachment categories | [attachment-categories.md](references/attachment-categories.md) |
| Attachment file formats | [attachment-file-formats.md](references/attachment-file-formats.md) |

Do not infer attachment REST endpoints or transport. Use
`shared.setup-export.task-level-export` only for export and `core.data-loader`
only for approved FSM CSV import for attachment entities and categories. Route
attachment file formats only to `shared.common.manual-tasks`.

## Preflight and Error Handling

Resolve the calling pillar skill's exact task identity, verify
`ExportImportSupportedFlag`, and preflight the selected workflow's target,
artifact, and approval requirements. For attachment entities and categories,
the task-level export workflow separately enforces
`CSVExportImportSupportedFlag` before it creates an export. For attachment file
formats, `CSVExportImportSupportedFlag=N` selects the manual-only workflow.
Classify an unsupported task as `catalog_or_metadata_mismatch` and an
unapproved import as `approval_blocker`. Redact credentials, tokens, and
sensitive setup data from diagnostics.

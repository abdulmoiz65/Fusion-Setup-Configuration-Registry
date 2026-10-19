---
task_code: "ORA_FND_SUGGESTION_GROUPS"
task_name: "Manage Applications Core Global Search Suggestion Groups"
parent_skill_id: "hcm.learning-management.learning-management-common"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Management Common"
functional_area_code: "ORA_LEARNING_MANAGEMENT_COMMON"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Applications Core Global Search Suggestion Groups

## Setup Task Metadata

- Task name: `Manage Applications Core Global Search Suggestion Groups`
- Task code: `ORA_FND_SUGGESTION_GROUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: ``

## Learning Scope and Execution Gate

Read [the Common skill](SKILL.md), its selected provider contract and the task's
compiled resource plan before using this metadata. Catalog availability and
CSV/export flags are not execution approval. Do not equate a suggestion group with a Learning search view or an assignment audience; no empty-object loader request.

The task's resource contract is incomplete; preserve the documented proposal
and resolve the gap shown by the planner before execution. No provider shortcut.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review.


## Data Loader Contract Not Resolved

The generated REST import mode has an empty businessObject. Do not call sample
download, GET, POST, PATCH or import with that empty value. Obtain a catalog-owner
confirmed task-specific provider and registered business-object contract first.
Do not infer one from the task label, change CSV flags, or substitute direct REST.

## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Applications Core Global Search Suggestion Groups` under `Learning Management Common`.

Guidance migrated from the offering setup workflow and PM FDD version 7;
source review dates and limits are retained in [taxonomy and sources](references/taxonomy-and-sources.md).
Use [Common workflow](references/workflow.md) for intake, proposal, approval and
reconciliation. This is task-specific guidance within the Common skill, not a
new nested skill or a new executor.

## Learning search-suggestion handoff

Capture the exact group, desired suggestions, Learning consumers, personas
and verified current definition. Release/build is optional context; verify
feature applicability using current authoritative capability evidence. Keep suggestion groups
separate from [global search configuration](manage-applications-core-global-search-configurations.md),
[Learning indexes](manage-search-indexes.md) and assignment audiences.

Resolve the task-specific provider and exact identifiers before an external
read or write. With no complete contract, retain the design and identify the
missing provider step. Never invent a business object from the group name or
treat CSV/export metadata as approval. Acceptance must verify the intended
suggestions for the agreed personas without changing unrelated search behavior.

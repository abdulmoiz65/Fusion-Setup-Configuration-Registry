---
task_code: "ORA_FND_GLOBAL_SEARCH_CONFIGURATIONS"
task_name: "Manage Applications Core Global Search Configurations"
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

# Manage Applications Core Global Search Configurations

## Setup Task Metadata

- Task name: `Manage Applications Core Global Search Configurations`
- Task code: `ORA_FND_GLOBAL_SEARCH_CONFIGURATIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: ``

## Learning Scope and Execution Gate

Read [the Common skill](SKILL.md), its selected provider contract and the task's
compiled resource plan before using this metadata. Catalog availability and
CSV/export flags are not execution approval. CSV is not supported; blank businessObject does not authorize REST or Data Loader; distinguish global search from HCM Tool Search Views.

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

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Applications Core Global Search Configurations` under `Learning Management Common`.

Guidance migrated from the offering setup workflow and PM FDD version 7;
source review dates and limits are retained in [taxonomy and sources](references/taxonomy-and-sources.md).
Use [Common workflow](references/workflow.md) for intake, proposal, approval and
reconciliation. This is task-specific guidance within the Common skill, not a
new nested skill or a new executor.

## Learning global-search handoff

Capture the requested global-search behavior, configuration identity,
personas and verified current configuration. Release/build is optional context,
not a required input; validate supported capabilities from current evidence. Review intended changes with the
Learning Configurations owner. Global search settings are not the Learning DFF
index configuration or HCM Tool Search Views; use
[Manage Search Indexes](manage-search-indexes.md#learning-index-readiness)
for those dependencies and [suggestion groups](manage-applications-core-global-search-suggestion-groups.md)
only when suggestions are requested.

The approved taxonomy associates this task with the Application Search
Configuration foundation. It supplies no complete task-specific execution
contract here. Preserve the requirement, baseline status, missing contract
and acceptance cases; neither the generated REST mode nor a UI navigation path
authorizes a direct REST, Data Loader or browser fallback.

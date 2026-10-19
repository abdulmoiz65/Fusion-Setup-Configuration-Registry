---
task_code: "ORA_GMS_MANAGE_AUDIT_TYPES"
task_name: "Manage Audit Types"
parent_skill_id: "hcm.learning-management.learning-management-common"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Management Common"
functional_area_code: "ORA_LEARNING_MANAGEMENT_COMMON"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Audit Types

## Setup Task Metadata

- Task name: `Manage Audit Types`
- Task code: `ORA_GMS_MANAGE_AUDIT_TYPES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Learning Scope and Execution Gate

Read [the Common skill](SKILL.md), its selected provider contract and the task's
compiled resource plan before using this metadata. Catalog availability and
CSV/export flags are not execution approval. Preserve the taxonomy entry but stop execution on the Grants/Learning mismatch; do not substitute Manage Audit Policies or create award audit types.

The task's resource contract is incomplete; preserve the documented proposal
and resolve the gap shown by the planner before execution. No provider shortcut.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Learning Management`
- Functional area / Setup Object: `Learning Management Common`
- Setup task name: `Manage Audit Types`
- Setup task code: `ORA_GMS_MANAGE_AUDIT_TYPES`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Audit Types` under `Learning Management Common`.

Guidance migrated from the offering setup workflow and PM FDD version 7;
source review dates and limits are retained in [taxonomy and sources](references/taxonomy-and-sources.md).
Use [Common workflow](references/workflow.md) for intake, proposal, approval and
reconciliation. This is task-specific guidance within the Common skill, not a
new nested skill or a new executor.

## Resolve Learning applicability before execution

The approved taxonomy includes this row, but its exact task code is
`ORA_GMS_MANAGE_AUDIT_TYPES`. Oracle's
[Grants configuration documentation](https://docs.oracle.com/en/cloud/saas/project-management/25c/oapfm/overview-of-grants-management-configuration.html)
describes Manage Audit Types for award audits, not Learning audit policy.

Ask the taxonomy owner to confirm or correct the Learning applicability and
exact task identity. Preserve the row and current catalog flags until that is
resolved; do not change the catalog here, create award audit types for Learning,
or substitute [Manage Audit Policies](manage-audit-policies.md). The incomplete
identity/provider contract blocks this task's execution, not independent setup
proposals or already-supported tasks.

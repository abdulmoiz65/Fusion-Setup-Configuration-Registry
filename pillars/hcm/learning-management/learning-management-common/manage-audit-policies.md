---
task_code: "FND_MANAGE_AUDIT_POLICIES"
task_name: "Manage Audit Policies"
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

# Manage Audit Policies

## Setup Task Metadata

- Task name: `Manage Audit Policies`
- Task code: `FND_MANAGE_AUDIT_POLICIES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Learning Scope and Execution Gate

Read [the Common skill](SKILL.md), its selected provider contract and the task's
compiled resource plan before using this metadata. Catalog availability and
CSV/export flags are not execution approval. Overall Fusion audit switch is manual-only; audit inventory is not enabled-field state; no profile REST workaround; verify current Learning audit coverage.

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
- Setup task name: `Manage Audit Policies`
- Setup task code: `FND_MANAGE_AUDIT_POLICIES`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Audit Policies` under `Learning Management Common`.

Guidance migrated from the offering setup workflow and PM FDD version 7;
source review dates and limits are retained in [taxonomy and sources](references/taxonomy-and-sources.md).
Use [Common workflow](references/workflow.md) for intake, proposal, approval and
reconciliation. This is task-specific guidance within the Common skill, not a
new nested skill or a new executor.

## Learning audit scope and evidence

Confirm the audit objective, exact Learning objects/parents/fields
and whether the request concerns overall Fusion auditing or object/field
settings. Release/build is optional; assess coverage from current provider and
implementor evidence. [Learning setup guidance](https://docs.oracle.com/en/cloud/saas/talent-management/famlc/set-up-oracle-learning.html)
describes coverage for Redwood/API-managed self-paced items, events, courses
and paths; verify the selected target's supported coverage.

Read [Audit Setup](../../../../core/fusion-api/audit-setup/SKILL.md) before its
handoff. The overall Fusion audit switch is manual-only, and available audit
field inventory does not reveal which fields are currently enabled. Request
implementor UI evidence for those controls; do not infer state or automate a
browser. Do not call profile REST to bypass the overall-switch limitation.

Supported object/field changes retain the provider's exact contract, baseline
and approval gates. The Common API/UI evidence binding remains incomplete;
retain that gap rather than claiming a complete executable graph. Verify the
approved audit scope and record the actual evidence after a supported operation.

[Manage Audit Types](manage-audit-types.md) is a separate, unresolved catalog
mapping; it must not be treated as an alias for this policy task.

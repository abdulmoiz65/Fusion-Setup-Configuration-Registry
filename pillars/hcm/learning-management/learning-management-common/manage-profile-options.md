---
task_code: "FND_MANAGE_PROFILE_OPTIONS"
task_name: "Manage Profile Options"
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

# Manage Profile Options

## Setup Task Metadata

- Task name: `Manage Profile Options`
- Task code: `FND_MANAGE_PROFILE_OPTIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Learning Scope and Execution Gate

Read [the Common skill](SKILL.md), its selected provider contract and the task's
compiled resource plan before using this metadata. Catalog availability and
CSV/export flags are not execution approval. Do not recreate a delivered definition to update a configured value; the provider parent is read-only.

Readiness here is rule-contract readiness only; environment, privileges, current
state, exact values and approval still require the selected provider's gates.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Learning Management`
- Functional area / Setup Object: `Learning Management Common`
- Setup task name: `Manage Profile Options`
- Setup task code: `FND_MANAGE_PROFILE_OPTIONS`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Profile Options` under `Learning Management Common`.

Guidance migrated from the offering setup workflow and PM FDD version 7;
source review dates and limits are retained in [taxonomy and sources](references/taxonomy-and-sources.md).
Use [Common workflow](references/workflow.md) for intake, proposal, approval and
reconciliation. This is task-specific guidance within the Common skill, not a
new nested skill or a new executor.

## Profile definitions and value handoff

The FDD's section title "Manage Profile Options Task Implementation" describes
C1, Manage Administrator Profile Values. For a business request to set up or
change Learning profile settings, use the [value task's entry paths](manage-administrator-profile-values.md#entry-paths-and-baseline-aware-questions),
with definition inspection as a prerequisite. Reserve this definition task
for definition-focused work; the broad phrase does not authorize creating a
profile definition or changing the generated task identity.

Use [Apps Common Profile Options](../../../../core/fusion-api/apps-common/profile-options/SKILL.md)
for technical validation and supported reads. Its routing key is
`manage-profile-options`; a routing key is not an FSM task code or a
Data Loader business-object name. The parent definition resource is read-only.

Capture exact `ProfileOptionName`, purpose and requested operation. The Fusion
application release/build is optional context, not a mandatory functional input.
If unknown, record it as unknown and continue the declared read workflow once
its other prerequisites pass; do not ask for a release or About screenshot just
to read fresh definitions and values. Core still owns the REST service version.
Verify the delivered definition, actual display name, permitted value
representation, enabled/updatable levels and applicable overrides. Do not assume
a WLF/ORA_WLF prefix authorizes changes to every matching option, that all
options are Boolean, or that every value belongs at Site level.

Unknown codes and ambiguous definitions need correction or an exact supported
identifier, not a fuzzy match or creation of a substitute delivered definition.
Definition availability does not prove that a configured value child exists.

For business questions, the seven-option Redwood recommendation, conditional
prerequisites, on-demand review, source conflicts, configured value changes and
readback, continue with [Manage Administrator Profile Values](manage-administrator-profile-values.md).
Keep this definition task distinct from value-child create/update and from an
effective session-value read. The provider owns identifiers and supported
operations; this task adds no direct REST endpoint or version.

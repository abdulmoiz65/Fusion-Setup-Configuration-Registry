---
task_code: "FND_MANAGE_DESCRIPTIVE_FLEXFIELDS"
task_name: "Manage Descriptive Flexfields"
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

# Manage Descriptive Flexfields

## Setup Task Metadata

- Task name: `Manage Descriptive Flexfields`
- Task code: `FND_MANAGE_DESCRIPTIVE_FLEXFIELDS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Learning Scope and Execution Gate

Read [the Common skill](SKILL.md), its selected provider contract and the task's
compiled resource plan before using this metadata. Catalog availability and
CSV/export flags are not execution approval. Establish compatible value sets before segment configuration; separate import and deployment; no search-ready claim until the requested index and ingestion are verified.

Use [DFF verification](references/dff-verification.md) for the export-preparation
and provider-artifact assessment branches. A ready rule plan is not verified pod
state or export approval. Runtime schema/evidence gaps remain explicit; no
provider shortcut and no automatic creation of missing seeded definitions.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export task setup data with `shared.setup-export.task-level-export`.
2. Validate exported or prepared task setup data with `shared.validation.setup-data-validator`.
3. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Learning Management`
- Functional area / Setup Object: `Learning Management Common`
- Setup task name: `Manage Descriptive Flexfields`
- Setup task code: `FND_MANAGE_DESCRIPTIVE_FLEXFIELDS`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Descriptive Flexfields` under `Learning Management Common`.

Guidance migrated from the offering setup workflow and PM FDD version 7;
source review dates and limits are retained in [taxonomy and sources](references/taxonomy-and-sources.md).
Use [Common workflow](references/workflow.md) for intake, proposal, approval and
reconciliation. This is task-specific guidance within the Common skill, not a
new nested skill or a new executor.

## Learning DFF design

Ask what business question the extra attribute answers, which Learning object
owns it, who enters it, and whether it must appear in details, reports, or
search. Reuse a delivered attribute when it already meets the requirement.
The Learning sources identify **descriptive** flexfields; do not infer a
Learning key or extensible flexfield from another HCM product's foundation
task list.

Select the object using the [Learning DFF reference](https://docs.oracle.com/en/cloud/saas/talent-management/famlc/descriptive-flexfields-for-oracle-learning.html):

| Exact DFF code | Intended use |
| --- | --- |
| `WLF_LEARNING_ITEM` | Learning creation/details attributes, with catalog search/filter capability where configured. |
| `WLF_LEARNING_REQUEST_DFF` | Request Details for learners, managers, and specialists. |
| `WLF_LI_COURSE` | Course details. |
| `WLF_LI_OFFERING` | Offering details. |
| `WLF_LI_SPECIALIZATION` | Learning path details; retain this technical code despite the business label. |
| `WLF_RESOURCE_DFF` | Content and instructor-led resources, including classrooms, instructors, and suppliers. |

Customer navigation: **Setup and Maintenance > Tasks > Search > Manage
Descriptive Flexfields**; use **Manage Value Sets** for associated value-set
design. Do not infer a context code, segment column, REST attribute, or
application ID from the DFF name.

### Design worksheet and checks

| Decision to capture | Guideline |
| --- | --- |
| Object, DFF, context, segment code, prompt, and purpose | Inspect existing definitions and usages; choose a global or context-specific segment only when its applicability is established. Avoid duplicate attributes. |
| Data type, length/precision, requiredness, default | Match business data and current metadata. Consider existing records, bulk loads, and integrations before making a segment required or changing its type. |
| Value-set readiness | Apply [Manage Value Sets](manage-value-sets.md#learning-value-set-design) before configuring dependent segments; capture the verified compatible set and supported values. |
| Translations, help text, ordering, and visibility | Agree who maintains the attribute and which personas need it. Page visibility does not establish data security. |
| Reporting, search/filter needs, and consuming integrations | Confirm support for the specific segment and consuming surface; adding a segment does not automatically expose it everywhere. |
| Existing-data impact and recovery | Capture the prior definition and any data-migration requirement. Do not delete populated segments or change shared value sets without an impact review and supported recovery plan. |

### Configuration, deployment, and acceptance

1. Confirm task identity and export/import eligibility with the DFF provider.
   Its configuration inspection uses task-level export, which creates a
   remote process; it is not a side-effect-free metadata GET. Use the selected
   workflow's approval and artifact requirements and the
   [data-export evidence contract](references/dff-verification.md).
2. Establish required value sets and valid values, then configure contexts and
   segments using the supported task artifact. An import must pass the DFF
   provider and Data Loader checks, including the immutable ZIP contract.
3. After successful configuration/import, use the separate DFF deployment
   workflow with exact identifiers and its execution approval. Stop on failed
   validation or deployment; record the job and diagnostics before recovery.
4. For search requirements, hand the deployed DFF/context/segment and accepted
   filter requirements to [Manage Search Indexes](manage-search-indexes.md#learning-index-readiness).
   Do not mark the DFF search-ready before the separate index, ingestion and
   Search Views checks are complete.
5. Validate with synthetic records in a nonproduction environment: correct
   object/context, valid and invalid input, required/default behavior, saved
   values, translations, and intended persona access. Verify requested search
   filters, reports, and integrations separately. Deployment success alone
   does not establish business acceptance.


The DFF provider's routing key is `manage-descriptive-flexfield`. Supply exact
DFF code, resolved task code/name, offering, functional area, sequence and
validated artifact; deployment also needs confirmed application and flexfield
identifiers. Task name, provider routing key and business-object code are not
interchangeable. Core owns endpoint versions and execution mechanics.

Search configuration, ingestion, and page extensions remain dependencies.
When their declared workflows are unavailable, report the missing capability
and next owner action instead of claiming the DFF is fully ready for use.

For a course-level “Regulatory Category” request, first check whether delivered
classification meets the need. If a DFF is justified, prepare the segment and
value-set proposal and confirm its intended search support before planning
configuration, deployment and acceptance. This is a design example, not a
prescribed delivered segment.

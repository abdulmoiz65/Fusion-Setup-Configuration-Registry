---
task_code: "FND_MANAGE_COMMON_LOOKUPS"
task_name: "Manage Common Lookups"
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

# Manage Common Lookups

## Setup Task Metadata

- Task name: `Manage Common Lookups`
- Task code: `FND_MANAGE_COMMON_LOOKUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Learning Scope and Execution Gate

Read [the Common skill](SKILL.md), its selected provider contract and the task's
compiled resource plan before using this metadata. Catalog availability and
CSV/export flags are not execution approval. Preserve seed restrictions, stable in-use codes and distinct business actions; required review does not require new codes.

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
- Setup task name: `Manage Common Lookups`
- Setup task code: `FND_MANAGE_COMMON_LOOKUPS`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Common Lookups` under `Learning Management Common`.

Guidance migrated from the offering setup workflow and PM FDD version 7;
source review dates and limits are retained in [taxonomy and sources](references/taxonomy-and-sources.md).
Use [Common workflow](references/workflow.md) for intake, proposal, approval and
reconciliation. This is task-specific guidance within the Common skill, not a
new nested skill or a new executor.

## Lookups: Agree the Business Vocabulary

Customer navigation: **Setup and Maintenance > Tasks > Search > Manage Common
Lookups**. Begin with the [documented extensible lookup types](https://docs.oracle.com/en/cloud/saas/talent-management/famlc/extensible-lookups-for-oracle-learning.html)
and review only those used by the selected Learning processes.

Use the [lookup review buckets](#lookup-review-buckets)
from the PM workbook. Required review means confirm that the applicable process
has suitable governed choices; it does not mandate adding codes. Optional review
means retain suitable existing choices unless a business gap is identified.
Neither bucket establishes the current tenant configuration.

### From review guidance to value proposals

The PM workbook is a lookup-type review inventory, not a list of tenant lookup
values to load. Its `Lookup name` describes the type; it is not a proposed
lookup-code meaning. Its examples are possible business reasons, not approved
code/meaning pairs. Do not turn its 30 type rows into 30 create operations.

For a broad request, identify relevant catalog, assignment and recommendation
processes, read existing choices through the selected workflow, and ask for
gaps only. For a partial value list, retain valid supplied rows and ask for
missing type, code, meaning or business action. For a complete value list,
validate and reconcile it without repeating answered questions. A suitable
existing value can satisfy required review without any new value.

Ask which delivered choices already fit, what business distinction is missing,
who owns the vocabulary, and which languages and effective dates are needed.
For each proposed value record lookup type, stable code, meaning, description,
enabled state, dates, and translation requirements. Use concise meanings for
users and descriptions for administrator context.

Apply these design and validation guidelines:

- Read existing codes first. Reuse an appropriate value; do not create a
  synonym merely because the customer uses different wording. Do not assume
  the provider supports a mutation because a lookup is readable.
- Check configuration level and delivered-code restrictions before changing
  existing values. Adding customer choices to an extensible lookup does not
  imply unrestricted editing or deletion of Oracle seed data.
- Preserve stable codes used by integrations and historical records. Prefer
  a supported end date or disable action to deleting an in-use customer code,
  after reviewing its impact on consumers.
- Keep learner withdrawal and specialist withdrawal, assignment attribution
  and recommendation attribution, and different activity completion reasons
  separate. Confirm the field and business action before selecting its type.
- Route through Common lookups for the documented Learning task; any different
  category needs provider confirmation. "Extensible lookup" describes
  configuration behavior; it does not mean an extensible flexfield or prove
  that the generic/extended lookup endpoint is appropriate.
- Test the relevant catalog, assignment, or recommendation page, including
  translations and dates. A new lookup value alone does not establish a new
  workflow, alert template, pricing behavior, or supported learning format.

### Published action distinctions

The [Oracle lookup reference](https://docs.oracle.com/en/cloud/saas/talent-management/famlc/extensible-lookups-for-oracle-learning.html),
rechecked 2026-09-22, refines selection within the review buckets:

- `ORA_WLF_BUSINESS_DRIVER` classifies self-paced learning;
  `ORA_WLF_ELEARNING_TYPE` covers formats across self-paced learning, events,
  courses and learning paths. `ORA_WLF_PRICING_TYPE` applies to offering pricing.
- `ORA_WLF_DL_REACTIVE_REASON` is for content reactivation. Keep content
  deletion, learning deletion and learning inactivation/event cancellation
  distinct rather than treating them as one lifecycle action.
- `ORA_WLF_COMPLT_RSN_ONLINE_SP` documents completion, not exemption.
  `ORA_WLF_COMPLT_RSN_ONLINE_IL` includes virtual instructor-led exemptions.
  `ORA_WLF_COMPLT_RSN_EVENT` and `ORA_WLF_COMPLT_RSN_ONSITE_IL` also cover no-show.
  Do not infer identical actions from similar completion-reason names.

These are business-action mappings, not new lookup codes or permission to
perform the underlying actions. Required/optional review remains a PM-workbook
classification, not an Oracle-mandated configuration level.

## Lookup review buckets

`oracle-learning-extensible-lookups-guidance.xlsx` (attachment 21940378739),
`Lookup guidance` rows 7–36, defines 30 types: 22 required-review and 8
optional-review types. These counts describe this attachment version only.
Derive each run's counts from applicable validated rows.

### Required review when the process is in scope

| Business process / source rows | Exact lookup types | Question that changes the proposal |
| --- | --- | --- |
| Lifecycle, 11–14 | `ORA_WLF_DL_CONT_DEL_REASON`, `ORA_WLF_DL_DELETE_REASON`, `ORA_WLF_DL_INACTIVE_REASON`, `ORA_WLF_DL_REACTIVE_REASON` | Do existing reasons cover content deletion, learning deletion, inactivation/cancellation and reactivation under the customer's policy? |
| Communications, 16 | `ORA_WLF_NOTIF_PATTERN` | Which approved notification patterns are needed, and who owns each template/trigger? A code does not configure an alert. |
| Event/request administration, 18–21 | `ORA_WLF_ASSN_ALLOCATE_SEAT_RSN`, `ORA_WLF_ASSN_UPDATE_RSN`, `ORA_WLF_ASSN_WAITLIST_RSN`, `ORA_WLF_ASSN_WAIVE_PREREQS_RSN` | Which seat, approval/rejection, waitlist and prerequisite-exception reasons need governance? |
| Corrections, 22–23 | `ORA_WLF_ASSN_UNDO_RSN`, `ORA_WLF_ASSN_UNDO_COMPLETE_RSN` | How must reversal of bypass and reversal of completion be distinguished for audit? |
| Activity outcomes, 24–30 | `ORA_WLF_COMPLT_RSN_EVAL`, `ORA_WLF_COMPLT_RSN_EVENT`, `ORA_WLF_COMPLT_RSN_OFFLINE_SP`, `ORA_WLF_COMPLT_RSN_ONLINE_IL`, `ORA_WLF_COMPLT_RSN_ONLINE_SP`, `ORA_WLF_COMPLT_RSN_ONSITE_IL`, `ORA_WLF_COMPLT_RSN_SELF_PACED` | Which activity types are used, and what completion/exception evidence does each require? Do not collapse these into one lookup. |
| Assignment outcomes, 31–32 | `ORA_WLF_COMPLT_RSN_SPEC`, `ORA_WLF_REC_DELETE_RSN_SPEC` | Are assignment completion/exemption and deletion reasons sufficient for policy and reporting? |
| Withdrawals, 33–34 | `ORA_WLF_WITHD_RSN_SS`, `ORA_WLF_WITHD_RSN_SPEC` | Which learner-facing versus specialist reasons are needed? Preserve their distinct audiences. |

Review does not require creation. Read the delivered and customer codes,
confirm suitability, and propose additions only for an agreed gap. The PM
examples (such as duplicate content or manager escalation) are suggestions,
not seeded codes or customer-approved additions.

### Optional review for an identified business gap

| Business process / source rows | Exact lookup types | Review only when |
| --- | --- | --- |
| Catalog taxonomy/pricing, 7–10 | `ORA_WLF_BUSINESS_DRIVER`, `ORA_WLF_ELEARNING_TYPE`, `ORA_WLF_LEARNING_LEVEL`, `ORA_WLF_PRICING_TYPE` | Existing classifications do not support the agreed strategy, delivery format, proficiency framework or pricing/reporting need. |
| Incident classification, 15 | `ORA_WLF_LEARN_INCIDENT_TYPE` | A defined incident-triage policy needs additional distinctions. |
| Assignment attribution, 17 | `ORA_WLF_ASSIGN_ATTR_LOOKUP` | Existing organizational sources do not describe the assignment model. |
| Recommendation attribution/category, 35–36 | `ORA_WLF_RECOM_ATTR_LOOKUP`, `ORA_WLF_RECOM_CATEGORY` | A governed recommendation use case needs an additional source/category. |

Avoid synonyms and personal names as organizational attribution values.
Record the customer's vocabulary owner, stable code, meaning, language,
effective dates, consumer impact and source. Preserve seeded restrictions.
Inspect configuration level and the selected provider's mutation support.
Do not attempt a prohibited change by switching lookup categories.

## Source-count conflict

The workbook's Review summary reports 27 required / 3 optional types, but its
30 detailed rows classify 22 / 8. Use the per-type classifications above and
derive each run's counts after applicability checks; do not copy summary totals.

### Source-content conflicts

The `Lookup guidance` sheet, row 12, describes `ORA_WLF_DL_DELETE_REASON` using
"learning record" wording. The current Oracle reference distinguishes learning
deletion from assignment deletion (`ORA_WLF_REC_DELETE_RSN_SPEC`, row 32).
Ask which object/action is intended; never choose the deletion type from that
ambiguous phrase alone. Row 27 describes `ORA_WLF_COMPLT_RSN_ONLINE_IL` only as
completion, while current product guidance also includes exemption. Use the
published action mapping and target-supported choices, keeping the discrepancy
visible in the affected proposal's source basis.

## Completion evidence

Reconcile each approved value by its exact type/code and applicable language or
set context. Distinguish existing matching values from supported creates and
updates; report unresolved keys separately, not as known zero changes. Apply
the [Common summary and readback rules](references/workflow.md#implementer-facing-validation-and-confirmation).
Confirm the selected business action shows the approved meanings, translations,
dates and enabled state. Existing integrations and historical codes must remain
valid. New lookup values do not create a workflow or alert configuration.

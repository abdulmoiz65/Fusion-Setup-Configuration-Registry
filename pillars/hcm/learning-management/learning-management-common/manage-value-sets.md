---
task_code: "FND_MANAGE_VALUE_SETS"
task_name: "Manage Value Sets"
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

# Manage Value Sets

## Setup Task Metadata

- Task name: `Manage Value Sets`
- Task code: `FND_MANAGE_VALUE_SETS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Learning Scope and Execution Gate

Read [the Common skill](SKILL.md), its selected provider contract and the task's
compiled resource plan before using this metadata. Catalog availability and
CSV/export flags are not execution approval. Reuse a compatible governed definition; no root value-set create/update through the child-value provider; inspect all consumers before changing shared values.

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
- Setup task name: `Manage Value Sets`
- Setup task code: `FND_MANAGE_VALUE_SETS`




## Usage

Use this metadata file when planning, sequencing, exporting, importing, or validating setup data for `Manage Value Sets` under `Learning Management Common`.

Guidance migrated from the offering setup workflow and PM FDD version 7;
source review dates and limits are retained in [taxonomy and sources](references/taxonomy-and-sources.md).
Use [Common workflow](references/workflow.md) for intake, proposal, approval and
reconciliation. This is task-specific guidance within the Common skill, not a
new nested skill or a new executor.

## Learning value-set design

Use Oracle's [Manage Values (26C)](https://docs.oracle.com/en/cloud/saas/applications-common/26c/oaext/manage-values.html)
and [Overview of Value Sets](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/overview-of-value-sets.html),
reviewed 2026-09-22. These describe product behavior and UI tasks, not a new
REST definition-creation capability or execution approval.

Use **Setup and Maintenance > Tasks > Search > Manage Value Sets** for design
context, and the [Apps Common Value Sets provider](../../../../core/fusion-api/apps-common/value-sets/SKILL.md)
for its supported operations (routing key `manage-value-sets`).
Establish what business question the additional Learning attribute answers,
which object/segment consumes it and whether a delivered attribute already fits.

| Decision | Required design/evidence |
| --- | --- |
| Exact value-set code, validation type and consuming segment | Reuse a compatible governed set. The provider resolves actual returned identifiers; do not derive IDs from names or invent a Learning default set. |
| Data type, length/precision, requiredness and default | Match segment requirements and current metadata; consider existing records, loads and integrations before type or requiredness changes. |
| Dependent or table-validated set | Inspect the actual dependencies and supported values; do not assume all value sets behave like independent lists. |
| Shared consumers and maintenance owner | Identify DFFs/integrations using the set, vocabulary ownership, translations and effective dates where applicable. |
| Change impact and recovery | Capture current definitions/values and migration needs; do not delete in-use values or alter shared validation without review and a supported recovery plan. |

Ask only for unresolved segment requirements. Identify needed value sets from
the selected Learning attributes and existing usages; these documents do not
provide a universal list of Learning value-set codes to create. For each
selected set, show its resolved code/name, purpose, current validation and
value evidence, proposed action and missing decisions using the
[Common proposal rules](references/workflow.md#implementer-facing-validation-and-confirmation).
Unread state is Not validated, not an empty set.

### Choose validation to match the segment

The [validation-type guidance](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/validation-type-options-for-value-sets.html)
distinguishes these designs:

| Validation type | Design decision |
| --- | --- |
| Format only | Free entry constrained by format/length/range, without an LOV to populate. |
| Independent | A maintained list of permitted choices. |
| Dependent | Choices depend on an independent segment in the same flexfield; resolve its set and selected parent value first. |
| Subset | Select from an existing independent set; unlike dependent validation, another segment need not be selected first. |
| Table | Choices come from an application table; do not manufacture child-value rows for that list. |

A dependent set cannot use another dependent set as its parent. For numeric
data, precision limits total digits and scale limits fractional digits.
Global and context-sensitive segments require a value set; a context segment
can instead use its configured context values. When assigning a set to a context
segment, verify the documented independent/table and character-length constraints.
Do not import Accounting Key Flexfield-specific restrictions into Learning DFFs.

Capture intended translations before definition design: the Translatable choice
cannot be switched later. For table validation, resolve actual metadata through
the provider; this guidance supplies no SQL, table names or write-to-table route.

### Protection, shared usage and security

The [overview](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/overview-of-value-sets.html)
prohibits changing/deleting protected sets or adding, editing or deleting their
values. Protected sets may still be referenced. Check protection before proposing
any mutation; if evidence is missing, resolve it through the declared workflow
instead of assuming editability or trying another route.

Value-set security applies through flexfield usage, covers independent,
dependent and table validation, and affects every usage of a secured set.
It does not control visibility of previously stored DFF data when queried.
Keep data-access requirements with the appropriate security workflow; do not
present value filtering as complete Learning data security or assign roles here.

Use the [usage guidance](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/how-flexfields-and-value-sets-work-together.html)
to identify all consumers, including those outside Learning, before approving
a shared change. Reuse only when the validation and business meaning fit each
consumer. A readable or reusable set is not necessarily mutable.

### Manage Values and execution boundaries

Oracle's [Manage Values procedure](https://docs.oracle.com/en/cloud/saas/applications-common/26c/oaext/manage-values.html)
supports maintaining lists and display order for independent, dependent and
subset sets. For an implementer using an approved manual workflow:

1. Open Manage Value Sets in Setup and Maintenance, search for the exact set,
   and select Manage Values.
2. Create the approved values, or select the specifically approved value for
   deletion after the protection and consumer-impact checks.
3. Save and Close, then verify the saved values and their intended behavior.

These are reference instructions for the implementer, not authorization for
agent-driven browser actions or a fallback from an unavailable provider.
The existence of a UI Create/Delete action does not establish API support.
Display-order changes likewise require a verified supported field/operation.
Do not infer deletion from a value omitted in an input file or proposal.

The shared value-set provider reads definitions and maintains supported child
values. It does not currently create or alter root value-set definitions.
If a new definition is required, document the design and resolve a supported
setup route before dependent DFF execution; do not manufacture a REST route.

Read current values through the selected provider before proposing child-value
changes. Validate duplicates, dates, translations and exact provider keys as
applicable. A readable definition does not authorize root or child mutations.
Catalog FSM support is not permission to bypass an unsupported provider contract.

### Deployment and acceptance

Follow [testing and maintenance guidance](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/validation-type-options-for-value-sets.html):
value sets aren't managed in Fusion configuration sandboxes. This is distinct
from using a nonproduction environment for testing. Inspect every affected
flexfield's deployment status after a set change; redeploy affected flexfields
marked Edited through their authorized workflows before claiming readiness.
Keep these deployments separate from child-value persistence/readback.

Only after the required set and values are established should
[Manage Descriptive Flexfields](manage-descriptive-flexfields.md#learning-dff-design)
configure a dependent segment. Validate accepted/rejected values and saved
data with synthetic examples, including affected existing consumers; creating
one value alone does not prove DFF deployment or search readiness.

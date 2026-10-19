---
skill_id: "hcm.workforce-absence-management.absence.absence-categories"
name: "Absence Categories Setup Task Guidance"
description: "Provides task-specific setup guidance for Absence Categories under the Absence functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Absence Management"
functional_area: "Absence"
functional_area_code: "ORA_ABSENCE"
task_code: "ORA_ANC_MANAGE_ABSENCE_CATEGORIES"
task_name: "Absence Categories"
parent_skill_id: "hcm.workforce-absence-management.absence"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "absenceCategories"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM workforce absence management pillar team"
version: "1.0.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
persists_project_state: true
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
state_updates:
  - "setup_task_sequence"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absence/absence-categories/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absence/absence-categories/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects: []
required_privileges: []
---

# Absence Categories Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Absence Categories` under `Absence`.

## Setup Task Skill Contract

- task_code: `ORA_ANC_MANAGE_ABSENCE_CATEGORIES`
- task_name: `Absence Categories`
- parent_skill_id: `hcm.workforce-absence-management.absence`
- pillar: `HCM`
- offering: `Workforce Absence Management`
- functional_area: `Absence`
- functional_area_code: `ORA_ABSENCE`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `absenceCategories`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `absenceCategories` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "absenceCategories" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Absence Categories` under `Absence`.

## Setup Task Metadata

- Task name: `Absence Categories`
- Task code: `ORA_ANC_MANAGE_ABSENCE_CATEGORIES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `absenceCategories`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Workforce Absence Management`
- Functional area / Setup Object: `Absence`
- Setup task name: `Absence Categories`
- Setup task code: `ORA_ANC_MANAGE_ABSENCE_CATEGORIES`

## Date-Effective Data Loader Contract

The registered `absenceCategories` UCM DAT template exposes `effectiveOf` on
the parent, both flexfield sections, and `absenceCategoryTypes`. Refresh that
template before every date-effective source; do not infer DAT columns from REST
`/describe` metadata or a reduced sample.

- Keep `EffectiveStartDate` for a create when live parent metadata marks it
  mandatory. `effectiveOf` selects the date-effective range and does not
  replace the DAT field.
- Derive `effectiveOf` from each row's operation. Never accept a caller
  authored range string. Existing DDF/DFF rows participating in the parent's
  update use its derived value; a new association uses the create mapping,
  not the parent's UPDATE or CORRECTION mode. Do not add an empty child row
  solely to carry a range value.
- Require one exact selected effective-dated category identity for every non-create
  operation. Route all mutations only through `core.data-loader` and its
  immutable preview and approval lifecycle.
- Support correction and update of both `AbsenceCategoriesDDFFlex` and
  `AbsenceCategoriesFlex` using their registered `AbsenceCategoryId`. The BO
  registration uses that same surrogate and parent ID on
  `ANC_ABSENCE_CATEGORIES_F`; it does not require a separate flex identifier.
  Resolve the existing child and preserve both effective date fields. A
  returned composite REST key is lookup evidence, not a value to put in
  `AbsenceCategoryId` and not a reason to prohibit maintenance.

The operation mapping and validation requirements are in
`ora-resource/ora_defaulting_rules.md` and
`ora-resource/ora_input_validation.md`.

For every date-effective source, derive Task Hook evidence from the final
immutable DAT member that Data Loader will upload. A caller-provided
rule-result record is not evidence that `effectiveOf` was serialized. Block the
preview when any included parent, `AbsenceCategoriesDDFFlex`,
`AbsenceCategoriesFlex`, or `absenceCategoryTypes` `METADATA` header or `MERGE`
row omits the derived `effectiveOf` value.

### Add an association to an existing category

Resolve the category and association history before preparation. Treat a new
association as a child create, even when the user calls the overall request a
category update. Apply the row-operation mapping in `ora_defaulting_rules.md`
and key validation in `ora_input_validation.md`. Do not patch an existing
association to add a different type. When no parent business change remains,
prepare only the new association under the registered absenceCategories root;
do not repeat a parent update that already succeeded in a partial load.

An association's registered parent ID is `AbsenceCategoryId`; its own generated
ID is `AbsenceTypeCateId`. A blank diagnostic User Key is not evidence that
the parent ID was omitted. Follow the association failure guidance in
`ora_error_handling.md` before a newly approved retry.

### DDF and DFF maintenance

Use `AC.RESOLVE_FLEX_ROW` and its resolver before preparation. Keep the existing
child's ID/start/end values separate from the requested effective date. Both
flex registrations include `AbsenceCategoryId`, `EffectiveStartDate` and
`EffectiveEndDate`; do not discard the resolved end date under the ordinary
create-default omission rule. Preserve the real returned end date without
substituting a sentinel or describing it as a new end-date request.

For an update, prepare the parent PATCH first to establish the requested dated
slice, preserving unchanged parent business values. Follow it with only the
requested flex section(s), using the same registered ID, planned slice start,
observed slice end and derived UPDATE `effectiveOf`. For a correction, retain
the selected existing slice's start/end and use CORRECTION `effectiveOf`;
include a parent PATCH only if parent fields also change. A request to correct
the original effective date selects the original slice rather than today's
slice. Follow the operation mapping in `ora-resource/ora_defaulting_rules.md`.

Use `MERGE` DAT records with `RestAction=PATCH`. A blank segment on an existing
child is still a PATCH. Include changed segments and required identity/context
only, so unrelated segments are not cleared. Keep all preparation and mutation
in `core.data-loader`; empty registration `PostUrl`/`PatchUrl` values do not
authorize a fabricated override URL. Show the category, current/proposed values,
correction or update, effective date, and retained end date in the creation
summary before the immutable Data Loader approval.

The complete date-key source corrects the prior omission of child
`EffectiveEndDate`; end-to-end success must still be verified from the actual
load and effective-dated readback. When the user requests continued validation,
follow the core status workflow, then read the changed child and the preceding
date for an update (or selected historical slice for a correction). A parent
success with a child failure is a partial failure, not a completed flex change.

## Read-Only Category Resolution and Change Intent

For every non-create request, use the read-only
`find_absence_category_by_exact_name` resolver in
`ora-resource/ora_reference_lookups.md` through
`core.fusion-api.rest-api-client`. Search using the exact category name and,
when supplied, legislation. Match in the selected effective-date context and
resolve one category only. If the user supplies today's name for a historical
correction, resolve the current identity first, then query the historical slice
by its registered ID and selected correction date. Use that slice's returned
name and range. Retain only the identity and values needed for preparation.
A zero-match, multiple-match, ineffective or legislation-mismatched result
needs resolution; a historical slice is not rejected merely because it ended
before today. Never choose a row arbitrarily.

When a requester asks to remove a category but does not state the operation,
ask whether they mean **End date**, **Delete changes**, or **ZAP**. Recommend
end-dating when the intent is to stop future use while preserving history. Do
not infer `DELETE_CHANGES` or `ZAP` from the word “delete”; ZAP additionally
requires explicit destructive intent. An end date must be an explicit supplied
date (including an explicit request for “today”).

After the identity and operation resolve, derive the matching `effectiveOf`,
prepare and validate the immutable Data Loader artifact, present the resolved
target and operation in the preview, and require the normal Data Loader
approval immediately before upload or initiation. The read-only lookup never
authorizes a direct REST mutation.

## Browse, Detail, and History

For a request to view Absence Categories, use the read-only
`find_absence_categories` resolver. When no filter is supplied, use the current
system date and active status as the view context. Support optional category
name, effective date, status, and legislation filters; apply the exact filters
locally after reading every returned page. Show Name, Effective Start Date,
Effective End Date, Status, and Legislation for every returned category.
Render this view as a five-column Markdown table in that exact order. Preserve
an empty Effective End Date as `—` and retain a returned date exactly as
supplied. Do not label a date as "open-ended" or otherwise derive business
meaning from it. Never omit an empty table cell or shift Status into the
Effective End Date column.

For a selected category, use the exact-name resolver to establish its current
identity. To show its associated types or effective-dated history, route the
read-only configuration baseline through `shared.setup-export.task-level-export`
for task `ORA_ANC_MANAGE_ABSENCE_CATEGORIES`; do not infer associations from a
category name alone. Display the associated type Name, Pattern, Status,
Legislation, and effective dates from the export or current type lookup.
Display a Management value only when the refreshed Absence Types metadata
exposes one; otherwise state that it is unavailable rather than inventing it.
For the selected category, also show Description when present and only the
applicable legislative and descriptive flexfields confirmed by current
`absenceCategories/describe` metadata.

## Policy Grouping and Reporting Guardrails

When asked to design category taxonomy, collect or explicitly mark unresolved:
policy scope, leave inventory, jurisdiction, reporting purpose, separation
rules, and effective date. Produce a policy-to-category proposal that names
the proposed categories, associated types, grouping rationale, unresolved
decisions, and the decision owner. Do not infer statutory, pay, eligibility,
or reporting rules.

Use the requester-supplied policy to explain whether types should be combined
or separated. When supplied policy confirms different statutory reporting by
legislation, recommend legislation-specific categories. Warn when a proposed
broad category would combine types with distinct statutory, pay, eligibility,
or compliance outcomes. Categories never substitute for eligibility,
entitlement, accrual, pay, approval, or plan-balance design; route those
requirements to their owning Absence setup task.

For a create, retain an employee-safe supplied description in the category and
store technical rationale, policy citations, reporting mapping, and unresolved
decisions only in the project policy-to-category summary. Before a maintenance
preview, show field-level and association-level current-versus-proposed impact.
After validation or execution, return the category identity, effective date,
associated types, outcome, and unresolved decisions; persist the summary and
test-evidence checklist in the project workspace. Mutations still require the
separate immutable Data Loader confirmation.

## Guided Creation, Association, and Maintenance

Build the normalized category source from confirmed attributes and current
metadata, not from UI tabs or a hand-built REST mutation. Require Name, Status,
and Effective Start Date. If the consultant asks to use the system date,
present that date and obtain explicit confirmation before using it; otherwise
do not default the date. Default Status to Pending only when current lookup
metadata supports it and the consultant explicitly confirms that choice.

For each requested association, resolve the available Absence Type in the
selected legislation and effective-date context through the Absence Types
workflow. Present its observed Name, Pattern, Status, Management, Legislation,
and effective dates. Require the association Type, Status, and Effective Start
Date. Require both the category and type to be effective on the association
start date; a later association start is allowed within their effective ranges.
Block an association that is inaccessible, inactive on that date,
legislation-incompatible, outside either effective range, duplicated, or
has unresolved governing configuration. Confirm duplicate checks and
association history from the category task export before preparation; do not
rely on a name-only assumption.

For update, correction, future-dated change, end date, delete-changes, ZAP, or
association maintenance, resolve the exact effective-dated category row and
retrieve the available category and association history. Explain that a
correction amends the selected historical row while a future-dated change
creates a later context. Before the Data Loader preview, show changed fields,
added/removed/changed associations, active-associated-type and reporting
impact, and any Fusion-reported deletion dependency. For delete actions, do not
submit unless Fusion permits the exact action and the consultant explicitly
confirms the current immutable preview.




## Required Portable Source Preparation and Verification

For REST Data Loader source preparation, read
[Portable Source Preparation](../references/portable-source-preparation.md)
and use `pillars/hcm/workforce-absence-management/absence/scripts/prepare_absence_source.py`.
Supply current registered metadata and resolved business decisions; do not
create ad hoc project or temporary generators. Verify the exact final DAT or
ZIP with `--verify` and `--model` before the existing Data Loader preview.
This local check does not replace task rules, live lookups, target-key collision
checks, immutable approval, submission, or post-load verification.

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.workforce-absence-management.absence` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

When interacting with a requester, identify inputs, missing values, and validation errors by their business-facing labels rather than raw Data Loader or REST attribute names. For example, say `Category Effective Start Date`, `Associated Absence Type`, and `Associated Type Effective Start Date`, not `EffectiveStartDate`, `AbsenceTypeId`, and `absenceCategoryTypes.EffectiveStartDate`. Keep raw attribute names only in technical artifacts, loader-source previews, or when the requester explicitly asks for them.

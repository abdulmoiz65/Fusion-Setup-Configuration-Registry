---
skill_id: "hcm.workforce-absence-management.absence.absence-plans"
name: "Absence Plans Setup Task Guidance"
description: "Provides task-specific setup guidance for Absence Plans under the Absence functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Absence Management"
functional_area: "Absence"
functional_area_code: "ORA_ABSENCE"
task_code: "ORA_ANC_MANAGE_ABSENCE_PLANS"
task_name: "Absence Plans"
parent_skill_id: "hcm.workforce-absence-management.absence"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "absencePlans"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absence/absence-plans/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absence/absence-plans/current/"
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

# Absence Plans Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Absence Plans` under `Absence`.

## Setup Task Skill Contract

- task_code: `ORA_ANC_MANAGE_ABSENCE_PLANS`
- task_name: `Absence Plans`
- parent_skill_id: `hcm.workforce-absence-management.absence`
- pillar: `HCM`
- offering: `Workforce Absence Management`
- functional_area: `Absence`
- functional_area_code: `ORA_ABSENCE`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `absencePlans`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `absencePlans` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "absencePlans" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Absence Plans` under `Absence`.

## Setup Task Metadata

- Task name: `Absence Plans`
- Task code: `ORA_ANC_MANAGE_ABSENCE_PLANS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `absencePlans`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` in `REST` mode using `absencePlans`.

Use this task metadata when invoking those skills:

- Offering: `Workforce Absence Management`
- Functional area / Setup Object: `Absence`
- Setup task name: `Absence Plans`
- Setup task code: `ORA_ANC_MANAGE_ABSENCE_PLANS`




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

For a create request that omits both `EffectiveStartDate` and `RangeStartDate`, propose the current system date as the business effective start date and require explicit user confirmation before using it in `YYYY-MM-DD` format. Preserve any requester-supplied date, require explicit date inputs for date-scoped non-create operations, derive the matching `effectiveOf` value, and never emit physical `EffectiveStartDate` in a Data Loader section. ZAP instead requires explicit complete-deletion scope for the selected logical target and a freshly validated dated identity at the recorded lookup as-of date; its loader mapping has no range date.

When interacting with a requester, identify inputs, missing values, and validation errors by their business-facing labels rather than raw Data Loader or REST attribute names. For example, say `Calendar Start Month` and `Calendar Start Day`, not `CalendarStartMonth` and `CalendarStartDay`. Keep raw attribute names only in technical artifacts, loader-source previews, or when the requester explicitly asks for them.

When a requester says `repeating`, `repeating monthly`, or names a `Monthly*`
period, treat this as a request for **Balance Frequency Source = Repeating
period**, not Person primary frequency. Before DAT preparation, resolve one
existing Repeating Period through
`resolve_absence_plan_repeating_period`: an exact supplied name must match once;
a generic `Monthly*` search may proceed only when it yields one candidate, and
otherwise requires the requester to select a candidate. Resolve and retain the
current target's source code and relationship field only after current
contract validation. Do not create a repeating period automatically, do not use
a calendar plan-term anchor or payroll frequency as a substitute, and never
allow a captured default to choose either Balance Frequency Source or Repeating
Period. A calendar-year plan term and its January 1 anchor remain separate from
the frequency of accrual postings.

## Read-Only Plan Search

For AC1 list/view and multi-filter searches, access **Absence Plans** in the
Absences work area. The work area defaults to the current effective date and
Active status. Use its Plan, Effective Date, Status, Plan Type, Legislation,
and Legislative Data Group controls, and display Plan, Effective Start Date,
Effective End Date, Status, Plan Type, Legislation, LDG, and Management.
This UI search route is read-only: it is not an LOV-resolution source and it
does not enter DAT preparation or a mutation approval flow. Do not substitute
client-side filtering after an unfiltered REST result for an AC1 filter.

Use the documented `absencePlansLOV` collection for legacy name discovery. An
exact-name lookup resolves one row only after matching the supplied (or
defaulted) legislation and lookup as-of date. A keyword lookup performs a
case-insensitive contained-name match and returns every qualifying row; it
never selects one arbitrarily. When either value is omitted for a lookup only,
default legislation to `US` and the as-of date to the current system date.
These lookup defaults never provide a business effective date for a mutation:
an update, correction, end-date, or delete-changes operation still requires its
explicit operation-specific date and final primary-key validation. ZAP instead
requires explicit complete-deletion scope for the selected logical target and
final primary-key validation at the recorded lookup as-of date; this does not
create a range date for ZAP.

## Read-Only Plan History

For AC9, resolve one existing plan first, then use
`retrieve_absence_plan_effective_history` from `ora_reference_lookups.md`.
Traverse the complete logical plan through its returned effective-date
boundaries and retrieve the full parent record, including supported children,
for every physical slice. Compare those complete slices to derive the changed
configuration context.

Return only a newest-first history table with these four columns in this exact
order: `Effective Period`, `Changes`, `Last Updated Date`, and `Last Updated
By`. For a bounded row, format `Effective Period` as start date - end date. If
the returned end date is Fusion's high date `4712-12-31`, display only the
start date; do not add `open-ended` or another assumed label. Use
application-provided changed-attribute labels when available; otherwise derive
business-facing labels by comparing adjacent complete slices. Leave `Changes`
blank when the response and comparison provide no change evidence, including
the earliest slice; never invent `Initial record`.

Do not display the full record payload, ordinary current-plan details, child
payloads, status, available actions, pagination metadata, identifiers, links,
or other technical response data. `Last Updated Date` and `Last Updated By`
are the only who-column values included because they are part of the requested
history summary. Use the Fusion History presentation for its
application-provided change labels and `Last Updated Date` when that
presentation is available. Use the supported REST slice contract for
complete-record comparison and `LastUpdatedBy`; the standard REST response does
not guarantee `LastUpdateDate`. Leave any unavailable cell blank and disclose
the source limitation outside the table; never invent a timestamp or attribute
label. Retain plan type, legislation, LDG, and each slice's composite
dated identity internally so that a row selected for later correction or
update can be revalidated through `find_absence_plan_by_primary_key`. A history
request is read-only and does not enter DAT preparation or mutation approval.

## LOV Name Resolution

Treat every Absence Plans LOV value supplied by the requester as its selected
display name, not as a technical identifier. Resolve that exact name through
the current target Fusion REST environment with the field-specific resolver in
`ora-resource/ora_reference_lookups.md`. Require exactly one current,
effective, controller-compatible result. Preserve the selected and matched name
in the plain-language preview, but write only the returned code or numeric ID
to the compact DAT.

This applies to the documented common lookup fields; Conversion Formula;
field-specific enrollment, accrual, elective-disbursement,
discretionary-disbursement, donation, and rate formulas; all four Rate
Definition targets; Element; Alternative Schedule Category; Event; Event
Action; Eligibility Profile; Legislative Data Group; legislation; Repeating
Period; and flexfield contexts and segments. A
name supplied for one field must not be reused for another field unless the
request explicitly selects the same name there and that field resolves it
independently. When a controller such as legislation, LDG, Rate Rule, plan type,
or flex context changes, discard dependent results and resolve the retained
names again.

For now, do not interpret a supplied value as an LOV description. Description-
based matching is reserved for a later UI contract. If a description is
supplied instead of the selected name, stop and request the name; do not use
contains, fuzzy matching, or a first result. A formula name may exist in
normalized request state only until resolution. Do not emit any read-only
`FormulaName`, `Meaning`, or other display attribute in the DAT.

## 27A Condition Builder Exclusion

When an administrator is creating an Absence Plan in release 27A, do not offer,
invoke, route to, or emulate a Condition Builder skill. If the request depends
on Condition Builder, identify that capability as unavailable in 27A and keep
the plan blocked until the requester supplies a supported policy design. Do not
replace it silently with a formula, eligibility profile, derived factor, or
another configuration object.

## Durable Policy Traceability

For AC10, persist a sanitized policy-to-configuration summary in the selected
implementation project before creation approval. The durable artifact must
identify the policy source, plan name and type, legislation, LDG, effective
date, status, included and excluded populations, supplied or confirmed policy
decisions and their configuration mappings, separately routed dependencies,
unresolved decisions, omitted optional settings, validation evidence, and the
current outcome. Record its artifact reference in the skill-run and validation
records. If the artifact cannot be written, stop without claiming readiness.
Preserve it for prepared, submitted, pending, failed, and verified-success
outcomes; never persist credentials, session material, opaque internal URLs,
or protected payloads.

## Data Loader REST Execution Boundary

Route every Absence Plans mutation exclusively through `core.data-loader` in `REST` mode with the registered business object `absencePlans`.

- Do not invoke `core.fusion-api.rest-api-client` for `POST`, `PATCH`, or `DELETE` operations on Absence Plans.
  Read-only list/filter access uses the work-area route above; it does not
  authorize a REST POST search action or any direct REST mutation.
- Use `core.data-loader` for its preview, approval, execution, and diagnostic workflow.
- Treat metadata/sample retrieval as read-only; it does not authorize a direct REST mutation.

## Defaulted DAT Preparation

For a create that uses a documented Absence Plan profile, prepare the compact
DAT from one normalized value set, not directly from requester inputs. After
the current Data Loader template and describe contract have been refreshed:

1. Preserve every requester-supplied value.
2. Resolve the plan type and classify fields using the policy decision gate in
   `ora-resource/ora_design_enforcement.md`. Captured examples are not defaults:
   ask for required or policy-relevant missing decisions and omit optional
   fields without a policy requirement. Apply only the permitted setup defaults
   and supplied or explicitly confirmed policy values under
   `ora-resource/ora_defaulting_rules.md`.
3. Record every applied value in the `ora_defaulting_rules.md` Task Hook rule
   result as a change with its business-facing label, technical DAT field,
   prior value, final value, and reason.
4. Build each compact `METADATA` and `MERGE` pair from that normalized value
   set. An applied default must appear in both the header and its matching row;
   do not rely on Fusion to default it server-side.
5. Before the immutable Data Loader preview, inspect the exact DAT member in
   the final archive. Block the load when an applied default is absent, blank,
   changed, duplicated, or would replace a requester-supplied value.

The defaulting rule may be recorded as `passed` with no changes only when no
permitted setup default applies. For example, do not insert
`ORA_ANC_RND_NONE` merely because an Accrual capture used it. Ask for a rounding
decision when required or policy-relevant; otherwise omit the optional field.
When the requester selects Always round down, Always round up, or Standard
rounding but omits Rounding Precision, apply and disclose
`RoundingPrecision=0` for whole plan-UOM units. Preserve any explicit precision
and verify that the selected rule and its conditionally required precision are
both present in the same compact parent DAT row.

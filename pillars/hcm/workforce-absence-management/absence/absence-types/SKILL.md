---
skill_id: "hcm.workforce-absence-management.absence.absence-types"
name: "Absence Types Setup Task Guidance"
description: "Provides task-specific setup guidance for Absence Types under the Absence functional area."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Absence Management"
functional_area: "Absence"
functional_area_code: "ORA_ABSENCE"
task_code: "ORA_ANC_MANAGE_ABSENCE_TYPES"
task_name: "Absence Types"
parent_skill_id: "hcm.workforce-absence-management.absence"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "absenceTypes"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absence/absence-types/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absence/absence-types/current/"
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

# Absence Types Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Absence Types` under `Absence`.

## Setup Task Skill Contract

- task_code: `ORA_ANC_MANAGE_ABSENCE_TYPES`
- task_name: `Absence Types`
- parent_skill_id: `hcm.workforce-absence-management.absence`
- pillar: `HCM`
- offering: `Workforce Absence Management`
- functional_area: `Absence`
- functional_area_code: `ORA_ABSENCE`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `absenceTypes`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Absence Types` under `Absence`.

For create requests without an explicit Absence Pattern, first analyze the
supplied absence type name and optional description using
`resolve_absence_pattern` in `ora-resource/ora_reference_lookups.md`. Suggest
one supported business pattern only when the purpose is clear, explain the
name/description clue, and ask the requester to confirm or choose another
pattern. Wait for that answer before applying the pattern or its dependent
defaults. If no pattern can be distinguished, keep the existing flow of asking
the requester to select Generic pattern, Illness or injury, or Childbirth or
placement (maternity). An explicit pattern takes precedence over an inferred
suggestion, subject to the existing lookup and design validation. This intake
step never reclassifies an existing type during update or correction and does
not replace the final immutable Data Loader approval.

When creating, updating, correcting, reviewing, or troubleshooting Absence Type Display Features or Rules, read `references/display-features-and-rules.md`.

For a US `GENERIC`, `II`, or `MAP` Display Features create, call the live
single-persona action through the authoritative standard resource route first.
If that action remains unavailable after its one permitted authentication
refresh, use the guarded US locked 3/5/4 catalog fallback defined in that
reference. Require the fresh exact live pattern template to prove placement
and fresh live lookups to validate the catalog's `DO_NOT_DISPLAY` defaults and
exact lookup types; never derive fallback shared defaults or lookup types from
the pattern template. When every fallback guard passes, this is the required
resolver path and does not require a separate readiness waiver or
production-only confirmation. The normal exact immutable Data Loader preview
and explicit approval immediately before upload remain mandatory.

## Setup Task Metadata

- Task name: `Absence Types`
- Task code: `ORA_ANC_MANAGE_ABSENCE_TYPES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `absenceTypes`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using absenceTypes as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Workforce Absence Management`
- Functional area / Setup Object: `Absence`
- Setup task name: `Absence Types`
- Setup task code: `ORA_ANC_MANAGE_ABSENCE_TYPES`

## Acceptance-Criteria Workflow

Use the same lifecycle pattern as the Workforce Scheduling and Time and Labor
task skills: read and resolve the exact target, validate the current live
contract, produce an immutable preview, obtain a fresh explicit confirmation,
then monitor the submitted Data Loader request and read the target back before
reporting success.

| Consultant request | Required behavior |
|---|---|
| View or filter absence types | Default the read context to active records as of the system date. Support Name, Pattern, Legislation, and Legislative Data Group filters. Render every returned record in one table, with these business-labelled columns in this order: Absence Type Name, Effective Start Date, Effective End Date, Status, Pattern, Entry Display Priority, Legislation, and Legislative Data Group. Show an unset display priority as `—`; do not return a names-only list. |
| Create | Require Name, Legislation, Legislative Data Group, Pattern, and Effective Start Date; default an omitted start date to the system date. Plans/reasons are optional. For a new type, set resolved-intent `hierarchyKeyStrategy` to `native-user-keys`. Omit root and child surrogate IDs. Bind direct children with `LegislationCode` plus `Name`; use unique `AbsenceRegionCode` for regions and unique `AbsenceUsageCode` for usages, with each usage carrying its owning `AbsenceRegionCode`. Verify these LOCAL/PARENT user-key alternatives against fresh registered metadata. Fusion allocates the IDs, so no client-generated-ID collision check or global collision endpoint is required. Include exactly one new type per archive. Retain all region and usage persona lookup/display/default fields from the fresh pattern. Omit standard rule rows and verify Fusion-generated rules after load; explicit rule creation is not supported by this key strategy. Existing-record operations continue to use exact returned IDs. Never automatically replay a create. |
| Configure a pattern | Guide Generic pattern, Illness or injury, and Childbirth or placement separately. Review Type Details, Plans and Reasons, Display Features, Rules, Action Items, and Event Processing before the immutable preview. |
| Update or correction | Resolve exactly one current type and the intended effective-dated record. State whether the request creates a future-dated change or corrects the selected record. Do not change Legislation or Pattern in an update. |
| End date or delete | Require the exact record and explicit operation. Preserve and disclose an application-reported constraint; never infer whether a record deletion or ZAP is intended. |
| History | Retrieve the available effective-dated records for the exact resolved type and present the change dates, status, pattern, and available change information. |

Every mutation requires the current immutable Data Loader preview and explicit
consultant approval. This skill never performs a direct REST mutation.

For a test-owned CRUD regression, create the complete pattern hierarchy in one
ZIP, read back the exact expanded hierarchy, update the parent and at least one
Display Features usage using only returned Fusion IDs, and verify history plus
only the requested deltas. Parent and Display Features mutations use separate
immutable ZIPs on the current registered contract: a combined parent MERGE and
child-update graph is a proven real failure with child `Not Found` and no
committed state. If either scope created a new effective slice, run and verify
Delete Changes on that exact section; parent Delete Changes does not cascade to
independently dated usage slices. Then ZAP only that disposable type after
explicit immutable Data Loader approval and require an exact zero-result final
readback. Fusion enforces dependency restrictions during the approved load;
do not require a separate dependency-validation API or treat empty child
collections as no-impact proof.
Reconcile every terminal result against live state before the next archive or
any replay. Use `reconcile_absence_type_create_result` for creates and
`reconcile_absence_type_non_create_result` for every update, correction, end
date, Delete Changes, ZAP, and child mutation. Both exact-ID and canonical
semicolon-delimited business-key reads must use the operation's effective date,
and every region, usage, and rule collection must be independently paged to its
own completion by following exact returned child links from a parent read that
omits `onlyData=true`; never treat a bare expanded array as complete. Preserve
the official loader result; a changed attempt is a new immutable archive with
new approval and, for a create, revalidated native business-key bindings.

## Date-Effective Data Loader Contract

The registered UCM DAT template—not REST `/describe` metadata and not a
reduced sample—is authoritative for date-effective controls. Refresh it before
preparing each create, update, correction, end-date, record-delete, or ZAP
source. Treat `EffectiveStartDate` as a normalized business input and emit it
only when the refreshed section header supports it. Emit `effectiveOf` only
when that exact section header supports it, deriving its value from the
operation; never accept a caller-authored range-control string.

- For a create, retain the requested business effective start date as an
  intent/audit value and disclose it in the final summary. On the current
  Absence Types loader contract, send it through the parent
  `effectiveOf=RangeStartDate=<YYYY-MM-DD>` create control. Do not substitute
  the physical parent `EffectiveStartDate` column: live CRUD evidence shows
  that Fusion accepts the archive but still assigns its server date. Stop when
  the refreshed parent header no longer supports the create `effectiveOf`
  control rather than silently accepting a different date.
  For a non-create operation, require the explicit operation date and derive
  the operation-specific mapping.
- Use the documented `RestAction` and `effectiveOf` mapping in
  `ora-resource/ora_defaulting_rules.md`. Stop before preview if the refreshed
  contract cannot represent the selected parent or included child operation.
- For **Delete Changes**, prepare the exact `absenceTypes` parent `DELETE`
  row with `RangeMode=DELETE_CHANGES;RangeStartDate=<EffectiveStartDate>`.
  Do not reinterpret it as ZAP or add a child merely to carry date context.
  This removes only the parent slice. If independently dated Display Features
  slices must also be reverted, reconcile the parent first and submit a
  separate metadata-root child Delete Changes archive for those exact usages.
- Do not include a child merely to carry date context. Include children only
  when they are requested and the current child contract supports the selected
  operation.
- Require one exact current absence-type identity for every non-create
  operation. Resolve the selected effective-dated record before preparation.

The operation validation and completion requirements are defined in
`ora-resource/ora_defaulting_rules.md`,
`ora-resource/ora_input_validation.md`, and
`ora-resource/ora_reference_lookups.md`.

## Plan Association Child

When a request associates an absence plan with an absence type, use the
registered `absenceTypes` Data Loader `plans` child. The child is optional: do
not require it for a standalone absence-type create, and do not require an
absence type for a standalone absence-plan create.

Require a verified Absence Plans workflow handoff for each requested
association. It must identify one exact current plan, its legislation and LDG,
effective dates, active status, and the plan values that the refreshed child
template marks as required. A name-only request must go through Absence Plans
`find_absence_plan_by_exact_name` followed by primary-key validation; do not
perform a type-local plan lookup or invent an ID. The plan must be active,
effective on the association date, and compatible with the type legislation
and LDG. Use a requester-supplied association date when present; otherwise use
the resolved absence type's `EffectiveStartDate`. Never substitute the system
date for this association-date default. The absence type's status does not
block a plan association; validate its exact effective-dated identity,
legislation, and LDG instead.

The live registered template is authoritative. Validate only the current
`plans` child attributes, parent key, and `RestAction` contract before
preparing the source. For every supported plans-child create or update flow, resolve the requested
association status through `resolve_type_plan_association_status` and map its
returned `LookupCode` to `PlanStatusCode` and its `Meaning` to
`PlanStatusMeaning` when that column is present. This is the status of the
type-plan association; do not derive it from the absence plan or absence type.
Map plan identity and compatibility values only from the verified handoff. Do
not send `AbsenceTypePlanId`, synthesize a plan/status/statutory display value,
reuse stale template columns, or invent a date-effective control. If the
refreshed template requires a value that the verified plan handoff or the
association-status LOV does not provide, stop as a template-contract gap rather
than guessing it. Do not query current type-plan associations solely to reject
a duplicate plan or priority: the Fusion REST/Data Loader layer owns those
business-rule validations and returns any resulting conflict.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `absenceTypes` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "absenceTypes" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Required Portable Source Preparation and Verification

For REST Data Loader source preparation, read
[Portable Source Preparation](../references/portable-source-preparation.md)
and use `pillars/hcm/workforce-absence-management/absence/scripts/prepare_absence_source.py`.
Supply current registered metadata and resolved business decisions; do not
create ad hoc project or temporary generators. Verify the exact final DAT or
ZIP with `--verify` and `--model` before the existing Data Loader preview.
This local check does not replace task rules, live lookups, native business-key linkage
checks, immutable approval, submission, or post-load verification.

Complete the applicable Task Hook rules before calling an archive ready for
submission or requesting upload approval. An offline pass or a successful live
schema validation is not completed task validation. Follow the **Task Hook
Continuation** section of Portable Source Preparation: a returned `ready`
rule plan requires assisted execution by Codex, not a new executor or a pause
for the requester to execute the rules. If a required dependency,
identity or effective-date check has no supported route, report that
specific blocker before approval. Do not invent a global child-resource URL,
treat HTTP 404 as an empty result, or treat a current-date hierarchy scan as a
complete global/history collision check. The native-user-keys create route
does not generate numeric child IDs and requires no such collision check or
test-only waiver. It still requires exact metadata and business-key validation.

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

When interacting with a requester, identify inputs, missing values, and validation errors by their business-facing labels rather than raw Data Loader or REST attribute names. For example, say `Effective Start Date`, `Absence Pattern`, and `Legislative Data Group`, not `EffectiveStartDate`, `AbsencePatternCode`, and `LegislativeDataGroupId`. Keep raw attribute names only in technical artifacts, loader-source previews, or when the requester explicitly asks for them.

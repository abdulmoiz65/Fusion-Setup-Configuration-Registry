---
skill_id: "hcm.workforce-absence-management.absences-additional.absence-certifications"
name: "Absence Certifications Setup Task Guidance"
description: "Guides conversational creation, viewing, and supported maintenance of absence certification setup definitions with Redwood Details/Rules intake, conditional lookups, effective-row validation, and approved Data Loader execution."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Absence Management"
functional_area: "Absences Additional"
functional_area_code: "ORA_ABSENCES_ADDITIONAL"
task_code: "ORA_ANC_MANAGE_ABSENCE_CERTIFICATIONS"
task_name: "Absence Certifications"
parent_skill_id: "hcm.workforce-absence-management.absences-additional"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "absenceCertifications"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM workforce absence management pillar team"
version: "1.3.3"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "requested_operation"
  - "business_configuration"
  - "target_environment"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "configuration_summary"
  - "lifecycle_readiness"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.project-mgmt.project-workspace-initializer"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absences-additional/absence-certifications/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absences-additional/absence-certifications/current/"
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
side_effects:
  - "Persists local configuration drafts, validation evidence, and skill-run records; approved Fusion mutations are delegated to core.data-loader."
required_privileges: []
---

# Absence Certifications Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Absence Certifications` under `Absences Additional`.

## Setup Task Skill Contract

- task_code: `ORA_ANC_MANAGE_ABSENCE_CERTIFICATIONS`
- task_name: `Absence Certifications`
- parent_skill_id: `hcm.workforce-absence-management.absences-additional`
- pillar: `HCM`
- offering: `Workforce Absence Management`
- functional_area: `Absences Additional`
- functional_area_code: `ORA_ABSENCES_ADDITIONAL`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `absenceCertifications`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `absenceCertifications` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "absenceCertifications" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Absence Certifications` under `Absences Additional`.

## Conversational Workflow and Required Read Order

The observed target Redwood UI is the functional source of truth. Use Jira
criteria for traceability and mark conflicting criteria not applicable to the
observed UI; do not add actions solely because a story requests them. This
certification UI retains Update, Correct, End Date, Delete and History, distinct
from the single-current-version Leave Agreements flow.

For this task, the current Redwood page has priority, followed by WFM-82961's
ACs. Limit Add to Documentation or Entitlement, and Status to Active or Inactive.
Management is read-only User-defined during Create. Do not accept backend-only
fields, an approved alternative classification, upsert/replacement, or worker
certification operations. Naming best practices are advisory.

The 2026-10-07 multi-row review exposed enabled Delete Record for the selected
non-first row. It extends the previous row to the deleted row's end date.
Require current configuration, exact stored row, complete contiguous History,
User-defined protection and the current physical-row DELETE_CHANGES adapter
contract before preparation. Never ask for a replacement deletion date.
Delete Certification is the whole object and all its date-effective records.
For Delete Record, use declared configuration and History REST reads only, then
the packaged local resolver. Never route a browser/UI read or mutation. Data
Loader remains the exclusive mutation route; Fusion enforces business restrictions.

Create and View use their own readiness checks. A new record does not require
an existing target-row identity or a deletion-impact resolver. Maintenance and
destructive operations retain their exact-row, capability and applicable
impact gates. Do not label every request blocked because a different operation
has a missing contract.

For an implementation request, enter through `router.implementation-router`
and use this generated task after project and task selection. This skill owns
setup certification definitions; worker certification evidence, completion,
and attachments are outside this task.

### Standalone Certification Routing

A request to create, view, or perform supported maintenance on one certification
uses this task's workflow. It does not require the parent's functional-area
task-dependency-resolver or an FSM/BOSS task-discovery call. A BOSS authentication
or discovery failure from another workflow is not a certification execution
prerequisite. Select this route from the requested scope before external calls,
not as a fallback after failed functional-area sequencing.

For the Data Loader route, require an active project Run Book bound to the selected environment and an
exact catalog-resolved `Absence Certifications` task context with task code
`ORA_ANC_MANAGE_ABSENCE_CERTIFICATIONS` and business object
`absenceCertifications`. Reuse the current matching task context. If it needs
adding or refreshing, delegate to `core.project-mgmt.project-workspace-initializer`:
preserve existing identified mapping rows, validate the exact task and offering/
functional-area context through its catalog checks, and use its
`create_project_runbook.py --dry-run` followed by `--refresh-artifacts` workflow.
Do not hand-edit the generated task context, reset an active Run Book binding,
or create/merge a live Run Book merely to refresh these local artifacts. A new
or unbound project still follows the initializer's normal Run Book creation gate.

Use only the owning helper's generated positive sequence to select the task for
Task Hook. Where no resolver sequence was supplied, that value is a local
selection index, not an Oracle/FSM dependency order; never invent a
`Resolver Sequence`. Missing or ambiguous catalog/context evidence stops with
that specific gap. Local context generation does not waive task rules, current
LOVs/template checks, supported-operation gates, or immutable approval.
After source preparation, `core.data-loader` owns Task Hook validation, the
exact-archive preview and approval lifecycle, and approved submission.

Read [Redwood workflow](references/redwood-workflow.md) for Details/Rules intake
and conditional fields, then [lifecycle and acceptance](../references/absence-additional-lifecycle.md)
for the requested view or maintenance operation. Follow the task registry,
execution guide, and the applicable owning `ora-resource` tables before any
declared lookup or Data Loader preparation. The lookup tables own API mechanics;
the Redwood reference owns conversation structure and source provenance.
Load [error handling](ora-resource/ora_error_handling.md) before preview or any
declared external operation.

The empty `required_privileges` list describes local planning only. Before an
external read or mutation, the selected core/read workflow must validate target
environment identity, authorized access, current task metadata, and applicable
inputs. Use that workflow's declared client and recovery rules; this skill does
not invent privileges or a parallel transport. Delegate polling, timeouts and
recovery to core, retain returned process/request identifiers, and persist
redacted failure diagnostics in the routed project workspace.

Use Name and Classification as the observed UI labels, while accepting the
existing Certificate Name and Certification Type aliases. Group missing inputs
by the current stage, reuse known choices, and present business meanings.
Show Description and requested rule details in a view; distinguish unavailable
evidence from blank values. Keep draft, validating, blocked, pending
confirmation, submitted, and completed states distinct. Report success only
after the core load and exact-record reconciliation pass.

Render only fields shown by the current Redwood view and its selected branch.
A full internal read for validation does not authorize displaying backend-only
fields. Native IDs and audit controls remain internal except UI-visible History.
The CSV/Data Loader capabilities below are technical transport for supported
actions; they do not introduce a separate Import, upsert or replacement action
into the Redwood conversation. A Redwood-style list export must preserve the
requested filters and visible columns, rather than being described as a whole
setup-task export when that is not what the user requested.

History uses the task's declared `read_absence_certification_history` resolver,
with the exact certification identity and current described History finder.
Display only the panel's effective date/range and Last Updated Date/By; retain
technical first-split/row identifiers internally. Read all pages and distinguish
empty from unavailable history. No mutation approval is required for this read.

For Update, never change Name, Classification, Legislation, Trigger, or the
stored Effective Start Date. Keep the explicit operation date separate from
those immutable values and send only resolved identity plus mutable changes.
Correct also retains the read-only identity, dates, Management, and disabled
Absence Record Update Rule. It does not unlock hidden Creation, due-date,
expiration or payment rules. Use the selected row's stored Start Date for
correction; do not ask for a replacement date. Resolve configuration-specific
Confirmation event visibility from current evidence. Correction, whole deletion, and end-date need their own exact
row, capability, protection/impact, preview, and approval evidence. The generic
date-control map alone does not establish support. Missing contracts block
execution and must be reported with one next action.

Functional review belongs to the HCM Absence Management pillar team; technical
review belongs to the Data Loader owner. The current public worker REST API
is not evidence for this internal setup resource's execution contract.

## Exact Search and Non-Create Identity Contract

Support read-only discovery of an absence certificate by exact `Name`, optional `Legislation`, and optional lookup as-of date through `find_absence_certification_by_exact_name`.

- Default an omitted lookup as-of date to the current system date for search only. A lookup date never supplies the effective date for a mutation.
- Do not default omitted search legislation to US. Search by exact name across legislation and continue only when one effective record is unambiguous; otherwise ask for the business-facing `Legislation` value.
- Read every result page, match the name exactly and case-insensitively, validate the returned effective range against the lookup as-of date, and require exactly one record.
- Retain the certificate identifier and stored codes internally. For the identity search summary, present the business-facing `Certificate Name`, `Certification Type`, `Legislation`, `Status`, `Effective Start Date`, and `Effective End Date` values. A full view additionally uses `refresh_absence_certifications_describe` and `read_absence_certification_configuration` for Description, Management, Trigger, requested rules, and requested children.
- Require this exact resolved identity before preparing any non-create Data Loader operation. Search remains read-only and never authorizes a mutation.

For Create, `ANC_CERT.VALIDATE_LOOKUPS` uses the same finder in its declared
`create_preflight` mode with the final proposed Name, resolved Legislation and
normalized Create Start Date. Read all pages: zero matching records returns
`collision_clear` within that queried scope; any match stops Create without
upsert or overwrite. Failed, unread or ambiguous results block readiness.
This scoped existence check does not prove global historical uniqueness and
does not supply an existing identity for the new record. Ordinary search and
maintenance keep their exactly-one behavior. Changes to the proposed identity,
date or target environment require renewed scoped collision evidence.

## Setup Task Metadata

- Task name: `Absence Certifications`
- Task code: `ORA_ANC_MANAGE_ABSENCE_CERTIFICATIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `absenceCertifications`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` in `REST` mode using `absenceCertifications`.

Use this task metadata when invoking those skills:

- Offering: `Workforce Absence Management`
- Functional area / Setup Object: `Absences Additional`
- Setup task name: `Absence Certifications`
- Setup task code: `ORA_ANC_MANAGE_ABSENCE_CERTIFICATIONS`




## Required Portable Source Preparation and Verification

For REST Data Loader source preparation, read
[Portable Source Preparation](../../absence/references/portable-source-preparation.md)
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
- `requested_operation`
- `business_configuration`
- `target_environment`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`
- `configuration_summary`
- `lifecycle_readiness`

## Implementation Notes

Use the parent functional-area skill `hcm.workforce-absence-management.absences-additional` when functional-area sequencing or scope planning is requested; its planning dependencies are not prerequisites for standalone certification configuration. Track token usage for any generated project artifact or skill-run record using the manifest policy.

When interacting with a requester, identify inputs, missing values, defaults, and validation errors by their business-facing labels rather than raw Data Loader or REST attribute names. For example, say `Effective Start Date`, `Certification Type`, `Status`, and `Legislation`, not `EffectiveStartDate`, `ClassificationCode`, `StatusCode`, and `LegislationCode`. Keep raw attribute names and stored lookup codes only in technical artifacts, loader-source previews, or when the requester explicitly asks for them.

Require a confirmed `Trigger` for every create, regardless of certification type. Never default or silently select it. After resolving `Certification Type`, use `resolve_absence_certification_trigger` to retrieve the applicable live Trigger options. Validate an explicitly supplied value against that list. When Trigger is omitted and the requester's business intent clearly identifies exactly one available option, present that option as a business-facing suggestion and require explicit confirmation. When intent is unclear, present all available business-facing options for the resolved Certification Type and ask the requester to select one. Populate the loader value only after explicit supply, selection, or confirmation; keep stored lookup codes internal unless the requester explicitly asks for technical details.

For a create request that omits both `EffectiveStartDate` and `RangeStartDate`, default the business effective start date to the current system date in `YYYY-MM-DD` format. Preserve a requester-supplied date. If both business inputs are supplied, require them to match. Derive the Data Loader `effectiveOf` value from the normalized business date; never accept caller-authored `effectiveOf`.

Allow the registered Data Loader template and final DAT `METADATA` to retain an `EffectiveStartDate` attribute. By default, require its value to remain blank in every populated data record and carry the business start date only through the derived `effectiveOf`. Update always rejects a nonblank physical `EffectiveStartDate`, including an unchanged copied value; dual-population evidence cannot override that input contract. For other applicable operations, if both physical `EffectiveStartDate` and the `RangeStartDate` inside `effectiveOf` are populated, normalize and require equal dates, then still block preview unless current task-, operation-, and section-specific evidence explicitly proves that Fusion supports dual population. A mismatch always blocks and cannot be overridden by choosing either value.

Do not request or default `EffectiveEndDate` for create. Require the explicit operation date for Update; use the exact selected row's stored date for Correct. For End Date, preserve a supplied date or disclose Redwood's current-date candidate and bind confirmation to the final chosen date in core preview. Validate the applicable `effectiveOf` mapping against the current registered Data Loader template before preview. Prepare Delete Changes only after exact configuration and complete History validation; never navigate or inspect the UI for this operation. Whole-object ZAP has no range date: retain any lookup as-of date solely as target-selection context and reject a supplied mutation range date.

During maintenance, reuse the full before state for unchanged Classification,
Trigger, and conditional rules; do not collect new create inputs for a
Description-only Update. Resolve a saved Trigger's display meaning without
requesting a new selection or treating it as a payload change. Evaluate the
task graph as source validation to reach `source_ready_for_preview`, then use
core Data Loader to build the immutable preview and obtain its single final
approval. Validation readiness is neither approval nor a submitted mutation.

## Data Loader REST Execution Boundary

Resolve supplied Eligibility Profile, Due Date Reference Date, Expiration Reference Date, Due Date Unit of Measure, Expiration Unit of Measure, Confirmation Reasons, and Voiding Reasons through the additional LOV resolvers in `ora-resource/ora_reference_lookups.md`. Apply the corresponding input-validation and design-enforcement rules for every operation supplying these values. Resolve names to codes or identifiers internally; preserve validated user selections before applying defaults. Confirmation Reasons and Voiding Reasons are independent ordered multi-selects stored as comma-separated codes. An eligible optional empty selection is represented as null; Entry required instead blocks an empty or incomplete list.

Route every Absence Certifications mutation exclusively through `core.data-loader` in `REST` mode with the registered business object `absenceCertifications`.

- Do not invoke `core.fusion-api.rest-api-client` for `POST`, `PATCH`, `DELETE`, or upsert operations.
- Use `core.data-loader` for template validation, immutable preview, approval, execution, and diagnostics.
- Treat REST describe and other metadata reads as validation evidence only; they do not authorize a direct REST mutation.

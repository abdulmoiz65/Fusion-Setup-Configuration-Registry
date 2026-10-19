---
skill_id: "hcm.workforce-absence-management.absences-additional.leave-agreements"
name: "Leave Agreements Setup Task Guidance"
description: "Guides conversational leave agreement template creation, full viewing, and supported maintenance with Redwood pattern/legislation intake, entitlement and certification rows, live lookups, and approved Data Loader execution."
layer: "pillar"
pillar: "HCM"
offering: "Workforce Absence Management"
functional_area: "Absences Additional"
functional_area_code: "ORA_ABSENCES_ADDITIONAL"
task_code: "ORA_ANC_MANAGE_LEAVE_AGREEMENTS"
task_name: "Leave Agreements"
parent_skill_id: "hcm.workforce-absence-management.absences-additional"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "absenceLeaveAgreementTemplates"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM workforce absence management pillar team"
version: "2.0.0"
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
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absences-additional/leave-agreements/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/workforce-absence-management/absences-additional/leave-agreements/current/"
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

# Leave Agreements Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Leave Agreements` under `Absences Additional`.

## Conversational Workflow and Required Read Order

Create and View use their own readiness checks. A new record does not require
an existing target-row identity or a deletion-impact resolver. Maintenance and
destructive operations retain their exact-row, capability and applicable
impact gates. Do not label every request blocked because a different operation
has a missing contract.

For an implementation request, enter through `router.implementation-router`
and use this generated task after project and task selection. This skill owns
setup templates, not a worker's entitlement agreement or leave allocation.

Read [Redwood workflow](references/redwood-workflow.md) for staged Details,
Rules and Reasons, Entitlements, and Certifications intake. Read
[lifecycle and acceptance](../references/absence-additional-lifecycle.md)
before viewing or maintaining a record, then the task registry, execution guide,
and applicable owning `ora-resource` tables before any declared lookup or
Data Loader preparation.

Preserve the selected pattern, legislation, business dates, supplied choices,
and each child row's identity. Ask only for missing applicable fields using
the observed UI labels. Offer the observed Status choices Active, Closed,
Inactive, and Pending; resolve the selected choice in the target environment.
Present Pending as the lookup-verified create candidate when Status is omitted,
and User-defined as the observed management type. Show complete
parent details, Description, eligibility/rules, entitlement mappings, and
certification associations in a requested view. Never pass off an identity
lookup as a full configuration view.

The observed target Redwood UI is the functional source of truth. It supports
View, Create, Edit current template and Delete Agreement, with current child
maintenance in Edit. It has no history, dated Update/Correct, dated child
removal, or End Date actions. Explain those requests as unavailable and offer
applicable supported choices; conflicting story criteria are not applicable.
Never silently substitute Edit or whole deletion for a dated request. An
ordinary request such as "update the Description" means changing that current
field through Edit when no dated-slice intent is expressed; classify meaning
rather than treating the verb update alone as an unsupported action.

Edit reads the full before state and stages changes to currently editable fields.
It requires no new effective date. The observed header Start Date, Legislation,
Management and Pattern are read-only; Name, Status, Legislative Grouping and
Description are editable. Check the selected target for conditional Rules and
child fields. Current adapter metadata defines execution, not extra business
operations. A missing required adapter or impact contract blocks only execution
of the affected available action; draft review and other actions can continue.

Stage child choices as the UI drawers do, then review all parent and child
changes together. Core Data Loader owns the single immutable final approval.
Distinguish draft, validating, blocked, pending confirmation, submitted, and
completed; confirm completion only after load status and exact-record
reconciliation. Apply country guidance such as UK birth/adopter Conversion or
partner Agreement only when its prerequisites and declared resolvers support
the scenario. Never invent UK formulas or choose another country to cure a gap.

Functional review belongs to the HCM Absence Management pillar team; technical
review belongs to the Data Loader owner.

## Setup Task Skill Contract

- task_code: `ORA_ANC_MANAGE_LEAVE_AGREEMENTS`
- task_name: `Leave Agreements`
- parent_skill_id: `hcm.workforce-absence-management.absences-additional`
- pillar: `HCM`
- offering: `Workforce Absence Management`
- functional_area: `Absences Additional`
- functional_area_code: `ORA_ABSENCES_ADDITIONAL`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `absenceLeaveAgreementTemplates`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `absenceLeaveAgreementTemplates` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "absenceLeaveAgreementTemplates" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Leave Agreements` under `Absences Additional`.

## Requester Interaction Contract

When interacting with a requester, identify inputs, missing values, defaults, choices, search results, and validation errors by their business-facing labels rather than raw Data Loader or REST attribute names. For example, say `Agreement Name`, `Agreement Type`, `Target Plan`, `Source Plan`, `Source Absence Type`, `Management Type`, `Status`, `Partner Rule`, `Eligibility Rule`, `Legislation`, `Legislative Grouping`, `Validation Formula`, `Denial Reasons`, `Withdrawal Reasons`, `Event Type`, `Eligibility Formula`, `Eligibility Profile`, `Payment Percentage Display Formula`, `Override Allowed`, `Certification Name`, and `Effective Start Date`, not `AbsenceAgreementName`, `AgreementPatternCode`, `TargetPlanId`, `SourcePlanId`, `SourceAbsenceTypeId`, `ManagementTypeCode`, `StatusCode`, `PartnerRuleCode`, `EligibilityRuleCode`, `LegislationCode`, `LegislationGroupingCode`, `ValidationFormulaId`, `DenialReasonCode`, `WithdrawReasonCode`, `EventTypeCode`, `EligibilityFormulaId`, `EligibilityProfileId`, `PaymentPercentDisplayFormulaId`, `OverideFlag`, `AbsenceCertificationId`, and `EffectiveStartDate`.

Accept business-facing names and meanings wherever the documented resolver can map them to one exact current Fusion value. Keep raw attribute names, stored lookup codes, surrogate identifiers, resolver names, lookup types, and REST endpoints internal. They may appear only in technical artifacts, loader-source previews, failure diagnostics that require implementation-owner action, or when the requester explicitly asks for technical details.

For a Target Plan, prefer the exact plan name supplied by the requester and resolve its plan identifier internally through `resolve_target_absence_plan`. Do not ask for `TargetPlanId` merely because the loader requires it. Ask for a business-facing `Target Plan` name first; request a plan identifier only when an exact name cannot resolve uniquely or the requester explicitly chooses to provide one. Present the resolved plan name, legislation, status, and effective dates, while keeping its identifier internal unless technical details were requested.

Apply the same name-first interaction to Legislative Grouping, Validation Formula, Denial Reasons, Withdrawal Reasons, Event Type, Eligibility Formula, Eligibility Profile, Payment Percentage Display Formula, Override Allowed, and Certification Name. Resolve each exact business name or meaning through the documented read-only resolver in `ora-resource/ora_reference_lookups.md`, retain only the required code or identifier internally, and never ask for the technical field first merely because the Data Loader template stores it.

Ask for Event Type only for Agreement. Ask for Eligibility Formula only when Eligibility Rule is Formula, or Eligibility Profile only when Eligibility Rule is Profile; never request or retain both. Ask for Override Allowed only after a Payment Percentage Display Formula is selected in the same Target Plan mapping. Treat Denial Reasons and Withdrawal Reasons as ordered multi-select business values. Scope Legislative Grouping and Certification Name to the resolved Legislation, and re-resolve or clear them whenever Legislation changes.

For a read-only agreement search or non-create target selection, retain the agreement identifier and stored codes internally. For the search summary, present `Agreement Name`, `Agreement Type`, `Legislation`, `Status`, `Effective Start Date`, and `Effective End Date` using current display values. For an AC1 list request without an exact name, use `list_leave_agreement_templates` in `ora-resource/ora_reference_lookups.md`; zero or multiple matching rows are valid results. Apply the requested Legislation and As-of Date across every current-collection page. If the requester wants the full configuration for every matching agreement, run `refresh_leave_agreement_describe` and `read_leave_agreement_configuration` for each selected parent. Route all reads through `core.fusion-api.rest-api-client`. No Data Loader source, approval, or mutation follows a read-only View. For a full view or maintenance review, use `refresh_leave_agreement_describe` and `read_leave_agreement_configuration` to retrieve the Description, rules and all child collections. Missing evidence is unavailable, not blank. If an exact single-target search is ambiguous, ask for the missing `Agreement Name`, `Legislation`, or `Status` using those business-facing labels.

## Current-Version Data Loader Controls

For Create, `LA.REFRESH_DATALOADER_CONTRACT` uses
`find_leave_agreement_template` in its declared `create_preflight` mode after
the final proposed Agreement Name and Legislation resolve. Reuse the current
paginated collection GET and check all returned statuses: zero matching records
returns `collision_clear` within that scope; any match stops Create without
upsert or overwrite. Failed, unread or ambiguous results block readiness.
The check does not prove global historical uniqueness or give the new record
an existing identity. Ordinary search and maintenance keep their exactly-one
behavior. A changed proposed identity or target invalidates collision evidence;
do not add a history query or date/status filter to make the check pass.

The portable helper accepts `create`, `edit`, and `delete` for this task.
Edit/Delete use exact returned identities and registered keys. Edit derives
PATCH and `effectiveOf=RangeMode=CORRECTION;RangeStartDate=<verified stored Start Date>`; Delete
uses DELETE with date-free `effectiveOf=RangeMode=ZAP`. These controls are
internal to the loader; they do not expose dated Correction or ZAP actions. Do not
request a new date, modify stored date/header values, or derive UPDATE,
END_DATE or DELETE_CHANGES controls, or accept a caller-selected ZAP. Current metadata and the selected adapter's
operation contract must pass before preparation and execution.

Create retains the existing declared native POST mapping from the parent Start
Date to `RangeStartDate`. Default the parent Start Date to the current date only
when omitted and disclose it. Keep physical date data-record values blank by
default; registered METADATA columns may remain. A new child in an existing
Edit may need the verified stored parent Start Date for this adapter's create
context. This is internal source representation, not a new business date or
history capability. Never accept caller-authored `effectiveOf`.

## Mutation Routing

Route supported parent and current-child Create/Edit/Delete operations
exclusively through `core.data-loader`, REST mode, BusinessObject
`absenceLeaveAgreementTemplates`. Its immutable artifact preview and approval
are the single final execution gate. Do not issue direct REST mutations or use
browser Save as an alternate execution route.

## Setup Task Metadata

- Task name: `Leave Agreements`
- Task code: `ORA_ANC_MANAGE_LEAVE_AGREEMENTS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `absenceLeaveAgreementTemplates`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `absenceLeaveAgreementTemplates` as the `BusinessObject` in `REST` mode.

Use this task metadata when invoking those skills:

- Offering: `Workforce Absence Management`
- Functional area / Setup Object: `Absences Additional`
- Setup task name: `Leave Agreements`
- Setup task code: `ORA_ANC_MANAGE_LEAVE_AGREEMENTS`




## Operational Preconditions and Failure Handling

Before a declared external step, validate the selected project workflow, exact
environment, task/catalog identity, authorized metadata/lookup access, current
native contract and applicable input/dependency evidence. The manifest's empty
privilege list applies to local planning; it does not grant Fusion access.
The selected core workflow owns actual identity and privilege checks.

Load `ora-resource/ora_error_handling.md` before preview or execution. Use its
operation-specific diagnosis and the shared lifecycle failure taxonomy. Core
owns authentication refresh, bounded polling, job status and recovery; never
retry an uncertain write. Persist redacted stage/status, available external
IDs, artifact references and next action under the selected project. On failed
jobs retain available status/process logs; on timeout retain the last status
and next-check guidance. Local preparation fails before overwrite or submission;
its receipt is evidence of source integrity, not execution approval.

## Compatibility and Migration

Version 2.0 targets the observed single-current-version Redwood flow. Skill ID,
folder, task code and business object remain unchanged. Legacy Leave source
intents `correction`, `end-date`, `delete-changes` and `zap` are rejected.
An undated `update` request maps to current `edit`, whose loader control is
internal CORRECTION at the verified stored Start Date. A supplied update date
is rejected, not used. Preserve any explicitly dated business intent, explain
availability and collect a supported choice.

Rebuild previous maintenance sources from current metadata and the exact full
before state, using `edit`/`delete` without range dates. A child Add uses the
verified stored parent Start Date as native create context. Do not reuse old
approved archives or hand-edit prepared models; run final source verification
and core's new immutable preview/approval. Certification and other absence
objects retain their own operation contracts. If another target UI exposes a
different lifecycle, author and validate that target contract before execution.

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

Use the parent functional-area skill `hcm.workforce-absence-management.absences-additional` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

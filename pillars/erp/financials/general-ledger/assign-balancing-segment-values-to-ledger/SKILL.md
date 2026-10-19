---
skill_id: "erp.financials.general-ledger.assign-balancing-segment-values-to-ledger"
name: "Assign Balancing Segment Values to Ledger Setup Task Guidance"
description: "Provides task-specific setup guidance for Assign Balancing Segment Values to Ledger under the General Ledger functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "General Ledger"
functional_area_code: "ORA_FIN_GENERAL_LEDGER"
task_code: "GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEDGER"
task_name: "Assign Balancing Segment Values to Ledger"
parent_skill_id: "erp.financials.general-ledger"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP financials pillar team"
version: "0.1.1"
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
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/general-ledger/assign-balancing-segment-values-to-ledger/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/general-ledger/assign-balancing-segment-values-to-ledger/current/"
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

# Assign Balancing Segment Values to Ledger Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Assign Balancing Segment Values to Ledger` under `General Ledger`.

## Setup Task Skill Contract

- task_code: `GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEDGER`
- task_name: `Assign Balancing Segment Values to Ledger`
- parent_skill_id: `erp.financials.general-ledger`
- pillar: `ERP`
- offering: `Financials`
- functional_area: `General Ledger`
- functional_area_code: `ORA_FIN_GENERAL_LEDGER`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Assign Balancing Segment Values to Ledger` under `General Ledger`.

## Setup Task Metadata

- Task name: `Assign Balancing Segment Values to Ledger`
- Task code: `GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEDGER`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. For an unscoped task baseline, export setup task data with `shared.setup-export.task-level-export`.
2. For a ledger-scoped baseline, use the task-local scoped-export route below through `core.fusion-api.rest-api-client`, then retrieve the created process with the existing `shared.setup-export.task-level-export` result helper.
3. Validate setup task data with `shared.validation.setup-data-validator`.
4. Validate reference data with `shared.validation.reference-data-validator`.
5. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Financials`
- Functional area / Setup Object: `General Ledger`
- Setup task name: `Assign Balancing Segment Values to Ledger`
- Setup task code: `GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEDGER`

## Ledger-Scoped Export Route

When the request identifies a target ledger, do not use the generic unscoped
task-export command as the assignment baseline. Obtain a paired, read-only
primary-ledger-scoped evidence set before previewing or validating an
assignment: one export for this task and one for `Assign Balancing Segment
Values to Legal Entities` (`GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEGAL_ENTITIES`).
The pair establishes direct-ledger assignments and legal-entity assignments
independently. Read the task-local input, reference-lookup, dependency,
design-enforcement, and error-handling resources before preparing either export.

## Task Selection Boundary

This skill owns a direct assignment to a ledger for nonlegal-entity use. It
does not own an assignment to a legal entity within a ledger.

- Route a request that supplies a Company Value and a target that resolves as
  a Ledger to this skill, unless it explicitly identifies a Legal Entity or
  says the assignment is to a Legal Entity. This includes ordinary wording such
  as "assign Company Value X to Y" once Y resolves exactly as a ledger; do not
  require the user to repeat the word "ledger" after the name.
- If the request explicitly names a Legal Entity or says "to a Legal Entity",
  stop before any lookup or export and route to Assign Balancing Segment Values
  to Legal Entities.
- A reference to a Legal Entity without its exact name is incomplete for the
  Legal Entity task: ask for that name. Do not substitute the supplied ledger
  as a Legal Entity. A request with no Legal Entity signal is a direct ledger
  assignment after exact ledger resolution.

This task assigns an existing value; it does not create or maintain the value.
Never ask the implementer for Summary, Allow Posting, Allow Budgeting,
hierarchy, or other value-definition fields. Obtain the assignment-relevant
enabled, effective, non-summary evidence from the resolved ledger value set;
those definition fields are neither assignment inputs nor assignment-import
columns.

Treat Company Value, StartDate, and EndDate as active-request inputs. Do not
reuse them from an earlier conversation, a prior project run record, an export
row, or another ledger's assignment. If the active request supplies LedgerName
but no Company Value, the only permitted outcome is the read-only preview
described below; do not validate, duplicate-check, package, or import any
previously seen value.

If the active request supplies a Company Value but no LedgerName, ask for the
exact target ledger and stop. Do not look up the value across arbitrary value
sets, assess assignment eligibility, or prepare an import until the ledger is
known and its balancing value set has been resolved.

1. Resolve exactly one ledger through the documented `ledgersLOV` lookup and
   retain its numeric `LedgerId`; do not use the display ledger name as scope.
   If it resolves as `SECONDARY`, ask the user for the exact owning primary
   ledger name and stop. The supported task export is primary-scoped: do not
   submit the secondary ledger ID as `PRIMARY_LEDGER_ID`, guess the owner, or
   use an unscoped export. After the user supplies the primary, resolve and
   verify that primary and use its numeric ID for the scope.
2. Validate the task-local `resolve_primary_ledger_export_scope` contract for
   each of the two requests. Each request must contain its own exact task code
   at the root, in its sole `SetupTaskCSVExportCriteria` item, and in its
   `SetupTaskCSVExportProcess` item. Both criteria must be
   `GL_PRIMARY_LEDGER` / `Set1` / `PRIMARY_LEDGER_ID` with the same verified
   numeric primary LedgerId.
3. Before submission, choose and create verified, writable absolute project
   artifact paths for both responses. Submit both independent read-only requests
   concurrently once their request shapes are validated, then retain and verify
   each returned ProcessId before invoking either result helper. Submit requests only through
   `core.fusion-api.rest-api-client` to the task CSV export REST resource, and
   These are task-specific read-only baseline routes, automatically authorized
   by a preview or assignment request; do not request approval for either
   export. They do not modify the shared export framework or create an
   alternate exporter.
4. Use the existing task-level export result helper with each returned task
   code and ProcessId to poll and download the existing processes. If local artifact
   handling fails after process creation but the ProcessId was retained,
   retrieve that same process with an explicit safe output path. If a successful
   process exposes an empty result-item collection, do not conclude that no
   package exists: use the retained ProcessId to retrieve and validate its
   `FileContent` enclosure through that helper before reporting an export
   blocker, reading a process log, or posting a replacement export. Only an
   unavailable or invalid `FileContent` result, followed by diagnostic process
   log retrieval, is an export-result blocker. Persist a retrieval receipt for
   that helper run: ProcessId, FileContent attempt outcome, safe output path,
   and ZIP member inventory when bytes are returned. Do not state that
   `FileContent` is unavailable, or disclose an export-result blocker, without
   that receipt; an empty result-item collection is never sufficient evidence.
   If a successful
   export response cannot be persisted and its ProcessId cannot be recovered,
   one replacement export with the identical, validated ledger scope is
   permitted because the operation is read-only. Persist and verify that retry's
   ProcessId before continuing; if it too cannot be retained, stop as an
   artifact-persistence blocker. Do not make an unscoped replacement export or
   retry repeatedly.
5. Confirm each manifest scope. Require
   `GL_LEDGER_SEG_VAL_ASSIGNMENT.csv` from this task export for direct-ledger
   assignment status, and current legal-entity assignment evidence from the
   legal-entities task export before determining direct-ledger eligibility,
   showing a preview, or creating an import package. A declared export size
   limit or missing assignment evidence is incomplete evidence, not an empty
   assignment list.

For a primary-ledger scope, related secondary-ledger assignments returned by
the assignment CSV are valid output evidence. Do not add an unsupported
secondary-ledger scope criterion merely to request those rows.

## Ledger-Only Company Value Preview

When LedgerName is present and Company Value is absent, resolve the ledger and
obtain both scoped exports using the route above. Return every enabled, effective,
non-summary Company Value in the resolved balancing value set, with Value,
Description, and value effective dates. Present exactly two clear tables:

1. **Eligible for direct ledger assignment**: values with no direct ledger
   assignment in any period and no legal-entity assignment. These are the only
   values offered for selection.
2. **Existing or blocked values**: every other value, with direct-ledger
   assignment period or periods (including past, current, future, and
   open-ended periods), legal-entity assignment state, and the reason it is not
   offered as a normal direct-ledger selection. A non-overlapping-date option,
   when applicable to an existing direct assignment, must be stated separately
   rather than mixing it into the eligible list.

Do not use a date-relative label such as "not assigned today". A value assigned
to a legal entity remains visible but must be marked `Not eligible for direct
ledger assignment — assigned to legal entity`. Clearly distinguish values whose
assignment state cannot be established because either scoped export is incomplete.
End at the preview result and wait for the user to select one exact Company
Value; never choose one from prior state or infer dates.

## Assignment Inputs

After the user selects or supplies a Company Value and the exact LedgerName is
known, validate that value against that ledger's resolved balancing value set
and the paired current direct-ledger and legal-entity assignment evidence.
StartDate and EndDate are optional: omit either only when the user intends an
open-ended effective period, and validate any supplied date range before package
generation. A value assigned to a legal entity is not eligible for a direct
ledger assignment. Existing direct-ledger assignments are per-Company-Value and
per-effective-period facts, not a ledger-wide blocker.

`BalSegValueOptionCode=A` in the current scoped export is a valid starting
state for a direct specific-value assignment. Do not block preview, package
generation, or import solely because the source value is `A`. Preserve the
exported parent-ledger metadata: the Fusion task performs any required option
transition as part of the assignment. Do not add a manual `A`-to-`I` parent-row
change merely to make a direct assignment eligible.

## Pre-Import Package Controls

Treat a scoped export as a source of current evidence and package structure,
not as an automatically import-safe payload. Before generating an import ZIP:

1. Inspect every populated CSV member. Do not carry forward unrelated ledger,
   legal-entity, journal-configuration, or other setup rows merely because they
   appeared in the export. Any populated row can cause Fusion to validate or
   update that object during import.
2. Preserve the exported ZIP member names, metadata, and order, but include
   data rows only for the requested assignment and its required parent chain.
   For a direct ledger assignment, retain the exact matching `GL_LEDGER` and
   `GL_SECONDARY_LEDGER` parent rows needed by the assignment row; do not omit
   those parents or add unrelated parent rows.
3. Before every direct balancing-segment assignment import, confirm the target
   ledger has a retained-earnings account configured. Check only its presence
   in the target ledger configuration; do not require the user to confirm its
   other account attributes. If this prerequisite changes, obtain a fresh scoped
   export and rebuild the package from that evidence.
4. Validate the final ZIP's member order, CSV headers, parent keys, row counts,
   effective dates, archive safety, and SHA-256 before seeking import approval.
   Parse every changed CSV member with a CSV parser and require the exact
   export-derived header, physical records, and field count; literal escape text
   is data rather than a record boundary. Reject absolute or traversal paths,
   duplicate member names, and unexpected executable content. A changed ZIP,
   baseline, mapping, or prerequisite requires a new validation and approval.

## Data Loader Submission and Recovery

After the final standalone approval, invoke the existing `core.data-loader`
adapter once with an outer command budget of at least 300 seconds. If the
execution host yields, continue waiting on the same invocation in intervals no
longer than 60 seconds; do not terminate, replay, or start another upload merely
because a wrapper response has not yet returned.

Before submission, persist a recovery anchor containing a ZIP basename unique to
this approved attempt, the exact immutable DataSetName, package SHA-256,
submitted-by identity, task code, environment, and bounded submission start
time; require that basename to be identical to the submitted fileName and
DataSetName, and capture the exact task import-process baseline when the
workflow permits it. Before reporting submission, persist the DataSetName and
every returned server identifier, including UCM Content ID, Data Loader Request
ID, and FSM import ProcessId when provided.

If the approved invocation ends without those identifiers, classify the outcome
as unknown and do not ask the user to supply server-generated IDs. First perform
a read-only exact recovery by DataSetName, submitted-by identity, source type
FSM, task code, and the bounded submission window. If that does not yield
exactly one identity, use the captured exact-task pre-submit baseline to recover
one new FSM import process. Zero or multiple results remain unresolved: preserve
the recovery record, do not resubmit, and reconcile through read-only status and
process-log evidence.

## Post-Import Confirmation

After an FSM import process reports completion, retrieve and read its
underlying process log before reporting a successful assignment. Require a
successful result for the relevant Ledger Segment Value Assignment object, a
positive processed/success count for the intended row, and no errors or
unreviewed warnings affecting that object. A completed process status by itself
is not sufficient evidence of success. Do not require a follow-up FSM export
solely to confirm this import; the completed process and its reviewed log are
the post-import confirmation evidence.




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

Use the parent functional-area skill `erp.financials.general-ledger` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

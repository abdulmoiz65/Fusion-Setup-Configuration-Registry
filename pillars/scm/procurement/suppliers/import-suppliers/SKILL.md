---
skill_id: "scm.procurement.suppliers.import-suppliers"
name: "Import Suppliers"
description: "Prepares and submits Supplier FBDI packages through the registered Supplier Data Loader business object. It validates the current Oracle Supplier Import template and routes the approved immutable package exclusively through core.data-loader."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Suppliers"
functional_area_code: "ORA_EGP_SUPPLIERS"
task_code: "POZ_IMPORT_SUPPLIERS"
task_name: "Import Suppliers"
parent_skill_id: "scm.procurement.suppliers"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "FBDI"
businessObject: "Supplier"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "assisted"
owner_team: "SCM procurement pillar team"
version: "0.1.0"
inputs:
  - "supplier_source_data_or_fbdi_package"
  - "target_environment"
  - "optional_batch_id"
  - "project_context"
  - "execution_approval"
outputs:
  - "supplier_fbdi_package"
  - "package_validation_result"
  - "import_preview"
  - "data_loader_execution_result"
  - "load_status_and_errors"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "scm.procurement.suppliers"
  - "core.data-loader"
uses_core:
  - "core.data-loader"
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
  - "configuration_blueprints"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/import-suppliers/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/import-suppliers/current/"
    versioning_policy: "append-only"
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
  - "Prepares Supplier FBDI packages; local sample deliverables are created only when explicitly requested."
  - "After approval, core.data-loader uploads the approved package and submits the registered Supplier FBDI import to the selected Fusion environment."
  - "The import can create or update Supplier-related records represented by the approved source data; Fusion processing is not automatically reversible."
required_privileges:
  - "Access to the selected Fusion environment through the configured Data Loader connection."
---

# Import Suppliers

## Purpose

Use this skill to prepare, validate, preview, submit, and monitor a Supplier
FBDI import. It is an operational import skill, not an FSM Setup and
Maintenance task. Core Data Loader selects the FBDI registration for the package.

## Supported Operations

This is an **FBDI data-migration import**, not a setup-data export or manual-only
task. Core Data Loader imports FBDI packages; this skill does not extract Fusion
records or prepare REST-business-object workbooks. REST transport does not
change that format or authorize direct REST execution.

For export or REST-format requests, explain the boundary and offer FBDI
preparation/import. Do not silently switch operations, invent mappings, require
a new REST registration for FBDI, or imply an import ran when extraction is
still requested.

Reuse supplied data/packages and help prepare the current target-release Oracle
FBDI template; ask only for missing or ambiguous values. Do not require a ready
CSV from users requesting preparation or substitute REST/DAT sample generation.
Report unavailable templates or registration mismatches as blockers. Preserve
Core validation and live approval; distinguish prepared, submitted, and completed.

## Reuse Supplied Import Inputs

Reuse supplied requirements, answers, files, spreadsheets, CSVs, images, tables,
and text, retaining source references without requiring repetition or
reformatting. Distinguish requested imports from current-state examples and
group only missing, unreadable, conflicting, ambiguous, or unsupported in-scope
inputs into a prompt. Preserve unrequested settings and explicit Preserve
choices; interpret blanks using the entity's import-field semantics, not as
Clear or false.

Reuse source files, mappings, selected entities, batch choices, and explicit
parent-readiness confirmations applicable to the same environment and scope.
Validate against the current template and live registration; correct only
affected rows or fields, retaining valid values. Do not regenerate a package
just to collect its values again.

Ask for prerequisite confirmation only when absent, ambiguous, or no longer
applicable. Task existence, screenshots, and samples do not establish readiness.
Declared checks and approval of the exact immutable package remain mandatory.

## Core Workflow and Approval

Delegate validation, preview, approval, submission, and execution-state handling
to `core.data-loader`. Display Core's final preview verbatim; do not add a
custom approval preview or expose internal hashes there.

Use Core's immutable approved artifact and its required preflight and Task Hook
envelopes for submission. Follow Core's integrity, context verification,
retention, and cleanup rules. Do not rebuild the approved package, reread the
original sources, recreate envelopes, or add Supplier-managed approval
snapshots. A changed or missing approved artifact or approval context requires
fresh Core validation and approval.

Explicitly requested samples and status logs follow Core's separate workflows.
Where project evidence is required, retain only permitted final business
results, such as request IDs, status, counts, and redacted errors. Output
declarations do not authorize separate temporary approval state. Follow Core's
initiation/status reporting and retry rules rather than adding a second
execution workflow.

## FBDI Registration Selection

Delegate registration, UCM account, and adapter selection to Core's
[FBDI identification workflow](../../../../../core/data-loader/SKILL.md),
which matches package filenames to live `fbdiMetadata` prefixes. Do not add
Supplier-side lookups, guess BO spellings, or hardcode registration/adapter IDs.

The manifest's `businessObject` is an optional FBDI hint—not a REST resource,
verified live identity, or exact-name requirement. Do not automatically pass it
as a BO override. For ambiguity, use Core's selection workflow and an exact
returned live candidate covering the requested entity/package. A spelling
difference alone is not a failure when Core resolves the correct contract.
Hints neither bypass metadata validation nor guarantee fewer metadata requests.

Use each skill's expected CSV filenames as package-preparation hints, not BO
names or fixed routing overrides. Confirm them against the current Oracle FBDI
template and Core's live file prefixes. Include companion data only when
applicable; preserve any empty-member requirements of the template. The outer
ZIP filename is separate from its CSV member names.

Before approval, verify that the resolved FBDI contract supports the requested
entity and template members; a name/filename match alone is insufficient.
Block unresolved or conflicting metadata. Do not substitute a REST workbook,
job, account, or direct submission route.

## Registered Data Loader Contract

Use Core's resolved live registration as the execution authority. The expected
Supplier contract below is task-scope reference information, not a BO-name
lookup or a substitute for Core validation:

| Setting | Value |
|---|---|
| Import entity | Supplier |
| FBDI data-file prefix | `PozSuppliersInt` |
| Expected CSV filename | `PozSuppliersInt.csv` |
| UCM account | `prc/supplier/import` |
| Primary interface table | `POZ_SUPPLIERS_INT` |
| Interface request column | `LOAD_REQUEST_ID` |
| Import scope | `BATCH_ID` when supplied |

The registration owns the FBDI job mapping, fixed import arguments, package
upload, submission, polling, and row-level diagnostics. Do not submit the ESS
job, call UCM, or invoke ERP Integrations REST directly from this task.

## Source and Package Preparation

1. Obtain the current Oracle Supplier Import FBDI workbook/control-file
   template for the target release. Treat its active sheet, column sequence,
   required fields, and CSV formatting rules as authoritative; do not invent
   columns or reuse a remembered template layout.
2. Prepare only Supplier import data requested for this run. Preserve the
   template's exact header/order and required control-file conventions.
3. Use a single, nonblank `BATCH_ID` for all rows in a package whenever the
   supplied template includes that column. If the source package intentionally
   has no batch identifier, retain it as blank rather than fabricating one.
4. Create a ZIP containing the current Supplier FBDI data member(s) whose
   names match the registered `PozSuppliersInt` prefix. Reject path traversal,
   duplicate members, unsupported files, and a package with no supplier data.
5. Validate that the package opens, contains the expected members, uses the
   current template layout, and contains the intended rows. Delegate immutable
   artifact preparation, approval integrity, and retention to Core.

Do not add `LOAD_REQUEST_ID`, `REQUEST_ID`, interface status, rejection, or
internal interface identifiers to source data. Fusion/Data Loader assigns and
uses those values after upload.

## Companion Data

Some Supplier import registrations support related or companion data members.
Include companion rows or files only when they are needed for the requested
business outcome and supported by the selected current template. Do not add
empty, unrelated, or speculative companion members merely because the
registration exposes them. When companion data is included, preserve its
template-required parent-child references and validate the complete package
against the live registration before approval.

## Entity Dependency Guidance

Treat a successfully processed Supplier as the root of the Supplier Model
import hierarchy. For a dependent-entity submission, reuse an applicable
explicit confirmation that its referenced parent has already been processed
in Fusion; ask only if that confirmation is missing or unclear. Do not require
the parent skill to have run in the current runbook when that prerequisite is
already satisfied.

```text
Supplier
├─ Address → Site → Site Assignment
├─ Contact → Contact Address
├─ Business Classification
└─ Products and Services Category
```

- Import an Address only after its Supplier exists.
- Import a Site only after its Supplier and referenced Address exist.
- Import a Site Assignment only after its Supplier Site exists.
- Import a Contact only after its Supplier exists. A Contact Address requires
  the related Supplier Address and a contact that is created in the same load
  or already exists.
- Import Business Classifications and Products and Services Categories only
  after their Supplier exists. They can run in parallel after that point.
- `PROSPECTIVE` suppliers support Supplier-level dependent data such as
  Addresses, Contacts, Business Classifications, and Products and Services
  Categories. They cannot have Supplier Sites or Supplier Site Assignments.
- Use `SPEND_AUTHORIZED` for a Supplier that requires Sites or Site
  Assignments. Business relationship cannot be changed through Supplier import.
- Attachments are outside the default dependency sequence. When explicitly in
  scope, their referenced Supplier, Site, or Business Classification must
  already exist.

## Run Book Child-Task Provisioning

When the user explicitly requests `Import Suppliers` execution with child
tasks, use the existing `core.runbook` ad hoc-task workflow to add only the
applicable manual task or tasks: Supplier Addresses, Supplier Sites, Supplier
Site Assignments, Supplier Contacts, Supplier Business Classifications,
Supplier Products and Services Categories, or Supplier Attachments. The
catalog-backed `Import Suppliers` task remains the governing Data Loader task.
Do not automatically add every child task, or add separate child tasks for
template acquisition, sample generation, validation-only, or preview-only work.

Each manual task links to its corresponding child skill and acts as a
dependency-controlled operational checklist. A child skill can run
independently when its parent entities are already processed; verify those
prerequisites rather than treating task existence as proof of import success.

## Child-Task Guidance at Execution

When the user starts `Import Suppliers`, keep the initial response focused on
the requested Supplier import. First inspect the active runbook. If it already
contains one or more Supplier import child tasks, acknowledge the selected
tasks and do not offer them again. If no child-task scope has been established
and dependent supplier data may also be needed, ask once:

> Do you also need to import Supplier Addresses, Sites, Site Assignments,
> Contacts (including Contact Addresses), Business Classifications, Products
> and Services Categories, or Attachments?

Add a child task only for each entity the user selects and that is not already
in the active runbook. Briefly state the relevant prerequisite before execution
and reuse an applicable confirmation that it is already available in Fusion,
asking only when missing or unclear; do not require a
prior child task to have run. Do not offer or add child tasks when the request
is limited to package preparation, validation, preview, or a Supplier-only
import.

## Mandatory Execution Route

1. Run preflight before any Fusion-changing action: validate the target
   environment identity, Data Loader session and access, source/ZIP shape,
   optional batch scope, and whether the operation is preview or live. Stop
   before preview when input is ambiguous or the ZIP fails validation.
2. Resolve the requested supplier outcome, source data, and any retry identity
   before creating an execution preview.
3. Let `core.data-loader` identify the FBDI registration from the prepared ZIP
   and live metadata, then validate the package and requested Supplier scope
   against the resolved contract.
4. Let Data Loader derive the optional `BATCH_ID` scope from the package and
   apply its registered Supplier import arguments. Do not override argument
   positions or hardcode Data Loader identifiers in the package.
5. Follow [Core workflow and approval](#core-workflow-and-approval) for the final
   preview and approval. Submit the retained package through Core's approved-artifact workflow;
   changed data or target requires fresh Core validation and approval.
6. When status is requested, monitor through Data Loader. Interpret `PROCESSED` as successful,
   `REJECTED` as an error, and every other or null status as pending. Surface
   rejection code, attribute, supplied value, and supplier reference from the
   registered diagnostics.

## Retry and Recovery

- A rejected or uncertain submission must be reconciled through Data Loader
  before any retry. Never resubmit merely because a request identifier was not
  immediately returned.
- Correct only the rejected source rows, assign a new batch identifier when
  business traceability requires it, rebuild the ZIP, and obtain a replacement
  approval before retrying.
- Do not mutate Fusion interface tables or rejection tables directly.

## Failure Handling and Diagnostics

- Classify invalid source data, ZIP structure, or missing business input as
  `input_validation`; do not submit or retry until it is corrected.
- Classify a missing/changed Data Loader contract as
  `catalog_or_metadata_mismatch`, and stop rather than guessing a job mapping
  or interface table.
- For authentication, authorization, transport, or Fusion failures, retain the
  redacted Data Loader diagnostic and its request identifier when present;
  retry only read-only authentication/transport recovery within bounded
  attempts. A live import is never retried without explicit approval for the
  exact replacement package.
- On a monitoring timeout, preserve the last status and request identifier,
  stop polling, and ask whether to resume monitoring; do not resubmit the ZIP.
- Keep project evidence within the [Core workflow rules](#core-workflow-and-approval).
  Never persist or display credentials, tokens, token caches, private
  keys, full source rows, or full package/base64 content.

## Communication

Report the business result first: records prepared, target environment, batch
scope, import state, and actionable rejected rows. Keep file paths, command
details, and implementation mechanics concise unless requested. Ask for
approval only for the live import, after all safe preparation and validation
are complete.

---
skill_id: "erp.financials.customer-billing.manage-remit-to-addresses"
name: "Manage Remit to Addresses Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Remit to Addresses under the Customer Billing functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Customer Billing"
functional_area_code: "ORA_FIN_CUST_BILL"
task_code: "AR_MANAGE_REMIT_TO_ADDRESSES"
task_name: "Manage Remit to Addresses"
parent_skill_id: "erp.financials.customer-billing"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP financials pillar team"
version: "0.1.0"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-billing/manage-remit-to-addresses/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/customer-billing/manage-remit-to-addresses/current/"
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

# Manage Remit to Addresses Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Remit to Addresses` under `Customer Billing`.

## Setup Task Skill Contract

- task_code: `AR_MANAGE_REMIT_TO_ADDRESSES`
- task_name: `Manage Remit to Addresses`
- parent_skill_id: `erp.financials.customer-billing`
- pillar: `ERP`
- offering: `Financials`
- functional_area: `Customer Billing`
- functional_area_code: `ORA_FIN_CUST_BILL`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Remit to Addresses` under `Customer Billing`.

## Setup Task Metadata

- Task name: `Manage Remit to Addresses`
- Task code: `AR_MANAGE_REMIT_TO_ADDRESSES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Financials`
- Functional area / Setup Object: `Customer Billing`
- Setup task name: `Manage Remit to Addresses`
- Setup task code: `AR_MANAGE_REMIT_TO_ADDRESSES`




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

Use the parent functional-area skill `erp.financials.customer-billing` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Product Contract and Readiness

This source-reviewed contract models creation of remit-to locations and
their receipt-from criteria, plus exact-key criteria Status updates (A/I only).
Read [the lifecycle contract](references/lifecycle-contract.md) for operation
boundaries, source evidence, no-op handling and reverse-update constraints.
Exact FSM transport identity, parent dependencies,
deterministic packaging and reconciliation are implemented. Target-specific
country/address validation is performed by the normal FSM import; local checks
and post-import verification remain mandatory. Read
[the postal validation contract](references/postal-validation-contract.md)
for the separation and its limitations.
Readiness is determined by the compiled registry
and adapter, not by the presence of this skill.

<!-- fscr-supported-operations: create, update -->
<!-- fscr-update-fields: AR_REMIT_TO_ADDRESS::Status -->
<!-- fscr-create-fields: AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.Address1, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.City, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.OrigSystemReference, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.PostalCode, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.SetCode, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.State, AR_REMIT_TO_ADDRESS::AR_REMIT_TO_LOCATION.TerritoryCode, AR_REMIT_TO_ADDRESS::Country, AR_REMIT_TO_ADDRESS::PostalCodeHigh, AR_REMIT_TO_ADDRESS::PostalCodeLow, AR_REMIT_TO_ADDRESS::SetCode, AR_REMIT_TO_ADDRESS::State, AR_REMIT_TO_ADDRESS::Status, AR_REMIT_TO_LOCATION::AddrElementAttribute2, AR_REMIT_TO_LOCATION::AddrElementAttribute3, AR_REMIT_TO_LOCATION::Address1, AR_REMIT_TO_LOCATION::Address2, AR_REMIT_TO_LOCATION::Address3, AR_REMIT_TO_LOCATION::Address4, AR_REMIT_TO_LOCATION::City, AR_REMIT_TO_LOCATION::County, AR_REMIT_TO_LOCATION::OrigSystemReference, AR_REMIT_TO_LOCATION::PostalCode, AR_REMIT_TO_LOCATION::Province, AR_REMIT_TO_LOCATION::SetCode, AR_REMIT_TO_LOCATION::State, AR_REMIT_TO_LOCATION::TerritoryCode -->

An absent allowlist entry is not proof that Fusion prohibits that field.
Updates outside the exact criteria Status A/I contract, explicit clearing,
end-dating and task-CSV deletion are not implemented in this version.
Retain those requests, explain the specific evidence gap and ask
about intended business outcome; do not silently convert an update into create
or claim the operation is impossible in Fusion. A user answer cannot supply
missing product semantics. Route a remaining implementation gap to the owning
developer with its source conflict and resume context.

## Rule Read Order

Use the release-visible `core.data-loader.task-hook` data-load route and
`core/data-loader/references/task-rule-registry-execution.md`. After Task Hook
selects `AR_MANAGE_REMIT_TO_ADDRESSES`, use its returned execution guide and
this task's `ora-resource/ora_rule_registry.json`. Begin at `start_node`,
verify readiness, prerequisites and applicability for every reached node,
read its declared source anchor, record the declared outcome, and follow only
the corresponding registry transition. Read all reached source sections in:

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_reference_lookups.md`
3. `ora-resource/ora_dependency_readiness.md`
4. `ora-resource/ora_defaulting_rules.md`
5. `ora-resource/ora_design_enforcement.md`
6. `ora-resource/ora_error_handling.md`

Do not manufacture readiness or skip a reachable incomplete node. A registry
readiness override does not supply a missing key, resolver, field contract or
permission to mutate.

## Business Intake and Clarification

Bulk is a request size, not a separate Fusion operation. Accept multiple new
locations, new coverage rules and exact-key criteria Status updates in one
design. Derive parent references, validate all rows before writing a ZIP, and
reconcile every row afterward. Do not promise transaction-level atomicity.

For mixed create/update/delete/end-date input, retain every requested row and
its operation; never drop an unresolved row to generate the supported subset.
The adapter returns NEEDS_OPERATION_RESOLUTION with row-specific questions and
evidence gaps for all unimplemented operations in the batch. Ask only questions
not already answered in the request, retain answers, and re-run normalization
with the complete revised design. Distinguish business ambiguity from a missing
product contract: a developer must resolve the latter, not the customer through
repeated questions. This disposition is not an executable mixed-operation ZIP.

For retirement requests distinguish deletion of a location, removal of a
receipt-from rule, immediate inactivation and a future end date. Do not equate
them. RemitToUIAMImpl.deleteReceiptsFromCriteria removes a UI row, while the
reviewed FSM CSV has no end-date field and Oracle documents that CSV import
does not delete existing records. Immediate A/I criteria status updates are
supported separately; D is not an authorized deletion mechanism. Postal
fields mapped through LocationPEO are read-only in the migration VO; changing
lookup fields can resolve a different location instead of updating the old one.
Do not enable those ZIP operations merely by editing supportedOperations.

Accept ordinary language, business workbooks and tables. The business user need
not know task codes, CSV headers, internal IDs, authentication or import steps.
Extract only this task's requirements; route unrelated tasks through the parent
and Implementation Router. Keep each input row traceable to its source and
preserve exact spelling, postal leading zeros and customer references.

Separate the postal destination (where payment is sent) from receipt-from
criteria (which customer bill-to addresses use it). Ask concise business-language
questions for missing or ambiguous scope and coverage. For example: “Which
reference data set should own this remit-to address?” or “Should this address
apply to every customer in that country, or only particular states/postal areas?”
Ask further questions if the answer remains ambiguous; do not pick the first
match. Retain answered facts rather than restarting intake.

Treat every business request as standalone for identity resolution. Do not use
a preceding conversation, an earlier campaign row, or ordering words such as
"same", "above", "those", "it", or "the existing address" as evidence of a
reference-data set, remit-to destination, or receipt-from criterion. Continue
only when the current request or its explicitly attached business input names
the exact set and enough destination/coverage attributes to resolve one current
exported identity. Otherwise ask one concise business-language question and
generate no candidate. Prior answers may be retained only when they are part of
the same unresolved intake and are restated in the consolidated design shown
for confirmation.

Resolve existing identity before choosing create/update. A create collision is
not permission to update. An update with equivalent values is a no-op, not a
reason to import again. A multi-row or mixed request gets one complete design
and all-or-nothing preflight; no partial package while any requested operation
is unresolved. This does not promise transactional rollback inside Fusion.

Receipt-from transport identity includes the parent, but business uniqueness
does not: within one reference set, an exact country/state/postal-low/postal-high
combination cannot be created under another destination. Check all exported
criteria and every proposed child in the batch, including Inactive rows. Ask
which different coverage is intended or whether the existing coverage should
change; never choose another postal code, infer a reassignment, or inactivate
the old row to bypass this constraint. See
[coverage uniqueness](references/coverage-uniqueness.md).

## Preparation, Handoff and Verification

Use FSM export/import only for this task's Fusion data access. Obtain evidence
through `shared.setup-export.task-level-export` and submit approved candidates
through `core.data-loader` in FSM mode. Do not introduce SOAP, direct entity REST
lookups/writes, database access, or a task-local network client. Existing central
authentication, transport, process monitoring and download mechanisms used by
the FSM route remain unchanged.

Use exported evidence for local preflight and the reviewed FSM import service
for its source-backed resolution and application validation. Absence of a SOAP
or direct lookup API is not a prerequisite failure. Task-export absence does not
prove absence from shared postal locations; do not infer global uniqueness or
claim that import will create rather than reuse a shared location. This routing
choice does not override known identity conflicts or enable an incomplete rule node.
Do not demand a global HZ dump before an ordinary remit-to create. The adapter
binds pending application validation to each new parent's immutable blueprint;
that disclosure is not an override, prior success or an approval.
Verify the requested postal values and receipt-from criteria with a fresh FSM
export after processing; a successful process alone does not prove correctness.

Use the active project and authorized environment from FSCR orchestration. Never
embed a sandbox, a business set, a country, a username or a laptop path here.
Use fresh exact-task current data and a compatible genuine task template from
the shared export route. Validate metadata, successful status, task selection,
release compatibility, exact headers and every CSV row width before normalization.
The archive's ObjectShortName is not a REST Data Loader businessObject.

Current-data and verification exports may assign a different permutation of
NodeSequence values to the same exact BO paths than template exports. Validate
positive, unique values against the task's sequence set without treating that
permutation as a schema change. Keep template checks strict and preserve the
fresh baseline metadata byte-for-byte in candidates; never rewrite sequences
to make a candidate pass validation.

When the adapter capabilities and rule plan are ready, use the task-local
`scripts/fsm_task_adapter.py` seven-command protocol: manifest, normalize, build,
validate, determinism, rollback and reconcile. It is an offline helper, not the
user-facing entrypoint or a Fusion writer. Honor its explicit capability blockers.
Never copy IDs, audit values or a schema from another FSM task to bypass them.

The registered parent/criteria extension in `scripts/remit_identity.py` checks
the seven parent-reference columns, nullable reference components, orphaned or
duplicate criteria, and parent/child set consistency. Every adapter package read
runs those checks. The manifest also rejects unsuccessful process statuses,
environment relabeling and populated packages presented as templates. This
extension derives child references, includes unchanged parent dependency rows,
rejects known create collisions and reconciles service-generated external
references only when one exact persisted match exists. It does not establish
global shared-location uniqueness. Requested postal values are independently
compared after import, including values the reuse branch may ignore.

Show a consolidated business design including exact set, postal destination,
coverage, explicit defaults, operation, preserved values and unresolved items.
Do not generate a candidate until applicable rules are satisfied. Independently
validate the exact candidate and its SHA-256. Production execution remains owned
by the Run Book and `core.data-loader` in FSM mode, with that owner's current
approval policy; this task does not add a competing import approval controller.
Never issue direct REST writes or database updates to AR or HZ tables.

Capture the import request/process, final result, counts, warnings and diagnostics.
Upload acceptance is not success. An uncertain or failed process requires a
fresh read-only export before considering retry because partial persistence is
possible. Reconcile the exact submitted design against the fresh export: every
requested location and child criterion, preserved baseline rows, duplicates and
unexpected target changes. Unrelated concurrently created rows alone are not a
failure. Never report completion until persisted-state verification succeeds.

## Source-Backed Task Behavior

- The task has a remit-to location parent and receipt-from criteria children;
  postal destination and customer bill-to coverage are different business facts.
  Sources: SRC-REMIT-FSM-BO, SRC-REMIT-LOCATION-VO, SRC-REMIT-CRITERIA-VO.
- Seven template-derived parent-reference columns connect each exported child
  to its parent. Blank state, city or postal components are valid exported
  reference components, not permission to invent replacement identifiers.
  Sources: exact task template, SRC-REMIT-CRITERIA-EO AltCriteria.
- The import hook resolves SetCode and searches shared postal locations using
  nonempty Address1, OrigSystemReference, TerritoryCode, PostalCode, State and
  City inputs. It requests the first result, not proof of uniqueness; SetCode
  and Address2 are not search discriminators in that hook.
  Sources: SRC-REMIT-AM-IMPL, SRC-REMIT-LOCATION-LOOKUP.
- When the hook reuses a location, it does not apply the extra postal values
  copied on the new-location branch. A requested address change must not be
  reported as persisted merely because a package was accepted.
  Sources: SRC-REMIT-AM-IMPL, SRC-REMIT-LOCATION-VO.
- When creating a shared location, the hook can derive an omitted external
  reference from the created location identifier. Never manufacture that
  identifier or assume the unchanged candidate key will appear in the export.
  Source: SRC-REMIT-AM-IMPL.
- Active criteria creation has a source-reviewed UI default of A. Existing
  criteria can request A (Active) or I (Inactive) through the Status-only update
  contract. Neither is a future end date or physical deletion.
  Sources: SRC-REMIT-UI-STATUS, SRC-REMIT-CRITERIA-EO,
  SRC-REMIT-CODE-STATUS, SRC-REMIT-MIGRATION-UPDATE-TEST.
- Audit values are service-owned. Preserve them only as baseline evidence and
  leave them blank in any future generated import candidate.
  Sources: SRC-REMIT-LOCATION-VO, SRC-REMIT-CRITERIA-VO.
- Import can commit accepted work before returning collected recoverable row
  errors. After an uncertain or failed import, obtain a fresh FSM export before
  considering a retry; all-or-nothing preflight is not a transactional guarantee.
  Source: SRC-REMIT-AM-IMPL importData.

## Evidence Boundary

For release review or test-coverage questions, read
[release scope and coverage dispositions](references/release-scope-and-coverage.md)
and its per-variant machine-readable register. They distinguish supported
operations, executed unit tests, historical live evidence and unexecuted catalog
variants. Broad manifest applicability is not certification of every country,
release or scenario. Do not present disposition completeness as test completion.

Rules cite reviewed source identities and component names in their owning tables.
Source review used FPHDEV; that is not proof of a target's installed patch level.
The latest reviewed public reference is the Oracle 26C Implementing Receivables
Credit to Cash guide, remit-to addresses chapter. At runtime prefer documented
behavior matching the target's actual release; keep public and implementation
evidence distinct. Screenshots and existing export values are not universal
defaults, exhaustive reference lists or proof of supported update behavior.

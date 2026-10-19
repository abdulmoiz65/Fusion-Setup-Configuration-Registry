---
skill_id: "hcm.global-human-resources.person-record.manage-person-types"
name: "Manage Person Types Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Person Types under the Person Record functional area. Use when the user asks to plan, validate, or execute this task's declared scope; do not use it for unrelated HCM configuration."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Person Record"
functional_area_code: "ORA_PERSON_RECORD"
task_code: "PER_MANAGE_PERSON_TYPES"
task_name: "Manage Person Types"
parent_skill_id: "hcm.global-human-resources.person-record"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "PersonType"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
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
  - "operation_verification"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "hcm.global-human-resources.global-human-resources-common.manage-common-lookups"
  - "hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.fusion-api.rest-api-client"
oracle_supplied_guidance_files:
  - purpose: "Input validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Reference resolution"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Defaulting rules"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Design enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Failure handling"
    location: "ora-resource/ora_error_handling.md"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/person-record/manage-person-types/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/person-record/manage-person-types/current/"
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

# Manage Person Types Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Person Types` under `Person Record`.

## Task Overview

Use this task to plan and govern `Manage Person Types` configuration in Global Human Resources.

- **Task identity:** `PER_MANAGE_PERSON_TYPES` — Manage Person Types.
- **Scope:** HCM → Global Human Resources → Person Record.
- **Catalog routing:** CSV export/import support is `Y`; the declared Data Loader mode is `REST` with `PersonType`.
- **Read next:** [task contract](#setup-task-skill-contract) and [usage](#usage). Follow the task-specific routing, approvals, and restrictions in the detailed sections below.

## Setup Task Skill Contract
- task_code: `PER_MANAGE_PERSON_TYPES`
- task_name: `Manage Person Types`
- parent_skill_id: `hcm.global-human-resources.person-record`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Person Record`
- functional_area_code: `ORA_PERSON_RECORD`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `PersonType`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Person Types` under `Person Record`.

## Setup Task Metadata

- Task name: `Manage Person Types`
- Task code: `PER_MANAGE_PERSON_TYPES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `PersonType`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `PersonType` as the BusinessObject.

## CRUD and Reference Routing

- Resolve a supplied System Person Type through `SYSTEM_PERSON_TYPE`, then read `personTypes` using the returned `SystemPersonType` code. Match user type names against `UserPersonType`; for an explicit contains search by system code, use `q=SystemPersonType like '%term%'`. Do not derive a system code from its meaning.
- For a read, complete every applicable resolver and return the final result in the same turn; do not pause at an intermediate lookup.
- Route lookup resolution to [Global Human Resources Common > Manage Common Lookups](../../global-human-resources-common/manage-common-lookups/SKILL.md).
- Route profile option value resolution to [Global Human Resources Common > Manage Administrator Profile Values](../../global-human-resources-common/manage-administrator-profile-values/SKILL.md).
- For create, edit, or delete, run every applicable declared read and task rule in graph order. When the graph returns `PT.LOADER_READY`, invoke `core.data-loader` with the task metadata, project context, `PersonType`, operation, and resolved business values. For a document-specified mutation batch, use the single-DAT contract below instead of preparing one loader artifact per item. Keep control until Core returns the immutable ZIP preview; do not pause at an intermediate step. Then wait for standalone `approve`; ask only for unresolved business input. After that approval, continue in the same turn through Core's archive verification, upload/initiation, load monitoring, and this task's post-operation verification. Approval recording alone is not a completed Person Type operation.
- Before preparing a task-routed XLSX source for an edit, run Core Data Loader's `scripts/check_artifact_xlsx_runtime.py`. If it succeeds, use its verified bundled runtime even when a session dependency-loader capability is not exposed. Do not declare a runtime blocker solely because that host capability is absent, and do not reuse a workbook whose business key or `PersonTypeId` is stale.
- Do not issue mutating Fusion REST calls.
- Treat `SystemPersonType` plus `UserPersonType` as the business key. The same user-person-type name may be created under different resolved system-person-type codes; block only an exact duplicate pair. Resolve Yes/No to the stored `ActiveFlag` value and show the reviewed source and resulting immutable ZIP in the same approval preview.
- For a delete, prepare a PersonType DAT source whose root data row begins `DELETE|PersonType|` and contains the exact resolved paired business key. Do not add or require a `RestAction` column for this task. Validate the exact DAT and its ZIP through Core Data Loader, then obtain approval before submission. This rule is specific to PersonType deletion; do not apply it to other business objects without their declared contract.

## Post-operation verification

**Completion rule:** Never report a Person Type create, edit, rename, or delete as successful from an upload or initiation response. Report it as `pending confirmation` until this section's terminal load check and exact business-key reconciliation both pass.

## Multi-operation Continuation Contract

When one user request contains an ordered series of Person Type operations, retain that series as the active task queue. For mutations specified in the same supplied file, prepare one ordered `PersonType.dat` source with one `METADATA|PersonType|...` header and all mutation rows in document order, then validate it into one immutable ZIP and submit it as one Data Loader request after one standalone approval. Do not create separate DAT files, ZIPs, approvals, or uploads for individual items in that same batch. Requested reads are not DAT rows; execute them after the batch reaches a terminal status and the batch reconciliation is complete.

Before building the batch DAT, resolve every affected current business key and all supplied lookup values. Include `MERGE|PersonType|...` rows for supported create or edit mutations and `DELETE|PersonType|...` rows for deletes, with every row using the exact live schema and required current-run identity. The approval preview must enumerate every row's ordered operation, business key, values or deletion target, the resulting DAT, and the single ZIP SHA-256.

Use the single-DAT contract only when all rows can be fully resolved before source generation. A later row that needs an ID, generated value, or other state produced by an earlier row cannot safely be represented unless Fusion's current loader contract provides an already-resolved stable key for that row. Stop as an input-validation blocker rather than inventing an identifier, reusing a stale ID, or silently splitting the requested batch.

**Mandatory rule for document-specified queues:** When the user directs execution of all operations in a supplied file, continue the complete ordered queue without an intermediate final response. Do not stop after any individual operation, including after a submitted load, a nonterminal status, or a confirmed result. Continue until the full queue is complete unless the user explicitly directs a stop, replacement, cancellation, or reprioritization. A required standalone approval is a temporary approval gate, not the end of the queue; resume automatically after approval. A terminal failure, timeout, verification failure, or another declared blocker remains the only non-user stop condition.

For each document-specified mutation batch:

1. Prepare and validate the one immutable Data Loader artifact, then pause only for its required standalone `approve` message.
2. After approval, submit the exact artifact once, monitor the resulting load until it reaches a terminal status, and reconcile every affected business key against the ordered batch's expected final state.
3. If the first nonterminal status is returned, continue monitoring for up to one minute before reporting that confirmation is taking longer; do not treat that first status as a workflow endpoint.
4. On confirmed success, immediately execute any queued read in the same turn. Do not exit between batch completion and that read.
5. On a terminal failure, verification failure, timeout, or approval blocker, stop with the applicable diagnostic and preserve the uncompleted queue; do not skip, reorder, or split the batch.

Return a final completion response only after the batch has reached its declared terminal outcome and the final requested read has been completed. Approval gates remain mandatory and are the only normal user-interaction pause for the batch.

After `core.data-loader` accepts a create, edit, or delete request, confirm the result before reporting it as successful or failed.

1. Use the accepted request ID to wait for a terminal data-load result under the Core Data Loader monitoring contract. A failed data load is an operation failure; do not retry the load automatically.
2. For a successful data load, query the exact `personTypes` business key using both the resolved `SystemPersonType` and the affected `UserPersonType`. Use the declared Core REST client and request only the fields needed to evaluate the operation.
3. Confirm success only when the observed state matches the approved operation or the ordered batch's expected final state: create or edit requires exactly one matching record with every reviewed changed value; delete requires no matching record. For a rename, query the new pair and also confirm the old pair is absent. Do not claim an intermediate state that the batch intentionally superseded; reconcile the final state for that business key.
4. If the data load is terminal but the queried state does not match, report **verification failed**, including the intended versus observed business state. If the data load has not reached a terminal state by the monitoring timeout, report **not yet confirmed**, not failure. Do not retry, mutate through REST, or infer a result from the initiation response.
5. Persist the request ID, exact query key, terminal load status, expected state, observed state, verification outcome, and any diagnostic reference under the task's project workspace. Never persist credentials or access tokens.

Use this task metadata when invoking those skills:

- Offering: `Global Human Resources`
- Functional area / Setup Object: `Person Record`
- Setup task name: `Manage Person Types`
- Setup task code: `PER_MANAGE_PERSON_TYPES`




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

Use the parent functional-area skill `hcm.global-human-resources.person-record` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Resource References

- [Input validation](ora-resource/ora_input_validation.md)
- [Dependency readiness](ora-resource/ora_dependency_readiness.md)
- [Reference lookups](ora-resource/ora_reference_lookups.md)
- [Defaulting rules](ora-resource/ora_defaulting_rules.md)
- [Design enforcement](ora-resource/ora_design_enforcement.md)
- [Error handling](ora-resource/ora_error_handling.md)

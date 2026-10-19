---
skill_id: "scm.product-management.index-management.manage-product-management-indexes"
name: "Manage Product Management Indexes Setup Task Guidance"
description: "Validates and processes one Product Management index per invocation, applies its attribute delta through approved Data Loader execution, and submits its separately approved rebuild."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "Index Management"
functional_area_code: "CUSTOM_INDEX_MANAGEMENT"
task_code: "CUSTOM_EGP_MANAGE_PM_INDEXES"
task_name: "Manage Product Management Indexes"
parent_skill_id: "scm.product-management.index-management"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "productManagementESIndexedAttributes"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "SCM product management pillar team"
version: "0.4.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "canonical_index_name"
  - "single_index_request"
  - "attributes_to_add"
  - "attributes_to_remove"
  - "index_rebuild_requested"
  - "index_rebuild_skip_confirmation"
  - "ess_execution_options"
  - "data_loader_status_check_requested"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "seeded_indexed_attributes"
  - "index_attribute_delta"
  - "index_scope_validation_result"
  - "index_rebuild_ess_payload"
  - "index_rebuild_decision"
  - "index_rebuild_ess_submission_result"
  - "data_loader_submission_followup"
  - "data_loader_status_result"
  - "index_execution_state"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.data-loader"
  - "core.fusion-api.ess-job-submitter"
uses_core:
  - "core.data-loader"
  - "core.fusion-api.ess-job-submitter"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/index-management/manage-product-management-indexes/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/index-management/manage-product-management-indexes/current/"
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
  - "Persists the selected single-index request and its validation evidence under the project workspace; does not create or advance a batch plan."
  - "Persists a single-index continuation state after Data Loader submission, requested status checks, post-load readback, and ESS approval preparation."
  - "Imports an approved immutable productManagementESIndexedAttributes Data Loader artifact through core.data-loader only after the core Data Loader approval gate."
  - "When index rebuild is not explicitly skipped, conditionally submits one Product Management Index Maintenance ESS request through core.fusion-api.ess-job-submitter only after fresh explicit approval of the exact payload; verify Data Loader success first only when an indexed-attribute change was submitted."
required_privileges:
  - "Target-environment OAuth access and privileges to view productManagementESIndexedAttributes metadata and Data Loader data-set status, as preflighted by core.data-loader."
  - "Privileges to upload approved Data Loader content to UCM and initiate the selected productManagementESIndexedAttributes Data Loader operation, as preflighted by core.data-loader."
  - "Fusion privileges appropriate to submit and check the requested Product Management Index Maintenance ESS operation, as preflighted by core.fusion-api.ess-job-submitter."
---

# Manage Product Management Indexes Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Product Management Indexes` under `Index Management`.

## Setup Task Skill Contract

- task_code: `CUSTOM_EGP_MANAGE_PM_INDEXES`
- task_name: `Manage Product Management Indexes`
- parent_skill_id: `scm.product-management.index-management`
- pillar: `SCM`
- offering: `Product Management`
- functional_area: `Index Management`
- functional_area_code: `CUSTOM_INDEX_MANAGEMENT`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `REST`
- businessObject: `productManagementESIndexedAttributes`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Product Management Indexes` under `Index Management`.

## Setup Task Metadata

- Task name: `Manage Product Management Indexes`
- Task code: `CUSTOM_EGP_MANAGE_PM_INDEXES`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `productManagementESIndexedAttributes`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.

## REST Data Loader Import Workflow

`dataloader_import_mode: "REST"` identifies the registered Fusion Data Loader business-object contract; it does not authorize direct mutating REST calls. Route all setup-data mutations for `productManagementESIndexedAttributes` through `core.data-loader`.

1. Confirm the registered business object; canonicalize the supplied index name; obtain seeded indexed attributes; and calculate the addition/removal delta before preparing any row. When the user explicitly requests an index rebuild without an attribute list, calculate the seeded-attribute repair delta before preparing the ESS request. The read-only metadata and available-attributes endpoints are validation sources only.
2. Generate a current editable XLSX sample and use its metadata to prepare the source row. For a new indexed attribute, set `RestAction` to `POST` and leave `AttributeId` blank or omit it; Fusion generates that surrogate value.
3. Validate the prepared artifact through `core.data-loader`, preserving the validated artifact and its diagnostic output under the project workspace.
4. Present the exact target environment, operation, and immutable prepared artifact at the Data Loader approval gate. `core.data-loader` owns the subsequent approval and import execution.
5. If the import is accepted, complete the Submitted Data Loader Status Continuation response gate below in the same user-facing reply as the core initiation report. Do not end that reply with only a submission confirmation or wait for a later turn to offer the status check.
6. If the Data Loader template lacks a usable `METADATA` section, or its live business-object contract cannot represent the intended row, stop with a catalog-metadata mismatch. Do not substitute a native REST POST, PATCH, or DELETE route.

## Single-Index Scope Guard

The existing Run Book contains its catalog-resolved `Manage Product Management
Indexes` task. Do not change Run Book creation or use task Notes as execution
instructions. Start this task only after the active Run Book dashboard has been
delivered.

This skill handles exactly one requested index per invocation. Several
attributes for that index are allowed. If the user supplies two or more indexes,
stop with `input_validation` before any index-specific Fusion lookup, sample,
Task Hook, Data Loader, or ESS action. Ask the user to select one index and its
own attributes for this invocation. Do not choose the first index, split the
request into queued items, maintain batch status, or automatically start another
index after this one finishes. A later index requires a separate user request
and its own validation and approval gates.

Persist and register `single-index-request.json` under this skill's project
artifact directory. Its minimum non-sensitive contract is `schema_version:
"1.0"`, `environment`, one scalar `requested_index_name`,
`canonical_index_name` (null until the exact lookup resolves it), arrays of
`attributes_to_add` and `attributes_to_remove` whose rows inherit that index,
and boolean `index_rebuild_requested`. Record the request artifact, validation
result, Data Loader Request ID and last status, readback, ESS payload and
request ID, approvals, and failure diagnostics in the existing project
artifact/run services. Do not use chat history as the only checkpoint.

Persist `index-execution-state.json` beside the request artifact. It records
exactly one of `data_load_submitted`, `data_load_pending`,
`data_load_succeeded`, `readback_verified`, `ess_approval_pending`,
`ess_submitted`, `ess_skipped`, or `blocked`, together with the canonical index, the accepted
Data Loader Request ID when present, and non-sensitive artifact references.
Use the local helper to make lifecycle transitions; do not infer a continuation
from chat history.

The current state belongs to one invocation. Its canonical index and accepted
Data Loader Request ID are immutable after the first transition. For a later,
separately requested index in the same project, use the helper's `--start-new`
option with that new invocation's initial event. It archives the prior state
under `current/history/` before creating a new current state and refuses to
replace a pending state. Preserve the archived state and prior run record; do
not transfer approvals or external IDs to the new invocation.

Run the local, read-only guard before an index-specific Fusion lookup:

```text
python3 pillars/scm/product-management/index-management/manage-product-management-indexes/scripts/index_work_item_guard.py --request <single-index-request.json>
```

After the exact canonical index lookup, rerun it with `--mutation-ready` before
any Data Loader or ESS approval, including an empty-delta rebuild with no ZIP.
For a nonempty Data Loader change, run it with `--archive <final-zip>` after
`core.data-loader` prepares the final immutable ZIP and before Task Hook
validation and approval. It rejects rows for another index. A failed guard is
`input_validation` and blocks all Fusion-changing actions. Core Data Loader
still owns full schema validation and approval-bound artifact integrity.
The guard output includes `request_sha256`; rerun it after canonical lookup
updates the request and use that digest in the persisted delta.

## Submitted Data Loader Status Continuation

After `core.data-loader` accepts an indexed-attribute import and returns a
positive Request ID, preserve its initiation report and append the output of
the local response helper below **in the same user-facing submission reply**.
The helper states that status has not been checked and ends with the required
question, `Would you like me to check the status of this Data Loader request
now?` Do not omit, paraphrase, defer, or replace the question with a general
instruction to check status. The submission reply is incomplete until it
contains the accepted Request ID, the not-checked status, and that question.

```text
python3 pillars/scm/product-management/index-management/manage-product-management-indexes/scripts/data_loader_submission_followup.py --request-id <accepted-request-id>
```

This helper is offline and does not authorize or perform a status query. If
core reports acceptance without a positive Request ID, do not invent one or
claim a checkable submission; preserve the initiation diagnostics, classify
the outcome as uncertain, and block ESS preparation pending reconciliation.
Wait for the user to request a status check before invoking the core Data
Loader status workflow with the accepted Request ID in the same target
environment.

After each requested check, present the complete core status report. If the
result is pending or the data set is not yet available, offer the same status
choice again, using the same Request ID. Each subsequent check requires a new
user request; do not schedule, poll, or infer consent from an earlier check.
Keep the accepted request and last observed status available in the project
task run record so a later turn can resume without uploading or initiating the
artifact again.

When the result is terminal, stop offering the pending-load status choice. A
successful result still requires verification of every requested change for
the exact canonical `IndexName` before the separate ESS preparation and
approval gate. For a failed or uncertain result, report the core diagnostics
and keep ESS preparation blocked; do not resubmit the load as a status retry.

For a successful status result, this continuation is mandatory in the same
user-facing reply after the complete core status report:

1. Transition `index-execution-state.json` to `data_load_succeeded`.
2. Read back `productManagementESIndexedAttributes` for the exact canonical
   `IndexName` and verify every requested POST and DELETE result. A missing,
   extra, or wrong-index record transitions the state to `blocked` and blocks
   ESS preparation.
3. Transition the state to `readback_verified`, prepare the immutable ESS
   payload, then transition it to `ess_approval_pending`.
4. Append the target environment, affected index, rebuild impact, exact ESS
   payload, and a fresh explicit approval question. The complete core status
   report must remain unchanged; it is not a terminal response for the wider
   index-management workflow.

Use the helper for each state transition:

```text
python3 pillars/scm/product-management/index-management/manage-product-management-indexes/scripts/index_execution_state.py \
  --project-root project/<project_id> --event <event>
```

The helper derives the only permitted state path from `--project-root`:
`artifacts/pillars/scm/product-management/index-management/manage-product-management-indexes/current/index-execution-state.json`.
It rejects paths outside this repository's `project/{project_id}` workspace,
including symlinked artifact-path escapes, and reports local write failures as
`artifact_persistence` without exposing a path or state contents.

## Index Attribute Delta Workflow

For every requested index change or explicit index rebuild, calculate the target
state before preparing a Data Loader row. Use the exact canonical `IndexName` returned by
`ORA_EGP_PM_ES_INDEXES`.

1. POST `{"indexName":"<IndexName>"}` to the read-only
   `indexManagementMetadata` endpoint. Extract every value in
   `SeededIndexedAttributes`. Each value is an identity in the form
   `AttributeCode#GroupCode#ObjectCode`.
2. Resolve every user-requested addition through `indexAvailableAttributes`.
   Convert each validated attribute to that same three-part identity and take
   the de-duplicated union with `SeededIndexedAttributes`. For an explicit
   rebuild with no requested additions or removals, the union is the complete
   set of `SeededIndexedAttributes`; do not treat the empty user list as an
   empty target state.
3. Retrieve all existing Product Management Indexed Attributes for the exact
   index. Convert them to the same identity and subtract them from the union.
   The remainder is the addition delta; do not prepare POST rows for entries
   already present.
4. Resolve every remaining addition identity, including a missing seeded
   identity found during a rebuild-only request, to one exact
   available-attribute record. Then prepare `RestAction: POST` rows.
   `AttributeId` must remain blank or omitted for every new row.
5. Handle user-requested removals separately. Resolve each backend-issued
   `AttributeId` directly from `productManagementESIndexedAttributes` using its
   exact index, attribute, group, and object names. If the narrow name-filtered
   query returns zero rows, use the complete index-only read and match those
   same four names locally. Require one unique matching record and verify any
   supplied `AttributeId` before preparing its `RestAction: DELETE` row. Do not
   use a seeded/default identity to remove an attribute.
6. Submit one immutable Data Loader artifact containing the calculated POST
   rows followed by the requested DELETE rows. If both deltas are empty, skip
   only Data Loader and continue to the Index Rebuild ESS Workflow.

### Delta-before-preparation Gate

Before generating a Data Loader sample, preparing a source row, invoking Task
Hook validation, or requesting a Data Loader approval, persist
`index-attribute-delta.json` in this skill's current project artifact directory.
It must record the exact canonical index, selected environment, calculated POST
and DELETE rows, and the `data_loader_required` decision. Include the
`request_sha256` from the canonicalized request guard; ordered
`resolved_requested_additions` (one per requested addition, with
`request_index`, `attribute_name`, `attribute_code`, `group_code`, and
`object_code`, plus the validated group and object names); complete
`seeded_identities` and `existing_identities` snapshots (code triplets;
existing records also retain backend `attribute_id` and exact attribute,
group, and object names); `validated_seeded_additions` for exactly the
seeded identities absent from the existing snapshot, with their validated
names and codes; and POST/DELETE rows with exact attribute, group,
and object names. Every DELETE row also has its `request_index` and resolved
`attribute_id`. The guard recomputes the set difference and checks each
requested removal against its corresponding row. Then run:

```text
python3 pillars/scm/product-management/index-management/manage-product-management-indexes/scripts/index_delta_guard.py \
  --request <single-index-request.json> \
  --delta <index-attribute-delta.json> \
  --require-data-loader
```

This is a hard precondition, not a documentation checkpoint. A missing,
request-mismatched, environment-mismatched, index-mismatched, malformed, or empty delta blocks
Data Loader preparation. If the delta is empty, record Data Loader as skipped
and continue only to the separate ESS rebuild decision; do not generate a
sample as a substitute for delta calculation.

After preparing the final immutable ZIP, rerun the same guard with
`--archive <final-zip>` before Task Hook validation and Data Loader approval.
It checks ordered DAT rows against the persisted delta and returns the archive
SHA-256. Any ZIP or request change invalidates this check and requires a new
delta validation and approval preview.

The compiled task graph routes addition-only, removal-only, and mixed changes
through the same delta gate. Every nonempty change set reaches
`PMINDEX.DATA_LOADER_GATE` after any DELETE IDs are resolved. That gate
returns an approval-required or status-wait terminal until the exact approved
artifact has been submitted through `core.data-loader` and the user requests
a status check. Resume at the recorded gate with the same request fingerprint,
canonical index, accepted Request ID, and validated artifact references; do
not recompute the post-import delta, re-upload, or treat a prior status request
as consent for another check. Only a terminal successful status for that load
permits exact-index readback and then ESS preparation. An empty delta skips
Data Loader and reaches its own ESS preparation and approval-or-explicit-skip
branch.

## Preflight and Execution Safety

Before preparing a preview or performing any live Fusion activity, load and
apply `ora-resource/ora_error_handling.md`. Its task-specific classifications,
disclosure rules, and refusal rules are mandatory controls for Data Loader and
ESS preparation, approval, submission, status checks, and failure handling.
Do not proceed when that resource is unavailable or cannot be read; classify
the condition as `artifact_persistence` and stop before preview or live
execution.

Before any Fusion-changing action, confirm the target environment, Data Loader privileges, registered business object, exact index/attribute scope, seeded metadata, existing-attribute state, calculated addition/removal delta, and immutable prepared artifact. Use `validate_index_available_attribute` to confirm that each POST identity resolves to exactly one available source attribute. Validate the source row against the current Data Loader metadata and obtain the Task Hook preview before `core.data-loader` evaluates approval and submits the import.

Classify durable failures as `input_validation`, `catalog_or_metadata_mismatch`, `auth_expired_or_invalid`, `authorization_or_privilege`, `transport_or_environment`, `fusion_api_error`, `process_timeout`, `process_failed`, `artifact_persistence`, or `approval_blocker`. Retry only a cached-token 401 or 403 once through the core authentication service and bounded read-only transport failures. Do not retry a live POST, upload, initiation, or other Data Loader operation without idempotency or a new explicit approval.

For a timeout or failed import, persist sanitized diagnostics under the active project workspace with the stage, failure class, environment, artifact references, request ID or process ID, last known status, and next action. Never print or persist credentials, OAuth tokens, token-cache contents, private keys, tenant secrets, or full sensitive payloads.

## Index Rebuild ESS Workflow

Use this workflow after every requested index operation, including an operation
whose calculated attribute delta is empty. It is required by default because a
rebuild can be needed even when the indexed-attribute data already matches the
requested state. Skip it only when the user explicitly confirms that ESS
submission is not required; absence of a skip confirmation means the workflow
must prepare the rebuild request.

1. When the calculated POST or DELETE delta is nonempty, including a missing
   seeded-attribute repair delta from a rebuild-only request, submit the
   indexed-attribute change through `core.data-loader`. After submission,
   use the Submitted Data Loader Status Continuation above and, once the load
   is complete and successful for the exact canonical `IndexName`, proceed
   with preparation of the Product Management index rebuild ESS job and obtain
   separate approval to submit that index rebuild job. Do not prepare,
   preview, or submit the ESS job while that related Data Loader request is
   pending, failed, or unverified. When the delta is empty, record that Data
   Loader was intentionally skipped and continue directly to the ESS decision
   and its separate approval gate.
2. When more than one attribute is added or removed, require every requested
   change for that one index to be verified before preparing one rebuild job.
   If any change fails, is pending, or targets a different index, do not submit
   the job.
3. Build the following immutable request using the exact canonical `IndexName`
   already validated for the indexed-attribute operation. Substitute only the
   two marked values; preserve every other field and the one-element parameter
   order exactly:

   ```json
   {
     "description": "rebuildIndex-<index name>",
     "jobDefinitionId": "JobDefinition://oracle/apps/ess/scm/productCatalogManagement/common/PMESIndexMaintenanceJob",
     "application": "FscmEss",
     "requestType": "SINGLETON",
     "requestParameters": [
       {
         "name": "submit.argument1",
         "paramType": "STRING",
         "value": "<index name>"
       }
     ]
   }
   ```

4. Prompt the user with the target environment, the affected index, the
   rebuild impact, and this exact payload. Require a new explicit approval
   immediately before submission. The user may instead explicitly confirm that
   ESS submission is not required, which records a skip and ends the rebuild
   workflow. Approval of the Data Loader import, an earlier plan, or the
   combined attribute-and-rebuild request does not approve this ESS POST.
   On an explicit skip, transition the continuation state from
   `ess_approval_pending` to terminal `ess_skipped` and persist the skip
   decision; absence of approval is not a skip.
5. After approval, submit exactly once through
   `core.fusion-api.ess-job-submitter` using its `--payload-file` and
   `--submit-only` route. Persist the returned positive `requestId` and the
   sanitized payload fingerprint under the active project workspace. Do not
   call Scheduler REST directly from this task skill.
6. Do not automatically poll, retry, or submit a replacement request. When the
   user asks for job status, use the core ESS submitter's `--request-id` route.
   On a missing response, timeout, or transport ambiguity, retain the payload
   fingerprint and any returned ID, reconcile with read-only evidence, and
   require new explicit approval before another submission.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `productManagementESIndexedAttributes` is the exact registered Data Loader business object.
2. Complete the **Delta-before-preparation Gate**. Do not generate this sample
   until `index_delta_guard.py --require-data-loader` succeeds for the
   persisted `index-attribute-delta.json`.
3. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "productManagementESIndexedAttributes" \
     --output-dir "<project-artifact-directory>"
   ```

4. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
5. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.



## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `canonical_index_name`
- `single_index_request`
- `attributes_to_add`
- `attributes_to_remove`
- `index_rebuild_requested`
- `index_rebuild_skip_confirmation`
- `ess_execution_options`
- `data_loader_status_check_requested`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `seeded_indexed_attributes`
- `index_attribute_delta`
- `index_scope_validation_result`
- `index_rebuild_ess_payload`
- `index_rebuild_decision`
- `index_rebuild_ess_submission_result`
- `data_loader_submission_followup`
- `data_loader_status_result`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `scm.product-management.index-management` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

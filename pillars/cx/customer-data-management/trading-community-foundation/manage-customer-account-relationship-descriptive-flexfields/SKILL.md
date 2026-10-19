---
skill_id: "cx.customer-data-management.trading-community-foundation.manage-customer-account-relationship-descriptive-flexfields"
name: "Manage Customer Account Relationship Descriptive Flexfields Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Customer Account Relationship Descriptive Flexfields under the Trading Community Foundation functional area."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Trading Community Foundation"
functional_area_code: "ORA_HZ_CDM_FOUNDATION"
task_code: "HZ_CUSTOMER_ACCOUNT_RELATIONSHIP_DESCRIPTIVE_FLEXFIELDS"
task_name: "Manage Customer Account Relationship Descriptive Flexfields"
parent_skill_id: "cx.customer-data-management.trading-community-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "CX customer data management pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-customer-account-relationship-descriptive-flexfields/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-customer-account-relationship-descriptive-flexfields/current/"
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

# Manage Customer Account Relationship Descriptive Flexfields Setup Task Guidance

## Purpose and Boundary

Use this skill to export, import, migrate, validate, or resume status for the
complete FSM setup package of `Manage Customer Account Relationship Descriptive Flexfields`.
The fixed task code is `HZ_CUSTOMER_ACCOUNT_RELATIONSHIP_DESCRIPTIVE_FLEXFIELDS`.
Use this skill when planning, sequencing, exporting, importing, or validating
setup data for `Manage Customer Account Relationship Descriptive Flexfields` under
`Trading Community Foundation`.

Do not create, update, delete, deploy, or inspect individual flexfields,
contexts, segments, value sets, or attributes. Do not use direct descriptive
flexfield REST CRUD, task-local HTTP, loose CSV, templates, filters, or partial
package migration. The shared FSM exporter owns export validation and execution.
Core Data Loader owns every import, including adapter, endpoint, payload,
submission, status, and retry-policy selection.

## Fixed Task Context

- Pillar: `CX`
- Offering: `Customer Data Management`
- Functional area: `Trading Community Foundation`
- Functional area code: `ORA_HZ_CDM_FOUNDATION`
- Task name: `Manage Customer Account Relationship Descriptive Flexfields`
- Task code: `HZ_CUSTOMER_ACCOUNT_RELATIONSHIP_DESCRIPTIVE_FLEXFIELDS`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- Data Loader import mode: `FSM`

Never accept a caller override for the task name or code. Use the parent skill
for broader functional-area sequencing.

## Oracle Source Boundary

Use these Oracle sources for deployment and migration guardrails:

- [How Flexfields Work with Oracle Application Cloud Architecture](https://docs.oracle.com/en/cloud/saas/applications-common/26c/oaext/how-flexfields-work-with-oracle-application-cloud-architecture.html)
- [Overview of Flexfield Configuration](https://docs.oracle.com/en/cloud/saas/applications-common/26c/facia/overview-of-flexfield-configuration.html)
- [Business Objects for Moving Common Reference Objects](https://docs.oracle.com/en/cloud/saas/applications-common/26b/facia/business-objects-for-moving-common-reference-objects.html)

Oracle states that only `Deployed` or `Deployed to Sandbox` flexfields are
eligible to be moved. Treat that as Fusion migration behavior, not as a manual
status-evidence prerequisite for starting an FSM export. Do not ask the user for
source deployment status, observation time, or an evidence reference before
export; rely on the export process and its `ProcessLog` to report exportability.
Descriptive-flexfield sandbox testing remains required before manual publication.
Import can change deployment status and can submit affected flexfields for
redeployment; neither an accepted import nor automatic redeployment proves that
target deployment and functional verification passed. Do not apply
extensible-flexfield background-deployment queue behavior here.

## Supported Operations

1. `export`: authorize and run one complete, unfiltered, non-template task export.
2. `import`: validate and authorize one complete, unchanged FSM ZIP and run one import.
3. `migrate`: finish and persist source export, then perform separate target preflight and approval before import.
4. `validate`: validate fixed task context, operation-specific routing, package identity when supplied, and approval readiness without submission.
5. `status`: resume polling or retrieve results for one persisted `ProcessId`; never create another process.

## Export and Import Adapter Contract

For export, preserve the existing export route: validate the fixed task and
whole-task scope, display one exact task-level export preview, obtain explicit
approval for that environment and process creation, and invoke
`shared.setup-export.task-level-export` directly. Do not route export through
`core.data-loader`, `approved-loader-payload`, or `executionRoute=data-loader`.
An export never requires a pre-existing ZIP path or SHA-256.

Use this fixed export final data:

```text
operation=export
task_code=HZ_CUSTOMER_ACCOUNT_RELATIONSHIP_DESCRIPTIVE_FLEXFIELDS
task_name=Manage Customer Account Relationship Descriptive Flexfields
offering_name=Customer Data Management
functional_area_name=Trading Community Foundation
template_only=false
export_criteria=[]
output_dir=project/{project_id}/exports/customer-data-management/trading-community-foundation/manage-customer-account-relationship-descriptive-flexfields/
execution_adapter=shared.setup-export.task-level-export
wait_seconds=300
poll_interval=10
```

After export approval, invoke `shared.setup-export.task-level-export` exactly once. The
shared exporter owns the export POST, `ProcessId`, polling, `FileContent`, and
`ProcessLog` behavior. After download, compute and persist the exported ZIP's
SHA-256. Do not implement task-local export HTTP.

For import, route exclusively through `core.data-loader`. Require one unchanged
ZIP and supply only this task context to Core Data Loader:

```text
operation=import
task_code=HZ_CUSTOMER_ACCOUNT_RELATIONSHIP_DESCRIPTIVE_FLEXFIELDS
task_name=Manage Customer Account Relationship Descriptive Flexfields
setup_data_zip_path=<validated ZIP path>
setup_data_zip_sha256=<SHA-256 of the exact ZIP bytes>
```

Require a valid ZIP signature and exactly one case-sensitive member basename
`ASM_SETUP_CSV_METADATA.xml`. Require its single task identity to equal the
fixed task code. Preserve the archive byte for byte. Do not construct or change
an import payload or request a revision-mismatch override.

Let Core Data Loader prepare the final immutable artifact, invoke its `data-load`
Task Hook, build the approval preview, and obtain the user's separate explicit
approval. The Task Hook validation envelope must remain bound to the exact ZIP
SHA-256. Core Data Loader then owns UCM upload, initiation-payload construction,
endpoint and FSM adapter selection, accepted-request reporting, status
diagnostics, and retry policy. This pillar skill must not select or invoke an
import adapter, endpoint, routing field, payload builder, or retry behavior.

## Post-Import Deployment Verification

After a terminally successful import, require target deployment evidence and a
functional verification result:

- Return `import_succeeded_deployment_verified` only when target status is
  `Deployed` or `Deployed to Sandbox` and the customer account relationship DFF functional test
  passed in the named target environment.
- Return `import_succeeded_deployment_pending` when import succeeded but target
  status or functional verification is missing, nonterminal, `Edited`,
  `Patched`, or `Error`. Report the manual validation, sandbox deployment/test,
  publication, or redeployment action required; do not perform it.
- Return `import_failed` only when the FSM import process fails. Retrieve and
  persist `ProcessLog` when available.

Never collapse import acceptance, import process success, automatic
redeployment submission, target deployment status, UI rendering, and
functional verification into one success claim.

## Preflight and Approval

Before any live export or import:

1. Resolve a valid project, exact environment, fixed task context, durable
   output paths, and task-local compiled rules.
2. Authenticate separately. If a cache-managed token fails on a read-only
   preflight, refresh once and repeat only that GET. A second rejection blocks
   submission.
3. Confirm live task discovery returns the fixed task code and
   `CSVExportImportSupportedFlag=Y`. Do not reject solely because offering or
   functional-area fields are absent in the live row.
4. For export, validate the fixed whole-task non-template contract. Do not ask
   for deployment status, a ZIP path, or a SHA-256 before export.
5. For import, validate the unchanged archive, exact metadata identity, hash,
   and target, then hand control exclusively to Core Data Loader.
6. For export, display one redacted task-level preview containing the environment,
   task, whole-task scope, output path, adapter, execution options, and one-process
   impact. Bind approval to those values and then call the shared exporter directly.
7. For import, let Core Data Loader display the immutable preview and obtain
   approval bound to its environment, task, ZIP/hash, validation envelope, and
   impact. Any changed import-bound value restarts Core Data Loader validation,
   Task Hook, preview, and approval.

## Submission, Polling, and Reconciliation

Persist an external identifier returned by the owning exporter or Core Data
Loader immediately in an append-only run record. Delegate polling, log retrieval,
and status semantics to that owner. On timeout, preserve the identifier and safe
resume stage; never submit a replacement process.

Never automatically retry an export or import mutation after 401, 403, timeout,
connection closure, or an uncertain response. For import, follow only Core Data
Loader's reconciliation and status contract. For export, reconcile using
read-only process lookup for the fixed task and run-start window:

- One matching process: persist and resume its `ProcessId`.
- No matching process: record `not_created`; a new POST needs fresh approval.
- Multiple or unidentifiable matches: record `ambiguous` and fail closed.

## Diagnostics and Results

Classify failures as `input_validation`, `catalog_or_metadata_mismatch`,
`auth_expired_or_invalid`, `authorization_or_privilege`,
`transport_or_environment`, `fusion_api_error`, `process_timeout`,
`process_failed`, `artifact_persistence`, `approval_blocker`, or
`deployment_verification`.

Report the exact task, environment, operation, owning execution skill, `ProcessId`,
terminal or last-known process status, artifact paths, ZIP SHA-256 when
applicable, deployment-verification result, warnings, blockers, and one safe
next action. Never print or persist tokens, secrets, Authorization headers,
token-cache contents, full base64 payloads, or sensitive environment values.

## Refusal Rules

Refuse:

- Direct descriptive flexfield REST CRUD or a task-local endpoint/script.
- Individual context, segment, value-set, attribute, deployment, or UI changes.
- Template/spec exports, export criteria, filters, or partial migration.
- Loose CSV, an edited/repacked ZIP, missing or ambiguous metadata identity,
  revision mismatch override, task-code override, or changed approved artifact.
- Task-local import adapter, endpoint, routing-field, payload, or retry selection.
- A new submission while a previous response or `ProcessId` is uncertain.
- A complete-success claim without target deployment and functional evidence.

## Golden Scenarios

| Scenario | Expected result |
|---|---|
| Export the complete task from TEST | Do not ask for deployment evidence or a pre-existing ZIP/hash; approve the fixed whole-task contract, submit once through the shared exporter, and persist ZIP, hash, ProcessId, and status |
| Import the unchanged ZIP into UAT | Validate exact task metadata and hash, hand the archive to Core Data Loader, approve its immutable preview, let it execute and report status, and classify deployment verification separately |
| Migrate TEST to UAT | Finish source export before separate target validation and import approval; return complete only after target deployment and functional verification |
| Export a template or one flexfield | Refuse without a Fusion call |
| Edit a segment through REST | Refuse because direct DFF CRUD is unsupported |
| Import succeeds but target is Patched | Return import_succeeded_deployment_pending and report manual validation/redeployment and sandbox-test action |
| Polling times out | Preserve the same ProcessId and allow status-only continuation; never resubmit |

## Ownership and Review

- Owner: CX Customer Data Management pillar team.
- Functional reviewer: CX Customer Data Management Pillar Lead or Trading Community Foundation SME.
- Framework reviewer: FSCR A-Team/core reviewer.
- QA reviewer: required for FSM routing, approval, deployment, or verification changes.

Track token usage for generated project artifacts and skill-run records using
the manifest policy.

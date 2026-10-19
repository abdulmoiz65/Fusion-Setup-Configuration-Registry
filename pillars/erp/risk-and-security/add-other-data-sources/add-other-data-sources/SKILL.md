---
skill_id: "erp.risk-and-security.add-other-data-sources.add-other-data-sources"
name: "Add Other Data Sources Setup Task Guidance"
description: "Provides task-specific setup guidance for Add Other Data Sources under the Add Other Data Sources functional area."
layer: "pillar"
pillar: "ERP"
offering: "Risk and Security"
functional_area: "Add Other Data Sources"
functional_area_code: "ORA_GTG_ADD_OTHER_DATA_SOURCES"
task_code: "ORA_GTG_ADD_OTHER_DATA_SOURCES"
task_name: "Add Other Data Sources"
parent_skill_id: "erp.risk-and-security.add-other-data-sources"
available_flag: "Y"
export_import_supported_flag: "UNKNOWN"
csv_export_import_supported_flag: "UNKNOWN"
dataloader_import_mode: "REST"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "hybrid"
owner_team: "ERP risk and security pillar team"
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
  - "runbook_task_completion"
uses_core:
  - "core.fusion-api.rest-api-client"
  - "core.auth.fusion-oauth-authentication"
  - "core.runbook"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/risk-and-security/add-other-data-sources/add-other-data-sources/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/risk-and-security/add-other-data-sources/add-other-data-sources/current/"
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
  - "Reads Data Integrator connector definitions through the approved Fusion BOSS REST client for exact post-registration verification."
  - "After explicit approval, can POST a validated connector-definition payload through the approved Risk Cloud REST client."
  - "After the final connector-definition result is verified successful, can complete the linked Add Other Data Sources Run Book task through core.runbook when the originating request includes configuration or task completion."
required_privileges:
  - "BOSS read access for Data Integrator connector definitions"
  - "Risk Cloud REST access to create connector definitions"
---

# Add Other Data Sources Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Add Other Data Sources` under `Add Other Data Sources`.

## Setup Task Skill Contract

- task_code: `ORA_GTG_ADD_OTHER_DATA_SOURCES`
- task_name: `Add Other Data Sources`
- parent_skill_id: `erp.risk-and-security.add-other-data-sources`
- pillar: `ERP`
- offering: `Risk and Security`
- functional_area: `Add Other Data Sources`
- functional_area_code: `ORA_GTG_ADD_OTHER_DATA_SOURCES`
- available_flag: `Y`
- export_import_supported_flag: `UNKNOWN`
- csv_export_import_supported_flag: `UNKNOWN`
- dataloader_import_mode: `REST`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Add Other Data Sources` under `Add Other Data Sources`.

## Setup Task Metadata

- Task name: `Add Other Data Sources`
- Task code: `ORA_GTG_ADD_OTHER_DATA_SOURCES`
- Available: `Y`
- Export/import supported: `UNKNOWN`
- CSV export/import supported: `UNKNOWN`
- CSV export/import routing: `not catalog-supported`
- Data Loader import mode: `REST`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `UNKNOWN`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.

## Hybrid Execution Preflight Checks

Complete these checks before the preview creates an approval artifact and repeat
the execution-specific checks immediately before the REST POST. Stop on any
failed, missing, or ambiguous check; do not use another client, endpoint, or
target as a fallback.

1. Confirm `project_context` resolves to an initialized FSCR project workspace
   when preview, execution, Run Book completion, or durable artifacts are in
   scope. Confirm the declared project artifact paths are writable without an
   unapproved overwrite.
2. Confirm the connector type has one valid local profile and a matching
   `sourceTypeName` and `sourceTypeCode` in `connector-source-types.json`.
   Confirm the documentation-backed OpenAPI input and extracted REST Operations
   pass their respective validation before payload generation.
3. Confirm the target is an explicit HTTPS Fusion base URL, the only mutation
   route is `POST /api/risk-cloud/rc-tools-ms/dataintegration/v1/dataIntegratorConnectorDefinitions`,
   and the approved Risk Cloud client, `rmc_scope`, and create/read privileges
   are available for the target environment.
4. Confirm the generated payload is credential-free, recursively rejects
   prohibited fields, uses only profile-allowlisted setup keys, and contains no
   undocumented setup values. Preview may write only review artifacts; it must
   not call Fusion.
5. Before execution, confirm a clear, contextual user approval exists for the
   exact persisted artifact. Recalculate the payload digest and require the
   target, method, endpoint, and payload to match the approval artifact.
6. Before execution, require `restBaseUrl` in the supplied properties file to
   equal the approval-bound target after URL normalization. The runner fails
   closed on mismatch before it writes a request body or sends the POST.
7. Before Run Book completion, confirm the exact registered connector is
   `COMPLETED` and `ACTIVE`, the project task context resolves the exact task
   code, and the originating request includes configuration or task completion.

## Failure Handling and Redaction

Classify every failure using the task-local
[`ora_error_handling.md`](ora-resource/ora_error_handling.md) contract. On an
input, catalog, target-binding, privilege, payload, or approval failure, stop
before the POST, retain only sanitized diagnostic metadata, and report the next
safe action. Refresh a cached token at most once for a recoverable 401/403
read-only check; never retry a connector-definition POST or an indeterminate
Run Book PATCH without fresh approval or an idempotency guarantee. On an
uncertain POST, use the declared read-only BOSS verification path before any
new preview.

Redact and never print or persist credentials, `authenticationDetails`, client
secrets, bearer or refresh tokens, private keys, complete authorization
headers, token-cache contents, or full untrusted response bodies. Persist only
the approved credential-free payload, digest, target, method, endpoint,
sanitized HTTP status, connector identifier, and next safe action in the
declared project artifacts.


## REST connector-definition workflow

This task uses the Risk Cloud REST connector-definition POST. It does not use
a Data Loader business object or Data Loader upload/initiation.

1. Resolve the connector type and load its profile from
   `connector-profiles/`. New connector types add a profile rather than a new
   orchestration branch. Resolve `sourceTypeName` and `sourceTypeCode` from
   the parent functional area's `connector-source-types.json`; do not accept
   either value as a task-local runtime input.
2. Use `references/generate-openapi-spec.md` to discover and validate the
   connector's OpenAPI JSON. OCI is a temporary, explicitly scoped exception:
   use the validated pinned document at `references/oci-openapi-spec.json` as
   directed by that workflow. For every other connector, if discovery cannot
   establish a usable, documentation-backed specification, stop and request
   the required documentation or clarification; do not use a local sample or
   fallback.
3. Use `references/extract-operations.md` to derive the complete `REST
   Operations` contract from the validated OpenAPI JSON. Keep both contracts
   in memory until preview creates the approval-bound payload artifact.
4. Convert the extracted operations into connector extraction objects and
   source endpoints, then build the connector-definition payload:

   ```bash
   python3 scripts/run_connector_definition.py format \
     --operations <rest-operations.json> \
     --output <formatted-operations.json>
   ```

5. Validate the complete credential-free payload, target environment, and
   endpoint before any write. Reject credentials, `authenticationDetails`,
   bearer tokens, refresh tokens, private keys, and undocumented setup keys.
   Persist the exact payload, target, method, and SHA-256 digest as an
   approval-bound project artifact. Do not POST during preview:

   ```bash
   python3 scripts/run_connector_definition.py preview \
     --operations <rest-operations.json> \
     --openapi-spec <discovered-openapi.json> \
     --profile connector-profiles/<connector-type>.json \
     --connector-name <connector-name> \
     --connector-setup-json <connector-setup.json> \
     --target-url <fusion-base-url> \
     --project-root <project-root>
   ```
6. After a later clear approval, execute the unchanged approval artifact once:

   ```bash
   python3 scripts/run_connector_definition.py execute \
     --approval-state <approval-state> \
     --approve-digest <approved-digest> \
     --properties <fusion-properties-file>
   ```

7. Return the sanitized HTTP result and server request/connector identifier.
   When an exact connector identifier is returned, present the connector setup
   page for the user to enter credentials:

   ```text
   {restBaseUrl}/fscmUI/redwood/rc-dataintegration/rc-ai-datasource/connector-authentication?connectorId=<connector_id>&connectorType=OCI
   ```

   Never retry an uncertain POST. Instead, use the exact read-only BOSS
   verification query below before deciding whether a new preview and approval
   are needed.

### Connector Registration Verification and Recovery

Use this read-only path after an uncertain connector-definition POST, or after
the user completes the connector setup page and explicitly asks for a status
check. Query the supported source-type field through
`core.fusion-api.rest-api-client/scripts/boss-rest_client.py`:

```text
POST /api/boss/data/objects/ora/riskMgmtRisk/dataIntegration/v1/connectorDefinitions/$query
```

Build a body file using the centrally resolved `sourceTypeName`:

```json
{
  "collection": {
    "filter": "sourceTypeName='<source_type_name>' and connectorStatus='ACTIVE' and creationStatus='COMPLETED'"
  }
}
```

Run the existing BOSS client with explicit properties and an output file:

```bash
python3 core/fusion-api/rest-api-client/scripts/boss-rest_client.py \
  /api/boss/data/objects/ora/riskMgmtRisk/dataIntegration/v1/connectorDefinitions/$query \
  --method POST \
  --body-file <connector-verification-query.json> \
  --properties <boss-properties-file> \
  --output <connector-verification-response.json>
```

This is a read-only BOSS query using `boss_scope` and its separate local token
cache. The BOSS resource does not support `name` in its server-side filter, so
select an exact `name` match locally from the returned collection. Treat a
missing name, multiple exact name matches, or `hasMore: true` as ambiguous.
Sanitize the response and persist only the exact connector's ID,
`creationStatus`, `connectorStatus`, HTTP status, target, and next safe action.

- Zero records: the approved POST did not produce a discoverable connector.
  Do not retry automatically; rebuild the preview and obtain fresh approval
  before another creation attempt.
- More than one exact name match or `hasMore: true`: stop on the ambiguous
  result and require user selection. Do not choose a connector or retry the
  POST.
- Exactly one record that is not both `creationStatus: COMPLETED` and
  `connectorStatus: ACTIVE`: present its connector setup URL, keep the Run
  Book task open, and wait for the user to complete UI setup and request a
  later status check.
- Exactly one record that is `COMPLETED` and `ACTIVE`: verification succeeds.
  Continue to the Run Book completion handoff only when the originating
  request includes configuration or task completion.

### Run Book Completion Handoff

After the final REST workflow result is verified successful, invoke
`core.runbook` to complete the linked `Add Other Data Sources` task. This step
applies when the originating request asks to configure or complete the task;
preview-only, readiness-only, and contract-only requests stop after their
declared result.

Resolve the active Run Book and the exact task code
`ORA_GTG_ADD_OTHER_DATA_SOURCES` from the initialized project's task context.
Set the task status to `completed` and completion percentage to `100`, then
persist the refreshed task detail and the update result in the skill-run
record. A successful HTTP response alone is not sufficient when the connector
registration result is uncertain or the required verification artifact is
missing.

If the Run Book PATCH fails or is indeterminate, preserve the successful REST
result, record that the Run Book task was not updated, and do not retry the
PATCH automatically.

The generic reference procedures are in `references/`: OpenAPI generation,
operation extraction, connector authentication configuration, mapping, and
function generation. They are connector-neutral and may be reused by every
profile.

The REST execution route owns approval immediately before the mutation. Do not
request a second Data Loader approval or upload a loader artifact.

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

Use the parent functional-area skill `erp.risk-and-security.add-other-data-sources` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

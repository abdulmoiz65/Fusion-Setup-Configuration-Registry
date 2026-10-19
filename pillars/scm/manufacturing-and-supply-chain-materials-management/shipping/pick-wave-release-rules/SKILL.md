---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.shipping.pick-wave-release-rules"
name: "Pick Wave Release Rules Setup Task Guidance"
description: "Provides task-specific setup guidance for Pick Wave Release Rules under the Shipping functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Shipping"
functional_area_code: "WSH_ENABLE_SHIPPING"
task_code: "ORA_PICK_WAVE_RELEASE_RULES"
task_name: "Pick Wave Release Rules"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.shipping"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "releaseRules"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM manufacturing and supply chain materials management pillar team"
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
  - "core.fusion-api.rest-api-client"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/shipping/pick-wave-release-rules/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/shipping/pick-wave-release-rules/current/"
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

# Pick Wave Release Rules Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Pick Wave Release Rules` under `Shipping`.

## Setup Task Skill Contract

- task_code: `ORA_PICK_WAVE_RELEASE_RULES`
- task_name: `Pick Wave Release Rules`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.shipping`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Shipping`
- functional_area_code: `WSH_ENABLE_SHIPPING`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `releaseRules`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Pick Wave Release Rules` under `Shipping`.

## Setup Task Metadata

- Task name: `Pick Wave Release Rules`
- Task code: `ORA_PICK_WAVE_RELEASE_RULES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `releaseRules`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using releaseRules as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Shipping`
- Setup task name: `Pick Wave Release Rules`
- Setup task code: `ORA_PICK_WAVE_RELEASE_RULES`


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `releaseRules` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "releaseRules" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.



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

## Machine-Readable Output Contract

Every planning, routing, and validation artifact produced by this skill must
conform to `contracts/planning-validation-output.schema.json`. Use one document
per artifact with `artifact_type` set to `setup_task_plan`,
`setup_data_routing`, or `validation_result`.

The contract requires the exact task identity, a status, generated timestamp,
source-evidence references, validation summary, and errors array. A passed
artifact must have an empty `errors` array. Downstream skills must validate the
document before consuming it and fail closed on a task identity mismatch,
unsupported artifact type, missing required field, or a non-passed validation
result when a passed result is required.

`tests/fixtures/planning-validation-output-example.json` is a synthetic,
schema-valid representative artifact. It contains no customer, environment, or
credential data.

## Read-Only Lookup Delegation

The `reference_lookup` nodes in `ora-resource/ora_reference_lookups.md` must
run only through `core.fusion-api.rest-api-client`. That core capability owns
OAuth acquisition and refresh, REST transport, request headers, redaction, and
the single cached-token 401 or 403 refresh/retry boundary.

Before a lookup, confirm the configured target environment and the resolver's
exact documented GET path. Use no request body and never invoke a direct
transport client from this pillar skill. Record only sanitized resolver name,
match count, mapped fields, and failure class; never record tokens,
authorization headers, client secrets, token-cache contents, or raw sensitive
responses. Classify failures as `auth_expired_or_invalid`,
`authorization_or_privilege`, `transport_or_environment`, or
`fusion_api_error`; do not retry a non-auth lookup failure automatically.

## Implementation Notes

Use the parent functional-area skill `scm.manufacturing-and-supply-chain-materials-management.shipping` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

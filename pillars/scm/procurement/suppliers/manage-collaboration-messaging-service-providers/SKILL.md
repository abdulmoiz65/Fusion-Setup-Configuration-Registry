---
skill_id: "scm.procurement.suppliers.manage-collaboration-messaging-service-providers"
name: "Manage Collaboration Messaging Service Providers Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Collaboration Messaging Service Providers under the Suppliers functional area."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Suppliers"
functional_area_code: "ORA_EGP_SUPPLIERS"
task_code: "ORA_CMK_COLLAB_MESG_SERVICE_PROVIDER"
task_name: "Manage Collaboration Messaging Service Providers"
parent_skill_id: "scm.procurement.suppliers"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM procurement pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/manage-collaboration-messaging-service-providers/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/manage-collaboration-messaging-service-providers/current/"
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

# Manage Collaboration Messaging Service Providers Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Collaboration Messaging Service Providers` under `Suppliers`.

## Setup Task Skill Contract

- task_code: `ORA_CMK_COLLAB_MESG_SERVICE_PROVIDER`
- task_name: `Manage Collaboration Messaging Service Providers`
- parent_skill_id: `scm.procurement.suppliers`
- pillar: `SCM`
- offering: `Procurement`
- functional_area: `Suppliers`
- functional_area_code: `ORA_EGP_SUPPLIERS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Supplied Task Inputs

Reuse clearly mapped requirements and answers from supplied spreadsheets,
CSVs, images, tables, and text, retaining source references without requiring
repetition or reformatting. Distinguish requested changes from current-state
examples; group only missing, unreadable, conflicting, ambiguous, or unsupported
in-scope values into one prompt. Preserve unrequested settings and explicit
Preserve choices; blanks do not mean Clear or false. Supplied snapshots do not
replace fresh lookups. Keep the task's validation, prerequisite checks, execution
route, and approval gates; do not ask twice for the same operation's approval.

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Collaboration Messaging Service Providers` under `Suppliers`.

## Development Readiness

This is a draft catalog-generated skill structure. Task-specific resource rules
and a rule registry are present and compile as ready. A live import still requires
the exact target feature check, immutable ZIP validation, project Run Book
binding, Task Hook approval preview, and Data Loader approval. No customer
release has been qualified for import.

Before using a live workflow, establish the applicable release and feature state, supported task-specific import contract, required privileges, validation rules, and outcome verification. Catalog export/import flags do not establish the exact create/update package contract. Resolve missing evidence through the declared workflow; do not substitute an undocumented API or browser route. Customer shipment requires completed functional testing and the applicable release reviews.

## Setup Task Metadata

- Task name: `Manage Collaboration Messaging Service Providers`
- Task code: `ORA_CMK_COLLAB_MESG_SERVICE_PROVIDER`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

Before a template export, populated setup-data export, or task-CSV import,
verify that `ORA_CMK_B2B_DOCUMENT_SETUP` is enabled in the environment that
will perform that operation. Check the source environment before the export
POST. For import, check the destination during Task Hook preapproval validation
for the exact immutable ZIP, before presenting upload approval. Require a
fresh, exact-code, same-target result showing `EnabledFlag: Y`; a catalog flag,
prior export, Redwood page profile, or another environment's result does not
establish current opt-in state. If the feature is disabled, missing, ambiguous,
or cannot be read, stop before creating an export process or uploading an
import. Use the declared read-only client and decision rules in
`ora-resource/ora_reference_lookups.md` and
`ora-resource/ora_dependency_readiness.md`; do not enable the feature as part of
an export or import request.

Run the shared Core REST client against the exact host already selected by the
export or import workflow:

```text
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  --properties <selected-fusionEnv.properties> \
  --method GET \
  --query "q=FeatureCode='ORA_CMK_B2B_DOCUMENT_SETUP'" \
  --query "fields=FeatureCode,FeatureType,EnabledFlag" \
  --query "onlyData=true" \
  /fscmRestApi/resources/11.13.18.05/features
```

Confirm that `restBaseUrl` resolves to the selected host. Proceed only when the
response contains exactly one item with `FeatureCode:
ORA_CMK_B2B_DOCUMENT_SETUP`, `FeatureType: FEATURE`, and `EnabledFlag: Y`.
For import, record that result as evidence for
`verify_cmksp_b2b_document_setup_enabled` in the Task Hook rule results before
building the approval preview. A failed lookup blocks this task's export or
import. Recheck for each operation and target; do not reuse an earlier result.
The command only reads feature state.

When Fusion returns `EnabledFlag: N`, show the preflight's action message with
the selected environment: "Service Providers export/import is blocked in
{environment}: go to Navigator > My Enterprise > Offerings, select Procurement
> Opt In Features, enable Simplify Configuration and Processing for B2B Messaging
(`ORA_CMK_B2B_DOCUMENT_SETUP`), and wait for opt-in processing to complete. Then
retry this operation." Keep missing, ambiguous, and unreadable
results distinct from a confirmed disabled feature.

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Procurement`
- Functional area / Setup Object: `Suppliers`
- Setup task name: `Manage Collaboration Messaging Service Providers`
- Setup task code: `ORA_CMK_COLLAB_MESG_SERVICE_PROVIDER`

This is an assisted, task-specific gate. The shared export CLI and Data Loader
do not invoke the preflight automatically. Route Service Providers work through
this skill and stop before those CLIs when the preflight is absent or blocked.
Direct use of the generic CLIs bypasses this gate and is not a verified
Service Providers workflow.




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

Use the parent functional-area skill `scm.procurement.suppliers` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

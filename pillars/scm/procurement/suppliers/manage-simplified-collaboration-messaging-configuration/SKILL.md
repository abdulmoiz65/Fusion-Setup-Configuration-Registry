---
skill_id: "scm.procurement.suppliers.manage-simplified-collaboration-messaging-configuration"
name: "Manage Simplified Collaboration Messaging Configuration Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Simplified Collaboration Messaging Configuration under the Suppliers functional area."
layer: "pillar"
pillar: "SCM"
offering: "Procurement"
functional_area: "Suppliers"
functional_area_code: "ORA_EGP_SUPPLIERS"
task_code: "ORA_CMK_MNGE_SIMPLIFIED_COLLAB_MSG_CONFIG"
task_name: "Manage Simplified Collaboration Messaging Configuration"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/manage-simplified-collaboration-messaging-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/procurement/suppliers/manage-simplified-collaboration-messaging-configuration/current/"
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

# Manage Simplified Collaboration Messaging Configuration Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Simplified Collaboration Messaging Configuration` under `Suppliers`.

## Setup Task Skill Contract

- task_code: `ORA_CMK_MNGE_SIMPLIFIED_COLLAB_MSG_CONFIG`
- task_name: `Manage Simplified Collaboration Messaging Configuration`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Simplified Collaboration Messaging Configuration` under `Suppliers`.

## Setup Task Metadata

- Task name: `Manage Simplified Collaboration Messaging Configuration`
- Task code: `ORA_CMK_MNGE_SIMPLIFIED_COLLAB_MSG_CONFIG`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

Before exporting or importing this task's setup data, verify that
`ORA_CMK_B2B_DOCUMENT_SETUP` is enabled on the exact source or destination
Fusion host selected for the operation. Use the shared Core REST client for
this read-only preflight before an export process is created or an import
approval is presented:

```text
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  --properties <selected-fusionEnv.properties> \
  --method GET \
  --query "q=FeatureCode='ORA_CMK_B2B_DOCUMENT_SETUP'" \
  --query "fields=FeatureCode,FeatureType,EnabledFlag" \
  --query "onlyData=true" \
  /fscmRestApi/resources/11.13.18.05/features
```

Confirm that `restBaseUrl` resolves to the selected host and proceed only when
the response contains exactly one item with `FeatureCode:
ORA_CMK_B2B_DOCUMENT_SETUP`, `FeatureType: FEATURE`, and `EnabledFlag: Y`.
Recheck for each operation and target. If
Fusion returns `EnabledFlag: N`, show: "Simplified Collaboration Messaging
Configuration export/import is blocked in {environment}: go to Navigator > My
Enterprise > Offerings, select Procurement > Opt In Features, enable Simplify
Configuration and Processing for B2B Messaging (`ORA_CMK_B2B_DOCUMENT_SETUP`),
and wait for opt-in processing to complete. Then retry this operation." Keep
missing or unreadable states
distinct from confirmed disabled.
The shared export and import CLIs do not invoke this preflight automatically;
route work through this skill.

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

For a standalone task-CSV import, use an exported FSM ZIP for this exact task.
An implementation-project configuration package and prior package upload apply
only to the separate all-object configuration-package migration. Do not impose
those package steps on the standalone Data Loader route. This task skill does
not execute the separate configuration-package migration; that operation must
be routed and approved through its own project/package workflow. Before Core
Data Loader approval, bind the completed export, immutable ZIP and SHA-256, task identity,
destination host, and Run Book context to its Task Hook validated preview.
Core Data Loader owns upload and submission. When status is explicitly requested,
use its status-only route and ProcessLog/result retrieval. Bound repeated checks
to ten minutes at intervals of at least thirty seconds. Confirm the task result
and target setup before reporting a completed import; an accepted upload or
ESS success alone is not verification. See `ora-resource/ora_input_validation.md` and
`ora-resource/ora_error_handling.md` for the route-specific gates.

Use this task metadata when invoking those skills:

- Offering: `Procurement`
- Functional area / Setup Object: `Suppliers`
- Setup task name: `Manage Simplified Collaboration Messaging Configuration`
- Setup task code: `ORA_CMK_MNGE_SIMPLIFIED_COLLAB_MSG_CONFIG`




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

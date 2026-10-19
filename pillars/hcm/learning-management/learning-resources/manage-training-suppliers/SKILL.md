---
skill_id: "hcm.learning-management.learning-resources.manage-training-suppliers"
name: "Manage Training Suppliers Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Training Suppliers under the Learning Resources functional area."
layer: "pillar"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Resources"
functional_area_code: "ORA_LEARNING_RESOURCES"
task_code: "CUSTOM_MANAGE_TRAINING_SUPPLIERS"
task_name: "Manage Training Suppliers"
parent_skill_id: "hcm.learning-management.learning-resources"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "learningTrainingSuppliers"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM learning management pillar team"
version: "0.1.4"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "execution_route_choice"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-resources/manage-training-suppliers/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-resources/manage-training-suppliers/current/"
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

# Manage Training Suppliers Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Training Suppliers` under `Learning Resources`.

## Setup Task Skill Contract

- task_code: `CUSTOM_MANAGE_TRAINING_SUPPLIERS`
- task_name: `Manage Training Suppliers`
- parent_skill_id: `hcm.learning-management.learning-resources`
- pillar: `HCM`
- offering: `Learning Management`
- functional_area: `Learning Resources`
- functional_area_code: `ORA_LEARNING_RESOURCES`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `REST`
- businessObject: `learningTrainingSuppliers`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Training Suppliers` under `Learning Resources`.

## Setup Task Metadata

- Task name: `Manage Training Suppliers`
- Task code: `CUSTOM_MANAGE_TRAINING_SUPPLIERS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `learningTrainingSuppliers`

## Execution Channel Requirements

- Before preparing the proposal, present both supported creation routes and require the user to choose `REST upload` or `Data Loader`.
- `REST upload` uses direct `POST /hcmRestApi/resources/latest/learningTrainingSuppliers` requests through the standard authenticated Fusion REST client.
- `Data Loader` uses `core.data-loader` with the registered business object `learningTrainingSuppliers`.
- Recommend REST upload for one approved create row and Data Loader for two or more approved create rows, but do not override the user's selection.
- Record the selected route in the versioned proposal. A route change invalidates the existing approval and requires a new proposal version.
- Do not create any training supplier through the Fusion browser UI.
- Use read-only `GET /hcmRestApi/resources/latest/learningTrainingSuppliers` requests for the pre-create duplicate check and the post-create verification. Do not use the browser UI for either check.
- Page the REST collection to completion. A partial first page is not evidence that no duplicate exists.
- Treat HTTP 401, 403, transport failure, incomplete paging, or an unreadable response as a blocked or unknown verification result, never as zero matches.

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `learningTrainingSuppliers` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "learningTrainingSuppliers" \
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

## Implementation Notes

Use the parent functional-area skill `hcm.learning-management.learning-resources` for functional-area sequencing and scope decisions. The latest approved OLC-116674 FDD governs functional behavior; Jira OLC-120235 provides traceability.

## Oracle Resource Read Order

Read `ora-resource/ora_input_validation.md`, `ora_reference_lookups.md`, `ora_dependency_readiness.md`, `ora_design_enforcement.md`, and `ora_error_handling.md` before preparing a proposal. Stop if the compiled registry or execution plan reports a reachable `TBD` lookup contract; never invent an endpoint.

## Functional Workflow

1. Extract one row per requested supplier and preserve each user-provided name except for leading or trailing whitespace.
2. Block the initial proposal when a row has no identifiable user-provided name. Never derive, default, translate, or recommend the supplier name.
3. After the name is collected, explicitly offer Description and Contact as **Recommended (optional)** fields. Do not call either field required and do not imply that creation is blocked when the user skips one or both. Ask in user-facing language such as:
   - `Description (Recommended, optional): Enter a description, or choose Skip.`
   - `Contact (Recommended, optional): Enter a full name, person number, person ID, or email, or choose Skip.`
   Record an explicit value or `Skip` for each recommended field before preparing the proposal. Draft a description only from supplied business context, label it skill-generated, and keep it editable.
4. Resolve a supplied contact by full name, person number, person ID, or email. Require user selection for multiple matches and allow correction or removal when the optional contact is invalid.
5. Read existing suppliers through the documented `learningTrainingSuppliers` REST `GET` contract before proposing creation. Match the normalized requested name exactly after complete paging. A same-name match is not proof of duplicate intent; show identifiers and statuses and require the user to choose whether to use an existing record or create another.
6. Prompt for Set and configured flexfields as **Conditional**. Use tenant metadata to show the accessible Set and configured Context Segment or flexfield segments, identify which configured segments are required, and allow `Skip` only for nonrequired values. If the tenant does not expose them, state `Not applicable`. Never default the Set; disclose that it is immutable after creation.
7. Prompt for Related Materials as **Optional** using customer-facing language such as `Related materials (Optional): Enter an administrator-only URL or readable file, or choose Skip.` Validate retained URLs and files, and record a value or explicit `Skip` before proposal.
8. Ask the user to choose REST upload or Data Loader, then present a versioned proposal showing the selected route, exact name, description source, resolved contact, Set and flexfields, warnings, and proposed action.
9. Require `Approve proposal vN` for the exact current version. Execute only the approved route: direct REST `POST` for REST upload, or `core.data-loader` with business object `learningTrainingSuppliers` for Data Loader.
10. After the selected mutation completes, read back each attempted creation through the documented `learningTrainingSuppliers` REST `GET` contract. Prefer the returned resource ID or resource number; require the returned name to agree with the approved value. Report supplier name, number or identifier, status, and any optional child-data failure.

Never ask for system-generated status, supplier number, supplier ID, audit fields, or creation metadata unless the selected integration explicitly requires a user-supplied resource number. Never use a browser UI as a creation, duplicate-check, or verification fallback. Never silently substitute one creation route for the approved route. Never automatically retry a failed or uncertain create. Track token usage using the manifest policy.

## Customer Prompt Contract

Ask every customer-entered category before the proposal and preserve these labels:

| Category | Field | Prompt behavior |
|---|---|---|
| Required | Name | Require a user-provided value; never suggest or generate it |
| Recommended (optional) | Description | Ask for a value or `Skip`; a skill-generated draft must use only supplied context and remain editable |
| Recommended (optional) | Contact | Ask for a person identifier or `Skip`; resolve retained values uniquely |
| Conditional | Set | Show and ask only when set filtering is enabled; required then, immutable after creation |
| Conditional | Context Segment and configured flexfields | Show configured segments and requiredness; allow `Skip` only for nonrequired segments |
| Optional | Related materials | Ask for an administrator-only URL or file, or `Skip` |
| Required workflow choice | Creation route | Ask the user to choose REST upload or Data Loader |

Tell the customer that Status, Supplier Number, Supplier ID, and audit fields are system-populated and will be reported after creation; do not request values for them.

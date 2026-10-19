---
skill_id: "hcm.learning-management.learning-resources.manage-classrooms"
name: "Manage Classrooms Setup Task Guidance"
description: "Creates Learning classrooms through a count-first workflow: one classroom uses the Learning Classrooms REST resource, while multiple or bulk classrooms use Data Loader with Excel or DAT input."
layer: "pillar"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Resources"
functional_area_code: "ORA_LEARNING_RESOURCES"
task_code: "CUSTOM_MANAGE_CLASSROOMS"
task_name: "Manage Classrooms"
parent_skill_id: "hcm.learning-management.learning-resources"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "learningClassrooms"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "HCM learning management pillar team"
version: "0.3.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "classroom_count_or_bulk_intent"
  - "bulk_source_format"
  - "classroom_values"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "classroom_creation_route"
  - "classroom_creation_result"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "hcm.global-human-resources.locations.manage-locations"
  - "core.fusion-api.apps-common.value-sets"
  - "core.fusion-api.apps-common.descriptive-flexfields"
  - "hcm.hcm-security.hcm-security-profile"
  - "hcm.hcm-security.hcm-data-role"
uses_core:
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.fusion-api.apps-common.value-sets"
  - "core.fusion-api.apps-common.descriptive-flexfields"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-resources/manage-classrooms/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-resources/manage-classrooms/current/"
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
  - "May create one approved classroom through POST /hcmRestApi/resources/latest/learningClassrooms."
  - "May route an approved multi-row Excel or DAT artifact through core.data-loader for upload and initiation."
required_privileges:
  - "Fusion privileges to read locations and classroom duplicate-check finders."
  - "Fusion privilege to create Learning Classrooms through REST for the single-classroom route."
  - "Fusion Data Loader metadata, UCM upload, and initiation privileges for the bulk route."
---

# Manage Classrooms Setup Task Guidance

## Purpose

Creates and validates Learning classrooms through a count-first route under `Learning Resources`. One classroom uses direct REST creation; multiple classrooms use the registered `learningClassrooms` Data Loader business object with Excel or DAT input.

## Setup Task Skill Contract

- task_code: `CUSTOM_MANAGE_CLASSROOMS`
- task_name: `Manage Classrooms`
- parent_skill_id: `hcm.learning-management.learning-resources`
- pillar: `HCM`
- offering: `Learning Management`
- functional_area: `Learning Resources`
- functional_area_code: `ORA_LEARNING_RESOURCES`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `REST`
- businessObject: `learningClassrooms`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Classrooms` under `Learning Resources`.

## Creation Route Selection

Before collecting classroom fields, ask exactly:

> How many classrooms do you want to create? Enter `1` for a single classroom, a number greater than `1`, or say `Bulk` if you want to create bulk data.

Route the answer as follows:

| User answer | Selected route | Required next question or action |
|---|---|---|
| `1` | Single-classroom REST | Collect one classroom, validate it, preview the exact JSON payload, obtain approval, POST once, and read it back |
| Integer greater than `1` | Data Loader bulk | Ask whether the source will be an Excel workbook or a DAT file, then collect or accept exactly that source |
| `Bulk`, bulk upload, mass creation, or an existing multi-row file | Data Loader bulk | Ask whether the source is Excel or DAT when the format is not already evident |
| Missing, zero, negative, fractional, or unclear | Blocked | Ask the count-or-bulk question again; do not collect payload fields or select an executor |

If the user selected bulk and has no file yet, ask exactly:

> Do you want to prepare the bulk classrooms in an Excel workbook or a DAT file?

Do not implement bulk creation as a loop of individual REST POST requests. If an uploaded Excel or DAT source contains exactly one classroom, disclose the mismatch and ask whether to use the normal REST route or explicitly continue with Data Loader. Never change routes after approval without rebuilding the preview and obtaining the approval required by the newly selected route.

## Setup Task Metadata

- Task name: `Manage Classrooms`
- Task code: `CUSTOM_MANAGE_CLASSROOMS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `learningClassrooms`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.


## Download Fusion Data Loader Sample

Use this workflow when the multiple-or-bulk route is selected and a Fusion Data Loader sample is needed for the task's business object.

1. Confirm from live Data Loader metadata that `learningClassrooms` is the exact registered FSCR Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "learningClassrooms" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow. Generate a DAT sample only when the user explicitly selects DAT.



## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `classroom_count_or_bulk_intent`
- `bulk_source_format`
- `classroom_values`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `classroom_creation_route`
- `classroom_creation_result`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.learning-management.learning-resources` for functional-area sequencing and scope decisions. The latest approved OLC-116674 FDD governs functional behavior; Jira OLC-120236 provides traceability.

## Oracle Resource Read Order

Read `ora-resource/ora_input_validation.md`, `ora_reference_lookups.md`, `ora_dependency_readiness.md`, `ora_defaulting_rules.md`, `ora_design_enforcement.md`, and `ora_error_handling.md` before preparing a proposal. Stop if the compiled registry or execution plan reports a reachable `TBD` lookup contract; never invent an endpoint or assume one country's address rules apply to another.

## Functional Workflow

1. Ask the mandatory count-or-bulk question in `Creation Route Selection`. Do not choose REST or Data Loader from an attachment name alone.
2. For one classroom, preflight `/hcmRestApi/resources/latest/learningClassrooms/describe` and select the single-classroom REST contract. For multiple or bulk classrooms, preflight the registered `learningClassrooms` Data Loader metadata and template.
3. Collect every required business field for each classroom: Title, Description, and one existing HCM Location. Preserve each user-provided Title except for outer whitespace; never derive or recommend it.
4. Ask for Description. Only after explicit one-time acceptance may the exact Title be used as its default, and disclose that default in the proposal.
5. Ask each optional business field separately and allow an explicit Skip: Owner, Capacity, Contact, Training Supplier, and initial Status when the selected live contract documents an accepted value. Do not silently omit an optional-field question.
6. Ask conditional business fields only when applicable: Set Code and configured descriptive flexfield context and segments. Do not require or prompt for a Data Loader identity in an ordinary create. Validate `ClassroomResourceNumber` or the complete `SourceSystemOwner` and `SourceSystemId` pair only when the user explicitly supplies that mapping for an integration or migration.
7. Resolve Location through `locationsLov`; retained Owner and Contact through `workersLov`; Set through `hcmSetsLOV`; and route-specific writable fields through the selected live contract. Never choose among multiple matches automatically.
8. When no accessible active location with address details matches, preserve the affected row as blocked and hand off location setup to `hcm.global-human-resources.locations.manage-locations`. Require validated location identifier, code, name, address, and status evidence, then re-run `locationsLov` before resuming.
9. A Training Supplier can be populated by its exact resource ID or number only after verification. A name-only supplier remains blocked until its read-only lookup contract is documented; offer Skip rather than inventing a service.
10. Treat related materials as a separate post-create workflow. Do not include them in the direct classroom JSON or the `learningClassrooms` loader artifact.
11. When an explicit integration or migration ClassroomResourceNumber is retained, run `findByClassroomNumber` and block on an exact existing number. For every ordinary create, run `findByKeyword` with the Title, retain exact case-insensitive same-title candidates after paging, and show them as informational because Title is not unique. Never issue an unfiltered `learningClassrooms` collection GET.
12. For the REST route, map only live-writable attributes and build one exact JSON proposal. Require route-specific approval bound to the environment, endpoint, method, and immutable JSON body.
13. Submit the approved REST payload exactly once through `core.fusion-api.rest-api-client` to `POST /hcmRestApi/resources/latest/learningClassrooms`. Read back the returned item by its generated classroom number or canonical item link and reconcile submitted and generated values.
14. For the Data Loader route, ask Excel or DAT when the format is not known. Accept `.xlsx` for Excel, or `.dat` or a ZIP containing the validated DAT for DAT. Route the source, task context, and business object `learningClassrooms` through `core.data-loader`; do not call UCM or initiation endpoints directly.
15. Let `core.data-loader` perform mapping, live-schema validation, immutable artifact preparation, Task Hook validation, approval, upload, and initiation. Its approval workflow is authoritative; do not add a second task-level approval prompt.
16. Validate bulk rows independently before approval. Show valid, blocked, and excluded rows, but never silently drop an invalid classroom. A change to any row or source file invalidates the current preview.
17. After a Data Loader initiation, return its authoritative report. Check status only when the user explicitly asks for status, progress, results, counts, or errors.
18. Track token usage using the manifest policy and preserve the selected route and sanitized verification result in the project workspace.

## Single-Classroom REST Contract

- Executor: `core.fusion-api.rest-api-client`.
- Endpoint: `POST /hcmRestApi/resources/latest/learningClassrooms`.
- Minimum route mapping: Title to `classroomTitle`, Description to `classroomDescription`, and resolved LocationId to `classroomLocationId`.
- Optional capacity mapping: `classroomCapacity`, only when the user supplies a whole number.
- Include any other optional field only when the current `describe` response confirms it is writable and the user retained the value.
- Omit classroom ID, classroom number, audit values, status, owner, contact, supplier, and readiness-override fields unless the current contract and user input explicitly support them.
- Present the exact environment, endpoint, HTTP method, and JSON payload immediately before approval. Any payload or environment change invalidates approval.
- POST once. Verify success through a read-only item GET and return the generated classroom ID, number, status, and persisted business values.

## Bulk Data Loader Contract

- Executor: `core.data-loader`.
- Registered business object: `learningClassrooms` under Fusion Setup and Configuration Registry.
- Excel mode accepts an `.xlsx` workbook with one classroom per populated root row. Generate the editable live-metadata sample when the user needs a template.
- DAT mode accepts an explicit `.dat` source or validated ZIP containing the DAT. Generate a DAT sample only when the user explicitly selects DAT.
- The declared classroom count must equal the normalized nonblank classroom-row count before approval. A mismatch blocks until the count or source is corrected.
- Preserve Data Loader's immutable preview, Task Hook, upload, initiation, and reporting contracts.

## Route Fallback Discipline

- A known local preparation failure before an HTTP request is dispatched may be corrected without changing the approved REST payload; disclose that no request was sent.
- A known REST validation or HTTP 4xx failure does not authorize Data Loader automatically. Offer a route change, rebuild the Data Loader artifact, and use Data Loader's approval workflow.
- A timeout, connection loss, HTTP 5xx response, or other uncertain REST outcome requires read-only reconciliation before any second write or route change.
- Never retry a REST POST, replay a Data Loader upload, or switch executors merely because creation was not immediately visible.

## Diagnostic Redaction

- Before displaying or persisting diagnostics, redact authorization headers, access and refresh tokens, cookies, credentials, client secrets, private keys, token-cache content, tenant secrets, and strings that resemble bearer tokens or private-key material.
- Never print or persist a full base64 payload, an unredacted REST request or response containing customer-sensitive values, or classroom source rows beyond the minimum business evidence needed for reconciliation.
- Persist only sanitized environment identity, endpoint path, HTTP status, ECID or request identifier, failure classification, row-safe validation summary, approval fingerprint, and verification result.
- If redaction prevents a required value from being verified safely, stop before execution and report the blocking validation rather than weakening redaction.

Do not request or populate ClassroomResourceId, GUID, audit values, availability, or other read-only/system-generated values. Do not ask for ClassroomResourceNumber or source-system keys in an ordinary create; leave them omitted so Fusion can generate or manage identity. If the user explicitly supplies an integration or migration identity, validate either ClassroomResourceNumber or the complete source-system key pair before retaining it. Never automatically retry a failed or uncertain create. Track token usage using the manifest policy.

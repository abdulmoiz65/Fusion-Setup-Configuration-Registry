---
skill_id: "hcm.learning-management.learning-resources.manage-instructors"
name: "Manage Instructors Setup Task Guidance"
description: "Prepare standalone Learning instructor creation from an explicitly supplied or selected HCM person, including partial-name discovery, duplicate checks and approval-gated shared Data Loader handoff. Excludes supplier association and instructor updates."
layer: "pillar"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Resources"
functional_area_code: "ORA_LEARNING_RESOURCES"
task_code: "CUSTOM_MANAGE_INSTRUCTORS"
task_name: "Manage Instructors"
parent_skill_id: "hcm.learning-management.learning-resources"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "learningInstructors"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM learning management pillar team"
version: "0.2.1"
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
uses_core:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
  - "core.data-loader.task-hook"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-resources/manage-instructors/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-resources/manage-instructors/current/"
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
  - "Declared shared GETs may authenticate and read accessible people and instructors only after readiness."
  - "Creation uses the shared Data Loader exact-artifact approval workflow; no private writer."
required_privileges:
  - "WLF_MANAGE_TRAINING_RESOURCES"
  - "WLF_MANAGE_TRAINING_RESOURCES_DATA"
  - "PublicPerson data access and applicable shared Data Loader privileges"
---

# Manage Instructors Setup Task Guidance

## Purpose

Prepare standalone instructors from explicitly nominated HCM people, using shared
FSCR reads, validation and Data Loader approval. No instructor update or supplier
association is enabled by this package.

## Setup Task Skill Contract

- task_code: `CUSTOM_MANAGE_INSTRUCTORS`
- task_name: `Manage Instructors`
- parent_skill_id: `hcm.learning-management.learning-resources`
- pillar: `HCM`
- offering: `Learning Management`
- functional_area: `Learning Resources`
- functional_area_code: `ORA_LEARNING_RESOURCES`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `REST`
- businessObject: `learningInstructors`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill to prepare standalone instructors, find a nominated person, check
an existing instructor or verify a separately requested creation result.

## Setup Task Metadata

- Task name: `Manage Instructors`
- Task code: `CUSTOM_MANAGE_INSTRUCTORS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `learningInstructors`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `learningInstructors` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "learningInstructors" \
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

Use the parent functional-area skill `hcm.learning-management.learning-resources` for functional-area sequencing and scope decisions. The latest approved OLC-116674 FDD governs functional behavior; Jira OLC-120237 provides traceability.

## Oracle Resource Read Order

Read `ora-resource/ora_input_validation.md`, `ora_reference_lookups.md`, `ora_dependency_readiness.md`, `ora_design_enforcement.md`, and `ora_error_handling.md` before preparing a proposal. Stop creation preparation if the compiled registry or execution plan reports a reachable `TBD` lookup contract; never invent an endpoint or infer a person from contextual clues. Independent discovery follows the read-only route below, not the create graph.

## Functional Workflow

1. Extract one row per instructor using a supplied full name, person number, person ID or partial-name search. Email resolution is not enabled. Never infer a person from job, department, location, supplier, manager or another row.
2. Resolve the person against accessible HCM data. Show display name, person number, department, location when available, and worker-assignment status. Require user selection for ambiguous matches.
3. Check whether the resolved person already has an instructor resource. Show its identifier and status and exclude that row from creation.
4. Keep training supplier absent for this standalone scope. Ask to remove/defer supplied supplier inputs rather than silently dropping them.
5. Require configured mandatory flexfields and an accessible Set when enabled. Never default the Set; disclose that it is immutable after creation.
6. Defer materials and virtual-classroom accounts explicitly; child loading is not implemented here.
7. Only ACTIVE assignments are enabled in this increment. FDD inactive/terminated behavior conflicts with the UI create finder; suspended is not silently treated as active. Block these cases pending verified contracts.
8. Present a versioned proposal showing the verified person identity, assignment status, supplier, Set and flexfields, warnings, and proposed action.
9. Use one shared Data Loader approval for the final immutable artifact and current proposal. Earlier identity confirmation is not upload approval; do not ask for an additional generic proposal approval.
10. Return the shared initiation report immediately. Only after a separate status/results request use shared job/error checks and person-based readback. Report instructorStatus, generated identifiers, supplier omission, unknown defaults and unverified scheduling availability separately.

Never ask for system-generated instructor number, ID, status, availability, person display values, department, location, or audit fields. Never automatically retry a failed or uncertain create. Track token usage using the manifest policy.

## Standalone implementation boundary

This increment implements local intake, candidate/identity rules, proposal versions,
readback evaluation and root-archive cross-checks. It does not certify live creation.
The root-only configuration resolver requires an explicit recorded user deferral
of Set filtering and live evidence of optional global DFF fields without an
advertised context default. Run `validate-configuration` as described in
[prerequisite inspection](references/prerequisite-inspection.md) before every
create preview. A planned graph is not a passed check. Do not treat unknown
configuration as disabled or fabricate a Task Hook result. Set-enabled creation
and supplied/required custom values remain unavailable pending verified mappings.

For an explicit person search or duplicate check, `lookup` and `check-existing`
use independent read-only readiness from [person-resolution](references/person-resolution.md).
Require the selected environment AND exact origin, validate person input, and
use only the declared shared GET client and fixed source-backed queries. A pending
Run Book, unknown create-only Set/DFF configuration or invalid loader template does
not block these reads. Read readiness never clears the create graph, Task Hook,
privileges, artifact validation or approval. Post-create `readback` retains its
existing graph gate. No upload or write command is introduced.

For an explicit request to inspect prerequisites, the separate metadata-only route
in [prerequisite inspection](references/prerequisite-inspection.md) uses its own
target/operation checks. It can read the declared instructor describe endpoint
without claiming the create graph is ready. Metadata inspection alone does not enable
person lookup, uploads, deployments or create validation; person discovery uses
the separate checks above.

Training suppliers, materials, provider accounts, email resolution and lifecycle
writes are unavailable here. If supplied, ask to remove/defer the unsupported input;
do not silently discard it. Required tenant configuration cannot
be deferred: the minimal root adapter blocks additional mandatory fields until a
verified mapping is implemented.

## Implementation read order

- Read [person-resolution](references/person-resolution.md) for identifiers,
  partial names, explicit candidate selection and bounded shared GETs.
- Read [create-contract](references/create-contract.md) before preparation,
  Task Hook, approval, submission or separately requested readback.
- Read [acceptance-matrix](references/acceptance-matrix.md) for implemented versus
  blocked/deferred behavior. Source behavior is not target acceptance.
- Read all five task-local ora-resource files and the shared execution guide
  before executing the graph. Use the shared planner without overrides.

## Local tools and privacy

Requires Python 3.11+. `scripts/instructor_workflow.py --help` lists intake,
readiness, lookup, existing-instructor, readback and archive-check commands.
`scripts/instructor_validation.py` supplies pure business rules, not network code.
No command uploads or creates an instructor. Follow the shared handoff in the
create-contract reference; do not interpret a local pass as write readiness.

Example local intake: `python3.11 <skill>/scripts/instructor_workflow.py
validate-request --input <private-request.json>`. The request schema is in
`schemas/instructor-request.schema.json`. The helper returns exit 2 on a blocker,
0 on a local result; inspect pagination completeness and verification status too.

Keep real-person candidates, proposals and load files in protected untracked
runtime storage outside `project/`; use only synthetic people in tracked tests.
Project records contain sanitized counts, hashes, source references and outcomes,
not identities, raw responses or authentication material. Runtime results shown
to an authorized requester are not permission to store a personnel roster.

Reviewer: HCM Learning pillar reviewers; shared service ownership remains central.

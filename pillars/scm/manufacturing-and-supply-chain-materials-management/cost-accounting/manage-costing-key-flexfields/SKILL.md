---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.cost-accounting.manage-costing-key-flexfields"
name: "Manage Costing Key Flexfields Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Costing Key Flexfields under the Cost Accounting functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Cost Accounting"
functional_area_code: "CST_DEFINE_COST_MANAGEMENT"
task_code: "CST_MANAGE_COSTING_KEY_FLEXFIELDS"
task_name: "Manage Costing Key Flexfields"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.cost-accounting"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM manufacturing and supply chain materials management pillar team"
version: "1.0.2"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "affected_flexfield_codes"
  - "setup_data_artifacts"
  - "approved_change_set"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "deployment_preflight_result"
  - "import_change_report"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "core.fusion-api.apps-common.key-flexfields"
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
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/manage-costing-key-flexfields/current/costing-kff-setup-task-plan.json"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/manage-costing-key-flexfields/current/costing-kff-setup-data-routing.json"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/manage-costing-key-flexfields/current/costing-kff-validation-checkpoints.json"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/manage-costing-key-flexfields/current/costing-kff-deployment-preflight.json"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/manage-costing-key-flexfields/current/import-change-report.md"
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

# Manage Costing Key Flexfields Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Costing Key Flexfields` under `Cost Accounting`.

## Setup Task Skill Contract

- task_code: `CST_MANAGE_COSTING_KEY_FLEXFIELDS`
- task_name: `Manage Costing Key Flexfields`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.cost-accounting`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Cost Accounting`
- functional_area_code: `CST_DEFINE_COST_MANAGEMENT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Costing Key Flexfields` under `Cost Accounting`.

## Setup Task Metadata

- Task name: `Manage Costing Key Flexfields`
- Task code: `CST_MANAGE_COSTING_KEY_FLEXFIELDS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

## Deployment-State Preflight

Before preparing a change for an affected Costing KFF, obtain each exact
flexfield code from the approved scope (for example, `VALU` or `CONS`). Do not
infer affected codes from a partial export.

Use `core.fusion-api.apps-common.key-flexfields` to read a submitted
deployment job's state for application ID `707`. A returned job state of
`DEPLOYED` is positive deployment evidence. A response with no job ID and a
message that deployment is “not Submitted” is neither a failure nor proof of
deployment: it means that no deployment job exists for that API route. Do not
require UI access solely to resolve this result.

For a no-job result, continue with an automated fresh task-level export and
verify that its parent data includes every expected affected KFF code and that
the approved target records are present. A complete validated export is the
operational preflight for change preparation; a missing expected code or target
record is a blocker and must be reported as an incomplete-export prerequisite.
This prevents a modified, undeployed KFF from silently becoming the basis for a
candidate archive without making UI access mandatory.

Record the code, environment, job-state result, export-completeness result,
evidence source, and timestamp in the validation artifact. A transient job
state such as `DEPLOYING`, a reported deployment error with a job ID, or an
incomplete validated export is a deployment preflight blocker.

When two or more expected KFF roots are absent from the export and their
deployment-job results are `not Submitted`, issue an advisory rather than
automatically deploying. Identify the missing codes and offer exactly these
recovery paths: (1) the user deploys the affected KFFs manually in the
delivered UI and requests a fresh export, or (2) the user requests API
deployment for named codes. The latter routes through the core KFF skill and
requires its exact pre-POST approval for each deployment request. Do not
prepare, import, or deploy a candidate archive until a fresh export contains
all expected roots and approved target records.

When blocked, present the affected code and observed status and request a
decision. Never deploy implicitly: if deployment is requested, route it to the
core KFF skill and obtain its separate immediate pre-POST approval. After a
successful deployment, re-read the status and proceed only if it is
`DEPLOYED`.

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Cost Accounting`
- Setup task name: `Manage Costing Key Flexfields`
- Setup task code: `CST_MANAGE_COSTING_KEY_FLEXFIELDS`

### FSM Import Semantics and Change Control

FSM CSV import is merge-oriented. A target record that is absent from a
configuration package is not deleted; omission is not a delete instruction.
Use a fresh task-level export as an immutable baseline for comparison and
recovery evidence, not as a requirement to re-enter or recreate all existing
Costing KFF setup data.

For every candidate import:

1. Capture a fresh baseline export before preparing the candidate archive.
2. Perform the **exact duplicate-key gate** below against that same baseline
   before writing or copying any proposed KFF row.
3. Declare the approved change set by business-object key and field: only
   additions and explicitly approved updates are eligible for import.
4. Compare the candidate with the baseline and produce an import change report
   that identifies added rows, updated fields, unchanged rows, required parent
   rows, and any unexpected differences.
5. Preserve required CSV files, headings, `ASM_SETUP_CSV_METADATA.xml`, and
   parent/dependency rows. Never delete a CSV file or manually alter generated
   metadata to simulate a delete.
6. Treat the validated candidate ZIP as immutable. Any row, metadata, or ZIP
   member change requires a new validation and approval cycle.

#### Exact Duplicate-Key Gate for Costing KFF Candidates

Parse the fresh baseline CSV members with a CSV-aware parser and resolve each
requested record by its complete exported identity. Do not infer absence from a
partial member, a prior candidate, or an earlier export. Use these keys:

| Record | Required exact key |
| --- | --- |
| Structure | `KeyFlexfieldCode`, `ApplicationId`, `StructureCode` |
| Structure segment | structure key plus `SegmentCode` |
| Structure segment label | structure key plus `SegmentCode`, `SegmentLabelCode` |
| Structure instance | `KeyFlexfieldCode`, `ApplicationId`, `StructureInstanceCode` |
| Instance segment mapping | instance key plus `SegmentCode` |

For every requested create, record the baseline match count and compare all
user-managed fields of a single exact match with the requested values.

- A match count greater than one is ambiguous and blocks candidate preparation.
- When exactly one matching record has equivalent user-managed values, classify
  it as `already_configured`. Stop as a no-op: do not create a ZIP, request
  import approval, import, or deploy that record again.
- When exactly one matching record differs, classify it as `existing_conflict`.
  Stop and show the differing fields; proceed only after the user explicitly
  authorizes an update to that exact record. Do not append a duplicate create
  row.
- Only a zero match count permits a create row. After assembling the candidate,
  repeat the key check across its CSV members and block any duplicate key unless
  it is the one explicitly approved update row.

The import change report and validation checkpoints must show each requested
key, its baseline match count, the classification (`create`,
`already_configured`, `existing_conflict`, or `approved_update`), and the
evidence member. An absent structure does not prove that its instance or
segment mappings are absent; evaluate every requested record independently.

### CSV Shape Validation

Before packaging or presenting any FSM candidate for approval, parse every
CSV member with a CSV-aware parser. Require every data row, including retained
baseline rows and newly added or updated rows, to contain exactly the same
number of fields as that member's header. Preserve quoted values and trailing
empty fields; do not use line-oriented or delimiter-count checks as a
substitute. A row-width mismatch is an import blocker because Fusion can
create earlier parent rows and then stop processing the remaining rows in that
CSV member.

Use a fresh task export as the baseline. Use a full baseline-derived candidate
only when a smaller candidate cannot be produced and validated safely. A
smaller delta archive is permitted only when the task's generated package,
metadata, and dependency validation prove that it is task-valid; do not
hand-assemble a delta ZIP by removing rows from a full export.

#### Import Change Report Contract

Before import, persist `import-change-report.md` at the manifest's
`import_change_report` workspace-output location. It is a validation artifact,
not an import authorization. It must identify the target environment and task,
the baseline and candidate archive names and hashes, the approved additions and
updates by record key and field, retained required CSV and metadata members,
any omitted rows classified as no-change rather than delete, validation
findings, and the approval reference or blocker. Do not include credentials,
tokens, or sensitive setup values that are unnecessary for review.

Do not infer a delete capability from FSM omission. When Costing KFF
configuration must be retired, first check dependencies and use the delivered
UI's supported lifecycle action. If deletion is unavailable, explicitly set
the disposable structure or structure instance to `Enabled = N`, import that
approved update when using FSM, deploy the KFF, and verify that it is no
longer available at runtime. Record this as retirement, not deletion.

### Editing a Consumed VALU Structure or Instance

Do not treat the delivered UI allowing an edit or save as proof that a VALU
structure or structure instance is unused. Before an approved edit, identify
the dependent valuation structures and downstream cost-profile use of the
target structure instance, assess compatibility with existing combinations,
and record the result in the import change report. Do not alter segment order
after deployment; use only the explicitly approved compatible field changes.
Require post-deployment verification of the affected valuation configuration.

### CONS Required Segment Labels

For application `707` and key flexfield `CONS`, every new or changed structure
must assign each of these delivered required segment labels to an **enabled**
segment before deployment:

- `CST_CONS_OWNER_NAME`
- `CST_CONS_OWNER_TYPE`
- `CST_CONS_ORIGINAL_RECEIPT_NUM`

Use a distinct, semantically appropriate, enabled segment for each label. A
new custom label does not replace a required delivered label. A label assigned
only to a disabled segment does not satisfy the requirement. The metadata error
`FND-2742` is a deployment blocker, not an import success condition.

Validate metadata after assigning all three labels and treat any further
reported required-label error as an additional explicit requirement for the
candidate.

## KFF Post-Import Deployment

After `core.data-loader` reports that the exact approved FSM ZIP completed
successfully, invoke `core.fusion-api.apps-common.key-flexfields` to deploy
each affected Key Flexfield before using a subsequent task export as the basis
for another change. Deployment compiles the imported metadata; it is not part
of the CSV import and must not run after an incomplete or failed import. A
successful import alone is not sufficient export-completeness evidence: an
undeployed structure can be absent from a later FSM export.

This applies to every successful Costing KFF FSM import, including VALU and
CONS, and including an instance-only or instance-segment-mapping change.
Before post-import validation or reporting the requested configuration as
confirmed, present the separate deployment request and obtain explicit approval
for each affected KFF.

After a verified successful import and before any deployment POST, present the
user with the exact target environment, application ID, flexfield code,
deployment endpoint, and immutable JSON payload. Obtain a separate explicit
deployment approval at that point. Import approval never authorizes deployment,
and deployment approval never authorizes a different flexfield or payload.

### Environment-Neutral Approval Language

Never hardcode an environment label in an approval message or copy one from
test evidence, a prior run, or an example. Resolve the target name from the
active Fusion environment configuration immediately before approval. Lead with
a plain-language summary of the deployment and its resolved target; place the
exact endpoint and immutable payload as supporting approval evidence. If no
friendly environment name is configured, say “configured Fusion environment”
and include the resolved host. Do not omit the target, endpoint, or payload
evidence required by the core KFF deployment workflow.

Before the core KFF skill can submit a deployment, provide the confirmed target
Fusion environment, `application_id`, exact `flexfield_code`, and optional
`forceDeployment` value. Do not infer these identifiers. The only accepted
force values are the strings `"true"` and `"false"`; when omitted, the core
skill uses `"false"`.

The core KFF skill owns the REST transport and approval gate. Immediately
before its deployment POST, it must present the exact environment, endpoint,
and immutable JSON payload and obtain explicit approval. It records the
deployment job ID, deployment status, validation status, report, error message,
and response links. For a requested status check, it uses the same resolved
identifiers and stops on a terminal outcome or timeout.

For a change set affecting more than one KFF, submit deployments serially.
Immediately before each individual POST, obtain a separate explicit approval.
Present the request in plain language while retaining its exact meaning: target
environment, application ID, flexfield code, deployment endpoint, and whether
force deployment is enabled. For example: “Deploy VALU metadata in the target
Fusion environment for application 707, using the standard non-force setting.”
Approval for one code
does not authorize the next code or parallel deployment. Wait for each
deployment to reach `DEPLOYED` before requesting approval for, and then
submitting, the next code; parallel deployment can collide on shared Flexfield
metadata.

When a change creates a new structure with segments or required label mappings
and also needs a structure instance, use two FSM imports. Stage one contains
the structure, segments, and label mappings only. After its successful import,
deploy every affected KFF serially. Stage two is permitted only after a fresh
task export confirms the new structure; it contains the structure instance and
its instance-segment mappings. Do not put a new structure and an instance that
references it in the same FSM import: Fusion can reject the instance with
`StructureCodeLOV`/`JBO-25072` because the new structure is not yet available
to that lookup.

After all affected codes are `DEPLOYED`, use the deployment-state GET only as
confirmation of terminal status; it does not force a metadata refresh. Create
a fresh task-level data export and verify that every approved target record is
present before preparing any follow-up candidate archive. If the first export
is incomplete immediately after deployment, sleep and retry only the
read-only export, up to three additional attempts, with bounded backoff of
15–30 seconds. Record each ProcessId, attempt number, wait interval, and
observed completeness result. If the target record remains absent after the
three retries, stop as an incomplete-export blocker rather than preparing the
next candidate. Tell the user: "The deployed metadata is not yet present in
the setup-task export after three retries. Please verify it manually, or wait
for metadata propagation and request another export retry." Do not imply that
deployment failed solely because this propagation check is incomplete.

Do not create or resolve a registered Data Loader business object for this
task. Its supported setup-data route is FSM CSV Import, identified by the
validated task context and immutable ZIP.

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `affected_flexfield_codes`
- `setup_data_artifacts`
- `approved_change_set`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `deployment_preflight_result`
- `import_change_report`
- `skill_run_record`
- `token_usage_record`

## Machine-Readable Output Contract

Persist each task-specific planning or validation output as a UTF-8 JSON object
at its corresponding manifest `workspace_outputs` location. Each document must
include these common fields:

- `schema_version`: `"1.0"`
- `skill_id`: this skill's manifest `skill_id`
- `project_id`
- `artifact_type`
- `status`: `draft`, `reviewed`, `approved`, `blocked`, or `failed`
- `created_at` and `updated_at`: RFC 3339 timestamps
- `task_context`: object with `task_code`, `task_name`, `offering`, and
  `functional_area`
- `evidence_refs`: array of project-relative artifact paths or immutable archive
  hashes; never include credentials, tokens, or unnecessary sensitive values

Register each persisted JSON artifact with
`core.project-mgmt.artifact-registry-manager` using the required metadata in
`schemas/project-artifact.schema.json`. The JSON content below is the stable
task-level contract consumed by downstream workflow stages.

| Output | JSON artifact | Required task-level fields |
| --- | --- | --- |
| `setup_task_plan` | `costing-kff-setup-task-plan.json` | `objective`, `approved_change_set_ref`, `affected_flexfield_codes`, `preconditions`, `ordered_actions`, `approval_gates`, `postconditions` |
| `setup_data_routing` | `costing-kff-setup-data-routing.json` | `baseline_export_route`, `setup_data_validation_route`, `reference_data_validation_route`, `import_route`, `deployment_route`, `routing_decision`, `blocking_conditions` |
| `validation_checkpoints` | `costing-kff-validation-checkpoints.json` | `baseline_comparison`, `csv_shape_validation`, `dependency_validation`, `metadata_validation`, `retirement_validation`, `overall_result` |
| `deployment_preflight_result` | `costing-kff-deployment-preflight.json` | `environment`, `flexfield_results`, `export_completeness_result`, `evidence_source`, `decision`, `blocking_conditions` |

`flexfield_results` must contain one object per approved flexfield code with
`flexfield_code`, `application_id`, `deployment_job_state`, `job_id` when
available, `status`, and `evidence_refs`. Each validation checkpoint must
include `name`, `status`, `evidence_refs`, and `failure_class` when its status
is `blocked` or `failed`.

The Markdown `import-change-report.md` remains the review artifact defined in
the Import Change Report Contract. It must link to the relevant JSON artifact
paths and immutable archive hashes; it is not a replacement for the JSON
planning or validation records.

## Implementation Notes

Use the parent functional-area skill `scm.manufacturing-and-supply-chain-materials-management.cost-accounting` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

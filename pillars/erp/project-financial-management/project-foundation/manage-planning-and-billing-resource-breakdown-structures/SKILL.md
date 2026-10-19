---
skill_id: "erp.project-financial-management.project-foundation.manage-planning-and-billing-resource-breakdown-structures"
name: "Manage Planning and Billing Resource Breakdown Structures Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Planning and Billing Resource Breakdown Structures under the Project Foundation functional area."
layer: "pillar"
pillar: "ERP"
offering: "Project Financial Management"
functional_area: "Project Foundation"
functional_area_code: "ORA_PJF_PROJECT_FOUNDATION_FA"
task_code: "PJF_MANAGE_PLANNING_BILLING_RESOURCE_BREAKDOWN_STRUCTURES"
task_name: "Manage Planning and Billing Resource Breakdown Structures"
parent_skill_id: "erp.project-financial-management.project-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP project financial management pillar team"
version: "0.1.2"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-planning-and-billing-resource-breakdown-structures/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-planning-and-billing-resource-breakdown-structures/current/"
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
  - "Writes declared task planning/validation artifacts and the task-owned immutable create package through the documented serializer and core project services."
  - "Delegates scoped exports and approved imports to the declared shared/core workflows under their existing gates."
required_privileges: []
---

# Manage Planning and Billing Resource Breakdown Structures Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Planning and Billing Resource Breakdown Structures` under `Project Foundation`.

## REST Request Preflight

Before any workflow-selected REST request, apply the offering's
[REST version and query compatibility preflight](../../references/rest-query-compatibility.md).
Determine the effective framework version from the selected core client or
workflow, construct compatible query parameters, and verify that the outgoing
header agrees. Do not hardcode a separate pillar version. Existing route,
validation, classification/matching, persistence and approval gates still apply.

## Setup Task Skill Contract

- task_code: `PJF_MANAGE_PLANNING_BILLING_RESOURCE_BREAKDOWN_STRUCTURES`
- task_name: `Manage Planning and Billing Resource Breakdown Structures`
- parent_skill_id: `erp.project-financial-management.project-foundation`
- pillar: `ERP`
- offering: `Project Financial Management`
- functional_area: `Project Foundation`
- functional_area_code: `ORA_PJF_PROJECT_FOUNDATION_FA`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Planning and Billing Resource Breakdown Structures` under `Project Foundation`.

## Supported Task Behavior

The authored rules cover **new custom PLANNING resource breakdown structures only**. They accept customer business values for Name, Project Unit, and From Date, with the observed optional inputs and resource rows documented in `ora-resource/ora_input_validation.md`. The observed create profile covers Resource Class, Named Person, Project Nonlabor Resource, Organization, Job, Expenditure Type, Expenditure Category, an actual `Job: Expenditure Category` child, and a format-only `Organization: Inventory Item` selection. Other descendants are not established by the current UI and FSM import/readback evidence; an exported format ID alone does not establish a new-create rule.

For UI-equivalent minimum creation, the FSM package must explicitly contain the Resource Class format and root plus four class elements. A sparse header/version import does **not** create that tree. Reconcile the new header, version, target-language translations, format hierarchy, and element tree against a fresh complete same-task export. Obtain the Project Unit and conditional Organization CSV context without prevalidating their name, classification, or date eligibility; Fusion import makes those business-validity decisions. Keep the proven Set, Job and Person conversions. Unknown context or conversion contracts fail closed; do not guess codes, IDs, dates, or enterprise values. Update, end-date, delete, and billing-maintenance requests are outside this authored create-only workflow and must not be routed through it.

Use task-scoped FSM CSV; the project-assignment REST resource is not a setup-definition write contract.

## Setup Task Metadata

- Task name: `Manage Planning and Billing Resource Breakdown Structures`
- Task code: `PJF_MANAGE_PLANNING_BILLING_RESOURCE_BREAKDOWN_STRUCTURES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Obtain one complete current task-scoped package through `shared.setup-export.task-level-export` in data-export mode, retaining all target-supported header, version, translation, format, and element members. A failed or partial export is a blocker, never evidence of absence. Do not invent package members or columns.
2. Perform [Task Plan Validation and Execution](#task-plan-validation-and-execution) using this skill, the shipped registry and its reachable source rules. Record a `planned` / `ready` plan without an override before evaluating the graph or serializing the package.
3. After every required lookup and the format-label-to-ID mapping has been independently validated against the same target, use the [offline batch serializer](scripts/build_prbs_create_package.py) to build one consolidated create-only seven-member package for all new structures and resource rows. Include the explicit Resource Class default tree for each structure and only the observed additional format/resource paths and proven parent closure; do not infer untested descendants.
4. Validate new RBS identity, planning type, date shape, CSV context presence, conditional code/number conversions, tested formats, class/curve choices, element tree, and observed flags. Do not decide Project Unit or Organization business eligibility before Fusion import. Stop on missing source-backed context or serialization contracts.
5. Produce an immutable preview and checksum.
6. Delegate the final immutable archive to `core.data-loader`. Its read-only Task Hook validates the final artifact before the loader's own approval gate. `RBS.RETURN_SUCCESS` means task validation/preparation completed; it neither supplies upload approval nor certifies an import. The loader owns approval and submission; do not add a second task approval or call an import adapter directly.
7. Accepted initiation is terminal for that request and means in progress. Return the loader's complete `Data Load In Progress` Markdown verbatim. Do not automatically poll, retrieve logs, export again, or create loader result/failure files or run records. Never retry an uncertain or failed submission automatically.
8. Only on a later explicit request for status, progress, results, counts, errors, or verification, select the loader's status workflow. Bind the returned request or UCM identifier to the same target, task, and approved artifact context; missing or conflicting identity blocks the check. Do not repeat preparation, approval, or submission. A status-only request ends with the loader's status report; an active, timed-out, failed, or uncertain result cannot be called verified completion.
9. For explicitly requested setup verification, first require terminal loader success, then obtain a fresh complete same-task export through `shared.setup-export.task-level-export` and compare every approved header/child delta, parent relationship, ordering, and preserved collection. Missing or partial exports block verification. On a mismatch or partial success, report the affected stage and safe reconciliation path; do not replay the import or invent a compensating delete.

Use this task metadata when invoking those skills:

- Offering: `Project Financial Management`
- Functional area / Setup Object: `Project Foundation`
- Setup task name: `Manage Planning and Billing Resource Breakdown Structures`
- Setup task code: `PJF_MANAGE_PLANNING_BILLING_RESOURCE_BREAKDOWN_STRUCTURES`

## Task Plan Validation and Execution

At workflow step 2, build `setup_task_plan` by assisted inspection of
[the shipped registry](ora-resource/ora_rule_registry.json) and its six owning
`ora-resource/ora_*.md` files. This local check requires no authoring tool,
planner script or external call, and does not repeat step 1's export.

- Select exactly one `PJF_MANAGE_PLANNING_BILLING_RESOURCE_BREAKDOWN_STRUCTURES`
  / `Manage Planning and Billing Resource Breakdown Structures` entry in the
  nested schema `3.0` registry. Require task and reachable-node readiness `ready`
  without blocking reasons; stored readiness flags alone are insufficient.
- Confirm unique node IDs, start node `RBS.VALIDATE_INPUT`, supported actions,
  existing prerequisites/transition targets and terminating paths. Resolve each
  source file inside this task's resource folder and its heading. Match each node
  to exactly one source Task Nodes row by Rule ID; compare type, sequence, action,
  transitions, prerequisites, failure behavior and applicability. Source line
  numbers are navigation hints. Read each owning rule and named resolver's one
  definition, including inputs, authority, matching, outputs and failure behavior.
- Missing, unresolved, ambiguous or inconsistent required contracts block the
  plan. Do not repair the registry, invent context or run undeclared lookups.
  Preserve the observed create-only scope and source limits: copied Project Unit
  and Organization context is not an FSCR business-eligibility verdict, and a
  serializer input assertion is not independent reference evidence.

After these checks pass, record `status: planned`, `validation.status: ready`,
task identity, start node, checked sources and validated nodes in the task-owned
plan through the declared project services and workspace paths. No readiness
override is allowed. Recheck each new preparation run or changed rule source.
On failure, stop before subsequent lookups/serialization; persist a redacted
diagnostic with stage, failure class, target/task, blockers and one safe next
action. Use `input_validation` or `catalog_or_metadata_mismatch` for input or
rule-contract gaps; preserve the actual class of a failed delegated operation.

Start at `RBS.VALIDATE_INPUT`, satisfy every prerequisite, evaluate applicability
and apply only the reached owning rule. Record sanitized evidence and the
observed outcome, follow exactly its declared transition and stop at a terminal.
Never execute all nodes by sequence number or treat an undeclared outcome as
success. Use `core.fusion-api.rest-api-client` for only the declared read-only
lookups after their existing gates. Final immutable-artifact Task Hook validation
still runs through Data Loader; this early plan supplies no upload approval.

Retain the normalized request fingerprint, current node, completed path/outcomes,
sanitized context/conversion evidence, missing requirements and safe resume stage
in task-owned preparation evidence. Return task identity, actual stage/outcome,
blockers and one safe next action. Resume preparation only after comparing
fingerprints and refreshing changed evidence. Changed intended inputs, target or
upload artifact require fresh validation/approval. Later approved submission uses
Data Loader's retained-artifact integrity checks without original-source rereads
or live revalidation. Follow steps 8-9 for uncertain results; do not copy delegated
loader records or replay a submission.

## Offline Batch Serializer Contract

`scripts/build_prbs_create_package.py` is the task-owned CSV serializer, not a lookup client or an import route. It takes a fresh, complete export from the same environment and a JSON create batch containing `target_environment`, the export's SHA-256, one observed minimal planning-RBS template name, a source-attributed format-label-to-ID map, and `structures`. Each structure requires `name`, `from_date`, and Project Unit CSV context; it may add the observed optional description, resolved Job Set, formats, and resource rows. Project Unit and Organization objects carry the supplied names, target-environment context provenance, classification and effective dates (plus Organization enterprise context) required by the tested CSV shape. The serializer copies their classification values without applying its own business-eligibility rule. Other resolved references carry the names/codes required by the CSV. See `--help` and the task-local serializer tests for the exact JSON contract.

The serializer verifies package shape, the target/export binding, tested format and resource-type IDs, an unchanged minimal template, duplicate names, supported combinations, and one explicit Resource Class tree per structure. It requires a same-target, existing minimal planning RBS with version 1, only Resource Class, and the five observed default elements as that template; if the target has no such baseline, stop rather than fabricating one. It writes one new immutable ZIP plus a checksum/row-count preview under this task's `project/{project_id}/artifacts/.../current/` directory; `--dry-run` writes nothing. It never copies existing RBS rows into the new package. Run its dry-run before writing, then register the ZIP and preview through the declared core project services and pass the immutable ZIP to `core.data-loader` only at the declared handoff.

The JSON evidence fields are caller-supplied assertions, **not** independent Fusion lookup results. The workflow must retain the actual target-environment context reads for Project Unit and Organization, and independently validate the exact conversion matches for Job Set, Job and Person before using the serializer. A Project Unit or Organization context read is not an FSCR eligibility verdict; missing context still blocks the proven CSV shape. The source export must also be independently certified complete and unfiltered by the shared export workflow; the ZIP parser alone cannot prove name absence from a filtered export. Project Unit, Job, Named Person and Organization mappings are confirmed in `ora-resource/ora_reference_lookups.md`; Named Person requires one consistent date/enterprise context for its resolved PersonNumber in that complete export and blocks at runtime when absent. A plausible JSON object, an unrelated export value, or a successful offline ZIP build cannot override that gate or authorize upload.


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

Use the parent skill for sequencing. Supplied reports are observed exports, not blank templates. Track token usage for task-owned planning/validation using the manifest policy. Persist those artifacts through the declared core project services; delegated Data Loader reporting and persistence restrictions take precedence during its execution. Retain the original approval-bound artifact for any later requested reconciliation; do not reconstruct it from chat or guess its identity.

## Offline Validation Evidence

Use the source-linked review cases and graph/Task Hook tests in
[the RBS test folder](noship/tests/).
They review the observed create-only input/default/format contract,
hierarchy/reference refusals, consolidated-package requirements, and the
preparation/approval handoff. Assisted business-rule outcomes are review
expectations, not results of a new domain evaluator or evidence of successful
Fusion imports. The [functional YAML suite](noship/tests/manage-planning-and-billing-resource-breakdown-structures-test.yaml)
tests a minimum create with an explicit Resource Class tree and declares its
remaining live omissions.

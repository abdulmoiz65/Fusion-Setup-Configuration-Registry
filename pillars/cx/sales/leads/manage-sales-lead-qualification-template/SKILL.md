---
skill_id: "cx.sales.leads.manage-sales-lead-qualification-template"
name: "Manage Sales Lead Qualification Template Setup Task Guidance"
description: "Exports current Lead qualification templates, reconciles duplicate evidence, validates a reference-derived single-template FSM package, and hands the final archive to core.data-loader for its separate approval and import lifecycle."
layer: "pillar"
pillar: "CX"
offering: "Sales"
functional_area: "Leads"
functional_area_code: "ORA_LDS_LEADS"
task_code: "MKL_MANAGE_SALES_LEAD_QUALIFICATION_TEMPLATE"
task_name: "Manage Sales Lead Qualification Template"
parent_skill_id: "cx.sales.leads"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "hybrid"
owner_team: "CX sales pillar team"
version: "0.6.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "fusion_environment_context"
  - "operation"
  - "template_design"
  - "reference_data_set_decision"
  - "execution_approval"
  - "task_context_path"
  - "task_sequence"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "current_template_reference_export"
  - "lead_template_inventory"
  - "duplicate_reconciliation_result"
  - "validated_single_template_import_package"
  - "immutable_import_preview"
  - "data_loader_task_validation_result"
  - "data_loader_approval_preview"
  - "task_validation_envelope"
  - "data_load_initiation_result"
  - "import_handoff_result"
  - "post_import_verification"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/leads/manage-sales-lead-qualification-template/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/sales/leads/manage-sales-lead-qualification-template/current/"
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
  - "Submits and downloads a read-only task-level CSV export from the selected Oracle Fusion environment."
  - "Reads the assessmentTemplatesLOV endpoint to reconcile exact Lead template-name matches."
  - "Persists reference exports, validation evidence, previews, and approved import results in the implementation project workspace."
  - "After the separate core.data-loader preview and approval lifecycle, uploads and initiates the unchanged FSM ZIP through core.data-loader."
required_privileges:
  - "Access to the selected Oracle Fusion environment and privileges to export setup task data."
  - "Privileges to read Assessment Templates list-of-values data."
  - "Privileges required by core.data-loader for an explicitly approved FSM import."
---

# Manage Sales Lead Qualification Template Setup Task Guidance

## Purpose

Exports the current Lead qualification-template baseline, validates a new
reference-derived package, reconciles duplicates from both the export and live
REST state, and hands a validated FSM archive to the mandatory Data Loader
approval and import lifecycle.

## Setup Task Skill Contract

- task_code: `MKL_MANAGE_SALES_LEAD_QUALIFICATION_TEMPLATE`
- task_name: `Manage Sales Lead Qualification Template`
- parent_skill_id: `cx.sales.leads`
- pillar: `CX`
- offering: `Sales`
- functional_area: `Leads`
- functional_area_code: `ORA_LDS_LEADS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Sales Lead Qualification Template` under `Leads`.

## Runtime Interface and Handoff

Apply the parent `cx.sales.leads` runtime-interface guidance. For the normal
workflow, prefer the declared export, validation, read-only lookup, and Data
Loader skill contracts before considering implementation or test source.

This task hands Data Loader only the task-context path, exact task name,
positive sequence, environment, final ZIP path and SHA-256, operation, template
identity and set, export identity/hash/release, duplicate evidence, row counts,
task-rule results, and `finalData.archiveSha256`. Data Loader owns its preview,
approval record, `taskValidationEnvelope`, authentication, upload, and
initiation structures. If a declared interface fails or differs from its
contract, follow the parent's scoped diagnostic escalation and reuse the
resolved interface for the rest of the run.

## Setup Task Metadata

- Task name: `Manage Sales Lead Qualification Template`
- Task code: `MKL_MANAGE_SALES_LEAD_QUALIFICATION_TEMPLATE`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## Mandatory Create Workflow

For `Create`, do not require the user to supply an existing ZIP. Export the
current task data automatically from the selected environment before generating
or approving a new qualification template.

1. Preflight the target environment identity, task code, catalog flags,
   authentication, export privilege, project destination, and import approval
   state. Never print or persist credentials.
2. Invoke `shared.setup-export.task-level-export` in current-data mode for
   `MKL_MANAGE_SALES_LEAD_QUALIFICATION_TEMPLATE`; do not use template/spec mode.
3. Capture the export `ProcessId` from either the collection form or
   `SetupTaskCSVExportProcess.items[0].ProcessId`, poll that exact process, and
   download the result from its `enclosure/FileContent` endpoint. Do not infer
   completion from a collection response or download a collection resource.
4. Validate the downloaded ZIP before use: ZIP signature and CRCs, the exact
   required members below, metadata task code, `ObjectType=TASK`,
   `ProcessType=EXPORT`, `ProcessStatus=COMPLETED`, target `ProcessEnv`, target
   Fusion release, and `LEAD` scope. Record its SHA-256 hash and export
   `ProcessId`.
5. Inventory every `LEAD` template from both template CSVs and retain exact
   name, `AssessTemplateNumber`, `SetId`, and `StatusCode`. Also run the
   documented live exact-name lookup.
6. Reconcile the proposed exact name against both sources. Continue only when
   both return zero matches. One match in either source is a duplicate;
   disagreement is stale or incomplete evidence and requires a fresh export;
   multiple matches are ambiguous and block the operation.
7. Use the validated ZIP only as the target environment's schema, column,
   metadata, and relationship reference. Construct a new package containing
   exactly one proposed Lead template and its dependency closure. Generate new
   identifiers; never carry another template's rows, identifiers, audit values,
   or unrelated setup records into the import package.
8. Route the proposed package through `shared.validation.setup-data-validator`
   and `shared.validation.reference-data-validator`, then apply the task-local
   graph through its `data_loader_ready` terminal. This validates the final
   archive for handoff but does not create an import approval.
9. Hand the final validated ZIP, task context, task name, sequence, and exact
    package SHA-256 to `core.data-loader` only when the task graph reaches
    `data_loader_ready`. The task graph does not approve or execute the import.
10. Let Data Loader invoke Task Hook `data-load`, evaluate this task registry,
    and build its immutable approval preview for the final archive. Include the
    environment, release, export ProcessId/hash, inventory count, duplicate
    evidence, package hash/rows, template design, set decision, and validation
    results. Stop and require the user's later standalone `approve` message.
11. After approval, let Data Loader revalidate the same archive, verify its
    SHA-256, create the `taskValidationEnvelope`, and pass that envelope to its
    upload/initiation workflow. The archive contains
    `ASM_SETUP_CSV_METADATA.xml`, so Data Loader must preserve it unchanged and
    submit it with `sourceType: FSM`. Do not call a shared import script,
    `setupTaskCSVImports`, UCM, or an initiation endpoint from this task skill.
12. Treat accepted Data Loader initiation as terminal for that request. Do not
    poll automatically. When the user later asks for status or results, use
    Data Loader status handling to retrieve data-set errors and the FSM
    ProcessLog, then verify the template with a new exact-name read or export.
    Never retry an import automatically.

The export invocation must carry the selected project and target environment
through the shared authentication/export contracts. Its task arguments are:

```text
--task-code MKL_MANAGE_SALES_LEAD_QUALIFICATION_TEMPLATE
--offering-name Sales
--functional-area-name Leads
--project-id {project_id}
```

Do not add `--template-only`. Treat an export created during the current Create,
Copy, or Review run as fresh. An older or user-supplied archive requires an
explicit offline/fallback decision and must still pass environment, release,
task, scope, integrity, and live-lookup checks.

The required current-data export contains exactly these members:

- `MOW_ASSESSMENT_TEMPLATE.csv`
- `ORA_CRM_ASSESSMENT_TEMPLATE_FOR_RATING.csv`
- `ORA_CRM_ASSESSMENT_TEMPLATE_RATING.csv`
- `ORA_CRM_ASSESSMENT_ATTRIBUTE_GROUP.csv`
- `ORA_CRM_ASSESSMENT_ATTRIBUTE.csv`
- `ORA_CRM_ASSESSMENT_ATTRIBUTE_VALUE.csv`
- `ORA_CRM_ASSESSMENT_SCORE_RANGE.csv`
- `ASM_SETUP_CSV_METADATA.xml`

The new package must retain those filenames and metadata structure. CSV header
order comes from the fresh export and must not be guessed or normalized.

## User-Supplied ZIP Fallback

A user-supplied export is a fallback only when automatic export fails and the
user explicitly chooses offline continuation, or when the user explicitly asks
to work offline. Validate its task code, environment, release, LEAD scope,
member list, headers, integrity, and freshness before use. A ZIP from another
environment or release is not valid reference evidence without a new explicit
decision and validation; it never substitutes for the live duplicate lookup.

## Other Supported Operations

- `Copy`: export and resolve the source exactly, then create a new package with
  new identifiers and a distinct name. Never modify a deployed source.
- `Review`: export current data and reconcile it with the live exact-name result;
  do not prepare or import a mutation package unless the user changes scope.
- `Deploy`: provide read-only deployment-readiness review only. Actual
  deployment is refused because this task does not yet have a validated FSM
  package contract for the status transition; never substitute REST, browser,
  or assisted Setup and Maintenance mutation.

## Routing Metadata

`CSVExportImportSupportedFlag` is `Y`, so use these routes:

1. Export with `shared.setup-export.task-level-export`.
2. Validate with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Gate and execute an approved import only through `core.data-loader`.

Do not invoke `shared.setup-import.task-level-import`, its scripts,
`setupTaskCSVImports`, or a direct import endpoint. Data Loader is the mandatory
orchestrator and owns final-archive validation, Task Hook evaluation, immutable
preview, standalone approval, approval-envelope verification, upload, and FSM
initiation. Do not add task-local authentication or import code.

Use this task metadata when invoking those skills:

- Offering: `Sales`
- Functional area / Setup Object: `Leads`
- Setup task name: `Manage Sales Lead Qualification Template`
- Setup task code: `MKL_MANAGE_SALES_LEAD_QUALIFICATION_TEMPLATE`

## Task-Local Rule Workflow

Use the task-local `ora-resource/` rules after the fresh export is available and
before any preview or import handoff. The supported operations are `Create`,
`Copy`, `Review`, and `Deploy`.

1. Validate the requested operation, template identity, reference-data set,
   ratings, question groups, questions, weights, responses, and score ranges.
2. Confirm the questionnaire design and reference-data-set scope are ready.
3. Reconcile the exported inventory with the documented read-only assessment-
   template lookup.
4. Apply package-isolation, duplicate, deployed-template, score-model,
   reference-data-set, and immutable-preview design gates.
5. Route a validated Create or Copy package to the Data Loader approval gate,
   return Review or Deploy-readiness results as read-only, and block any actual
   Deploy mutation until an export-derived Data Loader contract is documented.

The task-local rule graph never authorizes a REST write, browser/assisted
deployment, or direct import.
It may orchestrate read-only export and lookup operations and return a validated
final FSM archive to Data Loader. A Create or Copy import executes only after
`core.data-loader` independently builds its preview, receives the later
standalone approval, verifies the unchanged archive, and produces the matching
Task Hook approval envelope. No task-local rule or implicit approval may bypass
that boundary.

## Failure and Recovery

Load and apply `ora-resource/ora_error_handling.md` before export, preview, or
Data Loader handoff. Classify failures as input validation, catalog mismatch,
authentication or authorization, transport or environment, Fusion API,
process timeout, process failure, artifact persistence, approval blocker,
verification mismatch, or partial completion.

Allow only the owning shared/core client's documented single cached-token
refresh for an eligible read. Never retry or resubmit an export, upload,
import, deployment, POST, PATCH, or DELETE automatically. On timeout, stop and
report the environment, task code, ProcessId or request ID, last status,
elapsed wait, and exact resume path. Preserve successful outputs and list
failed or unattempted units instead of presenting partial work as complete.

Persist sanitized diagnostics and available ProcessLog or status evidence with
the failure class, stage, external identifiers, and one safe next action. Do
not issue automatic compensation. Redact and never print or persist
credentials, bearer tokens, authorization headers, client secrets, token-cache
content, private keys, full base64 payloads, or sensitive customer details.

## Oracle Documentation Sources

- [Create a Lead Qualification Template](https://docs.oracle.com/en/cloud/saas/sales/fadsi/create-a-lead-qualification-template.html)
- [Lead Qualification Templates](https://docs.oracle.com/en/cloud/saas/sales/oasal/lead-qualification-templates.html)
- [Assessment Templates REST Endpoints](https://docs.oracle.com/en/cloud/saas/sales/faaps/api-list-values-assessment-templates.html)

## Follow-On Scope

Assigning a deployed qualification template to lead profile options is outside
this task-local graph. Route that later work to `MKL_MANAGE_SALES_LEAD_PROFILE_OPTIONS`
when the Leads implementation is expanded; do not start that setup task from
this skill's rule registry.


## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `fusion_environment_context`: selected environment URL/identity and release;
  credentials remain in the core authentication service
- `operation`: `Create`, `Copy`, `Review`, or `Deploy`
- `template_identity`: template name and, for `Copy`, the source and new names
- `reference_data_set`: template set and intended business-unit coverage
- `ratings`
- `question_groups`
- `questions`
- `question_weights`
- `responses`
- `score_ranges`
- `task_template_associations_optional`
- `execution_approval`: absent until the user approves the immutable preview

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `current_template_reference_export`: ZIP, ProcessId, SHA-256, environment,
  release, and freshness evidence
- `lead_template_inventory`
- `duplicate_reconciliation_result`
- `validated_single_template_import_package`: exact ZIP and SHA-256
- `immutable_import_preview`
- `import_handoff_result`
- `post_import_verification`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.sales.leads` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

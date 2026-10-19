---
skill_id: "erp.project-financial-management.project-foundation.manage-project-templates"
name: "Manage Project Templates Setup Task Guidance"
description: "Provides REST-only, documented-contract guidance for Manage Project Templates under the Project Foundation functional area."
layer: "pillar"
pillar: "ERP"
offering: "Project Financial Management"
functional_area: "Project Foundation"
functional_area_code: "ORA_PJF_PROJECT_FOUNDATION_FA"
task_code: "PJF_MANAGE_PROJECT_TEMPLATES"
task_name: "Manage Project Templates"
parent_skill_id: "erp.project-financial-management.project-foundation"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP project financial management pillar team"
version: "0.6.5"
inputs:
  - "project_id"
  - "target_environment"
  - "requested_template_change"
  - "project_template_identity"
  - "business_and_project_unit"
  - "project_type_and_plan_type"
  - "owning_organization_and_legal_entity"
  - "initial_status_and_effective_dates"
  - "requested_template_tasks"
  - "current_target_state"
  - "execution_approval"
outputs:
  - "validated_project_template_request"
  - "dependency_readiness_result"
  - "immutable_rest_preview"
  - "rest_execution_result"
  - "target_state_verification"
  - "runtime_readiness_note"
  - "execution_receipt_record"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.data-loader"
uses_core:
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
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
persists_project_state: true
state_updates:
  - "setup_task_sequence"
  - "configuration_blueprints"
  - "validation_results"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-project-templates/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-project-templates/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-project-templates/current/"
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
  - "Reads Project Templates REST resources for discovery and verification."
  - "Executes approved REST create, update, end-date, and documented child-row operations."
  - "Writes task plans, validation/preview evidence, execution receipts and redacted diagnostics to the selected project workspace through core project services."
required_privileges:
  - "Project Templates REST read access"
  - "Project Templates REST create/update/delete-child access for the requested operation"
---

# Manage Project Templates Setup Task Guidance

## Purpose

Provides task-specific setup planning, documented REST contract validation, and REST execution guidance for `Manage Project Templates` under `Project Foundation`.

Prepared payload destinations must be new, versioned files. The helper refuses
an existing file, directory or symlink before writing output and uses exclusive
creation to prevent a concurrent run from replacing the artifact. Retain the
original payload and preparation evidence; intentional regeneration uses a new
destination and a fresh preview through the declared artifact services.
`--validation-output` remains a current validation record and may be refreshed;
use a separate path when retaining approval revalidation evidence.

## REST Request Preflight

Before any workflow-selected REST request, apply the offering's
[REST version and query compatibility preflight](../../references/rest-query-compatibility.md).
Determine the effective framework version from the selected core client or
workflow, construct compatible query parameters, and verify that the outgoing
header agrees. Do not hardcode a separate pillar version. Existing route,
validation, classification/matching, persistence and approval gates still apply.

## Setup Task Skill Contract

- task_code: `PJF_MANAGE_PROJECT_TEMPLATES`
- task_name: `Manage Project Templates`
- parent_skill_id: `erp.project-financial-management.project-foundation`
- pillar: `ERP`
- offering: `Project Financial Management`
- functional_area: `Project Foundation`
- functional_area_code: `ORA_PJF_PROJECT_FOUNDATION_FA`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill to validate, preview, execute, and verify a customer-FSCR project-template create or update for `Manage Project Templates` under `Project Foundation`.

## Supported Task Behavior

Create, update, end-date, and validate project templates through the published Project Templates REST resource. It covers the documented core fields and the explicitly requested child collections: classifications, customers, team members, transaction controls, provider business units, quick entries, setup options, tasks, and task transaction controls. The precise method, path, parent/child key, and supported CUD actions are in [the static REST contract reference](references/project-template-rest-contract.md).

This is a REST-only skill. Browser and guided-UI execution are not routes for this task. FSM and CSV export/import are also unsupported. Duplicate, create-from-project/template, root-template delete, a child operation not listed in the REST contract, and any field that cannot be mapped to the documented operation schema must stop with an unsupported-surface report. Never infer whole-template coverage from the root collection and never substitute an undocumented route after approval.

For customer-facing capability blockers, follow the wording contract in
ora-resource/ora_error_handling.md. Explain which requested settings the current
skill cannot yet save and why creation is paused; keep internal mapping/schema
terminology in diagnostics unless the customer asks for technical details.

## Setup Task Metadata

- Task name: `Manage Project Templates`
- Task code: `PJF_MANAGE_PROJECT_TEMPLATES`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`

## REST-only Validation and Execution Workflow

`ExportImportSupportedFlag` and `CSVExportImportSupportedFlag` are both `N`. Do not invent an FSM package or Data Loader route.

1. Normalize input aliases to documented REST field names and enumerate the requested core changes and child operations. Reject unknown fields rather than silently dropping them.
2. Execute `ora-resource/ora_rule_registry.json` in sequence. Initial input validation checks scope and supplied-value shape; apply documented defaults and resolve references before checking prepared-payload completeness. Request only required values that remain unresolved.
3. Read the collection baseline for duplicate detection. For create, zero exact matches is ready: use the published root POST path and schema. Do not require a nonexistent item `self` link or child link before the parent is created. Returned canonical links remain mandatory for update, child-after-parent operations, and readback.
4. Validate identity, ISO dates, documented project/business unit/type/organization/legal-entity/status representations, setup-option prerequisites, child keys, and downstream reuse impact where a documented consumer lookup is available. Treat customer-supplied names as first-class REST values and require exactly one documented name/ID/code representation for each required reference. Do not call `/projectTemplates/{existing-template}/lov/ProjectTypes`, `/ProjectUnits`, or `/OwningOrganizations` while validating a new-template create; those values belong to the existing parent template's context. Fusion validates whether submitted root reference values exist and are compatible when the approved REST request is executed.
5. Before approval, run scripts/validate_project_template_payload.py with the exact --operation and --child-family where applicable. Whenever defaults, inheritance or lookup resolution apply, use --prepared-payload-output for a separate immutable body and --validation-output for its preparation record. Use --priority-lookup-json for priority names, --lookup-evidence-json for other registered code-only aliases, and an explicit --effective-date for all lookup resolution. Approval and submission bind to the prepared body and its digest. Preserve the original preparation/default/resolution evidence; approval revalidation writes a separate report. No create defaults are added to PATCH. Generic describe flags cannot make generated/defaulted fields required or authorize unpublished write fields. All checks must pass before preview.
6. Produce an immutable REST operation plan and payload checksum. Prefer one documented root POST with validated nested Tasks over a deliberately staged create. A single request does not prove server rollback on failure: reconcile uncertain outcomes through selected reads and retain partial-state evidence. Keep metadata and validation digests internally. Show the target, business values, method/path, body when requested and readback plan; request one approve/decline decision on the business change.
7. Before execution approval, record the active workflow's operation classification and selected executor. Every import/load, including registered-business-object creation routed as an import, enters `core.data-loader` and its adapter/Task Hook approval workflow; missing adapter or registration blocks that route. Do not relabel an import as direct REST. For a task operation explicitly selected outside import scope, use the shared REST client with its supported body/output/timeout options after approval of the exact target, method, URI and payload. The consuming workflow owns artifact integrity and sanitized receipts. The approved POST is the first live authorization check; on `401` or `403`, stop without retry. On success, use only returned canonical links for readback.

For nested template create, leave omitted task organization fields out of the request and verify Fusion-derived values from task readback. Successful target response and canonical task readback supplied on 2026-10-14 evidence this behavior. Preserve explicit overrides and validate fresh operation-specific target requirements. The published Oracle required array remains recorded as-is. Direct task create retains its existing explicit/evidenced organization contract. Apply documented task cross-charge defaults/inheritance. Oracle work type and ExternalTaskId requiredness remain operation-specific. For nested template creation, preserve supplied valid external task IDs and generate omitted IDs under the FSCR policy in ora_defaulting_rules.md. Reuse a supplied unique TaskNumber for the generated external ID; when no number is supplied, allocate a request-unique sequence. Persist generated values before approval and verify task numbers from readback. Target execution evidence shows ExternalTaskId becoming the saved TaskNumber on create, and a TaskNumber PATCH also changing ExternalTaskId. Disclose both resulting values in create/update previews; do not promise independent preservation of ExternalTaskId when changing TaskNumber. Verify both fields after execution. Validate supplied date ordering and known project schedule bounds; template availability dates are not project schedule substitutes.

Apply the four root boolean defaults and ALL_COSTS only on create, preserve explicit choices, and leave interest capitalization and asset allocation omitted for project-type derivation when not supplied. Resolve a supplied priority display name through the documented enabled/effective lookup and include the returned code and redacted evidence in the preview. The defaulting, lookup and input-validation resources own these rules; do not duplicate or override them from a historical successful payload.

## Inputs

- Target environment and requested create, update, end-date, validation, or documented child operation.
- Exact template name/number and requested description.
- Business context for create; status, dates and optional associations only when supplied or explicitly operation-required. PATCH supplies requested changes and preserves omissions.
- Project plan type as an exact target name or independently resolved ID when that association is requested.
- Requested task rows; omitted nested task organization remains omitted for Fusion derivation and task readback verification. Explicit task overrides remain supported. Omitted task cross-charge flags inherit evidenced project/parent-task values. Supplied external IDs are preserved; omitted nested-create IDs are generated once and persisted before approval under the defaulting policy.
- Fresh target baseline/schema evidence and explicit approval of the immutable REST preview.

## Outputs

- Validated project-template request and dependency readiness.
- Customer-readable REST preview with an internally checksum-bound exact payload.
- One approved execution result and independent target readback.
- Runtime-readiness note for any unresolved permission, reference, schema, or environment fact.

## Runtime Readiness

### Supported Executor Handoff

The pillar returns task-specific validation, dependency, design and evidence
requirements to the active workflow. The workflow owns payload preparation,
approval and dispatch through the selected core executor. The static reference
is not a write route. Current v3 ora-resource files contain only the supported
task-rule resources and compiled registry; there is no separate pillar REST
execution authority or transport wrapper.

Use the existing `core.fusion-api.rest-api-client` contract. The client supports
`--body` or `--body-file`, `--output` and `--timeout`; it does not own the
customer's approval or the consuming task's durable audit record. There is no
blanket executor blocker for absence of task-specific CLI options.

The active workflow must classify the operation before selecting an executor.
Every import/load goes through `core.data-loader` first. Its selected adapter,
source/API validation, immutable artifact, Task Hook and approval checks are
authoritative. Catalog flags N prohibit inventing FSM/CSV support; they do not
prove a REST-backed Data Loader adapter exists. Missing or ambiguous adapter
evidence blocks the affected import before approval. Never substitute a generic
REST POST or reclassify the request to bypass that gate.

For a direct task REST operation explicitly selected outside import scope,
validate the payload and preserve the approved artifact, target, method, URI and
readback plan. Immediately before dispatch, verify that these still match the
approval record. `validate_project_template_payload.py` supports optional
`--expected-payload-sha256` to check the task-local artifact; this check alone is
not execution authorization. Do not modify the artifact between verification
and handoff. Pass it through the supported shared client. The client parses and
serializes JSON; the approved data must remain unchanged, but whitespace and
wire-byte formatting are not the approval contract. Any payload, target, method,
URI or route change requires a new preview and approval.

The workflow's immutable preview must enumerate the complete ordered method/URI
list, exact body for each call, changed fields and child rows, preserved omissions,
artifact digest and independent readback plan. Prefer an atomic root POST when
the complete requested nested arrays validate; this describes one request, not
a documented rollback guarantee. An explicitly approved staged
plan must disclose partial-root impact. Later child creates require the selected
family's documented POST, returned parent URI, required fields and duplicate
checks; updates require a fresh baseline and mutable-field-only PATCH; child
deletes require a documented DELETE and exact returned child identity disclosed
in the preview. Approval is one business-change decision, not a request for the
customer to compare internal digests. No probe write or route change is permitted.

The consuming workflow captures status, safe returned identities, request UTC
window, endpoint and sanitized errors in task receipts through the existing
project services. `--output` saves response bytes only; it is not an error-log
or redaction option. Use it only for an approved response artifact permitted by
the active workflow; never persist raw customer-sensitive output as diagnostics.
Retain only correlation information actually exposed by the client. If required
evidence is unavailable, report the gap without inventing it. Stop on uncertain
or failed writes and reconcile through selected reads; never retry blindly.

Skill generation and local planning do not require a probe write. The active workflow supplies target identity, current operation evidence and required business context. Generic describe metadata cannot establish POST requiredness or authorize fields absent from the published request schema. Only fresh operation-specific POST evidence may require otherwise optional currency, work type or external task IDs. Supported names remain first-class values; a genuinely ID-only contract requires a proven resolver. Missing actual operation-required data or permission evidence blocks execution. Do not use an existing template contextual LOV to validate a new template.

After any rejected POST, discard that preview and approval. Retain the sanitized response correlation headers, exact UTC request window, and Fusion error. Do not call another structurally passing preflight production-ready or change fields automatically. Correct only a user-approved value or identified structural defect, rebuild the complete payload, produce new checksums, obtain fresh approval, submit once, and independently read back the returned template and tasks. If the target error is not actionable, return it and require user direction or target diagnostics before another write.

## Implementation Notes

The reviewed 26C request constraints are in [the operation contract snapshot](references/project-template-operation-contracts.json). The validator checks the published root, nested and direct-child schemas as well as selected target metadata. Response-only IDs, audit fields and unrecognized UI/resource labels cannot become write fields through generic describe metadata. The source links and unresolved evidence boundaries are recorded in the static REST reference.

The Oracle Project Templates create contract and the target pod's `projectTemplates/describe` metadata both expose `ProjectPlanType` and `ProjectPlanTypeId`, not `ProjectPlanTypeName`. The published operation schema and target-exposed REST links are the authority for field and child handling; preserve omitted update fields and child rows.

## Durable Artifacts and Review

Resolve `project_id` from the selected existing implementation project before preparation or execution; missing project identity is an input-validation blocker. Persist plans, validation results, immutable previews, approved package references, execution receipts and redacted failure diagnostics under `project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-project-templates/current/`. Raw exports belong under `project/{project_id}/exports/project-financial-management/project-foundation/manage-project-templates/`. Never persist credentials or tokens there.

Use `core.project-mgmt.artifact-version-manager` for major new versions and confirmed minor updates, `core.project-mgmt.artifact-registry-manager` to register each durable artifact, and `core.project-mgmt.project-state-manager` to update only declared state fields and record the run under `project/{project_id}/state/runs/`. Persist each receipt before the next external call; append later statuses and retain partial failures, environment, operation, external IDs, artifact references and next action. Recover uncertain writes through supported reads; do not resubmit automatically. Record token usage using the manifest policy.

Required reviewers: responsible ERP Pillar Development Lead or SME, FSCR A-Team/core reviewer, and QA for validation/execution changes. Package readiness does not replace merge approval.

## Local Validation Evidence

The payload regression suite is owned by
[noship/tests/project-foundation/manage-project-templates](../../noship/tests/project-foundation/manage-project-templates/).
It covers supported operations, malformed task identifiers, graph/date rules,
approval-bound artifact changes and persisted CLI failure results. Shared handoff checks are at
[the functional-area test level](../../noship/tests/project-foundation/test_project_foundation_executor_contract.py).
Passing these offline tests does not prove a target adapter, privilege or live
reference is available; those remain request-specific execution prerequisites.

---
skill_id: "erp.project-financial-management.project-foundation.manage-project-statuses"
name: "Manage Project Statuses Setup Task Guidance"
description: "Guides consultants through Project Status setup in Codex, resolves object/classification capabilities, applies create defaults, and executes approved FSM CSV changes through Data Loader with independent export readback."
layer: "pillar"
pillar: "ERP"
offering: "Project Financial Management"
functional_area: "Project Foundation"
functional_area_code: "ORA_PJF_PROJECT_FOUNDATION_FA"
task_code: "PJF_MANAGE_PROJECT_STATUSES"
task_name: "Manage Project Statuses"
parent_skill_id: "erp.project-financial-management.project-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP project financial management pillar team"
version: "0.6.0"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-project-statuses/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/project-financial-management/project-foundation/manage-project-statuses/current/"
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
  - "Writes local task blueprints, validation results, skill-run records and token-usage entries, and updates their project artifact/state references."
  - "Delegates task-scoped Fusion exports and separately approved imports to the declared shared/core workflows."
required_privileges:
  - "Read access to projectStatusesLOV for current status identity and workflow-code resolution."
  - "Task export, UCM upload and import privileges enforced by the delegated export and Data Loader workflows."
---

# Manage Project Statuses Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Project Statuses` under `Project Foundation`.

## REST Request Preflight

Before any workflow-selected REST request, apply the offering's
[REST version and query compatibility preflight](../../references/rest-query-compatibility.md).
Determine the effective framework version from the selected core client or
workflow, construct compatible query parameters, and verify that the outgoing
header agrees. Do not hardcode a separate pillar version. Existing route,
validation, classification/matching, persistence and approval gates still apply.

## Setup Task Skill Contract

- task_code: `PJF_MANAGE_PROJECT_STATUSES`
- task_name: `Manage Project Statuses`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Project Statuses` under `Project Foundation`. Also use it to read a named status or explain the permitted fields, defaults and LOV choices without preparing a write.

## Supported Release Contract

This assisted package supports current-state reads, task exports and native FSM change preparation within the conditional scope below. Its local helpers never contact Fusion, generate an import package, authorize a write, or replace Task Hook validation. All live imports retain the existing Data Loader workflow and exact approval gates. Merge readiness for this package does not certify full UI parity or a successful target import.

Run [the operation scope guard](scripts/check_operation_scope.py) before external lookups, then again after resolving the current baseline for an existing status. Its normalized input, result mapping and limits are defined in `ora-resource/ora_reference_lookups.md`. An explicit unsupported intent returns immediately without collecting create fields. A name change, persisted clear, lifecycle removal or type reinterpretation expressed as an ordinary update must receive the same refusal. A genuine append carries forward the complete existing target set.

Read [coverage and remaining capabilities](references/coverage-and-limitations.md) when explaining support or reviewing a release. It tracks unsupported operations, required evidence and verification cases without representing them as implemented features. Missing target-specific evidence blocks the affected request; it is not permission to change this reusable skill, invent a route, or use the setup UI during consultant execution.

## Operation Coverage

| Consultant intent | Codex behavior | Limit |
|---|---|---|
| Read a status or explain configuration | Resolve the current identity; return available fields and explicitly identify missing native details | A seed-filtered export is not a complete inventory |
| Create a custom status | Apply the addable-pair and field matrix, documented defaults and native package checks | Exact current control inheritance and Progress weight require current evidence; the disclosed standard PROJECT policy remains available |
| Change description, effective dates, Initial, action Allow or supported workflow fields | Preserve the current identity and unrequested values; prepare an exact diff through Data Loader | Object/classification editability and required current-use evidence still apply |
| Add lifecycle targets | Resolve the complete intended U/S target set and native bridges before preview | A genuine append preserves existing targets; an unavailable S bridge blocks that target |
| Rename, clear a stored value, replace/remove lifecycle targets, or disable workflow with cleared outcomes | Explain the precise missing native mutation contract and retain the valid business request | These non-delete UI operations are not yet verified through the selected Codex route; do not claim full UI parity |
| Delete a status | Decline execution | Outside this skill's supported execution scope |

Capability declarations and local validation do not certify every operation as tested in Fusion. Report execution evidence separately for each requested operation. An unresolved operation must not become an implicit create, retained old value, or partial import.

## Supported Task Behavior

Create a custom status under an addable object/classification, or update permitted fields of an existing status. Status object maps to StatusType; classification maps to ProjectSystemStatusCode. Match an existing status by StatusType and ProjectStatusName across all classifications. A different classification does not make a duplicate name unique.

Resolve object/classification LOVs from `ora-resource/ora_reference_lookups.md`. Create permission, field editability, and lifecycle permission are separate checks. A classification that disallows creation can still permit an existing status's lifecycle to be edited. Apply the object-specific workflow and read-only exceptions in that resource. Multiple statuses may be marked Initial; the flag makes a status eligible for selection when creating an object.

For creation, require a name and From Date. Default Initial to No, Enable Workflow to No, and Next Allowable Status Type to All unless explicitly supplied. Explain that All permits transitions to any status. Resolve action controls using the create policy below, and inherited progress weight where applicable, before preview; FSM import must not be assumed to call UI defaulting methods. For updates, omission means preserve the baseline in the proposed diff. This is FSCR intent handling, not proof that an omitted CSV field or child member is preserved by every importer.

Map an action-control **Allow** request to `AllowOverridesFlag`. The UI's `EnabledBool` checkbox reads that flag and its setter updates it. `EnabledFlag` is a separate inherited value and must not be substituted for Allow. Verify both flags against the approved business intent in a fresh native export; import success alone cannot prove that the intended Allow value changed.

Resolve current status identities and stored codes through the declared read-only projectStatusesLOV lookup, or a complete current response supplied from that same target. Join it to the native export by object and exact name. Do not use a seed-filtered export as the only identity inventory. Keep object/classification capability catalogs local; this lookup supplies current identities, not configurable capability flags.

Treat Next Allowable Status Type and its lifecycle targets as one change. U means named statuses of the same object; S means classifications of the parent object. Never ask the consultant to select a custom status merely to represent an S-mode classification. The native CSV name/code bridge for S is separate from U and can be unavailable for a particular classification; apply the exact bridge check in the lookup resource. Missing or unencodable targets block the affected operation.

Enable Workflow and its accepted/rejected outcomes are also one change. Resolve outcome names to verified ProjectStatusCode values of the same object; never place a display name or classification code in BpSuccessStatusCode/BpFailureStatusCode by assumption. Preserve fixed milestone outcomes and other read-only fields. Disclose missing downstream graph evidence as deferred, never passed. Missing required identity, controls unresolved under the selected policy, package shape, or clear/delete semantics remains a blocker. Ordinary lifecycle cycles can support reopening and are warnings, not an automatic prohibition.

Use task-scoped FSM CSV; no exact writable public setup REST contract is declared.

## Create Control Policy

For PROJECT creation, use `prefer-current-else-standard` unless the consultant explicitly requires exact current UI inheritance. First use complete current controls of the exact classification source. When that source is excluded from the native export, prepare the seven standard Oracle source controls documented in the lookup resource as explicit proposed configuration. Record `controls_basis: standard_source`, `inheritance_verified: false`, and the affected names in the immutable preview. This mode makes ordinary creates executable through the existing approval/import route; it does not establish current pod default parity. No extra policy question is required for every create: approval of the exact disclosed package is authoritative.

The UI copies ActionCode, SortOrder, StatusType and EnabledFlag from controls whose ProjectStatusCode equals the selected ProjectSystemStatusCode. It then sets AllowOverridesFlag to N for DRAFT/CLOSED and Y otherwise, and CopyToUserStatusFlag to N. It does not copy an arbitrary custom status or that status's Allow choices. Resolve these values using the exact classification identity and complete current same-target control evidence described in `ora-resource/ora_reference_lookups.md`.

Native FSM exports can exclude unmodified seeded statuses and their controls. The declared projectStatusesLOV lookup supplies identities, not controls; no live non-UI classification-control lookup is declared. Under `exact-inheritance`, missing current controls remain `operation_status: blocked`, `request_validation: passed` when applicable, `blocker_type: workflow_gap`, and `failure_class: catalog_or_metadata_mismatch`. Missing identities, malformed or inconsistent supplied controls, unsupported objects/classifications and current-value preservation on updates never use the standard fallback. Do not copy a custom status, ask for valid dates/names again, or require UI flag collection. Full current UI default parity still needs a confirmed read contract.

The controls helper reports `controls_request_validation`, which covers its normalized control inputs only. The caller may report full `request_validation: passed` only after validating all other requested status fields. In particular, `controls_request_validation: passed` with `blocker_type: workflow_gap` means preserve the valid inputs and resolve missing evidence; it does not mean the create or import is ready.

Run [the local create-controls resolver](scripts/resolve_project_controls.py) for PROJECT creation after the declared identity lookup and native export. It consumes normalized create requests, complete unfiltered identity coverage and the native export, then emits all control rows, basis, warnings and input checksums. It makes no external calls and produces no import package. Its output does not verify target provenance, freshness, other status fields or import readiness; the calling workflow must complete those checks. See the invocation and input contract in `ora-resource/ora_reference_lookups.md`.

Consultants execute this task through Codex's declared export, Task Hook validation, approval, Data Loader import, and independent export-readback workflows. Do not use the Fusion setup UI to create, update, rename, delete, clear, or remove children, or make UI verification a required consultant step. UI inspection is authoring/review evidence only when explicitly requested, as in a skill-parity review; it is not a runtime execution route. If the declared non-UI workflows and supplied current artifacts cannot establish required identity, inheritance, or mutation semantics, report the missing evidence or unsupported operation instead of opening the setup UI as a fallback. Authentication remains delegated to the core authentication workflow.

## Consultant Conversation

Reuse the target environment and supplied context. Ask for the status object, classification, status name, intent, and start date only when still missing for a create. Accept familiar labels such as Project and Active; normalize them using the local catalogs. For a named read or update, resolve classification from current identity/baseline rather than requiring the consultant to supply it again. Ask only about remaining ambiguous behavior. Show the resolved defaults, inherited controls, date range, workflow outcomes, and transition scope before approval.

Example: "Prepare a new Active project status named FSCR_STATUS_REVIEW_20261014, effective 14 October 2026, with no outgoing transitions."

Expected preview: PROJECT/ACTIVE, explicit start date, blank end date, Initial=N, Enable Workflow=N, NextAllowableStatusFlag=N overriding the All default, and classification-derived action controls. Do not submit during review. This prompt is a prepared sandbox case, not a passed create test.

## Resource Read Order

Read input validation, reference lookups, defaulting, dependency readiness, design enforcement, and error handling under `ora-resource/`. Resource compilation is an authoring-only activity. Consultant execution consumes the compiled registry through Data Loader Task Hook and its required execution guide; it must not invoke authoring to modify the skill. A planned graph is not proof of a successful Fusion import.

## Setup Task Metadata

- Task name: `Manage Project Statuses`
- Task code: `PJF_MANAGE_PROJECT_STATUSES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Run the local operation scope guard before any external call; return a refusal or input issue immediately when indicated. For a request that can continue, use the declared Task Level Export workflow to obtain the required current data and native template from the selected target. Check whether seeded/unmodified rows were excluded; export absence alone is not proof that a status does not exist.
2. Execute `ora-resource/ora_rule_registry.json` in sequence. The input gate refuses explicit unsupported intents before identity lookup; baseline resolution rechecks implicit unsupported updates before defaulting or graph preparation.
3. Build explicit base/child diffs using the native members and field mapping in the lookup resource. Preserve the two parent representations and their metadata order; do not combine them into one invented CSV.
4. Validate local capabilities and current identity, lifecycle, workflow, controls, translations, and current-use evidence. Use only the declared core REST read-only identity lookup and same-target export artifacts; never query another pod or database. Apply the object/classification field matrix, including protected and legacy values. Keep unavailable downstream graph checks separate from identity or package blockers.
5. Produce an immutable graph-aware preview and checksum.
6. Import only after approval; do not retry automatically. Initiation is an in-progress result and retains Data Loader's authoritative output. When the user requests status, results or completion verification, use the declared Data Loader status workflow and compare a fresh same-task export against the original business request, including complete control/lifecycle sets and both outcome codes. Do not poll status endpoints outside that requested scope or declare completion from upload, initiation or a prepared package.

Use this task metadata when invoking those skills:

- Offering: `Project Financial Management`
- Functional area / Setup Object: `Project Foundation`
- Setup task name: `Manage Project Statuses`
- Setup task code: `PJF_MANAGE_PROJECT_STATUSES`


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

Use the parent skill for sequencing. Keep delete, rename by CSV alternate key, child replacement/removal, and clearing stored values blocked until their exact loader semantics are verified. A Delete button in Fusion or a readable REST resource does not establish an FSCR execution route. Track token usage using the manifest policy.

FSM CSV import does not delete by omission. Do not propose dropping a parent or child row as cleanup or deletion. See the native contract and Oracle FSM source in `ora-resource/ora_reference_lookups.md`. Advertise the verified operation scope explicitly; planner readiness, a valid package, and one successful create do not establish full UI parity. Report each live create, update, rename, delete, clear, and child-removal case separately as passed, failed, blocked, or not run, with independent readback for executed cases.

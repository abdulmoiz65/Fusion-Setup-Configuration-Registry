---
skill_id: "hcm.learning-management.learning-catalog.self-paced-learning"
name: "Self-Paced Learning Setup Task Guidance"
description: "Plans, validates, previews, executes, and verifies approval-gated Self-Paced Learning changes through Data Loader BC REST, with documented Direct REST exceptions."
layer: "pillar"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Catalog"
functional_area_code: "ORA_LEARNING_CATALOG"
task_code: "CUSTOM_SELF_PACED_LEARNING"
task_name: "Manage Self-Paced Learning"
parent_skill_id: "hcm.learning-management.learning-catalog"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "learningSelfPacedItems"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "HCM learning management pillar team"
version: "1.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "requested_operation"
  - "target_environment"
  - "self_paced_learning_definition"
  - "content_source"
  - "multi_row_manifest"
  - "demo_generation_request"
  - "current_state_evidence"
  - "execution_intent"
  - "approval"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "dependency_readiness"
  - "change_preview"
  - "row_scoped_results"
  - "execution_authorization"
  - "execution_result"
  - "post_action_verification"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.fusion-api.apps-common.lookups"
  - "core.fusion-api.apps-common.descriptive-flexfields"
  - "hcm.hcm-tool.questionnaire"
  - "hcm.learning-management.learning-catalog.manage-catalog-administration-profiles"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-catalog/self-paced-learning/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-catalog/self-paced-learning/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
oracle_supplied_guidance_files:
  - purpose: "Input and row-scoped validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Operation-scoped dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Read-only lookup contracts"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Safe defaults and demo generation"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Mandatory design and lifecycle gates"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Approval, retry, and reconciliation gates"
    location: "ora-resource/ora_error_handling.md"
oracle_supplied_guidance_status: "Aligned to OLC-116681 FDD version 5, current public REST documentation, and sanitized target Describe evidence reviewed 2026-09-22"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release; target metadata and enabled values must be refreshed at runtime"
side_effects:
  - "After Data Loader registration and contract validation, an immutable preview, and exact approval, may submit one supported parent create or update through core.data-loader."
  - "After a fresh immutable preview and exact approval, may submit one documented activation or another task-listed Direct REST exception when Data Loader does not expose that exact operation."
  - "After a fresh immutable preview and exact approval, may submit one documented Self-Paced Learning content mutation only through Data Loader or a task-listed Direct REST exception."
  - "A multi-row request may submit only its independently approved valid rows once and returns row-scoped results."
required_privileges:
  - "Authenticated Data Loader access to the registered learningSelfPacedItems business object and its supported operations"
  - "Authenticated read access to learningSelfPacedItems and its documented child resources and actions"
  - "Applicable Direct REST write access only for an explicitly selected exception"
  - "Read-only access to applicable Worker or Public Worker, language, lookup, questionnaire, HCM list, catalog profile, and flexfield metadata resources"
  - "Learning administrator authorization for the requested mutation"
---

# Self-Paced Learning Setup Task Guidance

## Purpose

Use this canonical task skill to create, read, update, publish, reprocess, or
delete Self-Paced Learning items and to manage their documented content child.
The earlier task label Self-Paced Learning is accepted as a routing
synonym only; persisted artifacts and new routing use the canonical task ID,
code, name, and folder in this manifest.

## Source Contract

The business rules come from OLC-116681 FDD version 5, section OLC-120241,
reviewed 2026-09-22. The wire contract comes from Oracle's public Self-Paced
Learning and Learning Content REST documentation and the sanitized raw target
Describe reviewed 2026-09-21. The Describe inventory has 20 resource nodes,
410 attributes, 77 LOV-decorated attributes, and 300 queryable attributes.
Do not persist the source environment hostname or treat its enabled values as
portable between pods.

The confirmed raw REST contract includes collection GET and POST; item GET,
PATCH, and DELETE; collection publish; item reprocess; exact number and ID
finders; and content collection and item GET, POST, PATCH, and DELETE. Parent
creation requires a learning item number and visibility and defaults status to
ORA_DRAFT. The Describe createability of content `status` and `autoCommit`
applies to the standalone child resource and does not make them mandatory in a
parent deep insert. For a parent deep insert, omit child `status` and
`autoCommit`; the successful trace did so and Fusion derived
`status=ORA_ACTIVE` and `autoCommit=Y`. Upsert metadata is not
exposed as a user-facing operation in this release.

Always follow the item or child link returned by Fusion. Never construct an
opaque item hash. No supplied source confirms ETag or If-Match, so freshness is
enforced with immediate read, normalized fingerprints, single submission, and
post-write readback rather than an atomic-concurrency claim.

## Route Summary

- Canonical mutation route: `core.data-loader` with the exact registered
  business object `learningSelfPacedItems`.
- Before create or update, resolve one exact registration, the current template
  and component attributes, and the operation supported by the live target.
- Direct REST is read-only for Describe, collision/current-state checks, and
  readback, except for the operation-specific exceptions below.
- Activation may use the proven returned-item PATCH only when Data Loader does
  not expose the required status update. The exception sets
  `learningItemStatus` to `ORA_ACTIVE` with
  `Effective-Of: RangeMode=UPDATE` and requires its own preview and approval.
- Publish, reprocess, delete, or content-child mutations may use Direct REST
  only when their exact row below is selected, live Data Loader metadata proves
  the operation unavailable, and current REST metadata still confirms the
  route. There is no automatic fallback.
- When neither route is authorized, stop with an operation-scoped blocker.

## Supported Operations

| Operation | Route Contract | Required Safeguard |
|---|---|---|
| Read or collision check | Collection finder, returned item link, and documented child links | Exact match and complete paged evidence |
| Create draft | Data Loader BC REST for learningSelfPacedItems | Exact live registration, template validation, number collision check, required values, immutable artifact, and approval |
| Update | Data Loader BC REST for learningSelfPacedItems | Supported live update operation, fresh current-state fingerprint, and narrow delta |
| Activate | Data Loader update when supported; otherwise the documented returned-item PATCH exception | Set learningItemStatus to ORA_ACTIVE; for the exception send Effective-Of RangeMode=UPDATE; verify Active, DraftExists=N, and PublishedExists=Y |
| Publish content | Documented collection publish action as a distinct Direct REST exception | Do not treat it as item activation; require current action metadata, content readiness, and separate approval |
| Reprocess | Documented returned-item reprocess action as a Direct REST exception | Applicable rich-media state and exact parameters |
| Delete item | Documented returned-item DELETE exception | Eligible state, no unresolved usage/history impact, and explicit approval |
| Content CRUD | Data Loader when supported; otherwise documented content child links as an exception | Compatible content type, current child identity, and state-specific rules |

## Read Order

1. ora-resource/ora_input_validation.md
2. ora-resource/ora_dependency_readiness.md
3. ora-resource/ora_reference_lookups.md
4. ora-resource/ora_defaulting_rules.md
5. ora-resource/ora_design_enforcement.md
6. ora-resource/ora_error_handling.md
7. ora-resource/ora_rule_registry.json

Before consuming the registry, load the repository Ora-Resource Task Node
Execution Guide and require a current successful planner result. Registry
readiness does not authorize a Fusion write.

## Input Modes

- A single guided request supplies one item intent and zero or one supported
  content source.
- A multi-row file or table represents one independent Self-Paced Learning
  request per row. Validate, resolve, preview, approve, submit, and reconcile
  each row independently. Invalid rows do not become payloads.
- A demo request can omit item metadata. Generate ten candidates when count is
  omitted, accept an explicit count from one through ten, and reject a request
  above ten. A supplied industry, domain, or topic guides generation.

For demo candidates, generate reviewable title, short or long description,
expected effort, and an Article plus URL intent. Resolve an actual compatible
content type, reachable absolute URL, visibility, and the target's one verified
default seeded Catalog Administration Profile before execution. Generated
Objective and Ideal Learner text is preview metadata only because neither field
exists in the confirmed REST schemas. Execution requires an explicit approval
that accepts their omission from the REST request and readback. Never silently
place either value into another field.

## Workflow

1. Normalize the requested operation, target environment, input mode, item
   values, content intent, row identity, and lifecycle intent.
2. Validate business minimums. For an ordinary create require title, subtype or
   content type, and compatible content intent; resolve the REST-required number
   and visibility before preview. Owner, language, and effective dates are
   conditional, not universal create blockers.
3. Resolve applicable dependencies only. Read owner identity through the
   documented Worker or Public Worker read route, convert a supplied language
   label through the active installed-language lookup, and resolve exact current
   item, content, status, questionnaire, HCM list, catalog profile, or DFF
   evidence only when the operation uses it.
4. For an existing item, use findByLearningItemNumber or
   findByLearningItemId, follow the returned item link, and fingerprint identity,
   last-modified time, lifecycle, content, metrics, where-used relationships,
   action hints, and change-request processing state.
5. Build an immutable sanitized preview. For multi-row input include every row,
   its validation state, exclusions, resolved references, intended operation,
   before/after values, and one aggregate manifest fingerprint made from the
   row fingerprints. For demo input also show generated provenance and the
   Objective and Ideal Learner omission.
6. Obtain fresh explicit approval for the exact environment, operation, item or
   row manifest, dependencies, content reference, business effects, omission
   choices, and preview fingerprint. Any changed row or target state invalidates
   that approval.
7. Submit each approved create or update once through `core.data-loader` using
   the exact immutable artifact and approved loader contract. Use Direct REST
   only for a Route Summary exception whose Data Loader operation check proved
   unavailable. Do not automatically retry POST, PATCH, DELETE, import, upload,
   publish, or reprocess. Stop the batch on an uncertain write and reconcile
   before any new attempt.
8. Follow documented change-request or content-processing state within a
   bounded poll window when applicable. Return the sanitized process identifier,
   last status, and safe next check on timeout.
9. Read the parent and applicable child again and compare persisted fields and
   unchanged protected state with the approved preview. Return verified,
   partial, failed, or indeterminate results per row.

## Preflight, Failure, and Redaction

Preflight every selected row immediately before submission. Reconfirm the
environment, operation, exact item or create key, returned links, applicable
dependencies, privileges, payload shape, current fingerprint, preview scope,
and approval. A validation or reference failure stops the affected row before
side effects. Apply the row-scoped error handling in ora_error_handling.md to
execution, timeout, partial, and readback failures; an uncertain write stops
later submissions and is reconciled by safe reads without automatic replay.
Never print or persist credentials, tokens, binary bodies, environment
hostnames, raw sensitive responses, or unnecessary person data. Keep only the
minimum sanitized identifiers and diagnostics required for a safe next action.

## FDD Acceptance Traceability

| FDD Test | Covered Scenario |
|---|---|
| SPL-AT-01 | Missing ordinary-create title, subtype, or content intent stops before proposal or write |
| SPL-AT-02 | Supported URL or binary content is validated, approved, persisted, and read back |
| SPL-AT-03 | Invalid MIME, URL, questionnaire, or processing state blocks only the affected row |
| SPL-AT-04 | Private publish resolves exact CAP and audience evidence before separate approval |
| SPL-AT-05 | Content replacement discloses active and completed assignment impact |
| SPL-AT-06 | Activation, deactivate, reactivate, content delete, and item delete enforce route, state, history, and readback gates |
| SPL-AT-07 | Mixed valid and invalid rows are corrected or excluded and return row-scoped results |
| SPL-AT-08 | A changed item or row invalidates its approval and requires a refreshed preview |
| SPL-AT-09 | No-input demo generation defaults to ten, caps at ten, previews generated data, and writes only approved compatible fields |

## Execution and Refusal Rules

- Data Loader BC REST through `core.data-loader` is the canonical mutation
  route. The catalog's CSV flags remain N; user-supplied CSV is intake, while
  the loader prepares and validates its own immutable artifact.
- Do not use a Direct REST mutation as a fallback. It must be a named Route
  Summary exception with current unsupported-operation evidence from Data
  Loader, an exact preview, and operation-specific approval.
- Do not require content `status` or `autoCommit` for a parent deep insert.
  Omit both and verify Fusion derived `ORA_ACTIVE` and `Y`. Apply standalone
  child-resource requirements only when that exact exception is selected and
  current Describe confirms them.
- Do not map UI Activate to the collection publish action. Activate through a
  supported Data Loader update or the documented returned-item PATCH exception,
  then verify Active, DraftExists=N, and PublishedExists=Y without changing the
  approved content source.
- Do not send Objective, Ideal Learner, learningItemSourceId,
  learningItemSourceType, or learningItemSourceInformation through these REST
  routes; they are absent from the confirmed schemas.
- Do not infer owner identity from a display-name first match, language codes
  from English labels, status codes from meanings, or target-specific DFF
  segments from another environment.
- Do not publish incomplete or still-processing required content.
- Do not delete content unless the item is in the FDD-permitted inactive state.
  Do not delete a parent with unresolved assignments, transcripts, or where-used
  relationships. If completion preservation requires an operation parameter not
  present in the confirmed contract, stop rather than invent it.
- Do not treat an HTTP success, an action acceptance, or a change-request ID as
  proof of final success. Report success only after the required readback agrees.
- Redact credentials, tokens, binary bodies, opaque URLs, and environment hosts
  from project artifacts and routine output.

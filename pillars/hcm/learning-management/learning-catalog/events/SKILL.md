---
skill_id: "hcm.learning-management.learning-catalog.events"
name: "Events Setup Task Guidance"
description: "Plans, validates, previews, executes, and verifies approval-gated Learning Catalog event changes."
layer: "pillar"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Catalog"
functional_area_code: "ORA_LEARNING_CATALOG"
task_code: "CUSTOM_EVENTS"
task_name: "Manage Events"
parent_skill_id: "hcm.learning-management.learning-catalog"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "learningEvents"
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
  - "event_rows"
  - "schedule_and_resource_plans"
  - "current_state_evidence"
  - "execution_intent"
  - "approval"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "dependency_readiness"
  - "row_results"
  - "change_preview"
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
  - "core.fusion-api.apps-common.value-sets"
  - "core.fusion-api.apps-common.descriptive-flexfields"
  - "hcm.hcm-security.hcm-security-profile"
  - "hcm.hcm-tool.questionnaire"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-catalog/events/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-catalog/events/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
oracle_supplied_guidance_files:
  - purpose: "Input, row-scope, operation, and verification rules"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Conditional dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Read-only event and resource lookup contracts"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Safe draft and linkage defaults"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Activation, schedule, resource, lifecycle, and stale-state gates"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Approval, execution, error, reconciliation, and refusal rules"
    location: "ora-resource/ora_error_handling.md"
oracle_supplied_guidance_status: "source-aligned with FDD v5, public REST guidance, and sanitized target Describe evidence"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "After live registration validation, an exact row-scoped preview, and fresh explicit approval, may create or update eligible events through core.data-loader."
  - "After the same gates and unavailable Data Loader operation evidence, may use a listed Direct REST exception for copy, lifecycle, or documented activity-child mutations."
required_privileges:
  - "Authenticated Data Loader access to the registered learningEvents business object and supported components"
  - "Read-only access to learningEvents and applicable write access for a listed Direct REST exception"
  - "Read access to applicable course, supplier, instructor, classroom, virtual-classroom, lookup, and extensibility resources"
  - "Learning administrator privileges required by the selected operation"
---

# Events Setup Task Guidance

## Purpose

Use this skill to plan, validate, preview, execute, and verify the Event
scenarios in OLC-116681 FDD version 5. It supports standalone and course-linked
events, incomplete Draft capture, activation-ready schedules, multiple
activities, row-scoped mixed inputs, and safe lifecycle changes.

## Canonical Task Contract

- Skill ID: `hcm.learning-management.learning-catalog.events`
- Task code: `CUSTOM_EVENTS`
- Task name: `Events`
- Functional area code: `ORA_LEARNING_CATALOG`
- Data Loader business object: `learningEvents`
- Import mode: Data Loader BC REST through `core.data-loader`; CSV
  export/import is not a catalog-supported transfer route.

The word *row* means one logical event request, whether it came from a prompt,
JSON, a table, or a user-supplied CSV used only as intake. A CSV does not turn
this task into a CSV import operation.

## Route Summary

- Canonical create and update route: `core.data-loader` with the exact live
  registration for `learningEvents`.
- Resolve the registration, current template and components, and supported
  operation before preparing an immutable loader artifact.
- Use Direct REST for Describe, duplicate and current-state reads, resource
  lookups, and post-load verification.
- Copy, lifecycle actions, and activity-child mutations are Direct REST
  exceptions only when live Data Loader metadata does not expose that exact
  operation and the current REST contract still confirms it. Obtain a separate
  route-specific preview and approval; never fall back automatically.
- Block when neither Data Loader nor a listed exception supports the operation.

## Source and Route Contract

OLC-116681 FDD version 5 and OLC-120242 define the business behavior. Oracle's
public Learning Events REST guide documents the event and activity resources.
The sanitized developer-supplied raw target Describe, reviewed 2026-09-22,
contains 21 resource nodes, 365 attributes, 56 LOV-decorated attributes, and
283 queryable attributes. It confirms:

- [OLC-116681 FDD](https://confluence.oraclecorp.com/confluence/display/VS/OLC-116681+FDD+%5BP1%5D+Learning+Catalog+Setup+Skill)
- [Oracle Learning Events REST endpoints](https://docs.oracle.com/en/cloud/saas/human-resources/farws/api-learning-events.html)
- sanitized raw target `learningEvents` Describe and auxiliary-resource
  Describes supplied for this implementation; raw files and target hosts are
  not persisted in this skill

- collection GET and POST create;
- item GET and PATCH;
- the `copy` action;
- `findByLearningItemNumber` and `PrimaryKey` finders;
- activity collection GET and POST and activity item GET, PATCH, and DELETE;
- required, defaulted, writable, and read-only fields and exact lookup routes.

The raw contract does not expose parent-event DELETE or a finalize action.
Those operations are unsupported even though FDD test EVT-AT-05 asks the
skill to handle them. The Describe advertises upsert metadata, but this
release intentionally exposes explicit create versus update plans only.

Create requires event number and visibility at the REST layer and defaults
status to `ORA_DRAFT`. This skill sends Draft explicitly when Draft behavior
is intended. The only confirmed standard DFF context is
`WLF_LEARNING_ITEM`; actual target segments must be read from live metadata.
No supplied payload advertises ETag or `If-Match` support.

Auxiliary raw target Describes establish read-only validation contracts for:

- `learningCourses` for exact course linkage;
- `learningTrainingSuppliers` for exact supplier identity;
- `learningInstructors` for identity, status, schedule availability, and its
  `learningVirtualClassrooms` child;
- `learningClassrooms` for identity, status, location, schedule availability,
  and capacity;
- `commonLookupsLOV` routes named by the Event and auxiliary schemas.

These auxiliary resources are validators only. This skill never creates,
updates, deletes, or upserts a course, supplier, instructor, classroom, or
provider account.

## Read Order

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_dependency_readiness.md`
3. `ora-resource/ora_reference_lookups.md`
4. `ora-resource/ora_defaulting_rules.md`
5. `ora-resource/ora_design_enforcement.md`
6. `ora-resource/ora_error_handling.md`
7. `ora-resource/ora_rule_registry.json`

## Supported Operations

| Operation | Authoritative route | Execution rule |
|---|---|---|
| Read or duplicate check | Event collection finder, then the server-returned item link | Read-only; require zero or one exact business-key result as appropriate |
| Create Draft | Data Loader BC REST for learningEvents | May preserve an incomplete schedule; require live registration, template validation, identity fields, and every activation gap |
| Update | Data Loader BC REST for learningEvents | Preserve omitted values; validate only changed fields and their dependencies |
| Copy | Direct REST exception using learningEvents/action/copy | Require unavailable Data Loader operation evidence, source identity, a new unique number and title, preview, and approval |
| Activate, cancel, reactivate, reschedule, or close | Data Loader update when supported; otherwise a confirmed item PATCH exception | Require live enabled LOV values, FDD transition eligibility, fresh impact evidence, and route-specific approval |
| Create activity | Data Loader component operation when supported; otherwise the returned activities child POST exception | Require activity number and status plus operation-specific schedule/resource fields |
| Read activity | GET the returned activities link or exact activity item link | Read-only |
| Update activity | Data Loader component operation when supported; otherwise the returned activity item PATCH exception | Require current event/activity fingerprints and changed-field validation |
| Delete activity | Returned activity item DELETE exception | Require unavailable Data Loader operation evidence, usage/enrollment/history safety, preview, and approval |
| Finalize event | No authoritative route | Unsupported; stop before approval |
| Delete parent event | No authoritative route | Unsupported; stop before approval |

Never manufacture an opaque item hash. Follow the link returned by the exact
finder or collection response for the parent and child item routes.

## Draft and Activation Boundary

An incomplete schedule, capacity plan, instructor, classroom, or webinar
resource does not block creation of an otherwise valid Draft. The preview must
list every missing activation requirement, and the created row remains Draft.
An activation request is stricter: every activity must fit inside the event
boundary, all required schedule and enrollment fields must be complete, every
applicable resource must resolve and be available, classroom capacity must
cover planned demand, and the status transition must be live-valid and
FDD-eligible.

Do not use Draft permissiveness to omit REST-required identity or visibility,
to send unsupported fields, or to bypass a dependency explicitly included in
the Draft payload.

## Row-Scoped Workflow

1. Normalize one or more event rows and assign each a stable local row key.
2. Validate identity, operation, target environment, supplied fields, and the
   operation-specific minimum for each row. Reject finalize and parent delete
   immediately.
3. Resolve current state and only the dependencies applicable to that row.
   An unresolved row does not erase valid rows or make the entire task
   registry unavailable.
4. Apply safe defaults and enforce Draft-versus-activation, schedule,
   capacity, resource, lifecycle, and stale-state rules per row.
5. Return one row result: `READY_FOR_PREVIEW`, `DRAFT_WITH_ACTIVATION_GAPS`,
   `BLOCKED`, or `NO_CHANGE`.
6. Build an immutable preview for every row selected for execution. Bind the
   target, operation, parent and child payload intent, current-state and
   dependency fingerprints, and expected readback to that preview.
7. Obtain fresh explicit approval for the exact selected-row preview. Mixed
   input never implies approval to execute all rows.
8. Immediately refresh each selected row's current event and applicable
   resource evidence. Any change invalidates that row's approval.
9. Submit each still-valid create or update once through `core.data-loader`, in
   deterministic row order. Use only a Route Summary exception for an
   unsupported loader action or child operation. Do not batch unrelated rows
   into one assumed transaction and do not automatically retry any load,
   write, upload, or action call.
10. Follow server-returned links and read back identity, lifecycle, schedule,
    capacity, activities, learner-impact metrics, usage, and last-modified
    state. Report each row independently as verified, partial, failed,
    indeterminate, or blocked.

## Resource Validation

- Course linkage uses one exact active course by number or ID.
- Supplier linkage uses `findByTrainingSupplierNumber` and a live enabled
  `ORA_WLF_LI_STATUS` value.
- Instructor validation always resolves `findByInstructorNumber`; activation
  or active scheduling additionally uses the schedule-aware `findByWord`
  contract with the exact activity window and course ID where supported. The
  target's affirmative `instructorAvailability` value is then required.
  `hasFutureBookings` is informational only.
- Classroom validation always resolves `findByClassroomNumber`; activation or
  active scheduling additionally uses the schedule-aware `findByWord`
  contract. The target's affirmative `classroomAvailability` value and
  `classroomCapacity` at least equal to planned demand are then required.
- Provider-backed webinars resolve one virtual-classroom account by its exact
  raw finder. For activation or active scheduling, the `validateProviderUser`
  action exposes an opaque payload and result; run it only when the caller
  supplies an approved provider-specific request and success-evaluation
  contract. A fixed meeting URL remains governed by the Event schema and does
  not automatically require this action.
- Event ad hoc-resource child rows prove assignment, not a global resource or
  conflict contract. A row requesting an ad hoc resource stops until an
  approved provider supplies exact identity, quantity, and availability
  evidence. Rows without ad hoc resources continue.

## Concurrency, Approval, and Retry Discipline

Because there is no confirmed atomic conditional-write mechanism, use a
defensive sequence: preflight read, immutable preview fingerprint, explicit
approval, immediate pre-write refresh, one submit, and post-write readback.
This detects but cannot eliminate every race. State that limitation in the
preview.

Approval is valid only for the exact target, row set, operation, payload
intent, event/activity identities, schedule, enrollment and capacity counts,
resource evidence, lifecycle state, and fingerprint shown. Any change requires
a new preview and approval. A cache-managed authentication refresh may occur
once for a read; a POST, PATCH, DELETE, or action call is never replayed
automatically.

## Preflight, Failure, and Redaction

Preflight each selected row against its current event, activity, enrollment,
resource, route, fingerprint, privilege, and approval evidence immediately
before submission. Apply the row-scoped error handling classifications in
`ora_error_handling.md` to every validation, execution, and verification
failure. Never print or persist credentials, tokens, environment hostnames,
raw request or response bodies, or sensitive learner and provider data; redact
diagnostics to the minimum sanitized identifiers and evidence needed for a
safe next action.

## Acceptance Traceability

| FDD Test | Covered Scenario |
|---|---|
| EVT-AT-01 | Missing event identity is rejected per row |
| EVT-AT-02 | Valid Draft creation and separately gated activation |
| EVT-AT-03 | Schedule, resource, and capacity errors; incomplete Draft remains permitted |
| EVT-AT-04 | Active-event reschedule with fresh enrollment and resource evidence |
| EVT-AT-05 | Cancel and reactivate checks; explicit refusal of unsupported finalize and parent delete |
| EVT-AT-06 | Duplicate through the exact copy action with a unique target identity |
| EVT-AT-07 | Mixed-row CSV intake with row-scoped validation, preview, execution, and results |
| EVT-AT-08 | Stale event or resource state invalidates approval before submission |

## Refusal Rules

- Do not write without an immutable preview and fresh explicit approval.
- Do not bypass `core.data-loader` for a supported create or update, and do not
  use a Direct REST exception without current unsupported-operation evidence.
- Do not treat an incomplete Draft as activation-ready.
- Do not infer lookup codes, availability meanings, provider payload members,
  ad hoc-resource routes, DFF segments, or opaque item hashes.
- Do not finalize or delete a parent event.
- Do not expose Describe-advertised upsert as a user-facing operation.
- Do not retry an uncertain write, claim transactionality across rows, or
  claim success until readback matches the approved result.
- Do not persist credentials, raw payloads, environment hostnames, or sensitive
  response bodies in project artifacts.

## Implementation Notes

Use the parent functional-area skill for cross-task sequencing. Track token
usage only when this task writes a project artifact or skill-run record.

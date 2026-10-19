---
skill_id: "hcm.learning-management.learning-catalog.courses"
name: "Courses Setup Task Guidance"
description: "Provides approval-gated definition, default-resource, relationship, lifecycle, and reconciliation guidance for Learning Catalog courses."
layer: "pillar"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Catalog"
functional_area_code: "ORA_LEARNING_CATALOG"
task_code: "CUSTOM_COURSES"
task_name: "Manage Courses"
parent_skill_id: "hcm.learning-management.learning-catalog"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "learningCourses"
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
  - "course_definition"
  - "offering_and_relationship_plan"
  - "current_state_evidence"
  - "execution_intent"
  - "approval"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "dependency_readiness"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-catalog/courses/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-catalog/courses/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
oracle_supplied_guidance_files:
  - purpose: "Input contract and verification rules"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Read-only lookup contracts"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Safe default behavior"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Mandatory design gates"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Approval, error, and recovery gates"
    location: "ora-resource/ora_error_handling.md"
oracle_supplied_guidance_status: "FDD v5 and target-Describe aligned with request-scoped child-eligibility gates"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "After live registration validation, an exact preview, applicable dependency resolution, and fresh explicit approval, may create or update a course through core.data-loader."
  - "After the same gates and unavailable Data Loader operation evidence, may use a listed Direct REST exception for copy, activation, or retirement."
required_privileges:
  - "Authenticated Data Loader access to the registered learningCourses business object"
  - "Read-only access to learningCourses and applicable write access for a listed Direct REST exception"
  - "Learning administrator privileges required by the selected operation"
---

# Courses Setup Task Guidance

## Purpose

Use this skill to plan, validate, preview, execute, and verify Courses changes
described by the Manage Courses section of OLC-116681 FDD v5. The current
taxonomy identity is Manage Courses, matching the FDD wording.

## Route Summary

- Canonical create and update route: `core.data-loader` with business object
  `learningCourses`.
- Before a mutation, require one exact live registration, the current template
  and component attributes, and support for the intended operation.
- Use Direct REST for Describe, identity/current-state reads, dependency
  resolution, and post-load readback.
- Copy and lifecycle PATCH are Direct REST exceptions only when live Data
  Loader metadata does not expose the exact operation and current REST metadata
  still confirms it. There is no automatic fallback.
- Parent/activity deletion remains unsupported. Block any other mutation when
  neither Data Loader nor a listed exception provides an authoritative route.

## Supported Scope

- Create a Draft course with an optional user-supplied course number.
- Read and update lifecycle, visibility, publication, validity, renewal,
  default capacity, waitlist, facilitator, instructors, activities, metrics,
  usage, and applicable change requests.
- Validate default instructors and type-routed facilitators through read-only
  instructor and training-supplier contracts.
- Treat the activities child as current membership and assignment-impact
  evidence, not as proof that a new child is eligible.
- Copy through the exact three-parameter target action only as a Route Summary
  exception and verify the returned copy is Draft before claiming success.
- Activate or retire through Data Loader update when supported; otherwise use
  the listed learningItemStatus PATCH exception after live value and
  FDD-transition validation.
- Reject parent deletion, activity deletion, and user-facing upsert because
  they are outside the confirmed release contract.

New offering or child eligibility and course-versus-learning-path exclusivity remain
request-scoped and non-executable until an authoritative resolver is available.
They do not block reads, parent-only Draft creation, default-resource changes,
copy, or lifecycle operations that do not add or replace a child.

## Source and Route Contract

The sanitized raw learningCourses Describe supplied for the preproduction
target contains 15 resource nodes, 307 attributes, 46 LOV-decorated
attributes, and 252 queryable attributes. It confirms collection GET/POST,
item GET/PATCH, copy, exact number and ID finders, writable/read-only fields,
activities, defaults, lookup routes, and WLF_LEARNING_ITEM. Parent DELETE and
activity DELETE are absent. No Course-specific DFF context is confirmed or
portable.

The target defaults type to ORA_COURSE, status to ORA_ACTIVE, and visibility
to PUBLIC. FDD Draft creation must send and live-validate ORA_DRAFT explicitly.
Copy accepts learningItemNumber, learningItemTitle, and
learningItemCatalogProfileNumber. Follow returned item links rather than
constructing opaque hashes. The payload declares no ETag or If-Match contract.
The Courses contract remains target-scoped until Oracle publishes a portable
public contract.

The supplied auxiliary Describes confirm read-only validation contracts for
learningInstructors and learningTrainingSuppliers and their exact number
finders. The Course Describe supplies ORA_WLF_FACILITATOR_TYPE and the
read-only courseDefaultInstructorDetails child. Do not derive
courseDefaultInstructors request serialization from that read-only child.
Parent and activity deletion are unsupported.

## Read Order

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_dependency_readiness.md`
3. `ora-resource/ora_reference_lookups.md`
4. `ora-resource/ora_defaulting_rules.md`
5. `ora-resource/ora_design_enforcement.md`
6. `ora-resource/ora_error_handling.md`
7. `ora-resource/ora_rule_registry.json`

## Workflow

1. Normalize the operation, environment, one or many rows, identity, parent
   definition, defaults, offerings, relationships, validity, and lifecycle.
2. Validate each row independently; correct, version, exclude, or retain it
   without silently changing other rows.
3. Resolve existing identity with findByLearningItemNumber or
   findByLearningItemId, follow the returned item link, and read defaults,
   instructors, activities, metrics, usage, and change-request state.
4. Resolve each supplied default instructor, facilitator type, and type-routed
   facilitator. Resolve owner/person labels through the documented read-only
   Worker contract when a technical identifier is not supplied.
5. Block only rows that add or replace offerings or child learning while
   eligibility and exclusivity evidence is unavailable.
6. Validate explicit Draft status, defaults, assignment impact, lifecycle
   readiness, and copy parameters; produce immutable row-specific previews.
7. Execute only valid approved rows. Immediately reread current state, compare
   its fingerprint, submit each supported create or update once through
   `core.data-loader`, and use only a Route Summary exception for an unsupported
   copy or lifecycle operation. Never automatically retry.
8. Reconcile documented asynchronous processing and read back identity,
   lifecycle, defaults, activities, instructors, metrics, usage, and
   applicable change-request state.

## CSV and Data Loader Boundary

The effective catalog does not advertise native CSV export/import. Multi-row
inputs are intake for individually validated Data Loader records and are not
native task-level CSV support. The raw Describe does not prove registration.
Use `core.data-loader` to resolve the exact live business object, template,
components, and operation; missing or ambiguous registration blocks mutation
while read-only REST planning may continue.

## Acceptance Traceability

| FDD Test | Covered Scenario |
|---|---|
| CRS-AT-01 | Missing course identity or minimum definition returns row-specific corrections |
| CRS-AT-02 | A valid course is created explicitly as Draft with approved defaults |
| CRS-AT-03 | Missing, inactive, ineligible, conflicting, or ambiguous child evidence blocks only affected rows |
| CRS-AT-04 | Activation without a valid learning option or complete readiness evidence stops before approval |
| CRS-AT-05 | Updating defaults or children on a course with assignments refreshes impact and relationship evidence |
| CRS-AT-06 | Copy uses the exact action and verifies Draft readback; retirement uses a validated status transition |
| CRS-AT-07 | Mixed rows receive independent validation, previews, approval selection, execution, and results |
| CRS-AT-08 | Changed course, resource, child, assignment, or lifecycle evidence invalidates preview and approval |

## Approval, Retry, and Diagnostics

Approval is bound to the exact environment, course identity or create key,
operation, selected rows, relationship effects, and preview fingerprint.
Refresh cache-managed authentication once for a 401 or 403. Never
automatically retry POST, PATCH, or copy. Return the failure class, affected
row, current rule, sanitized evidence, verified side effects, and one safe
next action without exposing credentials, opaque identifiers, or full
response bodies.

## Preflight and Failure Handling

Preflight checks confirm target identity, privileges, operation support,
course identity or create key, applicable dependencies, current-state
fingerprint, exact preview, and fresh approval before any side effect. Error
handling classifies input, metadata, authorization, transport, Fusion API,
timeout, process, persistence, and approval failures. Redact credentials,
tokens, secrets, opaque identifiers, and full response bodies from diagnostics
and durable artifacts.

## Controlled Reentrancy

This enriched manifest must not be replaced by an unreviewed generator rerun.
Future taxonomy regeneration must preserve the authored body, version,
hybrid execution contract, resources, and canonical task identity, with the
contract tests serving as the regression guard.

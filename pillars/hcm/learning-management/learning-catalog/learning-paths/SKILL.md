---
skill_id: "hcm.learning-management.learning-catalog.learning-paths"
name: "Learning Paths Setup Task Guidance"
description: "Provides approval-gated definition, graph validation, lifecycle, and reconciliation guidance for Learning Catalog learning paths."
layer: "pillar"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Catalog"
functional_area_code: "ORA_LEARNING_CATALOG"
task_code: "CUSTOM_LEARNING_PATHS"
task_name: "Manage Learning Paths"
parent_skill_id: "hcm.learning-management.learning-catalog"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "learningPaths"
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
  - "learning_path_definition"
  - "section_activity_and_dependency_plan"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-catalog/learning-paths/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-catalog/learning-paths/current/"
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
oracle_supplied_guidance_status: "FDD v5 and target-Describe aligned with request-scoped activity eligibility gates"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "After live registration validation, an exact preview, applicable activity resolution, and fresh explicit approval, may create or update a learning path through core.data-loader."
  - "After the same gates and unavailable Data Loader operation evidence, may use a listed Direct REST exception for lifecycle, safe deletion, section, or nested-activity mutations."
required_privileges:
  - "Authenticated Data Loader access to the registered learningPaths business object and supported components"
  - "Read-only access to learningPaths and applicable write access for a listed Direct REST exception"
  - "Learning administrator privileges required by the selected operation"
---

# Learning Paths Setup Task Guidance

## Purpose

Use this skill to plan, validate, preview, execute, and verify Learning Paths
changes described by the Manage Learning Paths section of OLC-116681 FDD v5.
The current taxonomy identity is Manage Learning Paths, matching the FDD wording.

## Route Summary

- Canonical create and update route: `core.data-loader` with business object
  `learningPaths`.
- Resolve one exact live registration, its template and component hierarchy,
  and the selected operation before creating the immutable loader artifact.
- Use Direct REST for Describe, identity/current-graph reads, reference checks,
  and post-load verification.
- Lifecycle, parent deletion, section CRUD, and nested-activity CRUD are Direct
  REST exceptions only when live Data Loader metadata does not expose that
  exact operation and the current REST contract confirms it. Never fall back
  automatically.
- Copy remains unsupported. Block every mutation without a supported loader
  operation or a listed exception.

## Supported Scope

- Create an explicitly requested empty Draft or a Draft with ordered sections
  and activities.
- Read current identity, lifecycle, validity, renewal, sections, activities,
  predecessor relationships, usage, metrics, and change requests.
- Validate display and completion-access predecessor references, ordering,
  dangling references, self-references, and direct or indirect cycles.
- Create and update the parent through Data Loader; manage sections and nested
  activities through registered components or listed CRUD exceptions.
- Activate or retire through Data Loader update when supported; otherwise use
  the listed learningItemStatus PATCH exception after live value and
  FDD-transition validation.
- Delete a parent only as a listed exception after current usage and
  learner-impact evidence proves deletion safe.
- Reject copy and user-facing upsert because neither is an approved operation.
  Copy remains unsupported.

New-activity eligibility for a new or replaced activity remains request-scoped and non-executable
until an authoritative catalog-item resolver is available. It does not block
an empty Draft, reads, current-graph validation, or mutations that do not add
or replace an activity.

## Source and Route Contract

The sanitized raw learningPaths Describe reviewed from the supplied
preproduction target contains 16 resource nodes, 292 attributes, 41
LOV-decorated attributes, and 239 queryable attributes. It confirms collection
GET and POST, item GET/PATCH/DELETE, exact finders, section CRUD, nested
activity CRUD, required/defaulted/writable properties, lookup routes,
WLF_LEARNING_ITEM, and WLF_LI_SPECIALIZATION. Copy is absent.

A path number is required. The target defaults type to ORA_SPECIALIZATION,
status to ORA_ACTIVE, and visibility to PUBLIC. FDD Draft creation must send
and live-validate ORA_DRAFT explicitly. Sections require a section number and
status; nested activities require an activity number. Follow returned item
links instead of constructing opaque hashes. The payload declares no ETag or
If-Match contract. Courses and Learning Paths remain target-scoped until
portable public REST contracts are published.

## Read Order

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_dependency_readiness.md`
3. `ora-resource/ora_reference_lookups.md`
4. `ora-resource/ora_defaulting_rules.md`
5. `ora-resource/ora_design_enforcement.md`
6. `ora-resource/ora_error_handling.md`
7. `ora-resource/ora_rule_registry.json`

## Workflow

1. Normalize the operation, environment, one or many input rows, identity,
   empty-Draft intent, sections, activities, edges, validity, renewal, and
   lifecycle intent.
2. Validate each row independently. Group rows for the same path before
   section, membership, ordering, and graph validation.
3. Resolve current identity with findByLearningItemNumber, PrimaryKey, or
   RowFinder with pLearningItemId and follow the returned item link.
4. Read current sections, activities, predecessor edges, validity, renewal,
   metrics, usage, and applicable change-request state.
5. Block only rows that add or replace activities while authoritative
   eligibility and relationship evidence is unavailable.
6. For activation, require a non-empty complete structure, valid graph, live
   status value, and allowed transition. An explicitly requested empty Draft
   bypasses only the structure requirement, never identity or approval gates.
7. Produce row-specific validation outcomes and a versioned immutable preview.
   Execute only approved valid rows; any material edit invalidates approval.
8. Immediately reread current state, compare its fingerprint, submit each
   approved create or update once through `core.data-loader`, and use only a
   Route Summary exception for an unsupported lifecycle, delete, section, or
   activity operation. Never automatically retry an uncertain write.
9. Reconcile documented change-request processing and read back the path,
   graph, validity, renewal, usage, metrics, and lifecycle state.

## CSV and Data Loader Boundary

The effective catalog does not advertise native CSV export/import. Multi-row
inputs are grouped and validated before `core.data-loader` prepares the
immutable artifact; they are not native task-level CSV support. The raw
Describe does not prove registration. Missing or ambiguous registration or
component metadata blocks mutation while read-only REST graph analysis may
continue.

## Acceptance Traceability

| FDD Test | Covered Scenario |
|---|---|
| LPT-AT-01 | Missing path identity or required structure input returns row-specific corrections; an empty Draft requires explicit intent |
| LPT-AT-02 | A valid multi-section path preserves ordering, completion rules, activities, and predecessor edges |
| LPT-AT-03 | Missing, inactive, conflicting, dangling, self-referential, or cyclic activity and predecessor evidence blocks the affected rows |
| LPT-AT-04 | Activation of an empty or incomplete path stops before approval |
| LPT-AT-05 | Updating an active path refreshes usage, graph, activity, and learner-impact evidence |
| LPT-AT-06 | Validity and renewal values are checked together and against live enabled values |
| LPT-AT-07 | Mixed rows are grouped per path, graph-validated, previewed, and executed only when individually approved |
| LPT-AT-08 | Changed identity, graph, activity, validity, usage, or lifecycle evidence invalidates the preview and approval |

## Approval, Retry, and Diagnostics

Approval is bound to the exact environment, path identity or create key,
operation, grouped manifest, preview fingerprint, and valid-row selection.
Refresh cache-managed authentication once for a 401 or 403. Never
automatically retry POST, PATCH, DELETE, section, or activity writes. Return
the failure class, affected row, current rule, sanitized evidence, verified
side effects, and one safe next action without exposing credentials, opaque
identifiers, or full response bodies.

## Preflight and Failure Handling

Preflight checks confirm target identity, privileges, operation support, path
identity or create key, applicable graph and usage evidence, current-state
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

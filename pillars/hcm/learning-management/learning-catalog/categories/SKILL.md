---
skill_id: "hcm.learning-management.learning-catalog.categories"
name: "Categories Setup Task Guidance"
description: "Provides approval-gated creation, retrieval, update, Topic-relationship, membership, branding, and reconciliation guidance for Learning Catalog Categories."
layer: "pillar"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Catalog"
functional_area_code: "ORA_LEARNING_CATALOG"
task_code: "CUSTOM_CATEGORIES"
task_name: "Manage Categories"
parent_skill_id: "hcm.learning-management.learning-catalog"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "learningCommunities"
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
  - "category_definition"
  - "topic_relationship_plan"
  - "membership_plan"
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
  - "core.fusion-api.apps-common.profile-options"
  - "core.fusion-api.apps-common.lookups"
  - "core.fusion-api.apps-common.descriptive-flexfields"
  - "hcm.hcm-security.hcm-security-profile"
  - "hcm.hcm-security.hcm-data-role"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-catalog/categories/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-catalog/categories/current/"
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
oracle_supplied_guidance_status: "FDD v7 (updated 2026-09-22 15:54:32) and supplied learningCommunities Describe aligned; unproven child writes remain runtime-gated"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "After live registration validation, exact preview, dependency validation, and fresh explicit approval, may create or update an Active Category through core.data-loader."
  - "After the same gates and unavailable Data Loader operation evidence, may perform a listed Direct REST exception for target-confirmed Topic, membership, or branding child operations."
  - "When a v7 profile-option trigger applies, may route an exact separately approved option change through the Application Profile Option Foundation capability and require readback before Category execution."
required_privileges:
  - "Authenticated Data Loader access to the registered learningCommunities business object and supported components"
  - "Read-only access to learningCommunities and applicable write access for a listed Direct REST exception"
  - "Learning administrator view/manage privileges and Category manager or all-items access required by the selected operation"
  - "Profile-option administration privilege when an applicable dependency value change is explicitly approved"
---

# Categories Setup Task Guidance

## Purpose

Use this skill to plan, validate, preview, execute, and verify Categories
changes described by OLC-120246 in OLC-116681 FDD v7, page 21981496001,
updated 2026-09-22 15:54:32. It creates Categories as
Active, preserves manager and relationship safety, and verifies every attempted
parent and child operation.

## Route Summary

- Canonical parent create and update route: `core.data-loader` with business
  object `learningCommunities` and the exact Category subtype.
- Require one exact live registration, current template and component
  attributes, supported operation, and subtype before mutation preparation.
- Use Direct REST for Describe, subtype/identity/current-state reads,
  dependency lookups, and post-load verification.
- Topic relationships, membership, branding, and other child mutations are
  Direct REST exceptions only when live Data Loader metadata does not expose
  that exact operation and a current returned REST link confirms it. Never
  fall back automatically.
- Block any mutation without a supported loader operation or a listed,
  target-confirmed exception.

## Supported Scope

- Create, retrieve, and update an Active Learning Category with a
  user-provided title, optional summary, visibility, featured dates, branding
  image, and target-confirmed DFF values.
- Resolve an existing Category by ID, number, or subtype-filtered unique title.
- Add or remove accessible Topics and manage association-level featured dates
  only through a target-confirmed Category-to-Topic write contract.
- Add Category managers after creation only through target-confirmed person
  selection. Manage required or voluntary members through target-confirmed
  person, CSV, filtered-list, analysis, user-group, hierarchy-manager, and
  directs capabilities.
- Preserve the creator as initial manager and at least one active manager.
- Treat criteria/group processing as asynchronous when applicable and report
  parent, child, and row outcomes independently.

Direct learning, skills and qualifications, member contributions, and
self-service conversations belong to Topics rather than Categories. Draft,
deactivate, reactivate, object deletion, and generic upsert are outside this
story and must not be exposed.

## Source and Route Contract

The approved baseline maps Categories to the Redwood
`redwood/learning-catalog/main/manage-catalog-organization` experience and to
the BC REST `/learningCommunities` resource. The supplied sanitized file is a
target-specific Describe containing 22 resource nodes, 420 attributes, 36
LOV-decorated attributes, and 359 queryable attributes. It confirms collection
GET/POST, item GET/PATCH,
identity finders, subtype and visibility LOVs, assets, DFFs, membership
criteria, and user access. Its generic DELETE and upsert capabilities are not
authorization to expose operations excluded by the FDD.

The shared endpoint does not itself distinguish Category intent. Resolve and
retain the live Category subtype before every read or write. The supplied
Describe does not prove the subtype code values, Data Loader registration,
every group-selection route, or a writable Category-to-Topic association
contract. It also supplies no ETag or If-Match concurrency contract. Those
capabilities are runtime gates: retain the requested
operation, identify the exact missing capability, and block only affected
parent or child rows. Never invent a path or payload.

## FDD v7 Related Setup and Dependencies

Before proposal or execution, use the Application Profile Option Foundation
Skill through `core.fusion-api.apps-common.profile-options` to read the current
effective values. Evaluate only options whose trigger applies. Record an
already-correct option as satisfied and omit it from the user dialog. Include
every proposed change in the exact immutable approval payload, execute it only
through the governed provider, and read it back before dependent Category work.

| Profile Option | When Relevant | Required Handling |
|---|---|---|
| ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD | Categories are managed through unified Redwood catalog listing or CAP-based administration | Require applicable Catalog Administration Profiles to be created or validated through their separate excluded scope, then set Site to Y only with exact approval/readback and verify intended category or catalog administrator access |
| ORA_WLF_CATG_TOP_REDWOOD_ENABLED | Category management is in scope | Set Site to Y when needed through exact approval/readback, then validate related Category/Topic privileges and HCM data-role access for the intended role |
| ORA_WLF_SS_CATALOG_SEARCH_MODE | Catalog search behavior is being designed or tuned for Categories | Ask whether search should favor broader recall, balanced matching, or tighter precision; preserve the current value unless an exact change is approved, then read it back and test representative searches |

## Read Order

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_dependency_readiness.md`
3. `ora-resource/ora_reference_lookups.md`
4. `ora-resource/ora_defaulting_rules.md`
5. `ora-resource/ora_design_enforcement.md`
6. `ora-resource/ora_error_handling.md`
7. `ora-resource/ora_rule_registry.json`

## Workflow

1. Normalize the operation, target environment, one or many parent rows,
   Category identity, definition, Topic rows, membership rows, branding, and
   whether unified catalog listing/CAP administration or catalog-search design
   makes a conditional profile option relevant.
2. Validate rows independently and preserve stable parent/child row IDs through
   correction, exclusion, versioning, and approval.
3. Use the Application Profile Option Foundation capability to read current
   effective values before proposal or execution. Always evaluate
   `ORA_WLF_CATG_TOP_REDWOOD_ENABLED`; evaluate
   `ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD` only for unified catalog listing or
   CAP-based administration, and `ORA_WLF_SS_CATALOG_SEARCH_MODE` only when
   Category search behavior is being designed or tuned.
4. Record already-correct applicable options as satisfied and omit them from
   the user dialog. Put every proposed option change in the exact approval
   payload, route it through the governed provider, and read it back. A Single
   Catalog Listing change additionally requires applicable Catalog
   Administration Profiles to have been created or validated outside this
   excluded task scope. Do not invent or execute CAP setup here.
5. Resolve access, Category subtype, visibility, current Category state, Topic
   references, people, and applicable DFF or asset metadata through documented
   read-only routes. After the Category/Topic Site value is Y, validate the
   intended role's related privileges and HCM data-role access.
6. Resolve advanced membership and child-write capabilities. Block only the
   rows whose registered route, payload, privilege, or runtime contract is not
   proven.
7. Validate Active-on-create behavior, featured-date ordering, duplicate and
   wrong-subtype relationships, and the post-operation one-manager minimum.
8. Produce an immutable versioned preview with exact environment, identities,
   applicable option decisions or changes, generated/defaulted values,
   relationship effects, asynchronous behavior, and fingerprint. Obtain
   approval bound to that preview.
9. Immediately reread state before mutation. Invalidate stale approval, then
   execute each approved parent create or update once through
   `core.data-loader` before its eligible children. Use only a Route Summary
   exception for an unsupported child operation; never automatically retry an
   uncertain load or write.
10. Follow returned item links and read back the persisted Category and every
   attempted child result without rolling back unrelated successes.

## CSV and Data Loader Boundary

The effective catalog does not advertise native CSV export/import. A multi-row
input is intake for independently validated Data Loader records and is not
native task-level CSV support. The raw Describe does not prove registration.
Use `core.data-loader` for exact registration, template, component, and
operation discovery; missing or ambiguous registration blocks mutation while
read-only REST planning may continue.

## Acceptance Traceability

| FDD Test | Covered Scenario |
|---|---|
| CAT-AT-01 | Missing create title returns a correction and performs no write |
| CAT-AT-02 | Approved Active creation validates summary generation, visibility, featured dates, branding, and readback |
| CAT-AT-03 | ID, number, and subtype-filtered title resolution blocks ambiguous, inaccessible, or wrong-subtype targets |
| CAT-AT-04 | Topic add, feature, and removal validate identity, duplicate state, dates, scope, route readiness, and readback |
| CAT-AT-05 | Manager/member operations validate supported selection methods, privileges, criteria behavior, row results, and one-manager minimum |
| CAT-AT-06 | Direct learning, skills, contributions, conversations, Draft, lifecycle, and deletion are rejected or redirected |
| CAT-AT-07 | Mixed parent and Topic rows retain stable IDs and independent validation, approval, execution, and reconciliation |
| CAT-AT-08 | Changed Category, manager set, or Topic relationship invalidates affected approval and requires a refreshed proposal |

## Approval, Retry, and Diagnostics

Approval binds the exact target environment, Category identity or create key,
operation, selected parent and child rows, every proposed profile-option
change, generated/defaulted values,
relationship effects, asynchronous behavior, and preview fingerprint. Refresh
cache-managed authentication once for a 401 or 403. Never automatically retry
POST, PATCH, association, asset, membership, or group writes. Return the
failure class, affected stable row, current rule, sanitized evidence, verified
side effects, and one safe next action without exposing credentials, opaque
identifiers, or full response bodies.

## Preflight and Failure Handling

Preflight requires target identity; all applicable profile-option reads,
conditional CAP readiness, approved changes, and readbacks; manual Redwood and
HCM Filtered Lists readiness where applicable; privileges and HCM data-role
access; subtype isolation; current-state evidence; registered route and payload
capability; an exact preview; and fresh approval. Error handling classifies
input, metadata, authorization, transport, Fusion API, timeout, process,
persistence, and approval failures. Report unproven Category-to-Topic, group,
or other child write capabilities as precise operation-scoped blockers. Redact
credentials, tokens, secrets, opaque identifiers, unnecessary personal data,
and full response bodies from diagnostics and durable artifacts.

## Controlled Reentrancy

This enriched manifest must not be replaced by an unreviewed generator rerun.
Future taxonomy regeneration must preserve the authored body, version, hybrid
execution contract, resources, and canonical task identity, with contract
tests serving as the regression guard.

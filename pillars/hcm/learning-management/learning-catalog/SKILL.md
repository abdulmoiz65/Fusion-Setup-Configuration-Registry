---
skill_id: "hcm.learning-management.learning-catalog"
name: "Learning Catalog Implementation Guidance"
description: "Orchestrates approval-gated Learning Catalog setup for self-paced learning, events, courses, learning paths, official communities, categories, topics, and catalog administration profiles."
layer: "pillar"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Catalog"
functional_area_code: "ORA_LEARNING_CATALOG"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "HCM learning management pillar team"
version: "1.2.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "learning_catalog_scope"
  - "learning_catalog_requirements"
  - "requested_operation"
  - "target_environment"
  - "current_state_evidence"
  - "execution_intent"
  - "approval"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "dependency_readiness"
  - "change_preview"
  - "execution_authorization"
  - "execution_result"
  - "post_action_verification"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
  - "core.fusion-api.apps-common.profile-options"
  - "core.fusion-api.apps-common.lookups"
  - "core.fusion-api.apps-common.value-sets"
  - "core.fusion-api.apps-common.descriptive-flexfields"
  - "hcm.hcm-security.hcm-security-profile"
  - "hcm.hcm-security.hcm-data-role"
  - "hcm.hcm-tool.questionnaire"
  - "core.fusion-ai.workflow-agent-invoker"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
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
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-catalog/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-catalog/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-catalog/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "CUSTOM_SELF_PACED_LEARNING"
  - "CUSTOM_EVENTS"
  - "CUSTOM_COURSES"
  - "CUSTOM_LEARNING_PATHS"
  - "CUSTOM_OFFICIAL_COMMUNITIES"
  - "CUSTOM_CATEGORIES"
  - "CUSTOM_TOPICS"
  - "CUSTOM_MANAGE_CATALOG_ADMINISTRATION_PROFILES"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "After task validation, an immutable preview, and fresh explicit approval, a child skill may submit one supported Learning Catalog mutation to the exact target environment."
required_privileges:
  - "Authenticated access to the selected Data Loader BC REST business object through core.data-loader"
  - "Read-only access to the applicable Learning Catalog REST resources for Describe, preflight, and verification"
  - "Write access to an explicitly documented Direct REST exception when the selected task and operation require one"
  - "Product privileges required for the selected Learning Catalog operation"
---

# Learning Catalog Implementation Guidance

## Purpose

Orchestrates the current-release Learning Catalog setup scope under Learning
Management. It routes each request to one task-local skill and never treats a
functional-area plan, prior approval, or batch approval as authorization for a
Fusion mutation.

## When to Use

Use for Learning Catalog setup requests involving the eight tasks below, including
CAP identification, listing, proposals, creation, and supported basic updates.
Route by the primary object: a course that references a CAP stays with Courses;
a request to change that profile belongs to CAP. Learner enrollment and security
role grants are not CAP operations; return to the implementation router for them.

## Setup Tasks

1. [Manage Self-Paced Learning](self-paced-learning/SKILL.md)
   (`CUSTOM_SELF_PACED_LEARNING`, `learningSelfPacedItems`)
2. [Manage Events](events/SKILL.md)
   (`CUSTOM_EVENTS`, `learningEvents`)
3. [Manage Courses](courses/SKILL.md)
   (`CUSTOM_COURSES`, `learningCourses`)
4. [Manage Learning Paths](learning-paths/SKILL.md)
   (`CUSTOM_LEARNING_PATHS`, `learningPaths`)
5. [Manage Official Communities](official-communities/SKILL.md)
   (`CUSTOM_OFFICIAL_COMMUNITIES`, `learningCommunities`)
6. [Manage Categories](categories/SKILL.md)
   (`CUSTOM_CATEGORIES`, `learningCommunities`)
7. [Manage Topics](topics/SKILL.md)
   (`CUSTOM_TOPICS`, `learningCommunities`)
8. [Manage Catalog Administration Profiles](manage-catalog-administration-profiles/SKILL.md)
   (`CUSTOM_MANAGE_CATALOG_ADMINISTRATION_PROFILES`, `learningCatalogProfiles`)

These are the executable Learning Catalog task routes in this package.
The current taxonomy uses `Manage ...` names for the first seven tasks and
CAP. The child folders and stable task codes retain their existing identities.

## Data Loader BC REST Route Policy

The approved taxonomy and each child manifest select **Data Loader BC REST**.
`dataloader_import_mode: REST` and `businessObject` identify the registered
Data Loader business object; they do not authorize a caller to bypass
`core.data-loader` and invoke the similarly named Fusion REST collection.

- Route supported create and update mutations through `core.data-loader`.
- Before preparing a mutation, require one exact live Data Loader registration,
  its current template and component attributes, and operation support for the
  selected business object. A raw REST Describe is not registration evidence.
- Use Direct REST for Describe, duplicate/current-state reads, dependency
  lookups, and post-load readback.
- A Direct REST mutation is allowed only when the child skill names that exact
  operation as an exception and live Data Loader metadata proves the operation
  is unavailable. Never fall back automatically.
- If neither a supported Data Loader operation nor a documented exception is
  available, return an operation-scoped blocker without constructing or
  submitting a substitute request.

The route labels are:

| Task | Data Loader Business Object |
|---|---|
| Self-Paced Learning | learningSelfPacedItems |
| Events | learningEvents |
| Courses | learningCourses |
| Learning Paths | learningPaths |
| Official Communities | learningCommunities |
| Categories | learningCommunities |
| Topics | learningCommunities |

## Source Authority

Use these sources in order:

1. The approved Learning taxonomy and Learning guide-skill baseline. The
   effective taxonomy identifies this functional area as
   `ORA_LEARNING_CATALOG`.
2. OLC-116681 FDD, version 7, page `21981496001`, updated and reviewed
   2026-09-22 15:54:32. The in-scope detailed sections are OLC-120241 through
   OLC-120247 and acceptance scenarios `SPL-AT-01..09`, `EVT-AT-01..08`,
   `CRS-AT-01..08`, `LPT-AT-01..08`, `OCM-AT-01..08`, `CAT-AT-01..08`,
   and `TOP-AT-01..08`.
3. OLC-116676 and the CAP child skill's
   [FDD traceability](manage-catalog-administration-profiles/references/fdd-traceability.md)
   and [operation evidence](manage-catalog-administration-profiles/references/operation-contract-evidence.md).
   Neither source grants support for an operation the selected child blocks.
4. Current Oracle Fusion Cloud HCM REST documentation for publicly documented
   Self-Paced Learning and Events contracts.
5. Developer-supplied raw, target-specific Oracle Describe payloads reviewed
   2026-09-21: Self-Paced Learning has 20 resource nodes, 410 attributes, 77
   LOV-decorated attributes, and 300 queryable attributes; Events has 21 nodes,
   365 attributes, 56 LOV-decorated attributes, and 283 queryable attributes;
   Courses has 15 nodes, 307 attributes, 46 LOV-decorated attributes, and 252
   queryable attributes; Learning Paths has 16 nodes, 292 attributes, 41
   LOV-decorated attributes, and 239 queryable attributes; the shared
   `learningCommunities` resource has 22 nodes, 420 attributes, 36
   LOV-decorated attributes, and 359 queryable attributes.
6. Developer-supplied raw validation-resource Describe payloads reviewed
   2026-09-21: `hcmLists` has 1 node, 16 attributes, and 15 queryable
   attributes; `learningTrainingSuppliers` has 3 nodes, 64 attributes, 3
   LOV-decorated attributes, and 49 queryable attributes;
   `learningInstructors` has 5 nodes, 96 attributes, 9 LOV-decorated
   attributes, and 80 queryable attributes; `learningClassrooms` has 5 nodes,
   142 attributes, 4 LOV-decorated attributes, and 99 queryable attributes.
7. Current target-environment Data Loader registration, live LOVs, DFF
   metadata, privileges, and current-state evidence.

When sources conflict, stop and record the conflict. A taxonomy resource name
does not prove Data Loader registration. Describe evidence establishes the
wire contract only for its identified preproduction target; it does not make
target-specific Courses or Learning Paths behavior publicly portable. No
payload advertises ETag or `If-Match`, so do not claim atomic concurrency.

## Routing and FDD v7 Behavior

The OLC-116681 evidence and catalog-item/community inventories above apply to
the first seven tasks, not CAP. CAP uses its separately cited source contract.

Route by the requested primary object. A request spanning tasks produces one
task-local plan per object; the parent does not encode cross-task mutation
order. Each child loads its compiled `ora-resource/ora_rule_registry.json`
before evaluating readiness.

- Self-Paced Learning covers required-input failure, supported URL and binary
  creation, row-scoped invalid-content or processing failures, private publish
  with catalog-administration-profile and audience checks, content replacement,
  lifecycle and deletion safety, mixed-row batches, stale approval, and
  no-input demonstration generation capped at ten records.
- Events covers missing identity, valid single- or multi-activity creation and
  activation, schedule/resource/capacity errors, enrolled-event rescheduling,
  lifecycle requests, duplicate-to-Draft, mixed-row CSV, and stale resource or
  event state. Finalize and parent deletion remain unsupported by the REST
  contract even when the FDD asks the skill to assess them.
- Courses covers missing identity, Draft creation, child eligibility,
  activation readiness, assignment-safe default or child updates, copy and
  retirement, mixed-row upload, and stale relationship evidence. Parent and
  activity deletion remain unsupported.
- Learning Paths covers required identity and structure, valid multi-section
  paths, membership and cycle errors, activation readiness, assignment-safe
  structural updates, renewal and validity, grouped-graph batches, and stale
  path or child state. Copy remains unsupported.
- Official Communities covers Active creation, retrieval and update, catalog
  learning, membership and groups, assignment profiles, contributions,
  skills and qualifications, moderation, media, related materials, DFFs, and
  translations. Tenant summary rules and every capability are runtime gates.
- Categories covers Active creation, retrieval and update, Topic
  relationships and relationship featured dates, membership and groups,
  branding, DFFs, and supported child data. Direct learning, skills,
  contributions, and self-service conversations remain outside this task.
- Topics covers Active creation, retrieval and update, Category and catalog
  learning relationships, membership and groups, contributions, skills and
  qualifications, moderation, media, related materials, and DFFs. A Topic may
  remain standalone; self-reference and relationship cycles are blocked.
- Catalog Administration Profiles covers proposals, exact lookup, listing,
  evidence-gated root creation, and sparse name/description/visibility updates.
  Use its declared shared GET, Data Loader, or shared REST update workflow;
  the parent does not substitute a generic client. Contributor mutations,
  status/lifecycle writes, defaults, certificates, and explicit reconciliation
  remain blocked by the child contract.

## Dependency Readiness

- Resolve field-specific lifecycle values through the exact live LOV routes
  exposed by Describe; never invent enabled values.
- Resolve an HCM list read-only through `hcmLists` by `ListId` or `findByWord`
  with `Subscriber` and `ObjectName`. Require exactly one active result with a
  compatible returned scope. This proves identity and active state only; it
  does not authorize a Learning Catalog association write.
- Resolve Event course, supplier, instructor, classroom, and provider-account
  references through their exact target finders. Use schedule-aware
  availability and capacity evidence. Ad hoc resources and an opaque or
  indeterminate `validateProviderUser` result block only requests that need
  them; they are not blanket Event readiness failures.
- Resolve Course default instructors and type-routed facilitators through
  `learningInstructors`, `learningTrainingSuppliers`, and live
  `ORA_WLF_FACILITATOR_TYPE` values. New-child eligibility and
  course-versus-path exclusivity block only requests that add or change those
  relationships.
- Learning Path new-activity eligibility blocks only requests that add or
  replace activities. Existing membership and read-only operations continue
  when their own evidence is complete.
- Self-Paced owner/coordinator and language-label resolution are request-scoped
  gates when the caller supplies labels rather than accepted technical values.
- The raw payloads confirm `WLF_LEARNING_ITEM` for the seven catalog-item and
  community task routes and
  `WLF_LI_SPECIALIZATION` for Learning Paths. Exact target DFF segments and
  values still require live metadata.
- Before proposal or execution, use the Application Profile Option Foundation
  dependency to read current effective values. Show and propose only profile
  options whose FDD trigger applies and whose current value needs a user
  decision or change; record already-correct values as satisfied and omit them
  from the user dialog. Include every proposed profile change in the exact
  approval payload and read it back after execution.
- When an object is managed through the unified Redwood catalog listing or
  Catalog Administration Profile (CAP)-based administration,
  `ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD` is a conditional gate. The
  applicable CAP must already exist and validate through its separately scoped
  owner before this package can propose Site=`Y`; afterward, verify access with
  the intended object or catalog administrator. A non-CAP catalog request does
  not implicitly create or modify the profile; route an explicit CAP operation
  to the integrated CAP child.
- For Official Communities in scope, runtime-discover
  `ORA_WLF_COMMUNITIES_REDWOOD_ENABLED`; do not hard-code or propose it when
  the target does not expose the control, and verify both the effective value
  and community-management surface when it is present. For Categories and
  Topics, require Site=`Y` for `ORA_WLF_CATG_TOP_REDWOOD_ENABLED`, then verify
  the applicable privilege and HCM data-role access for the intended role.
- When catalog search behavior is explicitly designed or tuned,
  `ORA_WLF_SS_CATALOG_SEARCH_MODE` is a conditional gate. Ask whether broader
  recall, balanced matching, or tighter precision is intended, preserve the
  current value unless a change is explicitly approved, and test
  representative searches after an approved change.
- Also require the applicable manage privilege and manager-scoped or all-items
  access for the selected object.
- Resolve the exact `learningItemSubType`, status, visibility, and tenant DFF
  values before preview. The shared endpoint's generic "Learning Topics"
  labels and `ORA_COMMUNITY` item-type default do not prove a task subtype.
- Visual Builder/Redwood availability and HCM Filtered Lists are manual
  provider gates. Do not invent dependency skill IDs for them. HCM Data Role
  readiness is represented by `hcm.hcm-security.hcm-data-role`.
- The supplied Describe confirms catalog-item, user-access, membership-
  criteria, asset, content, DFF, forum, rating, related-material, translation,
  summary, rich-media, and where-used surfaces. Assignment, skills and
  qualifications, every group action, rating deletion, and Category-Topic
  writes require a current registered capability; block only the affected
  operation when no supported route is available.

## Execution Contract

CAP delegates operation readiness and execution to its child workflow. Read/list
readiness never grants write readiness. Parent dependencies are request-scoped:
do not add HCM lists, questionnaires, or the other tasks' object prerequisites
to CAP. Its declared business-skill dependencies remain empty, while its shared
technical prerequisites still apply. A CAP association in another task does
not authorize creating or modifying the profile itself.

For CAP Data Loader operations, use core.data-loader's authoritative exact-load
approval once, including the child's supported aggregate approval bound to every
member. This is not blanket parent-level batch approval. For its non-import
REST updates, obtain fresh exact-payload approval at the child's declared step.
Do not impose another parent approval on an already approved loader task action.
The numbered mutation sequence below retains the other seven tasks' contract;
CAP follows its linked child contract and reports loader completion separately
from CAP processing and independent readback.

1. Normalize the requested task, operation, exact target environment, and
   request row or grouped object.
2. Route to exactly one child and evaluate its compiled task graph.
3. Resolve the exact Data Loader business-object registration, current
   template, component attributes, supported operations, identity, current
   state, request-scoped dependencies, privileges, and target capability with
   read-only operations.
4. Produce a sanitized preview and fingerprint covering the environment,
   identity, operation, business effect, and immutable request or artifact.
5. Obtain fresh explicit approval bound to that fingerprint. In a multi-row
   request, approval and execution readiness remain row- or group-scoped.
6. Submit each approved supported create or update once through
   `core.data-loader`. Use a child-declared Direct REST mutation exception only
   after its operation-specific Data Loader support check fails closed and the
   exception has its own exact preview and approval. Never automatically retry
   POST, PATCH, DELETE, import, upload, or action calls.
7. Poll only documented asynchronous work within the child timeout policy.
8. Read back and reconcile each result with its approved preview.

An unresolved required value, ambiguous identity, stale preview, changed
artifact, failed dependency, or unavailable registration returns a bounded
`MISSING` or `FAILED` result without mutating the affected request. One invalid
row never authorizes dropping, rewriting, or silently executing another row.

## Deferred Scope

- Manage Access Groups remains outside the current release.
- Catalog Administration Profiles is now routed to its integrated nested child;
  its unsupported operations remain deferred, not enabled by this integration.
- The optional Learning Catalog Assistant
  (`ORA_HCM_LEARNING_CATALOG_MANAGEMENT_ASSISTANT`) remains non-executable until
  its provider contract and configuration readiness are confirmed.

## Controlled Reentrancy

Do not run the current `pillar-skill-gen` reentrantly over this enriched
package as an ordinary refresh. Version 0.2.0 identifies tasks by current
catalog code, does not migrate task-local resources, and replaces enriched
frontmatter with generic planning metadata.

For a later task addition or taxonomy rename:

1. Run the generator in dry-run mode and review every proposed path.
2. Refuse duplicate semantic tasks, legacy identifiers, or an unreviewed
   parent-frontmatter replacement.
3. Generate only the missing canonical scaffold in an isolated or explicitly
   controlled change.
4. Preserve this orchestration contract and all existing task-local resources;
   author and compile source-grounded resources for the new task separately.
5. Re-run manifest, resource, contract, auditor, and stale-identity checks
   before merging.

## Diagnostics and Recovery

Preflight checks confirm the environment, task, operation, identity,
privilege, current state, request-scoped dependencies, target capability,
registry readiness, preview fingerprint, and approval before a side effect.

Classify failures as input validation, catalog or metadata mismatch,
authentication, authorization, transport or environment, Fusion API, process
timeout, process failed, artifact persistence, or approval blocker. Refresh a
cache-managed token once for a 401 or 403; do not replace an explicit token.
Never replay an uncertain write. Reconcile first with a safe read, redact
credentials and payload bodies, and persist durable diagnostics only inside
the selected project workspace.

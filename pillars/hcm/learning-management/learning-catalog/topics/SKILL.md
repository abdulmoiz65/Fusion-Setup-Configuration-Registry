---
skill_id: "hcm.learning-management.learning-catalog.topics"
name: "Topics Setup Task Guidance"
description: "Provides approval-gated creation, maintenance, relationship, membership, contribution, moderation, and reconciliation guidance for Learning Catalog topics."
layer: "pillar"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Catalog"
functional_area_code: "ORA_LEARNING_CATALOG"
task_code: "CUSTOM_TOPICS"
task_name: "Manage Topics"
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
  - "topic_definition"
  - "category_and_learning_relationship_plan"
  - "membership_and_contribution_plan"
  - "skills_and_qualifications_plan"
  - "rating_moderation_plan"
  - "media_and_related_materials"
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
  - "core.fusion-api.apps-common.profile-options"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.fusion-api.apps-common.lookups"
  - "core.fusion-api.apps-common.value-sets"
  - "core.fusion-api.apps-common.descriptive-flexfields"
  - "hcm.hcm-security.hcm-security-profile"
  - "hcm.hcm-security.hcm-data-role"
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
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-catalog/topics/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-catalog/topics/current/"
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
  - "After live registration validation, an exact preview, request-scoped dependency resolution, current-state recheck, and fresh explicit approval, may create or update a Topic through core.data-loader."
  - "After the same gates and unavailable Data Loader operation evidence, may submit a listed Direct REST exception for supported child relationship operations."
  - "When a v7 profile-option trigger applies, may route an exact separately approved option change through the Application Profile Option Foundation capability and require readback before Topic execution."
required_privileges:
  - "Authenticated Data Loader access to the registered learningCommunities business object and supported components"
  - "Read-only access to learningCommunities and applicable write access for a listed Direct REST exception"
  - "Learning administrator manage access and manager-scoped or all-items access required by the selected operation"
  - "Operation-specific contribution or rating moderation privilege when requested"
  - "Profile-option administration privilege when an applicable dependency value change is explicitly approved"
---

# Topics Setup Task Guidance

## Purpose

Use this skill to plan, validate, preview, execute, and verify Learning Topic
changes described by OLC-120247 in OLC-116681 FDD v7, page 21981496001,
updated 2026-09-22 15:54:32. A Topic may remain standalone. This skill never
invents a Category relationship, catalog item, subtype, lifecycle action, or
unavailable write route.

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Topics` under `Learning Catalog`.

## Route Summary

- Canonical parent create and update route: `core.data-loader` with business
  object `learningCommunities` and the exact Topic subtype.
- Resolve one exact live registration, its current template and component
  attributes, supported operation, and subtype before preparing a mutation.
- Use Direct REST for Describe, subtype/identity/current-state reads,
  relationship and dependency lookups, and post-load verification.
- Category, learning, membership, contribution, skills, moderation, media, and
  related-material mutations are Direct REST exceptions only when live Data
  Loader metadata does not expose that exact operation and a current returned
  REST link confirms it. Never fall back automatically.
- Block any mutation without a supported loader operation or a listed,
  target-confirmed exception.

## Supported Scope

- Create an Active Topic from a user-provided title; retrieve or update an
  existing Topic by ID, number, or uniquely resolved title.
- Propose an optional summary generated only from the user-supplied title when
  Generate is enabled and the user permits it. Keep generated text editable
  and visibly generated.
- Maintain target-supported visibility, featured dates, branding, trailer,
  conversation settings, related materials, DFF values, and other confirmed
  child information.
- Maintain Category relationships only through the target-confirmed
  Category/Topic relationship capability. A Topic can remain standalone.
- Add or remove supported self-paced learning, standalone events, courses, and
  learning paths, including association-level featured dates.
- Maintain supported membership, manager safety, pending requests, member
  types, criteria or groups, reconciliation, and member contributions.
- Maintain post-create skills and qualifications and perform rating or comment
  moderation only when the applicable capability and privilege are confirmed.
- Process interactive and multi-row requests with stable parent and child row
  identifiers, dependency ordering, independent outcomes, and exact readback.

Draft creation, deactivate, reactivate, and Topic deletion are outside the
current 26C story. Block them with a scoped next step even though the generic
REST root advertises DELETE. Never add a Category as catalog learning, a Topic
as its own child, a duplicate relationship, or a cyclic parent-child graph.

## Source and Route Contract

The approved taxonomy and Learning baseline map Topics to the confirmed BC
REST root `/learningCommunities` and the Product UI route
`redwood/learning-catalog/main/manage-catalog-organization`. The generator
business-object value is `learningCommunities`; its presence does not prove
Data Loader registration in the selected environment.

The user-supplied target Describe identifies `learningCommunities` as a
BusinessObject with 22 resource nodes, 420 attributes, 36 LOV-decorated
attributes, and 359 queryable attributes. It confirms collection GET/POST,
item GET/PATCH/DELETE,
`learningItemType` default `ORA_COMMUNITY`, a runtime-LOV
`learningItemSubType`, status and visibility fields, featured dates,
`allowMemberUploads`, and child surfaces for catalog items, user access,
membership criteria, media, DFFs, forums, ratings, related materials,
translations, summary, rich media, and where-used evidence. Its generic
"Learning Topics" labels do not establish the Topic subtype. Resolve the
exact subtype and all lookup-backed values from the current target.

The Describe supplies no ETag or `If-Match` contract. A normalized
current-state fingerprint detects stale evidence for approval purposes but is
not atomic concurrency control.

The Describe does not prove write routes for Category relationships, skills
and qualifications, every membership-group operation, or rating deletion.
Those operations are request-scoped runtime dependencies: use a current
registered capability when available and otherwise block only the affected
operation. Do not construct a substitute request from a similarly named child
or from UI behavior.

## Related Setup and Profile Options

Use `core.fusion-api.apps-common.profile-options`, the Application Profile
Option Foundation capability, to read the current effective value and scope of
every applicable option before proposal or execution.

- `ORA_WLF_CATG_TOP_REDWOOD_ENABLED` applies to every executable Topic
  request. Require the Site value `Y`; after it is confirmed or changed,
  validate the intended role's Category/Topic privileges and HCM data-role
  access.
- `ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD` applies only when the unified
  Redwood catalog listing or CAP-based administration is used. For that
  trigger, require the applicable Catalog Administration Profiles to have been
  created or validated by their separate, excluded task scope before using or
  setting the Site value `Y`. This skill blocks on missing CAP evidence and
  never creates CAPs or invents a CAP dependency skill ID.
- `ORA_WLF_SS_CATALOG_SEARCH_MODE` applies only when Topic catalog-search
  behavior is being designed or tuned. Ask whether the user wants broader
  recall, balanced matching, or tighter precision; preserve the current value
  unless an exact change is approved, and test representative searches after
  the change.

Record an already-correct applicable option as a satisfied dependency and omit
it from the user dialog. Include every proposed option change, its Site scope,
trigger, prerequisite evidence, and current and proposed values in the exact
approval payload; route only the approved change through the foundation
capability and read it back before continuing.

## Read Order

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_dependency_readiness.md`
3. `ora-resource/ora_reference_lookups.md`
4. `ora-resource/ora_defaulting_rules.md`
5. `ora-resource/ora_design_enforcement.md`
6. `ora-resource/ora_error_handling.md`
7. `ora-resource/ora_rule_registry.json`

## Workflow

1. Normalize the requested operation, exact target environment, one or many
   Topic rows, stable child rows, requested parent and child changes, and
   whether unified catalog listing/CAP administration or search design makes a
   conditional profile option relevant.
2. Validate shape and minimum identity. Create requires a nonblank,
   user-provided title; an existing action requires an ID, number, or title.
3. Use the Application Profile Option Foundation capability to read current
   effective values before proposal or execution. Always evaluate
   `ORA_WLF_CATG_TOP_REDWOOD_ENABLED`; evaluate
   `ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD` and
   `ORA_WLF_SS_CATALOG_SEARCH_MODE` only when their documented triggers apply.
4. Record already-correct applicable options as satisfied and omit them from
   the user dialog. Put every proposed option change in the exact approval
   payload and read it back. Block the triggered Single Catalog Listing
   dependency until the separate excluded scope has created or validated the
   applicable CAPs, even when the option value is already correct; never invent
   or execute CAP setup here.
5. Confirm manage privilege, manager scope or all-items scope, HCM data-role
   access, route support, Topic subtype, status, visibility, required DFFs, and
   operation-specific capabilities through read-only target evidence.
6. Resolve every Category, learning item, person, criteria source, skill,
   qualification, rating, asset, and related-material reference. Require one
   accessible result of the allowed subtype and retain its technical ID.
7. Validate featured dates, association dates, duplicates, manager count,
   contribution or moderation privilege, relationship ordering, and the full
   batch graph. Mark blocked child rows without silently dropping them.
8. Produce an immutable, versioned proposal containing exact IDs and codes,
   applicable profile-option decisions or changes, generated and defaulted
   values, warnings, effects, standalone behavior, parent-first ordering,
   included and excluded rows, and a current-state fingerprint.
9. Obtain fresh explicit approval for that exact proposal. Immediately reread
   the parent, manager set, and affected relationships; skip stale actions and
   require a refreshed proposal.
10. Submit each approved parent create or update once through
    `core.data-loader`. Create and read back the Active parent first, then use
    only a Route Summary exception for an unsupported eligible child operation
    in dependency order and read back every attempted parent and child result.
11. Preserve independent successes. Report partial configuration, asynchronous
    status, row-level failures, and safe next actions without automatically
    retrying a write or rolling back unrelated rows.

## CSV and Data Loader Boundary

The effective catalog does not advertise native CSV export/import. Multi-row
files are intake for individually validated Data Loader records and do not
create native task-level CSV support. Do not route task export to
`shared.setup-export.task-level-export`. Route registration discovery, sample
generation, source mapping, immutable artifact validation, approval, upload,
and initiation through `core.data-loader` for `learningCommunities`. Missing or
ambiguous registration blocks mutation while read-only REST planning may
continue.

## Batch Contract

- Assign stable IDs to every Topic row and each Category, Learning,
  membership, skill, media, or moderation child row.
- Classify rows as Valid, Blocked, Warning, or No-op/duplicate. A blocked child
  is corrected or explicitly excluded before a revised proposal is approved.
- Validate parent and child rows independently. An inaccessible Category can
  be excluded so an otherwise valid Topic remains standalone.
- Reject self-reference, duplicate edges, cycles, and references to failed
  parent rows before approval.
- Execute approved valid parents before their children. A child failure does
  not conceal or roll back unrelated parent or row successes.
- Return persisted Topic IDs and numbers plus per-child readback and process
  status. Never summarize a criteria or group row as proof that all people
  processed successfully.

## Acceptance Traceability

| FDD Test | Covered Scenario |
|---|---|
| TOP-AT-01 | Missing user-provided title stops before proposal or write |
| TOP-AT-02 | Approved Active creation covers summary, visibility, featured dates, media, DFFs, related materials, and readback |
| TOP-AT-03 | ID, number, unique title, ambiguous title, access, and subtype resolution |
| TOP-AT-04 | Category and learning association add, remove, and featured-date validation |
| TOP-AT-05 | Post-create skills, qualifications, membership, contributions, manager safety, and independent child results |
| TOP-AT-06 | Privilege-gated rating moderation and precise refusal of unsupported lifecycle actions |
| TOP-AT-07 | Mixed parent and child rows are revised, approved, dependency-ordered, and reconciled independently |
| TOP-AT-08 | Changed Topic, manager set, or relationship invalidates approval and skips the stale action |

## Approval, Retry, and Diagnostics

Approval is bound to the exact environment, operation, Topic create key or
persisted identity, selected rows, relationship effects, target-resolved codes,
immutable artifacts, and preview fingerprint. Changing any bound value
requires a new proposal and approval.

Refresh cache-managed authentication once for a 401 or 403. Never replace an
explicit token and never automatically retry POST, PATCH, DELETE, upload,
moderation, or group actions. After an uncertain outcome, reconcile through a
safe read before offering a new action. Return the failure class, affected row,
rule, sanitized evidence, verified side effects, and one safe next step without
exposing credentials, opaque identifiers, or full response bodies.

Redact credentials, bearer tokens, authorization headers, opaque identifiers,
and full request and response bodies from diagnostics and durable artifacts in
accordance with `governance/error-handling-guidelines.md`.

## Preflight and Failure Handling

Preflight confirms environment, operation, identity, all applicable
profile-option reads, conditional CAP readiness, approved option changes and
readbacks, privileges and HCM data-role access, scope, route support, subtype,
lookup-backed values, required DFFs, reference resolution, manager safety,
graph validity, current-state fingerprint, exact preview, and fresh approval
before any side effect.

Classify failures as input validation, metadata or capability mismatch,
authentication, authorization, transport or environment, Fusion API, upload,
process timeout, process failed, artifact persistence, stale state, or approval
blocker. Optional child failures remain separate from a successfully verified
parent. Unproven write contracts remain explicit runtime blockers, never
invented payloads or silently omitted steps.

## Controlled Reentrancy

This enriched manifest must not be replaced by an unreviewed generator rerun.
Future taxonomy regeneration must preserve this authored body, version, hybrid
execution contract, resources, canonical task identity, and FDD traceability.
Review proposed paths in dry-run mode and rerun manifest, resource, registry,
planner, and contract validation before merging any structural refresh.

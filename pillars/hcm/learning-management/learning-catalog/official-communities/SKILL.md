---
skill_id: "hcm.learning-management.learning-catalog.official-communities"
name: "Official Communities Setup Task Guidance"
description: "Plans, validates, previews, executes, and verifies approval-gated Official Community changes through Data Loader BC REST, with documented Direct REST exceptions."
layer: "pillar"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Catalog"
functional_area_code: "ORA_LEARNING_CATALOG"
task_code: "CUSTOM_OFFICIAL_COMMUNITIES"
task_name: "Manage Official Communities"
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
  - "official_community_definition"
  - "catalog_relationships"
  - "membership_and_group_plan"
  - "assignment_plan"
  - "multi_row_manifest"
  - "current_state_evidence"
  - "execution_intent"
  - "approval"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "dependency_readiness"
  - "change_preview"
  - "profile_option_results"
  - "row_and_child_results"
  - "execution_authorization"
  - "execution_result"
  - "post_action_verification"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-catalog/official-communities/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-catalog/official-communities/current/"
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
  - purpose: "Safe defaults"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Official Community policy and capability gates"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Approval, retry, and reconciliation gates"
    location: "ora-resource/ora_error_handling.md"
oracle_supplied_guidance_status: "Aligned to OLC-116681 FDD version 7 updated 2026-09-22 15:54:32, the approved Learning baseline and taxonomy, and the supplied learningCommunities Describe"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release; target metadata, privileges, profile values, and capabilities must be refreshed at runtime"
side_effects:
  - "After exact approval, may update an applicable supported profile-option value through the Application Profile Option Foundation route and read it back before the dependent Official Community operation."
  - "After live registration validation, a fresh immutable preview, and exact approval, may submit one supported Official Community parent create or update through core.data-loader."
  - "After parent readback, separate applicability checks, and unavailable Data Loader operation evidence, may submit a listed Direct REST exception for supported child operations."
  - "A multi-row request may submit only its independently approved valid rows once and returns row- and child-scoped results."
required_privileges:
  - "Authenticated Data Loader access to the registered learningCommunities business object and supported components"
  - "Authenticated read access to learningCommunities and applicable write access for a listed Direct REST exception"
  - "Official Community manager scope or the applicable all-items access for the selected operation"
  - "Operation-specific membership, required-learning assignment, contribution, and rating-moderation privileges when those operations are requested"
  - "FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV when an approved profile-option change is requested"
---

# Official Communities Setup Task Guidance

## Purpose

Use this canonical task skill to create, retrieve, and update Official
Communities and to manage only the catalog, membership, assignment, rating,
skills and qualifications, media, related-material, translation, and DFF
operations proven for the current target. It converts user intent into a
versioned proposal, preserves manager safety, obtains exact approval before
each mutation set, and reads back the parent and every attempted child.

## Route Summary

- Canonical parent create and update route: `core.data-loader` with business
  object `learningCommunities` and the exact Official Community subtype.
- Require one exact registration, current template and component attributes,
  supported operation, and subtype before preparing an immutable artifact.
- Use Direct REST for Describe, identity/current-state reads, relationship and
  dependency lookups, and post-load verification.
- Child and action mutations are Direct REST exceptions only when live Data
  Loader metadata does not expose the exact operation and the current returned
  REST link confirms it. Never fall back automatically.
- Block any mutation without a supported loader operation or a listed,
  capability-gated exception.

## Source Contract

The business rules come from OLC-116681 FDD version 7, section 5.0 and Jira
story OLC-120245, reviewed from the page updated 2026-09-22 15:54:32. The
approved Learning baseline maps Official Communities to REST resource
`/learningCommunities` and Product UI route
`redwood/learning-catalog/main/manage-communities`. The approved taxonomy maps
Official Communities to Learning Catalog (`ORA_LEARNING_CATALOG`) with sequence
31.

The wire evidence is the user-supplied `learningCommunities` Describe. It has
22 resource nodes, 420 attributes, 36 LOV-decorated attributes, and 359
queryable attributes. It confirms parent collection GET and POST, item GET and
PATCH, exact ID and number finders, word and manage-scope finders, and returned
child links. Although generic Describe metadata also exposes collection upsert
and item DELETE, the FDD excludes user-facing upsert, Draft, deactivate,
reactivate, and delete-object behavior from this story. The Describe's generic
Learning Topics labels do not establish Official Community subtype values.

Always filter and verify the target subtype before treating a returned item as
an Official Community. Follow the item and child links returned by Fusion;
never construct an opaque item hash. No supplied source confirms ETag or
If-Match, so freshness uses immediate reads, normalized fingerprints, one
submission, and post-write readback rather than an atomic-concurrency claim.
Do not persist the source environment hostname or treat its enabled values as
portable between pods.

## Supported Operations

| Operation | Contract Status | Required Safeguard |
|---|---|---|
| List, search, or retrieve | Confirmed parent GET and finders | Apply manager or all-items view scope, require subtype isolation, and follow returned links |
| Create Active Official Community | Data Loader BC REST for learningCommunities; exact subtype and runtime-required fields remain target-resolved | Require exact registration, user title, summary rule, target values, immutable artifact, approval, and parent readback |
| Update parent | Data Loader BC REST for learningCommunities | Resolve one exact Official Community, verify update support, and compare a fresh current-state fingerprint |
| Profile-option readiness or change | Application Profile Option Foundation route | Read only applicable effective values before proposal; omit satisfied options from the dialog; include each proposed change in exact approval and read it back before dependent community work |
| Catalog learning relationships | Data Loader component when registered; otherwise the returned communityLearningCatalogItems link is a capability-gated exception | Resolve supported active learning, prevent duplicates, preview association dates and impact, and verify each relationship |
| Assets, related materials, translations, conversations, and DFFs | Registered Data Loader component when supported; otherwise an applicable returned child link exception | Validate target schema, content rules, privileges, and parent identity; isolate child failures |
| Membership, groups, assignments, skills, qualifications, contributions, and moderation | FDD scope is confirmed but the supplied Describe does not prove every authoritative write route | Proceed only when the registered target exposes the exact operation contract; otherwise return a precise operation blocker |

## Read Order

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_dependency_readiness.md`
3. `ora-resource/ora_reference_lookups.md`
4. `ora-resource/ora_defaulting_rules.md`
5. `ora-resource/ora_design_enforcement.md`
6. `ora-resource/ora_error_handling.md`
7. `ora-resource/ora_rule_registry.json`

Before consuming the registry, load the repository Ora-Resource Task Node
Execution Guide and require a current successful planner result. A ready graph
means the authoring contract is complete; it does not mean every target
capability is available or authorize a Fusion write.

## Input Modes

- A guided request supplies one Official Community parent intent and any
  supported child-operation rows.
- A multi-row file or table has one stable parent row ID and stable child row
  IDs. Validate, resolve, preview, approve, submit, and reconcile each parent
  and child independently. A blocked optional child does not invalidate an
  otherwise valid parent unless the user made that child mandatory.
- One add-members transaction uses exactly one selection method: person, one
  supported CSV, worker-assignment filtered list, learning-assignment filtered
  list, analysis criteria, user group, hierarchy manager, or directs. Clear
  staged selection before changing methods.

## Workflow

1. Normalize the exact target environment, requested operation, parent row,
   child rows, membership selection method, and execution intent.
2. For create, require the title from the user. Resolve the Official Community
   subtype, tenant summary requirement, status, visibility, contribution
   capability, service-required fields, and target DFFs without deriving a
   title or code from a label.
3. Through `core.fusion-api.apps-common.profile-options`, read the current
   effective values of only the FDD-triggered profile options. Record an
   already-correct option as satisfied and omit it from the user dialog.
   Apply the conditional CAP, unified-listing, community-control, and search
   mode rules below before proposing a change. Also require applicable
   Learning administrator access, manager or all-items scope, and the exact
   operation-specific privileges. Treat Visual Builder/Redwood enablement and
   HCM Filtered Lists as manual readiness gates where no delivered provider
   skill exists.
4. For an existing item, resolve by exact ID or number. A title search is valid
   only when subtype-filtered results yield one accessible Official Community
   or the user selects one. Fingerprint parent fields, active manager count,
   selected relationships, last-modified evidence, and child state used by the
   proposal.
5. Resolve only applicable references. People accept technical ID, person
   number, exact work email, or a uniquely selected full name. Learning accepts
   ID, number, or uniquely selected title and only current supported catalog
   types. Resolve skills, qualifications, criteria sources, groups, assets,
   related materials, translations, DFFs, and lookup-backed values through
   their documented target authority.
6. Build an immutable, sanitized, versioned proposal. Show generated or
   defaulted values, applicable unsatisfied profile dependencies, every
   proposed profile-value change, creator-as-manager, final manager count,
   parent-first ordering, child dependencies, association dates,
   member/assignment impact, optional blocked children, per-row eligibility,
   and a proposal fingerprint.
7. Obtain fresh explicit approval for the exact environment, proposal version,
   selected parent and child rows, resolved identities, every proposed profile
   option name, level, old value and new value, business impact, and
   fingerprint. Any correction, exclusion, reorder, capability change, or
   target-state change invalidates approval.
8. Re-read applicable state immediately before mutation. For an approved
   profile change, use only the Application Profile Option Foundation route,
   submit it once, and read back both the configured and effective value before
   dependent community work. Submit each approved parent create or update once
   through `core.data-loader`; use only a Route Summary exception for an
   unsupported child or action operation. Create and read back the parent
   before attempting eligible child rows. Never automatically retry import,
   POST, PATCH, DELETE, upload, reconcile, assignment, group, moderation, or
   profile-value mutations when the outcome is uncertain.
9. For asynchronous reconcile, assignment, upload, or processing work, return
   the sanitized process identity, last status, elapsed time, and safe next
   check on timeout. Do not claim completion from request acceptance alone.
10. Read the parent and every attempted child again. Compare persisted state
    with the approved proposal and return verified, partial, blocked, failed,
    or indeterminate results for each row without hiding independent success.

## Related Setup and Profile Options

Before proposal or execution, use
`core.fusion-api.apps-common.profile-options`, the Application Profile Option
Foundation route, to read current effective values. Evaluate only each
option whose trigger applies. Record an already-correct value as a satisfied
dependency and omit it from the user dialog. Preserve current values unless a
change is needed and explicitly approved. Every proposed change belongs in the
same exact approval payload as its dependent Official Community operation and
must be read back before that operation proceeds.

| Profile Option | Applies When | Required Handling |
|---|---|---|
| ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD | Official Communities use the unified Redwood catalog listing or CAP-based administration | Require external evidence that the applicable Catalog Administration Profiles are created or validated first. CAP implementation is outside this skill. Only then may the proposal set the Site value to Y and verify access with an intended community or catalog administrator. |
| ORA_WLF_COMMUNITIES_REDWOOD_ENABLED | Official Community management is in scope and the current tenant/release exposes this control | Discover the control at runtime. When present, verify its current effective value and the community-management surface. When absent, do not hard-code it, propose a value, or manufacture a replacement; require evidence for the supported current-release control and surface. |
| ORA_WLF_SS_CATALOG_SEARCH_MODE | Official Community catalog search behavior is being designed or tuned | Ask whether search should favor broader recall, balanced matching, or tighter precision only when a decision or change is required. Preserve the current value unless a target-supported value change is explicitly approved, then test representative searches. |

Do not create, validate, or modify Catalog Administration Profiles from this
skill and do not invent a CAP provider skill ID. When the unified-listing
trigger applies and CAP evidence is absent, return the exact external
prerequisite as a runtime blocker. HCM Filtered Lists remains a separate manual
readiness gate for applicable membership selection methods.

## Membership and Relationship Safety

- The creator is automatically proposed and verified as the initial manager.
  No individual or bulk operation may leave fewer than one active manager.
- Required and voluntary membership types may be changed only for eligible
  active members. Preserve already-matching rows and disclose that required
  membership can drive community learning assignments.
- Closed-community pending requests may be approved or rejected only with the
  target capability and compatible pending state. Approval creates an active
  voluntary member; rejection removes the active/pending request.
- Criteria evaluation is Once or Continuous. Continuous withdrawal is allowed
  only for a supported criteria type and target contract. Preserve legacy
  multi-destination groups and never flatten them into a single destination.
- Group edit, remove, and reconcile require the FDD-defined runtime group
  capability. Group removal and reconcile must preview membership impact.
- Individual removal is a soft functional removal and administrator override.
  Preserve target retention/exclusion behavior so later reconciliation does
  not silently re-add the person when exclusion is required.
- Catalog learning is limited to selector-supported accessible self-paced
  learning, standalone events, courses, and learning paths. Removal deletes
  only the association, not the catalog item.
- Assign Learning requires learning already associated with the community and
  required members. Cancel requires reason, outcome status, impact preview,
  and confirmation.

## Data Loader Preparation

REST endpoint availability or the taxonomy mapping alone is not proof that
`learningCommunities` is registered. Route registration discovery, sample
generation, source mapping, immutable artifact preparation, validation,
approval, upload, and initiation through `core.data-loader`. Keep generated
workbooks together, validate the exact subtype and every supplied component,
and treat sample generation as read-only rather than approval to load.

## Preflight, Failure, and Redaction

Preflight every selected row immediately before submission. Reconfirm target
identity, subtype, applicable effective and configured profile-option values,
CAP evidence when required, privileges, exact operation capability, registered
route, parent and child links, DFF context, final manager count, current
fingerprint, preview selection, and approval. Read back every approved profile
change before dependent work. Stop only the affected row when a validation or
optional child dependency fails. Stop later submissions after an uncertain
mutation until safe reads reconcile it.

Never print or persist credentials, tokens, binary bodies, source environment
hostnames, opaque URLs, raw sensitive responses, membership CSV contents, or
unnecessary person data. Retain only sanitized identifiers, counts, statuses,
evidence references, and diagnostics needed for a safe next action.

## FDD Acceptance Traceability

| FDD Test | Covered Scenario |
|---|---|
| OCM-AT-01 | Missing create title stops before proposal or write and no title is generated |
| OCM-AT-02 | Runtime summary, visibility, dates, assets, DFFs, and related materials are proposed, approved, executed parent-first, and read back independently |
| OCM-AT-03 | ID and number resolve exactly; subtype-filtered title ambiguity, inaccessibility, and wrong subtype block until corrected or selected |
| OCM-AT-04 | Supported catalog learning and association dates validate; duplicate or invalid rows block; removal affects only the community association |
| OCM-AT-05 | Person, CSV, criteria, request, type-change, removal, and group flows enforce one selection method, privileges, manager safety, impact approval, and capability gates |
| OCM-AT-06 | Assignment and moderation operations enforce state, privilege, impact, no-retry, processing, and readback rules |
| OCM-AT-07 | Mixed parent and child rows retain stable IDs, revised selection, dependency order, and independent reconciliation |
| OCM-AT-08 | A changed parent, manager set, or child relationship invalidates approval and requires a refreshed proposal |

## Execution and Refusal Rules

- Data Loader BC REST through `core.data-loader` is the canonical parent
  mutation route. Catalog CSV flags are `N`; user-supplied spreadsheets are
  intake, not native task-level CSV export/import support.
- Do not use a Direct REST mutation as a fallback. It must be a listed child or
  action exception with live unsupported-operation evidence from Data Loader,
  a current returned route, an exact preview, and operation-specific approval.
- Do not infer an Official Community subtype from the resource name or generic
  Learning Topics labels. Do not infer lookup codes from translated meanings.
- Do not offer generic upsert, Draft, deactivate, reactivate, or delete-object
  operations in this release, even though generic Describe metadata exposes an
  upsert header and DELETE method.
- Do not implement CAP setup, invent a CAP skill dependency, or set
  `ORA_WLF_SINGLE_CATALOG_LISTING_REDWOOD` to Y before applicable CAP readiness
  and intended-administrator access are evidenced.
- Do not hard-code or propose `ORA_WLF_COMMUNITIES_REDWOOD_ENABLED` when the
  current tenant and release do not expose it. Do not change
  `ORA_WLF_SS_CATALOG_SEARCH_MODE` without an applicable search-design trigger,
  a target-supported value, and exact approval.
- Do not show already-satisfied profile options as user decisions. Do not
  execute a profile-value change omitted from the exact approved proposal or
  continue dependent work until the configured and effective value readback
  agrees.
- Do not execute a membership, group, assignment, skills/qualifications,
  contribution, or moderation write when the registered target lacks its exact
  authoritative operation contract. Return the missing capability and preserve
  unaffected rows.
- Do not remove the last active manager, mix membership selection methods in
  one add flow, flatten legacy group destinations, assign learning absent from
  the community catalog, or treat contributions as manager access.
- Do not call a child operation before parent readback, and do not roll back or
  hide an independently successful parent because an optional child failed.
- Do not treat HTTP success, a process ID, or a registry entry as persisted
  success. Report success only after the required readback agrees.

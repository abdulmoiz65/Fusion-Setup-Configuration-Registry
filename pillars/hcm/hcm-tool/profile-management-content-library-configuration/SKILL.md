---
skill_id: "hcm.hcm-tool.profile-management-content-library-configuration"
name: "Profile Management Content Library Configuration Implementation Guidance"
description: "Captures supplied Oracle HCM Content Library configuration through direct values, a blank requirements template, or a readable file; preserves complete parent/child sets, exact duplicate checks, separately approved supported create-only FSM execution, and the explicitly selected verified GOAL HDL exception."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Profile Management Content Library Configuration"
functional_area_code: "CUSTOM_TALENT_PROFILE_CONTENT_LIBRARY"
type: "import"
execution_mode: "hybrid"
owner_team: "HCM hcm tool pillar team"
version: "0.15.10"
inputs:
  - "template_guidance_checklist_or_example_request"
  - "supplied_configuration_objects_and_values"
  - "confirmed_source_to_field_mappings"
  - "supplied_applicable_dates_and_optional_values"
  - "expert_task_scope_or_explicit_configuration_values"
  - "implementation_objective"
  - "project_context"
  - "configuration_values_or_source_file"
  - "target_environment_context_for_read_only_evidence"
  - "approved_create_only_proposal_and_fingerprint"
  - "approved_provider_rows_fingerprint"
  - "fresh_current_state_and_package_baseline_exports"
  - "canonical_configuration_set"
  - "target_environment_alias"
  - "sanitized_routed_proficiency_reference_evidence"
  - "retained_new_catalog_set_lifecycle_and_core_approval_evidence"
  - "new_catalog_set_target_classification_confirmation"
outputs:
  - "deterministic_blank_setup_intake_template"
  - "assumption_ledger"
  - "authenticated_environment_capability_result"
  - "xlsx_delivery_route_result"
  - "supplied_object_routing_result"
  - "non_executable_exact_check_report"
  - "normalized_input_with_provenance"
  - "source_backed_field_readiness_matrix"
  - "review_only_scope_proposal"
  - "complete_review_only_configuration_set_proposal"
  - "exact_match_evidence"
  - "fresh_customer_plus_seeded_catalog_resolution"
  - "registered_content_item_rest_evidence"
  - "fsm_evidence_envelope"
  - "task_local_exact_comparison"
  - "readback_comparison_result"
  - "immutable_proposal_fingerprint"
  - "provider_readiness_result"
  - "immutable_fsm_package"
  - "fsm_package_readiness_receipt"
  - "core_data_loader_handoff_result"
  - "canonical_configuration_set_contract"
  - "complete_immutable_creation_preview"
  - "fingerprint_bound_approval_record"
  - "submitted_pending_verification_record"
  - "complete_set_readback_result"
  - "proficiency_reference_validation_report"
  - "blocked_complete_preview"
  - "new_catalog_set_candidate_validation"
  - "controlled_new_catalog_set_package_preview_and_receipt"
  - "bound_new_catalog_set_lifecycle_verification_result"
  - "validation_result"
  - "traceability_record"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "hcm.hcm-tool.profile-management-content-library-configuration.content-types"
  - "hcm.hcm-tool.profile-management-content-library-configuration.content-items"
  - "hcm.hcm-tool.profile-management-content-library-configuration.item-catalogs"
  - "hcm.hcm-tool.profile-management-content-library-configuration.instance-qualifiers"
  - "hcm.hcm-tool.profile-management-content-library-configuration.educational-establishments"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
  - "core.data-loader"
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
  - "requirements"
  - "setup_task_sequence"
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "requirement"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-management-content-library-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-management-content-library-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-management-content-library-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-management-content-library-configuration/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "HRT_MANAGE_PROFILE_CONTENT_TYPES"
  - "HRT_MANAGE_PROFILE_CONTENT_ITEMS"
  - "ORA_MANAGE_PROFILE_ITEM_CATALOG"
  - "HRT_MANAGE_INSTANCE_QUALIFIERS"
  - "HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "May create local review-only input-normalization, requirement, proposal, validation, traceability, and skill-run artifacts in the selected project workspace."
  - "May request a routed read-only FSM task export when exact current-state evidence is required."
  - "May read an explicitly supplied local FSM export ZIP and emit a sanitized schema, duplicate, or readback evidence summary without modifying the archive."
  - "May read the checked-in, source-backed Oracle-seeded Content Type and Content Item catalogs for local exact-key resolution; these catalogs are evidence only and are never import payloads."
  - "May use the standard read-only talentContentItemCatalogs resource and one source-backed registry-selected child relation for Content Item duplicate or readback evidence; read support does not imply create support."
  - "May create one project-local immutable create-only FSM ZIP and sanitized readiness receipt for Content Types, supported-mode Content Items, Educational Establishments, Item Catalog catalog rows, or one anchored catalog-owned Content Item after separate package-preparation authorization."
  - "May prepare one new Item Catalog and all supplied portable children only under the separate controlled-certification, non-production new-set contract and its exact complete-set preparation approval."
  - "May route an exact reviewed FSM ZIP through core.data-loader; upload and initiation remain subject to its Task Hook, immutable preview and authoritative approval workflow."
  - "May prepare and hand off one verified four-field GOAL HDL exception through core.data-loader only after explicit exception selection and its separate evidence, lifecycle, package and approval gates."
  - "May create a local immutable complete-set preview, approval record, submission receipt summary, and readback discrepancy result; the local lifecycle helper has no Fusion connectivity."
required_privileges:
  - "View and export access for the selected Profile Management setup tasks when live read-only evidence is requested."
  - "FSM task CSV import and Fusion Documents upload privileges for the selected core.data-loader execution."
  - "For an explicitly selected verified GOAL exception only, ContentItem HDL and upload privileges required by core.data-loader."
---

# Profile Management Content Library Configuration Implementation Guidance

## Purpose

Capture supplied configuration through direct values, a blank requirements template, or a readable existing file. Keep one complete parent/child/relationship request, confirm uncertain mappings, and leave omitted optional values omitted. Select tasks from supplied objects and fields. Do not ask for business purpose, downstream consumers, workforce design or intended use. Current V1 follows FDD v3 and all 25 Jira acceptance criteria; unsupported providers remain visible blockers.

Execution applicability: do not persist customer-bearing source or export data
in this workspace. For Item Catalogs, apply the [optional-export policy](item-catalogs/references/optional-export-policy.md): skip pre-import export without attempting it; post-import export failures route to registered REST verification with coverage disclosed. Other live package preparation requires complete exports
proven to contain only permitted synthetic or approved seed data. Otherwise the
missing Core data-handling contract blocks export acquisition and execution;
local guidance and sanitized review preparation may continue.

## When to Use

Use this skill when an implementation needs controlled reusable definitions for competencies, skills, behaviors, certifications, education, or other approved Profile Management content. A user may begin with business language, a source file, or expert technical values.

Route these requests elsewhere:

- Rating models: `hcm.hcm-tool.profile-rating-model-configuration`.
- Profile Types, Content Sections, or behavior enablement on a section: the Profile Types and Content Section owner.
- Worker, job, position, or other profile-instance changes: the owning profile or data-maintenance skill.
- Migration or independent bulk content-item, translation, or relationship loading: Profile Management Data Load, Migration, and Maintenance. Repeating child rows within one supplied configuration set are not, by themselves, bulk migration; retain the complete set and evaluate its supported provider shape.
- Downstream goals, templates, plans, meetings, notifications, performance, talent review, succession, compensation, or Skills Center setup: the consuming product skill.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `HCM Tool` (`CUSTOM_HCM_TOOL`)
- Functional area / Setup Object: `Profile Management Content Library Configuration` (`CUSTOM_TALENT_PROFILE_CONTENT_LIBRARY`)

## Workflow Entry and Project Context

Enter implementation requests through `router.implementation-router`. Use the
selected `project/{project_id}` workspace for durable artifacts and run records;
if no project exists, initialize `draft-impl-project-<YYYY-MM-DD>` from
`project/_template` before project-impacting work. Record token usage in that
project's prescribed token-usage log. A REST path, OAuth session, export helper,
or loader is never an alternate entry route.

## Runtime Prerequisite

Repository automation requires Python 3.10 or newer; Python 3.11 or 3.12 is
recommended. Verify the interpreter before invoking a helper and do not use a
host `python3` command that resolves to an older runtime. The copy-ready
commands in this package use `python3.11` explicitly.

## Execution Phases and Approval Boundaries

| Phase | Permitted work | Gate to continue |
|---|---|---|
| Setup guidance | Generate or return the deterministic blank intake XLSX and a business-language checklist | Terminal review-only result; no Fusion preflight is required |
| Review proposal | Local normalization, validation, dependency resolution, and routed read-only evidence | User reviews the proposal; no execution approval is created |
| Package preparation | After the applicable preview and exact provider-row approvals, build and reopen one project-local immutable FSM archive for the supported task | Package readiness receipt and exact archive fingerprint |
| Core Data Loader preview | Run Task Hook and build the loader's immutable preview for the unchanged archive | Core Data Loader's authoritative fingerprint-bound approval |
| Submission | Upload and initiate the one approved unchanged archive | Accepted initiation receipt; never replay automatically |
| Verification | Poll when requested and obtain fresh same-target readback | Exact approved-versus-saved comparison |

Copyable phase checklist:

- [ ] Offer direct values, a blank requirements template, or an existing readable file without requiring a Fusion task, release, URL, or screenshot.
- [ ] For template-only guidance, return the deterministic blank workbook without Fusion preflight. For incomplete readable intake, retain supplied rows and identify missing values or mappings in a preliminary review.
- [ ] Normalize the intake and resolve task-local dependencies without creating a package.
- [ ] Collect fresh same-target evidence, overlay integrity-validated seed evidence where allowed, and classify every exact provider key.
- [ ] Present all supplied values, confirmed or uncertain mappings, omissions, exact identifiers, exclusions, blockers and the proposal fingerprint.
- [ ] After a new package-preparation request, obtain `PREPARE PACKAGE <preview_fingerprint>` where the canonical preview applies, then present the exact provider rows and their fingerprint for separate approval under the [approval sequence](references/fsm-import-contract.md#fingerprint-and-approval-sequence).
- [ ] Only after those applicable approvals, build and reopen the supported immutable FSM archive and record its SHA-256 receipt. Material changes invalidate the earlier approvals.
- [ ] Hand the unchanged archive to `core.data-loader` for Task Hook validation and its authoritative upload/initiation approval.
- [ ] Preserve submission receipts, poll only within the bounded timeout policy, and compare fresh readback with the approved preview.

## Setup Tasks

1. [Content Types](content-types/SKILL.md) (`HRT_MANAGE_PROFILE_CONTENT_TYPES`)
2. [Content Items](content-items/SKILL.md) (`HRT_MANAGE_PROFILE_CONTENT_ITEMS`)
3. [Item Catalogs](item-catalogs/SKILL.md) (`ORA_MANAGE_PROFILE_ITEM_CATALOG`)
4. [Instance Qualifiers](instance-qualifiers/SKILL.md) (`HRT_MANAGE_INSTANCE_QUALIFIERS`)
5. [Educational Establishments](educational-establishments/SKILL.md) (`HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS`)

## Proposal Boundaries

- Capture supplied objects, identifiers, parents, children and relationships in ordinary language or technical fields. The [supplied-configuration contract](business-intent-contract.md) owns routing and mapping provenance.
- Select a child only from an unambiguous supplied object or explicit task. Clarify an uncertain object or field mapping without asking why or for downstream use.
- Mark uncertain record review as `inferred-pending-review` and canonical `mappings[].status` as `uncertain`; require confirmation before creation. Never infer missing configuration from comparable setups.
- Use only provider-defined exact keys and case/normalization semantics. Stop on duplicates and display actual matched identifiers. Do not perform fuzzy, semantic, near-match or intelligent reuse analysis.
- Leave omitted optional values omitted; descriptions, translations and dates require supplied values and applicable supported contracts.
- Never create rating models, levels or foundations; never update, merge, delete, end-date, migrate or change downstream configuration.
- Catalog flags are metadata, not execution authority. A proposal cannot call an import, loader or write provider. Only the explicitly selected [verified GOAL fallback exception](references/verified-fallback-contract.md) can use its registered HDL provider; other HDL routes remain inactive and fallback evidence is excluded from FSM-only acceptance.

## Required Inputs

Offer these three entry methods:

1. Directly supplied configuration values.
2. A blank requirements template: the [multi-sheet XLSX](templates/profile-management-content-library-configuration-intake.xlsx) is the default for repeating data; [flat CSV](templates/profile-management-content-library-configuration-intake.csv) is optional.
3. An existing readable spreadsheet, CSV, Word, PDF or text file.

For a template-only request, use the [setup-guidance contract](references/setup-guidance-template-contract.md) without Fusion preflight. For values or an existing file, preserve the complete supplied request and normalize supported fields. A host-readable document requires extraction and confirmed source-to-field mappings; the CSV/XLSX helpers do not parse arbitrary Word or PDF.

Preserve input method, safe filename, source fingerprint, page/sheet/row, values and confirmed mappings. Show uncertain mappings for confirmation and missing required values with their object/row correction. Omitted optional values remain omitted. Keep sources unchanged and customer-sensitive contents outside the project. Intake files are neither loader packages nor import authority.

## Phase-Conditional Read Order

Load only the material required for the active phase and selected task:

1. For template-only guidance, read only the [setup-guidance and blank-template contract](references/setup-guidance-template-contract.md) and run the local generator.
2. For every proposal, read the [supplied-configuration contract](business-intent-contract.md), [source-backed input contract](references/source-backed-input-contract.md), [complete review-only proposal contract](references/review-only-proposal-contract.md), [canonical configuration-set schema](schemas/profile-content-library-configuration-set.schema.json), and each selected child `SKILL.md`. For an Item Catalog route, also read the task-local [supplied catalog routing reference](item-catalogs/references/business-intent-routing.md).
3. Before any live read, read the [authenticated environment and REST capability contract](references/environment-preflight-contract.md).
4. For task-local validation, read only the selected child's `ora-resource/ora_rule_registry.json` and the source anchors reachable from the chosen graph nodes.
5. When executing a task-node graph, also read the [task-node execution guide](references/task-node-execution.md).
6. For historical technical Data Loader workbook regression review only, read the [XLSX delivery-route contract](references/xlsx-delivery-route-contract.md). The verified GOAL exception uses its exact isolated helper, not generic technical workbook or HSDL preparation.
7. When inspecting an existing export ZIP, also read the [FSM evidence and exact-comparison contract](references/fsm-evidence-contract.md).
8. When assessing package eligibility, read the [create-only FSM import contract](references/fsm-import-contract.md); for one new catalog with portable children also read the [new-set contract](references/new-catalog-set-contract.md). Reading eligibility rules during proposal review does not prepare a package. Construction still requires a separate package-preparation request and exact approval.

The task-node guide and registry do not authorize a Fusion write.

## Provenance Contract

Every material value must record its value, owning task, source type, sanitized evidence, exact source reference, confidence, materiality, review status, inference reason, proposal/execution status, and last-confirmed fingerprint. Allowed review statuses are `supplied`, `inferred-pending-review`, `confirmed`, `blocked`, and `not-applicable`.

Retain supplied values, unresolved mappings, and blocked rows in an immutable review-only proposal with their actual review status. Only an executable creation preview or package requires every material value and mapping to be supplied and confirmed as applicable. Do not add omitted optional values or defaults. A provider-generated technical field requires its documented approved execution/readback rule.

## Phase-Conditional Preflight

Do not run Fusion preflight for a blank-template or setup-guidance request. Do not require complete requirements for that stage.

For a configuration-ready local proposal, confirm the following. Preliminary
review may retain unresolved task ownership in `unmapped_records`; missing
scope confirmation blocks exact checking and execution, not display of supplied rows.

- `project_id` and safe project artifact paths.
- Input method, source fingerprint, supplied objects and values, applicable supplied dates, and each mapping's actual confirmation status.
- An unambiguous supplied object structure, exact task/object scope, or confirmed technical mapping.
- One functional-area request or one complete related set.
- The selected child tasks and exact task codes.
- Input readability, source fingerprint, and mapping review status.
- Required task-local registries and source anchors.
- Exact current-state evidence only where duplicate classification is required; otherwise label the proposal preliminary.
- Provider readiness is `eligible-for-separate-package-review` only for a create-only Content Types, Item Catalog catalog-row or phase-one anchored Content Item, or Educational Establishments request that satisfies the FSM import contract, or a Content Items request that satisfies its profile-mode-selected guarded FSM or Item Catalog FSM handoff contract. The explicitly selected verified GOAL exception instead requires its complete four-field single-row fallback contract and fresh dual-key evidence; it does not enable a combined FSM preview or authorize package construction. Keep every other creation/import route blocked.
- The explicit new-catalog portable-child mode is a separate controlled-certification eligibility case under the new-set contract, not general-use or canonical mixed-task eligibility. Preserve all supplied rows and apply its complete-set, non-production and exact approval checks.
- The operation is local or read-only and has no Fusion side effect.

Stop the affected exact-check, package or execution phase on missing, ambiguous, stale, unsupported or conflicting inputs. Readable incomplete configuration stays in preliminary review with explicit blockers; do not discard it or require confirmed mappings merely to show it. Unreadable or unsafe input cannot be normalized and requires a safe replacement.

Before any Fusion operation, use the [operation-scoped preflight](references/environment-preflight-contract.md). FSM exports and template/spec exports use the existing task-level export workflow's authentication, task/CSV, privilege and approval checks; they do not require a Content Items REST capability receipt. Only the registered Content Items REST branch requires its bounded capability GET. Never substitute screenshots or user attestations for authenticated target identity or privilege evidence. The [new-set contract](references/new-catalog-set-contract.md) alone permits explicit user-confirmed non-production classification bound to that authenticated target and reviewed proposal; export data-handling and import-approval gates are unchanged.

Release metadata is informational for every task and phase, including availability, seed overlays, exact checks, FSM packaging/import, all nine catalog-backed contexts, test batches and the selected verified GOAL fallback. Do not require, verify or match a release to proceed. Follow the [release policy](references/environment-preflight-contract.md#release-metadata-is-informational): preserve source provenance, validate actual provider/schema and complete target evidence, and use unknown where metadata is unavailable. A successful read does not certify a create provider.

## Supplied-Configuration and Expert Scope Routing

1. Offer direct values, a blank requirements template or an existing readable file.
2. Preserve supplied configuration without requiring Fusion terminology or business-purpose discovery.
3. Select task ownership using the supplied objects/fields or explicit task/code in the [routing contract](business-intent-contract.md).
4. Clarify an ambiguous object or source mapping before creation; never silently infer values or select from an intended downstream use.
5. Apply the explicit Content Type of the current item; do not inherit a previous item's context, evidence or builder. Preserve PROJECT versus SPECIAL_PROJECT and all registered context gates.
6. Keep all related task rows in one complete request; selected child graphs own task-local checks only.
7. Reject out-of-scope update, delete, merge, migration, foundation or downstream work and name its owner.

## Current V1 Execution Scope

The governed intake workbook is local requirements input and has no delivery authority. Strict V1 acceptance supports only the declared create-only FSM routes. The separately selected [verified GOAL fallback exception](references/verified-fallback-contract.md) is available through Core Data Loader; it does not enable generic HDL/HSDL/DAT or direct REST/browser creation.

Historical technical-workbook and other DAT/HDL helpers remain regression history. Only the verified single-row GOAL provider is selectable under the explicit exception contract. Preserve complete-set review, all exact locks, immutable approval and independent readback. Never auto-fail over after submission or promote fallback evidence into FSM acceptance.

An expert request naming Content Types, Content Items, Item Catalogs, Instance Qualifiers, Educational Establishments or an exact task code uses the same preflight and continues without a business-language restatement.

## Complete-Set Coordination

Keep all supplied parents, child rows, translations, descriptions, memberships, qualifier rows, establishments, and relationships in one request even when they arrive on separate sheets or pages. The parent owns set integrity and proposal assembly; children own only task-local checks. Child registries must not encode cross-task order.

The parent may propose these review mappings:

- Controlled type definitions, properties, or type relationships: Content Types.
- Approved items, translations, item-specific proficiency descriptions, or item relationships: Content Items.
- Controlled catalogs, memberships, item rating descriptions, or behavior catalogs: Item Catalogs, with Content Items when item definitions are supplied.
- Instance qualifier sets and qualifier rows: Instance Qualifiers.
- Approved schools or educational establishments: Educational Establishments.

The canonical contract always carries all 14 governed groups: Content Types, Content Type Properties, Content Type Relationships, Content Items, item-specific rating descriptions, Content Item Relationships, Item Catalogs, catalog memberships, catalog item-specific rating descriptions, Instance Qualifiers, Instance Qualifier Sets, Educational Establishments, Behavior Item Catalogs, and Competency-to-Behavior Relationships. An omitted group is an explicit empty array, never a silently dropped section.

## Exact-Match Rule

Use only a workflow-approved, unfiltered current-state task export or another explicitly authorized read source. For Content Types, and for Content Items whose selected evidence provider is FSM, overlay the integrity-validated Oracle seed catalog after the fresh customer export. For a registered enhanced-profile Content Item context, use its exact Talent Catalog child GET across every owning catalog instead. The customer/seed order is fixed where it applies: fresh customer rows override the same seeded provider key; seed rows fill only keys or child rows that the task export omits. Classify each independently identifiable record as `exact`, `not-found`, `multiple-exact`, or `evidence-unavailable`; for an exact seeded-overlay Content Type or Content Item, record `match_source` separately as `customer` or `seeded`.

- `exact`: stop creation and display the actual matched identifier and its evidence.
- `not-found`: retain the value in the review-only proposal.
- `multiple-exact`: block and ask for authoritative disambiguation.
- `evidence-unavailable`: block duplicate disposition; do not assume the value is new.

A header-only Content Types or Content Items export remains schema-only by itself. It may act as an empty customer layer only when the export is explicitly attested as unfiltered, is bound to the exact target, and is combined with a validated seed catalog for the declared task/provider schema. A catalog mismatch, missing manifest fingerprint, or filtered/ambiguous export fails closed.

Do not compute or display fuzzy, normalized-name similarity, semantic or intelligent reuse analysis. Provider-defined exact case/normalization rules remain authoritative, including real Name/code collision guards. An exact duplicate blocks create regardless of whether other values differ; display those differences without proposing an update.

## Review-Only Proposal

Return one proposal conforming to the [complete review-only proposal contract](references/review-only-proposal-contract.md), containing:

- Complete supplied objects and values, source references, and confirmed or pending-review technical mappings.
- Selected task scopes and complete-set boundary.
- Supplied values with provenance and review status; omitted optional groups and unresolved required values.
- Exact-match classifications, actual matched identifiers, target/source binding and evidence freshness.
- Validation and dependency results.
- Omissions, assumptions, exclusions, and provider blockers.
- Source and proposal fingerprints.
- The pre-execution actions `Prepare configuration` and `Review assumptions`.

`Prepare configuration` means prepare or refine a local immutable proposal artifact. It does not authorize creation, package construction, import, or any provider call.

Example response:

> An exact duplicate blocks creation. The report identifies the matched record and retains all supplied parent, child and relationship rows for review.
>
> No Rating Model, Profile Type, employee Talent Profile, import, or downstream configuration will be changed.
>
> Prepare configuration | Review assumptions

## Proposal and Approval Separation

Fingerprint the complete supplied request, target, source and mappings, dependencies, exact evidence, exclusions and provider-readiness result. Any material change invalidates confirmation.

A review proposal or exact-check report cannot authorize package construction or upload. A separately requested package phase may prepare a supported create-only FSM artifact, or the explicitly selected isolated [verified GOAL exception](references/verified-fallback-contract.md), and hand it to Core Data Loader's authoritative Task Hook, immutable preview and approval/auto-approval workflow. No other HDL fallback is enabled. Do not manufacture or transfer approval evidence.

Content Types, supported-mode Content Items, catalog identity rows, the guarded existing-parent/one-child catalog path and Educational Establishments retain their existing package boundaries. Do not remove catalog/rating-description guards or introduce an unsupported qualifier, relationship or HDL route to satisfy a complete-set request.

## Creation Preview and Lifecycle

For one new Item Catalog with all supplied portable children, use the separate
[new catalog set contract](references/new-catalog-set-contract.md). Its explicit
complete-set preview and preparation modes are controlled-certification only,
not general-use or live-verified. Existing canonical and candidate-only modes
are unchanged; never discard unsupported rows to enter the new mode.

On a later new-set status/readback request, obtain evidence through the declared
Core status, task export and registered Content Items read workflows first.
Then run the contract's local `scripts/verify_new_catalog_set_lifecycle.py`
command to bind the complete proposal, archive, Core approval, accepted IDs,
terminal status and complete readback. This is offline post-processing, not a
new acquisition or execution route. Missing ProcessLog or partial readback must
not erase a retained failed import. Mixed-task canonical lifecycle support is
unchanged; do not treat this single-task result as verification of other groups.

For local development verification of conditional proficiency references,
complete blocked previews and new-catalog/multi-child candidates, use the
[three-task validation contract](references/three-task-validation-contract.md).
These reports do not promote provider capability, construct a broader import
package or authorize a Fusion operation. Existing execution gates remain intact.

After validation and exact duplicate checks, build the canonical complete-set object with `scripts/build_profile_content_library_preview.py`. Its combined-set preview supports only eligible Content Types, legacy standalone Content Items and Educational Establishments. It does not approve an Item Catalog handoff. Catalog-row creation and the existing-parent/one-child Item Catalog path use their task-specific FSM package and `core.data-loader` Task Hook preview instead, and remain blocked on this combined-set submission surface. Rating-description, competency-to-behavior and Instance Qualifier rows remain reviewable but block persistence. Never drop blocked rows to make a subset appear complete.

The complete preview includes all represented values, parents, relationships, exact-match results, dependencies, omissions, target alias, provider route, exclusions, and a SHA-256 fingerprint. Obtain the exact statement `PREPARE PACKAGE <preview_fingerprint>` before constructing the local immutable per-task package. This statement authorizes only package preparation; it does not authorize upload, initiation, or any Fusion mutation. Any material change invalidates the authorization. `core.data-loader` remains the sole authority for the later upload/initiation approval, and this skill does not perform a direct Fusion write.

Follow the [fingerprint and approval sequence](references/fsm-import-contract.md#fingerprint-and-approval-sequence) to distinguish complete-preview review, exact provider-row approval and the final Core archive gate.

After the loader returns one receipt per selected task, record `submitted_pending_verification`; initiation is not completion. In a later status/readback request, revalidate the exact approval statement, approved lifecycle, same-set submission identity and complete receipts before comparing fresh same-target evidence. The local helper accepts normalized task statuses `succeeded`, `failed`, `pending` or `timeout`; a failed task returns `process_failed`, while pending/timeout remains `readback_pending`. Unknown statuses are invalid input. Preserve the status evidence and inspect failed ProcessLogs without resubmitting.

Require every process to succeed before comparing all 14 groups to the approved preview. Compare canonical local mapping keys, provider keys, values and relationship links; only `source_references` and `review_status` annotations may differ or be absent in independent readback. The approved preview retains both annotations unchanged. Missing/extra groups, rows or persisted values cannot be verified. Return the invalid-shape diagnostic or `readback_mismatch` as applicable, disclose differences, and never auto-correct or automatically resubmit. The `verify` CLI exits nonzero for failed, pending or mismatched results.

## Read-Only Evidence and Readback

Route current-state evidence collection through `shared.setup-export.task-level-export` with the exact task code. Treat exports as evidence only:

- Content Types can provide schema evidence even when no business rows are present.
- Content Items and Educational Establishments can support exact current-state comparison when their complete exports are fresh.
- Item Catalog identity supports exact full-export comparison, catalog-only create packaging, and fresh full-export readback. The phase-one route also supports one catalog-owned Content Item through one exact existing-catalog anchor, with code/name duplicate locks and parent-no-drift readback. Rating-description mutation remains blocked. `talentContentItemCatalogs` and one source-backed child may still be used read-only by the Content Items workflow.
- Instance Qualifiers has source-backed proposal and identity fields, but the standalone 26C task is diagnostic-only: Fusion moved qualifier sets under Profile Type Sections in 21A, and standalone exports return no CSV columns. Route current/readback evidence through the Profile Types owner using HRT_MANAGE_PROFILE_TYPES; never retry or import the standalone task.

If a future provider is approved, read back every saved value through that provider's canonical read contract or a fresh complete task export, compare it with the exact approved proposal, report discrepancies, and never auto-correct them.

## Local Provider Foundation

Use [the FSM evidence contract](references/fsm-evidence-contract.md) and `scripts/profile_content_library_fsm_evidence.py` to inspect already exported Content Types, Content Items, Item Catalogs, or Educational Establishments ZIPs. The helper validates archive safety, exact observed headers, task identity, evidence purpose, same-target eligibility, task-local dependencies, exact duplicates, and readback differences without persisting full current rows.

The evidence helper remains read-only. For a separately approved create-only
package phase, read [the FSM import contract](references/fsm-import-contract.md)
and use `scripts/prepare_profile_content_library_fsm_package.py`. The package
helper accepts only project-local artifacts, requires a separate fingerprint
for exact provider rows and dependency evidence, preserves export-derived
metadata, blocks existing keys and generated identifiers, emits a sanitized
readiness receipt, and has no Fusion connectivity.

Package readiness routes to `core.data-loader`; it never authorizes upload.
Core Data Loader must invoke Task Hook against the exact final ZIP, create its
own immutable preview, apply its authoritative approval policy, verify the same
SHA-256, and only then upload and initiate with the selected `sourceType`.
That policy permits same-request unambiguous no-confirmation authority only for
the identified load; otherwise require a later contextual approval. Neither
case waives validation or authorizes a standalone, later, or session-wide load.
Guarded FSM readback uses a fresh complete same-target export when available. Item Catalogs may skip or fail export and use registered REST reads, reporting partial or incomplete verification under their optional-export policy. Registered enhanced-profile
Content Item readback uses the exact selected Item Catalog child resource when its active workflow declares it.

This route currently supports create-only Content Types and Educational
Establishments through FSM, Item Catalog catalog rows and one anchored
catalog-owned Content Item through FSM, and profile-mode-selected Content Items
through guarded FSM or an eligible Item Catalog FSM handoff. Registered REST
read evidence and historical HDL certification do not establish current V1 creation support. Content Types remains operationally blocked with header-only evidence alone;
an attested, unfiltered, exact-target empty customer layer may be combined with the integrity-validated seed catalog under the declared overlay contract. Item Catalog
rating-description rows, Instance Qualifiers, item-specific proficiency
descriptions, updates, merges, deletes, and end-dates remain unsupported.

The separate new-set contract additionally permits controlled-certification
preparation and retained lifecycle verification for one new catalog and all
portable children. It does not inherit the anchored-child route's live status.

## Refusal Rules

Refuse the affected check, package or execution action and return one safe next action when:

- Input is unreadable or unsafe, or an action's required input is incomplete, ambiguous, invalid or stale. Retain readable supplied rows and unresolved mappings in preliminary review; missing execution evidence is not a reason to erase the proposal.
- Required parents, endpoints, identifiers, relationships, dependencies, or exact current evidence are missing.
- An exact duplicate, multiple exact matches, or unavailable exact evidence prevents creation.
- The request asks this skill to make workforce-design decisions or invent competencies, behaviors, certifications, degrees, or controlled values.
- The request belongs to another skill.
- The request asks to update, merge, delete, end-date, replace, or use an unsupported task/provider. Creation/import is permitted only through the separately gated FSM routes or the explicitly selected verified GOAL exception under its isolated contract; that exception does not establish original FSM-only acceptance.
- The provider, field, privilege, idempotency, error, or readback contract is missing.
- Proposal confirmation is presented as execution approval.

## Error and Traceability Contract

Classify durable failures as `input_validation`, `catalog_or_metadata_mismatch`, `auth_expired_or_invalid`, `authorization_or_privilege`, `transport_or_environment`, `fusion_api_error`, `process_timeout`, `process_failed`, `artifact_persistence`, or `approval_blocker`.

### Retry, Timeout, and Recovery Policy

- Treat input, catalog, privilege, artifact, and approval failures as non-recoverable until the stated prerequisite is corrected; do not retry them automatically.
- Allow the routed core authentication workflow to refresh a managed cached token once after a 401 or 403. Never replace an explicitly supplied token, and treat a repeated 403 as `authorization_or_privilege`.
- Retry read-only transport failures at most twice with bounded backoff. Never retry POST, import, upload, initiation, or ESS submission without an idempotency guarantee or a new explicit Data Loader approval.
- Delegate process polling to `core.data-loader` with a default 300-second ceiling and 10-second interval unless its approved preview declares a stricter bound. On timeout, stop and return the target alias, task code, source type, ProcessId or requestId, last status, elapsed seconds, and one status-only next-check action.
- On terminal process failure, retrieve the sanitized ProcessLog or status payload when available and preserve the task code, ProcessId, requestId, ECID, archive SHA-256, and diagnostic artifact reference.
- For a multi-task set, retain successful submission and verification receipts, append each failed task to an `errors` array with stage, task code, failure class, message, and safe next action, and return an overall nonzero or not-verified result. Never resubmit successful or failed units automatically.
- Recover by correcting inputs and creating a new fingerprinted preview/package, or by resuming status/readback for an existing external ID. Do not auto-correct Fusion data, roll back another successful task, or reuse an approval after any material change.

Persist only sanitized input method and source references, source fingerprint, volunteered optional context, normalized non-sensitive values, mappings, validation, dependency and duplicate results, proposal/preview fingerprints, exclusions, provider readiness, lifecycle state, and one safe next action under the declared project workspace. Never store source documents, credentials, tokens, employee data, real customer data, customer-bearing exports, or sensitive environment details. Project-local package inputs may contain only verified non-customer synthetic or approved seed setup data; if a required full export may contain customer data, stop before acquisition and record the missing Core data-handling contract. Do not filter, redact, relocate, or weaken complete-evidence checks to bypass this gate.

### Redaction Behavior

Before display or persistence, recursively redact values under credential, authorization, client ID, password, secret, token, token-cache, or private-key fields and redact strings that resemble bearer tokens, credentials, or private-key material. Never print or persist the original sensitive value, full base64 payload, source document, or customer-sensitive row. If redaction makes a required provider value unverifiable, stop with `input_validation`; do not continue to preview or execution.

## Source Basis

- [HCM Tool FSCR taxonomy](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/hcm-tool-fscr-taxonomy/)
- [HCM Tool foundation baseline](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/hcm-common-foundation-skill-baseline/)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
- [Profile Management components](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/profile-management-components-how-they-work-together.html)
- [Using Enhanced Talent Profiles](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/using-enhanced-talent-profiles.pdf)
- [Content Types](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/content-types.html)
- [Content Type Properties](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/content-type-properties.html)
- [Content Items](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/content-items.html)
- [Content Type Relationships](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/examples-of-content-type-relationships.html)
- [Competency-to-Behavior Relationships](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/considerations-for-associating-behaviors-with-competencies.html)
- [Content Section Properties](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/content-section-properties.html)
- [Instance Qualifier Sets](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/instance-qualifier-sets.html)

## Provider Readiness

Content Types, Content Items, Item Catalog catalog rows and phase-one anchored
Content Items, and Educational
Establishments have a local create-only package contract and a mandatory execution handoff to
`core.data-loader`. Runtime readiness still requires an approved proposal,
complete fresh same-target duplicate evidence, a reviewed same-task package
baseline, exact provider-row values and their separately approved fingerprint,
task-local dependency evidence, a ready
Task Hook graph, and approval of the immutable Data Loader preview.

For Content Items, legacy profile mode selects guarded FSM and enhanced mode
requires an eligible Item Catalog FSM handoff. Generic enhanced-profile Content Item rows must
never enter the Content Items FSM package: non-`GOAL` uses its registered
evidence and eligible Item Catalog FSM handoff, while
`GOAL` FSM creation remains blocked after the verified companion-document transformation
failure. The separately selected verified GOAL fallback can be evaluated under its
own contract; no selection or live approval is implied by the FSM failure. Header-only Content Types evidence does not satisfy the duplicate lock
by itself; it is eligible only as an attested unfiltered same-target customer
layer combined with the integrity-validated seeded catalog. Item Catalog
package readiness permits skipped/failed current-state export and reusable validated
package templates under its optional-export policy, with unverified checks disclosed.
It permits catalog identity rows or one intended anchored Content Item child.
The explicit new-set contract is the separate exception for one new catalog and
all supplied portable children, with certification-only, non-production scope
and its own complete preview, package and retained lifecycle verification.
Instance Qualifiers and Item Catalog rating-description or advanced child rows
have no approved package contract. Item-specific proficiency
descriptions remain blocked. These gaps do not block intake normalization or
review proposals, but they prevent the affected package or execution path.

## Source Provenance and Reviewer Requirements

Manifest applicability is not blanket create-provider certification. Source
release labels and historical canary versions describe where evidence came
from, not runtime eligibility. Validate packaged catalogs by kind, hashes,
shape and exact keys without matching the target release. Keep customer-export
and packaged-seed availability separate; missing complete target evidence is
still an evidence gap. No release label is required to resolve that gap.

Before merge, require the HCM Pillar Development Lead or delegated Profile
Management SME plus an FSCR A-Team/core reviewer. Because this package contains
hybrid import and verification paths, also require automation and QA review;
add security or publication review when the merge scope triggers those gates.

## Implementation Notes

Use the generated nested setup-task skills for task-local planning and validation. Generate the default workbook with `scripts/generate_profile_content_library_template.py`; normalize it with `scripts/normalize_profile_content_library_workbook.py`, or normalize the optional flat CSV with `scripts/normalize_profile_content_library_intake.py`. Validate canonical JSON against `schemas/profile-content-library-configuration-set.schema.json` and use `scripts/build_profile_content_library_preview.py` for local preview, approval binding, submission-state, and readback comparison. These helpers have no network or Fusion-write route. Track token usage for every generated project artifact or skill-run record using the manifest policy. The approved external taxonomy ID `hcm.hcm-tool.profile-management-content-library-configuration-skill` is retained as source identity evidence; this repository skill's generator-authoritative ID is `hcm.hcm-tool.profile-management-content-library-configuration`.

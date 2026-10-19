---
skill_id: "hcm.hcm-tool.profile-management-content-library-configuration.item-catalogs"
name: "Item Catalogs Setup Task Guidance"
description: "Captures supplied Item Catalogs configuration from direct values, a blank requirements template, or a readable existing file; preserves complete-set provenance, exact duplicate reporting, and supported V1 FSM boundaries."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Profile Management Content Library Configuration"
functional_area_code: "CUSTOM_TALENT_PROFILE_CONTENT_LIBRARY"
task_code: "ORA_MANAGE_PROFILE_ITEM_CATALOG"
task_name: "Item Catalogs"
parent_skill_id: "hcm.hcm-tool.profile-management-content-library-configuration"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "HCM hcm tool pillar team"
version: "0.9.9"
inputs:
  - "supplied_configuration_objects_and_values"
  - "direct_values_blank_template_or_readable_existing_file"
  - "source_provenance_and_confirmed_mappings"
  - "conditional_supported_dates_descriptions_and_translations"
  - "template_guidance_checklist_or_example_request"
  - "expert_task_scope_or_explicit_item_catalog_values"
  - "project_context"
  - "normalized_task_request"
  - "approved_item_catalog_values"
  - "current_task_evidence"
  - "approved_create_only_catalog_provider_rows"
  - "approved_provider_rows_fingerprint"
  - "approved_content_type_dependency_evidence"
  - "validated_package_template_or_baseline"
  - "skipped_pre_import_export_receipt"
  - "test_only_batch_manifest"
  - "approved_test_batch_authorization_fingerprint"
  - "item_catalog_test_verification_receipt"
  - "item_catalog_fsm_provider_promotion_evidence_index"
  - "retained_new_catalog_set_lifecycle_and_core_approval_evidence"
  - "new_catalog_set_target_classification_confirmation"
outputs:
  - "supplied_object_routing_result"
  - "setup_guidance_or_blank_template_result"
  - "assumption_ledger"
  - "fusion_environment_capability_result"
  - "item_catalog_review_proposal"
  - "exact_match_result"
  - "non_executable_exact_check_report"
  - "dependency_readiness_result"
  - "sanitized_fsm_evidence_summary"
  - "item_catalog_readback_result"
  - "bound_new_catalog_set_lifecycle_verification_result"
  - "item_catalog_content_item_readback_result"
  - "immutable_fsm_package"
  - "fsm_package_readiness_receipt"
  - "core_data_loader_handoff_result"
  - "proposal_fingerprint"
  - "test_batch_execution_state"
  - "item_catalog_fsm_provider_promotion_proposal"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.data-loader"
oracle_supplied_guidance_files:
  - purpose: "Item Catalog input validation and supplied-configuration start nodes"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Item Catalog and Rating Model dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Exact current-evidence classification"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Item Catalog design enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Proposal terminal and refusal behavior"
    location: "ora-resource/ora_error_handling.md"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-management-content-library-configuration/item-catalogs/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-management-content-library-configuration/item-catalogs/current/"
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
  - "May create local review-only proposal, validation, and traceability artifacts."
  - "May request a routed read-only FSM task export for exact current evidence."
  - "May read an explicitly supplied local Item Catalog FSM export for sanitized exact-comparison evidence."
  - "May create one project-local Item Catalog FSM ZIP for either a new catalog row or one create-only Content Item with one exact existing-catalog anchor, after a separate package-preparation request."
  - "May route the exact package through core.data-loader after Task Hook validation; upload and initiation require the loader's separate immutable-preview approval."
  - "May orchestrate a fingerprint-bound test-only sequence through the unchanged core.data-loader initiation and status CLIs after one explicit composite batch authorization."
  - "May validate project-local canary evidence and create a review-only Item Catalog FSM provider-promotion proposal; it never promotes providers automatically."
  - "May prepare one explicitly approved certification-only new-catalog portable-child set and locally verify its retained lifecycle evidence; it never promotes this capability or submits from the verifier."
required_privileges:
  - "View access to Item Catalogs when live read-only evidence is requested."
  - "Item Catalogs task CSV import and Fusion Documents upload privileges for a separately approved core.data-loader execution."
---

# Item Catalogs Setup Task Guidance

## Purpose

Capture supplied catalog identities, memberships, rating descriptions, and supplied relationship references. Accept direct values, the blank requirements template, or a readable existing file; use the spreadsheet by default for repeating rows. Preserve every parent, child and relationship with exact source provenance and confirmed mappings. Do not discover business purpose, downstream consumers or workforce design, invent values, or infer omitted optional fields. Review remains non-executable.

Current GROW-8154 V1 permits only the independently supported create-only FSM shape through the authoritative Core Data Loader route. Catalog flags and source graphs are not live acceptance proof.

## Setup Task Skill Contract

- task_code: `ORA_MANAGE_PROFILE_ITEM_CATALOG`
- task_name: `Item Catalogs`
- parent_skill_id: `hcm.hcm-tool.profile-management-content-library-configuration`
- pillar: `HCM`
- offering: `HCM Tool`
- functional_area: `Profile Management Content Library Configuration`
- functional_area_code: `CUSTOM_TALENT_PROFILE_CONTENT_LIBRARY`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill for supplied catalog identities, memberships, rating descriptions, and supplied relationship references. Users need not know Fusion task terminology; route from their actual object fields and confirmed mappings. Ask only for missing required configuration or an ambiguous mapping. Do not request a business-purpose restatement. Return the complete review set and a non-executable exact-check report when requested.

A separate package request may use only the current supported FSM contract after its evidence and lifecycle gates. Never use HDL/HSDL as a V1 fallback.

## Workflow Entry and Runtime

Invoke this task through the parent skill after `router.implementation-router`
selects the project and task scope. Persist artifacts and token usage in that
workspace. Use Python 3.10 or newer; Python 3.11 is recommended.

[Release metadata is informational](../references/environment-preflight-contract.md#release-metadata-is-informational)
for every task phase. Do not require, infer, verify or match a quarterly or
technical release to select a catalog, report availability, check exact keys,
export, prepare a package or import. Use unknown when metadata is unavailable.
Validate actual task/provider/schema, target, complete evidence, dependencies,
lifecycle and approval instead. Keep seed/source provenance separate from
current target evidence. This does not enable an unsupported execution route.

## Setup Task Metadata

- Task name: `Item Catalogs`
- Task code: `ORA_MANAGE_PROFILE_ITEM_CATALOG`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Catalog Support and Controlled Route

`CSVExportImportSupportedFlag` is `Y` and `dataloader_import_mode` is generated as `FSM`. The product provider is `oracle.apps.hcm.profiles.contentLibrary.itemCatalogMigrationService.ItemCatalogMigrationService`. The task never calls that service directly.

1. Skip pre-import export; do not acquire current state or a new baseline. Use a supplied or reusable reviewed package/template and record the skipped checks under the [optional-export policy](references/optional-export-policy.md).
2. Validate supplied or exported data with `shared.validation.setup-data-validator`.
3. Validate referenced data with `shared.validation.reference-data-validator`.
4. For separately approved catalog-row package preparation, use the parent [create-only FSM import contract](../references/fsm-import-contract.md).
5. Route the immutable ZIP only through `core.data-loader`. Task Hook validation and a new immutable Data Loader preview must pass before a separate submission approval.
6. Do not use direct SOAP, REST, HDL, HSDL, browser automation, or a full export as a live payload.

If a reusable template is missing or an independently requested export fails on
an unrelated catalog's `RatingModelId`, read the
[filtered schema recovery guide](references/filtered-schema-recovery.md).
Offer that separately approved export investigation instead of treating an
attached template or a database repair as the only way forward. It is not an
automatic pre-import step and does not establish import or duplicate readiness.

Use this task metadata when invoking those skills:

- Offering: `HCM Tool`
- Functional area / Setup Object: `Profile Management Content Library Configuration`
- Setup task name: `Item Catalogs`
- Setup task code: `ORA_MANAGE_PROFILE_ITEM_CATALOG`




## Owned Scope

- Item Catalog identity and supplied translations or dates.
- Membership of already approved content items.
- Item-specific catalog rating descriptions when the exact Rating Model dependency is ready.
- Behavior Item Catalog scope and supplied competency-to-behavior relationships, with item definitions owned by Content Items.

Do not own Rating Model creation, Content Item business-intent invention, behavior enablement on a competency section, Profile Types, Content Sections, or profile instances. Content Items owns the requested item definition and hands its approved normalized values here for persistence. This execution increment supports either catalog identity rows or exactly one `ORA_TALENT_CATALOG_CONTENT_ITEM.csv` create row that is anchored to one exact current `ORA_TALENT_PROFILE_ITEM_CATALOG.csv` row. The rating-description member must remain empty.

Those are the default paths. Only the separate new-set contract below permits
one new catalog with multiple portable children for controlled certification;
it does not broaden the existing verified route or permit rating descriptions.

An explicit Skill item remains ContextName `SKILL`. Read
[Skill catalog creation](references/skill-catalog-creation.md) to select either
the controlled new-catalog route or the separate
[existing custom catalog canary](references/existing-skill-catalog-certification.md).
The latter prepares exactly one explicitly selected child for non-production
certification with supplied current parent evidence; it is not general-use or
six-item batch support. Neither route is an HDL fallback, Skills Center
configuration, or verified live acceptance. Never silently trim a supplied batch.

## Business-Intent Entry Contract

Follow the task-local [supplied-configuration routing contract](references/business-intent-routing.md). The compatibility filename does not require business-purpose discovery. Route supplied objects and confirmed mappings, preserve exact provenance, and stop ambiguous configuration mappings. Exact existing identifiers block creation; no reuse recommendation or comparable-value default is allowed.

## Required Read Order

Select the phase before applying this list. Guidance and blank-template requests
stop at step 2. For a local preliminary review, use the parent review-only
proposal contract and retain unresolved values or mappings; execution readiness
is not required merely to display the supplied request. Steps 4-9 apply when
entering the task graph for readiness, exact checking or execution, not as a
gate on preliminary review. Later phase-specific contracts remain conditional.

1. Read the parent [supplied-configuration contract](../business-intent-contract.md).
2. For guidance or a blank intake artifact, read the parent [setup-guidance and blank-template contract](../references/setup-guidance-template-contract.md) and do not enter the task graph.
3. For any Fusion-touching phase, read the parent [environment preflight contract](../references/environment-preflight-contract.md).
4. Read the [task-node execution guide](../references/task-node-execution.md) in full.
5. Confirm this selected task `SKILL.md` has the exact task code, task name, scope, and approval rules.
6. Load the [compiled registry](ora-resource/ora_rule_registry.json) and select the exact `ORA_MANAGE_PROFILE_ITEM_CATALOG` task.
7. Validate the selected registry against its source rows and graph using the task-node guide; require task readiness `ready` before proceeding.
8. Load the source file and heading for every reachable registry node: [input validation](ora-resource/ora_input_validation.md), [dependency readiness](ora-resource/ora_dependency_readiness.md), [reference lookups](ora-resource/ora_reference_lookups.md), [design enforcement](ora-resource/ora_design_enforcement.md), and [error handling](ora-resource/ora_error_handling.md).
9. Before entering the start node, load task-local [business-intent routing](references/business-intent-routing.md) and the canonical [review-only proposal contract](../references/review-only-proposal-contract.md).
10. For package preparation or import, read the [optional-export policy](references/optional-export-policy.md), the parent [create-only FSM import contract](../references/fsm-import-contract.md) and the source-backed [catalog Content Item provider registry](references/catalog-content-item-fsm-provider.json) in full. The Item Catalog optional-export policy controls export-related checks.
11. For an explicitly requested low-interruption test batch, also read the [test-only composite batch contract](references/test-only-composite-batch.md) in full.
12. For the separate new-catalog set mode or its later retained-evidence verification, read the [complete new-set contract](../references/new-catalog-set-contract.md) in full. Local post-submission verification follows the owning status/readback workflows; it is not a pre-import task-node prerequisite.
13. For one SKILL child in an existing custom catalog, read the [existing-catalog certification contract](references/existing-skill-catalog-certification.md). Its separate registry, explicit mode and local approval are mandatory; missing current parent evidence blocks this controlled test without triggering an export.

## Preflight

Guidance and blank-template generation require no Fusion access, target, release, lookup, credentials, completed requirements, or approval. Intake captures supplied configuration through the three input choices, records exact source provenance, confirms mappings and preserves omitted optional values. Do not discover comparable configurations or invent defaults.

Exact classification additionally requires complete fresh structured same-target evidence under the selected provider's supported identifier semantics. Display actual matched identifiers and stop creation on any exact match, including equal values. Do not produce generic fuzzy or near-match recommendations. Preserve real provider Name/code collision guards.

A live phase uses the parent operation-scoped preflight: the owning FSM export or Core Data Loader workflow supplies its task-specific checks; only registered Content Items REST reads require the bounded REST capability receipt. Unknown quarterly metadata does not block local review or eligible evidence acquisition. Release labels never gate classification, availability, packaging or execution; preserve actual provider/schema checks and never replace authenticated target identity or privilege evidence with screenshots or attestations. Only the [new-set contract](../references/new-catalog-set-contract.md) permits explicit user-confirmed non-production classification bound to that authenticated target and reviewed proposal; data-handling and import-approval gates remain unchanged.

Package preparation requires a separately approved complete proposal, exact provider-row fingerprint, a validated same-task template or baseline, applicable dependencies, target bindings and safe project-local output paths. Skip pre-import export without attempting it. Preserve unverified duplicate, parent-drift and indirect Profile V2 checks in the preview. Already-supplied evidence remains subject to validation and known conflicts must not be ignored. Unsupported rows remain in the review set with blockers; never trim the set to make an executable package appear complete.

The narrow child route still requires one exact intended existing catalog anchor and one eligible child, an approved supplier, empty rating descriptions and no advanced fields. Reject known code/Name collisions or parent drift; without current evidence mark those target comparisons unverified. Full-set capability is not established by this narrow route.

## Proposal Workflow

1. Start at `IC.CAPTURE_CONFIGURATION`; capture direct values, blank-template rows, or a readable existing file.
2. Preserve the complete supplied parent/child/relationship set, source references and mappings. Ask for missing required values or ambiguous mappings only.
3. Leave omitted optional fields omitted. Validate conditional descriptions, translations and dates only when supported and applicable.
4. Normalize confirmed mappings without creating dependencies or designing nearby objects.
5. For exact current-state claims, use only complete current evidence under exact provider semantics. Display matched identifiers and block creation on any exact match or collision; never recommend reuse. An import skips pre-import export and discloses unavailable target checks.
6. Retain unsupported rows and exact evidence gaps in one review-only set. Enforce ownership and no-update/delete/merge boundaries.
7. Fingerprint the complete review. Terminate at `IC.RETURN_PROPOSAL`, `IC.RETURN_EXACT_DUPLICATE`, or a precise blocker. Proposal confirmation never authorizes execution.

## Package, Approval, and Readback Workflow

The separate [new catalog set contract](../references/new-catalog-set-contract.md)
adds an explicit controlled-certification preview/preparation mode for one new
catalog and every supplied portable child. Only that mode replaces the existing
parent-anchor and one-child limits below. All other field, duplicate, target,
dependency and Core approval checks remain. It has no inherited runtime
verification and cannot use the existing one-child test-batch runner.

For that new-set mode, finish a later status/readback request with the contract's
`../scripts/verify_new_catalog_set_lifecycle.py` command. Retain the exact Core
envelope and task context used at submission, accepted request/process evidence,
ProcessLog and the available readback evidence. Attempt post-import export; on failure report it and try registered REST reads under the [optional-export policy](references/optional-export-policy.md). If the export omits child codes, obtain
every independent registered child observation through the Content Items owner.
The verifier can join those observed codes by exact provider key; it never fills
values from the proposal. A failed import stays failed even if its log or partial
readback is unavailable. The helper does not fetch, poll, upload, approve or retry.

`IC.RETURN_PROPOSAL` is terminal. Proposal confirmation cannot prepare a ZIP or authorize import.

1. On a separate explicit package request, validate the approved proposal/provider-row fingerprints, exact Content Type evidence, reviewed same-task package template and exact rows. Skip pre-import export and record skipped status with unverified checks; do not acquire a new baseline export either. For a Content Item, require a source-backed provider entry, lifecycle-compatible use (`controlled-certification` or verified-provider `general-use`), one intended parent anchor, one new child key, a supported supplier and no advanced fields. Known collisions still block; absence is not claimed without evidence.
2. Run `../scripts/prepare_profile_content_library_fsm_package.py` locally. A catalog-only package keeps both child members empty. A Content Item package contains one exact existing-catalog anchor and one create-only content-item row; the rating-description member remains empty. Return only `package_ready_for_core_data_loader_preview` plus the immutable ZIP and sanitized receipt.
3. Start a separate `core.data-loader` run for the exact ZIP. Task Hook must resolve the exact task context and build its immutable preview.
4. Apply Core Data Loader's authoritative approval policy: same-request unambiguous no-confirmation authority is limited to the identified validated load; otherwise require later contextual approval. The optional test-batch runner additionally requires its exact composite contract. Proposal confirmation alone remains insufficient.
5. After an approved load succeeds, capture status and ProcessLog and perform verification. Attempt post-import export; if it fails, report the failure and try supported registered REST reads. Compare exact child keys and all observable fields; report remaining parent/field/count coverage gaps as partially_verified or verification_incomplete. Do not replay or auto-correct imports because verification fails.
6. For the optional low-interruption test route, validate `../schemas/item-catalog-fsm-test-batch.schema.json` through `../scripts/run_item_catalog_fsm_test_batch.py`. The pillar runner may sequence the unchanged Core Data Loader initiation and status CLIs only when the user explicitly requested auto-approval, monitoring, and readback for the fingerprint-bound test batch. It must stop after each successful load until this Item Catalog skill supplies a bound verification receipt; that receipt resumes orchestration without another user approval. A blocked or completed state is terminal.

## Verified FSM Provider Lifecycle

The source-backed registry now marks `BEHAVIOR`, `CERTIFICATION`, `COMPETENCY`,
`DEGREE`, `EDUCATION_LEVEL`, `HONOR`, `LANGUAGE`, `MEMBERSHIP`, and `PROJECT`
as `verified` for the narrow 26C Content Item FSM shape. General-use routing is
therefore allowed only for that exact shape; it is not a standing authorization
to import.

Use `../scripts/item_catalog_fsm_provider_promotion.py propose` to reopen a
project-local, hash-bound evidence index and create a review-only lifecycle
proposal. The helper requires successful Data Loader and ProcessLog results,
exact child readback, a populated full Item Catalog export, parent no drift,
and the duplicate-create lock for every registered context. After the reviewed
source edit, use `verify-applied` to prove that the checked-in registry matches
the proposed logical contract. The helper is local-only and never calls Fusion,
changes the registry, uploads, retries, or approves a future package.

Every future general-use row follows the optional-export policy and still requires
one intended parent, rejection of known code and same-catalog name collisions,
an immutable one-parent/one-child package, Task Hook validation, and the normal
Core Data Loader package approval. The promotion does not enable Rating Model
values, rating-description rows, translations, relationships, dynamic fields,
generated fields, updates, deletes, end dates, multiple children, or
multi-context packages.

## Refusal Rules

Refuse an unresolved exact Rating Model reference for requested rating descriptions, missing item identities, invalid memberships, incomplete evidence presented as an exact-match result, multiple exact matches, invented catalog values, behavior-section enablement, another skill's scope, update/merge/delete/end-date, a missing or differing parent anchor or more than one Content Item child outside the explicit new-set contract, nonempty rating-description rows, unsupported child fields, a production or changed target in the test-only route, session-wide auto-approval, or any import route outside the parent FSM contract and `core.data-loader`. Incomplete evidence may yield only a clearly labeled preliminary scope proposal. Proposal or package confirmation never authorizes Data Loader submission. Core Data Loader alone decides whether an identified load has valid same-request auto-approval; the optional test-batch runner additionally requires its exact composite authorization and never creates session-wide authority.

## Data Safety

Persist only sanitized source references, fingerprints, non-sensitive normalized values, exact-match results, lifecycle status, and one safe next action. Never persist source documents, credentials, tokens, private keys, employee data, customer-sensitive values, full existing export rows, base64 content, audit identities, or sensitive environment endpoints.

### Redaction Behavior

Before display or persistence, recursively redact values under credential,
authorization, client ID, password, secret, token, token-cache, or private-key
fields and strings that resemble bearer tokens, credentials, or private-key
material. Never print or persist the original sensitive value, full base64
payload, source document, or customer-sensitive row. If redaction makes a
required provider value unverifiable, stop with `input_validation`.

## Required Reviewers

Before merge, require the HCM Pillar Development Lead or delegated Profile
Management SME plus an FSCR A-Team/core reviewer, with QA review for this
catalog-only hybrid package path.

## Implementation Notes

Use the parent skill for complete-set integrity and minimal cross-task coordination. Use the task-local business-intent reference for Item Catalog ownership, ambiguity, samples, and provenance. Package construction reuses the task-level Setup Hub FSM provider contract; transport remains owned by `core.data-loader`. The catalog Content Item provider registry is independently lifecycle-gated: no HDL provider state is inherited. All nine registered 26C contexts are now `verified` from their separately hash-bound FSM canary evidence, but only for the unchanged create-only, one-parent/one-child, supplier-C, blank-Rating-Model, zero-rating-description contract. Rating-description mutation remains blocked pending the next increment. Track token usage for generated project artifacts using the manifest policy.

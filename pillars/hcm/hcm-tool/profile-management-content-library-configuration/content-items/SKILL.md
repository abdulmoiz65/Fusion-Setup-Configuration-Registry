---
skill_id: "hcm.hcm-tool.profile-management-content-library-configuration.content-items"
name: "Content Items Setup Task Guidance"
description: "Captures supplied Content Items configuration from direct values, a blank requirements template, or a readable existing file; preserves complete-set provenance, exact duplicate reporting, supported V1 FSM boundaries and an explicitly selected verified GOAL fallback exception."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Profile Management Content Library Configuration"
functional_area_code: "CUSTOM_TALENT_PROFILE_CONTENT_LIBRARY"
task_code: "HRT_MANAGE_PROFILE_CONTENT_ITEMS"
task_name: "Content Items"
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
version: "0.14.7"
inputs:
  - "supplied_configuration_objects_and_values"
  - "direct_values_blank_template_or_readable_existing_file"
  - "source_provenance_and_confirmed_mappings"
  - "conditional_supported_dates_descriptions_and_translations"
  - "template_guidance_checklist_or_example_request"
  - "expert_task_scope_or_explicit_content_item_values"
  - "project_context"
  - "normalized_task_request"
  - "approved_content_item_values"
  - "current_task_evidence"
  - "validated_seeded_content_type_and_item_catalogs"
  - "approved_create_only_provider_rows"
  - "approved_provider_rows_fingerprint"
  - "fresh_package_baseline"
  - "profile_mode_evidence"
  - "exact_item_catalog_evidence"
  - "registered_content_item_rest_provider"
  - "explicit_verified_goal_fallback_selection_and_execution_history"
outputs:
  - "supplied_object_routing_result"
  - "setup_guidance_or_blank_template_result"
  - "assumption_ledger"
  - "fusion_environment_capability_result"
  - "xlsx_delivery_route_result"
  - "content_item_review_proposal"
  - "exact_match_result"
  - "non_executable_exact_check_report"
  - "sanitized_fsm_evidence_summary"
  - "content_item_readback_result"
  - "normalized_content_item_provider_evidence"
  - "content_item_read_certification_result"
  - "dependency_readiness_result"
  - "immutable_fsm_package"
  - "fsm_package_readiness_receipt"
  - "core_data_loader_handoff_result"
  - "item_catalog_fsm_handoff_result"
  - "verified_goal_fallback_readiness_receipt"
  - "proposal_fingerprint"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "hcm.hcm-tool.profile-management-content-library-configuration.item-catalogs"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.data-loader"
  - "core.fusion-api.rest-api-client"
oracle_supplied_guidance_files:
  - purpose: "Content Item input validation and supplied-configuration start nodes"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Content Item dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Exact current-evidence classification and registered read-only catalog lookups"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Content Item design enforcement"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-management-content-library-configuration/content-items/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-management-content-library-configuration/content-items/current/"
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
  - "May read an explicitly supplied local Content Items FSM export for sanitized schema and exact-comparison evidence."
  - "May create one project-local create-only Content Items FSM ZIP and sanitized readiness receipt after a separate package-preparation request."
  - "May use the standard read-only talentContentItemCatalogs REST resource and one registry-selected child relation through core.fusion-api.rest-api-client to collect exact duplicate or readback evidence."
  - "May hand one approved catalog-backed Enhanced Profile Content Item to Item Catalogs for its source-backed FSM package contract without calling Fusion."
  - "May route the exact package through core.data-loader after Task Hook validation; upload and initiation require the loader's separate immutable-preview approval."
required_privileges:
  - "View access to Content Items when live read-only evidence is requested."
  - "Content Items task CSV import, plus Fusion Documents upload privileges, for a separately approved core.data-loader execution."
  - "Read access to talentContentItemCatalogs and the registry-selected child relation for enhanced-profile duplicate and readback checks."
---

# Content Items Setup Task Guidance

## Purpose

Capture supplied item identities, translations, supported proficiency descriptions, dates, and relationships. Accept direct values, the blank requirements template, or a readable existing file; use the spreadsheet by default for repeating rows. Preserve every parent, child and relationship with exact source provenance and confirmed mappings. Do not discover business purpose, downstream consumers or workforce design, invent values, or infer omitted optional fields. Review remains non-executable.

Original GROW-8154 V1 acceptance permits only independently supported create-only FSM shapes. The separately selected verified GOAL exception is available through the authoritative Core Data Loader route; it is not FSM acceptance. Catalog flags and source graphs are not live acceptance proof.

## Setup Task Skill Contract

- task_code: `HRT_MANAGE_PROFILE_CONTENT_ITEMS`
- task_name: `Content Items`
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

Use this skill for supplied item identities, translations, supported proficiency descriptions, dates, and relationships. Users need not know Fusion task terminology; route from their actual object fields and confirmed mappings. Ask only for missing required configuration or an ambiguous mapping. Do not request a business-purpose restatement. Return the complete review set and a non-executable exact-check report when requested.

A separate package request prefers the supported FSM contract. The explicitly selected [verified GOAL fallback](../references/verified-fallback-contract.md) is available after its distinct evidence, lifecycle, complete-request and not-submitted gates. Never silently select HDL or substitute HSDL.

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

- Task name: `Content Items`
- Task code: `HRT_MANAGE_PROFILE_CONTENT_ITEMS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Catalog Support and Profile-Mode Route

An explicit FSM template or task-export request selects the existing export
workflow directly. Profile-mode and create-provider proof are needed when
interpreting evidence coverage or choosing an import, not merely to acquire
that task's template/export. Do not make evidence acquisition depend on the
proof the export is intended to supply.

`CSVExportImportSupportedFlag: Y`, `dataloader_import_mode: FSM`, and blank `businessObject` are catalog facts, not runtime certification.

1. Obtain current task evidence only through `shared.setup-export.task-level-export` or the separately selected registered read-only provider.
2. Validate setup and references using the shared validators. Resolve target profile mode before selecting a provider; release labels are not eligibility gates.
3. Legacy standalone FSM retains the parent exact package contract and Core Data Loader handoff.
4. Enhanced non-GOAL evidence requires an eligible registered context and complete declared child reads. A supported catalog-backed item may hand off to Item Catalogs under its independent lifecycle and unchanged one-parent/one-child FSM guards.
5. Enhanced standalone GOAL FSM remains blocked by the retained companion-document failure. Do not fabricate members; offer only the separately selected verified GOAL exception and preserve every gate.
6. `PROJECT` is catalog-backed Projects, not free-form `SPECIAL_PROJECT`. Explicit `SKILL` creation routes to the [controlled new-custom-catalog FSM contract](../item-catalogs/references/skill-catalog-creation.md), not historical HDL. `EDUCATIONAL_ESTABLISHMENT` retains its recorded provider/ownership blocker. Skills Center enablement and subscriptions remain separate from Skill catalog/item creation.
7. Keep update, delete, end-date, merging existing records, direct writes, unregistered reads, unsupported full sets and other HDL/HSDL fallbacks blocked. The selected verified single-row GOAL exception does not activate historical catalog or Competency HDL providers and never proves FSM acceptance.

In a route review, name the explicit context and its registered child relation,
then distinguish that declared route from current target evidence. Preserve
the registry's read limitations: a nullable ContentItemCode is not complete
row identity coverage, and empty owning catalogs do not certify positive-match
fields. An exact lookup must cover every owning catalog and required page.
For conditional Item Catalog creation, state both the global code collision
guard and the case-insensitive same-catalog Name guard, plus the unchanged
one-parent/one-child limit. Explain the current child eligibility alongside the
supplied values and identify missing required inputs by field name. A catalog
child requires an explicit `DateFrom` in `YYYY-MM-DD`; never fill it from today's
date. Supplier `C` must be explicitly supplied and validated, not
defaulted; `RatingModelCode` must be blank; rating-description rows, translations,
relationships and advanced/dynamic child fields are unsupported. Preserve any
such supplied values in the complete review and hold that package; do not drop
them or require package readiness merely to display a preliminary draft.

Apply the Item Catalog [export policy](../item-catalogs/references/optional-export-policy.md):
skip pre-import export and disclose unverified code/Name and parent comparisons.
Require the applicable owning Content Type evidence; the Item Catalog child
route does not use the legacy Content Items seed overlay. For SKILL, read the
[creation contract](../item-catalogs/references/skill-catalog-creation.md) before
handoff: only a new custom catalog with its portable children in the explicit
non-production new-set mode is enabled. Do not turn the historical HDL blocker
or uncertified positive REST match into a blanket FSM refusal. Do not claim
verified runtime support, create into an existing catalog, or configure Skills Center.

## Owned Scope

- Content item identity, supplied translations, and effective dates.
- Item-specific proficiency descriptions when the applicable type and Rating Model evidence are supplied.
- Content-item relationship endpoints and supplied relationship attributes.

Do not own Content Type creation, Item Catalog membership, behavior enablement on a Content Section, Rating Model changes, Profile Types, or profile instances.

## Phase-Conditional Read Order

The parent's phase-specific required inputs still apply. Load only the active phase:

- Template-only guidance: the parent [blank-template contract](../references/setup-guidance-template-contract.md); no environment or execution preflight.
- Preliminary proposal: the parent [supplied-configuration contract](../business-intent-contract.md) and [review-only proposal contract](../references/review-only-proposal-contract.md), [input validation](ora-resource/ora_input_validation.md), and [design enforcement](ora-resource/ora_design_enforcement.md). When normalizing supplied local input, read its capture resolver in [reference lookups](ora-resource/ora_reference_lookups.md). Retain unresolved fields visibly; no live evidence is required merely to show the preliminary review.
- Before task-node validation or execution: read the [task-node execution guide](../references/task-node-execution.md), then the [compiled registry](ora-resource/ora_rule_registry.json), validated task plan and reachable source anchors, including applicable [dependency readiness](ora-resource/ora_dependency_readiness.md) and [error handling](ora-resource/ora_error_handling.md). Select the declared branch; never skip a reached gate.
- Before any live read: also read the parent [environment preflight contract](../references/environment-preflight-contract.md); use only the selected workflow's client and checks.

For exact checks or separately requested package work, also read the selected branch:

- Exact-identifier review: [reference lookups](ora-resource/ora_reference_lookups.md) and [design enforcement](ora-resource/ora_design_enforcement.md); incomplete evidence blocks exact claims, not preliminary review.
- Registered REST read or readback branch: [reference lookups](ora-resource/ora_reference_lookups.md)
  and the [provider registry](references/content-item-rest-provider-registry.json),
  then the reference and design rules.
- Current FSM package branch: the reference and design rules plus the parent
  [create-only FSM import contract](../references/fsm-import-contract.md).
- Explicit verified GOAL fallback exception branch: the parent [fallback contract](../references/verified-fallback-contract.md), the [GOAL provider
  contract](references/content-item-goal-hdl-provider.json), parent [FSM
  evidence contract](../references/fsm-evidence-contract.md), reference and
  design rules, and the isolated GOAL package helper.
  In a fallback route or preparation response, distinguish an available candidate
  from an exception explicitly selected in the recorded request/project decision.
  Name the planned independent complete Content Items FSM readback and comparison
  of all four approved fields; an accepted load or receipt is not verification.
- Item Catalog FSM handoff branch: the [Item Catalog FSM provider registry](../item-catalogs/references/catalog-content-item-fsm-provider.json), parent [FSM evidence contract](../references/fsm-evidence-contract.md), and Item Catalogs package rules.
- Historical catalog HDL regression reference only (not a V1 route): the [catalog provider
  contract](references/content-item-catalog-hdl-provider.json), the unchanged historical
  `ora-resource/ora_rest_execution.md` document, reference and design rules,
  and `../scripts/prepare_catalog_content_item_hdl_package.py`.

The historical REST-execution document is not active guidance or an executable
V1 route. Current lookup mechanics belong only to `ora_reference_lookups.md`
and its registered Task Nodes; historical HDL lifecycle records do not authorize
current FSM creation or duplicate reuse.

## Preflight

Guidance and blank-template generation require no Fusion access, target, release, lookup, credentials, completed requirements, or approval. Intake captures supplied configuration through the three input choices, records exact source provenance, confirms mappings and preserves omitted optional values. Do not discover comparable configurations or invent defaults.

Exact classification additionally requires complete fresh structured same-target evidence under the selected provider's supported identifier semantics. Display actual matched identifiers and stop creation on any exact match, including equal values. Do not produce generic fuzzy or near-match recommendations. Preserve real provider Name/code collision guards.

For legacy FSM, the source-declared item identity is ContextName plus Name,
with ContentItemCode retained as a separate collision guard. A different code
does not make an existing Name new. Relationship identity is its resolved
endpoint pair, not RelationshipCode. Supplied endpoint aliases must agree and
legacy item/relationship packages require explicit DateFrom; no current-date
default is approved. Enhanced catalog routes retain their distinct registered
semantics. Source-backed local validation is not deployed-provider acceptance.

A live phase uses the parent operation-scoped preflight: the owning FSM export or Core Data Loader workflow supplies its task-specific checks; only registered Content Items REST reads require the bounded REST capability receipt. Unknown quarterly metadata does not block local review or eligible evidence acquisition. Release labels never gate classification, availability, packaging or execution; preserve actual provider/schema checks and never replace target evidence with screenshots or attestations.

Package preparation additionally requires a separately approved complete proposal, exact provider-row fingerprint, fresh same-task baseline, all declared exact dependencies, target bindings and safe project-local output paths. Unsupported rows remain in the review set with blockers; never trim the set to make an executable package appear complete.

Legacy FSM and the independently registered one-parent/one-child Item Catalog FSM handoff retain their exact provider gates. Enhanced standalone GOAL FSM remains blocked by the retained companion-document failure; non-GOAL rows are rejected by that standalone provider. The explicitly selected verified GOAL exception is available under its own contract; other HDL helpers remain inactive. Exception evidence never establishes FSM-only acceptance.

## Proposal Workflow

1. Start at `CI.CAPTURE_CONFIGURATION`; capture direct values, blank-template rows, or a readable existing file.
2. Preserve the complete supplied parent/child/relationship set, source references and mappings. Ask for missing required values or ambiguous mappings only.
3. Leave omitted optional fields omitted. Validate conditional descriptions, translations and dates only when supported and applicable.
4. Normalize confirmed mappings without creating dependencies or designing nearby objects.
5. Use only complete current evidence under exact provider semantics. Display matched identifiers and block creation on any exact match or collision; never recommend reuse.
6. Retain unsupported rows and exact evidence gaps in one review-only set. Enforce ownership and no-update/delete/merge boundaries.
7. Fingerprint the complete review. Terminate at `CI.RETURN_PROPOSAL`, `CI.RETURN_EXACT_DUPLICATE`, or a precise blocker. Proposal confirmation never authorizes execution.

## Local Evidence Foundation

When an already exported ZIP is supplied, use the parent [FSM evidence and exact-comparison contract](../references/fsm-evidence-contract.md). The local helper validates Content Item and relationship CSVs, checks the fresh customer layer before `../assets/seeded-content-items/`, resolves owning seeded Content Type rules from `../assets/seeded-content-types/`, enforces source-required fields and applicable dynamic fields, validates Rating Model evidence and relationship endpoints, and can compare a later same-target item readback. The seed catalogs are evidence only and are never provider rows or import payloads.

Approved item-specific proficiency descriptions may be retained in a
review-only proposal. Their provider rows, package construction, import, and
readback remain blocked until the provider-owned CSV and readback fields are
proven. For supported item and relationship rows, use
`../scripts/prepare_profile_content_library_fsm_package.py` under the parent
[FSM import contract](../references/fsm-import-contract.md). The builder
requires exact provider fields and dependency evidence, preserves
export-derived metadata, and blocks existing keys and generated identifiers.

## Create-Only Import Workflow

1. Complete and fingerprint one review set; terminate the proposal run.
2. Prefer a supported legacy FSM or independent Item Catalog FSM route using fresh authenticated profile-mode and applicable capability evidence. For enhanced GOAL, an explicitly selected verified fallback must first pass CI.VALIDATE_GOAL_FALLBACK and the complete [exception contract](../references/verified-fallback-contract.md); strict FSM-only remains held.
3. Bind the full current same-task evidence, dependencies, duplicate locks, exact provider rows and reviewed baseline. Do not omit unsupported supplied rows to imply full-set readiness.
4. Legacy FSM retains all Content Type, Rating Model, supplier, seeded, dynamic-field and relationship guards. The Item Catalog route retains one exact unchanged parent anchor, one eligible child, all Name/code locks, an empty rating-description member and no advanced fields.
5. Build and reopen the deterministic immutable ZIP using the owning task builder. Item Catalogs owns its Task Hook identity, archive and parent-no-drift readback. Stop at `package_ready_for_core_data_loader_preview`.
6. Use `core.data-loader` for Task Hook, immutable preview, authoritative approval, upload and initiation. The historical catalog HDL branch remains unreachable. CI.RESOLVE_GOAL_HDL_EVIDENCE is reachable only through explicit verified fallback selection; it reopens supplied FSM evidence locally and cannot upload or approve a load.
7. Capture accepted IDs, terminal status and ProcessLog through the allowed status workflow. Independently read back the complete supported set; for catalog children also verify parent no drift and duplicate-create refusal. No blind retry, repair, cleanup or automatic resubmission.

## Refusal Rules

Refuse missing Content Types, unresolved profile mode, invalid dates, unresolved endpoints or catalogs, unregistered selectors, partial/stale/wrong-target evidence, exact keys or provider Name/code collisions, missing source-required fields, invented values, unsupported objects, update/delete/merge/end-date, and routes bypassing the task contract or Core Data Loader. Retain supplied proficiency descriptions and relationships as blocked review rows until their exact provider/readback contract is proven. Standalone enhanced FSM remains blocked; a separately eligible Item Catalog FSM handoff does not broaden that provider. Only the explicitly selected verified GOAL exception may use HDL. No generic HDL/HSDL fallback, unverified provider, trimmed full set or automatic failover after submitted/unknown mutation is allowed. Proposal/package confirmation is not submission approval.

## Failure Handling

Classify and stop on invalid input, unavailable evidence, catalog or metadata
mismatch, authentication, authorization, transport/environment, Fusion API,
artifact persistence, process, or approval failures as defined in [error
handling](ora-resource/ora_error_handling.md). Retry only a read-only transport
failure within the documented bound and allow only the core client's one
managed cached-token refresh. Never retry, auto-correct, resubmit, upload, or
initiate a package after a failure.

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
Management SME plus an FSCR A-Team/core reviewer, with automation and QA review
for the guarded FSM and ContentItem V2 HDL paths. A certification-only
lifecycle is not a claim that the provider is production-ready.

## Implementation Notes

Use the parent skill for complete-set integrity. The standalone Content Items provider rejects enhanced non-GOAL rows and the retained enhanced GOAL package fails its companion-document transformation; neither failure alone authorizes another provider. Item Catalog base children are part of the root graph, which commits before translation handling. The registered adapter owns read-only evidence and the owning FSM builder owns package shape. Only the explicitly selected verified GOAL exception may use its isolated HDL helper; historical Competency and catalog HDL helpers remain inactive. Fallback evidence never certifies FSM. Every supported future row still requires fresh exact evidence, an immutable package, Task Hook validation, Core Data Loader authority and independent readback. Track project token usage.

## Historical HDL Certification Automation (Not V1)

For historical regression review only, `../scripts/catalog_content_item_certification.py` was used to create a durable
local plan for all `certification-only` catalog contexts, prove a duplicate
lock from a fresh exact-collision receipt, and prepare a review-only lifecycle
promotion proposal. The helper is intentionally local-only: it neither calls
Fusion nor uploads/retries a package or edits the provider contract. Its
post-load readback stage always routes through the unfiltered Item Catalog task
`ORA_MANAGE_PROFILE_ITEM_CATALOG`, whose required members are
`ORA_TALENT_PROFILE_ITEM_CATALOG.csv`, `ORA_TALENT_CATALOG_CONTENT_ITEM.csv`,
and `ORA_TALENT_CATALOG_CONTENT_ITEM_RDESC.csv`; do not substitute the Content
Items export task. A provider becomes `verified` only after the existing
approved Data Loader path, both readbacks, duplicate-lock proof, and a separate
reviewed source change to the provider contract.

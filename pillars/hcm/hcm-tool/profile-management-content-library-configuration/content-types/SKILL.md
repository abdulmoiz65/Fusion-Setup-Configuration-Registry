---
skill_id: "hcm.hcm-tool.profile-management-content-library-configuration.content-types"
name: "Content Types Setup Task Guidance"
description: "Captures supplied Content Types configuration from direct values, a blank requirements template, or a readable existing file; preserves complete-set provenance, exact duplicate reporting, and supported V1 FSM boundaries."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Profile Management Content Library Configuration"
functional_area_code: "CUSTOM_TALENT_PROFILE_CONTENT_LIBRARY"
task_code: "HRT_MANAGE_PROFILE_CONTENT_TYPES"
task_name: "Content Types"
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
version: "0.8.3"
inputs:
  - "supplied_configuration_objects_and_values"
  - "direct_values_blank_template_or_readable_existing_file"
  - "source_provenance_and_confirmed_mappings"
  - "conditional_supported_dates_descriptions_and_translations"
  - "template_guidance_checklist_or_example_request"
  - "expert_task_scope_or_explicit_content_type_values"
  - "project_context"
  - "normalized_task_request"
  - "approved_content_type_values"
  - "current_task_evidence"
  - "validated_seeded_content_type_catalog"
  - "approved_create_only_provider_rows"
  - "approved_provider_rows_fingerprint"
  - "fresh_package_baseline"
outputs:
  - "supplied_object_routing_result"
  - "setup_guidance_or_blank_template_result"
  - "assumption_ledger"
  - "fusion_environment_capability_result"
  - "content_type_review_proposal"
  - "exact_match_result"
  - "non_executable_exact_check_report"
  - "sanitized_fsm_evidence_summary"
  - "content_type_graph_readback_result"
  - "dependency_readiness_result"
  - "immutable_fsm_package"
  - "fsm_package_readiness_receipt"
  - "core_data_loader_handoff_result"
  - "proposal_fingerprint"
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
  - purpose: "Content Type input validation and supplied-configuration start nodes"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Content Type dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Exact current-evidence classification"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Content Type design enforcement"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-management-content-library-configuration/content-types/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-management-content-library-configuration/content-types/current/"
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
  - "May read an explicitly supplied local Content Types FSM export for sanitized schema and exact-comparison evidence."
  - "May create one project-local create-only Content Types FSM ZIP and sanitized readiness receipt after a separate package-preparation request."
  - "May route the exact package through core.data-loader after Task Hook validation; upload and initiation require the loader's separate immutable-preview approval."
required_privileges:
  - "View access to Content Types when live read-only evidence is requested."
  - "Content Types task CSV import and Fusion Documents upload privileges for a separately approved core.data-loader execution."
---

# Content Types Setup Task Guidance

## Purpose

Capture supplied content type identities, properties, and relationships. Accept direct values, the blank requirements template, or a readable existing file; use the spreadsheet by default for repeating rows. Preserve every parent, child and relationship with exact source provenance and confirmed mappings. Do not discover business purpose, downstream consumers or workforce design, invent values, or infer omitted optional fields. Review remains non-executable.

Current GROW-8154 V1 permits only the independently supported create-only FSM shape through the authoritative Core Data Loader route. Catalog flags and source graphs are not live acceptance proof.

## Setup Task Skill Contract

- task_code: `HRT_MANAGE_PROFILE_CONTENT_TYPES`
- task_name: `Content Types`
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

Use this skill for supplied content type identities, properties, and relationships. Users need not know Fusion task terminology; route from their actual object fields and confirmed mappings. Ask only for missing required configuration or an ambiguous mapping. Do not request a business-purpose restatement. Return the complete review set and a non-executable exact-check report when requested.

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

- Task name: `Content Types`
- Task code: `HRT_MANAGE_PROFILE_CONTENT_TYPES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## Catalog Support and Import Route

`CSVExportImportSupportedFlag` is `Y` and `dataloader_import_mode` is generated as `FSM`. These are catalog facts, not GROW-8154 execution authorization.

1. Export current task data read-only with `shared.setup-export.task-level-export`.
2. Validate supplied or exported data with `shared.validation.setup-data-validator`.
3. Validate referenced data with `shared.validation.reference-data-validator`.
4. For an approved create-only package, use the parent FSM import contract and route the final immutable ZIP only through `core.data-loader`.
5. Keep update, merge, delete, end-date, direct REST, HDL, HSDL, and alternate providers blocked.

Use this task metadata when invoking those skills:

- Offering: `HCM Tool`
- Functional area / Setup Object: `Profile Management Content Library Configuration`
- Setup task name: `Content Types`
- Setup task code: `HRT_MANAGE_PROFILE_CONTENT_TYPES`




## Owned Scope

- Content type identity and supplied translations.
- Source-backed content type properties.
- Content type relationship endpoints and supplied relationship attributes.

Do not own content items, catalog membership, qualifier sets, schools, Rating Models, Profile Types, Content Sections, or profile instances.

## Required Read Order

1. Parent [supplied-configuration contract](../business-intent-contract.md).
2. Parent [setup-guidance and blank-template contract](../references/setup-guidance-template-contract.md) when guidance or a blank intake artifact is requested.
3. Parent [environment preflight contract](../references/environment-preflight-contract.md) for any Fusion-touching phase.
4. [Task-node execution guide](../references/task-node-execution.md) when selecting or executing task nodes.
5. [Compiled registry](ora-resource/ora_rule_registry.json): select the requested phase, its nodes and reachable source anchors only.
6. Read the selected anchors in [input validation](ora-resource/ora_input_validation.md), [dependency readiness](ora-resource/ora_dependency_readiness.md), [reference lookups](ora-resource/ora_reference_lookups.md), [design enforcement](ora-resource/ora_design_enforcement.md), and [error handling](ora-resource/ora_error_handling.md) when reached by that phase. These are anchor sources, not an instruction to read every resource for template-only work.
7. Parent [create-only FSM import contract](../references/fsm-import-contract.md) when package preparation or import is requested.

## Preflight

Guidance and blank-template generation require no Fusion access, target, release, lookup, credentials, completed requirements, or approval. Intake captures supplied configuration through the three input choices, records exact source provenance, confirms mappings and preserves omitted optional values. Do not discover comparable configurations or invent defaults.

Exact classification additionally requires complete fresh structured same-target evidence under the selected provider's supported identifier semantics. Display actual matched identifiers and stop creation on any exact match, including equal values. Do not produce generic fuzzy or near-match recommendations. Preserve real provider Name/code collision guards.

A live phase uses the parent operation-scoped preflight: the owning FSM export or Core Data Loader workflow supplies its task-specific checks; only registered Content Items REST reads require the bounded REST capability receipt. Unknown quarterly metadata does not block local review or eligible evidence acquisition. Release labels never gate classification, availability, packaging or execution; preserve actual provider/schema checks and never replace target evidence with screenshots or attestations.

Package preparation additionally requires a separately approved complete proposal, exact provider-row fingerprint, fresh same-task baseline, all declared exact dependencies, target bindings and safe project-local output paths. Unsupported rows remain in the review set with blockers; never trim the set to make an executable package appear complete.

## Proposal Workflow

1. Start at `CT.CAPTURE_CONFIGURATION`; capture direct values, blank-template rows, or a readable existing file.
2. Preserve the complete supplied parent/child/relationship set, source references and mappings. Ask for missing required values or ambiguous mappings only.
3. Leave omitted optional fields omitted. Validate conditional descriptions, translations and dates only when supported and applicable.
4. Normalize confirmed mappings without creating dependencies or designing nearby objects.
5. Use only complete current evidence under exact provider semantics. Display matched identifiers and block creation on any exact match or collision; never recommend reuse.
6. Retain unsupported rows and exact evidence gaps in one review-only set. Enforce ownership and no-update/delete/merge boundaries.
7. Fingerprint the complete review. Terminate at `CT.RETURN_PROPOSAL`, `CT.RETURN_EXACT_DUPLICATE`, or a precise blocker. Proposal confirmation never authorizes execution.

## Local Evidence Foundation

When an already exported ZIP is supplied, use the parent [FSM evidence and exact-comparison contract](../references/fsm-evidence-contract.md). The local helper validates the header, property, and relationship CSV graph; reads the fresh customer layer first; then overlays the integrity-validated `../assets/seeded-content-types/` catalog. Fresh rows override the same seeded provider key. The helper requires approved property combinations, refuses guessed provider-derived fields, and can compare a later same-target readback graph. The seed catalog is local evidence only and is never an import payload.

This evidence capability remains read-only. For a separate create-only package
run, use `../scripts/prepare_profile_content_library_fsm_package.py` under the
parent [FSM import contract](../references/fsm-import-contract.md). The builder
requires every provider field explicitly, preserves export-derived metadata,
and blocks existing keys and generated identifiers.

## Create-Only FSM Import Workflow

1. Finish and fingerprint the review proposal; terminate the proposal run.
2. On a separate package request, validate the fresh unfiltered same-target
   customer layer, integrity-validated seeded catalog, approved
   property/dependency evidence, and a fresh same-task baseline.
3. Build and reopen one deterministic project-local FSM ZIP; stop at
   `package_ready_for_core_data_loader_preview`.
4. Start a separate `core.data-loader` run for the exact package. Task Hook must
   execute this task's compiled import branch and bind its preview to the same
   archive SHA-256.
5. Apply Core Data Loader's authoritative approval policy to the exact immutable preview. Use auto-approval only when that policy's explicit authority and binding requirements pass; otherwise hold for the scoped submission approval.
6. Verify through a fresh same-target export when the user later requests
   status/readback; never auto-correct a mismatch.

## Refusal Rules

Refuse missing identities, invalid properties, unresolved relationship endpoints, filtered or target-mismatched current evidence, missing/stale/tampered seed catalogs, multiple exact matches, business-design invention, another skill's scope, update/merge/delete/end-date, or any route that bypasses the create-only FSM contract and `core.data-loader`. Proposal or package confirmation never authorizes Data Loader submission.

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
for this hybrid import path.

## Implementation Notes

Use the parent functional-area skill `hcm.hcm-tool.profile-management-content-library-configuration` for scope proposals and complete-set integrity. A header-only task export remains insufficient alone; when it is attested as an unfiltered customer layer, the 26C seeded catalog supplies the omitted Oracle reference model for exact classification. Track token usage for generated project artifacts using the manifest policy.

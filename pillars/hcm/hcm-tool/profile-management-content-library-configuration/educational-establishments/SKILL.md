---
skill_id: "hcm.hcm-tool.profile-management-content-library-configuration.educational-establishments"
name: "Educational Establishments Setup Task Guidance"
description: "Captures supplied Educational Establishments configuration from direct values, a blank requirements template, or a readable existing file; preserves complete-set provenance, exact duplicate reporting, and supported V1 FSM boundaries."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Profile Management Content Library Configuration"
functional_area_code: "CUSTOM_TALENT_PROFILE_CONTENT_LIBRARY"
task_code: "HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS"
task_name: "Educational Establishments"
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
version: "0.6.3"
inputs:
  - "supplied_configuration_objects_and_values"
  - "direct_values_blank_template_or_readable_existing_file"
  - "source_provenance_and_confirmed_mappings"
  - "conditional_supported_dates_descriptions_and_translations"
  - "template_guidance_checklist_or_example_request"
  - "expert_task_scope_or_explicit_educational_establishment_values"
  - "project_context"
  - "normalized_task_request"
  - "approved_educational_establishment_values"
  - "current_task_evidence"
  - "approved_create_only_provider_rows"
  - "approved_provider_rows_fingerprint"
  - "fresh_package_baseline"
outputs:
  - "supplied_object_routing_result"
  - "setup_guidance_or_blank_template_result"
  - "assumption_ledger"
  - "fusion_environment_capability_result"
  - "educational_establishment_review_proposal"
  - "exact_match_result"
  - "non_executable_exact_check_report"
  - "sanitized_fsm_evidence_summary"
  - "educational_establishment_readback_result"
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
  - purpose: "Educational Establishments proposal input validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Educational Establishments dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Exact current-evidence classification"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Educational Establishments design enforcement"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-management-content-library-configuration/educational-establishments/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-management-content-library-configuration/educational-establishments/current/"
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
  - "May read an explicitly supplied local Educational Establishments FSM export for sanitized schema and exact-comparison evidence."
  - "May create one project-local create-only Educational Establishments FSM ZIP and sanitized readiness receipt after a separate package-preparation request."
  - "May route the exact package through core.data-loader after Task Hook validation; upload and initiation require the loader's separate immutable-preview approval."
required_privileges:
  - "View and export access to Educational Establishments when live read-only evidence is requested."
  - "Educational Establishments task CSV import and Fusion Documents upload privileges for a separately approved core.data-loader execution."
---

# Educational Establishments Setup Task Guidance

## Purpose

Capture supplied school, college, university, and other establishment reference values. Accept direct values, the blank requirements template, or a readable existing file; use the spreadsheet by default for repeating rows. Preserve every parent, child and relationship with exact source provenance and confirmed mappings. Do not discover business purpose, downstream consumers or workforce design, invent values, or infer omitted optional fields. Review remains non-executable.

Current GROW-8154 V1 permits only the independently supported create-only FSM shape through the authoritative Core Data Loader route. Catalog flags and source graphs are not live acceptance proof.

## Setup Task Skill Contract

- task_code: `HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS`
- task_name: `Educational Establishments`
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

Use this skill for supplied school, college, university, and other establishment reference values. Users need not know Fusion task terminology; route from their actual object fields and confirmed mappings. Ask only for missing required configuration or an ambiguous mapping. Do not request a business-purpose restatement. Return the complete review set and a non-executable exact-check report when requested.

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

- Task name: `Educational Establishments`
- Task code: `HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS`
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
5. Keep update, merge, delete, end-date, direct REST, browser automation, HDL, HSDL, and alternate providers blocked.

Use this task metadata when invoking those skills:

- Offering: `HCM Tool`
- Functional area / Setup Object: `Profile Management Content Library Configuration`
- Setup task name: `Educational Establishments`
- Setup task code: `HRT_MANAGE_EDUCATIONAL_ESTABLISHMENTS`




## Owned Scope

- Educational-establishment identity and approved controlled reference values.

Do not own employee education records, degrees or fields of study, Content Items, Rating Models, Profile Types, Content Sections, profile instances, update/delete/end-date operations, or generic FSM transport. Package construction is owned only for the task-specific create-only contract; all transport remains owned by `core.data-loader`.

## Required Read Order

1. Parent [supplied-configuration contract](../business-intent-contract.md).
2. Parent [setup-guidance and blank-template contract](../references/setup-guidance-template-contract.md) when guidance or a blank intake artifact is requested.
3. Parent [environment preflight contract](../references/environment-preflight-contract.md) for any Fusion-touching phase.
4. [Task-node execution guide](../references/task-node-execution.md).
5. [Compiled registry](ora-resource/ora_rule_registry.json).
6. [Input validation](ora-resource/ora_input_validation.md).
7. [Dependency readiness](ora-resource/ora_dependency_readiness.md).
8. [Reference lookups](ora-resource/ora_reference_lookups.md).
9. [Design enforcement](ora-resource/ora_design_enforcement.md).
10. [Error handling](ora-resource/ora_error_handling.md).
11. Parent [create-only FSM import contract](../references/fsm-import-contract.md) when package preparation or import is requested.

## Preflight

Guidance and blank-template generation require no Fusion access, target, release, lookup, credentials, completed requirements, or approval. Intake captures supplied configuration through the three input choices, records exact source provenance, confirms mappings and preserves omitted optional values. Do not discover comparable configurations or invent defaults.

Exact classification additionally requires complete fresh structured same-target evidence under the selected provider's supported identifier semantics. Display actual matched identifiers and stop creation on any exact match, including equal values. Do not produce generic fuzzy or near-match recommendations. Preserve real provider Name/code collision guards.

A live phase uses the parent operation-scoped preflight and this task's declared FSM route. Check authenticated target, exact TaskCode, CSV support, privileges, data handling and required approval. Missing quarterly metadata or a Content Items REST capability receipt is not a blocker for this task. Never substitute screenshots or user attestations for actual target evidence.

Package preparation additionally requires a separately approved complete proposal, exact provider-row fingerprint, fresh same-task baseline, all declared exact dependencies, target bindings and safe project-local output paths. Unsupported rows remain in the review set with blockers; never trim the set to make an executable package appear complete.

## Proposal Workflow

1. Start at `EE.CAPTURE_CONFIGURATION`; capture direct values, blank-template rows, or a readable existing file.
2. Preserve the complete supplied parent/child/relationship set, source references and mappings. Ask for missing required values or ambiguous mappings only.
3. Leave omitted optional fields omitted. Validate conditional descriptions, translations and dates only when supported and applicable.
4. Normalize confirmed mappings without creating dependencies or designing nearby objects.
5. Use only complete current evidence under exact provider semantics. Display matched identifiers and block creation on any exact match or collision; never recommend reuse.
6. Retain unsupported rows and exact evidence gaps in one review-only set. Enforce ownership and no-update/delete/merge boundaries.
7. Fingerprint the complete review. Terminate at `EE.RETURN_PROPOSAL`, `EE.RETURN_EXACT_DUPLICATE`, or a precise blocker. Proposal confirmation never authorizes execution.

## Local Evidence Foundation

When an already exported ZIP is supplied, use the parent [FSM evidence and exact-comparison contract](../references/fsm-evidence-contract.md). The local helper validates `HRT_SCHOOL.csv`, enforces explicit geography pairs, matches only exact `SchoolCode`, does not produce generic normalized-name/location similarity warnings, keeps generated IDs out of the business comparison, and can compare a later same-target readback.

The evidence capability remains read-only. For a separate create-only package
run, use `../scripts/prepare_profile_content_library_fsm_package.py` under the
parent [FSM import contract](../references/fsm-import-contract.md). The new
shared builder supersedes the deferred task-only prototype, preserves
export-derived metadata, enforces the approved geography and generated-ID
rules, and has no Fusion connectivity.

## Proposal and Execution Separation

`EE.RETURN_PROPOSAL` is terminal. Proposal review cannot construct a ZIP or authorize a create/import route. A separate explicit package run may build the create-only ZIP. Package readiness then routes to a separate Core Data Loader preview and never authorizes submission.

## Create-Only FSM Import Workflow

1. Finish and fingerprint the review proposal; terminate the proposal run.
2. On a separate package request, validate the approved value authority,
   complete fresh same-target evidence, and a same-task package baseline.
3. Build and reopen one deterministic project-local FSM ZIP; stop at
   `package_ready_for_core_data_loader_preview`.
4. Start a separate `core.data-loader` run for the exact package. Task Hook must
   execute this task's compiled import branch and bind its preview to the same
   archive SHA-256.
5. Apply Core Data Loader's authoritative approval policy to the exact immutable preview. Use auto-approval only when that policy's explicit authority and binding requirements pass; otherwise hold for the scoped submission approval.
6. Verify through a fresh same-target export when the user later requests
   status/readback; never auto-correct a mismatch.

## Refusal Rules

Refuse missing identity, stale or incomplete evidence, multiple exact matches, employee education-record changes, another skill's scope, update/merge/delete/end-date rows, or any import/write route that bypasses the create-only FSM contract and `core.data-loader`. Proposal or package confirmation never authorizes Data Loader submission.

## Error and Diagnostics Contract

Classify failures as `input_validation`, `catalog_or_metadata_mismatch`, `authorization_or_privilege`, `transport_or_environment`, `process_timeout`, `process_failed`, `artifact_persistence`, or `approval_blocker`.

Persist only sanitized source references, evidence fingerprints, non-sensitive normalized values, exact-match results, proposal/preview fingerprints, lifecycle status, and one safe next action. Never persist source documents, credentials, tokens, private keys, employee data, customer-sensitive values, full existing export rows, base64 content, metadata audit identities, or sensitive environment endpoints.

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

Use the parent skill for scope proposals and complete-set integrity. The current export evidence supports exact current-state comparison; package construction additionally binds that fresh evidence, the reviewed baseline, and proposal fingerprint into one immutable readiness receipt. Track token usage for generated project artifacts using the manifest policy.

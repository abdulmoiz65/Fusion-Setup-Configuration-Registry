---
skill_id: "hcm.hcm-tool.profile-management-content-library-configuration.instance-qualifiers"
name: "Instance Qualifiers Setup Task Guidance"
description: "Captures supplied Instance Qualifiers configuration from direct values, a blank requirements template, or a readable existing file; preserves complete-set provenance, exact duplicate reporting, and supported V1 FSM boundaries."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Profile Management Content Library Configuration"
functional_area_code: "CUSTOM_TALENT_PROFILE_CONTENT_LIBRARY"
task_code: "HRT_MANAGE_INSTANCE_QUALIFIERS"
task_name: "Instance Qualifiers"
parent_skill_id: "hcm.hcm-tool.profile-management-content-library-configuration"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM hcm tool pillar team"
version: "0.5.3"
inputs:
  - "supplied_configuration_objects_and_values"
  - "direct_values_blank_template_or_readable_existing_file"
  - "source_provenance_and_confirmed_mappings"
  - "conditional_supported_dates_descriptions_and_translations"
  - "template_guidance_checklist_or_example_request"
  - "expert_task_scope_or_explicit_instance_qualifier_values"
  - "project_context"
  - "normalized_task_request"
  - "approved_instance_qualifier_values"
  - "current_task_evidence"
outputs:
  - "supplied_object_routing_result"
  - "setup_guidance_or_blank_template_result"
  - "assumption_ledger"
  - "fusion_environment_capability_result"
  - "instance_qualifier_review_proposal"
  - "provider_contract_diagnosis"
  - "profile_types_readback_handoff"
  - "exact_match_result"
  - "non_executable_exact_check_report"
  - "dependency_readiness_result"
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
oracle_supplied_guidance_files:
  - purpose: "Instance Qualifier input validation and supplied-configuration start nodes"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Instance Qualifier field and dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Exact current-evidence classification"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Instance Qualifier design enforcement"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-management-content-library-configuration/instance-qualifiers/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/profile-management-content-library-configuration/instance-qualifiers/current/"
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
  - "May request a routed read-only standalone task export only to diagnose provider capability."
  - "May hand off a read-only Profile Types export request to the owning skill for exact current evidence."
required_privileges:
  - "View access to Instance Qualifiers when live read-only evidence is requested."
---

# Instance Qualifiers Setup Task Guidance

## Purpose

Capture supplied qualifier-set identities and qualifier rows. Accept direct values, the blank requirements template, or a readable existing file; use the spreadsheet by default for repeating rows. Preserve every parent, child and relationship with exact source provenance and confirmed mappings. Do not discover business purpose, downstream consumers or workforce design, invent values, or infer omitted optional fields. Review remains non-executable.

The standalone provider is disabled. Containing Profile Types evidence does not authorize qualifier mutation or an invasive Profile Types import.

## Setup Task Skill Contract

- task_code: `HRT_MANAGE_INSTANCE_QUALIFIERS`
- task_name: `Instance Qualifiers`
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

Use this skill for supplied qualifier-set identities and qualifier rows. Users need not know Fusion task terminology; route from their actual object fields and confirmed mappings. Ask only for missing required configuration or an ambiguous mapping. Do not request a business-purpose restatement. Return the complete review set and a non-executable exact-check report when requested.

Keep creation blocked and obtain containing evidence only through the separately owned Profile Types workflow.

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

- Task name: `Instance Qualifiers`
- Task code: `HRT_MANAGE_INSTANCE_QUALIFIERS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: catalog-declared, but standalone 26C route is non-executable
- Data Loader import mode: `FSM`
- Business Object: ``

## Catalog Support and V1 Route

`CSVExportImportSupportedFlag` is `Y` and `dataloader_import_mode` is generated
as `FSM`. These remain catalog facts, but they do not describe an executable
standalone provider in Fusion 26C.

The release source and the retained live failure establish the operational
contract:

1. Since 21A, Fusion exports qualifier sets as children of Profile Type
   Sections in the Profile Types migration object. The standalone migration
   service forces an empty export selection and its import implementation is
   disabled.
2. A standalone data or template export that contains only
   `ASM_SETUP_CSV_METADATA.xml` and reports unavailable column information is a
   catalog-capability mismatch. Do not retry it and do not interpret it as an
   empty configuration.
3. Use the source-backed Profile Types view contract for proposal fields and
   exact identity. Obtain current/readback evidence only through a separately
   routed read-only `HRT_MANAGE_PROFILE_TYPES` export owned by
   `hcm.hcm-tool.profile-types-and-content-section-configuration`.
4. The peer Profile Types skill declares a separately governed Instance Data
   Export through `shared.setup-export.task-level-export`; this is not proof of
   complete qualifier-specific contents or an approved qualifier create executor.
   This child remains review-only for mutation and must not invoke
   `core.data-loader`, FSM import, HDL, HSDL, REST mutation, browser automation,
   or another provider.

Use this task metadata when invoking those skills:

- Offering: `HCM Tool`
- Functional area / Setup Object: `Profile Management Content Library Configuration`
- Setup task name: `Instance Qualifiers`
- Setup task code: `HRT_MANAGE_INSTANCE_QUALIFIERS`




## Owned Scope

- Instance qualifier-set identity.
- Supplied qualifier rows and their parent-child integrity.

Do not own Content Types, Content Items, Item Catalogs, Rating Models, Profile
Type design, Content Section design, or profile-instance assignments. A
Profile Types export is a technical containment handoff for evidence only; it
does not transfer those design responsibilities into this skill.

## Fusion 26C Source-Backed Contract

| Contract area | Source-backed value |
|---|---|
| Standalone lifecycle | QualifierSetMigrationAMImpl documents that qualifier sets moved under Profile Type Sections in 21A; standalone import logic is disabled |
| Set exact identity | QualifierSetCode, ProfileTypeCode, ContextName, SectionContext |
| Set proposal fields | Description, QualifierSetCode, QualifierTypeCode, KeyTableName, ProfileTypeCode, ContextName, SectionContext |
| Qualifier exact identity | Set exact identity plus QualifierCode |
| Qualifier proposal fields | QualifierCode, Description, QualifierSeqNumber, EmpViewFlag, EmpDefFlag, MgrViewFlag, MgrDefFlag, SearchFlag |
| Qualifier type values | P means prompt or key-table sourced; Q means selected qualifier rows. Preserve an approved value and never infer it from the business name alone |
| Excluded technical fields | Surrogate IDs, BusinessGroupId, ContentTypeId, SectionId, ProfileTypeId, audit fields, and object version values are not user proposal fields |

The corresponding source files are under
`fusionapps/hcm/components/hcmCoreSetup/profiles/setup/qualifierSetService`,
`fusionapps/hcm/components/hcmCoreSetup/profiles/setup/profileTypeService`, and
`fusionapps/hcm/hrt/db/data/HcmProfileTop`. Oracle's current Instance Qualifier
Sets guidance supplies the business meaning of priority, employee/manager
visibility, search inclusion, and defaults. These sources establish proposal
and comparison semantics only; they do not authorize persistence.

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

## Preflight

Guidance and blank-template generation require no Fusion access, target, release, lookup, credentials, completed requirements, or approval. Intake captures supplied configuration through the three input choices, records exact source provenance, confirms mappings and preserves omitted optional values. Do not discover comparable configurations or invent defaults.

Exact classification additionally requires complete fresh structured same-target evidence under the selected provider's supported identifier semantics. Display actual matched identifiers and stop creation on any exact match, including equal values. Do not produce generic fuzzy or near-match recommendations. Preserve real provider Name/code collision guards.

A live phase uses the parent operation-scoped preflight: the owning FSM export or Core Data Loader workflow supplies its task-specific checks; only registered Content Items REST reads require the bounded REST capability receipt. Unknown quarterly metadata does not block local review or eligible evidence acquisition. Release labels never gate classification, availability, packaging or execution; preserve actual provider/schema checks and never replace target evidence with screenshots or attestations.

The standalone provider is unavailable. Keep exact absence claims blocked until complete current containing Profile Types evidence is obtained through its owning workflow. No qualifier import, loader, or invasive containing import is authorized.

## Proposal Workflow

1. Start at `IQ.CAPTURE_CONFIGURATION`; capture direct values, blank-template rows, or a readable existing file.
2. Preserve the complete supplied parent/child/relationship set, source references and mappings. Ask for missing required values or ambiguous mappings only.
3. Leave omitted optional fields omitted. Validate conditional descriptions, translations and dates only when supported and applicable.
4. Normalize confirmed mappings without creating dependencies or designing nearby objects.
5. Use only complete current evidence under exact provider semantics. Display matched identifiers and block creation on any exact match or collision; never recommend reuse.
6. Retain unsupported rows and exact evidence gaps in one review-only set. Enforce ownership and no-update/delete/merge boundaries.
7. Fingerprint the complete review. Terminate at `IQ.RETURN_PROPOSAL`, `IQ.RETURN_EXACT_DUPLICATE`, or a precise blocker. Proposal confirmation never authorizes execution.

## Refusal Rules

Refuse undocumented fields, standalone export retries after the no-column
signature is confirmed, missing parents, incomplete Profile Types evidence,
multiple exact matches, another skill's scope, or any
create/import/update/merge/delete request. Proposal confirmation never
authorizes execution.

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
validation-only task path.

## Implementation Notes

Use the parent skill for scope proposals and complete-set integrity. The 26C
proposal/readback field identity is source-backed, but the standalone provider
is unavailable, current exact evidence must come from Profile Types, and the
mutation provider remains unapproved. Return a closed, actionable readiness
result whenever the containing evidence is absent. Track token usage for
generated project artifacts using the manifest policy.

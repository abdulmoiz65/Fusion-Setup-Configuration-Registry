---
skill_id: "hcm.global-human-resources.document-types.manage-extended-lookup-codes"
name: "Manage Extended Lookup Codes Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Extended Lookup Codes under the Document Types functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Document Types"
functional_area_code: "ORA_DOCUMENT_TYPES"
task_code: "PER_MANAGE_EXTENDED_LOOKUP_CODE"
task_name: "Manage Extended Lookup Codes"
parent_skill_id: "hcm.global-human-resources.document-types"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "ExtendedLookupCode"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
version: "0.1.3"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "hcm.global-human-resources.global-human-resources-common.manage-common-lookups"
  - "hcm.global-human-resources.global-human-resources-common.manage-administrator-profile-values"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
oracle_supplied_guidance_files:
  - purpose: "Input validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Dependency readiness"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Reference resolution"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Defaulting rules"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Design enforcement"
    location: "ora-resource/ora_design_enforcement.md"
  - purpose: "Failure handling"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/document-types/manage-extended-lookup-codes/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/document-types/manage-extended-lookup-codes/current/"
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
side_effects: []
required_privileges: []
---

# Manage Extended Lookup Codes Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Extended Lookup Codes` under `Document Types`.

## Task Overview

Use this task to plan and govern `Manage Extended Lookup Codes` configuration in Global Human Resources.

- **Task identity:** `PER_MANAGE_EXTENDED_LOOKUP_CODE` — Manage Extended Lookup Codes.
- **Scope:** HCM → Global Human Resources → Document Types.
- **Catalog routing:** CSV export/import support is `Y`; the catalog declares Data Loader mode `REST` with `ExtendedLookupCode`. For mutations, use the live-validated native HCM Data Loader DAT contracts described below; do not issue a direct REST write.
- **Read next:** [task contract](#setup-task-skill-contract) and [usage](#usage). Follow the task-specific routing, approvals, and restrictions in the detailed sections below.

## Setup Task Skill Contract
- task_code: `PER_MANAGE_EXTENDED_LOOKUP_CODE`
- task_name: `Manage Extended Lookup Codes`
- parent_skill_id: `hcm.global-human-resources.document-types`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Document Types`
- functional_area_code: `ORA_DOCUMENT_TYPES`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `ExtendedLookupCode`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Extended Lookup Codes` under `Document Types`.

## Setup Task Metadata

- Task name: `Manage Extended Lookup Codes`
- Task code: `PER_MANAGE_EXTENDED_LOOKUP_CODE`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `ExtendedLookupCode`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using `ExtendedLookupCode` as the BusinessObject.

## CRUD and Reference Routing

### Live-State Preflight

Before every create, edit, delete, retry, or reconciliation, query the selected
Fusion environment for the exact current `LookupType`, `LookupCode`,
`ExtendedLookupCode`, and legislation scope. Prior run records, source files,
archives, and chat history are context only and never prove that a current
record exists.

- For a create request, proceed when the exact live tuple is absent, even if a
  previous run recorded a successful creation; a user may have deleted it
  manually.
- For an edit or delete request, use only one freshly resolved exact target.
- Rebuild the source and approval preview from the live state whenever it
  differs from earlier artifacts; do not interrupt solely because of that
  difference.

- Read only through `hcmExtendedLookupCodes`. Resolve exact names against `ExtendedLookupName`; when the caller explicitly requests a contains search, use `q=ExtendedLookupName like '%term%'`, replacing `term` with the escaped caller-supplied value.
- For a counted read, group translated projections before applying the count and continue to the requested number of unique records or exhaustion; return the final result in the same turn.
- Route lookup resolution to [Global Human Resources Common > Manage Common Lookups](../../global-human-resources-common/manage-common-lookups/SKILL.md).
- Treat a supplied Lookup Type or Lookup Code as a UI display value only when it is not an exact stored value. Resolve it by exact Common Lookup `Meaning`, then use the returned stored `LookupType` and `LookupCode` in the XLSX source; never send the display meaning as a loader key.
- Route profile option value resolution to [Global Human Resources Common > Manage Administrator Profile Values](../../global-human-resources-common/manage-administrator-profile-values/SKILL.md).
- For create, edit, or delete, run every applicable declared read and task rule in graph order. When the graph returns `XLOOK.LOADER_READY`, invoke `core.data-loader` with the task metadata, project context, an editable XLSX source generated from current loader metadata, and the resolved business values. Keep control until Core freezes the XLSX, converts it to DAT internally, and returns the immutable ZIP preview; do not pause at an intermediate step. Then wait for standalone `approve`; ask only for unresolved business input.
- Use `ExtendedLookupCode` as the primary XLSX business-object worksheet. Use `ExtendedLookupCodeTranslation` only for an explicitly requested non-base-language name, and package it with its resolved parent code when both are changed.
- Generate the editable XLSX sample through `core.data-loader` from the current live UCM template. Populate and review that XLSX before DAT generation; DAT is an internal conversion artifact and must not be hand-authored or used as the approval source. The supplied Oracle reference headers are validated examples of the conversion contract: `ExtendedLookupCode` contains the base code, legislation DDF, source-reference, and identity attributes; `ExtendedLookupCodeTranslation` contains `Language`, `ExtendedLookupCodeName`, and the scoped parent fields. Retain a DFF column only when the request supplies a value for that exact DFF context; omit unrelated columns when preparing a minimal mutation source.
- Name each ZIP member after its exact top-level discriminator: `ExtendedLookupCode.dat` for base codes and `ExtendedLookupCodeTranslation.dat` for translations. The local source filename may differ, but it must never become the archive member name.
- Use `MERGE` records for create and edit. Use `DELETE` records for delete. `RestAction` is not an Extended Lookup DAT attribute and must not be added to either metadata header.
- For every base `ExtendedLookupCode` create, use the scoped business fields `LookupType`, `LookupCode`, `LegislationCode`, `ExtendedLookupCode`, and `ExtendedLookupCodeName`, and always include a complete nonblank `SourceSystemOwner`/`SourceSystemId` pair in the XLSX row and generated DAT. Do not rely on default source-key generation for this business object: Fusion can reject a keyless `MERGE` before row loading because it has no unique record reference.
- Preserve a caller-supplied source-key pair only when both values are present and the owner provenance is validated. When the caller supplies neither value, generate the repository-owned pair after resolving the stored business key: use `FDOS` as `SourceSystemOwner`; encode the compact JSON array `[LookupType,LookupCode,LegislationCode-or-GLOBAL,ExtendedLookupCode]` as UTF-8; set `SourceSystemId` to `FDOS_XLOOK_` plus the first 32 uppercase hexadecimal characters of its SHA-256 digest. Validate both attributes against the current live schema and record the generated pair in the immutable preview. A partial, blank, stale, or differently generated pair blocks approval.
- For edits and deletes, resolve one exact current target first. A newly resolved `ExtendedLookupCodeId` may be used only in that single prepared DAT to identify the target; never accept a caller-supplied or previously persisted ID. Include the complete scoped business key as reconciliation evidence. For translations, resolve and include the exact `Language` plus the freshly resolved parent identity.
- Do not issue mutating Fusion REST calls.

Use this task metadata when invoking those skills:

- Offering: `Global Human Resources`
- Functional area / Setup Object: `Document Types`
- Setup task name: `Manage Extended Lookup Codes`
- Setup task code: `PER_MANAGE_EXTENDED_LOOKUP_CODE`




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.global-human-resources.document-types` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Resource References

- [Input validation](ora-resource/ora_input_validation.md)
- [Dependency readiness](ora-resource/ora_dependency_readiness.md)
- [Reference lookups](ora-resource/ora_reference_lookups.md)
- [Defaulting rules](ora-resource/ora_defaulting_rules.md)
- [Design enforcement](ora-resource/ora_design_enforcement.md)
- [Error handling](ora-resource/ora_error_handling.md)

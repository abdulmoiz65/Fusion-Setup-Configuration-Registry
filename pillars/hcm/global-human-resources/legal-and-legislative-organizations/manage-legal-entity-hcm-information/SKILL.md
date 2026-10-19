---
skill_id: "hcm.global-human-resources.legal-and-legislative-organizations.manage-legal-entity-hcm-information"
name: "Manage Legal Entity HCM Information Setup Task Guidance"
description: "Finds, synchronizes, and views Legal Entity HCM Information through declared REST reads and the registered ManageLegalEntity Core Data Loader synchronization object, while routing supported Legal Employer and Payroll Statutory Unit EFF mutations and eligible date-effective parent-row deletion through Core Data Loader. Do not use for Legal Entity creation, parent-field or classification changes, physical deletion, or unrelated legal-structure setup."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Legal and Legislative Organizations"
functional_area_code: "ORA_LEGAL_AND_LEGISLATIVE_ORGANIZATIONS"
task_code: "PER_MANAGE_LEGAL_ENTITY_HCM_INFORMATION"
task_name: "Manage Legal Entity HCM Information"
parent_skill_id: "hcm.global-human-resources.legal-and-legislative-organizations"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObjects:
  - "ManageLegalEntity"
  - "legalEmployersEFF"
  - "payrollStatutoryUnitsEFF"
  - "DeleteOrganizationUnitForDTDelete"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
version: "0.1.4"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "legal_entity_name_or_identifier"
  - "operation"
  - "effective_start_date"
  - "eff_changes"
  - "approval"
  - "source_requirement_document"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
  - "legal_entity_hcm_information_result"
  - "validation_result"
  - "readiness_result"
  - "resume_context"
  - "diagnostics"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.rest-api-client"
  - "core.data-loader"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/legal-and-legislative-organizations/manage-legal-entity-hcm-information/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/legal-and-legislative-organizations/manage-legal-entity-hcm-information/current/"
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
  - "Hands the mandatory ManageLegalEntity synchronization for the uniquely resolved Legal Entity to core.data-loader before branch reads."
  - "Hands supported Legal Employer and Payroll Statutory Unit EFF mutations and eligible date-effective parent-row deletion to core.data-loader."
required_privileges:
  - "Read access to Legal Entity, Legal Employer, Payroll Statutory Unit, EFF metadata, and date-effective history resources."
  - "Core Data Loader privileges for the registered ManageLegalEntity, supported EFF, and DeleteOrganizationUnitForDTDelete business objects."
---

# Manage Legal Entity HCM Information Setup Task Guidance

## Purpose

Provides task-specific planning, read, synchronization, Core Data Loader
routing, and validation guidance for Manage Legal Entity HCM Information under
Legal and Legislative Organizations.

## Task Overview

Use this task to read Legal Employer and Payroll Statutory Unit HCM Information
and to govern supported EFF changes and eligible date-effective parent-row
deletion.

- **Task identity:** `PER_MANAGE_LEGAL_ENTITY_HCM_INFORMATION` — Manage Legal Entity HCM Information.
- **Scope:** HCM → Global Human Resources → Legal and Legislative Organizations.
- **Catalog routing:** CSV export/import support is `Y`; Data Loader mode is `REST` with `ManageLegalEntity`, `legalEmployersEFF`, `payrollStatutoryUnitsEFF`, and `DeleteOrganizationUnitForDTDelete`. `ModifyOrganizationUnitForChildCorrect` and `SplitOrganizationUnitForEFFUpdate` are action sections embedded in the applicable EFF object, not top-level business objects.
- **Read next:** Follow the task contract, usage, CRUD routing, and uniform authoring/read contract below.

## Setup Task Skill Contract

- task_code: `PER_MANAGE_LEGAL_ENTITY_HCM_INFORMATION`
- task_name: `Manage Legal Entity HCM Information`
- parent_skill_id: `hcm.global-human-resources.legal-and-legislative-organizations`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Legal and Legislative Organizations`
- functional_area_code: `ORA_LEGAL_AND_LEGISLATIVE_ORGANIZATIONS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObjects: `ManageLegalEntity`, `legalEmployersEFF`, `payrollStatutoryUnitsEFF`, `DeleteOrganizationUnitForDTDelete`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Prepare Fusion Data Loader DAT Source

Use this workflow when a current Fusion Data Loader sample or mutation handoff
is required.

1. Confirm the registered business objects in manifest order: `ManageLegalEntity`, `legalEmployersEFF`, `payrollStatutoryUnitsEFF`, and `DeleteOrganizationUnitForDTDelete`.
2. Generate current editable samples through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "ManageLegalEntity" \
     "legalEmployersEFF" \
     "payrollStatutoryUnitsEFF" \
     "DeleteOrganizationUnitForDTDelete" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep each editable workbook, attribute-details workbook, and key-fields workbook together. Sample generation does not authorize upload or initiation. During this task's payload preparation, normalize every populated date-only DAT value from accepted input or a generic sample to ISO `YYYY-MM-DD` before handing the immutable source to Core Data Loader, including action `StartDate` and `effectiveOf` `RangeStartDate`. Reject the source when any date-only DAT value remains non-ISO; do not alter timestamps or datetimes.
4. Use `ManageLegalEntity` only for the mandatory synchronization custom action. Its current template requires `legalEntityId` and `RestAction=POST`. Keep the synchronization archive separate from every EFF or delete mutation.
5. Use `legalEmployersEFF` for Legal Employer EFF work and `payrollStatutoryUnitsEFF` for Payroll Statutory Unit EFF work. Preserve this order when both branches change.
6. For every affected top-level organization, compare the requested `EffectiveStartDate` with the current top-level business-object `EffectiveStartDate`. Equal requires `effectiveOf=RangeMode=CORRECTION;RangeStartDate=YYYY-MM-DD` and the embedded `ModifyOrganizationUnitForChildCorrect` action section; a later date requires `effectiveOf=RangeMode=UPDATE;RangeStartDate=YYYY-MM-DD` and the embedded `SplitOrganizationUnitForEFFUpdate` action section; an earlier date is invalid. Include the selected action section within each affected `legalEmployersEFF` or `payrollStatutoryUnitsEFF` branch, including when its EFF child is new.
7. Preserve every root locator required by the current branch template. For the current Legal Employer and Payroll Statutory Unit EFF templates, that includes `OrganizationId`, `OrgUnitClassificationId`, `OrganizationEffectiveStartDate`, `OrgUnitClassEffectiveStartDate`, and `OrgUnitClassEffectiveEndDate`, in addition to `EffectiveStartDate`, `FLEX:PER_ORGANIZATION_INFORMATION_EFF`, and `EFF_CATEGORY_CODE`. These locators identify the existing root; they do not choose correction versus update semantics. An existing EFF child requires its current `OrgInformationId`, `RestAction=PATCH`, and the branch `effectiveOf` mode. A new child leaves `OrgInformationId`, `EffectiveStartDate`, and `EffectiveEndDate` blank and uses `RestAction=POST`. In a dated-update branch, a new child must still set `effectiveOf=RangeStartDate=YYYY-MM-DD`, without `RangeMode=UPDATE`.
8. For the embedded correction action, use the current action template order and the confirmed values: blank `dummyId`, blank `OrgInformationId`, `RestAction=invoke`, ISO `StartDate` (`YYYY-MM-DD`), and the resolved branch `OrganizationId`. For the embedded split action, derive its current template contract before source construction and populate every required field, including its ISO `effectiveStartDate` and resolved `organizationId` when present. Do not put the EFF child identifier on either action row or copy an action contract across objects. Use ISO `YYYY-MM-DD` for every DAT date value.
9. For eligible parent-row deletion, use only `DeleteOrganizationUnitForDTDelete` and the greatest current history row with a predecessor and `FirstSplitFlag=false`. Use current template order and `RestAction=POST` transport with `Content-Type: application/vnd.oracle.adf.action+json`; do not include EFF locators, action sections, or another branch object. Do not invoke `deleteOrganizationUnitForDTDelete` directly.
10. Let `core.data-loader` validate the selected object contract, build the immutable DAT/ZIP, present the preview and approval gate, submit once, monitor, and return diagnostics. Never hand-build or replay an uncertain mutation.

## Usage

Use this skill when planning, reading, synchronizing, exporting, importing, or
validating Manage Legal Entity HCM Information.

## Setup Task Metadata

- Task name: `Manage Legal Entity HCM Information`
- Task code: `PER_MANAGE_LEGAL_ENTITY_HCM_INFORMATION`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Objects: `ManageLegalEntity`, `legalEmployersEFF`, `payrollStatutoryUnitsEFF`, `DeleteOrganizationUnitForDTDelete`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y`, so route task setup data through the
declared shared and core skills:

1. Export explicitly requested setup task data with `shared.setup-export.task-level-export`.
2. Validate setup data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import only through `core.data-loader` using the operation-appropriate configured business object or objects.

Use offering `Global Human Resources`, functional area `Legal and Legislative
Organizations`, task name `Manage Legal Entity HCM Information`, and task code
`PER_MANAGE_LEGAL_ENTITY_HCM_INFORMATION` when invoking those skills.

## CRUD Routing

- Run export only when explicitly requested.
- For an explicit HCM Information detail read, complete the full task chain before responding: resolve one exact Legal Entity by advanced search; reuse a successful terminal `ManageLegalEntity` synchronization from the same interaction session for the same normalized identity and environment when it is no more than 24 hours old, or otherwise submit and poll that synchronization to terminal status; refresh the match; then resolve the applicable `legalEmployers` and `payrollStatutoryUnits` roots, contexts, and requested details. Do not stop at an accepted synchronization initiation or return an initiation report in place of the requested details. Do not poll another loader operation automatically or reuse synchronization across sessions.
- Use today's system date for a normal read. When the user supplies a date, normalize it to `YYYY-MM-DD`, append `&effectiveDate=<YYYY-MM-DD>` only to the top-level GET, and follow only child links returned by that dated root.
- Treat `LegalEmployerFlag` and `PsuFlag` as read-only routing facts. Resolve each applicable root's exact `CategoryCode`, polymorphic describe, contexts, values, and value sets independently.
- For every read, resolve metadata before contexts, show each applicable branch's business details first, then an `EFF Name: <business EFF name>` heading followed by one heading per business context. Under a populated context show only each configured business segment and its display value. Under a describe-backed zero-row context show `No configured segments`; do not enumerate empty segment fields.
- Reject Legal Entity creation, rename, status or classification changes, physical deletion/ZAP, historical or first-row deletion, and unsupported single-row EFF deletion.
- For an EFF edit, accept only explicitly changed, describe-approved segments; preserve omitted values; resolve multirow identity when required; and classify correction versus dated update from the top-level organization dates.
- For an unqualified delete, explain that only the latest eligible date-effective HCM Information row can be removed and that the Legal Entity remains.
- Return `LE.SYNC_LOADER_READY` for synchronization, `LE.LOADER_READY` for a validated EFF/delete handoff, `LE.DONE` for a completed read, `LE.EXPORT_DONE` for export, or `LE.BLOCKED` for a safe stop.
- After a successful synchronization poll, refresh the affected roots and contexts before returning the requested details. After another successful loader completion, refresh only when the user requested verification. Report success only when every requested value and effective boundary verifies.

## Uniform Authoring and Read Contract

- Load task resources in this order: input validation, reference lookups, dependency readiness, defaulting, design enforcement, error handling, then the compiled rule registry.
- Interpret every requested business or EFF attribute within its selected branch, category, and context using current REST `describe` and Data Loader metadata. Match the exact technical name first, then an exact normalized business label or declared task alias, then one unique case-, space-, and punctuation-insensitive match. If multiple attributes remain plausible, show their business labels and ask the user to choose; if none match, report the attribute as unsupported. Never guess or copy a value between attributes.
- Map only requested business values and operation-required identity. Preserve omitted current values and unrelated contexts.
- Require one exact Legal Entity identity, applicable branch evidence, current effective boundary, metadata, value-set evidence, row selection, registered loader contract, required privileges, and current approval before mutation handoff.
- Core Data Loader owns the only mutation preview and approval. Synchronization approval authorizes only synchronization. Any material source, metadata, environment, business-state, or mapping change invalidates approval.
- Never fall back to direct REST, ADF batch, PATCH, PUT, DELETE, `splitOrganizationUnitForEFFUpdate`, or direct `deleteOrganizationUnitForDTDelete` invocation for a supported mutation.
- Retry only eligible read-only requests. After a failed, partial, timed-out, or uncertain loader result, preserve diagnostics, reconcile through declared reads, and require a rebuilt preview plus renewed approval before any retry.
- For normal output, present business labels and values; render the Fusion terminal date as `End of Time`. Do not expose internal IDs, flags, `CategoryCode`, context VO names, paths, links, payloads, tokens, audit fields, or raw loader metadata.
- Return task identity, normalized intent, status, validated inputs, resolved dependencies, selected objects, missing requirements, sanitized evidence, completed side effects, errors, one recommended action, and resume context.
- Treat a mutation as complete only after Core Data Loader reaches a known successful result and fresh declared reads verify the requested business effect. Transport acceptance alone is not completion.

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `legal_entity_name_or_identifier`
- `operation`
- `effective_start_date`
- `eff_changes`
- `approval`
- `source_requirement_document`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`
- `legal_entity_hcm_information_result`
- `validation_result`
- `readiness_result`
- `resume_context`
- `diagnostics`

## Implementation Notes

Use parent skill `hcm.global-human-resources.legal-and-legislative-organizations`
for functional-area sequencing and scope. The six task-local resource files own
validation and task-node behavior; `core.data-loader` owns mutation artifact
construction and approval. Track token usage for durable project artifacts
using the manifest policy.

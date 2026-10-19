---
skill_id: "hcm.global-human-resources.legal-and-legislative-organizations.manage-legal-reporting-unit-hcm-information"
name: "Manage Legal Reporting Unit HCM Information Setup Task Guidance"
description: "Synchronizes, finds, and views Legal Reporting Unit HCM Information, routes explicit Tax Reporting Unit and Reporting Establishment classification changes through Core Data Loader, and routes supported EFF mutations and eligible date-effective parent-row deletion through Core Data Loader. Do not use for unrelated parent organization changes, physical deletion, or unrelated HCM setup."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "Legal and Legislative Organizations"
functional_area_code: "ORA_LEGAL_AND_LEGISLATIVE_ORGANIZATIONS"
task_code: "PER_MANAGE_LEGAL_REPORTING_UNIT_HCM_INFORMATION"
task_name: "Manage Legal Reporting Unit HCM Information"
parent_skill_id: "hcm.global-human-resources.legal-and-legislative-organizations"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObjects:
  - "ManageLegalReportingUnit"
  - "ManageLegalReportingUnitHcmClassifications"
  - "taxReportingUnitsEFF"
  - "reportingEstablishmentsEFF"
  - "DeleteOrganizationUnitForDTDelete"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
version: "0.1.8"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "legal_reporting_unit_name"
  - "operation"
  - "effective_start_date"
  - "tax_reporting_unit_classification"
  - "reporting_establishment_classification"
  - "eff_changes"
  - "approval"
  - "source_requirement_document"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
  - "lru_hcm_information_result"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/legal-and-legislative-organizations/manage-legal-reporting-unit-hcm-information/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/legal-and-legislative-organizations/manage-legal-reporting-unit-hcm-information/current/"
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
  - "Hands mandatory ManageLegalReportingUnit synchronization for the uniquely resolved LRU to core.data-loader before branch reads."
  - "Hands explicit Tax Reporting Unit and Reporting Establishment classification changes to core.data-loader through ManageLegalReportingUnitHcmClassifications."
  - "Hands supported EFF mutations and eligible date-effective parent-row deletion to core.data-loader."
required_privileges:
  - "Read access to LRU, Tax Reporting Unit, Reporting Establishment, EFF metadata, and history resources."
  - "Core Data Loader privileges for the registered ManageLegalReportingUnit, ManageLegalReportingUnitHcmClassifications, supported EFF, and DeleteOrganizationUnitForDTDelete business objects."
---

# Manage Legal Reporting Unit HCM Information Setup Task Guidance

## Purpose

Provides task-specific planning, read, synchronization, classification, Core
Data Loader routing, and validation guidance for Manage Legal Reporting Unit HCM
Information under Legal and Legislative Organizations.

## Task Overview

Use this task to read Tax Reporting Unit and Reporting Establishment HCM
Information, manage their classifications, and govern supported EFF changes and
eligible date-effective parent-row deletion.

- **Task identity:** `PER_MANAGE_LEGAL_REPORTING_UNIT_HCM_INFORMATION` — Manage Legal Reporting Unit HCM Information.
- **Scope:** HCM → Global Human Resources → Legal and Legislative Organizations.
- **Catalog routing:** CSV export/import support is `Y`; Data Loader mode is `REST` with `ManageLegalReportingUnit`, `ManageLegalReportingUnitHcmClassifications`, `taxReportingUnitsEFF`, `reportingEstablishmentsEFF`, and `DeleteOrganizationUnitForDTDelete`. `ModifyOrganizationUnitForChildCorrect` and `SplitOrganizationUnitForEFFUpdate` are action sections embedded in the applicable EFF object, not top-level business objects.
- **Read next:** Follow the task contract, usage, CRUD routing, and uniform authoring/read contract below.

## Setup Task Skill Contract

- task_code: `PER_MANAGE_LEGAL_REPORTING_UNIT_HCM_INFORMATION`
- task_name: `Manage Legal Reporting Unit HCM Information`
- parent_skill_id: `hcm.global-human-resources.legal-and-legislative-organizations`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `Legal and Legislative Organizations`
- functional_area_code: `ORA_LEGAL_AND_LEGISLATIVE_ORGANIZATIONS`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObjects: `ManageLegalReportingUnit`, `ManageLegalReportingUnitHcmClassifications`, `taxReportingUnitsEFF`, `reportingEstablishmentsEFF`, `DeleteOrganizationUnitForDTDelete`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Prepare Fusion Data Loader DAT Source

Use this workflow when a current Fusion Data Loader sample or mutation handoff
is required.

1. Confirm the registered business objects in manifest order: `ManageLegalReportingUnit`, `ManageLegalReportingUnitHcmClassifications`, `taxReportingUnitsEFF`, `reportingEstablishmentsEFF`, and `DeleteOrganizationUnitForDTDelete`.
2. Generate current editable samples through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "ManageLegalReportingUnit" \
     "ManageLegalReportingUnitHcmClassifications" \
     "taxReportingUnitsEFF" \
     "reportingEstablishmentsEFF" \
     "DeleteOrganizationUnitForDTDelete" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep each editable workbook, attribute-details workbook, and key-fields workbook together. Sample generation does not authorize upload or initiation. During this task's payload preparation, normalize every populated date-only DAT value from accepted input or a generic sample to ISO `YYYY-MM-DD` before handing the immutable source to Core Data Loader, including action `StartDate` and `effectiveOf` `RangeStartDate`. Reject the source when any date-only DAT value remains non-ISO; do not alter timestamps or datetimes.
4. Use `ManageLegalReportingUnit` only as a synchronization-only operation when no successful terminal synchronization for the same normalized LRU identity and environment exists in this session within 24 hours. Its current template requires `establishmentId` and uses `RestAction=POST`. After completion, refresh advanced search. Keep this archive separate and do not treat its approval as classification approval.
5. For a classification change, ask exactly `Should be classified as Tax Reporting Unit? Yes/No` and `Should be classified as Reporting Establishment? Yes/No`. Require both answers, map them internally, and use only `ManageLegalReportingUnitHcmClassifications`. When the two questions are pending, an explicit answer of `Both` or `Yes to both` means Yes/Yes; do not ask again. Resolve the pre-classification `OrganizationId` from `organizationsLOV` by exact Name plus `ClassificationCode=HCM_LRU`, not from `taxReportingUnits` or `reportingEstablishments`, because those roots do not exist until their classifications are active. Then immediately prepare the classification-only Core Data Loader preview. The classification answer does not approve submission. Never expose `isTRU` or `isRE` to the user.
6. Use `taxReportingUnitsEFF` for Tax Reporting Unit EFF work and `reportingEstablishmentsEFF` for Reporting Establishment EFF work. Preserve this order when both branches change.
7. For every affected top-level organization, compare the requested `EffectiveStartDate` with the current top-level business-object `EffectiveStartDate`. Equal requires the embedded `ModifyOrganizationUnitForChildCorrect` action section and `effectiveOf=RangeMode=CORRECTION;RangeStartDate=YYYY-MM-DD`; a later date requires the embedded `SplitOrganizationUnitForEFFUpdate` action section and `effectiveOf=RangeMode=UPDATE;RangeStartDate=YYYY-MM-DD`; an explicit end-date change uses `RangeMode=END_DATE`; earlier is invalid. Include the selected action section within each affected `taxReportingUnitsEFF` or `reportingEstablishmentsEFF` branch, including when its EFF child is new.
8. For an EFF context mutation, derive `FLEX:PER_ORGANIZATION_INFORMATION_EFF`, `EFF_CATEGORY_CODE`, every exposed root locator, child identity, `SourceRef010`, and the action contract from the selected object's current root, parent EFF row, context, and live loader metadata; each member must contain its own action section. Populate only fields exposed by that exact live template, using their fresh current values. Do not require or add `OrganizationEffectiveStartDate`, `OrgUnitClassEffectiveStartDate`, `OrgUnitClassEffectiveEndDate`, or another locator merely because a sibling EFF object exposes it. For an existing EFF child, copy its current `OrgInformationId`, child `EffectiveStartDate`, and child `EffectiveEndDate` exactly from the fresh selected effective row, use `RestAction=PATCH`, and apply the branch `effectiveOf` mode; never replace an existing child's current key or dates with the requested operation date. Different effective dates across the top-level row, parent EFF row, and existing child are valid and must be validated independently rather than forced to match. A new child must omit only child `OrgInformationId` and use `RestAction=POST`. When its flattened live template exposes only the shared `EffectiveStartDate` and `EffectiveEndDate` pair on the EFF business-object line, those columns are the parent EFF locator: copy the fresh selected parent EFF row's dates exactly and never substitute the requested operation date. Populate child dates only when the exact live template exposes distinct child-date columns separate from that parent locator. Put the requested operation date in `effectiveOf` and the embedded action fields required by the live contract. In a dated-update branch, a new POST child must set `effectiveOf=RangeStartDate=YYYY-MM-DD`, without `RangeMode=UPDATE`; leave action `OrgInformationId` blank. Before preview, compare every populated parent locator date with the fresh selected parent EFF key and block on any mismatch. The registered Data Loader mapping owns ancestor REST routing; do not synthesize REST paths or block solely because the selected template omits locator columns exposed by another object.
9. For the embedded correction action, use its current template order and confirmed values: blank `dummyId`, blank `OrgInformationId`, `RestAction=invoke`, ISO `StartDate` (`YYYY-MM-DD`), and the resolved branch `OrganizationId`. For the embedded split action, derive its current template contract before source construction and populate every required field, including its ISO `effectiveStartDate` and resolved `organizationId` when present. Do not put the EFF child identity on either action row. Use ISO `YYYY-MM-DD` for every DAT date value and never copy an action contract across objects.
10. For eligible parent-row deletion, use only `DeleteOrganizationUnitForDTDelete` and the greatest current history row with a predecessor and `FirstSplitFlag=false`. Use current template order and `RestAction=POST` transport with `Content-Type: application/vnd.oracle.adf.action+json`; do not include EFF locators, action sections, or another branch object. Do not invoke `deleteOrganizationUnitForDTDelete` directly.
11. Let `core.data-loader` validate the selected object contract, build the immutable DAT/ZIP, present the preview and approval gate, submit once, monitor, and return diagnostics. Never hand-build or replay an uncertain mutation.

## Usage

Use this skill when planning, reading, synchronizing, classifying, exporting,
importing, or validating Manage Legal Reporting Unit HCM Information.

## Setup Task Metadata

- Task name: `Manage Legal Reporting Unit HCM Information`
- Task code: `PER_MANAGE_LEGAL_REPORTING_UNIT_HCM_INFORMATION`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Objects: `ManageLegalReportingUnit`, `ManageLegalReportingUnitHcmClassifications`, `taxReportingUnitsEFF`, `reportingEstablishmentsEFF`, `DeleteOrganizationUnitForDTDelete`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y`, so route task setup data through the
declared shared and core skills:

1. Export explicitly requested setup task data with `shared.setup-export.task-level-export`.
2. Validate setup data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import only through `core.data-loader` using the operation-appropriate configured business object or objects.

Use offering `Global Human Resources`, functional area `Legal and Legislative
Organizations`, task name `Manage Legal Reporting Unit HCM Information`, and
task code `PER_MANAGE_LEGAL_REPORTING_UNIT_HCM_INFORMATION` when invoking those
skills.

## CRUD Routing

- Run export only when explicitly requested.
- For an explicit HCM-detail read, complete the full task chain before responding: resolve one exact Legal Reporting Unit by advanced search; reuse a successful terminal `ManageLegalReportingUnit` synchronization for the same normalized identity and environment from this session when it is no more than 24 hours old, or otherwise submit and poll that synchronization to terminal status; refresh the matched identity and classifications; if classification is a required approved prerequisite, submit and poll `ManageLegalReportingUnitHcmClassifications` to terminal status; then refresh classifications, resolve each active branch using its exact `EstablishmentId` root query, read the requested contexts, and return the requested details. Do not stop at an accepted synchronization or prerequisite-classification initiation, or return an initiation report in place of the requested details. Never reuse synchronization evidence across sessions.
- Treat `A` as active and `I`, null, or an absent supported indicator as inactive. When neither branch is active, or an explicit classification change is requested, ask both business-facing Yes/No questions and route only `ManageLegalReportingUnitHcmClassifications`. For a view or edit with neither branch active, require at least one Yes; both No remains blocked and must not invoke the classification loader. When those paired questions are pending, interpret a clear `Both` or `Yes to both` answer as explicit Yes/Yes, do not repeat the questions, resolve the classification identity from `organizationsLOV`, and continue immediately to the classification-only Core Data Loader preview and approval gate.
- When classification is an approved prerequisite for a still-pending explicit detail read or edit, poll that accepted classification load to terminal status as this task's continuation step, refresh advanced search, require both classification properties to match the approved answers, and resume the original read or edit. For a standalone classification request, return the accepted initiation response without automatic polling. Do not repeat synchronization while the same-session 24-hour evidence remains valid.
- For every normal read, resolve one effective read date: use today's system date unless the user explicitly asks for details on another date, then normalize that date to `YYYY-MM-DD`. Always append `&effectiveDate=<resolved YYYY-MM-DD>` to each top-level Tax Reporting Unit or Reporting Establishment GET, and follow only child links returned by that dated root. Never use an undated root response to choose the effective record.
- Resolve every active branch independently. Use each root's exact `CategoryCode`, polymorphic describe, contexts, values, and value sets. For a generic view, default only Tax Reporting Unit Details and Reporting Establishment Details.
- Show each applicable branch's business details first, then an `EFF Name: <business EFF name>` heading followed by one heading per business context. Under a populated context show only each configured business segment and its display value. Under a describe-backed zero-row context show `No configured segments`; do not enumerate empty segment fields.
- Reject LRU creation, rename, status change outside the classification route, physical deletion/ZAP, historical or first-row deletion, and unsupported single-row EFF deletion.
- For an EFF edit, accept only explicitly changed, describe-approved segments; preserve omitted values; resolve multirow identity when required; and classify correction versus dated update from the top-level organization dates.
- For an unqualified delete, explain that only the latest eligible date-effective HCM Information row can be removed and that the LRU remains.
- Return `LRU.SYNC_LOADER_READY` for synchronization, `LRU.CLASSIFICATION_LOADER_READY` for classification, `LRU.LOADER_READY` for a validated EFF/delete handoff, `LRU.DONE` for a completed read/export, or `LRU.BLOCKED` for a safe stop.
- After successful loader completion, refresh classifications, affected roots, contexts, and history. When the load was a classification prerequisite for a pending detail read or edit, continue through those refreshed reads and present the requested details or resume the edit. Report success only when every requested value and effective boundary verifies.

## Uniform Authoring and Read Contract

- Load task resources in this order: input validation, reference lookups, dependency readiness, defaulting, design enforcement, error handling, then the compiled rule registry.
- Interpret every requested business or EFF attribute within its selected branch, category, and context using current REST `describe` and Data Loader metadata. Match the exact technical name first, then an exact normalized business label or declared task alias, then one unique case-, space-, and punctuation-insensitive match. If multiple attributes remain plausible, show their business labels and ask the user to choose; if none match, report the attribute as unsupported. Never guess or copy a value between attributes.
- Map only requested business values and operation-required identity. Preserve omitted current values and unrelated contexts.
- Require one exact LRU identity, confirmed same-session synchronization evidence or a newly completed synchronization, explicit classification answers when applicable, the pre-classification `organizationsLOV` identity for classification, active branch evidence only for branch reads or EFF/history work, current effective boundary, metadata, value-set evidence, row selection, registered loader contract, required privileges, and current approval before mutation handoff.
- Core Data Loader owns the only mutation preview and approval. Synchronization approval authorizes only synchronization; classification approval authorizes only classification. Any material source, metadata, environment, business-state, or mapping change invalidates approval.
- Do not use direct REST, ADF batch, PATCH, PUT, or DELETE for an EFF mutation. Also never use direct POST, setup import, direct classification custom-method invocation, or direct `deleteOrganizationUnitForDTDelete` invocation for any supported mutation.
- Retry only eligible read-only requests. After a failed, partial, timed-out, or uncertain loader result, preserve diagnostics, reconcile through declared reads, and require a rebuilt preview plus renewed approval before any retry.
- For normal output, present business labels and values; render the Fusion terminal date as `End of Time`. Do not expose internal IDs, classification field names, `CategoryCode`, context VO names, paths, links, payloads, tokens, audit fields, or raw loader metadata.
- At approval, title the summary `Proposed changes` and show Classification, EFF Category, Context, Segment, Current Value when available, and New Value.
- Return task identity, normalized intent, status, validated inputs, resolved dependencies, selected objects, missing requirements, sanitized evidence, completed side effects, errors, one recommended action, and resume context.
- Treat a mutation as complete only after Core Data Loader reaches a known successful result and fresh declared reads verify the requested business effect. Transport acceptance alone is not completion.

## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `legal_reporting_unit_name`
- `operation`
- `effective_start_date`
- `tax_reporting_unit_classification`
- `reporting_establishment_classification`
- `eff_changes`
- `approval`
- `source_requirement_document`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`
- `lru_hcm_information_result`
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

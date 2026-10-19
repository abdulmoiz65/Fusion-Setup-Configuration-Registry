---
skill_id: "hcm.global-human-resources.hcm-responsibilities.areas-of-responsibility-templates"
name: "Areas of Responsibility Templates Setup Task Guidance"
description: "Provides task-specific setup guidance for Areas of Responsibility Templates under the HCM Responsibilities functional area. Use when the user asks to plan, validate, or execute this task's declared scope; do not use it for unrelated HCM configuration."
layer: "pillar"
pillar: "HCM"
offering: "Global Human Resources"
functional_area: "HCM Responsibilities"
functional_area_code: "CUSTOM_HCM_RESPONSIBILITIES"
task_code: "CUSTOM_AREAS_OF_RESPONSIBILITY_TEMPLATES"
task_name: "Areas of Responsibility Templates"
parent_skill_id: "hcm.global-human-resources.hcm-responsibilities"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "AORTemplate"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global human resources pillar team"
version: "0.1.9"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/hcm-responsibilities/areas-of-responsibility-templates/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-human-resources/hcm-responsibilities/areas-of-responsibility-templates/current/"
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

# Areas of Responsibility Templates Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Areas of Responsibility Templates` under `HCM Responsibilities`.

## Task Overview

Use this task to plan and govern `Areas of Responsibility Templates` configuration in Global Human Resources.

- **Task identity:** `CUSTOM_AREAS_OF_RESPONSIBILITY_TEMPLATES` — Areas of Responsibility Templates.
- **Scope:** HCM → Global Human Resources → HCM Responsibilities.
- **Catalog routing:** CSV export/import support is `N`; the declared Data Loader mode is `REST` with `AORTemplate`.
- **Read next:** [task contract](#setup-task-skill-contract) and [usage](#usage). Follow the task-specific routing, approvals, and restrictions in the detailed sections below.

## Setup Task Skill Contract
- task_code: `CUSTOM_AREAS_OF_RESPONSIBILITY_TEMPLATES`
- task_name: `Areas of Responsibility Templates`
- parent_skill_id: `hcm.global-human-resources.hcm-responsibilities`
- pillar: `HCM`
- offering: `Global Human Resources`
- functional_area: `HCM Responsibilities`
- functional_area_code: `CUSTOM_HCM_RESPONSIBILITIES`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `REST`
- businessObject: `AORTemplate`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Areas of Responsibility Templates` under `HCM Responsibilities`.

## Setup Task Metadata

- Task name: `Areas of Responsibility Templates`
- Task code: `CUSTOM_AREAS_OF_RESPONSIBILITY_TEMPLATES`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: `AORTemplate`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `AORTemplate` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "AORTemplate" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## CRUD and Reference Routing

- Read only through `areasOfResponsibilityTemplates`. For create, check only exact `TemplateCode` availability; an existing TemplateName does not block creation. If the code exists, stop before other resolution and return `PER-1532084 — You need to enter a different code. There's already a responsibility template with this code.` For get, update, or delete by name, return all exact TemplateName matches and require TemplateCode or TemplateId before acting when the name is ambiguous. For an explicitly requested name-fragment/contains search only, call `GET /hcmRestApi/resources/{version}/areasOfResponsibilityTemplates` with `q=TemplateName like '%<escaped-term>%'` (the unescaped query template is `q=TemplateName like '%term%'`), a bounded `limit`, and `REST-Framework-Version: 9`; with `fusion_rest_client.py`, pass `--header 'REST-Framework-Version: 9'`. Do not apply that header to exact TemplateCode, exact TemplateName, TemplateId, parent-item, or child-collection reads. A contains search is GET-only and does not generate HDL or DAT. For one resolved parent, read its `AoRTemplateScope`, `AoRTemplateCriteria`, and `AssignedReps` child collections directly and through every page. Treat those child-collection reads as authoritative; an expanded parent payload can omit children and must not be used to conclude that a scope, criterion, or assignment is absent.
- When the parent record returns `Usage: null`, report Approval / Checklist usage as not configured; it is a persisted empty value, not an unknown response.
- For GET and post-load reconciliation, read stored scope and criteria keys from the direct child collections, then reverse-resolve each static value through its registered LOV or Common Lookup contract using the stored ID, code, and set context. Present the resolved human-readable value first, followed by its ID, code, or set as supporting evidence. Keep those stored keys for later update or delete, but never present an ID alone as the meaning of the configuration. If a static value cannot be reverse-resolved exactly, label it as an unresolved persisted value with its raw stored key; do not guess a label or mutate it. Supported dynamic scope sentinels remain Dynamic Value enabled and skip reverse LOV resolution.
- Route lookup resolution to [Global Human Resources Common > Manage Common Lookups](../../global-human-resources-common/manage-common-lookups/SKILL.md).
- Route profile option value resolution to [Global Human Resources Common > Manage Administrator Profile Values](../../global-human-resources-common/manage-administrator-profile-values/SKILL.md).
- For create, edit, or delete, run every applicable declared read and task rule in graph order. Execute and map all applicable resolvers in the same turn. Do not return a progress-only response after routing, schema generation, lookup, or source mapping; continue until Core returns the immutable ZIP preview or a resolver returns a concrete blocker. Build the Data Loader Task Hook preview for that exact archive, then wait for standalone `approve`; ask only for unresolved business input.
- After approval, verify the unchanged archive through the Data Loader Task Hook. Pass the verification result's inner `taskValidationEnvelope` object, rather than its outer verification wrapper, to `core.data-loader` for the single approved upload and initiation. Wait for that initiation command to complete and capture its Content ID and Request ID before status polling. If the execution environment yields an active command session or an empty incremental response, retain and poll that same session to completion; do not treat it as a failed or absent upload, reconcile prematurely, or submit the archive again.
- Do not issue mutating Fusion REST calls.

## Areas of Responsibility Template Authoring Rules

- For create, collect `TemplateName`, `TemplateCode`, and `StartDate`, with only explicitly requested Basic Info, responsibility scope, criteria, or directly assigned representative rows. Normalize unambiguous request dates (`DD Month YYYY`, `D Mon YYYY`, `YYYY-MM-DD`, `YYYY/MM/DD`, `today`, and `one year from today`) to `YYYY/MM/DD` before validation and serialization. Ask for clarification for ambiguous numeric dates such as `01/02/2027`; DAT content must always use `YYYY/MM/DD`. For edit or delete, resolve one fresh template and require explicit changes or delete intent. Before generating an archive with any scope-child mutation, retrieve all current persisted scopes and calculate the final state after every requested scope operation. Reject the request if no populated static or dynamic responsibility scope remains; do not generate a DAT, ZIP, preview, checksum, or approval request.
- Resolve each required lookup and child identity before source generation, according to `ora-resource/ora_reference_lookups.md`; a display value never substitutes for the documented stored ID, code, or set context.
- For Location scope or criterion resolution, map the live `locationsLov` response field `SetCode` to the HDL target column `LocationSetCode`. A missing response property named `LocationSetCode` is not a resolver gap; never infer a set that the resolver did not return.
- Dynamic TemplateScope mode is supported only for `AOR_BUSINESS_UNIT`, `AOR_DEPARTMENT`, `AOR_LEGAL_EMPLOYER`, and `AOR_LOCATION`. Set `DynamicValueFlag=Y`, do not run that scope LOV resolver, and leave all static mapping fields blank. A dynamic scope counts as populated for final-state validation. For each template, allow one row only per canonical scope attribute; reject duplicate rows, an unsupported dynamic attribute, or a dynamic row with static values.
- For GET/reconciliation, normalize a scope as Dynamic Value enabled when `DynamicValueFlag=Y`, or when one of those four supported attributes returns `DynamicValueFlag=null` and `DefaultValueNumber=-999`. Do not expose `-999` as a static object ID, run an LOV resolver for it, or replace the dynamic state in a later update unless the user explicitly changes it. For an unsupported attribute, retain `DefaultValueNumber=-999` as an unexpected persisted value and report it rather than interpreting it as dynamic.
- For a bulk request with invalid rows, do not generate or upload an archive. Report every invalid row and field, retain fully resolved valid rows only in current request state, and ask whether to continue with those valid rows. Generate a fresh valid-only DAT/ZIP only after explicit approval; never silently discard invalid rows or create valid rows automatically.
- When a documented LOV rejects its display-name `q` filter, use its supported identifier filter when one is available; otherwise use a bounded collection read and compare the declared display field after trimming incidental outer whitespace. Require one active/effective exact match; do not use partial matching or broaden this fallback to unrelated REST reads.
- Keep the parent and requested children in one scoped workbook. Before LOV resolution or source generation, reject a create with no scope rows: “At least one responsibility scope must have a value. No responsibility scope was supplied.” A `DynamicValueFlag=Y` scope is populated, valid only for the four supported dynamic attributes, and skips LOV resolution. A blank static Required Flag=Y scope is invalid. Temporarily reject every blank static scope, regardless of Required Flag or other populated scopes, with “Static blank scope serialization is temporarily unsupported pending an attribute-specific loader-proven contract.” Do not emit empty mapped fields, `#NULL`, or a DynamicValueFlag substitute, and do not convert it to DELETE.
- Generate a fresh editable AORTemplate workbook and attribute-details workbook from live Data Loader metadata for every mutation. Build the source from those generated headers; do not reuse fixed AOR headers or a prior DAT as a template. Apply the scope, criteria, sequence, child-operation, and archive rules declared in the AOR `ora-resource` files while authoring the live-template source.
- For TemplateScope, TemplateCriteria, and DirectlyAssigned, use only the live-template columns that the applicable AOR authoring rule permits. A parent delete cascades its children. Before any parent lookup or resolver, reject a `MERGE` plus `DELETE` for the same template and logical scope or criterion; each child has one operation per archive. Emit one TemplateCriteria row per selected value, use canonical AttributeName or CriteriaAttributeName values, and assign CriteriaAttributeId in the documented DAT order. DirectlyAssigned requires the resolved TemplateId, PersonId/PersonNumber, AssignmentId/AssignmentNumber, and ResponsibilityName business keys.
- For an existing template with any TemplateScope, TemplateCriteria, or DirectlyAssigned `MERGE` or `DELETE`, emit one preceding `AORTemplate` `MERGE` identity row in the same archive, containing the resolved TemplateId and TemplateCode even when no parent attribute changes. This establishes Fusion's parent logical object for child-only operations. Do not use the identity row to invent parent values; parent delete continues to use its parent delete operation and cascades children.
- Before preview, verify the authored DAT against the live template: one METADATA section per emitted component, one union header per component for a multi-template archive, exact row/header field counts including trailing blanks, and exactly one root `AORTemplate.dat` in the ZIP. Run the existing generic `core/data-loader/scripts/validate_data_load_file.py` validation for the final archive. Pass only the resulting validated archive to `core.data-loader` for the approved upload.
- Name each outer archive `AORTemplate-<operation>-<primary-template-code-or-batch-label>.zip`. Use only `create`, `update`, `delete`, `copy`, `bulk-create`, or `bulk-crud`; sanitize tokens to letters, digits, `_`, and `-`. Keep exactly one root `AORTemplate.dat` inside. Include the selected archive name in the approval preview and artifact manifest; archive naming must not change HDL rows, metadata, validation, or upload behavior.
- Show the exact target, row mapping, source fingerprint, chosen ZIP filename, and immutable preview before approval. A changed target, source, mapping, or preview requires renewed approval.
- Preserve omitted edit values and retain resolved identifiers only for the run. Do not use mutating Fusion REST calls.
- After initiation, preserve the status result and poll through the declared Data Loader status route until it reaches a terminal state. Treat the known security-related AOR import message as informational only when rows are loaded, no rows have failed, and no terminal failure status is returned; retain the message without directing source correction. Do not report terminal success until Fusion reports a terminal success state.



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

Use the parent functional-area skill `hcm.global-human-resources.hcm-responsibilities` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Resource References

- [Input validation](ora-resource/ora_input_validation.md)
- [Dependency readiness](ora-resource/ora_dependency_readiness.md)
- [Reference lookups](ora-resource/ora_reference_lookups.md)
- [Defaulting rules](ora-resource/ora_defaulting_rules.md)
- [Design enforcement](ora-resource/ora_design_enforcement.md)
- [Error handling](ora-resource/ora_error_handling.md)

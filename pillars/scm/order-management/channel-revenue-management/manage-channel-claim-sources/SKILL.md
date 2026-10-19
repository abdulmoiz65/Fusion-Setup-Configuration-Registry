---
skill_id: "scm.order-management.channel-revenue-management.manage-channel-claim-sources"
name: "Manage Channel Claim Sources Setup Task Guidance"
description: "Provides create and update guidance for Channel Claim Sources and existing settlement methods, with operation-specific validation and approved Data Loader submission."
layer: "pillar"
pillar: "SCM"
offering: "Order Management"
functional_area: "Channel Revenue Management"
functional_area_code: "ORA_FOM_CHANNEL_REV_MGMT"
task_code: "ORA_CJM_MANAGE_CLAIM_SOURCES"
task_name: "Manage Channel Claim Sources"
parent_skill_id: "scm.order-management.channel-revenue-management"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "channelClaimSources"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM order management pillar team"
version: "0.2.1"
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
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/channel-revenue-management/manage-channel-claim-sources/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/order-management/channel-revenue-management/manage-channel-claim-sources/current/"
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

# Manage Channel Claim Sources Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Channel Claim Sources` under `Channel Revenue Management`.

## Setup Task Skill Contract

- task_code: `ORA_CJM_MANAGE_CLAIM_SOURCES`
- task_name: `Manage Channel Claim Sources`
- parent_skill_id: `scm.order-management.channel-revenue-management`
- pillar: `SCM`
- offering: `Order Management`
- functional_area: `Channel Revenue Management`
- functional_area_code: `ORA_FOM_CHANNEL_REV_MGMT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `channelClaimSources`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Channel Claim Sources` under `Channel Revenue Management`.

## Setup Task Metadata

- Task name: `Manage Channel Claim Sources`
- Task code: `ORA_CJM_MANAGE_CLAIM_SOURCES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `channelClaimSources`

## CSV Export, Import, and Validation Workflow

Read the task resources in order: [input contracts](ora-resource/ora_input_validation.md), [dependencies](ora-resource/ora_dependency_readiness.md), [lookups](ora-resource/ora_reference_lookups.md), [defaults](ora-resource/ora_defaulting_rules.md), [design gates](ora-resource/ora_design_enforcement.md), and [errors and readiness gates](ora-resource/ora_error_handling.md). Evaluate the compiled task graph through core.data-loader Task Hook. The graph validates readiness; it does not authorize a direct REST write.

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using channelClaimSources as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Order Management`
- Functional area / Setup Object: `Channel Revenue Management`
- Setup task name: `Manage Channel Claim Sources`
- Setup task code: `ORA_CJM_MANAGE_CLAIM_SOURCES`


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `channelClaimSources` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "channelClaimSources" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

For an update workbook, add `--operation update`. Samples may contain unrelated records or a POST fallback. Resolve the intended existing targets and require `RestAction=PATCH` on every actual update row; never upload untouched sample values.


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

Use the parent functional-area skill `scm.order-management.channel-revenue-management` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

## Create and Update Workflow

1. Require explicit create or update intent; never infer upsert. For update, resolve ClaimSourceMapId or the exact existing ClaimClassCode + ClaimSourceCode + reference-data set. Cross-check all supplied identity values. Resolve each existing settlement-method child by SourceSettlementMethodId under that parent; do not use the proposed SettlementMethod name to locate the old child.
2. Read the operation-specific [Update Fields](ora-resource/ora_input_validation.md#parent-update-fields). Support all seven parent scalar PATCH fields and four child PATCH fields subject to Oracle restrictions and the live loader contract. Codes and response fields are not writable merely because they appear in an export. Dates are not part of this API's PATCH contract; do not map FromDate/ToDate to invented attributes.
3. During preparation, use only the declared read-only resolvers through the shared REST client selected by core.data-loader. Establish the exact environment, privileges, current targets, reference values, and live loader field/key/child-linkage/PATCH support before mapping. API support alone is not loader support. Stop on a missing capability; do not substitute direct REST, a browser, or another import route.
4. Compare a full exported workbook with its trusted baseline and fresh instance values. Separate unchanged context from proposed edits. Preserve omitted values and unrelated children; no create defaults on update. Blank cells mean preserve, not clear. Explicit clears require a nullable field and a documented loader null encoding. Return NO_CHANGE for an empty diff.
5. Prepare sparse parent-only, child-only, or combined existing-record updates through core.data-loader. Include only verified identity/control fields and requested changes, with RestAction=PATCH. Represent settlementMethods as child rows, not a JSON cell or collection replacement. Child-only sources retain required workbook structure but must not fabricate a parent change. Split differing change-column sets unless the loader documents per-row omission. Do not add/delete child records as an update fallback.
6. Run normal Data Loader mapping/schema checks and create the immutable archive. Invoke Task Hook and evaluate this task graph for that exact artifact; show the validated before/after preview, target environment, and operation. Obtain approval under core.data-loader's workflow. At later submission verify only the saved artifact integrity, environment/context and approved Task Hook envelope; do not reopen the original source, refresh live metadata/references or rerun task rules. Readiness is not approval. Newly requested edits require a new artifact, validation and approval. Merely editing the original workbook does not alter the intact approved archive. Missing/changed approved bytes or a context/envelope mismatch blocks submission and requires a new cycle.
7. Submit once through core.data-loader. Initiation is not completion; retrieve status/errors when requested under that workflow. Verify requested values using the declared target reads. Preserve partial successes; reconcile an uncertain mutation before any approved retry. Never retry a POST/PATCH or resubmit an entire partially completed batch automatically.

Create retains the required claim-class/source codes, prefix, resolved set, reference checks, duplicate rejection, and documented create defaults. Updates never create a missing target. This assisted skill adds no writer or generic loader implementation. Review ownership: SCM Pillar Lead/SME and A-Team/core reviewer.

## Add Settlement Methods to an Existing Source

Use explicit operation create_child for a missing settlement method under a verified existing source. This is distinct from creating the parent and from updating an existing child. Resolve the parent, resolve method/accounting values, and check the complete child collection for duplicates through find_settlement_method_duplicate. Prepare child POST rows only, with verified parent linkage supported by live core.data-loader metadata. Do not fabricate a parent POST or PATCH, use upsert, or replace the collection. Parent PATCH changes from the same workbook use separate immutable artifacts and previews.

When the user explicitly requests create-missing/update-modified/skip-unchanged behavior, classify records during preparation using complete live evidence and the trusted baseline. Never infer this policy from upload alone. Existing child updates still require a verified child ID; a duplicate child-create blocks unless the user authorized classification, in which case identical rows are skipped and modified rows are separately validated as updates. Preserve unchanged baseline context rather than reverting earlier instance changes. Show omitted export-only fields and unresolved differences before approval. The create_child graph reaches CHILD_CREATE_READY only after exact child POST/linkage support is verified; API support alone is insufficient.

The child create request is documented by Oracle [26C Create settlement methods](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/fasrp/op-channelclaimsources-claimsourcemapid-child-settlementmethods-post.html). This is contract evidence, not authorization for a direct REST write.

## Parent and Child Update Contract Sources

Oracle's [26C resource index](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/fasrp/api-order-management-channel-claim-sources.html) lists parent PATCH. The [26B parent PATCH request schema](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/fasrp/op-channelclaimsources-claimsourcemapid-patch.html) was the latest retrievable parent schema during authoring on 2026-09-23; the 26C detail page could not be retrieved. Child fields follow the [26C settlement-method PATCH request schema](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/fasrp/op-channelclaimsources-claimsourcemapid-child-settlementmethods-sourcesettlementmethodid-patch.html). Recheck release-specific metadata at preparation time; response schemas are not update whitelists.

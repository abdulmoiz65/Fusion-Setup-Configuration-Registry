---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.advanced-inventory-management.advanced-inventory-parameters"
name: "Advanced Inventory Parameters Setup Task Guidance"
description: "Provides task-specific setup guidance for Advanced Inventory Parameters under the Advanced Inventory Management functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Advanced Inventory Management"
functional_area_code: "ORA_ADVANCED_INVENTORY_MANAGEMENT"
task_code: "ORA_ADVANCED_INVENTORY_PARAMETERS"
task_name: "Advanced Inventory Parameters"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.advanced-inventory-management"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "advancedInventoryParameters"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM manufacturing and supply chain materials management pillar team"
version: "0.1.0"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/advanced-inventory-management/advanced-inventory-parameters/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/advanced-inventory-management/advanced-inventory-parameters/current/"
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

# Advanced Inventory Parameters Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Advanced Inventory Parameters` under `Advanced Inventory Management`.

## Setup Task Skill Contract

- task_code: `ORA_ADVANCED_INVENTORY_PARAMETERS`
- task_name: `Advanced Inventory Parameters`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.advanced-inventory-management`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Advanced Inventory Management`
- functional_area_code: `ORA_ADVANCED_INVENTORY_MANAGEMENT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObjects: `advancedInventoryParameters`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Advanced Inventory Parameters` under `Advanced Inventory Management`.

## Setup Task Metadata

- Task name: `Advanced Inventory Parameters`
- Task code: `ORA_ADVANCED_INVENTORY_PARAMETERS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `advancedInventoryParameters`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import through `core.data-loader` using its source classification. For the REST-backed route, invoke the registered parent BO `advancedInventoryParameters`; its template contains the DFF child section. For an FSM archive, follow the FSM workflow below and preserve native package data; do not select REST BOs for that archive.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Advanced Inventory Management`
- Setup task name: `Advanced Inventory Parameters`
- Setup task code: `ORA_ADVANCED_INVENTORY_PARAMETERS`


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business objects.

1. Confirm the registered parent `advancedInventoryParameters`. Its template contains the DFF child section; do not separately register or invoke a child BO.
2. Generate the parent sample through `core.data-loader` and inspect its discovered child sections:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "advancedInventoryParameters" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep each business object's generated workbook set together:
   - editable sample workbook
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbooks as the starting point for the later Data Loader preparation and approval workflow.

Include DFF data through the parent workbook's child section when the parent template exposes it. Do not request a separate child sample, registration, or Data Loader invocation for `InvAdvancedInvParamsDFF`.

## Prepare and Import a Reviewed Workbook

Follow the same registered-BO workbook workflow as Receiving Parameters. This is the default REST-backed Data Loader route, not native FSM package preparation.

1. Generate the editable `advancedInventoryParameters` XLSX sample using the workflow above. Treat a review spreadsheet as source information, not as an already importable file. For a legacy `.xls` review file, transfer the reviewed values into the generated `.xlsx`; do not merely rename the extension.
2. Map the reviewed fields to the current registered BO attributes through `core.data-loader`'s mapping workflow. Resolve ambiguous or unmapped fields before handoff; any exclusions must be explicit and reported. Apply this task's approved meaning resolvers and input rules. Do not copy native FSM column names or assume FSM-only attributes are writable BO attributes. The FSM extra-attribute policy does not apply to this route.
3. Validate the prepared workbook through `core.data-loader`. The shared loader validates live BO metadata and converts the workbook into `advancedInventoryParameters.dat` inside a ZIP. This DAT ZIP is a BO load artifact, not an FSM ZIP; do not add `ASM_SETUP_CSV_METADATA.xml` or label it FSM.
4. Complete the shared source review, task validation, immutable-artifact preview, and applicable approval workflow before upload or initiation. A changed source, mapping, or artifact requires fresh validation and approval under the shared workflow. This preparation guidance does not authorize a Fusion load.
5. Keep create/update-only restrictions and verified parent/child packaging. If the user requires FSM import, use the FSM workflow below; do not silently substitute the BO route.

## Data Contract

For updates, use the current-value evidence and affected-field scope in `ora_input_validation.md`. Do not request every existing setting for an unrelated update.

The following BO attribute guidance applies to the REST-backed route. For FSM, use the native contract below. Delete operations are unsupported on both routes.

- Require `OrganizationCode`. Per the user's confirmed BO contract, BO-level SQL resolves internal `OrganizationId`; do not request that identifier from the caller.
- Preserve `CrossDockItemCategoryName` exactly as supplied. Its direct pass-through is intentional; no category lookup is required.
- Resolve approved Physical Inventory, Due Date Sort, and Put-away meanings to codes, then remove consumed meaning fields from write data. Cycle Count meaning resolution remains blocked pending feature verification.
- Reject delete operations for parent and child data. Apply the operation and effective-value guards in `ora_input_validation.md` before Data Loader handoff; confirmation cannot bypass them.
- On update, preserve omitted fields and use verified current values only for validation context. Preserve explicit nulls for validation. Apply the Due Date Sort default only on create under `ora_defaulting_rules.md`.
- No friendly Boolean normalization is approved. Confirm canonical BO/Data Loader representations before adding mappings such as Yes/Y/true.



## FSM Import Workflow and CSV Contract

FSM import is delegated to `core.data-loader`; keep `dataloader_import_mode: REST` as the default BO route. A genuine FSM export ZIP with member basename exactly `ASM_SETUP_CSV_METADATA.xml` is classified by the shared loader as FSM. A loose CSV or an arbitrary ZIP is not sufficient. The loader preserves the archive, skips REST BO/template validation for FSM, and sets `sourceType: "FSM"` at initiation. Shared task validation and immutable-artifact approval still apply.

1. Obtain the complete FSM task export ZIP and let core.data-loader classify and validate it.
2. Verify native package task identity. Reject explicit delete requests or known delete settings; let the shared workflow validate the import operation. An export-process label alone is not an import-operation validation failure.
3. Apply the FSM branch of task input/readiness rules; bypass REST field-name checks, meaning resolvers, defaulting, and REST child-BO metadata requirements.
4. Follow the shared Data Loader workflow for the classified FSM source.
5. Delegate validation, approval, upload, and initiation to `core.data-loader` through its current workflow. Do not invoke a task-local import adapter.
6. Report initiation and, when requested, status/errors through core.data-loader. Do not claim a successful task-specific FSM import based solely on catalog flags.

### FSM Parameter Handling

Accept native FSM parameters as supplied, preserving their names and values. Ignore additional attributes outside the inventory below for task-local processing; do not reject a package merely because it contains extra attributes or enforce a fixed column count. Ignoring means no task-local mapping, normalization, or validation for those additional attributes, not dropping embedded values. Shared Data Loader/FSM package validation still applies.

### Patch-dependent FSM Attributes

These five attributes depend on the target environment's patch level:

- `CrossDockAiEnabledFlag`
- `CrossDockExistingRsvFlag`
- `CrossDockExpSupplyDays`
- `CrossDockExpSupplyFlag`
- `PutAwayAiEnabledFlag`

For these five fields only, include supplied values when target-native FSM metadata exposes the columns; otherwise ignore/defer them and report skipped requested values. Do not add absent columns or infer support from another environment. Their absence is not a patch-readiness blocker. Shared validation still applies.



| Area | Observed FSM contract |
| --- | --- |
| Organization | `OrganizationCode` is present; `OrganizationId` is absent. Do not infer native requiredness from the REST-backed BO contract. |
| Category | `CrossDockItemCategoryCode`; preserve the code. REST-backed category-name pass-through does not apply. |
| Priorities | `PutAwaySuggestionP1` through `PutAwaySuggestionP4`; preserve native codes and names. |
| Include Existing Reservations (inferred label; unverified) | `CrossDockExistingRsvFlag`; patch-dependent. |
| Include Expected Supply (inferred label; unverified) | `CrossDockExpSupplyFlag`; patch-dependent. |
| Supply Expected Days (inferred label; unverified) | `CrossDockExpSupplyDays`; patch-dependent; dependency on expected-supply enablement is not yet verified. |
| Additional features | `CrossDockAiEnabledFlag`, `PutAwayAiEnabledFlag`, `FullLpnFeatureFlag`, `FullLpnOrgFlag`, `LpnReuseAllowedFlag`, `MheEnableDeliveryCarts`, `CycleCountCountingMode`. Presence does not establish accepted values or feature availability. |
| DFF | `AttributeCategory` plus 20 character, 5 date, 10 numeric, and 5 timestamp columns in the same CSV. Do not apply REST child packaging. |

### Observed CSV Attributes


| Position | Exact column name |
| --- | --- |
| 1 | `OrganizationCode` |
| 2 | `AllowLpnCooCommingling` |
| 3 | `AllowLpnProjectsCommingling` |
| 4 | `AllowLpnTasksCommingling` |
| 5 | `AttributeCategory` |
| 6 | `AttributeChar1` |
| 7 | `AttributeChar10` |
| 8 | `AttributeChar11` |
| 9 | `AttributeChar12` |
| 10 | `AttributeChar13` |
| 11 | `AttributeChar14` |
| 12 | `AttributeChar15` |
| 13 | `AttributeChar16` |
| 14 | `AttributeChar17` |
| 15 | `AttributeChar18` |
| 16 | `AttributeChar19` |
| 17 | `AttributeChar2` |
| 18 | `AttributeChar20` |
| 19 | `AttributeChar3` |
| 20 | `AttributeChar4` |
| 21 | `AttributeChar5` |
| 22 | `AttributeChar6` |
| 23 | `AttributeChar7` |
| 24 | `AttributeChar8` |
| 25 | `AttributeChar9` |
| 26 | `AttributeDate1` |
| 27 | `AttributeDate2` |
| 28 | `AttributeDate3` |
| 29 | `AttributeDate4` |
| 30 | `AttributeDate5` |
| 31 | `AttributeNumber1` |
| 32 | `AttributeNumber10` |
| 33 | `AttributeNumber2` |
| 34 | `AttributeNumber3` |
| 35 | `AttributeNumber4` |
| 36 | `AttributeNumber5` |
| 37 | `AttributeNumber6` |
| 38 | `AttributeNumber7` |
| 39 | `AttributeNumber8` |
| 40 | `AttributeNumber9` |
| 41 | `AttributeTimestamp1` |
| 42 | `AttributeTimestamp2` |
| 43 | `AttributeTimestamp3` |
| 44 | `AttributeTimestamp4` |
| 45 | `AttributeTimestamp5` |
| 46 | `CrossDockDemandDueDays` |
| 47 | `CrossDockDueDateSort` |
| 48 | `CrossDockEnabledFlag` |
| 49 | `CrossDockIncludeBackorders` |
| 50 | `JobDefinitionName` |
| 51 | `JobDefinitionPackage` |
| 52 | `LpnEnabledFlag` |
| 53 | `LpnGaplessFlag` |
| 54 | `LpnPrefix` |
| 55 | `LpnSuffix` |
| 56 | `LpnUcc128SuffixFlag` |
| 57 | `NextAutoLpnNumber` |
| 58 | `PhysicalInvCountingMode` |
| 59 | `PutAwaySuggestionP1` |
| 60 | `PutAwaySuggestionP2` |
| 61 | `PutAwaySuggestionP3` |
| 62 | `PutAwaySuggestionP4` |
| 63 | `PutAwaySuggestionsEnabled` |
| 64 | `StartAutoLpnNumber` |
| 65 | `TotalLpnLength` |
| 66 | `CrossDockItemCategoryCode` |
| 67 | `TaskManagementAllowed` |
| 68 | `OutboundLoadCreationAllowed` |
| 69 | `FullLpnFeatureFlag` |
| 70 | `FullLpnOrgFlag` |
| 71 | `LpnReuseAllowedFlag` |
| 72 | `CycleCountCountingMode` |
| 73 | `MheEnableDeliveryCarts` |
| 74 | `CrossDockAiEnabledFlag` |
| 75 | `CrossDockExistingRsvFlag` |
| 76 | `CrossDockExpSupplyDays` |
| 77 | `CrossDockExpSupplyFlag` |
| 78 | `PutAwayAiEnabledFlag` |

### Pending FSM Verification

Before an applicable load, establish complete-package task identity, non-delete operation semantics, and authoritative native field validation. Accepted flag values, blank handling, create/update requiredness, lookup domains, defaults, conditional requirements, and DFF contexts remain unverified. Preserve exported representations and obtain native validation evidence instead of inventing normalization. No task-specific successful FSM import has been verified. Registry readiness validates rule structure, not a live package.

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

Use the parent functional-area skill `scm.manufacturing-and-supply-chain-materials-management.advanced-inventory-management` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

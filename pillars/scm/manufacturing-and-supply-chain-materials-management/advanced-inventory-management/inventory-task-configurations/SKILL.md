---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.advanced-inventory-management.inventory-task-configurations"
name: "Inventory Task Configurations Setup Task Guidance"
description: "Provides task-specific setup guidance for Inventory Task Configurations under the Advanced Inventory Management functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Advanced Inventory Management"
functional_area_code: "ORA_ADVANCED_INVENTORY_MANAGEMENT"
task_code: "ORA_INVENTORY_TASK_CONFIGURATIONS"
task_name: "Inventory Task Configurations"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.advanced-inventory-management"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "inventoryZoneTaskConfigurations"
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
  - "core.fusion-api.rest-api-client"
uses_core:
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/advanced-inventory-management/inventory-task-configurations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/advanced-inventory-management/inventory-task-configurations/current/"
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

# Inventory Task Configurations Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Inventory Task Configurations` under `Advanced Inventory Management`.

## Setup Task Skill Contract

- task_code: `ORA_INVENTORY_TASK_CONFIGURATIONS`
- task_name: `Inventory Task Configurations`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.advanced-inventory-management`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Advanced Inventory Management`
- functional_area_code: `ORA_ADVANCED_INVENTORY_MANAGEMENT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObjects: `inventoryZoneTaskConfigurations`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Inventory Task Configurations` under `Advanced Inventory Management`.

## Setup Task Metadata

- Task name: `Inventory Task Configurations`
- Task code: `ORA_INVENTORY_TASK_CONFIGURATIONS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `inventoryZoneTaskConfigurations`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using the registered parent BO `inventoryZoneTaskConfigurations`. Its template contains the activity-usage child sections.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Advanced Inventory Management`
- Setup task name: `Inventory Task Configurations`
- Setup task code: `ORA_INVENTORY_TASK_CONFIGURATIONS`

## Download Fusion Data Loader Sample

Use this workflow only when the user explicitly requests a Fusion Data Loader sample, template, attribute details, key fields, or metadata inspection. For a selected Inventory Task Configurations request that supplies configuration values, do not generate or present sample workbooks. Prepare and validate the populated parent-root XLSX in the same turn.

1. Confirm that `inventoryZoneTaskConfigurations` is the registered parent Data Loader business object. Its template provides the activity-usage child sections; do not separately register or invoke a child BO.
2. Generate the default editable XLSX samples through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "inventoryZoneTaskConfigurations" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the parent BO's generated workbook set together:
   - editable sample workbook
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbooks as the starting point for the later Data Loader preparation and approval workflow.

## Data Loader Preparation Contract

This is the REST Data Loader contract only. It does not apply to an FSM ZIP.

1. Accept an operation of Create or Update, `OrganizationName`, and the five Redwood activity choices. The UI labels map to child `ActivityTypeCode` values: Pick confirm -> `PICK`, Cycle count -> `CC`, Physical count -> `PC`, PAR count -> `PAR`, and Receipt delivery -> `DEL`. An unqualified request is Create.
2. Resolve the organization only to derive `ZoneName` as `<OrganizationCode> Default` and to perform read-only default-zone existence checks.
3. Populate parent and child `OrganizationName`, and populate the derived `ZoneName` on every child row.
4. Do not resolve, populate, or pass a child `ZoneId`. The published BO relationship resolves the internal parent ID through `ParentUserKeys: OrganizationName,ZoneName`.
5. For Create, require that no default zone exists and set `RestAction` to `POST`. For Update, require that exactly one default zone exists, use the Data Loader update operation, and set `RestAction` to `PATCH`. The loader resolves the registered parent and child user keys to choose the final REST create-or-update action; this skill does not issue the Redwood batch call.
6. Emit exactly one `activityUsages` worksheet row for each of the five activity types, even when task generation is disabled. Set `TasksEnabled` from the user's Yes/No value, populate the mandatory grouping level from the canonical activity matrix in `ora_defaulting_rules.md`, and apply the operation's RestAction to every emitted row.
7. For Update, hydrate the current five activity usages from the read-only default-zone result, overlay only the user's requested values, and preserve the remaining values. This mirrors Redwood, which submits all five usage records in its existing-default-zone upsert.
8. Prepare one immutable parent-root XLSX for Data Loader validation. A parent-only workbook is invalid whenever any of the five activity choices was supplied. `core.data-loader` validates the final immutable upload artifact and owns the sole approval to upload and initiate it; do not request a task-local XLSX approval.

### Explicit FSM Import Contract

When FSM Import is explicitly selected, or the supplied archive contains `ASM_SETUP_CSV_METADATA.xml`, preserve its exported metadata and use only the flattened `ORA_INVENTORY_TASK_CONFIGURATION.csv` columns:

`OrganizationName`, `ParCount`, `CycleCount`, `PhysicalInventory`, `PickConfirm`, and `ReceiptDelivery`.

For this explicit FSM route, map friendly task-generation input to the exact FSM strings `Yes` and `No`. Do not add `activityUsages`, `ZoneName`, `TaskGroupingLevel`, `RestAction`, `ZoneId`, or `ZoneActivityUsageId` to the FSM archive. A successful FSM result reports one `InvZoneTaskConfigurationVO` row; the service owns persistence of its five underlying activity usages.

### FSM Template Policy

When an FSM package must be prepared for this task, use only an empty Inventory
Task Configurations template created by `shared.setup-export.task-level-export`
in `--template-only` mode. Do not use a current-data export as the package
source, do not manufacture `ASM_SETUP_CSV_METADATA.xml`, and do not convert a
loose CSV into an FSM ZIP.

Prefer the latest project-local template-only artifact only when all of these
checks pass:

- its recorded task code is `ORA_INVENTORY_TASK_CONFIGURATIONS`;
- its recorded source environment matches the selected target environment;
- its recorded Fusion release remains compatible with the target;
- its stored fingerprint matches the current ZIP bytes;
- it contains exactly one `ASM_SETUP_CSV_METADATA.xml` marker and the native
  `ORA_INVENTORY_TASK_CONFIGURATION.csv` member with the expected six-column
  header; and
- it contains no exported configuration rows before the requested rows are
  added.

Export a replacement empty template only when no reusable project-local
template exists, a provenance or integrity check fails, the environment or
compatible release changes, the member/header structure changes, or the user
explicitly requests a refresh. Keep a separately requested current-state
baseline export distinct; it must never become the editable FSM package source.

Use this command only when a replacement template is required:

```bash
python3 shared/setup-export/task-level-export/scripts/export_setup_task_csv.py \
  --task-code ORA_INVENTORY_TASK_CONFIGURATIONS \
  --offering-name "Manufacturing and Supply Chain Materials Management" \
  --functional-area-name "Advanced Inventory Management" \
  --project-id "<project_id>" \
  --token-cache auto \
  --template-only \
  --wait-seconds 300 \
  --poll-interval 15
```

Prepare a candidate FSM ZIP by copying the verified template and adding only
the requested data rows to `ORA_INVENTORY_TASK_CONFIGURATION.csv`. Preserve the
metadata XML, CSV header, encoding, member names, and package structure. The
candidate becomes immutable before Task Hook and Data Loader validation; a
changed template or row restarts template validation and the approval workflow.

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

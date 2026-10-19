---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.inventory-management.configure-subinventories"
name: "Configure Subinventories Setup Task Guidance"
description: "Provides task-specific setup guidance for Configure Subinventories under the Inventory Management functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Inventory Management"
functional_area_code: "ORA_WSH_INVENTORY_MGMT"
task_code: "ORA_INV_CONFIGURE_SUBINVENTORIES"
task_name: "Configure Subinventories"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.inventory-management"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObjects:
  - "subinventories"
  - "subinventoryItems"
  - "locatorItems"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/inventory-management/configure-subinventories/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/inventory-management/configure-subinventories/current/"
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

# Configure Subinventories Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Configure Subinventories` under `Inventory Management`.

## Setup Task Skill Contract

- task_code: `ORA_INV_CONFIGURE_SUBINVENTORIES`
- task_name: `Configure Subinventories`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.inventory-management`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Inventory Management`
- functional_area_code: `ORA_WSH_INVENTORY_MGMT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObjects: `subinventories`, `subinventoryItems`, `locatorItems`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Configure Subinventories` under `Inventory Management`.

## Setup Task Metadata

- Task name: `Configure Subinventories`
- Task code: `ORA_INV_CONFIGURE_SUBINVENTORIES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Objects: `subinventories, subinventoryItems, locatorItems`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. When locator rows require an FSM package, obtain or reuse a verified empty template from `shared.setup-export.task-level-export` in template-only mode. Do not use a current-data export as the FSM package source.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Select the object-level import route before preparing an artifact. Use REST by default for eligible registered business objects; use the FSM route for locator rows.
5. Import the resulting REST source or FSM ZIP through `core.data-loader`'s selected governed route.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Inventory Management`
- Setup task name: `Configure Subinventories`
- Setup task code: `ORA_INV_CONFIGURE_SUBINVENTORIES`

## Object-Level Import Routing

`dataloader_import_mode: REST` remains the task-level default. It does not make every child object REST-capable. Select one route for each requested object before artifact preparation.

| Object | Object Role | Supported Routes | Default Route | REST Business Object | Routing Rule |
|---|---|---|---|---|---|
| subinventories | Registered business object | REST, FSM | REST | subinventories | Use REST by default; use FSM only when it is explicitly selected for the requested subinventory data. |
| subinventoryItems | Registered business object | REST, FSM | REST | subinventoryItems | Use REST by default; use FSM only when it is explicitly selected for the requested subinventory-item data. |
| locatorItems | Registered business object | REST, FSM | REST | locatorItems | Use REST by default; use FSM only when it is explicitly selected for the requested locator-item data. |
| locators | Child object of subinventories | FSM | FSM | None | Locator rows are FSM-only. Do not prepare, map, validate, or submit locator-only rows as a REST, REST-BO, DAT, or XLSX Data Loader business-object source. |

For a request containing locators and REST-eligible objects, create separate immutable sources: an FSM ZIP for the locator rows and a REST source only for the selected registered business objects. Do not combine locator rows into a REST source or infer that locatorItems authorizes locators.

### Locator Structure Route Mapping

| Route | User Input | Target Field | Resolution Rule |
|---|---|---|---|
| REST subinventories business object | Locator Structure, `LocatorStructureMeaning`, or Structure Instance Code | `LocatorStructureMeaning` | Resolve the supplied logical value through `resolve_locator_structure_instance` and write the returned `StructureInstanceName`. |
| FSM Subinventories sheet | Locator Structure, `LocatorStructureMeaning`, or Structure Instance Code | `StructureInstanceCode` | Resolve the supplied logical value through `resolve_locator_structure_instance` and write the returned `StructureInstanceCode`. |
| FSM locator sheet | Locator Structure, `LocatorStructureMeaning`, or Structure Instance Code | `StructureInstanceCode` | Resolve the supplied logical value through `resolve_locator_structure_instance` and write the returned `StructureInstanceCode` to each applicable locator row. |

The locator-structure resolver is route-neutral: it returns the canonical `StructureInstanceCode` and `StructureInstanceName` from one enabled locator-structure row. The selected route controls only which returned field is written. The resolver is not applicable only when no Locator Structure value is supplied. If separate name and code inputs are supplied, both must resolve to the same row or validation blocks as conflicting input.

## FSM Locator Template Policy

When locator rows are requested, build their FSM ZIP only from an empty Configure Subinventories template produced by `shared.setup-export.task-level-export` with `--template-only`. Do not call the current-data `setupTaskCSVExports` route as an automatic package-preparation or preflight step, and do not convert a full-data export into the locator template.

Prefer the latest project-local template-only artifact when all of these checks pass:

- its recorded task code is `ORA_INV_CONFIGURE_SUBINVENTORIES`;
- its recorded source environment matches the selected target environment;
- its recorded Fusion release remains compatible with the target;
- its stored fingerprint matches the current ZIP bytes;
- it contains exactly one `ASM_SETUP_CSV_METADATA.xml` marker and the expected task CSV members and headers; and
- it contains no exported current setup-data rows before the requested locator rows are added.

Export a replacement empty template only when no reusable project-local template exists, any provenance or integrity check fails, the environment or compatible release changes, the expected member/header structure changes, or the user explicitly requests a refresh. Keep any separately requested current-configuration baseline export as a distinct artifact; never reuse it as the FSM package source.

Use this command only when a replacement template is required:

```bash
python3 shared/setup-export/task-level-export/scripts/export_setup_task_csv.py \
  --task-code ORA_INV_CONFIGURE_SUBINVENTORIES \
  --offering-name "Manufacturing and Supply Chain Materials Management" \
  --functional-area-name "Inventory Management" \
  --project-id "<project_id>" \
  --token-cache auto \
  --template-only \
  --wait-seconds 300 \
  --poll-interval 15
```


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business objects.

1. Confirm that `subinventories`, `subinventoryItems`, `locatorItems` are the exact registered Data Loader business objects.
2. Generate the default editable XLSX samples through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "subinventories" \
     "subinventoryItems" \
     "locatorItems" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep each business object's generated workbook set together:
   - editable sample workbook
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbooks as the starting point for the later Data Loader preparation and approval workflow.

Do not use this sample workflow for locators. Locator rows are child setup data and require the FSM CSV import route described above.



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

Use the parent functional-area skill `scm.manufacturing-and-supply-chain-materials-management.inventory-management` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

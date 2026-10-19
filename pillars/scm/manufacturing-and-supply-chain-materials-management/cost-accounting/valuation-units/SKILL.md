---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.cost-accounting.valuation-units"
name: "Valuation Units Setup Task Guidance"
description: "Provides task-specific setup guidance for Valuation Units under the Cost Accounting functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Cost Accounting"
functional_area_code: "CST_DEFINE_COST_MANAGEMENT"
task_code: "ORA_CST_VALUATION_UNITS"
task_name: "Valuation Units"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.cost-accounting"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "costAccountingValuationUnits"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/valuation-units/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/valuation-units/current/"
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

# Valuation Units Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Valuation Units` under `Cost Accounting`.

## Setup Task Skill Contract

- task_code: `ORA_CST_VALUATION_UNITS`
- task_name: `Valuation Units`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.cost-accounting`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Cost Accounting`
- functional_area_code: `CST_DEFINE_COST_MANAGEMENT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `costAccountingValuationUnits`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Valuation Units` under `Cost Accounting`.

## Setup Task Metadata

- Task name: `Valuation Units`
- Task code: `ORA_CST_VALUATION_UNITS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `costAccountingValuationUnits`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using costAccountingValuationUnits as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Cost Accounting`
- Setup task name: `Valuation Units`
- Setup task code: `ORA_CST_VALUATION_UNITS`


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `costAccountingValuationUnits` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "costAccountingValuationUnits" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Master and Detail Payload Mapping

`costAccountingValuationUnits` is the Data Loader REST business object for
this task. Use `core.data-loader` to convert the functional payload to the
live-generated workbook and submit it only through that workflow; do not send
direct REST mutation requests.

The supplied payload represents one valuation-unit master and two optional
detail segment values:

```json
{
  "ValuationUnitCode": "Test DKR",
  "costAccountingValuationUnitDetails": [
    {"SegmentValues": "Gujarat\\-CO-00ADELORG"},
    {"SegmentValues": "VisionOps\\-CO-ORG237"}
  ],
  "ValuationStructureId": "<ValuationStructureId>",
  "SetId": "<SetId>",
  "SetName": "<SetName>",
  "CostOrganizationId": "<CostOrganizationId>",
  "CostBookId": "<CostBookId>"
}
```

Prepare a master row for `costAccountingValuationUnits` and a detail row for
each `costAccountingValuationUnitDetails[].SegmentValues` value, using the
parent-child linkage and operation values in the current live Data Loader
template. A manual valuation-unit create must include at least one detail row:
Fusion rejects a master-only source with `CST-2385213`. Do not use a
master-first create followed by a later detail load for this business object.
The detail row must carry the parent linkage required by the live template and
the validated `ValuationUnitCombinationId` for its `SegmentValues` value.

For an existing-master update, resolve exactly one `ValuationUnitId` from the
supplied `ValuationUnitCode`, generate a fresh live-template workbook with
`RestAction` `PATCH`, and populate only the approved changed master fields.
Submit the update only through `core.data-loader` after its fresh preview and
approval gates pass.

For an existing-master deletion, resolve exactly one `ValuationUnitId` from the
supplied `ValuationUnitCode`, generate a fresh live-template workbook with
`RestAction` `DELETE`, and populate only the resolved identity fields required
by the live template. Submit the deletion only through `core.data-loader` after
its fresh preview and explicit approval gates pass.

### Master-detail identity

`ValuationUnitId` is the master surrogate key and the parent key for
`costAccountingValuationUnitDetails`; `ValuationUnitDetailId` is the detail
surrogate key. For a create-with-details source, assign a new nonblank numeric
local surrogate value to the master `ValuationUnitId`, use that exact numeric
value for every child `ValuationUnitId`, and assign a different new numeric
local surrogate value to each `ValuationUnitDetailId`. The values are Data
Loader source references; they are not Fusion-assigned IDs. Validate that the master and each child row
have this live-template parent linkage before preview. For a
later detail load against an existing master, resolve exactly one master by
`ValuationUnitCode`, `CostOrganizationId`, `CostBookId`, and
`ValuationStructureId`, then carry its `ValuationUnitId` in the child row as
required by the current Data Loader template. The REST child
path `/fscmRestApi/resources/11.13.18.05/costAccountingValuationUnits/<ValuationUnitId>/child/costAccountingValuationUnitDetails`
is a read-only mapping reference only; never use it for a mutation.

## Identifier Derivation

Users may provide internal IDs directly. When an ID is absent, use the
task-local read-only lookup contract through
`core.fusion-api.rest-api-client` to derive it before preparing the Data Loader
source:

| Required ID | Accepted Alternate Input | Resolver |
|---|---|---|
| CostOrganizationId | CostOrganizationName or CostOrganizationCode | resolve_cost_organization |
| CostBookId | CostBookCode plus resolved CostOrganizationId | resolve_cost_book |
| ValuationStructureId, SetId, SetName | ValuationStructureCode plus resolved CostOrganizationId | resolve_valuation_structure |

`resolve_valuation_structure` requests the full valuation-structure response without a
`fields` projection. It maps `ValStructureId` to `ValuationStructureId`,
`ValStructureSetId` to `SetId`, and `ValStructureSetName` to `SetName` in the
valuation-unit Data Loader source. These set values are derived from the selected
valuation-structure code; they are not independent mandatory inputs for every
valuation unit.

Every REST request declared by this skill, including all identifier and
structure GET lookups and the validation-only POST, must send
`REST-Framework-Version: 9`. Do not use REST to create, update, or delete
valuation units or details; mutations remain exclusively routed through
`core.data-loader`.

When details are supplied, validate each `SegmentValues` value before preview.
First derive `StructureInstanceNumber` with the read-only request
`/fscmRestApi/resources/11.13.18.05/costAccountingValuationStructures?q=ValStructureId=<ValuationStructureId>`.
Then call the ADF validation action
`/fscmRestApi/resources/11.13.18.05/FlexFndKffApi/action/validateCombination`
with `consumerId`
`oracle.apps.scm.costing.coreSetup.valuationUnits.restModel.view.ValuationUnitDetailsVO#ValUnitKff`,
the derived `structureInstanceNumber`, and the supplied `SegmentValues` as
`combination`. Use `REST-Framework-Version: 9` and
`Content-Type: application/vnd.oracle.adf.action+json`. This POST is
validation-only: it must not create, update, or delete Fusion data. The
combination is valid only when the action response returns a value; no returned
value means invalid and blocks the Data Loader preview and upload.

The ADF `Content-Type` applies only to the
`FlexFndKffApi/action/validateCombination` POST. Do not use it for identifier
or structure GET lookups, or for Data Loader requests.

When an accepted alternate business key is supplied, do not request its
internal ID. Run the corresponding documented lookup instead. If Fusion rejects
that lookup contract or it returns no exact match, report the lookup failure;
do not treat the internal ID as missing input.



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

Use the parent functional-area skill `scm.manufacturing-and-supply-chain-materials-management.cost-accounting` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

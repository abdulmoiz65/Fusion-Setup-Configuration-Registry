---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.cost-accounting.cost-analysis-groups"
name: "Cost Analysis Groups Setup Task Guidance"
description: "Provides task-specific setup guidance for Cost Analysis Groups under the Cost Accounting functional area."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Cost Accounting"
functional_area_code: "CST_DEFINE_COST_MANAGEMENT"
task_code: "ORA_CST_COST_ANALYSIS_GROUPS"
task_name: "Cost Analysis Groups"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.cost-accounting"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "REST"
businessObject: "costAccountingCostAnalysisGroups"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/cost-analysis-groups/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/cost-accounting/cost-analysis-groups/current/"
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

# Cost Analysis Groups Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Cost Analysis Groups` under `Cost Accounting`.

## Setup Task Skill Contract

- task_code: `ORA_CST_COST_ANALYSIS_GROUPS`
- task_name: `Cost Analysis Groups`
- parent_skill_id: `scm.manufacturing-and-supply-chain-materials-management.cost-accounting`
- pillar: `SCM`
- offering: `Manufacturing and Supply Chain Materials Management`
- functional_area: `Cost Accounting`
- functional_area_code: `CST_DEFINE_COST_MANAGEMENT`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `REST`
- businessObject: `costAccountingCostAnalysisGroups`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Cost Analysis Groups` under `Cost Accounting`.

## Setup Task Metadata

- Task name: `Cost Analysis Groups`
- Task code: `ORA_CST_COST_ANALYSIS_GROUPS`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `REST`
- Business Object: `costAccountingCostAnalysisGroups`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader` using costAccountingCostAnalysisGroups as the BusinessObject.

Use this task metadata when invoking those skills:

- Offering: `Manufacturing and Supply Chain Materials Management`
- Functional area / Setup Object: `Cost Accounting`
- Setup task name: `Cost Analysis Groups`
- Setup task code: `ORA_CST_COST_ANALYSIS_GROUPS`

Use `core.fusion-api.rest-api-client` for the task's read-only Fusion REST
lookups. This pillar skill supplies the Cost Analysis Group and Cost Analysis
Code selection rules; the core client owns OAuth, HTTP transport, bounded
read-only retry behavior, and redacted diagnostics.

## REST Payload Guidance

Use `costAccountingCostAnalysisGroups` as the parent REST business object.
Create an analysis group with `AnalysisGroupCode` and, when needed,
`AnalysisGroupDescription`. The `costAccountingCostAnalysisCodes` collection
is optional: a load may create only the analysis group, or may include one or
more child analysis codes in the same reviewed source artifact. Analysis codes
can also be created later through the appropriate child collection workflow.

### Update and delete routes (live-metadata gated)

The skill provides controlled update and delete routes for both the
`costAccountingCostAnalysisGroups` master and its
`costAccountingCostAnalysisCodes` detail records. The requested operation is
permitted only when the live Data Loader template and validation accept it for
the affected section. All operations use the routed `core.data-loader`
workflow; do not issue direct REST `PATCH` or `DELETE` requests from this
skill.

For an **update**, first resolve the existing master by exact
`AnalysisGroupCode`, then retrieve the live Data Loader template and its key
fields with a read-only update sample:

```bash
python3 core/data-loader/scripts/generate_sample_dat.py \
  "costAccountingCostAnalysisGroups" \
  --operation update \
  --output-dir "<project-artifact-directory>"
```

Populate only fields confirmed by that live template. Retain the resolved
master ID and every live key field. For a detail update, require the exact
parent ID and existing `AnalysisCode`; changing either identity value is a
delete-and-create design change, not an update. Preserve the detail
`RestAction` exactly as the live template requires: the established blank
`MERGE` behavior must not be overwritten with an assumed `PATCH`. Retrieve the
complete existing detail set before changing a default flag, and validate that
the resulting set still has exactly one default analysis code.

For a **delete**, first generate and review a read-only delete sample:

```bash
python3 core/data-loader/scripts/generate_sample_dat.py \
  "costAccountingCostAnalysisGroups" \
  --operation delete \
  --output-dir "<project-artifact-directory>"
```

Use the generated template's `RestAction` and live key fields; do not
hand-author an assumed key set. If live validation rejects `DELETE` for either
section, record the unsupported-operation result and stop; the skill must not
substitute a direct REST delete. A detail delete requires the exact parent and
analysis-code identities and must leave the group with exactly one default
code. A master delete requires confirmation from live metadata and read-only
lookups that there are no remaining detail records or dependent references. No
cascade delete is assumed. If a dependency cannot be read or its deletion
behavior is unclear, stop and use the Fusion UI/manual procedure confirmed by
the functional owner.

Deletion is destructive: complete Data Loader validation and present the exact
immutable source preview, target Fusion environment, and operation immediately
before execution. Submit only after the user explicitly approves that preview.

For a create-together load, use the unique `AnalysisGroupCode` as the
parent-child link, in the same way that Valuation Units uses its master code.
Generate the current Data Loader template first and use this pattern only when
that template exposes and accepts the code as the parent-child linkage. Put one
new parent row first and every new child row after it, with the same
`AnalysisGroupCode`; do not require or invent an `AnalysisGroupId` that does
not yet exist.

For child records added to an existing group, resolve `analysisGroupId` first.
The flattened Data Loader workbook must then carry that ID in the matching
parent row and every child row. Never submit an orphan child-only sheet.

### Create a master and children in one request

1. Generate and review the current Data Loader create template for
   `costAccountingCostAnalysisGroups`.
2. Prepare one immutable archive with a parent row and all requested
   `costAccountingCostAnalysisCodes` child rows. Put the parent first and use
   the identical unique `AnalysisGroupCode` in the parent and every child row.
3. Keep child `RestAction` blank so the supported Data Loader `MERGE` behavior
   is used; do not set it to `CREATE`.
4. Validate that the submitted child set has exactly one
   `DefaultAnalysisCodeFlag: "Y"`, then submit the one reviewed archive through
   `core.data-loader` after its normal approval gate.
5. If the live template or validation does not support code-based linkage for
   new parent and child rows, stop before import. Use the master-first fallback:
   create the group, resolve its `analysisGroupId`, then submit a new
   parent-plus-children archive. Do not substitute direct REST writes.

### Create children for an existing master

1. Require the parent `AnalysisGroupCode`.
2. Resolve the group and its `analysisGroupId` through the task-local,
   read-only lookup before creating a source artifact.
3. Retrieve the complete existing child-code set, combine it with the proposed
   children, and require exactly one default code.
4. Place the resolved `AnalysisGroupId` in the parent row and every child row.
   Keep child `RestAction` blank so the supported Data Loader `MERGE` behavior
   is used. Do not use `RestAction: CREATE`: Fusion rejects CREATE for this
   child Data Loader section.
5. Include all proposed new children for the same parent in one
   parent-plus-children workbook. This bulk pattern is supported; processing
   each child in a separate archive is unnecessary.
6. If the group or ID cannot be resolved, stop and ask the functional user to
   verify the group code.

For every `AnalysisGroupCode`, the resulting child-code set must contain
exactly one record with `DefaultAnalysisCodeFlag: "Y"`. Multiple child records
are allowed, but no more than one may be the default. Apply this rule both when
the group and children are created together and when children are added later.
For a child-only addition, first perform the task-local, read-only lookup of
the existing children for the supplied `AnalysisGroupCode`, then validate the
combined existing and proposed child records. Do not prepare a Data Loader
artifact unless the combined set has exactly one default child record. The
required source shape is one parent row plus all proposed child rows, with
blank child `RestAction` values.
This lookup does not apply when the analysis-group master and all requested
children are created together in one source artifact; validate that submitted
child set directly instead.

### Default analysis-code flag conversion

Functional users may express the default selection as `Yes`/`No` or
`True`/`False`. Normalize `Yes` and `True` to `Y`, and normalize `No` and
`False` to `N`, for `DefaultAnalysisCodeFlag`. Preserve the normalized values
as strings all the way through the workbook and DAT conversion; do not rely on
a spreadsheet tool to coerce the field type.

Before presenting an approval preview, inspect every populated child row in
the generated Data Loader source. It is valid only when each
`DefaultAnalysisCodeFlag` is exactly `Y` or `N`; otherwise stop, correct the
source, and regenerate the immutable archive and preview. This is in addition
to checking that exactly one resulting child code is `Y`.

The following reference payload illustrates a group with three optional child
codes. Treat it as a mapping example only; confirm the live Data Loader
metadata and generated workbook headers before preparing a load.

## Functional User Intake

Ask functional users for the setup details in plain text. Do not require JSON,
REST field names, business-object names, or Data Loader file layouts.

Use these questions, adapting them to the user's request:

1. Do you want to create, update, or delete an analysis group or an analysis code?
2. What is the analysis group code you want to create, update, or delete?
3. What description should appear for this analysis group? If no description is needed, say so.
4. Are you changing the analysis group only, or a specific analysis code within it?
5. For each analysis code being created or updated, provide its code and description.
6. Which one analysis code should be the default after the change? There must be exactly one default whenever child records remain.
7. For a delete, confirm the exact group or code identity and acknowledge that the reviewed immutable artifact will be permanently applied only after separate approval.

For a child-only request, ask for the existing analysis group code and explain
that the workflow will first resolve its parent ID and check its current
analysis codes before validating the requested additions. Convert the confirmed
business answers into the Data Loader source only after the task-local
validation and review gates pass. When the user answers `Yes`/`No` or
`True`/`False` for the default question, show the normalized `Y` or `N` values
in the source preview.

```json
{
  "AnalysisGroupCode": "Test FDOS REST",
  "AnalysisGroupDescription": "Test FDOS REST",
  "costAccountingCostAnalysisCodes": [
    {
      "AnalysisCode": "FDOS DIRECT",
      "AnalysisDescription": "FDOS Direct Cost",
      "DefaultAnalysisCodeFlag": "Y"
    },
    {
      "AnalysisCode": "FDOS INDIRECT",
      "AnalysisDescription": "FDOS Indirect Cost",
      "DefaultAnalysisCodeFlag": "N"
    },
    {
      "AnalysisCode": "FDOS OVERHEAD",
      "AnalysisDescription": "FDOS Overhead Cost",
      "DefaultAnalysisCodeFlag": "N"
    }
  ]
}
```


## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `costAccountingCostAnalysisGroups` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "costAccountingCostAnalysisGroups" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

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

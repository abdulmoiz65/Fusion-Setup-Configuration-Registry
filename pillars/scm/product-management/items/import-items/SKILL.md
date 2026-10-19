---
skill_id: "scm.product-management.items.import-items"
name: "Import Items Setup Task Guidance"
description: "Prepares a validated immutable Item Import FBDI ZIP from the current public Oracle template and hands it unchanged to core.data-loader."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "Items"
functional_area_code: "ORA_EGP_FA_ITEMS"
task_code: "EGP_IMPORT_ITEMS"
task_name: "Import Items"
parent_skill_id: "scm.product-management.items"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "FBDI"
businessObject: "item"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "SCM product management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "customer_item_source"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "normalized_item_mapping"
  - "generated_fbdi_zip"
  - "fbdi_preview"
  - "core_data_loader_handoff"
  - "skill_run_record"
  - "token_usage_record"
uses_core:
  - "core.data-loader"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/items/import-items/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/items/import-items/current/"
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

# Import Items Setup Task Guidance

## Purpose

Prepare an Oracle Item Import FBDI package from customer-supplied data. Fetch
the current public Oracle `ItemImportTemplate.xlsm`, map and validate the data
against that template, generate one ordered immutable ZIP, and hand the exact
same ZIP to `core.data-loader` for any later loader operation.

## Setup Task Skill Contract

- task_code: `EGP_IMPORT_ITEMS`
- task_name: `Import Items`
- dataloader_import_mode: `FBDI`
- businessObject: `item`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Preparation and Validation Workflow

Read `ora-resource/ora_fbdi_processing.md`, `ora-resource/ora_input_validation.md`,
`ora-resource/ora_dependency_readiness.md`,
`ora-resource/ora_defaulting_rules.md`,
`ora-resource/ora_error_handling.md`, and
`ora-resource/ora_rule_registry.json` before preparing a package.

1. Accept customer item data or a prebuilt FBDI ZIP. Treat supplied facts as
   evidence, not as Oracle-ready mappings.
2. Fetch the current public Oracle `ItemImportTemplate.xlsm` for this run.
   Record its public page and workbook URLs, retrieval time, SHA-256 digest,
   and sheet sequence. Never use remembered or stale layout details.
3. Map each source fact to the current template. Resolve every required or
   ambiguous business value before generating CSV files. Apply documented
   defaults only where the task resources permit them.
4. Generate headerless CSV members using the template's prescribed filenames,
   columns, field order, encoding, and ZIP-member order. Create the ZIP only
   in a customer-approved or controlled transient location.
5. Reopen and validate the ZIP against the same template: safe root-level
   members, exact member names and order, field counts including trailing empty
   fields, data types and constraints, coherent references, one numeric Batch
   ID, and SHA-256-bound preview.
6. Hand the validated ZIP unchanged to `core.data-loader` with task context,
   registered business object `item`, template provenance, ZIP digest, member
   manifest, row counts, mapping preview, and Batch ID.

## Immutable Handoff Boundary

The ZIP bytes, basename, members, member order, and SHA-256 digest must remain
unchanged after validation. Any alteration requires a new template-driven
validation cycle.

This skill must not upload the ZIP, call an ESS job, initiate or monitor an
import, poll a request, or directly call a Fusion execution endpoint. It must
not invoke a product-specific loader or construct transport parameters.
`core.data-loader` exclusively owns any subsequent validation, approval,
upload, import initiation, monitoring, and diagnostics.

## Outputs

Return local validation results and the immutable handoff evidence. Do not
store raw customer rows, intermediate CSVs, workbook copies containing customer
data, or the generated ZIP in the repository or project workspace.

## Boundaries

- Use Item Import FBDI; do not route through FSM CSV import.
- Do not invent missing customer values or silently discard source facts.
- Do not expose credentials, tokens, authorization headers, or UCM details.
- Use the parent skill `scm.product-management.items` for functional-area
  sequencing and scope decisions.
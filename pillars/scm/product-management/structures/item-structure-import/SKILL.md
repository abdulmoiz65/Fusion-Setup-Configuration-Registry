---
skill_id: "scm.product-management.structures.item-structure-import"
name: "Item Structure Import Setup Task Guidance"
description: "Prepares a validated immutable Item Structure Import FBDI ZIP from the current public Oracle template and hands it unchanged to core.data-loader."
layer: "pillar"
pillar: "SCM"
offering: "Product Management"
functional_area: "Structures"
functional_area_code: "EGO_ADVANCED_PRODUCT_STRUCT"
task_code: "CUSTOM_EGP_FBDI_IMPORT_STRUCTURES"
task_name: "Item Structure Import"
parent_skill_id: "scm.product-management.structures"
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
  - "customer_item_structure_source"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "normalized_item_structure_mapping"
  - "generated_fbdi_zip"
  - "fbdi_preview"
  - "core_data_loader_handoff"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.data-loader"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/structures/item-structure-import/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/product-management/structures/item-structure-import/current/"
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

# Item Structure Import Setup Task Guidance

## Purpose

Prepare an Oracle Item Structure Import FBDI package from customer-supplied
data. Fetch the latest release-compatible public Oracle
`ItemStructureImportTemplate.xlsm`, map and validate the data against that
template, generate one ordered immutable ZIP, and hand the exact same ZIP to
`core.data-loader` for any later loader operation.

## Setup Task Skill Contract

- task_code: `CUSTOM_EGP_FBDI_IMPORT_STRUCTURES`
- task_name: `Item Structure Import`
- parent_skill_id: `scm.product-management.structures`
- pillar: `SCM`
- offering: `Product Management`
- functional_area: `Structures`
- functional_area_code: `EGO_ADVANCED_PRODUCT_STRUCT`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `FBDI`
- businessObject: `item`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Item Structure Import` under `Structures`.

## Setup Task Metadata

- Task name: `Item Structure Import`
- Task code: `CUSTOM_EGP_FBDI_IMPORT_STRUCTURES`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `FBDI`
- Business Object: `item`

## Preparation and Validation Workflow

Read `ora-resource/ora_fbdi_processing.md`,
`ora-resource/ora_input_validation.md`,
`ora-resource/ora_dependency_readiness.md`,
`ora-resource/ora_defaulting_rules.md`,
`ora-resource/ora_error_handling.md`, and
`ora-resource/ora_rule_registry.json` before preparing a package.

1. Fetch the latest release-compatible public Oracle
   `ItemStructureImportTemplate.xlsm` in this run. Record the public page and
   template URLs, applicable Oracle release, retrieval time, SHA-256 digest,
   and workbook sheet sequence. Never rely on remembered, stale, or
   cross-release layout details.
2. Accept customer item-structure data or a prebuilt FBDI ZIP. Treat supplied
   facts as evidence, not as Oracle-ready mappings. Resolve missing, required,
   or ambiguous business values before generation; do not invent or silently
   discard source facts.
3. Before mapping, reject overlapping effective-date ranges for a repeated
   component on the same structure. Require every reference-designator
   effectivity date to match its component effectivity date; when importing
   reference designators or substitute components, include their parent
   component in the same package.
4. Map the validated source to the current template. Treat the workbook's
   sheets, technical columns, required markers, types, validations, allowed
   values, prescribed CSV filenames, field order, encoding, delimiter,
   quoting, null convention, and ZIP-member order as the sole schema authority
   for the run. Produce headerless CSV members only for populated interface
   sheets.
5. Generate a single ordered ZIP only in a customer-approved or controlled
   transient location. Reopen it and validate safe root-level members, no
   duplicates or unexpected files, exact template-prescribed names and order,
   headerless rows with exact field counts including trailing empty fields,
   current-template types and constraints, coherent parent/component,
   substitute-component, and reference-designator links, one numeric Batch ID,
   and a SHA-256-bound preview. Stop as template drift if the workbook's sheet
   sequence, CSV export contract, or prescribed filenames differ from the
   task's established package contract.
6. Hand the validated ZIP unchanged to `core.data-loader` with the task
   context, registered FBDI Data Loader business object `item`, template
   provenance, ZIP digest, member manifest, row counts, mapping preview, and
   Batch ID.

## Immutable Handoff Boundary

The ZIP bytes, basename, members, member order, and SHA-256 digest must remain
unchanged after validation. Any alteration requires a new template-driven
validation cycle.

This skill must not upload the ZIP, call an ESS job, initiate or monitor an
import, poll a request, or directly call a Fusion execution endpoint. It must
not invoke a product-specific loader or construct transport parameters.
`core.data-loader` exclusively owns any subsequent validation, approval,
upload, import initiation, monitoring, and diagnostics.

## Preflight, Failure Handling, and Redaction

Before generating a ZIP, verify the readable source, latest compatible
template provenance, complete mapping, structure-specific validation results,
and controlled transient output location. Stop before handoff when any
preflight check fails.

Classify local failures as input validation, catalog mismatch, or artifact
persistence. Do not retry a failed validation with unchanged input; correct the
identified issue and restart the template-driven validation cycle. This skill
does not poll or invoke a live operation, so timeout and live-mutation retry
policies belong to `core.data-loader`.

Never print or persist credentials, tokens, authorization headers, UCM details,
raw customer rows, or intermediate CSV data. Redact sensitive values from the
mapping preview and handoff evidence.

## Outputs

Return local validation results and immutable handoff evidence. Do not store
raw customer rows, intermediate CSVs, workbook copies containing customer data,
or the generated ZIP in the repository or project workspace.

## Boundaries

- Use Item Structure Import FBDI; do not route through FSM CSV import.
- Do not expose credentials, tokens, authorization headers, UCM details, or
  customer data.
- Use the parent skill `scm.product-management.structures` for functional-area
  sequencing and scope decisions.

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

Use the parent functional-area skill `scm.product-management.structures` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

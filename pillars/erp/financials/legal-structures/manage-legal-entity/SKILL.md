---
skill_id: "erp.financials.legal-structures.manage-legal-entity"
name: "Manage Legal Entity Setup Task Guidance"
description: "Provides task-specific setup guidance for Manage Legal Entity under the Legal Structures functional area."
layer: "pillar"
pillar: "ERP"
offering: "Financials"
functional_area: "Legal Structures"
functional_area_code: "ORA_ASK_LEGAL_STRUCTURES"
task_code: "XLE_MANAGE_LEGAL_ENTITY"
task_name: "Manage Legal Entity"
parent_skill_id: "erp.financials.legal-structures"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "ERP financials pillar team"
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
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/legal-structures/manage-legal-entity/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/erp/financials/legal-structures/manage-legal-entity/current/"
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
  - "Performs routed read-only Fusion reference lookups and prepares local FSM archives; core.data-loader owns approved upload and import."
required_privileges:
  - "Read access to the territory, address-geography, jurisdiction, legal-entity, and optional parent PSU references used by the applicable branch."
---

# Manage Legal Entity Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Manage Legal Entity` under `Legal Structures`.

## Setup Task Skill Contract

- task_code: `XLE_MANAGE_LEGAL_ENTITY`
- task_name: `Manage Legal Entity`
- parent_skill_id: `erp.financials.legal-structures`
- pillar: `ERP`
- offering: `Financials`
- functional_area: `Legal Structures`
- functional_area_code: `ORA_ASK_LEGAL_STRUCTURES`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Manage Legal Entity` under `Legal Structures`.

### Country and Identifying Jurisdiction

Load [the reference lookup rules](ora-resource/ora_reference_lookups.md) and
[the country/default mappings](ora-resource/ora_defaulting_rules.md) before
resolving a CREATE candidate. Use `territoriesLOV` followed by the minimal-field
`addressGeographies` country lookup. The selected primary country's
`GeographyValue` supplies `GeographyName`; retain `TerritoryShortName` separately.
The address lookup does not expose `GeographyId`, and obtaining a country ID is
not a prerequisite for this flow.

Reuse the user's identifying-jurisdiction name/search text or ask for it when
missing. Resolve it with `legalJurisdictionsLOV`, obtain an explicit choice if
multiple eligible records match, and verify the selected exact import name is
unambiguous. Name, identifying flag, and effective-date checks do not independently
prove jurisdiction-to-country association. Preserve that disclosure and the
documented `GeographyElement1` derivation limit in the package preview.

These lookups run only at the existing `LE.RESOLVE_REFERENCES` step through the
declared REST client and selected environment. The changes apply to the main LRU
and registration rows authored within this LE aggregate; they do not alter the
separate Manage Legal Reporting Unit or Manage Legal Jurisdictions skills.

## Setup Task Metadata

- Task name: `Manage Legal Entity`
- Task code: `XLE_MANAGE_LEGAL_ENTITY`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Load the task-local `ora-resource/ora_rule_registry.json` and run its referenced input, lookup, dependency, defaulting, design, error-handling, and final-package-readiness checks. The ora-resource graph validates the candidate; it does not create a Fusion mutation.
5. Prepare the FSM archive locally using the contract below.
6. Hand the exact final archive to `core.data-loader` only after the local workflow returns `READY_FOR_DATA_LOADER_PREVIEW`.

Use this task metadata when invoking those skills:

- Offering: `Financials`
- Functional area / Setup Object: `Legal Structures`
- Setup task name: `Manage Legal Entity`
- Setup task code: `XLE_MANAGE_LEGAL_ENTITY`

### Local-Only FSM Package Preparation

This assisted workflow prepares a package locally and stops before upload or any Fusion mutation.

1. Require a fresh, same-target, same-release, successful same-task FSM export as the immutable baseline. Bind the exact environment and task identity, current `ASM_SETUP_CSV_METADATA.xml`, the exact current entity-tree hierarchy and all six CSV members, exact header spelling and order, and the exported encoding.
2. Re-run the complete task ora-resource graph against the reviewed inputs and baseline. Fail closed with a task-specific package-contract gap if any source, mapping, value, member hierarchy, header, encoding, carrier, or aggregate rule is missing or ambiguous; do not invent a package contract.
3. Build the smallest supported UI-equivalent semantic delta from the task resources: the legal-entity root, its same-name main legal reporting unit, its identifying legal-entity registration, and the identifying main-LRU registration. Preserve all six current CSV members, all required unchanged parent rows, every unrelated row, and every untouched archive member. Preserve existing registration-function rows unchanged and add zero candidate function rows. Keep a registration-function member header-only only when it is already header-only in the baseline.
4. Do not copy physical IDs, audit fields, object-version fields, ESS fields, or service-owned values from the baseline or another row. Copy a value only when the task resources explicitly authorize it as a carrier.
5. Produce a ZIP-valid immutable FSM archive, its SHA-256 digest, a member inventory, a row/member semantic diff against the baseline, and a sanitized package-preparation receipt containing no secrets or sensitive payload values.
6. Any source, mapping, value, package byte, member inventory, or hash change invalidates this preview state and requires the full validation and package-preparation workflow to run again.
7. On success, return `READY_FOR_DATA_LOADER_PREVIEW`. Do not claim `READY_FOR_IMPORT` or approval. Stop before upload or mutation and hand the exact immutable archive to `core.data-loader`, which owns Task Hook validation, preview, explicit approval, archive-hash verification, upload, and initiation.


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

Use the parent functional-area skill `erp.financials.legal-structures` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

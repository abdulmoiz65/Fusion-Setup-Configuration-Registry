---
skill_id: "hcm.recruiting.recruiting-foundation.geography-hierarchy-structure"
name: "Geography Hierarchy Structure Setup Task Guidance"
description: "Reads and explains configured country hierarchy levels and provides FSM package guidance for Geography Hierarchy Structure under Recruiting Foundation."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Foundation"
functional_area_code: "ORA_RECRUITING_FOUNDATION_DATA"
task_code: "ORA_IRC_GEO_HRCHY_STRUCTURE"
task_name: "Geography Hierarchy Structure"
parent_skill_id: "hcm.recruiting.recruiting-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "HCM recruiting pillar team"
version: "0.2.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "validated_fsm_package"
  - "immutable_import_preview"
  - "post_import_verification"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-foundation/geography-hierarchy-structure/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-foundation/geography-hierarchy-structure/current/"
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
  - "Delegates an explicitly requested, validated, and approved FSM CSV import to core.data-loader."
required_privileges:
  - "FSM import privileges are required only for an explicitly requested package import."
---

# Geography Hierarchy Structure Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Geography Hierarchy Structure` under `Recruiting Foundation`.

## Setup Task Skill Contract

- task_code: `ORA_IRC_GEO_HRCHY_STRUCTURE`
- task_name: `Geography Hierarchy Structure`
- parent_skill_id: `hcm.recruiting.recruiting-foundation`
- pillar: `HCM`
- offering: `Recruiting`
- functional_area: `Recruiting Foundation`
- functional_area_code: `ORA_RECRUITING_FOUNDATION_DATA`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Geography Hierarchy Structure` under `Recruiting Foundation`.

## Scope Boundary

Use this task to define the allowed geography levels for one country. It changes the country-level mapping used by hierarchy-node packages; it does not create a named hierarchy or master geography nodes.

## Read and Explain Configured Levels (POC)

For a request to show a country's configured levels, obtain its current row through
`shared.setup-export.task-level-export` in data mode in the selected environment.
Do not use a template, a previous import draft, or another country's row as current
configuration. Preserve the export evidence and select exactly one CountryCode row.
Then follow the read branch in `ora_input_validation.md` and
`ora_reference_lookups.md`, using `core.fusion-api.rest-api-client` for the declared
read-only lookup. This branch requires neither an import ZIP nor import approval
and must not enter the package/import branch.

The address-format lookup is a POC/demo interpretation of the configured element
numbers, not a general replacement for geography-structure metadata. Report labels
alongside the unchanged configured element values, disclose unresolved labels,
and do not use this lookup alone to generate or change a country mapping.

## Package Preparation

1. Start from the target country's task-native FSM export or template.
2. Include only the intended country and its approved level mapping. Do not use Postal Code as a mapped level.
3. Require approved country and level-mapping evidence. A level-three mapping requires a populated level-two mapping.
4. When updating an export, preserve existing control values unless the approved design explicitly changes them. For a first-time country, do not invent control values.
5. Validate the exact archive before approval, then re-export the country structure after a successful import before using it as evidence for a dependent hierarchy package.

An import is permitted only after the exact ZIP and target environment are validated and explicitly approved immediately before `core.data-loader` is invoked. Inspect the detailed FSM process log after import; a top-level success alone is not completion evidence.

## Task-Local Resource Read Order

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_dependency_readiness.md`
3. `ora-resource/ora_reference_lookups.md` (configured-level read requests)
4. `ora-resource/ora_defaulting_rules.md`
5. `ora-resource/ora_design_enforcement.md`
6. `ora-resource/ora_error_handling.md`
7. `ora-resource/ora_rule_registry.json`

## Preflight

Before any import preview, confirm the task code and CSV support flags, exact target environment, required FSM import privilege, task-native ZIP structure, approved country and level mapping, and one-country scope. Treat an unsupported artifact, missing evidence, ambiguous target, or absent approval as a blocker.

## Failure Handling

Classify failures as input validation, catalog or metadata mismatch, authorization or privilege, transport or environment, process timeout, process failed, artifact persistence, or approval blocker. Do not retry an import automatically. Retrieve the detailed FSM process log when available and retain sanitized diagnostics and artifact references under the project workspace.

## Redaction

Never print or persist credentials, tokens, token caches, private keys, full base64 payloads, or sensitive tenant data. Keep only sanitized package fingerprints, environment identity, validation results, and external request identifiers in project evidence.

## Setup Task Metadata

- Task name: `Geography Hierarchy Structure`
- Task code: `ORA_IRC_GEO_HRCHY_STRUCTURE`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task, so route task setup data work through the relevant skills:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import setup task data with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Recruiting`
- Functional area / Setup Object: `Recruiting Foundation`
- Setup task name: `Geography Hierarchy Structure`
- Setup task code: `ORA_IRC_GEO_HRCHY_STRUCTURE`




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

Use the parent functional-area skill `hcm.recruiting.recruiting-foundation` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

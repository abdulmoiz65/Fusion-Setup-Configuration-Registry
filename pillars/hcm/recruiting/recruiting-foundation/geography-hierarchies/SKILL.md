---
skill_id: "hcm.recruiting.recruiting-foundation.geography-hierarchies"
name: "Geography Hierarchies Setup Task Guidance"
description: "Provides task-specific setup guidance for Geography Hierarchies under the Recruiting Foundation functional area."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Foundation"
functional_area_code: "ORA_RECRUITING_FOUNDATION_DATA"
task_code: "ORA_IRC_GEO_HRCHY"
task_name: "Geography Hierarchies"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-foundation/geography-hierarchies/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-foundation/geography-hierarchies/current/"
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

# Geography Hierarchies Setup Task Guidance

## Purpose

Provides task-specific setup planning, routing, export, import, and validation guidance for `Geography Hierarchies` under `Recruiting Foundation`.

## Setup Task Skill Contract

- task_code: `ORA_IRC_GEO_HRCHY`
- task_name: `Geography Hierarchies`
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

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Geography Hierarchies` under `Recruiting Foundation`.

## Scope Boundary

Use this task to create or change one named hierarchy from existing master geographies. It does not create master geography records or change a country's permitted geography-level mapping.

## Package Preparation

1. Start from a task-native FSM export or template; do not substitute an XML, JUnit migration ZIP, or a Setup and Maintenance configuration package.
2. Keep one approved hierarchy and its intended node tree in each package.
3. Require authoritative evidence for every geography element, parent relationship, and master-geography identifier before preparing a node row. Do not guess codes, spelling, accents, identifiers, or parentage.
4. Use unique, nonblank package-local `GeoNodeCode` values and link each child with its immediate parent's `ParentGeoNodeCode`.
5. Include one hierarchy identifier row for every imported node. The identifier name, hierarchy name, node code, and status must agree with the hierarchy and node data.
6. Validate CSV field counts before packaging: three hierarchy fields, 25 node fields, and six identifier fields. Preserve the matching task-native archive structure.

An import is permitted only after the exact ZIP and target environment are validated and explicitly approved immediately before `core.data-loader` is invoked. After the import, inspect the detailed FSM process log and verify the target hierarchy through the UI or a re-export. A top-level success alone is not completion evidence.

## Task-Local Resource Read Order

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_dependency_readiness.md`
3. `ora-resource/ora_defaulting_rules.md`
4. `ora-resource/ora_design_enforcement.md`
5. `ora-resource/ora_error_handling.md`
6. `ora-resource/ora_rule_registry.json`

## Preflight

Before any import preview, confirm the task code and CSV support flags, exact target environment, required FSM import privilege, task-native ZIP structure, CSV field counts, authoritative geography evidence, and one-hierarchy scope. Treat an unsupported artifact, missing evidence, ambiguous target, or absent approval as a blocker.

## Failure Handling

Classify failures as input validation, catalog or metadata mismatch, authorization or privilege, transport or environment, process timeout, process failed, artifact persistence, or approval blocker. Do not retry an import automatically. Retrieve the detailed FSM process log when available and retain sanitized diagnostics and artifact references under the project workspace.

## Redaction

Never print or persist credentials, tokens, token caches, private keys, full base64 payloads, or sensitive tenant data. Keep only sanitized package fingerprints, environment identity, validation results, and external request identifiers in project evidence.

## Setup Task Metadata

- Task name: `Geography Hierarchies`
- Task code: `ORA_IRC_GEO_HRCHY`
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
- Setup task name: `Geography Hierarchies`
- Setup task code: `ORA_IRC_GEO_HRCHY`




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

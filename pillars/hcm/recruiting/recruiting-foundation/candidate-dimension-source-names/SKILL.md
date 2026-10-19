---
skill_id: "hcm.recruiting.recruiting-foundation.candidate-dimension-source-names"
name: "Candidate Dimension Source Names Setup Task Guidance"
description: "Retrieves fresh Candidate Dimension Source Names through the shared task export workflow and prepares source-grounded Add Row or one-cell Name rename packages for approved FSM import through core.data-loader."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Foundation"
functional_area_code: "ORA_RECRUITING_FOUNDATION_DATA"
task_code: "ORA_MANAGE_CANDIDATE_DIMENSION_SOURCE_NAMES"
task_name: "Candidate Dimension Source Names"
parent_skill_id: "hcm.recruiting.recruiting-foundation"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM recruiting pillar team"
inputs:
  - "request"
  - "project_context"
  - "fusion_environment_context"
  - "setup_data_artifacts"
outputs:
  - "source_names"
  - "validation_results"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
  - "core.data-loader.task-hook"
uses_core:
  - "core.auth.fusion-oauth-authentication"
persists_project_state: true
state_updates:
  - "exports"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_export"
    default_location: "project/{project_id}/exports/recruiting/recruiting-foundation/candidate-dimension-source-names/"
    versioning_policy: "append-only"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
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
side_effects:
  - "Delegates fresh Fusion setup task export creation, polling, and download to shared.setup-export.task-level-export."
  - "Writes export evidence and run diagnostics to the active project workspace."
  - "Delegates an approved export-derived Add Row or Name rename archive to core.data-loader for FSM import."
required_privileges:
  - "Fusion privileges to discover and export Candidate Dimension Source Names setup data"
  - "Fusion privileges to import setup data through Data Loader"
---

# Candidate Dimension Source Names

Use only Oracle Recruiting > Recruiting Foundation > Candidate Dimension Source Names
(`ORA_MANAGE_CANDIDATE_DIMENSION_SOURCE_NAMES`). Preserve this task's retrieval,
Name rename and Add Row functionality through the shared FSM workflow.

## Supported work

- Retrieve Display Sequence, Name and Source URL from a fresh task export.
- Rename one exact exported source by changing its source-language SourceDisplayName.
- Add one direct source with an explicit Name and Source URL.
- Inspect Translation Editor requirements using verified task UI evidence. Translation
  writes, existing URL changes, reorder, removal and bulk maintenance have no verified
  import contract here.

## CSV Export, Import, and Validation Workflow

1. Read input validation and dependency readiness for the requested operation. Use
   the selected environment profile and OAuth token cache throughout. A live retrieval
   does not require a pre-existing export or an application browser session.
2. Delegate fresh normal data export to `shared.setup-export.task-level-export`.
   Use its task discovery, CSV capability checks, process receipt, polling and download.
   Follow the lookup resource to validate and interpret that exact completed export.
3. Use the compiled task plan and its source resources for task-specific checks.
   For rename or Add Row, prepare a new export-derived candidate using the mappings
   in design enforcement and defaulting rules; retain the baseline unchanged.
   Package preparation is agent-assisted artifact work, not a separate pillar runtime.
4. Validate through `shared.validation.setup-data-validator`, and use
   `shared.validation.reference-data-validator` when reference validation is applicable.
   Delegate normal FSM validation, Task Hook evaluation, immutable preview, approval,
   upload and initiation to `core.data-loader`. The approval rules of that skill apply.
5. Reconcile the detailed import result and perform a fresh task export when verifying
   persistence. Accepted initiation alone is not a completed rename or creation.

During internal `validate_import`, the Task Hook evaluates the supplied completed
baseline, final candidate and exact request. All lookups use those existing artifacts;
do not create another export, invoke the loader recursively, or submit anything.
The task graph returns validation findings to the shared/core caller; it does not
implement upload, OAuth or FSM execution itself.

Keep temporary preparation work and validation evidence under the active project's
artifact area. Do not add skill-local executable helpers or payload templates.
Do not guess package headers, identities or missing source rows, call product REST
or database writes directly, or switch to browser Save for an import request.
Browser use is limited to OAuth sign-in or an explicitly requested UI inspection.

## Task-local resources

- [Input validation](ora-resource/ora_input_validation.md): operation and field contracts.
- [Dependency readiness](ora-resource/ora_dependency_readiness.md): shared services and evidence.
- [Reference lookups](ora-resource/ora_reference_lookups.md): export, language mapping and product sources.
- [Defaulting rules](ora-resource/ora_defaulting_rules.md): direct-source fields and blank sequence.
- [Design enforcement](ora-resource/ora_design_enforcement.md): preparation and preservation checks.
- [Error handling](ora-resource/ora_error_handling.md): preview, approval and result gates.
- [Rule registry](ora-resource/ora_rule_registry.json): compiled task validation graph.

---
skill_id: "hcm.recruiting.recruiting-configuration.recruiting-and-candidate-experience-profile-option-values"
name: "Recruiting and Candidate Experience Profile Option Values Setup Task Guidance"
description: "Reviews Recruiting-owned profile options and safely manages supported Site, Product, or User configured values through the shared Common Profile Options capability."
layer: "pillar"
pillar: "HCM"
offering: "Recruiting"
functional_area: "Recruiting Configuration"
functional_area_code: "ORA_RECRUITING_CONFIGURATION"
task_code: "ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_PROFILE_OPTION_VALUES"
task_name: "Recruiting and Candidate Experience Profile Option Values"
parent_skill_id: "hcm.recruiting.recruiting-configuration"
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
  - "requested_business_change"
  - "target_environment"
  - "approved_profile_option_ownership_crosswalk"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "recruiting_profile_option_review"
  - "immutable_configured_value_preview"
  - "post_change_verification"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.fusion-api.apps-common.profile-options"
  - "shared.setup-export.task-level-export"
  - "shared.validation.setup-data-validator"
  - "shared.validation.reference-data-validator"
  - "core.data-loader"
uses_core:
  - "core.fusion-api.apps-common.profile-options"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-configuration/recruiting-and-candidate-experience-profile-option-values/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/recruiting/recruiting-configuration/recruiting-and-candidate-experience-profile-option-values/current/"
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
  - "Delegates one explicitly approved supported Site-, Product-, or User-level configured-value create, update, or delete to core.fusion-api.apps-common.profile-options."
  - "Delegates an explicitly requested, validated, and approved FSM CSV import to core.data-loader."
required_privileges:
  - "FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV for configured-value mutation in the selected Fusion environment."
  - "Read access required by core.fusion-api.apps-common.profile-options for effective values, definitions, configured values, and profile-user resolution."
  - "FSM import privileges are required only for an explicitly requested CSV import package."
---

# Recruiting and Candidate Experience Profile Option Values Setup Task Guidance

## Purpose

Provides a business-first hybrid wrapper for reviewing Recruiting and Candidate Experience profile options and managing supported configured values. The shared Common Profile Options skill owns transport, authentication, reads, user resolution, and configured-value CRUD; this wrapper owns Recruiting evidence, level/scope enforcement, definition boundaries, approval, verification, redaction, and project audit rules.

## Setup Task Skill Contract

- task_code: `ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_PROFILE_OPTION_VALUES`
- task_name: `Recruiting and Candidate Experience Profile Option Values`
- parent_skill_id: `hcm.recruiting.recruiting-configuration`
- pillar: `HCM`
- offering: `Recruiting`
- functional_area: `Recruiting Configuration`
- functional_area_code: `ORA_RECRUITING_CONFIGURATION`
- available_flag: `Y`
- export_import_supported_flag: `Y`
- csv_export_import_supported_flag: `Y`
- dataloader_import_mode: `FSM`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, sequencing, exporting, importing, or validating setup data for `Recruiting and Candidate Experience Profile Option Values` under `Recruiting Configuration`.

## Hybrid Wrapper Contract

- Begin with the desired Recruiting outcome, affected experience, intended users, timing, and requested profile-value behavior.
- Require a separately approved, current, versioned ownership crosswalk that maps one exact ProfileOptionName to one ModuleId in the complete task-local Recruiting allowlist. The ModuleId baseline alone is insufficient, and ownership must never be inferred from names, descriptions, prefixes, effective values, or configured values.
- Delegate effective-value reads for the authenticated current session, exact definition reads, level-specific configured-value reads and supported CRUD, and user identity/GUID resolution to `core.fusion-api.apps-common.profile-options`.
- Treat profile-option definitions as read-only. Permit only currently enabled and updatable Site, Product, or User configured child changes after exact identity, scope, preservation, sensitive-data, immutable-preview, and approval checks pass.
- Use only `SITE` for Site scope, an exact technical application key from approved evidence for Product scope, and the provider-resolved exact User identity/GUID for User scope.
- Never construct REST URLs, call curl, manage OAuth, use browser automation against Fusion, duplicate provider transport, or use FSM/export/import to bypass an unsupported request.
- Persist only sanitized run, approval, diagnostic, and token-usage evidence; redact sensitive configured values.

## Preflight

Before any external operation, validate the business request, exact target environment, current identity and privilege, complete ModuleId baseline, approved current ownership crosswalk, exact ProfileOptionName, selected level and scope, current definition metadata, current configured state, supported delta, project artifact destinations, and required approval state. Fail closed before side effects when any value is missing, stale, ambiguous, unsupported, unsafe, or cannot be persisted.

## Error Handling

Classify failures using `ora-resource/ora_error_handling.md`, disclose them in business language with sensitive values redacted, and persist only sanitized diagnostics. Permit the delegated provider's single cached-token refresh for a recoverable 401/403, but never retry an uncertain create, update, or delete. A failed or mismatched verification stops completion and does not authorize a corrective mutation.

## Task-Local Resource Read Order

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_dependency_readiness.md`
3. `ora-resource/ora_reference_lookups.md`
4. `ora-resource/ora_design_enforcement.md`
5. `ora-resource/ora_error_handling.md`
6. `ora-resource/ora_rule_registry.json`

The compiled registry is an execution handoff, not ownership evidence or mutation authorization. Missing, stale, ambiguous, or unmapped crosswalk evidence blocks runtime use. Follow the exact task-specific approval gate immediately before delegating one configured-value mutation.

## Setup Task Metadata

- Task name: `Recruiting and Candidate Experience Profile Option Values`
- Task code: `ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_PROFILE_OPTION_VALUES`
- Available: `Y`
- Export/import supported: `Y`
- CSV export/import supported: `Y`
- CSV export/import routing: `supported`
- Data Loader import mode: `FSM`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `Y` for this task. Use these routes only when the user explicitly requests task-level CSV export or an FSM CSV import package; they are not the default route for effective-value review, definition review, or configured-value CRUD:

1. Export setup task data with `shared.setup-export.task-level-export`.
2. Validate setup task data with `shared.validation.setup-data-validator`.
3. Validate reference data with `shared.validation.reference-data-validator`.
4. Import only an explicitly requested, validated, and approved FSM CSV package with `core.data-loader`.

Use this task metadata when invoking those skills:

- Offering: `Recruiting`
- Functional area / Setup Object: `Recruiting Configuration`
- Setup task name: `Recruiting and Candidate Experience Profile Option Values`
- Setup task code: `ORA_IRC_MANAGE_RECRUITING_AND_CANDIDATE_EXPERIENCE_PROFILE_OPTION_VALUES`




## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`
- `requested_business_change`
- `target_environment`
- `approved_profile_option_ownership_crosswalk`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `recruiting_profile_option_review`
- `immutable_configured_value_preview`
- `post_change_verification`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `hcm.recruiting.recruiting-configuration` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

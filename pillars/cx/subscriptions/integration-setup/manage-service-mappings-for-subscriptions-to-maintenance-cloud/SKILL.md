---
skill_id: "cx.subscriptions.integration-setup.manage-service-mappings-for-subscriptions-to-maintenance-cloud"
name: "Manage Service Mappings for Subscriptions to Maintenance Cloud Setup Task Guidance"
description: "Companion advisory workflow for Subscription Maintenance Program Integration Service Mapping source, describe-backed alias, access, and publication questions. Returns source-resolution results to the primary Algorithms skill."
layer: "pillar"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Integration Setup"
functional_area_code: "CUSTOM_INTEGRATION_SETUP"
task_code: "CUSTOM_MANAGE_SERVICE_MAPPINGS_FOR_SUBSCRIPTIONS_TO_MAINTENANCE_CLOUD"
task_name: "Manage Service Mappings for Subscriptions to Maintenance Cloud"
parent_skill_id: "cx.subscriptions.integration-setup"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "advisory"
execution_mode: "advisory"
owner_team: "CX subscriptions pillar team"
version: "0.1.6"
inputs:
  - "business_requirement"
  - "algorithm_bo_xml"
  - "maintenance_program_interface_source_xml"
  - "requested_source_attributes"
  - "implementation_project_context"
outputs:
  - "service_mapping_assessment"
  - "source_resolution_record"
  - "service_mapping_configuration_handoff"
  - "mapping_prerequisites"
  - "validation_result"
  - "skill_run_record"
  - "token_usage_record"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/integration-setup/manage-service-mappings-for-subscriptions-to-maintenance-cloud/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/integration-setup/manage-service-mappings-for-subscriptions-to-maintenance-cloud/current/"
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

# Manage Service Mappings for Subscriptions to Maintenance Cloud Setup Task Guidance

## Purpose

Provides companion advisory guidance for Service Mapping source evidence, source-resolution records, source alias assumptions, access prerequisites, and configuration handoff for `Subscription Maintenance Program Integration`.

## Companion Workflow and Return

This is the companion workflow for the primary `cx.subscriptions.integration-setup.manage-algorithms-for-subscriptions-to-maintenance-cloud` skill. It owns Service Mapping source evidence, source entities, aliases, source attributes, data types, service access, mapping prerequisites, publication readiness, and source-resolution handoff for Subscriptions to Maintenance Cloud. Before handling source resolution, read the primary workflow reference at `../manage-algorithms-for-subscriptions-to-maintenance-cloud/references/ora_maintenance_program_algorithm_workflow.md`.

When a requested source value is not present in the current Service Mapping source XML, perform or require the permitted read-only describe lookup before proposing a new Service Mapping variable. Use `/crmRestApi/resources/11.13.18.05/subscriptionProducts/describe` for `Products` values and `/crmRestApi/resources/11.13.18.05/subscriptionProducts/describe?partialDescription=coveredLevels` for `CoveredAssets` or covered-level values. Return the exact described source object, attribute name, data type, evidence source, and proposed alias. Do not invent `_Custom` aliases from business wording alone. If describe cannot be run, fails, or returns multiple plausible candidates, return `needs_describe` or `needs_decision` with the missing evidence or alternatives instead of choosing blindly. Assumptions are allowed only when the implementer explicitly asks to proceed without describe evidence.

Handle only the Service Mapping portion of a request. When source resolution, mapping readiness, publication evidence, or prerequisite analysis is complete, return automatically to the primary Manage Algorithms workflow. Pass confirmed sources, selected aliases, target-field pairing, alternatives, assumptions, unresolved decisions, access prerequisites, and publication status.

Do not continue into algorithm drafting, existing `ActionExpression` merge decisions, algorithm artifact creation, or final algorithm validation inside this companion skill. Those decisions belong to the primary Manage Algorithms workflow after the companion handoff returns. If the caller asks how approved Groovy should be applied, return to the primary workflow rules: provide the Groovy draft for approval first, use Service Mapping aliases directly as Groovy values, append to existing executable Groovy, and ignore or remove blank, placeholder, sample, or comment-only content.

## Setup Task Skill Contract

- task_code: `CUSTOM_MANAGE_SERVICE_MAPPINGS_FOR_SUBSCRIPTIONS_TO_MAINTENANCE_CLOUD`
- task_name: `Manage Service Mappings for Subscriptions to Maintenance Cloud`
- parent_skill_id: `cx.subscriptions.integration-setup`
- pillar: `CX`
- offering: `Subscriptions`
- functional_area: `Integration Setup`
- functional_area_code: `CUSTOM_INTEGRATION_SETUP`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `REST`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this companion advisory skill when the primary Algorithms workflow needs Service Mapping source exposure, describe-backed source candidates, exact attribute discovery, source alias assumptions, access prerequisites, publication readiness, or configuration steps for `Subscription Maintenance Program Integration`.

## References

Read task-local references from `references/` when a request needs source-derived Subscription Management or Maintenance Cloud documentation context:

- [Primary Maintenance Program Algorithm Workflow](../manage-algorithms-for-subscriptions-to-maintenance-cloud/references/ora_maintenance_program_algorithm_workflow.md) for mandatory attachments, `MaintenanceProgramInterface` source validation, describe-first source resolution, allowed describe paths, return-to-primary behavior, Groovy-first approval gates, direct source-value drafting rules, existing-Groovy merge rules, and Service Mapping steps for unresolved or assumed sources.
- [Subscription Management General Reference](references/ora_subscription_management_general_reference.md) for subscription, coverage product, covered level, validation, activation, and approval context.
- [Subscription Maintenance Readiness Reference](references/ora_subscription_maintenance_readiness_reference.md) for the 24B preventive maintenance flow, coverage-template association, and scheduled process sequence.
- [MNT_PROGRAMS_INT Reference](references/ora_mnt_programs_int_reference.md) for maintenance program header target-field evidence.
- [MNT_WORK_REQUIREMENTS_INT Reference](references/ora_mnt_work_requirements_int_reference.md) for maintenance work requirement target-field evidence.

Keep any new source-derived supporting notes in `references/`. Reserve `ora-resource/` for compiler-consumable `ora_*.md` rule files and `ora_rule_registry.json`.

## Setup Task Metadata

- Task name: `Manage Service Mappings for Subscriptions to Maintenance Cloud`
- Task code: `CUSTOM_MANAGE_SERVICE_MAPPINGS_FOR_SUBSCRIPTIONS_TO_MAINTENANCE_CLOUD`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Object: ``

## CSV Export, Import, and Validation Workflow

`CSVExportImportSupportedFlag` is `N`, so this task is not marked as CSV export/import supported in the effective setup-task catalog.

Do not route CSV export work to `shared.setup-export.task-level-export` or CSV import work to `core.data-loader` unless live Fusion metadata or Oracle guidance confirms support. Use `shared.validation.setup-data-validator` only when a setup data artifact is available for review. Use `shared.validation.reference-data-validator` when the task depends on cross-pillar reference data.


## Inputs

- `business_requirement`
- `algorithm_bo_xml`
- `maintenance_program_interface_source_xml`
- `requested_source_attributes`
- `implementation_project_context`

## Outputs

- `service_mapping_assessment`
- `source_resolution_record`
- `service_mapping_configuration_handoff`
- `mapping_prerequisites`
- `validation_result`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.subscriptions.integration-setup` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

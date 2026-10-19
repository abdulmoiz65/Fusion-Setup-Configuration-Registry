---
skill_id: "cx.subscriptions.integration-setup.manage-algorithms-for-subscriptions-to-maintenance-cloud"
name: "Manage Algorithms for Subscriptions to Maintenance Cloud Setup Task Guidance"
description: "Primary advisory workflow for Subscription Maintenance Program Integration Algorithm_BO.xml review, Groovy-first approval drafting, approved local XML updates, and describe-backed Service Mapping source routing."
layer: "pillar"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Integration Setup"
functional_area_code: "CUSTOM_INTEGRATION_SETUP"
task_code: "CUSTOM_MANAGE_ALGORITHMS_FOR_SUBSCRIPTIONS_TO_MAINTENANCE_CLOUD"
task_name: "Manage Algorithms for Subscriptions to Maintenance Cloud"
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
version: "0.1.5"
inputs:
  - "business_requirement"
  - "algorithm_bo_xml"
  - "maintenance_program_interface_source_xml"
  - "implementation_project_context"
outputs:
  - "attachment_preflight_result"
  - "source_resolution_handoff"
  - "groovy_proposal"
  - "algorithm_bo_xml"
  - "service_mapping_configuration_steps"
  - "validation_result"
  - "skill_run_record"
  - "token_usage_record"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
depends_on:
  - "cx.subscriptions.integration-setup.manage-service-mappings-for-subscriptions-to-maintenance-cloud"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/integration-setup/manage-algorithms-for-subscriptions-to-maintenance-cloud/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/integration-setup/manage-algorithms-for-subscriptions-to-maintenance-cloud/current/"
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

# Manage Algorithms for Subscriptions to Maintenance Cloud Setup Task Guidance

## Purpose

Provides advisory guidance for `Subscription Maintenance Program Integration` algorithm review, source-resolution coordination, Groovy drafting, approval-gated local `Algorithm_BO.xml` updates, and manual import handoff for `Manage Algorithms for Subscriptions to Maintenance Cloud`.

## Primary Workflow and Companion Routing

This is the primary workflow for Subscriptions to Maintenance Cloud algorithm work. It owns mandatory attachment preflight, algorithm artifact review, target-field fit, Groovy drafting, Groovy-first approval gating, approved local `Algorithm_BO.xml` changes, validation checkpoints, and final handoff. Before acting on any requirement, read and follow [Maintenance Program Algorithm Workflow](references/ora_maintenance_program_algorithm_workflow.md).

For any Service Mapping question, source exposure question, source alias, source object, source attribute, service access, type compatibility, mapping publication, or source-to-target readiness gap, invoke the companion skill `cx.subscriptions.integration-setup.manage-service-mappings-for-subscriptions-to-maintenance-cloud`. Pass the business requirement, requested Maintenance target field, known subscription or coverage context, current source evidence, and unresolved questions. When the current Service Mapping source XML does not expose the needed source value, require the companion to resolve the exact source attribute and data type from the permitted read-only describe paths before suggesting a Service Mapping variable; do not convert a business meaning into a guessed `_Custom` alias unless the implementer explicitly asks to proceed without describe evidence.

When the companion completes its work, resume this primary workflow automatically using the companion's confirmed sources, alternatives, assumptions, prerequisites, unresolved decisions, and publication status. Do not require the implementer to invoke the primary skill again after a companion call.

## Setup Task Skill Contract

- task_code: `CUSTOM_MANAGE_ALGORITHMS_FOR_SUBSCRIPTIONS_TO_MAINTENANCE_CLOUD`
- task_name: `Manage Algorithms for Subscriptions to Maintenance Cloud`
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

Use this advisory skill when reviewing, drafting, updating, or validating local `Algorithm_BO.xml` content for `Subscription Maintenance Program Integration` under `Manage Algorithms for Subscriptions to Maintenance Cloud`.

## References

Read task-local references from `references/` when a request needs source-derived Subscription Management or Maintenance Cloud documentation context:

- [Maintenance Program Algorithm Workflow](references/ora_maintenance_program_algorithm_workflow.md) for mandatory attachments, `MaintenanceProgramInterface` source validation, describe-first source resolution, `ProgramInterface.insert` syntax, direct source-value drafting rules, Groovy-first approval gates, local `Algorithm_BO.xml` update and existing-Groovy merge rules, and Service Mapping steps for unresolved or assumed sources.
- [Subscription Management General Reference](references/ora_subscription_management_general_reference.md) for subscription, coverage product, covered level, validation, activation, and approval context.
- [Subscription Maintenance Readiness Reference](references/ora_subscription_maintenance_readiness_reference.md) for the 24B preventive maintenance flow, coverage-template association, and scheduled process sequence.
- [MNT_PROGRAMS_INT Reference](references/ora_mnt_programs_int_reference.md) for maintenance program header target-field evidence.
- [MNT_WORK_REQUIREMENTS_INT Reference](references/ora_mnt_work_requirements_int_reference.md) for maintenance work requirement target-field evidence.

Keep any new source-derived supporting notes in `references/`. Reserve `ora-resource/` for compiler-consumable `ora_*.md` rule files and `ora_rule_registry.json`.

## Setup Task Metadata

- Task name: `Manage Algorithms for Subscriptions to Maintenance Cloud`
- Task code: `CUSTOM_MANAGE_ALGORITHMS_FOR_SUBSCRIPTIONS_TO_MAINTENANCE_CLOUD`
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
- `implementation_project_context`

## Outputs

- `attachment_preflight_result`
- `source_resolution_handoff`
- `groovy_proposal`
- `algorithm_bo_xml`
- `service_mapping_configuration_steps`
- `validation_result`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.subscriptions.integration-setup` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

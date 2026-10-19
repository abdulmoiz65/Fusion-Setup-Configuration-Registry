---
skill_id: "hcm.learning-management.learning-configurations"
name: "Learning Configurations"
description: "Guides Oracle Learning defaults and background-processing configuration: evaluates requirements, reports configured/missing/unverified settings, prepares an approved delta and gates execution on a supported task contract. Covers evaluations, enrollment, assignments, certificates, attendance, conversations, calendar templates and alerts."
layer: "pillar"
pillar: "HCM"
offering: "Learning Management"
functional_area: "Learning Configurations"
functional_area_code: "ORA_LEARNING_CONFIGURATIONS"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM learning management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "learning_configurations_scope"
  - "learning_configurations_requirements"
  - "requirement_documents"
  - "current_configuration_evidence"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "configuration_inventory"
  - "configuration_proposal"
  - "dependency_readiness"
  - "configuration_results"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
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
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-configurations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-configurations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/learning-management/learning-configurations/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "CUSTOM_CONFIGURE_LEARNING_DEFAULTS"
  - "CUSTOM_CONFIGURE_BACKGROUND_PROCESSING"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Persists sanitized inventory, proposal, readiness and results in the active project."
  - "Intended configuration mutations require a completed task contract, selected provider, current approval and readback; this version supplies no live configuration executor."
required_privileges: []
---

# Learning Configurations

## Purpose

Own the non-provider Learning configuration decisions, not Learning's entire
implementation. Explain each applicable setting, establish current evidence,
ask only missing business questions, and present the exact proposed changes.
Do not equate a new pod with an empty baseline.

## When to Use

Use for new implementation, existing-setup review, specific defaults, or
background-processing changes. Implementation runs enter through the
[Implementation Router](../../../../router/implementation-router/SKILL.md).
For broad Learning enablement, return to the
[offering](../SKILL.md) for other functional areas; do not silently restrict
the implementation to self-paced or instructor-led delivery.

Read [workflow and inventory](references/workflow.md) first, then the selected
task below and [sources and dependencies](references/sources-and-dependencies.md).
The latter records the current taxonomy and PM FDD C7 mapping. Global Human
Resources supplied a structural pattern only; it is not a Learning dependency.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Learning Management` (`ORA_LEARNING_MANAGEMENT`)
- Functional area / Setup Object: `Learning Configurations` (`ORA_LEARNING_CONFIGURATIONS`)

## Setup Tasks

1. [Configure Learning Defaults](configure-learning-defaults.md) (`CUSTOM_CONFIGURE_LEARNING_DEFAULTS`)
2. [Configure Background Processing](configure-background-processing.md) (`CUSTOM_CONFIGURE_BACKGROUND_PROCESSING`)

## Execution readiness and read order

The implementer has confirmed that Business Objects for both tasks are not
registered yet and has deferred their binding until they become available.
Functional guidance is ready for intake, source-based business review,
dependency planning, inventory preparation and draft proposals. Do not make
registration a prerequisite for that preparation or repeatedly request the
missing Business Objects. Resume discovery/binding only when the user asks;
see [deferred Business Object binding](references/workflow.md#deferred-business-object-binding).
This is not a claim that any pod settings or execution contracts are validated.

Both catalog tasks have CSV and export/import support N. Their generated
REST mode and empty businessObject are metadata, not a working Data Loader
route. The approved taxonomy marks both BC REST contracts TBD ETA 27B; the
FDD identifies OLC-100310 as the API dependency. An ETA is not availability.
Read, write, privilege and reconciliation bindings remain TBD. Do not infer
endpoints, run a blank-business-object sample command, use generic REST/ESS,
or substitute browser automation. UI navigation in the task files is product
context for the implementer, not an alternate agent execution route.

For task validation/execution, load the
[task-node execution guide](../learning-management-common/references/task-node-execution.md),
selected task metadata, [registry](ora-resource/ora_rule_registry.json), and
the local Learning rule plan from `../learning-management-common/scripts/rule_plan.py`. Load reachable source rows for that exact task:

1. [Input validation](ora-resource/ora_input_validation.md)
2. [Dependency readiness](ora-resource/ora_dependency_readiness.md)
3. [Reference lookups](ora-resource/ora_reference_lookups.md)
4. [Defaulting](ora-resource/ora_defaulting_rules.md)
5. [Design enforcement](ora-resource/ora_design_enforcement.md)
6. [Error handling and execution gates](ora-resource/ora_error_handling.md)

Both graphs intentionally remain incomplete until their authoring gaps are
resolved. Planning, intake and source-based recommendations can continue;
do not call them completed live validation. A readiness override cannot supply
a missing endpoint, privilege, payload, approval or readback contract.
Runbooks own payloads, processing and writes; these resource graphs do not.

## Output and persistence contract

Return the complete configuration inventory before the change proposal.
Keep configured/keep-current, change-needed, not-applicable, deferred and
unverified rows visible. Include dependencies, actionable gaps, acceptance
checks and per-operation counts; unknown state is not a missing setting.
`functional_area_setup_plan` records selected tasks and conditional handoffs;
`configuration_guidance` and `validation_checkpoints` point to the task's
business guidance and acceptance evidence. `configuration_results` distinguishes
planning from verified execution, partial failure and uncertainty.

Use the manifest's workspace locations for sanitized inventories, proposals,
blueprints and validation reports; record decisions, register/version artifacts,
update project state, record the skill run and append/report token usage.
No project: use the routed project service and draft-project convention, and
offer to rename it. Never put pod outputs, customer data, credentials or raw
responses in this reusable skill. Developer generation itself needs no tenant
project. See the workflow for compatibility and diagnostic requirements.

## Review and verification

Reviewers: HCM Learning SME/Pillar Lead, FSCR core reviewer and QA; security
review for privilege or run-as contracts. Run
[offline contract tests and acceptance scenarios](tests/acceptance.md).
Do not mark the skill live-ready merely because generation/tests succeeded.

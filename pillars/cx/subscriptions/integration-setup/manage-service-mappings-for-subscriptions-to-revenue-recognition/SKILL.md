---
skill_id: "cx.subscriptions.integration-setup.manage-service-mappings-for-subscriptions-to-revenue-recognition"
name: "Manage Service Mappings for Subscriptions to Revenue Recognition Setup Task Guidance"
description: "RMCS Service Mapping companion: validates current inputs, analyzes source exposure and metadata, and returns findings to the primary Algorithms workflow. No mapping or algorithm mutations."
layer: "pillar"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Integration Setup"
functional_area_code: "CUSTOM_INTEGRATION_SETUP"
task_code: "CUSTOM_MANAGE_SERVICE_MAPPINGS_FOR_SUBSCRIPTIONS_TO_REVENUE_RECOGNITION"
task_name: "Manage Service Mappings for Subscriptions to Revenue Recognition"
parent_skill_id: "cx.subscriptions.integration-setup"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "CX subscriptions pillar team"
version: "0.3.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
  - "rule_phase"
  - "rule_checkpoint_context"
  - "business_requirement"
  - "algorithm_bo_xml"
  - "service_mapping_source_xml"
  - "service_mapping_analysis_request"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "service_mapping_analysis_result"
  - "validation_checkpoints"
  - "source_resolution_records"
  - "configuration_handoff"
  - "rule_checkpoint_result"
  - "skill_run_record"
  - "token_usage_record"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/integration-setup/manage-service-mappings-for-subscriptions-to-revenue-recognition/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/integration-setup/manage-service-mappings-for-subscriptions-to-revenue-recognition/current/"
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
  - "Optional authorized describe GET and redacted project records; no Fusion mutation"
required_privileges: []
---

# Manage Service Mappings for Subscriptions to Revenue Recognition

## Purpose and execution boundary

This is the Service Mapping companion to [Manage Algorithms for Subscriptions to Revenue Recognition](../manage-algorithms-for-subscriptions-to-revenue-recognition/SKILL.md). It owns source/exposure analysis, metadata, aliases/types, VO mappings, service access, relationships and configuration/publication prerequisites. It returns its findings to the primary; it does not draft Groovy or edit algorithm or Service Mapping XML.

Apply the shared [current-input preflight](../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_algorithm_xml_guidance.md#input-preflight) before analysis. A primary invocation may reuse that request's validated pair and fingerprints. A directly invoked request must supply both current inputs and pass the same gates.

## Companion analysis and return

1. Read the primary's [analysis request](../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_use_case_resolution.md#companion-request-record), preserving request identity, business rule, known target/scope, prior decisions and return stage.
2. Follow [Service Mapping guidance](resources/ora_service_mapping_guidance.md) for source-owner discovery, active XML/provider/access checks and the distinction between source entities and protected output definitions. Function-backed ProductAssociations/BillLines do not require invented mapping entities.
3. Prefer the supplied current evidence. Only if a specific metadata question remains may the [declared optional describe GET workflow](ora-resource/ora_reference_lookups.md#live-lookups) be selected, after project, environment, identity, privilege, endpoint and diagnostic checks. No exploratory browser, direct REST client or alternative authentication route is selected.
4. Return service_mapping_analysis_result using the [handoff contract](../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_use_case_resolution.md#companion-handoff-template), separating confirmed facts, alternatives, assumptions and remaining prerequisites.
5. Hand control back automatically on every outcome: analyzed, needs_decision, prerequisite_pending, blocked or declined. The primary consumes it at the saved stage, asks remaining user questions and owns further computation and approval. Do not ask the implementer to invoke Algorithms again.

The return completes a companion call; it is not a recursive invocation or a reverse depends_on dependency. Do not repeat analysis without a changed question, decision or evidence.

For a direct mapping-only request, return the mapping analysis to the user. If that direct request also requires algorithm work, route the overall request to the primary once with the existing findings; the primary invokes the companion only for remaining mapping questions.

## Resource ownership

| Read when | Canonical resource |
|---|---|
| Resolving source exposure, protected outputs, access or optional describe metadata | [Service Mapping guidance](resources/ora_service_mapping_guidance.md) |
| Checking Subscription context and documentation | [Task-local general reference](resources/ora_subscription_management_general_reference.md) |
| Applying shared identity/version checks | [Primary Algorithm XML guidance](../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_algorithm_xml_guidance.md) |
| Classifying requirements and exchanging analysis records | [Primary use-case resolution](../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_use_case_resolution.md) |
| Resolving physical targets and algorithm output eligibility | [Primary RMCS data model](../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_rmcs_data_model_reference.md) |

The companion does not duplicate output-insert, Groovy, highest-version mutation or local-artifact rules. Those belong to the primary's linked resources.

The ora-resource package now implements the assisted checkpoints below. Current supplied files and recorded decisions are explicitly authorized local evidence, not proof of Fusion publication. The supporting guide owns source decisions and configuration semantics, including the accepted `_Custom` handoff for ordinary unexposed source attributes. [Reference lookups](ora-resource/ora_reference_lookups.md) alone owns local/live acquisition mechanics. The [source catalogue](ora-resource/ora_reference_lookups.md#source-catalogue) is preserved; [unsupported live contracts](ora-resource/ora_reference_lookups.md#unsupported-live-contracts) remain blocked outside the assisted graph. No other mapping default is inferred.

## Assisted rule checkpoints

Before consuming the [task registry](ora-resource/ora_rule_registry.json), read the core [task-node execution guide](../../../../../core/fusion-dev/fusionapps-resource-authoring/references/ora-resource-task-node-execution-guide.md) and obtain its current validated task plan. Missing, stale or incomplete registry readiness blocks that route and requires the resource-authoring workflow; do not edit readiness or use an override.

The caller supplies rule_phase and current rule_checkpoint_context. Start each phase invocation at the graph's declared start node, follow one outcome per node and evaluate only applicable rows. Record other rows as Not Applicable. A checkpoint validates the analysis stage; it does not certify publication or trigger the primary automatically through registry edges.

| rule_phase | Caller stage and required gate |
|---|---|
| intake | Before source analysis; validate the current pair and request/question scope, plus saved-stage context when invoked by the primary |
| analysis | During evidence-backed source analysis; validate source records and decisions; a specific missing metadata question may select the declared optional describe node after all live-read prerequisites |
| handoff | Before returning findings; validate source/configuration fields in the canonical handoff and the actual outcome, including unresolved decisions/prerequisites; do not acquire new live metadata |

Read the [input](ora-resource/ora_input_validation.md), [dependency](ora-resource/ora_dependency_readiness.md), [lookup](ora-resource/ora_reference_lookups.md), [design](ora-resource/ora_design_enforcement.md) and [error](ora-resource/ora_error_handling.md) tables through the plan's source anchors. Local evidence resolution uses a local evaluate_result node. Only the separate reference_lookup node may perform the selected, core-owned describe GET; existing evidence takes its no-lookup path. There is no mapping write/default node.

Return every outcome under the existing companion protocol, preserving the [single source record](resources/ora_service_mapping_guidance.md#source-resolution-record) and the primary's [single final handoff schema](../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_use_case_resolution.md#final-traceability-and-configuration-handoff). A valid needs_decision or prerequisite_pending record is not analyzed success. The manifest, not a cross-task registry edge, owns return to the primary's saved stage.

## Catalogue and mutation boundary

Preserve the task's catalogue identity under cx > subscriptions > Integration Setup. Export/import and CSV flags are N, businessObject is empty, and dataloader_import_mode REST does not select a loader or sample-download route.

No source/output entity edits, mapping XML generation, import, publication or Fusion execution tests are performed by this companion. A needed mapping change is a configuration handoff and prerequisite, not a mutation. Protected seeded output definitions remain unchanged; the primary may propose assignments only to their existing writable values under its own approval workflow.

## Inputs, outputs and persistence

Runtime inputs include the business rule, current validated algorithm and mapping, project context and service_mapping_analysis_request when called by the primary. Existing generic routing inputs remain supported. Optional describe requires a verified target environment and authorized metadata scope; required read privileges are established for that environment before the core client is invoked.

Return the structured analysis result, source/configuration findings and validation checkpoints. Persist permitted decisions, redacted diagnostics, run records and token usage through the declared project services. Never persist credentials or sensitive customer data. Skill-file authoring does not execute this runtime workflow or create an implementation project.

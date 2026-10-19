---
skill_id: "cx.subscriptions.integration-setup.manage-algorithms-for-subscriptions-to-revenue-recognition"
name: "Manage Algorithms for Subscriptions to Revenue Recognition Setup Task Guidance"
description: "Primary RMCS workflow: validates current exports, coordinates Service Mapping analysis, drafts RMCS Groovy and prepares an explicitly approved local Algorithm_BO.xml without deploying Fusion changes."
layer: "pillar"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Integration Setup"
functional_area_code: "CUSTOM_INTEGRATION_SETUP"
task_code: "CUSTOM_MANAGE_ALGORITHMS_FOR_SUBSCRIPTIONS_TO_REVENUE_RECOGNITION"
task_name: "Manage Algorithms for Subscriptions to Revenue Recognition"
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
  - "service_mapping_analysis_result"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "service_mapping_analysis_request"
  - "groovy_proposal"
  - "approval_evidence"
  - "algorithm_import_xml"
  - "validation_checkpoints"
  - "source_resolution_records"
  - "configuration_handoff"
  - "rule_checkpoint_result"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "cx.subscriptions.integration-setup.manage-service-mappings-for-subscriptions-to-revenue-recognition"
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
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/integration-setup/manage-algorithms-for-subscriptions-to-revenue-recognition/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/integration-setup/manage-algorithms-for-subscriptions-to-revenue-recognition/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/integration-setup/manage-algorithms-for-subscriptions-to-revenue-recognition/current/"
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
  - "Writes approved local algorithm artifact and project records; no Fusion mutation"
required_privileges: []
---

# Manage Algorithms for Subscriptions to Revenue Recognition

## Purpose and execution boundary

This is the primary assisted workflow for RMCS algorithm and combined algorithm/mapping requests. It owns input validation, version/action selection, existing-code review, Groovy proposals, Revenue Recognition output logic and an explicitly approved local Algorithm_BO.xml artifact. It does not deploy Fusion changes.

Read the [input preflight](resources/ora_algorithm_xml_guidance.md#input-preflight) before analyzing a runtime request. Both current inputs are mandatory. Wrong mapping context, wrong algorithm identity or an inactive highest version is a stop, not permission to use older/similar input. Source attachments provided for skill authoring are not runtime defaults and must not be bundled with the skill.

## Assisted workflow

1. Establish the implementation objective, task scope and selected project context through the repository's routed implementation workflow. Validate the current algorithm and mapping with the linked preflight and read-only helper.
2. Resolve the requirement and intended document/line/subline outcome using [use-case resolution](resources/ora_use_case_resolution.md). Select the highest eligible version's action by structure, not display name or ordinal.
3. Invoke the [RMCS Service Mapping companion](../manage-service-mappings-for-subscriptions-to-revenue-recognition/SKILL.md) for the scenarios below. Preserve the request, current evidence and return stage; do not ask the user to invoke it manually.
4. On return, consume its findings and resume automatically. Resolve target eligibility using the [data-model guide](resources/ora_rmcs_data_model_reference.md), then follow [Groovy guidance](resources/ora_groovy_function_guidance.md) for source scope, cardinality, function-backed inputs, existing code and layout.
5. Show the complete final Groovy and exact proposed XML scope in chat. Apply the [approval and local artifact procedure](resources/ora_algorithm_xml_guidance.md#approval-and-local-artifact) only after explicit approval. A needed missing subline step also requires an approved structural proposal and a supported row-identity contract.
6. Verify only the approved local changes, register permitted project artifacts and report what remains unverified in Fusion. No import, publication, activation, deployment or Fusion execution test is part of this route.

## Primary workflow and scenario routing

The companion skill ID is cx.subscriptions.integration-setup.manage-service-mappings-for-subscriptions-to-revenue-recognition. Route RMCS mapping work there, never to a Receivables skill.

| Scenario | Owner and continuation |
|---|---|
| Source entity/attribute is missing, unclear, unexposed or disputed | Companion analyzes functional owner and exposure; primary retains the requirement |
| Source XML, describe metadata, VO mapping, alias/type, service access or binding needs confirmation | Companion answers the precise metadata/mapping question |
| Mapping configuration or publication prerequisite needs assessment | Companion identifies required configuration and evidence; it performs no mapping mutation |
| Business-only requirement needs source discovery | Primary clarifies outcome/record level, then delegates source discovery |
| Target meaning, calculation or algorithm function/cardinality needs review and mapping evidence is resolved | Primary handles computation/action scope; delegate only a new mapping metadata question |
| Returned candidate is rejected or evidence changes | Record the decision and delegate only the newly affected question |

Use the [Types 1-5 classifier](resources/ora_use_case_resolution.md#input-type-classifier) and [companion request record](resources/ora_use_case_resolution.md#companion-request-record). Missing Service Mapping entities for function-backed sources are not automatically configuration defects.

## Automatic return and further processing

Every companion outcome returns to the primary's saved stage without requiring manual reinvocation. The [handoff and outcome procedure](resources/ora_use_case_resolution.md#automatic-return-and-further-processing) defines how to consume analyzed, needs_decision, prerequisite_pending, blocked and declined results.

The primary handles remaining user choices and blockers, then continues permitted processing. Do not start another primary workflow or repeat the same companion request without new evidence, a new decision or a new question. Analyzed is not deployment evidence or Groovy/XML approval.

## Resource ownership

| Read when | Canonical resource |
|---|---|
| Starting preflight, selecting actions, proposing Step 3 or preparing approved XML | [Algorithm XML guidance](resources/ora_algorithm_xml_guidance.md) |
| Classifying a requirement or exchanging companion results | [Use-case resolution](resources/ora_use_case_resolution.md) |
| Resolving target fields, mapped assignments, insert contexts or subline restrictions | [RMCS data model](resources/ora_rmcs_data_model_reference.md) |
| Reviewing/drafting selected action expressions or algorithm functions | [Groovy and functions](resources/ora_groovy_function_guidance.md) |
| Checking business/documentation context | [Subscription Management general reference](resources/ora_subscription_management_general_reference.md) |

These resources now define the assisted workflow; they are no longer blank RMCS templates. They share responsibilities with the AR skill structure, not AR Groovy behavior.

The ora-resource package now implements the assisted checkpoints below, using current supplied files and recorded decisions as the explicitly authorized local evidence. It does not prove Fusion publication. Detailed source/target, Groovy, XML and handoff procedures remain in their canonical resources; the rule tables validate their phase-specific checkpoints, rather than duplicate those procedures. The [source catalogue](ora-resource/ora_reference_lookups.md#source-catalogue) is preserved, and [unsupported live contracts](ora-resource/ora_reference_lookups.md#unsupported-live-contracts) remain explicitly blocked outside this assisted graph.

## Assisted rule checkpoints

Before consuming the [task registry](ora-resource/ora_rule_registry.json), read the core [task-node execution guide](../../../../../core/fusion-dev/fusionapps-resource-authoring/references/ora-resource-task-node-execution-guide.md) and obtain a current validated task plan through its declared planner. An absent, stale or incomplete registry is an authoring blocker; regenerate it only through the resource-authoring workflow, not by hand-editing readiness or applying an override.

The caller supplies rule_phase and current rule_checkpoint_context, starts the task graph at its declared start node and follows one outcome per node. Evaluate only phase-applicable rows; report other rows as Not Applicable, not passed. Every phase is a fresh checkpoint invocation with the same current evidence lineage. A passed checkpoint is not completion of the whole skill or approval for an external action.

| rule_phase | Caller stage and required gate |
|---|---|
| intake | Before requirement/source analysis; validate the current pair and request context without requiring a proposal or approval |
| proposal | After the needed companion analysis and primary drafting; validate source decisions, target/runtime policy and the complete chat-visible proposal/handoff |
| approved_change | Immediately before local XML preparation; validate exact persisted proposal/approval, current fingerprints, permitted destination and supported structural scope |
| artifact_result | After the caller creates the approved local artifact; read and compare the actual output against the approved expressions and allowed XML delta before handoff |

Read the [input](ora-resource/ora_input_validation.md), [dependency](ora-resource/ora_dependency_readiness.md), [lookup](ora-resource/ora_reference_lookups.md), [default](ora-resource/ora_defaulting_rules.md), [design](ora-resource/ora_design_enforcement.md) and [error](ora-resource/ora_error_handling.md) tables through their planned source anchors. The default node only fills the approved in-memory changeset; the graph never creates an XML file, invokes the companion or calls Fusion. The primary runbook owns those separately declared local operations and all saved-stage routing. A blocked checkpoint returns a precise issue to that runbook; retry only after the relevant input, decision or evidence changes.

The [source-resolution record](../manage-service-mappings-for-subscriptions-to-revenue-recognition/resources/ora_service_mapping_guidance.md#source-resolution-record) has one companion-owned schema. The [final traceability/configuration handoff](resources/ora_use_case_resolution.md#final-traceability-and-configuration-handoff) has one primary-owned schema. Show the latter alongside the exact proposal and final artifact report; link source records without copying them into a competing schema.

## Catalogue and external-operation boundary

Keep the manifest's existing task code, parent, offering and functional-area catalogue mapping. Both export/import and CSV flags are N, and businessObject is empty. The inherited dataloader_import_mode REST field is catalogue metadata, not an executable loader route. Do not request a sample for an empty business object, route this task to a loader or infer XML-import support from these flags.

The primary performs no live metadata calls. If metadata discovery is needed, the companion may select only its declared read-only describe workflow after its prerequisites pass. A request to deploy/import requires a separately supported routed workflow and its own exact-target approval; do not substitute browser, REST or OAuth exploration.

## Inputs, outputs and persistence

Runtime inputs are the business requirement, current raw `Algorithm_BO.xml`, current mapping source XML and project context, plus the companion result when resuming. Existing generic implementation_objective, setup_task_scope and setup_data_artifacts inputs remain available for routed compatibility. Groovy approval is obtained at the artifact stage, not presumed from the initial request.

Outputs are the analysis/plan, source-resolution records, canonical configuration handoff, checkpoint findings, complete Groovy proposal and exact approval evidence; a local algorithm_import_xml (workspace artifact type other) is conditional on the explicit approval and artifact prerequisites. Persist permitted durable decisions, artifact versions, redacted run diagnostics and token usage using the core services and workspace locations declared above. Do not persist secrets or sensitive customer payloads. Reusable skill authoring alone does not create a project or execute this implementation workflow.

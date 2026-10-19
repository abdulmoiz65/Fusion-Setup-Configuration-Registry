---
skill_id: "cx.subscriptions.integration-setup.manage-service-mappings-for-order-management-to-subscriptions"
name: "Manage Service Mappings for Order Management to Subscriptions Advisory"
description: "Read-only companion workflow for FOM-to-OSS Service Mapping XML validation, existing-or-missing mapping assessment, and describe-backed attribute discovery. Returns a validated service mapping assessment to the Manage Algorithms task without changing Fusion configuration."
layer: "pillar"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Integration Setup"
functional_area_code: "CUSTOM_INTEGRATION_SETUP"
task_code: "CUSTOM_MANAGE_SERVICE_MAPPINGS_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS"
task_name: "Manage Service Mappings for Order Management to Subscriptions"
parent_skill_id: "cx.subscriptions.integration-setup"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "advisory"
execution_mode: "assisted"
owner_team: "CX subscriptions pillar team"
version: "0.1.0"
inputs:
  - "business_requirement"
  - "service_mapping_source_xml"
  - "requested_mapping"
  - "mapping_placeholder_responses_when_available"
  - "implementation_project_context"
outputs:
  - "inline_service_mapping_assessment"
  - "inline_service_mapping_ui_steps"
  - "inline_algorithm_recommendation"
  - "inline_mapping_prerequisites"
  - "inline_mapping_information_request"
  - "validation_result"
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
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/integration-setup/manage-service-mappings-for-order-management-to-subscriptions/current/"
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
  - "May perform an authorized read-only Order Management or Subscription Management REST describe lookup when a mapping recommendation requires metadata evidence."
required_privileges:
  - "Fusion REST metadata read access appropriate to Sales Orders for Order Hub and Subscription Management CRM REST describe endpoints"
---

# Manage Service Mappings for Order Management to Subscriptions

## Purpose

Assess a supplied FOM-to-OSS Service Mapping export for the `OMIntegration`
context, determine whether a requested value is already exposed and assigned,
identify missing mapping prerequisites, and return a validated assessment for
the companion Algorithm task. This skill is read-only: it never edits Service
Mapping XML, creates an import artifact, publishes configuration, or changes
Fusion data.

## Resource Load Order

Use these task-local resources progressively; read only the files needed for the
current assessment stage.

1. `ora-resource/ora_input_validation.md` for required inputs, status values,
   Custom EFF contracts, output shape, and validation-skip handling.
2. `ora-resource/ora_reference_lookups.md` when XML evidence is insufficient
   and a documented read-only metadata `describe` lookup or task-local REST
   probe may be needed.
3. `ora-resource/ora_dependency_readiness.md` before handing an assessment to
   Manage Algorithms or before relying on metadata, source, target, or lineage
   prerequisites.
4. `ora-resource/ora_design_enforcement.md` for XML-first lineage, three-tab
   Service Mapping plan, Custom EFF, describe-backed target, and
   interface-table enforcement.
5. `ora-resource/ora_error_handling.md` for blockers, disclosure requirements,
   refusals, provisional handling, and failure classification.
6. `ora-resource/ora_rule_registry.json` when a durable rule-node trace or
   machine-readable route is needed.

## Essential Contract

Require a business requirement, requested outcome, and current Service Mapping
XML before assessing mapping evidence. Validate that the root
`transformContext` has exactly `contextName="OMIntegration"`; stop before using
entities, attributes, joins, permissions, or transformations from any other
context.

Treat the XML as the delivered data-lineage contract. It can prove available
entities, attributes, provider/source rows, service permissions, and explicit
assignment evidence. It does not authorize a Service Mapping mutation, prove a
runtime API, or turn similar names into a mapping fact.

Availability is not assignment. If source and target are exposed but the XML
contains no direct source-to-target assignment, return `source_target_available`
with `algorithm_assessment_required`. Do not describe a source-provider row as a
source-to-target mapping.

For cross-entity outcomes, establish the `OSSTransactions` lineage first. For a
fulfillment-line-to-product assessment, use only XML-evidenced keys such as
`FullfillLines.FulfillLineId` to
`OSSTransactions.SalesOrderFulfillLineId` and `Products.SubscriptionProductId`
to `OSSTransactions.SubscriptionProductId`. A direct target-to-source key is
corroborating evidence only.

For Custom EFF sources or targets, require the complete three-tab contract:
EFF entity, owner key, scalar types, provider mapping, source read-only service
exposure, writable target exposure, and the owner-to-`OSSTransactions`-to-target
lineage. Do not use Algorithm logic to bypass an incomplete EFF exposure.

When XML evidence cannot settle a requested source, target, correlation, or
compatibility question, resolve metadata for the requested entity before making
a final availability conclusion. Select the entity and, when applicable, its
parent-to-child documentation branch from the user's requested outcome; do not
hardcode a particular entity or silently substitute a different target. Use
current official documentation or an exact user-supplied environment
entity-level `describe` URL. A describe result is candidate evidence only; it
never proves a Service Mapping alias, provider row, permission, assignment, or
runtime collection name.

For a conditional primary/fallback requirement, treat metadata discovery as a
mandatory gate whenever the current XML does not expose the exact primary
source, fallback source, or requested target. Run the documented current
entity-level or root-descriptor `describe` lookup for each unresolved standard
entity before returning a mapping-information request, mapping gap, or metadata
blocker. Only ask the implementer for values that remain unresolved after that
fresh describe evidence is inspected, or for custom/EFF/provider details that no
documented describe route can safely derive.

If the user requires fresh data or prohibits cached data, perform a new
authenticated describe request and create a new response file outside the
repository. Do not reuse a prior response, project artifact, or OAuth result as
metadata evidence; pass the probe's fresh-login option when authentication is
needed.

For workflow-authorized GET-only metadata probes, use the task-local
`scripts/fusion_rest_curl_probe.py` and the rules in
`ora-resource/ora_reference_lookups.md`. The wrapper enforces the task-specific
CRM `/describe` and output-location boundaries, then delegates OAuth and HTTP
execution to `core.fusion-api.rest-api-client`.

## Assessment Output

Return one inline `service_mapping_assessment` with: validated XML context,
source and target entities and attributes, read/write evidence, provider/source
evidence, direct-assignment evidence, metadata candidates and type,
`mapping_status`, `algorithm_recommendation`, assumptions, prerequisites, and
interface-table lineage when applicable.

Allowed `mapping_status` values are `existing_mapping`,
`source_target_available`, `mapping_gap`, `metadata_blocked`, and
`incompatible`. Allowed `algorithm_recommendation` values are
`algorithm_not_required`, `algorithm_assessment_required`, and
`service_mapping_prerequisite`.

Return `service_mapping_ui_change_plan` directly in chat for the **Entities**,
**Sources**, and **Services** tabs. For each tab, state `no_change` with exact
rows to verify, or `change_required` with the row to add or edit, entity,
attribute, type, source mapping, and read/write setting. Do not create a
human-readable Markdown plan artifact or revised Service Mapping XML.

When information is missing, include `mapping_information_request` as a table
with exactly **Required Input**, **Why Needed**, and **Usage**. Ask only for
material values that cannot be derived from the XML, documented describe
metadata, or use-case defaults; keep independently configurable values in
separate rows.

Present results in this order: `## Result`, brief evidence, Service Mapping
changes table, required inputs when applicable, `## Validation`, guided current
stage and one free-text question only when action is needed, then
`## Exact steps used`. Use tables only for the UI change plan and missing-input
request.

If the complete three-tab plan is known but no post-change `OMIntegration`
export validates it, ask exactly: **"Service Mapping configuration has not been
revalidated from a post-change OMIntegration export. Do you want to skip this
validation step?"** On an explicit yes, record
`service_mapping_validation_skipped=true`, retain `mapping_status="mapping_gap"`
and `algorithm_recommendation="service_mapping_prerequisite"`, and hand off
only as a provisional plan.

## Workflow Summary

1. Validate required inputs and the `OMIntegration` root.
2. Inspect XML entities, attributes, providers, services, and assignment
   evidence before any metadata lookup.
3. Establish `OSSTransactions` lineage for cross-entity outcomes.
4. For every unresolved requested standard source or target entity, use its
   documented read-only describe evidence before concluding that the field is
   unavailable, asking for the field name, or returning a Service Mapping gap;
   use the exact documented parent-to-child branch for child entities.
5. Classify the result as existing mapping, available-without-assignment,
   mapping gap, metadata blocker, or incompatibility.
6. Return exact Entities, Sources, and Services tab instructions in chat.
7. Request only unresolved technical inputs, or ask the validation-skip question
   when the plan is complete but not revalidated.
8. Hand off the completed assessment or provisional mapping-gap plan to the
   companion Algorithm task.

## Outputs

- Inline Service Mapping assessment and recommendations
- Inline Entities, Sources, and Services UI steps
- Inline Algorithm recommendation and prerequisites
- `validation_result`
- `skill_run_record`
- `token_usage_record`

## Companion Task

Use `cx.subscriptions.integration-setup.manage-algorithms-for-order-management-to-subscriptions`
after this assessment is accepted. This Service Mapping task does not initiate,
sequence, or implement the Algorithm task.

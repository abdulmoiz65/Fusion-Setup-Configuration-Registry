---
skill_id: "cx.subscriptions.integration-setup.manage-algorithms-for-order-management-to-subscriptions"
name: "Manage Algorithms for Order Management to Subscriptions Advisory"
description: "Primary workflow for FOM-to-OSS Algorithm necessity assessment, Algorithm_BO.xml validation, safe in-progress-version selection, and approved local artifact preparation. It never imports, publishes, or deploys Fusion changes."
layer: "pillar"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Integration Setup"
functional_area_code: "CUSTOM_INTEGRATION_SETUP"
task_code: "CUSTOM_MANAGE_ALGORITHMS_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS"
task_name: "Manage Algorithms for Order Management to Subscriptions"
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
  - "algorithm_bo_xml"
  - "algorithm_source_definition_when_available"
  - "service_mapping_source_xml"
  - "service_mapping_assessment"
  - "service_mapping_ui_change_plan_when_provisional"
  - "resolved_mapping_information_when_available"
  - "continue_provisional_artifact_generation_when_requested"
  - "implementation_project_context"
outputs:
  - "inline_algorithm_recommendation"
  - "inline_algorithm_change_draft"
  - "algorithm_bo_import_artifact"
  - "subscription_management_and_order_management_integration_archive"
  - "validation_result"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "cx.subscriptions.integration-setup.manage-service-mappings-for-order-management-to-subscriptions"
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
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_export"
    default_location: "project/{project_id}/exports/manage-algorithms-for-order-management-to-subscriptions/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "other"
    default_location: "project/{project_id}/exports/manage-algorithms-for-order-management-to-subscriptions/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/subscriptions/integration-setup/manage-algorithms-for-order-management-to-subscriptions/current/"
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
  - "Creates a local Algorithm_BO.xml and SubscriptionManagementandOrderManagementIntegration.zip only after explicit approval of the exact reviewed change; a provisional artifact also requires a separate explicit continuation after its warning."
required_privileges: []
---

# Manage Algorithms for Order Management to Subscriptions

## Purpose

Consume the validated FOM-to-OSS Service Mapping assessment, decide whether an
Algorithm change is required, prepare an inline review draft when supported,
and create a local `Algorithm_BO.xml` plus
`SubscriptionManagementandOrderManagementIntegration.zip` only after the
required approval gates. This skill never imports, publishes, deploys, or
runtime-tests Fusion configuration.

## Resource Load Order

Use these task-local resources progressively; read only the files needed for the
current algorithm stage.

1. `ora-resource/ora_input_validation.md` for required inputs, mapping
   dependency, algorithm identity, active-version selection, Custom EFF rules,
   provisional gates, and artifact validation.
2. `ora-resource/ora_dependency_readiness.md` before deciding whether mapping,
   algorithm export, target version, approval, or artifact prerequisites are
   satisfied.
3. `ora-resource/ora_reference_lookups.md` to interpret mapping statuses and
   choose no-change, draft, provisional, or blocker outcomes.
4. `ora-resource/ora_design_enforcement.md` for OSSTransactions-first actions,
   `RUN_SCRIPT` preservation, version integrity, approval boundaries, and
   no-import enforcement.
5. `references/ora_conditional_action_serialization.md` whenever an approved
   artifact must add a new `CONDITIONAL_ACTION` to an eligible version.
6. `ora-resource/ora_error_handling.md` for blockers, refusal cases,
   provisional warnings, and disclosure requirements.
7. `ora-resource/ora_rule_registry.json` when a durable rule-node trace or
   machine-readable route is needed.

## Essential Contract

Require a business requirement and a validated `service_mapping_assessment` for
every recommendation, draft, or artifact. Require a current `Algorithm_BO.xml`
when inspecting existing logic, drafting against an export, or creating a local
artifact. If a Service Mapping XML is supplied as evidence, validate its root as
`contextName="OMIntegration"` before using it.

Accept only an `AlgorithmSetupVO` named `Subscription Management and Order
Management Integration`. Versions `0` and `1` are immutable. For a draft or
artifact, edit the highest numeric nonprotected version with `ActiveFlag="Y"`;
if none exists, create only the next unused numeric version with
`ActiveFlag="Y"`. Never generate `ActiveFlag="P"` as a target state.

Interpret `existing_mapping` plus `algorithm_not_required` as no algorithm
change unless an independent documented logic requirement is present. Interpret
`source_target_available` plus `algorithm_assessment_required` as a reviewable
draft candidate. Treat `mapping_gap`, `metadata_blocked`, `incompatible`, or
`service_mapping_prerequisite` as a Service Mapping prerequisite except for the
controlled provisional paths in the task-local resources.

For cross-entity actions, require the assessment's XML-evidenced
`OSSTransactions` bridge and intended cardinality. A direct product-to-source
key can be a consistency check only; it must not replace interface-table
traversal or justify an arbitrary collection scan.

Preserve the delivered `Process Order Management Transactions` `RUN_SCRIPT` step
and downstream invocation unchanged. Add cross-entity logic as a separate
`CONDITIONAL_ACTION` or `NESTED_ACTION`; for product-level actions, prefer an
`OSSTransactions` primary set with `ZERO_OR_ONE` contained target, owner, and
source sets, then guarded assignments.

## Mandatory Action-Creation Ownership

When the eligible active version contains only the delivered `RUN_SCRIPT` and
the approved change requires declarative cross-entity logic, **this skill must
create the separate canonical `CONDITIONAL_ACTION` itself**. Treat the absent
action as an action-creation case, not as a user prerequisite or a blocker.
Use `references/ora_conditional_action_serialization.md`, preserve the
`RUN_SCRIPT` byte-for-byte, and assign the next available sequence number.

Do not ask the user for a conditional-action sample, XML schema, or existing
action merely because the current export lacks one. User-supplied source,
target, lineage, type, approval, and provisional-continuation requirements
still apply; only those missing business-contract inputs can block creation.

For Custom EFF actions, use only exact source, target, aliases, joins, types,
permissions, conversion rules, and blank/null behavior from the companion
assessment. Missing target, owner, EFF row, source value, or cardinality mismatch
must leave the target unchanged. For string sources, guard both null and
non-whitespace before assignment.

Do not use historical P/N versions or examples for business-specific content,
aliases, joins, IDs, action names, or expressions. They may provide structure
only when the current request supplies the validated business contract.

## Draft and Artifact Gates

First return the Algorithm recommendation and any reviewable change draft
directly in chat. Put source in one fenced `groovy` block; state selected
version, expected result, source-null and blank behavior, overwrite behavior,
unmatched or duplicate handling, runtime assumptions, and affected mapping
assessment. Do not create a human-readable Markdown draft file.

Create no local artifact until the user explicitly approves the exact inline
draft. For a provisional mapping-gap draft, approval is still not enough: show
this warning and require a separate explicit yes before creating local XML:

> **Warning:** The required Service Mapping changes are planned and the Service
> Mapping validation was skipped or has not yet been completed. This provisional
> `Algorithm_BO.xml` references the proposed EFF mapping and must not be
> imported or runtime-tested until a current `OMIntegration` export proves those
> Entities, Sources, and Services rows. Continue to generate the local
> provisional `Algorithm_BO.xml`?

After approval and any required provisional continuation, return a well-formed
local file named exactly `Algorithm_BO.xml`. Preserve every nonselected version
subtree, compare Versions `0` and `1` for integrity, verify algorithm identity
and target selection, then create
`SubscriptionManagementandOrderManagementIntegration.zip` containing exactly one
top-level byte-identical `Algorithm_BO.xml`.

Record `provisional=true`, the unfulfilled Service Mapping prerequisite, and
the warning only in validation or registry metadata, never as a non-schema XML
marker. Never represent a provisional artifact as ready to import.

## Workflow Summary

1. Validate the mapping assessment and any supplied `OMIntegration` XML.
2. Validate `Algorithm_BO.xml` identity when existing logic, a draft, or an
   artifact is requested.
3. Classify the mapping outcome as no-change, draft candidate, Service Mapping
   prerequisite, or controlled provisional candidate.
4. Select the latest nonprotected active version, or plan the next active
   version only when no eligible target exists.
5. Draft the separate guarded action from validated assessment evidence and
   present it inline for review.
6. Require explicit draft approval and, for provisional output, the separate
   warning continuation.
7. Generate and validate the local XML and ZIP only after all applicable gates
   pass.

## Outputs

- Inline Algorithm recommendation
- Inline Algorithm change draft with fenced Groovy source
- `algorithm_bo_import_artifact`
- `SubscriptionManagementandOrderManagementIntegration.zip`
- `validation_result`
- `skill_run_record`
- `token_usage_record`

## Non-goals

This task does not diagnose runtime transactions, discover Service Mapping
attributes through direct REST, modify protected versions, import, publish,
deploy, or perform Fusion runtime testing.

---
skill_id: "scm.manufacturing-and-supply-chain-materials-management.supply-chain-financial-flows.register-financial-orchestration-third-party-transfer-pricing-service"
name: "Register Financial Orchestration Third-Party Transfer Pricing Service"
description: "Registers or updates the Financial Orchestration third-party transfer-pricing service URL and security policy through the approved Topology Manager endpoint workflow."
layer: "pillar"
pillar: "SCM"
offering: "Manufacturing and Supply Chain Materials Management"
functional_area: "Supply Chain Financial Flows"
functional_area_code: "ORA_FOS_SUPPLY_CHAIN_FIN_FLOW"
task_code: "ORA_FOS_REGISTER_PRICING_STUB"
task_name: "Register Financial Orchestration Third-Party Transfer Pricing Service"
parent_skill_id: "scm.manufacturing-and-supply-chain-materials-management.supply-chain-financial-flows"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "planning"
execution_mode: "assisted"
owner_team: "SCM manufacturing and supply chain materials management pillar team"
version: "0.1.0"
inputs:
  - "fusion_environment_context"
  - "service_url"
  - "security_policy"
  - "execution_options"
outputs:
  - "registration_preview"
  - "execution_result"
  - "diagnostics"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.baseline-assessment.topology-manager.application-endpoint"
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
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-financial-flows/register-financial-orchestration-third-party-transfer-pricing-service/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/scm/manufacturing-and-supply-chain-materials-management/supply-chain-financial-flows/register-financial-orchestration-third-party-transfer-pricing-service/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
applicability:
  industries: ["All"]
  countries: ["All"]
  fusion_releases: ["Current Oracle Fusion Cloud Applications release"]
side_effects: ["May register or update the third-party transfer-pricing service after explicit approval."]
required_privileges: ["Fusion setup privilege for the selected task and Topology Manager endpoint write access"]
---

# Register Financial Orchestration Third-Party Transfer Pricing Service

## Purpose

Register or update the URL and security policy for the Financial Orchestration
third-party transfer-pricing service. This is the task-specific FOS wrapper for
the shared Topology Manager application-endpoint workflow.

## Scope and routing

Use this skill only for setup task `ORA_FOS_REGISTER_PRICING_STUB`. The setup
page exposes two business inputs: **URL** and **Security Policy**. Do not ask
the user for an application identifier or endpoint key.

Route the request to
`shared.baseline-assessment.topology-manager.application-endpoint`. That skill
owns endpoint registration/update, security-policy validation, credential
redaction, request previews, and the underlying Topology Manager calls. This
wrapper supplies the verified task-to-endpoint mapping from the target
environment context; never invent or expose that technical mapping.

If the mapping is unavailable or does not resolve exactly one registered
endpoint, stop before any write and report that the service registration cannot
be resolved in the target environment. Do not substitute a similarly named
endpoint.

## Required inputs

- **URL** — required and passed as the endpoint URL.
- **Security Policy** — required and must be one of the values available in
  the selected Fusion page's Security Policy control.

Read the exact task page before planning a mutation. If the URL or Security
Policy control, or **Save and Close**, is unavailable or disabled, do not use
another route to bypass it. Respond: `Operation is not permitted due to a
privilege issue.`

## Confirmation and execution

Before writing, show one clear confirmation preview containing the target
environment, URL, and Security Policy. State that the operation will register
or update the third-party transfer-pricing service. Do not include technical
endpoint identifiers, credentials, tokens, or security-policy secrets.

After explicit confirmation:

1. Delegate the endpoint URL and policy operation to the shared Topology
   Manager skill.
2. Let the delegated skill determine whether the resolved endpoint requires a
   create or update and apply its exact preview, preflight, and approval rules.
3. Report the resulting registration status or the returned privilege/error
   message. Do not automatically retry a failed, timed-out, or unknown-outcome
   mutation.

Treat a successful completed delegated operation as equivalent to selecting
**Save and Close** on the Fusion setup page. Verify the resulting endpoint and
policy through the delegated skill's supported read path.

## Boundaries

- This task has no supported setup-data export, import, or CSV route.
- Change only the URL and/or Security Policy the user explicitly supplied.
- A user-facing request contains only URL and Security Policy; internal
  Topology Manager identifiers remain task-owned implementation data.

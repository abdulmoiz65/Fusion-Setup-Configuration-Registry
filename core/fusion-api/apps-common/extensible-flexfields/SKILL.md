---
skill_id: "core.fusion-api.apps-common.extensible-flexfields"
name: "Apps Common Extensible Flexfields"
description: "Manages Oracle Fusion Extensible Flexfield setup data through task-level CSV export, approved Data Loader FSM CSV import, and approval-gated REST deployment status workflows."
layer: "core"
pillar: "Core"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "Central platform team"
version: "0.3.1"
inputs: ["fusion_environment_context", "eff_task_context", "flexfield_deployment_context", "post_deployment_action", "execution_options"]
outputs: ["execution_result", "post_deployment_result", "diagnostics", "audit_summary"]
depends_on: ["shared.setup-export.task-level-export", "core.data-loader", "core.fusion-api.rest-api-client"]
uses_core: ["core.fusion-api.rest-api-client"]
persists_project_state: false
workspace_outputs: []
applicability:
  industries: ["All"]
  countries: ["All"]
  fusion_releases: ["Current Oracle Fusion Cloud Applications release"]
side_effects: ["May export EFF setup data, submit an approved FSM CSV import, or submit an approval-gated EFF deployment request."]
required_privileges: ["Fusion privileges required by the selected setup-task export, Data Loader, and EFF deployment workflows"]
---

# Apps Common Extensible Flexfields

## Purpose

Manage EFF setup-data tasks routed from pillar setup-task skills without owning
CSV transport. Read [EFF setup-task guidance](references/extensible-flexfields.md)
before acting.

Use `shared.setup-export.task-level-export` only for export and
`core.data-loader` only for approved FSM CSV import. For EFF metadata
deployment or deployment status, use only `core.fusion-api.rest-api-client`
as specified in the EFF reference.

## EFF Deployment Workflow

Read the **REST Deployment and Status** section of
[EFF setup-task guidance](references/extensible-flexfields.md). It is separate
from CSV import: an EFF deployment compiles the already-configured flexfield;
it does not transport setup data. After the **Import EFF Setup Data** workflow
has completed successfully, enter this workflow for the imported EFF. Do not
deploy after an incomplete or failed import.

1. Preflight the confirmed target environment, `application_id`, EFF
   `flexfield_code`, optional `force_deployment` value (`"true"` or
   `"false"`), and the caller's required Fusion privilege. When the calling
   skill omits it, set `forceDeployment` to the documented default, `"false"`.
   Preserve URL encoding in the flexfield code (for example, `%23`); do not
   infer or substitute identifiers.
2. For a live deployment, present the exact target environment, POST endpoint,
   and immutable JSON payload, then obtain explicit approval immediately before
   invoking the REST client. Submit the request with `fusion_rest_client.py`,
   which uses the default Fusion `scope` for `/fscmUI/applcoreApi`.
3. Capture `jobId`, `jobStatus`, `deploymentStatus`, `validationStatus`,
   `validationReport`, `deploymentErrorMessage`, and the response links. Do
   not retry a POST without explicit approval.
4. For status, call the documented `getDeploymentState` GET endpoint through
   the REST client using the same resolved identifiers. Poll only when asked,
   using the bounded interval and timeout in the reference; stop at a terminal
   response or timeout.
5. Run a caller-supplied `post_deployment_action` only after status confirms
   `DEPLOYED`. Follow the **Task-Specific Post-Deployment Action** section of
   the EFF reference. Do not infer, substitute, or run a post-deployment action
   for a task that does not explicitly define one.

## Preflight and Error Handling

Resolve task identity from the calling pillar skill, verify
`ExportImportSupportedFlag`, and preflight the selected workflow's target,
artifact, and approval requirements. Classify an unsupported task as
`catalog_or_metadata_mismatch` and an unapproved import as
`approval_blocker`. Redact credentials, tokens, and sensitive setup data from
diagnostics.

For deployment, classify malformed identifiers or force values as
`input_validation`; a 401/403 after the REST client's one refresh attempt as
`authorization_or_privilege`; HTTP failures as `fusion_api_error`; and a
nonterminal result at the polling limit as `process_timeout`. Return the last
safe status and job ID to the calling project workflow; never persist OAuth
tokens, secrets, Authorization headers, or sensitive setup data.

For a caller-supplied post-deployment action, classify a missing successful
`DEPLOYED` status as `process_failed`, an unapproved POST as
`approval_blocker`, and an unsuccessful job result as `process_failed`.
Capture the response and any request identifier in `post_deployment_result`.
Do not retry the POST without a new explicit approval.

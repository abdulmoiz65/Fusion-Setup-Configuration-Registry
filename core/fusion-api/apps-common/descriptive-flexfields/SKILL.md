---
skill_id: "core.fusion-api.apps-common.descriptive-flexfields"
name: "Apps Common Descriptive Flexfields"
description: "Resolves and validates Oracle Fusion Descriptive Flexfield context and segment designs, then routes task-level CSV export, approved Data Loader FSM CSV import, and approval-gated REST deployment status workflows."
layer: "core"
pillar: "Core"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "Central platform team"
version: "0.5.0"
inputs: ["fusion_environment_context", "dff_task_context", "dff_segment_or_context_specification", "candidate_fsm_zip", "flexfield_deployment_context", "execution_options"]
outputs: ["resolved_dff_blueprint", "validation_result", "execution_result", "diagnostics", "audit_summary"]
depends_on: ["shared.setup-export.task-level-export", "core.data-loader", "core.fusion-api.rest-api-client", "core.fusion-api.apps-common.value-sets"]
uses_core: ["core.fusion-api.rest-api-client", "core.fusion-api.apps-common.value-sets"]
persists_project_state: false
workspace_outputs: []
applicability:
  industries: ["All"]
  countries: ["All"]
  fusion_releases: ["Current Oracle Fusion Cloud Applications release"]
side_effects: ["May read value-set definitions, export DFF setup data, submit an approved FSM CSV import, or submit an approval-gated DFF deployment request."]
required_privileges: ["Fusion privileges required by the selected setup-task export, Data Loader, and DFF deployment workflows"]
---

# Apps Common Descriptive Flexfields

## Purpose

Provide a focused DFF setup-data route without owning CSV transport.

Read [DFF setup-task guidance](references/descriptive-flexfields.md) before
acting. Use `shared.setup-export.task-level-export` only for export and
`core.data-loader` only for approved FSM CSV import. For DFF metadata
deployment or deployment status, use only `core.fusion-api.rest-api-client`
as specified in the DFF reference.

## Segment and Context Design

For a DFF context or global/context-sensitive segment create or update, read
[defaulting rules](references/defaulting-rules.md) and resolve only values the
user omitted. Show the supplied, derived, and still-pending values in a
user-visible DFF blueprint before preparing an FSM ZIP. Include `ColumnName`
(Table Column) for every global and context-sensitive segment, showing the
resolved column or its pending status and reason. Keep `ShortPrompt` out of the
user-visible blueprint as specified in the defaulting rules. Return the resolved
design and its provenance to the calling task workflow for project-workspace
persistence. A displayed default is a proposal subject to the validation and
approval gates below; it does not authorize a Fusion write.

Read [mandatory validations](references/validations.md) before preparing an FSM ZIP
or handing a supplied ZIP to Data Loader. Validate the requested design against
the exact DFF task context, the current task-scoped export, and the candidate
package. When a segment has a value-set code, invoke
`core.fusion-api.apps-common.value-sets` for the live definition check described
there. Return each failed or unresolved check to the calling task workflow and
stop before import approval or deployment. These DFF checks supplement, and do
not replace, `core.data-loader` source validation and Task Hook approval.

## DFF Deployment Workflow

Read the **REST Deployment and Status** section of
[DFF setup-task guidance](references/descriptive-flexfields.md). Deployment
compiles the configured DFF; it is not a CSV import. After the **Import DFF
Setup Data** workflow has completed successfully, enter this workflow for the
imported DFF. Do not deploy after an incomplete or failed import.

1. Preflight the confirmed target environment, `application_id`, DFF
   `flexfield_code`, optional `force_deployment` value (`"true"` or
   `"false"`), and the caller's required Fusion privilege. When the calling
   skill omits it, set `forceDeployment` to the documented default, `"false"`.
   Preserve URL encoding in the flexfield code; do not infer or substitute
   identifiers.
2. For a live deployment, present the exact target environment, POST endpoint,
   and immutable JSON payload, then obtain explicit approval immediately before
   invoking the REST client. Submit with `fusion_rest_client.py`, using the
   default Fusion `scope` for `/fscmUI/applcoreApi`.
3. Capture `jobId`, `jobStatus`, `deploymentStatus`, `validationStatus`,
   `validationReport`, `deploymentErrorMessage`, and the response links. Do
   not retry a POST without explicit approval.
4. For status, call the documented `getDeploymentState` GET endpoint through
   the REST client using the same resolved identifiers. Poll only when asked,
   using the bounded interval and timeout in the reference; stop at a terminal
   response or timeout.

## Preflight and Error Handling

Preflight task identity, catalog eligibility, artifact shape, target
environment, and required approval with the selected workflow. Classify an
unsupported task as `catalog_or_metadata_mismatch` and an unapproved import as
`approval_blocker`. Redact credentials, tokens, and sensitive setup data from
diagnostics.

For deployment, classify malformed identifiers or force values as
`input_validation`; a 401/403 after the REST client's one refresh attempt as
`authorization_or_privilege`; HTTP failures as `fusion_api_error`; and a
nonterminal result at the polling limit as `process_timeout`. Return the last
safe status and job ID to the calling project workflow; never persist OAuth
tokens, secrets, Authorization headers, or sensitive setup data.

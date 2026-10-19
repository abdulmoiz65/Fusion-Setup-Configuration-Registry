---
skill_id: "hcm.hcm-tool.alert-foundation"
name: "Alert Foundation Skill"
description: "Provides governed HCM Tool alert planning, validation, read-only discovery, preview, and approval-gated eventAlerts CRUD operations for HCM and non-HCM consumers."
layer: "pillar"
pillar: "HCM"
offering: "HCM Tool"
functional_area: "Alert Foundation"
functional_area_code: "CUSTOM_ALERT_FOUNDATION"
required_setup_tasks:
  - "CUSTOM_ALERTS"
type: "planning"
execution_mode: "hybrid"
owner_team: "HCM hcm tool pillar team"
version: "0.11.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "alert_foundation_scope"
  - "alert_foundation_requirements"
  - "requested_intent"
  - "target_environment"
  - "source_artifact"
  - "source_workbook"
  - "alert_execution_mode"
  - "validation_mode"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "execution_preview"
  - "execution_work_unit_preview"
  - "execution_result"
  - "verification_result"
  - "business_execution_summary"
  - "technical_execution_report"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
  - "core.fusion-api.rest-api-client"
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
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/alert-foundation/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/alert-foundation/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/hcm-tool/alert-foundation/current/"
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
  - "May submit one JSON batch-create POST for all included workbook Alert hierarchies after provider gates and one exact aggregate approval; no automatic write retry or rollback."
  - "Performs governed read-only Fusion REST describe, lookup, finder, item, and child requests when the routed workflow reaches the external-read step."
  - "May execute an ordered Alert hierarchy create work unit after the compiled gates pass and the user approves its exact aggregate fingerprint immediately before execution."
  - "May create, update, disable, delete, or copy an event alert outside that bounded create work unit only after the compiled gates pass and the user approves the exact immutable mutation preview immediately before submission."
  - "May refresh the local gitignored OAuth token cache through the shared REST client."
required_privileges:
  - "Fusion privileges appropriate to the selected eventAlerts operation; the product owner states the authenticated role used for resource GET access is also authorized for the described CRUD methods."
---

# Alert Foundation Skill

## Purpose

Provides a shared Alerts provider for HCM and non-HCM consumer skills. It owns
business-intent normalization, governed `eventAlerts` discovery, immutable
preview, approval-gated CRUD execution, independent verification, and redacted
project evidence.

## When to Use

Use this functional-area skill after HCM Tool scope is confirmed and the project needs alert foundation setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `HCM Tool` (`CUSTOM_HCM_TOOL`)
- Functional area / Setup Object: `Alert Foundation` (`CUSTOM_ALERT_FOUNDATION`)
- Required setup task: `Alerts` (`CUSTOM_ALERTS`)

## Provider Contract

### Execution-mode selection

`alert_execution_mode` defaults to `sequential`; only an explicit batch-create
request selects batch packaging. Independently, `validation_mode` defaults to
`simple` and accepts only `simple` or `deep`. Both use contract `0.11.0`.
Load [validation modes](references/validation-modes.md) before selecting gates.
Simple CREATE uses local checks only; deep adds declared live preflight checks.
Keep approval phrases and submission behavior, but regenerate older previews:
validation mode and policy now form part of the approval fingerprint.

For `batch-create`, load [the batch-create runbook](references/batch-create-runbook.md).
It governs workbook packaging, approval and submission instead of the sequential
packaging/execution instructions below: the entire selected workbook becomes
one immutable work unit, with one JSON `parts` entry per included Alert hierarchy,
one `Confirm Alert Batch <SHA256>` approval, and one POST. Inline Body is encoded
once as UTF-8 Base64 inside its Template; no separate Body PATCH is submitted.
The JSON batch media type is not MIME `multipart/form-data`.
Before asking for its final approval, prove authentication readiness. The
noninteractive batch mutation mode accepts only a currently valid cached token;
it never opens login, refreshes credentials, or dispatches when the cache is
absent or expired. Each batch preview includes a unique attempt id and recovery
context in its approval digest, so a recovery POST always needs a fresh preview
and exact `Confirm Alert Batch <SHA256>` phrase. Persist a sanitized atomic
execution receipt containing only approval/authentication/request/response
lifecycle stages. A failure before `request_started` is `not_submitted`; after
it starts without a response it is `outcome_unknown`. Never retry a POST
automatically.
For batch-create, complete Fusion login/authentication-readiness before approval,
then dispatch with `--cached-token-only`. The adapter atomically reserves a new
receipt after approval validation and fsyncs the ordered transitions:
`approval_validated`, `authentication_ready`, `request_started`, and
`response_received`. A pre-existing, changed, completed, or mismatched receipt
blocks authentication and dispatch; interruption inside the POST remains
durably `outcome_unknown` for reconciliation.
The immutable batch document contains the active `project_id` and the generated
project-owned `execution_receipt_reference`
`project/<project-id>/state/runs/alert-receipts/<attempt-id>.json`. It resolves
from repository root, and `--receipt-output` must match it exactly, so a
different working directory or unsafe path cannot bypass replay prevention.

Load [the Alert Foundation provider contract](references/provider-contract.md)
before accepting requirements from an HCM or non-HCM consumer skill. The
contract defines the stable request and response boundary, provider and
consumer responsibilities, observed REST capability, supported operations,
approval discipline, failure handling, and refusal rules.

This functional-area skill owns the shared Alerts provider boundary. Consumers
must depend on `hcm.hcm-tool.alert-foundation` and provide business intent; they
must not call `eventAlerts`, copy its schema, select a transport, or hand-build
a REST payload.

Version `0.8.0` supports workbook intake, planning, validation, governed read-only discovery,
immutable payload preview, and approval-gated create, update, disable, delete,
and copy through the shared REST client. The bounded workbook route can package
one Alert CREATE, its Template CREATE operations, each optional inline
plain-text Body PATCH, and their Template Recipient CREATE operations into one
immutable Alert hierarchy work unit. One
explicit approval binds to the aggregate work-unit fingerprint and authorizes
only that exact ordered sequence. File-based Template Body enclosure execution,
upsert, and `processAlert` remain excluded. A workbook, plan, prior approval, or
successful GET never authorizes a mutation.

When the `Alert Templates.Body` cell contains plain text, omit `Body` from the
Template POST, verify the created Template, then PATCH the exact Template item
with `{"Body": "<exact workbook text>"}` before creating its Recipients. For
version `0.8.0`, HTTP 200 from that PATCH is the accepted verification result;
independent stored-content read-back is deferred and must be disclosed in the
preview and result. A blank or absent `Body` column preserves the legacy
Alert -> Template -> Recipient sequence. `Body` is mutually exclusive with
`BodyFilePath` and `BodyFileSHA256`, which remain future file-enclosure inputs.

Template Recipient `ValueExpression` remains required and is validated locally
for presence and maximum length. Live validation through the eventAlerts
`validateExpression` action is deferred in version `0.8.0`; do not call that
action or treat its absence as a preview or execution blocker. Reintroducing
live expression validation requires a separately reviewed provider-contract
change.

## Required Runtime Resources

Before validation or execution, load the compiled task-node execution guide,
the flat [Alerts setup-task metadata](alerts.md), this skill's
`ora-resource/ora_rule_registry.json`, the planner result, every reached source
anchor, [the provider contract](references/provider-contract.md), and [the
mutation runbook](references/mutation-runbook.md). Build the task rule plan with
`--setup-task Alerts`; it must be ready without a readiness override.

For workbook intake, prefer the installed host skill
`spreadsheets:Spreadsheets` when its artifact runtime is available. For the
bounded `.xlsx`-to-payload-plan workflow, use
`scripts/read-alert-intake.py` as the Alert-specific basic backend. The basic
backend requires `openpyxl`, is read-only, and cannot execute a REST request.
Do not list the host skill under `uses_core`; that field contains only
repo-native FDOS skill IDs.

## Provider Workflow

1. Validate the provider-contract version, consumer identity, project context,
   requested intent, and alert requirement. If the request supplies an Excel
   workbook, first use the host spreadsheet capability or the bounded basic
   reader using this provider's workbook mapping; stop unless it produces a
   valid preview candidate.
2. Classify the normalized request as planning, read-only discovery, preview, mutation,
   or notification delivery.
3. For planning and preview, produce a canonical configuration blueprint and
   expose unresolved facts required by the selected validation mode as `TBD`
   or a blocker. Simple CREATE explicitly delegates business-value checks to
   Fusion; skipped live checks are not unresolved blockers or passed checks.
4. For a read-only request, continue only when the active implementation
   workflow reaches its declared external-read step and selects the approved
   core REST route. Preserve sanitized evidence under the project workspace.
5. For sequential bounded Alert hierarchy CREATE, build the `Alerts` task rule plan,
   execute every reached preflight node, and produce one work-unit preview that
   contains the exact environment, ordered methods, URIs, canonical payloads,
   per-operation digests, effects, verification requests, execution policy,
   and aggregate SHA-256. Obtain one explicit approval for that aggregate
   fingerprint immediately before executing the work unit.
6. In sequential mode, after work-unit approval, route each mutation in order through
   `core.fusion-api.rest-api-client`, submit each operation exactly once, and
   verify it before continuing. Parent, Template, and Recipient creates require
   independent GET comparison. An inline Body PATCH is verified by its accepted
   HTTP 200 response in version `0.8.0`; disclose that independent Body read-back
   is deferred. Stop on the first failure or canonical-key mismatch. Report
   partial success; never automatically retry or roll back a write. Any change
   to environment, order, method, URI, payload, or verification contract
   invalidates the approval.
7. For update, disable, delete, copy, or a create outside the bounded hierarchy
   route, retain the individual immutable preview and immediate approval gate,
   followed by one submission and independent verification.
8. For upsert or `processAlert`, stop as unsupported. Do not substitute FSM,
   HDL, Data Loader, browser automation, or an ungoverned direct REST call.
9. Return the provider response contract with status, route, blueprint,
   evidence, diagnostics, and artifact references.

## Business and Technical Reporting

For CREATE preview and execution handoffs in either submission mode, use
[the reporting contract](references/execution-reporting.md). Produce one row
per Alert with Alert code, Alert name, Status, HTTP status, and a working
technical-details link. Generate the linked Markdown reports locally with
`scripts/render-alert-report.py` from sanitized, evidence-backed reporting
input. Keep actionable failures and deferred Body verification visible in the
business summary. Reporting never changes approval, execution or verification
gates, and never treats HTTP 200 alone as successful creation.

## Operation Object

The provider capability is `Alerts`. The observed initial REST adapter is
`/hcmRestApi/resources/11.13.18.05/eventAlerts`; the adapter is not the
capability identity. Deep preflight requires a target describe compatibility
check; simple CREATE uses the reviewed adapter without live describe. The provider contract owns the mapping so
consumer skills remain independent of REST release paths and transport details.

## Workbook Intake Route

For an Alert Foundation intake workbook, use the mapping in
[the provider contract](references/provider-contract.md). The expected sheets
are `Alerts` and `Alert Templates`; `Template Recipients` is optional. Correlate
included templates by exact `ClientAlertKey` and included recipients by exact
`ClientAlertKey` plus `TemplateKey` before building the provider request.

Run the basic reader from the repository root when the richer host spreadsheet
runtime is unavailable:

```text
python pillars/hcm/hcm-tool/alert-foundation/scripts/read-alert-intake.py <workbook.xlsx>
```

Supply `--target-environment https://<fusion-host>` when generating the
approval-bound work-unit preview. Without it, the reader emits a candidate
whose approval binding is incomplete. The provider may present the generated
approval phrase only after all gates applicable to the selected validation mode
pass without changing the work-unit document. Simple CREATE performs no live
preflight requests. Use `--validation-mode deep` to request enhanced checks.

Pass `--current-state` for UPDATE or DISABLE so PATCH contains only actual
differences and uses the server-returned canonical key. In deep mode, pass only MIME mappings
that were resolved from the exact target environment, for example
`--mime-type-map text/html=ORA_H`.

In sequential mode, each eligible work unit contains exactly one included Alert hierarchy. The
parent Alert, its Templates, each optional inline Body PATCH, and their
Recipients are ordered parent-first.
Client-supplied `AlertCode`, `TemplateCode`, and `RecipientCode` values form
the exact planned canonical item paths. If a create response returns a
different canonical key, stop the work unit before the next write.

Workbook fields are offline authoring input. `IncludeFlag`, `Operation`,
`ValidationStatus`, and `ValidationMessage` guide selection and validation but
do not select the execution adapter, prove Fusion readiness, or satisfy the
immediate approval gate. The provider owns payload construction; simple passes
literal business codes to Fusion, while deep revalidates them before approval.

## Setup Tasks

1. [Alerts](alerts.md) (`CUSTOM_ALERTS`)

## Inputs

- `implementation_objective`
- `project_context`
- `alert_foundation_scope`
- `alert_foundation_requirements`
- `requested_intent`
- `target_environment`
- `source_artifact`
- `source_workbook`
- `alert_execution_mode`
- `validation_mode`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `execution_preview`
- `execution_work_unit_preview`
- `execution_result`
- `verification_result`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the flat `Alerts` metadata artifact for catalog/task resolution while this
functional-area skill retains the customized provider runtime. Track token
usage for any generated project artifact or skill-run record using the manifest
policy.

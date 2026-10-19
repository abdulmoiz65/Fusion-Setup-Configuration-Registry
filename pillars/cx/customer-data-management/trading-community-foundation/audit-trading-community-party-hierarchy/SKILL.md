---
skill_id: "cx.customer-data-management.trading-community-foundation.audit-trading-community-party-hierarchy"
name: "Audit Trading Community Party Hierarchy Setup Task Guidance"
description: "Accepts Audit Party Hierarchy business parameters, builds a fixed ESS payload, previews it for approval, submits it once, and tracks the resulting Oracle Fusion scheduled process."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Trading Community Foundation"
functional_area_code: "ORA_HZ_CDM_FOUNDATION"
task_code: "HZ_RUN_HIERARCHY_AUDIT"
task_name: "Audit Trading Community Party Hierarchy"
parent_skill_id: "cx.customer-data-management.trading-community-foundation"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "ESS"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "CX customer data management pillar team"
version: "0.6.0"
inputs:
  - "execution_intent"
  - "fusion_environment_context"
  - "hierarchy_type"
  - "hierarchy_name"
  - "hierarchy_version"
  - "hierarchy_status"
  - "batch_id"
  - "requestId"
  - "execution_options"
  - "project_id"
outputs:
  - "execution_preview"
  - "ess_execution_result"
  - "diagnostics"
  - "skill_run_record"
  - "token_usage_record"
uses_core:
  - "core.fusion-api.ess-job-submitter"
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
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/audit-trading-community-party-hierarchy/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/audit-trading-community-party-hierarchy/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/audit-trading-community-party-hierarchy/current/"
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
  - "After an exact immutable preview and standalone approval, submits the Audit Party Hierarchy ESS scheduled process once to the selected Fusion environment."
  - "May log validation failures and may mark invalid hierarchies inactive; Oracle documentation is inconsistent about whether the audit changes the tree, so treat execution as potentially mutating."
  - "May refresh the local gitignored OAuth token cache through core.fusion-api.ess-job-submitter."
required_privileges:
  - "Manage Trading Community Import Batch Duty (ORA_MANAGE_TRADING_COMMUNITY_IMPORT_BATCH_DUTY)."
  - "Manage Trading Community Import Process Duty (ORA_MANAGE_TRADING_COMMUNITY_IMPORT_PROCESS_DUTY)."
---

# Audit Trading Community Party Hierarchy

## Purpose

Preview, submit, and track Oracle Fusion's `Audit Party Hierarchy` ESS scheduled process for setup task `HZ_RUN_HIERARCHY_AUDIT`. The process validates party hierarchy setup and records validation failures in its log.

This task is not a Data Loader import. Do not invoke `core.data-loader`, the task-level CSV exporter, or direct Scheduler REST calls.

## Setup Task Skill Contract

- task_code: `HZ_RUN_HIERARCHY_AUDIT`
- task_name: `Audit Trading Community Party Hierarchy`
- parent_skill_id: `cx.customer-data-management.trading-community-foundation`
- pillar: `CX`
- offering: `Customer Data Management`
- functional_area: `Trading Community Foundation`
- functional_area_code: `ORA_HZ_CDM_FOUNDATION`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `ESS`
- businessObject: ``
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Inputs

- `execution_intent`: advisory, preview-only, new submission, or status tracking for an existing `requestId`.
- `fusion_environment_context`: exactly one target Fusion environment for a new submission.
- `hierarchy_type`: mandatory internal hierarchy-type code. Do not submit a display label.
- `hierarchy_name`: optional environment-specific internal hierarchy identifier; use a null business argument when omitted.
- `hierarchy_version`: optional environment-specific internal hierarchy-version identifier; use a null business argument when omitted so ESS applies its active-version behavior.
- `hierarchy_status`: optional caller input for the mandatory ESS status argument; default an omitted value to the confirmed internal code `ACTIVE`.
- `batch_id`: optional batch identifier; preserve an explicitly supplied value exactly and use a null business argument when omitted.
- `requestId`: existing positive ESS request identifier; mutually exclusive with new-submission inputs.
- `execution_options`: optional bounded status-polling values.
- `project_id`: optional durable workspace. Do not create a project solely because this input is absent.

## Documented Business Parameter Contract

| Position | Parameter | Requirement | Documented behavior | Submission rule |
|---|---|---|---|---|
| 1 | Hierarchy Type | Mandatory to UI and skill | LOV `PARTY_HIERARCHY_TYPE`; the VO and PL/SQL default are `HZ_CUSTOMER_HIERARCHY` | Require an explicit internal code; do not silently apply the underlying source default |
| 2 | Hierarchy Name | Optional | Search-and-select hierarchy name | Require the target's internal hierarchy identifier when supplied; otherwise set business argument 2 to `null` |
| 3 | Hierarchy Version | Optional | Active version is the documented default | Require the target's internal version identifier when supplied; otherwise set business argument 3 to `null` and let ESS apply its default |
| 4 | Hierarchy Status | Mandatory to ESS | LOV `HZ_TREE_STATUS`; public choices are Active and Inactive | Default an omitted caller value to the confirmed internal code `ACTIVE` |
| 5 | Batch ID | Optional | Text input batch identifier | Preserve the exact supplied value; otherwise set business argument 5 to `null` |

Do not accept UI display text as proof of an internal submission value. Do not use a hierarchy name, version display date, lookup meaning, or historical identifier from another environment as the payload value.

## Confirmed Runtime Evidence

A successful historical request in the `cptcuqlqy` test environment on 2026-08-18 confirmed:

- Process display name: `Audit Party Hierarchy`
- Scheduler metadata name shown in the UI: `PartyHierarchyAudit`
- Terminal UI status: `Succeeded`
- Stored business-argument order: `argument1` through `argument5`
- UI mapping: `argument1` Hierarchy Type, `argument2` Hierarchy Name, `argument3` Hierarchy Version, `argument4` Hierarchy Status, `argument5` Batch ID
- Confirmed minimal stored values: `argument1=HZ_CUSTOMER_HIERARCHY`, `argument2=null`, `argument3=null`, `argument4=ACTIVE`, and `argument5=null`
- A separate successful request also showed non-null internal identifiers for Hierarchy Name and Hierarchy Version

Treat the request IDs and stored values as environment- and time-specific evidence. They prove the UI argument order, that arguments 2, 3, and 5 may be null, and that `ACTIVE` is an accepted internal status value. They do not prove the full allowed-value sets or parameter types.

Two later Scheduler submissions using REST names `ATTRIBUTE1` through `ATTRIBUTE5` completed with an empty UI parameter section. That runtime evidence proves the VO attribute names did not bind as this job's Scheduler request parameters. A Scheduler `Succeeded` state from either request proves process completion only and must not be represented as proof that the requested hierarchy type was applied.

## Source-Confirmed Parameter Model

The reviewed `ValidatePartyHierarchyParamVO` and `HZ_PARTY_TREE_AUDIT` package establish the following ordered model. All five values are Java `String`, VO SQL type `VARCHAR`, and PL/SQL `VARCHAR2`.

| Position | VO attribute | PL/SQL argument | Source default | LOV source |
|---|---|---|---|---|
| 1 | `ATTRIBUTE1` | `p_tree_structure_code` | `HZ_CUSTOMER_HIERARCHY` | `PARTY_HIERARCHY_TYPE` through `LOV_ATTRIBUTE1` |
| 2 | `ATTRIBUTE2` | `p_tree_code` | `NULL` | `HierarchyNameVO.FindByTS`, dependent on position 1 |
| 3 | `ATTRIBUTE3` | `p_tree_version_id` | `NULL` | `FndTreeVersionVO.AllVC`, dependent on positions 1 and 2 |
| 4 | `ATTRIBUTE4` | `p_status` | `ACTIVE` | `HZ_TREE_STATUS` through `LOV_ATTRIBUTE4` |
| 5 | `ATTRIBUTE5` | `p_batch_id` | `NULL` | None declared |

The procedure body forwards these five business arguments unchanged and in this order to `do_validate`. `ATTRIBUTE1` through `ATTRIBUTE5` are parameter-VO attribute names only; do not use them as Scheduler REST parameter names. Map the ordered business arguments to `submit.argument1` through `submit.argument5`, all with `paramType=STRING`.

## Fixed ESS Job Identity

| Field | Authoritative value |
|---|---|
| `jobDefinitionId` | `JobDefinition://oracle/apps/ess/cdm/foundation/parties/PartyHierarchyAudit` |
| `application` | `CrmEss` |
| `product` | `HZ` |
| Job type | `/oracle/as/ess/ext/JobType/PlsqlJobType.xml` |
| PL/SQL procedure | `hz_party_tree_audit.validate_batch_party_hierarchy` |
| Parameters VO | `oracle.apps.cdm.foundation.parties.auditTrees.publicEssModel.view.ValidatePartyHierarchyParamVO` |
| Business argument count | `5` |
| Default output extension | `txt` |

The full `jobDefinitionId` is constructed directly from the reviewed job metadata's exact `jobPackageName` (`oracle/apps/ess/cdm/foundation/parties/`) and `jobDefinitionName` (`PartyHierarchyAudit`). `SYS_effectiveApplication` proves application `CrmEss`, and `SYS_product` proves product `HZ`.

The job metadata declares `SYS_retries=5`. This is server-side job-definition metadata; the FSCR submission request must still use `--retries 0` so the client never retries an uncertain POST.

## Fixed REST Parameter Contract

Callers provide business values only. Do not ask callers for Scheduler parameter names, types, null serialization, job identity, application, or product.

Build `requestParameters` in this exact order:

```json
[
  {"name":"submit.argument1","paramType":"STRING","value":"<hierarchy_type>"},
  {"name":"submit.argument2","paramType":"STRING","value":""},
  {"name":"submit.argument3","paramType":"STRING","value":""},
  {"name":"submit.argument4","paramType":"STRING","value":"ACTIVE"}
]
```

Always include arguments 1 through 4 because argument 4 carries the required status. Use an empty string for an omitted Hierarchy Name or Hierarchy Version so their earlier positional placeholders remain present; the PL/SQL `VARCHAR2` procedure receives those empty strings as null values. When Batch ID is omitted, omit the unused trailing `submit.argument5` parameter. When Batch ID is supplied, append `{"name":"submit.argument5","paramType":"STRING","value":"<batch_id>"}`. Replace the empty placeholder for Hierarchy Name or Hierarchy Version with its exact validated value when supplied. When the caller supplies Hierarchy Status, replace `ACTIVE` with that validated internal code.

Reject any generated payload that uses `ATTRIBUTE1` through `ATTRIBUTE5` as request parameter names. Those identifiers belong only to `ValidatePartyHierarchyParamVO`; prior Scheduler submissions demonstrated that they are accepted at the HTTP boundary without binding to the displayed ESS arguments.

Use the fixed job identity from this skill. Do not inspect an older ESS request merely to reconstruct this contract, and do not ask the caller to provide technical ESS metadata.

## Preflight Checks

Before any new submission, confirm exactly one configured target environment,
the fixed job identity and positional parameter contract in this skill, the
required duty or job-role privilege, and all supplied business values. Confirm
that the project artifact destination is writable, that no conflicting active
request is known when target guidance requires that check, and that the exact
immutable preview has received standalone approval. Stop before side effects
when any preflight item is missing, ambiguous, or changed after approval.

## Execution Workflow

1. Classify the request as advisory, preview-only, new submission, or tracking an existing `requestId`. Never convert a status request into a new submission.
2. Only when the user explicitly asks to track an existing request, invoke the core skill with `--request-id <requestId>` and bounded polling. Preserve terminal Scheduler state, cause, ECID, and available diagnostics; do not submit another request.
3. For a new submission, resolve exactly one target Fusion environment. Require Hierarchy Type. Default an omitted Hierarchy Status to `ACTIVE`. Keep omitted Hierarchy Name, Hierarchy Version, and Batch ID business values as `null`; do not resolve or invent values for them.
4. Validate the selected Hierarchy Type and Hierarchy Status codes against their authoritative LOVs. Resolve any explicitly supplied Hierarchy Name or Hierarchy Version in the target. Reject display labels, ambiguous matches, identifiers copied from another environment, and unsupported Batch ID values.
5. Verify one of the documented duties or an applicable documented job role. Oracle documents no compatibility considerations or dependencies, but still check for an already-running equivalent request when target metadata or operating guidance requires it.
6. Build the exact payload using the Fixed REST Parameter Contract and the fixed ESS job identity. Assert that every emitted parameter name matches `submit.argument[1-5]` and that arguments are in ascending positional order. Do not perform historical-request discovery during a normal new run.
7. Present one concise immutable preview containing the target environment, job identity, five business values, exact emitted request parameters, potentially mutating hierarchy impact, `retries=0`, and preview fingerprint.
8. Stop and require a later standalone `approve` for that exact preview. Any change to environment, metadata, parameter value, null behavior, or fingerprint invalidates approval.
9. After approval, invoke `core.fusion-api.ess-job-submitter` with the exact approved contract, `--submit-only`, and `--retries 0`. Submit exactly once and capture the returned `requestId`.
10. Stop after submission. Monitor only after a separate explicit status request for that request ID.

## Approval and Retry Boundaries

- An initial request to run the audit authorizes validation and preview only.
- Only standalone `approve` authorizes the exact previewed ESS POST.
- Never retry an ESS POST automatically after transport failure, timeout, missing response, or missing request ID.
- Treat a missing request ID after submission as an uncertain mutation and reconcile server state before considering another request.
- Allow the core authentication workflow to refresh a rejected cached token once; token refresh does not authorize a second uncertain POST.
- Never claim hierarchy data is valid because the process reached `Succeeded`. Report business validation only from the process log and resulting hierarchy state.

## Oracle Behavior Conflict

The scheduled-process page says validation gaps are written to logs and no change is made to the tree. Oracle's hierarchy-validation guidance says a background audit job marks hierarchies that fail validation inactive. Until task-owner source or target verification reconciles these statements, disclose both and treat the job as potentially changing hierarchy status.

## Outputs

- `execution_preview`: exact target, technical contract, ordered internal values, impact warning, and approval fingerprint.
- `ess_execution_result`: request ID after submission, or terminal/last-known state for an explicit tracking request.
- `diagnostics`: failure class, missing evidence, safe next action, request ID, status, and available ECID without secrets.
- `skill_run_record`
- `token_usage_record`

## Failure Handling

Classify failures as `input_validation`, `catalog_mismatch`, `auth_or_authorization`, `transport_or_environment`, `Fusion_API`, `process_timeout`, `process_failed`, `artifact_persistence`, or `approval_blocker`. Preserve the request ID whenever one exists. On terminal failure, retrieve available Scheduler details and logs through declared workflows; never resubmit automatically.

Never print or persist access tokens, refresh tokens, client secrets, authorization headers, token-cache contents, or sensitive customer data.

## Golden Scenarios

| Scenario | Expected result |
|---|---|
| User supplies only Hierarchy Type | Emit `submit.argument1`, empty `submit.argument2` and `submit.argument3` placeholders, and `submit.argument4=ACTIVE`; omit trailing `submit.argument5`; show the preview without inspecting old requests |
| User supplies display labels | Resolve target internal values or stop; never submit the labels |
| User supplies a hierarchy display date | Resolve the internal version identifier or stop |
| Valid business parameters are supplied | Show the exact immutable preview and wait for standalone approval |
| Approved submission succeeds | Return the request ID and stop without polling |
| User supplies an existing request ID | Track that request without requiring the new-submission contract and without a POST |
| Polling times out | Preserve and resume the same request ID; do not submit a replacement |
| Scheduler returns `Succeeded` | Retrieve and interpret the audit log separately before claiming business validation success |

## Source Boundaries

- Oracle scheduled-process reference: `https://docs.oracle.com/en/cloud/saas/sales/fauss/audit-party-hierarchy.html`
- Oracle hierarchy-validation reference: `https://docs.oracle.com/en/cloud/saas/customer-data-management/faudm/hierarchy-validation-rules.html`
- Oracle 26B Scheduler submit schema: `https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-ess-rest-scheduler-v1-requests-post.html`
- Scheduler execution owner: `core.fusion-api.ess-job-submitter`
- Effective task catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`
- Reviewed job-definition source: `FUSIONAPPS_11.13.26.04.0_LINUX.X64/fusionapps/crm/components/crmEss/hz/parties/ess/essmeta/oracle/apps/ess/cdm/foundation/parties/Jobs/PartyHierarchyAudit.xml`
- Reviewed parameter source series: `FUSIONAPPS_PT.V2MIBOSCMATDEV_LINUX.X64`
- Reviewed parameter VO: `fusionapps/crm/components/crmEss/hz/parties/auditTrees/publicEssModel/src/oracle/apps/cdm/foundation/parties/auditTrees/publicEssModel/view/ValidatePartyHierarchyParamVO.xml`
- Reviewed procedure sources: `fusionapps/crm/hz/db/plsql/hz_party_tree_audit.pkh` and `fusionapps/crm/hz/db/plsql/hz_party_tree_audit.pkb`
- Target runtime evidence: successful `cptcuqlqy` Scheduled Processes request inspected on 2026-08-18
- Execution-contract provenance: `submit.argument1` through `submit.argument5` follow the working positional Scheduler contract used by parameterized HZ ESS skills and the Audit UI's `argument1` through `argument5` order; two Audit submissions using VO names `ATTRIBUTE1` through `ATTRIBUTE5` completed without stored/displayed parameters, so those VO names are explicitly prohibited for REST submission
- Runtime validation boundary: validate complete LOV values for any non-example selected hierarchy type or status code

## Parent Skill

Use the parent functional-area skill `cx.customer-data-management.trading-community-foundation` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

---
skill_id: "cx.customer-data-management.trading-community-foundation.manage-party-usages"
name: "Manage Party Usages Setup Task Guidance"
description: "Answers task-specific Manage Party Usages setup questions and exports or imports the complete task data as one unfiltered Oracle Fusion FSM package. Give documented UI guidance for individual setup; reserve live execution for the controlled whole-task FSM export/import route, including core.data-loader validation and approval for imports."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Trading Community Foundation"
functional_area_code: "ORA_HZ_CDM_FOUNDATION"
task_code: "HZ_MANAGE_PARTY_USAGES"
task_name: "Manage Party Usages"
parent_skill_id: "cx.customer-data-management.trading-community-foundation"
available_flag: "Y"
export_import_supported_flag: "Y"
csv_export_import_supported_flag: "Y"
dataloader_import_mode: "FSM"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "CX customer data management pillar team"
version: "0.8.1"
inputs:
  - "natural_language_request"
  - "operation"
  - "project_id"
  - "fusion_environment_context"
  - "setup_data_zip_path"
  - "execution_options"
  - "execution_approval"
outputs:
  - "task_guidance"
  - "configuration_export"
  - "export_submission_record"
  - "data_load_execution_result"
  - "immutable_import_preview"
  - "diagnostics"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.setup-export.task-level-export"
  - "core.data-loader"
  - "shared.setup-import.fsm-csv-import"
uses_core:
  - "core.auth.fusion-oauth-authentication"
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
  - "exports"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "configuration_export"
    default_location: "project/{project_id}/exports/customer-data-management/trading-community-foundation/manage-party-usages/"
    versioning_policy: "append-only"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-party-usages/current/"
    versioning_policy: "append-only"
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
  - "After explicit approval, creates and polls one whole-task FSM export process and writes its ZIP or process log to the project workspace."
  - "After explicit approval, imports one immutable whole-task FSM ZIP through the Data Loader-authorized task-local native FSM adapter and can change configuration owned by Manage Party Usages in the target Fusion environment."
  - "The native import adapter always enables source-target revision tolerance because this workflow exists to migrate setup data between Fusion environments."
  - "Writes redacted execution, diagnostic, run, artifact-registry, state, and token-usage records under the selected project workspace."
required_privileges:
  - "Fusion privileges to discover the setup task and run setup task CSV exports."
  - "Fusion privileges to submit, inspect, and retrieve logs for setup task CSV imports."
---

# Manage Party Usages Setup Task Guidance

## Purpose and Boundary

Use this skill to answer documented, task-specific questions about `Manage
Party Usages`, or to export/import its complete FSM setup package. Fix the task
identity to `HZ_MANAGE_PARTY_USAGES` under `Trading Community Foundation`.

For informational requests, provide the advisory guidance in
[Task Information and UI Guidance](#task-information-and-ui-guidance). Do not
open Fusion, inspect a configured environment, invoke an API, or create a
project artifact merely to answer an informational question.

For live execution, support only whole-task FSM export/import. Refuse filtered
exports, templates, direct REST or loader execution, and record-level
maintenance through this skill. Validation is permitted only as mandatory
preflight for an export or import.

## Task Information and UI Guidance

### What this task configures

Party usages define how persons or organizations can be used in application
business flows. The task lets an implementer define the usage itself and the
rules governing when it can be assigned, coexist with another usage, or
transition to another usage.

**Task location**

- Offering: `Customer Data Management`
- Functional area: `Trading Community Foundation`
- Task: `Manage Party Usages`
- FSM task code: `HZ_MANAGE_PARTY_USAGES`

### Create a party usage

1. In **Setup and Maintenance**, open the task location above.
2. Select **Actions > Create**.
3. In **Overview**, enter a unique **Code**, a **Name**, a party-usage
   **Type**, and optionally a description. The code cannot be changed after
   the party usage is created.
4. In **Assignment**, configure the applicable behavior:
   - **Restrict Manual Assignment** when only identified business events may
     create the assignment.
   - **Unconditional Assignment** when bulk import or a manual assignment may
     create it. This option is unavailable for predefined party usages.
   - **Restrict Manual Update** when only identified business events may
     update the assignment.
   - **Relationship Causes Assignment** when creating a party relationship
     should assign the usage.
   Add the relevant descriptions when needed.
5. In **Exclusivity Rules**, define the effective from/to dates for exclusive
   assignment, if applicable.
6. In **Incompatibility Rules**, select usages that cannot coexist with this
   one and, when needed, their effective dates.
7. In **Transition Rules**, select the target party usage and its effective
   dates. A transition can end-date the prior party usage.
8. Select **Save and Close**.

### Edit and design guidance

- An existing party usage code is immutable; update its name, description, and
  rule configuration instead.
- Use incompatibility rules for mutually exclusive lifecycle states, such as a
  prospect usage that must not coexist with a customer usage.
- Use transition rules to make lifecycle changes explicit and time-bound.
- Evaluate changes to assignment controls and rule dates with the business
  owners of the flows that assign party usages before saving them.
- Party Usage Filter Rules are a separate setup task. Use **Manage Party Usage
  Filter Rules** when a group of usages is needed to filter parties in the UI.

### Advisory versus execution requests

| User request | Skill behavior |
| --- | --- |
| “What is Manage Party Usages?” or “How do I create/edit a party usage?” | Answer from this section; no Fusion call or project artifact. |
| “Which rules should I use?” | Explain assignment, exclusivity, incompatibility, and transition rules; identify business-design decisions for the implementer. |
| “Create/edit/delete this party usage in Fusion.” | Provide the UI procedure only; do not execute record-level maintenance. |
| “Export/import Manage Party Usages.” | Use the controlled whole-task FSM workflow below. |

## Supported Operations

1. `export`: export every setup-data object owned by the fixed task as one
   unfiltered, non-template FSM package through
   `shared.setup-export.task-level-export`.
2. `import`: import one complete, unchanged FSM ZIP for the fixed task through
   mandatory `core.data-loader` validation and approval, then execute only
   through this skill's native FSM adapter, which reuses
   `shared.setup-import.fsm-csv-import` process mechanics.

Treat a migration as two operations in sequence. Persist and verify the export
before starting import preflight for that same immutable archive.

## One Consolidated Approval

Use exactly one conversational approval point for each export or import.
Environment resolution, project selection or creation, authentication, browser
sign-in, identity checks, live task lookup, privilege checks, destination-path
checks, package validation, and preview creation are preparation steps. Run all
safe preparation before asking for business-operation approval.

Resolve the environment from durable configuration instead of asking the user
to repeat it. When exactly one active configured Fusion environment is
available, select it automatically and show it in a brief progress update and
the final preview. Ask one short factual question only when no configured
environment can be resolved or multiple active environments remain ambiguous;
name the safe available choices when known.

Authentication is also unapproved preparation. Reuse the prescribed local,
gitignored token cache. If browser sign-in is required, tell the user to
complete sign-in in the opened window, keep waiting on the same callback
process, and continue preparation automatically. Never request `ready`,
`continue`, or a separate approval for login, token refresh, task discovery, or
another read-only check.

After preparation succeeds, persist an immutable approval preview and present
the same bound values as a CommonMark bullet list. For export, show:

- `Environment`: the automatically selected source environment;
- `Operation`: Export;
- `Task name`: Manage Party Usages;
- `Task code`: HZ_MANAGE_PARTY_USAGES;
- `Scope`: Complete task; unfiltered; setup data; not a template;
- `File name`: `<environment>_setup_task_csv_export_hz_manage_party_usages_<ProcessId>.zip`, noting that Fusion assigns `ProcessId` after submission;
- `File path`: the fixed output directory joined to that planned file name;
- `SHA-256`: Computed after download; unavailable before approval;
- `Execution adapter`: shared.setup-export.task-level-export;
- `Execution options`: 300-second wait and 10-second poll;
- `Side effect`: Create one FSM export process, wait for it, and download its ZIP or process log.

For import, show the selected target environment, fixed task name/code, exact
immutable ZIP path and SHA-256, whole-task scope, task-local native FSM adapter,
execution options, and configuration-changing side effect.

Keep the approval fingerprint in the preview and approval envelope for audit
and execution binding, but never show it or require the user to repeat it. Ask
once for the standalone response `approve`. One approval authorizes only the
exact immutable operation displayed: for export, one FSM export submission,
polling, and result retrieval; for import, one native setup-task CSV import
creation, polling, and log retrieval for its returned `ProcessId`. Pass that
approval through downstream boundaries without prompting again. Any change to
the environment, operation, task, scope, path, archive hash when applicable,
adapter, or execution options invalidates approval.

An `approve` received before a ready immutable preview is not authorization for
a POST. Continue or repair preparation automatically, then present the complete
preview and make the operation's single approval request. On a standalone
`approve` after a ready preview, load it, recompute its fingerprint, verify all
bound values and destination state, and immediately execute without repeating
discovery or asking again.

Cross-environment migration is the normal import behavior for this task. The
adapter always sends `SourceTargetDiffOkFlag=Y`; do not expose it as a user
option, approval condition, preview field, or separate override workflow. This
does not relax task identity, archive integrity, target environment, adapter
capability, or explicit approval checks.

## Direct Export Trigger and Resume

Treat `export manage party usages task`, `export fsm task Manage Party Usages`,
and equivalent whole-task wording as a complete export request. Infer
`operation=export`, the fixed task identity, `template_only=false`,
`export_criteria=[]`, `wait_seconds=300`, and `poll_interval=10`.

Resolve or create the implementation project and automatically select the sole
active configured Fusion environment. Run authentication and every safe
read-only preflight check in the same turn. Persist the redacted ready preview
at:

```text
project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/manage-party-usages/current/export-approval-preview.json
```

The preview must have `status=ready_for_approval` and bind its fingerprint to:

- project ID and source environment;
- operation, task name, and task code;
- whole-task, unfiltered, non-template scope;
- output directory and shared export adapter;
- empty export criteria;
- wait and polling options;
- exact live lookup artifact and selected lookup result.

Compute the fingerprint from canonical JSON for those values, excluding
timestamps, status, and the fingerprint field itself. Never persist a token,
secret, authorization header, or token-cache content. Present the final preview
and ask only for `approve`.

On the next standalone `approve`, load the persisted preview, recompute and
verify its fingerprint and every bound value, then immediately run the one
shared export command. Capture the `ProcessId`, poll the same process, retrieve
`FileContent` or `ProcessLog`, verify and register the result, update project
state, append token usage, and report completion. If no valid ready preview
exists, finish or repair preparation and present a new preview; never ask the
user to supply an environment already available in configuration.

## Fixed Task Context

- Pillar: `CX`
- Offering: `Customer Data Management`
- Functional area: `Trading Community Foundation`
- Functional area code: `ORA_HZ_CDM_FOUNDATION`
- Task name: `Manage Party Usages`
- Task code: `HZ_MANAGE_PARTY_USAGES`
- CSV export/import supported: `Y`
- Data Loader import mode: `FSM`

Never accept a task-code, offering, or functional-area override.

## Whole-Task FSM Export

1. Resolve or create `project_id`, then select the sole active environment from
   the configured Fusion properties without asking the user to restate it.
   Ask only if environment configuration is absent or genuinely ambiguous.
   Complete authentication and the read-only preflight defined by
   `ora-resource/ora_reference_lookups.md` and
   `ora-resource/ora_input_validation.md`. Search by the fixed task name with
   no offering or functional-area filters, then require exactly one row whose
   name/code are `Manage Party Usages` / `HZ_MANAGE_PARTY_USAGES` and whose
   availability and CSV-support flags are `Y`. Treat omitted live hierarchy
   fields as unavailable metadata, not as a mismatch; bind the offering and
   functional area from this task's fixed catalog-backed context. A nonblank
   contradictory live hierarchy value remains a blocking mismatch.
2. Fix `template_only=false` and `export_criteria=[]`. Refuse filters,
   business-object subsets, and template/specification requests.
3. Persist `export-approval-preview.json`, show the complete consolidated
   summary, and ask once for the standalone response `approve`. Do not create
   an export process before this approval.
4. After preview and approval verification, route exactly one submission
   through the shared exporter:

   ~~~bash
   python3 -u shared/setup-export/task-level-export/scripts/export_setup_task_csv.py \
     --data \
     --task-code HZ_MANAGE_PARTY_USAGES \
     --offering-name "Customer Data Management" \
     --functional-area-name "Trading Community Foundation" \
     --project-id "{project_id}" \
     --output-dir project/{project_id}/exports/customer-data-management/trading-community-foundation/manage-party-usages/ \
     --token-cache auto \
     --wait-seconds 300 \
     --poll-interval 10
   ~~~

5. Wait on the same process until it exits. Persist its `ProcessId` as soon as
   returned; never infer failure from an initially empty output buffer.
   Command-runner output yield is not process completion. When the runner
   returns a live session or cell identifier, retain it and resume that exact
   session until the exporter exits. Do not start a replacement command, mark
   the export pending, or give the user a final result merely because output
   temporarily stops or the orchestration wrapper yields control.
6. Interpret polling completion only from the exporter process exit:
   - exit `0`: retrieve and verify `FileContent`;
   - exit `3`: the declared 300-second polling window expired; persist the
     `ProcessId`, last status, and elapsed wait, then stop without resubmission;
   - any other nonzero exit: classify and persist the failure using
     `ora-resource/ora_error_handling.md`.
7. On success, verify the ZIP, calculate SHA-256, register it, and update project
   state. On timeout or uncertain response, preserve the same identifier and do
   not submit a replacement automatically.

## Whole-Task FSM Import Through the Data Loader-Authorized FSM Adapter

1. Require the project, exact target Fusion environment, and one explicit ZIP.
   Reject loose CSV files, multiple archives, directory scans, and repackaging.
2. Require a valid ZIP with exactly one member whose basename is
   `ASM_SETUP_CSV_METADATA.xml`; require its single `ObjectShortName` to equal
   `HZ_MANAGE_PARTY_USAGES`. Preserve the bytes and calculate SHA-256.
3. Enter the mandatory `core.data-loader` workflow for source review, Task Hook
   validation, immutable preview creation, and explicit approval. Data Loader
   owns adapter selection and approved-payload release; it does not require its
   generic UCM uploader to be the execution adapter. Do not invoke an import
   endpoint during preflight.
4. During adapter selection, inspect the target pod's live
   `dataLoaderDataSets/describe` action metadata. Never add `runID`,
   `sourceType`, or another property to an ADF action unless that exact action
   advertises the property. For this setup-task FSM package, select
   `cx.customer-data-management.trading-community-foundation.manage-party-usages.native-fsm-import`
   and its child-process create operation on
   `/fscmRestApi/resources/11.13.18.05/setupTaskCSVImports/{TaskCode}/child/SetupTaskCSVImportProcess`
   with a direct child payload containing `TaskCode`, `FileContent`, and
   `SourceTargetDiffOkFlag`. Require live metadata to expose those child
   attributes. Do not select
   `core/data-loader/scripts/upload_and_initiate.py`; the generic
   `initiateDataLoad` action is not the native setup-task CSV import contract.
5. Require the immutable preview and Task Hook approval envelope to retain
   `executionRoute=data-loader`,
   `executionAdapter=cx.customer-data-management.trading-community-foundation.manage-party-usages.native-fsm-import`,
   `packageType=FSM`, `targetEnvironment`,
   the exact target environment, fixed task name/code, absolute ZIP path,
   SHA-256, `wholeTask=true`, `waitSeconds=180`, and `pollInterval=15`. Any
   adapter, target, archive, task-context, or option change invalidates approval.
6. After approval, record Task Hook approval, verify the archive hash again,
   persist the approved envelope, and release that exact payload to the selected
   shared adapter without another prompt. Data Loader releases the approved
   payload only after all bindings still match.
7. Invoke the selected task-local adapter exactly once. Cross-environment
   revision tolerance is fixed inside the adapter and requires no command-line
   switch or separate approval field:

   ~~~bash
   python3 -u pillars/cx/customer-data-management/trading-community-foundation/manage-party-usages/scripts/import_manage_party_usages.py \
     --zip-file "{setup_data_zip_path}" \
     --task-validation-envelope "{task_validation_envelope_path}" \
     --token-cache auto \
     --wait-seconds 180 \
     --poll-interval 15 \
     --output-dir project/{project_id}/artifacts/shared/setup-import/task-level-import/manage-party-usages/
   ~~~

   The adapter validates the approved Task Hook envelope and exact archive
   bytes, creates the fixed native child-process payload, persists a redacted
   copy of the create response, captures the documented root-level `ProcessId`,
   and delegates polling and `ProcessLog` retrieval to
   `shared.setup-import.fsm-csv-import`. It may also accept the legacy nested
   response shape for compatibility. Do not call it before Data Loader releases
   the approved payload.
8. Never use `uploadDataLoaderFile`,
   `dataLoaderDataSets/action/initiateDataLoad`, or `sourceType=FSM` for this
   setup-task package. Those are generic Data Loader actions and fields, not the
   native setup-task CSV import contract.
9. If Fusion rejects the request, persist the HTTP diagnostic and stop. Do not
   change the payload or retry under the consumed approval. Correct the package,
   target, privileges, or live API contract as indicated by the diagnostic,
   then build a new immutable preview before any later submission.
10. Persist the complete Data Loader-authorized adapter result and redacted
    diagnostics. If a successful create response omits a usable root or legacy
    nested `ProcessId`, preserve the redacted response and stop without another
    POST. On polling timeout, retain the same `ProcessId` and resume only that
    process after a later status request.

## Error and Retry Contract

Use `ora-resource/ora_error_handling.md`. Refresh a cache-managed token once
after a read-only 401/403 when the selected workflow permits it. Never retry a
live export or native setup-task import POST automatically. Treat HTTP 400 /
`27503` from `initiateDataLoad` as evidence that the wrong adapter was selected,
not as permission to remove fields and retry. Never expose tokens, secrets,
authorization headers, token-cache contents, full Base64 payloads, or sensitive
customer data.

## Result Contract

For export, report the environment, task name/code, `ProcessId`, status, ZIP or
log path, enclosure type, and SHA-256. For import, return the Data
Loader-authorized native adapter result plus target, fixed task, immutable ZIP
path/hash, `ProcessId`, status, and available process log.
Record each durable run and token usage.

## Golden Scenarios

| Request | Expected route |
|---|---|
| Export all Manage Party Usages data | Automatically select the sole configured environment, finish authentication and read-only preflight, persist one ready preview, ask once for `approve`, then run the unfiltered FSM task export and persist its ZIP, hash, and process result |
| Configured environment is unambiguous | Select it automatically and include it in progress and preview; do not ask the user for an environment |
| Environment configuration is missing or ambiguous | Ask one short factual question with safe available choices; do not create an approval preview until resolved |
| Early `approve` before a ready preview | Finish or repair preparation, present the complete immutable preview, and ask once for `approve`; do not treat the early response as POST authorization |
| Ask for export approval | Show one labeled CommonMark list with environment, operation, task name/code, scope, planned filename/path, post-download SHA status, adapter, options, and side effect; hide the approval fingerprint; ask only for `approve` |
| Ask for import approval | Show a bulleted list with action, task name/code, target environment, whole-task ZIP scope, package path/hash, and configuration-change effect; hide implementation details and the approval fingerprint; ask `Approve this import?` |
| User replies `approve` to the displayed immutable preview | Verify the persisted preview and immediately execute that exact operation without requiring the fingerprint or another approval |
| Command runner yields while the export is polling | Retain and resume the same live command session; do not report pending until the exporter exits or reaches its declared timeout |
| Import that complete exported ZIP | Run Data Loader and Task Hook preflight, select the task-local native FSM adapter, and submit one cross-environment-tolerant `setupTaskCSVImports` process for the approved immutable ZIP |
| Fusion rejects the approved import | Stop without retry, persist the diagnostic, correct the reported package, target, privilege, or contract issue, and require a new immutable preview before any later submission |
| Generic `initiateDataLoad` does not advertise FSM parameters | Select the approved shared `setupTaskCSVImports` adapter; do not upload or submit the FSM ZIP through the generic action |
| Export one party usage | Refuse partial scope without a Fusion call |
| Ask how to create or edit a party usage | Provide the documented UI procedure; do not call Fusion or perform record-level maintenance |
| Create or edit a party usage in Fusion | Provide the UI procedure only; do not perform the record-level change |

## Sources

- `knowledge/setup-task-catalog/effective/setupTasksAll.json`
- `https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-do-i-manage-party-usages.html`
- `https://docs.oracle.com/en/cloud/saas/customer-data-management/faicd/toc.htm`
- `shared/setup-export/task-level-export/SKILL.md`
- `core/data-loader/SKILL.md`
- `shared/setup-import/fsm-csv-import/SKILL.md`
- `https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/op-fscmrestapi-resources-11.13.18.05-setuptaskcsvimports-post.html`
- `ora-resource/ora_reference_lookups.md`
- `ora-resource/ora_input_validation.md`
- `ora-resource/ora_error_handling.md`

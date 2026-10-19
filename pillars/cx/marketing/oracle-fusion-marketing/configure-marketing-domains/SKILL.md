---
skill_id: "cx.marketing.oracle-fusion-marketing.configure-marketing-domains"
name: "Configure Marketing Domains Setup Task Guidance"
description: "Provides task-specific setup guidance for Configure Marketing Domains under the Oracle Fusion Marketing functional area."
layer: "pillar"
pillar: "CX"
offering: "Marketing"
functional_area: "Oracle Fusion Marketing"
functional_area_code: "ORA_FMK_FUSION_MARKETING"
task_code: "ORA_FMK_CONFIGURE_EMAIL_DOMAINS"
task_name: "Configure Marketing Domains"
parent_skill_id: "cx.marketing.oracle-fusion-marketing"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObject: "domains"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "verification"
execution_mode: "hybrid"
owner_team: "CX marketing pillar team"
version: "0.1.1"
inputs:
  - "implementation_objective"
  - "project_context"
  - "setup_task_scope"
  - "setup_data_artifacts"
outputs:
  - "setup_task_plan"
  - "setup_data_routing"
  - "validation_checkpoints"
  - "continuation_checkpoint"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "core.data-loader"
uses_core:
  - "core.fusion-api.rest-api-client"
  - "core.auth.fusion-oauth-authentication"
  - "core.runbook"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/marketing/oracle-fusion-marketing/configure-marketing-domains/continuation/"
    versioning_policy: "append-only"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/marketing/oracle-fusion-marketing/configure-marketing-domains/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/marketing/oracle-fusion-marketing/configure-marketing-domains/current/"
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
  - "Reads Marketing Domains through BOSS GET operations."
  - "Delegates every Marketing Domain write to core.data-loader using the registered domains business object."
required_privileges:
  - "Authorized BOSS read access for Marketing Domains."
  - "Fusion privileges to upload and initiate an approved Data Loader operation for the domains business object."
---

# Configure Marketing Domains Setup Task Guidance

## Purpose

Provides source-backed, approval-gated domain-configuration guidance for `Configure Marketing Domains` under `Oracle Fusion Marketing`.

## Setup Task Skill Contract

- task_code: `ORA_FMK_CONFIGURE_EMAIL_DOMAINS`
- task_name: `Configure Marketing Domains`
- parent_skill_id: `cx.marketing.oracle-fusion-marketing`
- pillar: `CX`
- offering: `Marketing`
- functional_area: `Oracle Fusion Marketing`
- functional_area_code: `ORA_FMK_FUSION_MARKETING`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- dataloader_import_mode: `REST`
- businessObject: `domains`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business object.

1. Confirm that `domains` is the exact registered Data Loader business object.
2. Generate the default editable XLSX sample through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "domains" \
     --operation update \
     --token-cache "<absolute-repository-root>/.fusionaim_token.json" \
     --output-dir "<approved-private-working-directory>"
   ```

3. Keep the generated workbooks together:
   - editable sample
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbook as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this skill to list, select, and propose approved updates to Marketing email and microsite domains for `Configure Marketing Domains` under `Oracle Fusion Marketing`.

## Guided Continuation

Read [guided-continuation.md](references/guided-continuation.md) before the
first command and on every resume. It owns this Marketing caller's sequencing,
redacted checkpoints, cache selection, and running-process handling; it does
not replace the core Run Book, OAuth, or Data Loader implementations.

- After supported changes are supplied, continue through source preparation,
  core preflight, and Task Hook validation to the immutable approval preview.
  Do not ask the user to say "prepare preview" to advance an authorized update.
- Require an active project Run Book before Data Loader preparation. When
  initial creation succeeds, deliver its complete sanitized dashboard unchanged
  **in commentary**, then continue in the same turn. Dashboard delivery is an
  ordering requirement, not a user gate or a reason to end the update request.
  If creation was deferred or its outcome is failed/unknown, follow core's
  blocker/reconciliation path; never create another Run Book merely to resume.
- Treat "fetch updated record" and "check again" as read-only inspection when
  that is what the user asks. Preserve the pending update, answer the check,
  and continue already-authorized preparation unless explicitly paused or
  cancelled. If nothing was submitted, say **not submitted**, not "not yet
  propagated". A read-only follow-up or "resume" is never upload approval.
- Keep supplied selection and changes in transient context. Persist only the
  redacted checkpoint defined in the reference through the existing project
  managers, and reconstruct the next action from verified evidence on resume.
  Ask only for inputs no longer safely available; never store customer values
  in project checkpoints or infer them from field names.
- Pass the **absolute repository** `.fusionaim_token.json` path explicitly to
  every standard-scope Run Book and Data Loader invocation, including sample
  generation, validation, preflight, and approved submission. Use the separate
  absolute `.fusionaim_boss_token.json` path for BOSS reads. Let core validate
  caches; do not force login as a preflight or inspect token-cache contents.
- Retain the complete command result, including `session_id` and `exit_code`.
  Poll a running command through its original tool session; empty stdout is
  not completion. Serialize authentication-capable commands and do not launch
  another login while the first command is waiting for its callback.
- At a genuine pause, show what completed, the exact next action, and what
  input is needed. Use the unchanged core approval report for the approval
  gate. Respect an explicit stop/pause, and keep upload and initiation solely
  behind core's approval and integrity checks.

## Setup Task Metadata

- Task name: `Configure Marketing Domains`
- Task code: `ORA_FMK_CONFIGURE_EMAIL_DOMAINS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- Data Loader import mode: `REST`
- Business Object: `domains`

## Custom Execution Workflow

This task uses the registered Data Loader business object
`domains` in `REST` mode for every supported domain write. The registered
object supports `MERGE` and `DELETE`; use `MERGE` only to update one selected
existing domain and do not offer a standalone create operation.
`core.data-loader` is the sole mutation owner: it validates live metadata and
the prepared source, creates the immutable upload artifact and approval
preview, obtains the required approval, uploads the approved artifact, and
initiates the load. Do not issue a BOSS `PATCH`, `POST`, `PUT`, or `DELETE`
for this task.

The BOSS Domains API remains read-only in this skill, to list and resolve the
current domain record before source preparation and verify approved updates. Keep selected
record IDs and other server-only values transient; use them only when the live
`domains` Data Loader template requires them as update identity.

1. Route BOSS calls through `core.fusion-api.rest-api-client` and `core/fusion-api/rest-api-client/scripts/boss-rest_client.py`. Use `boss_scope` from `core/auth/fusionEnv.properties` and pass `--token-cache <absolute-repository-root>/.fusionaim_boss_token.json` explicitly; never construct or disclose an Authorization header. Apply Guided Continuation before any authentication-capable call.
2. Read the current domain list with `GET /api/boss/data/objects/ora/cxMarketingCommonShared/configuration/v1/domains` after target, identity, privilege, and input preflight. Start with `$limit=100` and `$offset=0`; follow every page, increasing `$offset` by the returned-page size until no records remain, before presenting domains by `primaryDomain`, active DNS status, enabled email/microsite domain types, and their available preference values. When listing to obtain a new selection, ask exactly: “Which primaryDomain would you like to inspect or update? Please provide one value exactly as shown.” In that selection phase, do not request changed fields, construct a preview, or perform another BOSS operation until the user supplies an exact listed value. Re-reading the list for an already selected domain, a status check, or post-load verification preserves the selection and does not repeat this gate.
3. Require the user to select exactly one `primaryDomain` value from that complete response. Reject an unknown or ambiguous value and show the available values again.
4. Re-run the paginated Domains GET and select exactly one record whose `primaryDomain` equals the selected value. Before requesting changes, render the record unredacted as a `Section | Field | Current Value` table: `Domain` contains Primary Domain and DNS Status; `Domain Settings` contains every enabled preference setting; and `Default Headers` contains Sender Name, Sender Email Address, Reply to Name, Reply to Email Address, and Bounceback mail Address. Do not display record IDs, self links, ETags, or If-Match values. If no or many matches are found, stop without preparing a write source.
5. For the displayed selected record, accept only enabled `emailDomainPreference` and `micrositeDomainPreference` fields, plus `senderName`, `senderEmail`, `replyToName`, `replyToEmail`, and `bounceBackEmail`. Reject unsupported or blank fields. For either preference, send lowercase `default` for “Set this domain as default domain (Available for use)”, `alternate` for “Set this domain as alternate domain (Available for use but not default)”, and `null` for “Domain unavailable for use.” Only `senderEmail` and `bounceBackEmail` may modify the local part and must preserve the selected domain suffix; `replyToEmail` accepts a valid external email address.
   When awaiting changes, after displaying the selected record, ask exactly: “Which fields would you like to update? Supported fields: emailDomainPreference and micrositeDomainPreference; use lowercase default for ‘Set this domain as default domain (Available for use)’, alternate for ‘Set this domain as alternate domain (Available for use but not default)’, or null for ‘Domain unavailable for use’. You can also update senderName, senderEmail (local part only), replyToName, replyToEmail (external address allowed), and bounceBackEmail (local part only). Values cannot be blank or unsupported. Provide one or more changes as key-value pairs. I’ll show the proposed field changes and immutable Data Loader preview for approval before initiating the load.” If changes are already supplied, retain them and continue validation; do not repeat this prompt during a status read, recovery, or post-load verification.
6. Confirm `domains` is the exact registered Data Loader business object through `core.data-loader` before source preparation. For a new editable source, generate the default XLSX sample with `core/data-loader/scripts/generate_sample_dat.py domains --operation update --token-cache <absolute-repository-root>/.fusionaim_token.json`; use its `domains` root worksheet and live template headers. Before validation, run `scripts/remove_domains_status_code.py <source.xlsx> <prepared.xlsx> --changed-field <each requested field>` for every generated Domains update source. It emits a sparse workbook containing only `domains_id`, `$operation`, and the explicitly changed fields. It sets the mandatory `$operation` field to `MERGE` for an update, including when the input operation cell is missing. It excludes `$statusCode`, all unchanged fields, and all blank fields by rejecting missing or blank identity and requested values in populated records; wholly empty rows are ignored and a source with no records is rejected. FMK `Domain` defines no `statusCode` attribute, and BOSS `status` values such as `ok` are read-only and must never be mapped to framework metadata. Use a fresh destination: the helper rejects existing destinations and identical source/destination paths instead of replacing an artifact. For an update or deletion source supplied by the caller, require the source to resolve case-sensitively to `domains` through the registered-object check. Preserve the selected domain's required identity only in the prepared source when the live template requires it. Do not infer source headers, required fields, `$operation`, `RestAction`, or other action values from the BOSS API.
7. Delegate the source to `core.data-loader` with task context `ORA_FMK_CONFIGURE_EMAIL_DOMAINS` and business object `domains`. Core must complete registered-object lookup, template retrieval, source/schema validation and immutable archive preparation before Task Hook validation. The task graph ends at `DOMAINS.VALIDATION_READY` after its input, lookup and design checks pass, without asking for or requiring user approval. Core then builds the immutable approval preview, obtains explicit approval, verifies its retained artifact and envelopes, uploads to UCM, and calls `initiateDataLoad`. The validation-ready terminal does not authorize a write. Do not ask for a second task-local approval or construct a BOSS JSON payload. On decline, do not upload; retain the selection and offer revision or cancellation. On ambiguity, let core clarify approval of the same exact preview. Any changed artifact requires new preparation, validation and approval.
8. After core accepts the load, wait 30 seconds, then re-run the paginated read-only BOSS Domains GET and render the complete selected-domain record. Compare every approved changed field with the read-back value. If any value differs, wait one further 30-second interval and read back the complete record again. If the mismatch remains, prepare a fresh sparse source from the latest record and request fresh explicit approval for one retry only; never automatically upload or initiate a retry. After an approved retry, wait 30 seconds and render the complete selected-domain record whether or not the expected values appear.

The task-local `ora-resource` files define preapproval validation. Keep them
aligned with `pillars/cx/marketing/noship/oracle-fusion-marketing-build-skill-metadata.yaml`.
Load `ora_error_handling.md` before preview or execution; its post-validation
approval and refusal policies apply through the core Data Loader lifecycle.

## Marketing Final Response

This task owns the final response after core.data-loader returns an accepted
initiation. Core's return ends its submission operation, not this Marketing
task: complete the bounded 30-second read-back workflow in step 8 first.

For this task only, the Marketing final response overrides core.data-loader's final-answer-only and terminal-response wording after accepted initiation.
All core validation, immutable-artifact integrity, approval, upload, initiation, and mutation retry controls remain unchanged.

Preserve the complete Data Loader initiation report verbatim in the final
response, then add the Marketing verification outcome and record view below.
Commentary may announce progress but must not be the only place the updated
record or verification result appears. Do not end with only Data Load In Progress.

Show the complete selected-domain record as a Section / Field / Current Value table, including every enabled preference and all five Default Headers fields.
If no fresh unambiguous record is available, report verification unavailable; never present a stale record as current.

| Outcome | Final Response |
|---|---|
| Matched | State "Updated values verified" only when every approved changed field matches the fresh read-back; include the complete record in the final response. This confirms field values, not asynchronous Data Loader job completion. |
| Mismatch | State "Update not yet verified"; include the latest complete record and requested-versus-observed values after the bounded read-back attempts. Do not claim success or retry automatically; at most one mutation retry requires a new immutable preview and fresh approval. |
| Unavailable | State "Verification unavailable"; retain the accepted initiation report and explain the read failure or ambiguous selection. Do not present a stale record as current or resend the load; offer a read-only verification retry. |

Keep the record ID, self link, ETag, and If-Match out of the record view.
The unchanged core initiation report retains its own permitted request/content
identifiers. Do not add another mutation approval gate or automatically begin
another update after displaying the verified result.

## Execution Boundaries

- Do not infer BOSS or CDP Unity write endpoints, authentication details beyond the configured BOSS read route, request fields, query parameters beyond `$limit` and `$offset`, or rollback behavior.
- Do not infer `domains` source headers, update identity, required fields, `$operation`, or `RestAction`; obtain them from the registered-object lookup and current Data Loader template.
- Every mutation must pass through `core.data-loader`'s immutable preview and approval lifecycle. Do not create a parallel task-local approval gate.
- Do not retry an upload or load initiation. Follow `core.data-loader` failure handling and require a fresh source review and approval when it reports an execution failure.

## Failure Handling and Diagnostics

- Classify failures as `input_validation`, `catalog_or_metadata_mismatch`, `auth_expired_or_invalid`, `authorization_or_privilege`, `transport_or_environment`, `fusion_api_error`, `process_timeout`, `process_failed`, `artifact_persistence`, `data_loader_validation`, `ucm_upload`, `data_load_initiation`, or `approval_blocker`. Stop before side effects on every failed preflight or ambiguous domain selection. A yielded running process is not a failure; use the continuation reference before diagnosing or retrying it.
- Do not automatically retry a Data Loader upload or initiation. A source, metadata, or validation change requires a fresh immutable artifact and approval through `core.data-loader`.
- When project output is in scope, persist only redacted diagnostics with status, stage, failure class, message, recommended action, environment identity, task identity, redacted endpoint path, completed checks, and verified side effects.
- Never print or persist credentials, tokens, authorization headers, token caches, record IDs, ETags, opaque self links, or If-Match values. For the selected-domain display and explicit user-requested verification only, render the approved response fields unredacted in the `Section | Field | Current Value` table. Do not persist those displayed values in project artifacts.



## Inputs

- `implementation_objective`
- `project_context`
- `setup_task_scope`
- `setup_data_artifacts`

## Outputs

- `setup_task_plan`
- `setup_data_routing`
- `validation_checkpoints`
- `continuation_checkpoint`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the parent functional-area skill `cx.marketing.oracle-fusion-marketing` for functional-area sequencing and scope decisions. Track token usage for any generated project artifact or skill-run record using the manifest policy.

For repository regeneration, maintain the Marketing `regeneration` contract in
`pillars/cx/marketing/noship/oracle-fusion-marketing-build-skill-metadata.yaml`
and its declared authored source bundle together. Run
`python3 -B pillars/cx/marketing/noship/scripts/regenerate_domains.py --check`
to compare the reconstructed package with these shipped files. The shared
scaffold generator alone does not reproduce this task's custom contract.

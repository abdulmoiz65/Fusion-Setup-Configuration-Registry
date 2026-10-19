---
skill_id: "cx.customer-data-management.enterprise-profile.run-maintain-geography-name-referencing"
name: "Run Maintain Geography Name Referencing"
description: "Converts plain-text Geography Name Referencing job parameters into the fixed eight-position Oracle Fusion ESS contract, previews the request, and submits or resumes Validate Geographies of Addresses Against Master Geographies under CX Customer Data Management Enterprise Profile."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Enterprise Profile"
functional_area_code: "ORA_ASK_ENTERPRISE_PROFILE"
setup_task_code: "HZ_RUN_MAINTAIN_GEOGRAPHY_NAME_REFERENCING"
setup_task_name: "Run Maintain Geography Name Referencing"
task_code: "HZ_RUN_MAINTAIN_GEOGRAPHY_NAME_REFERENCING"
task_name: "Run Maintain Geography Name Referencing"
parent_skill_id: "cx.customer-data-management.enterprise-profile"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "verification"
execution_mode: "hybrid"
owner_team: "CX customer data management pillar team"
version: "0.3.3"
inputs:
  - "job_parameters_text"
  - "fusion_environment_context"
  - "project_id"
  - "execution_intent"
  - "execution_options"
  - "request_id"
outputs:
  - "normalized_job_parameters"
  - "ess_request_payload"
  - "execution_preview"
  - "ess_submission_checkpoint"
  - "ess_execution_result"
  - "diagnostics"
  - "skill_run_record"
  - "token_usage_record"
uses_core:
  - "core.fusion-api.ess-job-submitter"
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
  - "setup_task_sequence"
  - "validation_results"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/enterprise-profile/run-maintain-geography-name-referencing/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/enterprise-profile/run-maintain-geography-name-referencing/current/"
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
  - "Connects to the configured Oracle Fusion ESS Scheduler REST API."
  - "Submits Validate Geographies of Addresses Against Master Geographies after explicit execution authorization; an unambiguous run or submit request can provide that authorization without a second confirmation."
  - "Creates or refreshes Geography Name Referencing mappings for the selected address records."
  - "May refresh the local gitignored OAuth token cache through the invoked ESS core skill."
required_privileges:
  - "Application Implementation Consultant role or equivalent access"
  - "Run Trading Community Geography Name Referencing Maintenance privilege"
---

# Run Maintain Geography Name Referencing

## Purpose

Accept the parameters for `Run Maintain Geography Name Referencing` in plain
text, convert them to the fixed Oracle Fusion ESS positional contract, validate
and preview the request, and submit or resume the scheduled process without
duplicating authentication, submission, or polling logic.

The task runs `Validate Geographies of Addresses Against Master Geographies`.
It validates address elements against master geography data and creates or
refreshes Geography Name Referencing mappings used by downstream processes.

## Setup Task Contract

- Task code: `HZ_RUN_MAINTAIN_GEOGRAPHY_NAME_REFERENCING`
- Application: `CrmEss`
- Job definition: `JobDefinition://oracle/apps/ess/cdm/foundation/geographies/HZ-HZGNR`
- Submit endpoint: `POST /ess/rest/scheduler/v1/requests`
- Track endpoint: `GET /ess/rest/scheduler/v1/requests/{requestId}`
- CSV export/import: not supported by the effective setup-task catalog
- Compatibility: self-incompatible and incompatible with Group Territory Geographies

Do not infer the ESS application or job definition from the setup task code.
Use the fixed values above.

## Inputs

- `job_parameters_text`: plain-text values for the job, for example, `Run new
  HZ locations for India using geography validation`.
- `fusion_environment_context`: target Fusion environment; resolve it only when
  exactly one configured environment is active.
- `project_id`: required for live submission so the request checkpoint survives
  an interrupted command session.
- `execution_intent`: `preview` or `execute`; a direct imperative such as `run`
  or `submit` authorizes one live submission once the parameters are unambiguous
  and no approval blocker remains. The intent remains active while missing
  parameters are collected.
- `execution_options`: optional `wait_seconds` and `poll_interval`.
- `request_id`: optional positive ESS request ID used only to resume tracking.

## Outputs

- `normalized_job_parameters`
- `ess_request_payload`
- `execution_preview`
- `ess_submission_checkpoint`
- `ess_execution_result`
- `diagnostics`
- `skill_run_record`
- `token_usage_record`

## Plain-Text Normalization

Interpret the user's text into this canonical model before running the bundled
builder:

| Canonical field | ESS position | Requirement | Accepted values |
|---|---|---|---|
| `location_table_name` | `submit.argument1` | Required | `HZ_LOCATIONS`, `PER_ADDRESSES_F` |
| `run_type` | `submit.argument2` | Required | `ALL`, `ERROR`, `NEW` |
| `usage_code` | `submit.argument3` | Optional | `GEOGRAPHY`, `TAX` |
| `country_code` | `submit.argument4` | Optional | ISO two-letter country code |
| `from_location_id` | `submit.argument5` | Optional | Positive integer |
| `to_location_id` | `submit.argument6` | Optional | Positive integer |
| `start_date` | `submit.argument7` | Optional | `YYYY/MM/DD` |
| `end_date` | `submit.argument8` | Optional | `YYYY/MM/DD` |

Apply these interpretation rules:

1. Map `HZ locations`, `customer locations`, or `trading community locations`
   to `HZ_LOCATIONS` only when the phrase is unambiguous.
2. Map `person addresses` or `employee addresses` to `PER_ADDRESSES_F`.
3. Map `all` to `ALL`, `new` or `not previously processed` to `NEW`, and
   `errors`, `failed`, or `revalidate errors` to `ERROR`.
4. Map explicit address or geography validation to `GEOGRAPHY` and explicit tax
   validation to `TAX`. Leave `usage_code` unset when the user does not specify
   it; do not silently default an optional argument.
5. Resolve an unambiguous country name to its uppercase ISO two-letter code.
   Ask for clarification instead of guessing an ambiguous country.
6. Preserve every unspecified optional argument as an empty ESS position.

### Parameter Intake

Collect parameters in plain business language. On a bare invocation, or when
both required values are missing, present this single checklist:

```text
Please provide the job settings. The first two are required. Country is optional but usually provided.

- Location table name: Customer locations (HZ_LOCATIONS) or Employee addresses (PER_ADDRESSES_F)
- Run mode: All records (ALL), New records (NEW), or Errors only (ERROR)
- Country (optional, usually provided): Country name or ISO two-letter country code
- Other optional settings: Validation use (Geography or Tax), from location ID, to location ID, and date range (YYYY/MM/DD).
```

Apply these intake rules:

1. Do not ask for a field already supplied unambiguously in the current request
   or earlier messages in the same intake.
2. When only one required field is missing, ask only for that field:
   - Source: `Which location table should the job process: Customer locations
     (HZ_LOCATIONS) or Employee addresses (PER_ADDRESSES_F)?`
   - Scope: `Which run mode should the job use: All records (ALL), New records
     (NEW), or Errors only (ERROR)?`
3. Optional fields do not block execution. If the user omits them, preserve
   them as `Not specified`; do not ask a second round of optional questions
   after the required values are known.
4. If a partially specified first request would benefit from the remaining
   optional choices, show one consolidated optional-settings prompt alongside
   the missing required field rather than repeating the full checklist.
5. Treat phrases such as `no filters`, `leave the rest blank`, or `use no other
   restrictions` as an explicit instruction to leave all remaining optional
   fields unset.
6. Keep an explicit `run`, `submit`, or equivalent execution instruction active
   while collecting missing values. A concise answer to the checklist completes
   the original request; do not make the user say `run` again.

Do not lead with table names, ESS argument names, task codes, or internal skill
names. Accept technical values when the user supplies them, but translate them
to business labels in the next response. Stop before submission when any value
is ambiguous.

## Deterministic Payload Builder

Write the canonical object to a temporary or project-local JSON file and run
from the repository root:

```bash
python3 pillars/cx/customer-data-management/enterprise-profile/run-maintain-geography-name-referencing/scripts/build_gnr_request.py \
  --input <canonical-parameters.json> \
  --description "FDOS:maintain-geography-name-referencing:<project_id>:<run_id>" \
  --payload-output <ess-request.json> \
  --report-output <request-preview.json>
```

The builder validates values and returns a structured document containing the
normalized parameters, warnings, approval requirement, and exact ESS payload.
`--payload-output` writes only the executable Scheduler payload accepted by the
core ESS submitter. `--report-output` writes the complete preview and validation
document.
All eight positional parameters use `paramType: STRING`. Optional null positions
remain present as parameter objects without a `value` property. Do not send a
JSON null, an empty string, or `#NULL` for those positions.

The builder fails closed when an output already exists. Create a new run path,
or use `--force` only after explicit overwrite approval. It never allows an
output to replace its input file or allows the payload and report to share one
path.

Use the generated payload file with `core.fusion-api.ess-job-submitter`. Do not
reimplement OAuth or HTTP transport in this task skill.

## Validation Rules

1. Require `location_table_name` and `run_type` before any side effect.
2. Reject values outside the documented enumerations.
3. Require `country_code` to contain exactly two ASCII letters and uppercase it.
4. Require location IDs to be positive integers.
5. When both location IDs exist, require `from_location_id < to_location_id`.
6. Require dates in `YYYY/MM/DD` format.
7. When both dates exist, require `start_date < end_date`.
8. Reject `PER_ADDRESSES_F` with `GEOGRAPHY`; that table is supported for tax
   validation rather than address validation.
9. Treat `ALL` without a country code as a broad-run approval blocker unless
   the user explicitly requested all countries or no country filter. Show the
   environment and complete normalized scope; require confirmation only when
   the broad country scope was not explicit.
10. Warn that `ALL` may take considerable time even when a country is supplied.
11. Do not modify `HZ_GNR_NUM_OF_WORKERS`, `HZ_GNR_COMMIT_SIZE`, or
    `HZ_POST_IMPORT_GNR_INVOKE`; mention them only as separate tuning decisions.

## Preview and Authorization

Always show one end-user preview before submission. Use the scheduled-process
name as the heading and show:

- target environment
- address source
- record scope
- validation use
- country
- starting and ending location IDs
- start and end dates
- broad-run or long-running warnings
- expected status-tracking window

Show every parameter, including optional parameters that were not supplied.
Render values with business labels first, for example `Customer locations
(HZ_LOCATIONS)` and `New records only (NEW)`. Render an unset optional value as
`Not specified`; where helpful, explain its business effect without inventing a
default.

Render the preview as a Markdown bulleted list. Do not display the settings as
an unbulleted block of label-value lines, a paragraph, or a table. Use this
compact layout when confirmation is still required:

```markdown
Validate Geographies of Addresses Against Master Geographies

- Environment: <environment name or host>
- Address source: <business label> (<canonical value>)
- Records to process: <business label> (<canonical value>)
- Validation use: <business label and canonical value, or Not specified>
- Country: <country and code, or Not specified>
- Location IDs: <start> to <end>, or Not specified
- Date range: <start> to <end>, or Not specified
- Status tracking: <wait window and poll interval in plain language>
- Warning: <broad-run or long-running warning; omit this bullet when none applies>

Run this job with these settings? Reply Yes to confirm, or tell me what to change.
```

When the request already carries explicit execution authorization and all
required values are unambiguous, use the same bulleted layout but replace the
final question with this status line and proceed directly to the two-phase live
execution:

```text
Proceeding with the explicitly requested run using these settings.
```

Keep application names, job-definition paths, ESS argument positions, core
skill IDs, repository policy, checkpoint paths, and other implementation
details out of the confirmation message. Persist the full technical preview in
the project artifacts and show those details only when the user asks or when
they are necessary to diagnose a failure.

Ask exactly one plain-language confirmation question only when explicit
execution authorization is absent or an approval blocker remains:

`Run this job with these settings? Reply Yes to confirm, or tell me what to
change.`

A direct, unambiguous request to `run`, `submit`, or `proceed` authorizes one
submission using the resolved parameters and replaces a separate preview
confirmation. This applies whether the parameters are complete in the first
message or are completed through the immediately following intake response.
Do not ask again for values already defined in the first message. The
authorization also covers the skill's declared internal execution services.
Do not ask the user to name, approve, or authorize core skills or dependencies
separately.

Do not infer execution authorization from informational, conditional, or
preview-only language such as `show me`, `what would happen`, `preview`, or `if
we ran this`. In those cases, show the preview without submitting. If the user
then gives an unambiguous affirmative response such as `yes`, `confirm`, `run`,
or `proceed`, treat it as approval for one submission using the displayed
parameters.

For `ALL` without `country_code`, make the broad scope prominent. A direct
request that explicitly says to process all countries or to run without a
country filter authorizes that broad run without a second confirmation. If the
country omission was implicit, treat it as an approval blocker and require the
same plain-language confirmation after the warning; do not add a second,
technical approval prompt.

## Live Execution

Use the two-phase submission pattern:

1. Require `project_id` and persist the normalized preview, exact payload,
   unique correlation description, target environment, and UTC submission
   window under the declared current artifact folder.
2. Invoke `core.fusion-api.ess-job-submitter` with `--payload-file` pointing to
   the builder's `--payload-output` file,
   `--submit-only`, `--retries 0`, and `--output` pointing to
   `ess-submission-checkpoint.json`.
3. Read the checkpoint and require one positive
   `execution_result.requestId`. Persist and report it before polling.
4. Invoke the core skill again with `--request-id <requestId>`, bounded
   `--wait-seconds`, `--poll-interval`, and `--output` pointing to
   `ess-execution-result.json`.
5. Never combine submission and long polling in one process.
6. Never automatically repeat the submission POST. Authentication refresh may
   retry request-ID tracking once, but it must never replay submission.
7. On timeout, retain the same request ID and resume tracking only when asked.

When `request_id` is supplied, skip normalization and submission unless the
user also asks for a parameter audit. Track only that existing request.

## Uncertain Submission Recovery

If the submission command may have reached Fusion but the checkpoint is missing
or unreadable, do not submit again. Use `core.fusion-api.rest-api-client` for a
read-only Scheduler query using all of these persisted values:

- exact correlation description
- application `CrmEss`
- fixed `HZ-HZGNR` job definition
- UTC submission window
- complete eight-position parameter contract

Accept recovery only when exactly one request matches. Persist its request ID
before polling. Zero or multiple matches are an `approval_blocker` and must not
trigger a replacement POST.

## Errors and Diagnostics

Classify failures as `input_validation`, `catalog_or_metadata_mismatch`,
`auth_expired_or_invalid`, `authorization_or_privilege`,
`transport_or_environment`, `fusion_api_error`, `process_timeout`,
`process_failed`, `artifact_persistence`, or `approval_blocker`.

On timeout or failure, report and persist:

- environment and business stage
- task code, application, and job definition
- request ID and ECID when available
- last ESS state and elapsed time
- safe Fusion error summary
- recommended resume or correction action

Refresh a cache-managed token after 401 or 403 at most once. Never retry a live
ESS POST without explicit reconciliation and approval. Never print or persist
tokens, secrets, token-cache contents, authorization headers, or sensitive
address data.

## References

- Oracle scheduled process and parameters:
  `https://docs.oracle.com/en/cloud/saas/customer-data-management/fageo/validate-geographies-of-addresses-against-master-geographies.html`
- Oracle Scheduler REST submission contract:
  `https://docs.oracle.com/en/cloud/saas/applications-common/25d/farca/op-ess-rest-scheduler-v1-requests-post.html`
- Oracle positional ESS argument convention:
  `https://docs.oracle.com/en/cloud/saas/financials/26b/oeswf/Chunk2108659685.html`

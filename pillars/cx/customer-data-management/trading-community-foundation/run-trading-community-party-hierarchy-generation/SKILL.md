---
skill_id: "cx.customer-data-management.trading-community-foundation.run-trading-community-party-hierarchy-generation"
name: "Run Trading Community Party Hierarchy Generation"
description: "Builds, previews, submits, and tracks Oracle Fusion Party Hierarchy Generation ESS requests. Use it for the Run Trading Community Party Hierarchy Generation FSM task with any documented hierarchy type and either Incremental or Force Flattening. When the user supplies a Version value, pass that exact value as the hierarchy-version argument."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Trading Community Foundation"
functional_area_code: "ORA_HZ_CDM_FOUNDATION"
task_code: "HZ_RUN_PARTY_HIERARCHY_GENERATION"
task_name: "Run Trading Community Party Hierarchy Generation"
parent_skill_id: "cx.customer-data-management.trading-community-foundation"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "ESS"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "verification"
execution_mode: "hybrid"
owner_team: "CX customer data management pillar team"
version: "0.9.1"
inputs:
  - "job_parameters_text"
  - "fusion_environment_context"
  - "project_id"
  - "execution_intent"
  - "execution_approval"
  - "execution_options"
  - "request_id"
outputs:
  - "normalized_job_parameters"
  - "execution_preview"
  - "contract_gap_report"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/run-trading-community-party-hierarchy-generation/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/run-trading-community-party-hierarchy-generation/current/"
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
  - "For any documented hierarchy type and flattening method, connects to the configured Oracle Fusion ESS Scheduler REST API only after exact-target checks and explicit execution authorization."
  - "An authorized submission generates or refreshes flattened trading-community party-hierarchy rows and columns."
  - "May refresh the local gitignored OAuth token cache through the invoked ESS core skill during authorized live execution."
required_privileges:
  - "ORA_ZCA_CUSTOMER_RELATIONSHIP_MANAGEMENT_APPLICATION_ADMINISTRATOR_JOB or ORA_ZCH_MASTER_DATA_MANAGEMENT_APPLICATION_ADMINISTRATOR_JOB"
  - "ORA_MANAGE_TRADING_COMMUNITY_IMPORT_BATCH_DUTY or ORA_MANAGE_TRADING_COMMUNITY_IMPORT_PROCESS_DUTY"
---

# Run Trading Community Party Hierarchy Generation

## Purpose

Accept the parameters for `Run Trading Community Party Hierarchy Generation` in
plain text, normalize them into a four-field business contract, validate and
preview the requested scope, build the exact ESS payload for every documented
hierarchy type and flattening method, and execute it through the shared ESS client
after environment, scope, and approval gates pass.

Oracle names the scheduled process `Party Hierarchy Generation` and describes
its action as `Flatten Party Hierarchy Rows and Columns`. Use it on demand after
hierarchy changes or when flattened hierarchy data appears inaccurate.

## Setup Task Contract

- Task code: `HZ_RUN_PARTY_HIERARCHY_GENERATION`
- Scheduled process: `Party Hierarchy Generation`
- Process description: `Flatten Party Hierarchy Rows and Columns`
- Application: `CrmEss`
- Job definition: `JobDefinition://oracle/apps/ess/cdm/foundation/parties/HzPartyHierarchyFlattenedDataGenJob`
- Positional argument order: `submit.argument1` hierarchy type, `submit.argument2` hierarchy name, `submit.argument3` hierarchy version identifier, `submit.argument4` flattening method
- Parameter types for `submit.argument1` through `submit.argument4`: `STRING`
- Hierarchy-type transports: Customer Hierarchy (`CUSTOMER`) -> `HZ_CUSTOMER_HIERARCHY`; Duns and Bradstreet Hierarchy (`DUNS_AND_BRADSTREET`) -> `HZ_DNB_HIERARCHY`; Partner Hierarchy (`PARTNER`) -> `HZ_PARTNER_HIERARCHY`; Trading Community Party Hierarchy (`TRADING_COMMUNITY_PARTY`) -> `HZ_PARTY_HIERARCHY`
- Flattening-method transports: Incremental Flattening (`INCREMENTAL`) -> `INCREMENTAL_FLATTENING`; Force Flattening (`FORCE`) -> `FORCE_FLATTENING`
- Hierarchy name transport (`argument2`): preserve the exact user-supplied text, or JSON `null` when omitted
- Hierarchy version transport (`argument3`): pass the exact user-supplied Version value unchanged, or omit its `value` when no version is selected; do not ask the user for a separate internal identifier
- Client safety policy: `retries: 0`, one POST per authorization, no automatic resubmission, and separate requestId polling
- Compatibility: do not rely on undocumented Scheduler compatibility; the client safety policy remains mandatory
- Golden evidence: developer-provided successful Scheduled Processes result plus the established repository payload convention used by executable ESS skills
- Submit endpoint: `POST /ess/rest/scheduler/v1/requests`
- Track endpoint: `GET /ess/rest/scheduler/v1/requests/{requestId}`
- CSV export/import: not supported by the effective setup-task catalog

Use the application, job definition, `STRING` parameter type, argument order,
hierarchy-type transports, and flattening-method transports exactly as declared
above. The `submit.argumentN` naming, `STRING` type, omitted `value` for a null
position, and `retries: 0` follow the repository's existing executable ESS
skills and shared ESS client contract, as explicitly authorized for this task.
Do not infer values beyond the documented option set. Do not call the ESS submitter
when a selected mapping is unknown, the target is unresolved, or approval
is blocked. Do not substitute
browser automation, a direct REST call, or another loader for the missing
declared contract.

## Resource Read Order

Before preview or execution-readiness evaluation, read the task-local resources
in this order:

1. `ora-resource/ora_input_validation.md`
2. `ora-resource/ora_defaulting_rules.md`
3. `ora-resource/ora_reference_lookups.md`
4. `ora-resource/ora_dependency_readiness.md`
5. `ora-resource/ora_design_enforcement.md`
6. `ora-resource/ora_error_handling.md`

Treat `ora-resource/ora_rule_registry.json` as compiled execution metadata, not
as authorization. A planner result blocked by `TBD` lookup contracts must stay
blocked.

## Inputs

- `job_parameters_text`: plain business-language job settings.
- `fusion_environment_context`: target Fusion environment; resolve it only when
  exactly one configured environment is active.
- `project_id`: required for any live submission so the preview and
  request checkpoint survive an interrupted session.
- `execution_intent`: `preview` or `execute`; retain a direct `run` or `submit`
  instruction while collecting missing values. Execution intent is not approval
  to submit.
- `execution_approval`: explicit confirmation of the single consolidated
  approval preview. Bind it to the exact target, normalized parameters, payload
  fingerprint and correlation description internally; do not display those
  internal identifiers in the user-facing confirmation.
- `execution_options`: optional `wait_seconds` and `poll_interval` for
  request tracking.
- `request_id`: optional positive ESS request ID used only to resume tracking
  after the exact job identity has been reconciled.

## Plain-Text Normalization

Normalize the user's text into this business contract before running the
bundled builder.

| Canonical field | Requirement | Accepted canonical values |
|---|---|---|
| `hierarchy_type` | Required | `CUSTOMER`, `DUNS_AND_BRADSTREET`, `PARTNER`, `TRADING_COMMUNITY_PARTY` |
| `hierarchy_name` | Optional | Exact user-supplied hierarchy name; transport as `null` when omitted |
| `hierarchy_version` | Optional | Exact user-supplied Version value; pass it unchanged as ESS argument 3 |
| `flattening_method` | Required | `INCREMENTAL`, `FORCE` |

Treat any supplied Version value as the exact value for `argument3`. Do not
expose the internal ESS term or ask the user for a separate transport ID. Use
JSON `null` only when no hierarchy version is supplied.

Also derive these preview-only authorization facts:

- `all_hierarchies_explicit`: true when the user explicitly says all
  hierarchies/no hierarchy-name filter, or directly confirms a consolidated
  execution preview that visibly states the omitted name applies to all
  hierarchies of the selected type.
- `force_flattening_explicit`: true only when the user explicitly asks for
  Force Flattening or an unambiguous full reflatten.

Apply these language rules:

1. Map `customer hierarchy` to `CUSTOMER`.
2. Map `D&B`, `Dun and Bradstreet`, or `Duns and Bradstreet` to
   `DUNS_AND_BRADSTREET`.
3. Map `partner`, `partner hierarchy`, or `partner hierarchies` to `PARTNER`.
   Map `trading community party` or `trading community party hierarchy` to
   `TRADING_COMMUNITY_PARTY`; the word `partner` alone never means Trading
   Community Party Hierarchy.
4. Map `incremental`, `changes only`, or `deltas` to `INCREMENTAL`.
5. Map `force flattening`, `full mode`, `full flattening`, `rebuild the
   flattened hierarchy`, or `reflatten from scratch` to `FORCE`. Treat a bare
   `full` as ambiguous only when the surrounding words do not identify either
   flattening method or hierarchy scope; include that ambiguity in the same
   combined intake question as any other missing detail.
6. Treat `active`, `current`, or `use the active version` as a request to leave
   `hierarchy_version` unset and transport JSON `null` for `argument3`.
7. Preserve the exact hierarchy name as `argument2` and the exact supplied
   Version value as `argument3`.
8. Allow live execution for every documented hierarchy type with either
   flattening method after all ordinary target, scope, payload, and approval
   gates pass.

### Parameter Intake

On a bare invocation, or whenever a required value is missing or genuinely
ambiguous, ask once for every unresolved value and show the complete supported
option list:

```text
Please provide the hierarchy-generation settings. Hierarchy type and flattening method are required. You can also say "use Oracle defaults."

- Hierarchy type: Customer, Duns and Bradstreet, Partner, or Trading Community Party
- Hierarchy name (optional): Exact hierarchy name, or all hierarchies of that type
- Hierarchy version (optional): Active/default version, or an exact version
- Flattening method: Incremental or Force
```

Apply these intake rules:

1. Do not ask for a field already supplied unambiguously in the current request
   or earlier messages in the same intake.
2. Gather all unresolved required fields in one message. Always show all four
   hierarchy-type options and both flattening-method options so the user can
   answer without another discovery round.
3. Interpret `use Oracle defaults` as explicit selection of Customer Hierarchy
   and Incremental Flattening. Show both derivations in the preview.
4. Optional fields do not cause a second intake round. Preserve a supplied
   Version exactly and use it directly for execution; do not ask for a separate
   internal identifier. For execution intent, interpret an omitted hierarchy
   name as the proposed scope `All hierarchies of the selected type` and an
   omitted version as `Active/default version`; transport both as `null` and
   show both proposed values in the consolidated confirmation list.
5. Treat explicit `all hierarchies`, `leave the name blank`, or `no name filter`
   as broad-scope authorization. When the name is merely omitted, do not ask a
   separate scope question: the single consolidated execution confirmation must
   explicitly state that the null name applies to all hierarchies, and the
   user's confirmation authorizes that broad scope together with submission.
6. Keep an explicit `run`, `submit`, or equivalent execution instruction active
   while collecting missing values; do not make the user repeat it. Treat it as
   execution intent only, not as submission approval.
7. For execution intent, resolve the configured Fusion environment after the
   required parameters are complete and before asking for approval. When exactly
   one environment is configured, select it automatically and show it in the
   consolidated approval. Ask the user to select an environment only when none
   or more than one can be resolved; this is input collection, not a separate
   approval.
8. Treat every new user request to `run`, `run again`, `rerun`, `submit`, or
   equivalent as a new run. Start a fresh intake and create a new run ID,
   preview, payload, and approval checkpoint. Never answer a new run request by
   reporting that a previous run completed, and never reuse parameters from a
   completed run unless the user supplies them again in the current intake.

Do not lead with task codes, lookup names, ESS argument names, application
names, or job-definition paths. Accept canonical values when supplied, but
translate them to business labels in the response.

## Deterministic Preview Builder

Write the canonical object to a temporary or project-local JSON file and run:

```bash
python3 pillars/cx/customer-data-management/trading-community-foundation/run-trading-community-party-hierarchy-generation/scripts/build_party_hierarchy_request.py \
  --input <canonical-parameters.json> \
  --description "FDOS:party-hierarchy-generation:<project_id>:<run_id>" \
  --payload-output <ess-request.json> \
  --report-output <request-preview.json>
```

The input may contain the four job fields plus `all_hierarchies_explicit` and
`force_flattening_explicit`. The builder rejects unknown fields, normalizes
documented labels, records broad-scope and force warnings, and emits the
verified four-position argument contract. Every documented hierarchy-type and
flattening-method combination returns the exact `ess_request_payload`; unknown
mappings emit no payload and return blocking gaps. Optional null positions remain present with `name` and
`paramType` but omit the `value` property.

The builder fails closed when an output already exists. Use a new run path, or
use `--force` only after explicit overwrite approval. It never permits an
output to replace the input file or permits the payload and report to share a
path.

## Preview and Single Consolidated Authorization

Always show every business parameter before submission:

Render values with business labels. Render omitted optional values as the
concrete proposed behavior, not as an unresolved question.

```markdown
Party Hierarchy Generation

- Job: Party Hierarchy Generation
- Environment: <environment name or host>
- Hierarchy type: <business label>
- Hierarchy scope: <exact name, or All hierarchies of the selected type (name filter omitted)>
- Hierarchy version: <exact version, or Active/default version (version omitted)>
- Flattening method: <business label>
- Warning: <broad-scope or Force warning; omit when none applies>
```

Keep the confirmation business-facing. Show the scheduled-process job name,
environment, hierarchy type, scope, version, flattening method, and applicable
warnings. Do not show the application name (`CrmEss`), job-definition path,
task code, ESS argument names, transport values, payload fingerprint,
correlation description, retry mechanics, or polling mechanics. Keep those
details in the persisted audit artifacts and use them internally to bind the
approval to the immutable request.

When the user asks only for a preview, return it without an execution question.
When the user asks to run, retain that intent. Missing required values or an
unresolved target are contract blockers. An omitted optional name or version is
not an intake blocker: disclose its exact effect in the confirmation list.

For execution intent, use exactly one business approval point:

1. Complete parameter intake, resolve exactly one configured environment, build
   the immutable payload, choose the tracking window, and persist the preview
   before asking for approval.
2. Do not ask separately to approve parameters, hierarchy scope, environment,
   Force impact, or job submission. Questions needed to obtain missing required
   values are intake questions, not approval prompts. The consolidated approval
   also confirms all-hierarchy scope when the hierarchy name was omitted.
3. Present one consolidated approval containing the job name `Party Hierarchy
   Generation`, exact environment, all four business parameters, and applicable
   warnings. Keep the application, job-definition path, task code, ESS
   arguments, transport values, payload fingerprint, correlation description,
   retry mechanics, and polling mechanics internal.
4. Ask once for explicit confirmation to submit that exact request. A prior
   `run`, `submit`, or `proceed` instruction expresses intent but does not replace
   this approval.
5. Treat `yes`, `confirm`, or `proceed` as approval only when it directly answers
   the consolidated approval prompt. If any bound detail changes, invalidate the
   approval, rebuild the preview, and present one replacement consolidated
   approval.

After approval, submit once without another business confirmation. An OAuth or
host-platform permission prompt is operational authentication, not an extra
approval of the job parameters or target.

### Fresh Run Semantics

A new run request always starts a new execution lifecycle, even when an older
run for the same task, environment, or parameters succeeded. Use prior runs
only as audit history. Do not present an older completion as the outcome of the
new request, do not treat it as satisfying current intake or approval, and do
not reuse its request ID. Collect the current request's parameters, generate a
new immutable preview and correlation description, and obtain a new approval
before submitting once.

## Live-Execution Contract

Developer-provided successful Scheduled Processes evidence currently
establishes:

1. Scheduler `application`: `CrmEss`.
2. `jobDefinitionId`: `JobDefinition://oracle/apps/ess/cdm/foundation/parties/HzPartyHierarchyFlattenedDataGenJob`.
3. Argument order: hierarchy type, hierarchy name, internal hierarchy version
   identifier, flattening method.
4. Hierarchy-type transports: `HZ_CUSTOMER_HIERARCHY`, `HZ_DNB_HIERARCHY`, `HZ_PARTNER_HIERARCHY`, and `HZ_PARTY_HIERARCHY` for the four documented hierarchy choices in their declared order.
5. Flattening-method transports: `INCREMENTAL_FLATTENING` and `FORCE_FLATTENING`.
6. Hierarchy name transport: exact user-supplied text or JSON `null`.
7. Hierarchy version transport: the exact user-supplied Version value, or JSON
   `null` when no version is supplied. Do not ask for a separate internal value.
8. One UI-submitted request completed with status Succeeded.

The repository's executable ESS skills and shared submitter establish the
remaining request convention for this task, as authorized by the developer:

1. Use `submit.argument1` through `submit.argument4`.
2. Use `paramType: STRING` for all four positions.
3. Keep all four position objects. Omit `value` when an optional position is
   null; never send JSON null, an empty string, or `#NULL`.
4. Accept `hierarchy_version` as exact user-supplied text and pass it unchanged
   as argument 3 when present.
5. Set `retries: 0`, submit once, persist the requestId checkpoint, and poll in
   a separate invocation. Never automatically resubmit an uncertain request.

Live execution supports all four documented hierarchy types with Incremental
or Force Flattening. Add mappings and tests before accepting any future Oracle
option beyond this documented set.

## Preflight Checks

Before any ESS submission, validate the exact target environment, required role
or duty, normalized hierarchy type and method, consolidated approval of the
displayed broad scope when the hierarchy name is omitted, displayed Force
impact when selected, all four ordered `STRING` arguments, immutable payload
fingerprint, project output paths, current consolidated approval, `retries: 0`,
and the separate polling checkpoint. Stop before submission when any check
fails or is ambiguous.

## Two-Phase Execution

For a supported and approved request, use the established two-phase pattern:

1. Require `project_id` and persist the normalized preview, exact payload,
   unique correlation description, target environment, and UTC submission
   window.
2. Require the consolidated approval bound to those persisted details, then
   invoke `core.fusion-api.ess-job-submitter` with `--payload-file`,
   `--submit-only`, `--retries 0`, and a checkpoint output path.
3. Persist and report exactly one positive `requestId` before polling.
4. Invoke the core skill separately with `--request-id`, bounded
   `--wait-seconds`, and `--poll-interval`.
5. Never combine submission and long polling or automatically repeat the POST.
6. On an uncertain submission, reconcile read-only using the persisted
   correlation description, exact job identity, UTC window, and complete
   parameter contract. Accept only one exact match.

When `request_id` is supplied, require source-verified job identity before
tracking it as this task. Do not assume an arbitrary ESS
request belongs to Party Hierarchy Generation.

## Errors and Diagnostics

Classify failures as `input_validation`, `catalog_or_metadata_mismatch`,
`auth_expired_or_invalid`, `authorization_or_privilege`,
`transport_or_environment`, `fusion_api_error`, `process_timeout`,
`process_failed`, `artifact_persistence`, or `approval_blocker`.

Persist and report the environment, stage, task code, safe message, recommended
action, artifact references, and external IDs when available. Refresh a
cache-managed token after 401 or 403 at most once. Never retry a live ESS POST
without reconciliation and approval. Never print or persist tokens, secrets,
token-cache contents, authorization headers, or sensitive hierarchy data.

## References

- Oracle scheduled process and parameter documentation:
  `https://docs.oracle.com/en/cloud/saas/sales/fauss/party-hierarchy-generation.html`
- Oracle predefined party hierarchy tree-structure codes:
  `https://docs.oracle.com/en/cloud/saas/customer-data-management/faudm/how-you-manage-hierarchies.html`
- Oracle Partner hierarchy tree-structure evidence:
  `https://docs.oracle.com/en/cloud/saas/sales/oedms/zcabipartnerhierarchiesv-3005.html`
- Oracle FSM-to-ESS process mapping:
  `https://docs.oracle.com/en/cloud/saas/sales/facaa/scheduled-processes-for-analytics.html#s20074846`
- Oracle Scheduler REST submission contract:
  `https://docs.oracle.com/en/cloud/saas/applications-common/25d/farca/op-ess-rest-scheduler-v1-requests-post.html`

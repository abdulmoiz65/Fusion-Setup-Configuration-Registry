---
skill_id: "cx.customer-data-management.enterprise-profile.manage-geographies"
name: "Manage Geographies Setup Task Guidance"
description: "Creates geography country structures and hierarchy master data for one country from either Oracle-licensed Loqate data or creation-only user-provided data under CX Customer Data Management Enterprise Profile."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Enterprise Profile"
functional_area_code: "ORA_ASK_ENTERPRISE_PROFILE"
task_code: "HZ_MANAGE_GEOGRAPHIES"
task_name: "Manage Geographies"
parent_skill_id: "cx.customer-data-management.enterprise-profile"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "CXIMPORT"
businessObject: ""
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
type: "import"
execution_mode: "hybrid"
owner_team: "CX customer data management pillar team"
version: "0.11.18"
inputs:
  - "country"
  - "geography_source"
  - "execution_phase"
  - "requested_scope"
  - "structure_definition_or_csv"
  - "hierarchy_definition_or_csv"
  - "fusion_environment_context"
  - "project_id"
  - "task_context"
  - "task_sequence"
  - "execution_options"
  - "execution_intent"
  - "execution_confirmation"
outputs:
  - "country_resolution"
  - "source_resolution"
  - "geography_request_model"
  - "geography_file_validation"
  - "geography_structure_csv"
  - "geography_hierarchy_csv"
  - "immutable_data_loader_artifact"
  - "data_loader_task_validation_envelope"
  - "structure_import_mapping_preview"
  - "hierarchy_import_mapping_preview"
  - "structure_import_mapping_result"
  - "hierarchy_import_mapping_result"
  - "data_loader_import_authorization"
  - "structure_import_preview"
  - "hierarchy_import_preview"
  - "cx_mapping_csvs"
  - "data_loader_preflight_envelopes"
  - "data_loader_initiation_result"
  - "pending_geography_stage"
  - "structure_ucm_upload_result"
  - "hierarchy_ucm_upload_result"
  - "structure_import_result"
  - "hierarchy_import_result"
  - "ucm_account_resolution"
  - "profile_preflight_result"
  - "profile_change_plan"
  - "profile_change_result"
  - "internal_execution_plan"
  - "ess_submission_checkpoint"
  - "approved_ess_submission"
  - "ess_recovery_result"
  - "ess_execution_result"
  - "geography_setup_result"
  - "next_country_prompt"
  - "diagnostics"
  - "skill_run_record"
  - "token_usage_record"
uses_core:
  - "core.data-loader"
  - "core.data-loader.task-hook"
  - "core.fusion-api.apps-common"
  - "core.fusion-api.ess-job-submitter"
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
depends_on:
  - "schemas/ess-delegation-contract.schema.json"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/enterprise-profile/manage-geographies/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/enterprise-profile/manage-geographies/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/enterprise-profile/manage-geographies/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
oracle_supplied_guidance_files:
  - purpose: "Source, execution phase, country, scope, file, hierarchy, mapping, and environment input collection"
    location: "ora-resource/ora_input_intake.md"
  - purpose: "Loqate and user-data country, CSV, hierarchy, import-mapping, polling, project-path, profile-value, and Data Loader approval validation"
    location: "ora-resource/ora_input_validation.md"
  - purpose: "Loqate, DaaS endpoint, Data Loader import authorization, and execution-intent dependencies"
    location: "ora-resource/ora_dependency_readiness.md"
  - purpose: "Supported country codes, site-level profile values, CX object metadata, and import-mapping resolvers"
    location: "ora-resource/ora_reference_lookups.md"
  - purpose: "Country-code, import-mapping, polling, job, parameter, and retry defaults"
    location: "ora-resource/ora_defaulting_rules.md"
  - purpose: "Single-country Loqate and user-provided CSV, table, tree, or bulk behavior"
    location: "ora-resource/ora_bulk_intake.md"
  - purpose: "Profile reads, Data Loader Task Hook approval, import-mapping persistence, UCM handoff, ESS/import submission, polling, and live gates"
    location: "ora-resource/ora_rest_execution.md"
  - purpose: "Geography structure and hierarchy scope boundaries"
    location: "ora-resource/ora_design_advisory.md"
  - purpose: "Failure classification, disclosure, retry, and recovery"
    location: "ora-resource/ora_error_handling.md"
  - purpose: "Mandatory country, profile, environment, immutable-artifact, and single-request gates"
    location: "ora-resource/ora_design_enforcement.md"
oracle_supplied_guidance_status:
  source_alignment: "Current Oracle Fusion Cloud 26C Loqate, Country Structure, Geography Import Management documentation, the core site-level profileOptions contract, and the user-supplied ESS/import contracts"
  execution_contract: "Uses core.data-loader and its Task Hook as the mandatory orchestrator, verifies the immutable artifact immediately before mutation, then invokes existing ESS, Fusion REST, or UCM core services; no task-local transport implementation"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Oracle Fusion Cloud 26C or a compatible current release"
side_effects:
  - "Uses the configured Fusion authentication flow automatically and may refresh or replace an expired cache-managed session without asking for authentication permission."
  - "Reads configured site-level profile option values and CX import-object metadata from Oracle Fusion."
  - "When ORA_HZ_ENABLE_DAAS_LOQATE is not Y, explicitly asks whether the user wants to use Loqate as the geography-data source and explains that doing so requires setting ORA_HZ_ENABLE_DAAS_LOQATE to Y; only after the combined business-level confirmation creates or updates it. When ORA_HZ_DAAS_GEO_ENDPOINT is missing or blank, asks the user to configure its SITE value and stops before import until a later read verifies it."
  - "After Data Loader validates the immutable request and the user explicitly approves that preview, submits the Import Geography Data ESS job for one country."
  - "A successful ESS job defines the selected country's geography structure and imports its hierarchy master data."
  - "For user-provided full_import, hands stage-specific mapping and data CSVs to core.data-loader; after its approval and integrity gates, the helper uploads CRM documents and initiates a CX data load. Structure and hierarchy are separate loads, with hierarchy blocked until a requested status check confirms structure success."
  - "Only mapping_only looks up or creates reusable Fusion import mappings through the authorized REST core service. Full imports supply mapping CSVs to Data Loader and do not create mappings or import activities directly."
  - "User-provided imports are additive only; this skill never deletes, replaces, or updates an existing geography structure or geography."
  - "May refresh the local gitignored OAuth token cache through the invoked core skills for read-only operations; it does not retry a live POST after an authentication or authorization response."
required_privileges:
  - "Master Data Management Applications Administrator role"
  - "FND_APP_MANAGE_ALL_PROFILE_VALUES_PRIV to create or update site-level profile option values"
  - "Fusion ESS privileges required to submit and monitor Import Geography Data"
  - "Fusion Import Management privileges for Country Structure and Geography objects"
  - "Fusion Import Mapping read and create privileges plus successful core.data-loader Task Hook validation and approval for the central REST service"
  - "CRM Documents upload and Data Loader initiation privileges for native CX full_import"
---

# Manage Geographies Setup Task Guidance

## Purpose

Define the geography country structure and import geography hierarchy master
data for one country from either Oracle-licensed Loqate data or creation-only
data gathered or supplied for the request. Accept a simple Loqate request such
as "Set up geographies for India," or a request containing an ordered structure,
a hierarchy tree/table, compatible CSV files, or a request to prepare the
reusable Country Structure and Geography import mappings. Preserve the existing
Loqate workflow. Route every live geography mutation through `core.data-loader`
and its Task Hook. Gather and validate the business data, resolve every technical
prerequisite internally, show one concise business preview, and after the user
approves it invoke the existing ESS service, mapping-only REST service, or
native Data Loader helper without adding task-local authentication or transport.

## Delegated Execution Boundary

This skill owns Manage Geographies business rules, geography-data
transformation, local preconditions and postconditions, and task-local outcome
transitions. It delegates authentication, transport, upload, submission,
polling, retry, artifact persistence, and cross-task workflow coordination to
the declared core services and the active implementation workflow. References
to core command modes, request paths, headers, checkpoint fields, or adapters
identify the task-specific values required by those contracts; they do not
create task-local technical implementations. The task registry represents only
the local rules and outcomes required to complete this setup task.

## Setup Task Skill Contract

- task_code: `HZ_MANAGE_GEOGRAPHIES`
- task_name: `Manage Geographies`
- parent_skill_id: `cx.customer-data-management.enterprise-profile`
- pillar: `CX`
- offering: `Customer Data Management`
- functional_area: `Enterprise Profile`
- functional_area_code: `ORA_ASK_ENTERPRISE_PROFILE`
- available_flag: `Y`
- export_import_supported_flag: `N`
- csv_export_import_supported_flag: `N`
- source_catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`

## Usage

Use this skill when planning, validating, or executing `Manage Geographies`
under `Enterprise Profile`, including custom or third-party creation-only
country structures, geography hierarchy master data, and their reusable Fusion
Import Management mappings.

## Setup Task Metadata

- Task name: `Manage Geographies`
- Task code: `HZ_MANAGE_GEOGRAPHIES`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- FSM CSV export/import routing: `not supported`
- Data Loader import mode: `CXIMPORT`
- User-provided CSV routing: `core/data-loader/scripts/upload_and_initiate.py`
  with `--cx-import`; this does not change the catalog flags above

## Inputs

- `country`: one country name or two-letter country code; Loqate requests must
  resolve against the Loqate-supported list, while user-provided structure
  requests use the explicit or locally resolved ISO two-letter country code
- `geography_source`: internally resolve `oracle_loqate` or `user_provided`;
  select Loqate for a standard supported-country setup request with no custom
  hierarchy, and select user-provided when custom structure/hierarchy data is
  supplied, requested, or gathered for a named hierarchy
- `execution_phase`: for `user_provided`, `mapping_only` or `full_import`;
  default to `full_import` when the request includes geography data and to
  `mapping_only` only when the user explicitly asks to prepare or register the
  reusable mappings
- `requested_scope`: for user-provided data, `structure_only`,
  `hierarchy_only`, or `structure_and_hierarchy`; during `mapping_only`, this
  selects which stable mapping definition or definitions to prepare
- `structure_definition_or_csv`: ordered geography levels or a local CSV with
  `CountryCode,LevelNumber,GeographyType`; required when scope includes structure
- `hierarchy_definition_or_csv`: hierarchy tree/table or a local Geography
  import CSV; required when scope includes hierarchy
- `fusion_environment_context`: optional when exactly one active configured
  Fusion environment can be resolved; otherwise require the target environment
- `project_id`: required for live execution so the submission checkpoint and
  request ID survive an interrupted command-output session
- `execution_options`: optional `wait_seconds` and `poll_interval` for Loqate;
  native CX status is requested separately and is never polled after initiation
- `task_context` and `task_sequence`: required Task Hook inputs for a live
  Data Loader route
- `execution_intent`: inferred from the user's request; any initial imperative
  authorizes validation and immutable preview generation only

`country`, `structure_definition_or_csv`, and `hierarchy_definition_or_csv`
are not required for `mapping_only`. The target environment, `project_id`,
requested scope, exact mapping preview, execution intent, and Data Loader Task
Hook approval remain mandatory because creating an import mapping changes
Fusion configuration.

The user never supplies an import-file account, object metadata result, mapping
number, adapter, REST path, or technical payload. Native full_import returns
Data Loader's required account and identifier fields in its preview and result.
Resolve those values internally, retain them only in redacted durable audit
artifacts, and omit extra technical payload details from normal previews and failures.
Expose additional raw technical details only when the user requests them.

The user also never supplies or overrides import-mapping names, object codes,
or column pairs. Load those reviewed values from
[the task-owned mapping definitions](references/import-mapping-definitions.json).
Run the mandatory `core.data-loader` validation, immutable-preview, and approval
gates. After authorization, invoke native Data Loader for full_import or the
authorized REST core service for mapping_only; do not implement task-local Fusion REST or file-staging transport.

## Outputs

For full_import also return `cx_mapping_csvs`, `data_loader_preflight_envelopes`,
`data_loader_initiation_result`, and `pending_geography_stage`. Legacy mapping
IDs and import-activity results below belong to mapping_only or historical runs.

- `country_resolution`
- `source_resolution`
- `geography_request_model`
- `geography_file_validation`
- `geography_structure_csv`
- `geography_hierarchy_csv`
- `immutable_data_loader_artifact`
- `data_loader_task_validation_envelope`
- `structure_import_mapping_preview`
- `hierarchy_import_mapping_preview`
- `structure_import_mapping_result`
- `hierarchy_import_mapping_result`
- `data_loader_import_authorization`
- `structure_import_preview`
- `hierarchy_import_preview`
- `structure_ucm_upload_result`
- `hierarchy_ucm_upload_result`
- `structure_import_result`
- `hierarchy_import_result`
- `ucm_account_resolution`
- `profile_preflight_result`
- `profile_change_plan`
- `profile_change_result`
- `internal_execution_plan`
- `ess_submission_checkpoint`
- `approved_ess_submission`: the validated ESS delegation envelope, created
  only after Task Hook approval and artifact verification
- `ess_recovery_result`
- `ess_execution_result`
- `geography_setup_result`
- `next_country_prompt`
- `diagnostics`
- `skill_run_record`
- `token_usage_record`

## Read Order

1. Read [input intake](ora-resource/ora_input_intake.md).
2. Read [input validation](ora-resource/ora_input_validation.md).
3. Read [reference lookups](ora-resource/ora_reference_lookups.md).
4. Read [defaulting rules](ora-resource/ora_defaulting_rules.md).
5. Read [dependency readiness](ora-resource/ora_dependency_readiness.md).
6. Read [bulk behavior](ora-resource/ora_bulk_intake.md).
7. Read [design advisory](ora-resource/ora_design_advisory.md).
8. Read [design enforcement](ora-resource/ora_design_enforcement.md).
9. Before payload construction, internal request validation, or live execution,
   read [REST and ESS execution](ora-resource/ora_rest_execution.md) and
   [error handling](ora-resource/ora_error_handling.md).
10. For user-provided mapping preparation or import, read
    [the task-owned mapping definitions](references/import-mapping-definitions.json).
11. Use [the compiled task registry](ora-resource/ora_rule_registry.json) as
    the task-local execution graph.

## Execution Discipline

1. Accept exactly one country and one source mode per run. Infer the source from
   the requested business outcome: standard country setup uses Loqate; a named
   custom structure or hierarchy uses user-provided data. Do not ask the user
   to choose an implementation route.
2. Start or refresh the configured Fusion authentication flow automatically
   when needed. Do not ask the user for permission to authenticate and never ask
   them to provide credentials or tokens in chat.
3. For `oracle_loqate`, use `core.fusion-api.apps-common` for configured site-level profile-value
   reads and any explicitly approved writes. Do not add OAuth or REST transport
   logic to this skill.
4. Apply the Loqate profile, supported-country, and ESS rules below only to the
   `oracle_loqate` branch. User-provided data must not read or mutate the two
   Loqate profile options and must not submit the Loqate ESS job.
5. For `oracle_loqate`, require `ORA_HZ_ENABLE_DAAS_LOQATE` = `Y`. Require
   `ORA_HZ_DAAS_GEO_ENDPOINT` to contain any non-null, non-empty value after
   trimming; do not require a specific endpoint URL.
6. When both profiles already satisfy those conditions, report them as
   validated and continue immediately. Do not write either profile and do not
   ask for profile-change confirmation.
7. If `ORA_HZ_ENABLE_DAAS_LOQATE` is missing or is not `Y`, the single
   geography execution preview must explicitly ask whether the user wants to
   use Loqate as the source for geography data. Explain that doing so requires
   setting `ORA_HZ_ENABLE_DAAS_LOQATE` to `Y`, and show the profile option's
   safe current state and proposed value. Use one combined Loqate-and-submission
   question; do not ask separate profile and submission questions.
8. If `ORA_HZ_DAAS_GEO_ENDPOINT` is missing or blank, ask the user to configure
   its site-level value and stop before import. Do not propose a default URL or
   write this profile option. On a later run, re-read and verify it before
   continuing. After approval for an eligible `ORA_HZ_ENABLE_DAAS_LOQATE`
   change, create or update only that profile and re-read both profiles.
9. Stop before internal request validation when the country, post-change
   profile verification, or environment gates fail.
10. Build and validate the exact request internally, resolve read-only technical
    prerequisites, create the immutable artifact, and render one business-only
    Data Loader preview. An initial imperative never authorizes the first POST.
11. After standalone approval of the current immutable preview, apply any
    included prerequisite remediation and then use
    `core.fusion-api.ess-job-submitter` in two phases: submit with
    `--submit-only` and a durable `--output` checkpoint, then track with
    `--request-id`. Do not combine submission and long polling in one process.
12. Before submission, persist a unique correlation description and the exact
    submission window. After submission, read the durable checkpoint, require
    its `requestId`, persist that ID, and report it before starting polling.
13. Submit once. Never automatically retry or replace an uncertain request.
    If command output is interrupted, inspect the checkpoint first and use the
    read-only recovery query through `core.fusion-api.rest-api-client` only when
    the checkpoint is missing or unreadable.
14. Treat a polling timeout as nonterminal and resume the same `requestId`.
15. Report prerequisite readiness in business language, geography structure and
    hierarchy status, and the ESS job ID (`requestId`). Always show
    `ORA_HZ_ENABLE_DAAS_LOQATE` and proposed value `Y` when asking whether the
    user wants Loqate to supply the geography data; keep the DaaS endpoint
    value out of every user-facing response and redacted diagnostic. Keep
    mappings, metadata, and file-staging details internal unless explicitly
    requested.
16. Ask a concise clarifying question only when a missing country or genuinely
    ambiguous target environment changes the business outcome. Never ask about
    source mode, mappings, import accounts, object metadata, adapters, payloads,
    or transport.
17. Tell the user whenever a lookup, profile mutation or verification, ESS
    submission, polling request, or ESS process fails. Include the failed
    business stage, safe error summary, known job ID, and recommended next step.
18. Persist only redacted project outputs and token-usage records.
19. After terminal success, ask whether the user wants to set up geographies
    for another country. If the user supplies another country, treat it as a
    fresh one-country run: resolve it, repeat all reads and gates, and submit a
    separate job only when that run is authorized. Never turn this into a
    multi-country batch.
20. If the terminal ESS error unambiguously states that geography data for the
    selected country already exists or was already imported, report that fact
    plainly and ask whether to set up another country, using the same prompt and
    fresh-run behavior as terminal success. Do not retry, claim a new import, or
    present generic troubleshooting for this known condition.
21. For `user_provided`, resolve `execution_phase` first. `mapping_only`
    retains the reviewed REST mapping-preparation route; `full_import` uses
    the native Data Loader CX Import route described below.
22. Load the reviewed mapping definitions and validate the complete one-country
    structure/hierarchy model before generating mapping and data CSVs.
23. For full_import, invoke only `core.data-loader`'s `upload_and_initiate.py`
    for preflight and approved submission. Do not call the standalone CX adapter,
    ERP Integration upload, importMappings, or importActivities as a fallback.
24. Use one mapping CSV and its data CSV per stage. The mapping CSV's
    `IMPORT OBJECT` is authoritative; do not also pass `--cx-import-object-code`.
25. Let Data Loader resolve the exact object's UCM account before approval and
    retain its normalized representation in the envelope. After approval, use
    only the saved envelope and artifact; never requery live metadata or rebuild
    sources. Return the Data Loader preview and result without hiding required
    Business Object Name, UCM Account, Content ID, or Request ID fields.
26. Reject update, upsert, delete, replacement, and ambiguous identifier semantics
    locally. The helper has no ImportMode flag: do not invent a CREATE_ONLY
    option or claim that it sets that mode. If target support cannot establish
    the required additive behavior, stop before approval as a catalog mismatch.
27. For structure_and_hierarchy, initiate structure first and stop with hierarchy
    pending. Only a user-requested status check may confirm successful structure
    completion and permit a separately validated and approved hierarchy load.
28. Preserve partial successes and reconcile uncertain uploads or initiation;
    never replay a load from the status path.

### Data Loader authorization lifecycle

Apply this lifecycle only to Loqate ESS submission and mapping_only REST
mapping preparation. Full imports use the native Data Loader envelope lifecycle
in the user-provided workflow below:

1. For `oracle_loqate`, complete the pillar-owned **Loqate ESS preflight and
   delegation** in `ora-resource/ora_rest_execution.md`. This explicitly selected
   ESS route uses the existing Task Hook validation and approval commands, with
   the Loqate preflight replacing their native file-import preflight prerequisite.
   This exception is limited to this pillar's `oracle_loqate` branch; it does not
   change the shared Data Loader or Task Hook contracts for other operations.
   For `mapping_only`, retain the existing Data Loader authorization requirement;
   stop if that route cannot authorize the mapping operation.
   Build one deterministic immutable artifact under the project workspace. For
   Loqate, use JSON containing the exact environment, country, job identity,
   request payload, execution options, prerequisite change plan, correlation
   description, checkpoint path, and business effect. For `mapping_only`, use JSON or ZIP
   containing the exact mapping definitions and environment. Do not use this JSON/manifest archive for full_import: CX archives accept
   only mapping and data CSVs. Calculate the applicable artifact SHA-256.
2. Resolve the task with `core/data-loader/task-hook/scripts/task_hook.py
   data-load` using the selected `task_context`, task name, and sequence. Read
   its execution guide and evaluate applicable registry nodes; `ready` alone
   is not completed validation. Stop if readiness or task-rule validation fails.
3. Run `build-data-load-preview --input-stdin` with the resolved task context,
   ordered rule results, the complete immutable request in `finalData`, and
   `finalData.archiveSha256`. Render only the country,
   target environment, source description, structure levels, hierarchy row or
   node counts, creation-only boundary, execution order, and any prerequisite
   business change. Do not render hashes, archives, mapping definitions or IDs,
   object metadata, import-file accounts, adapters, REST paths, or payloads.
   End with exactly: `Do you want to proceed with submitting the reviewed
   archive?`
4. Treat only a standalone affirmative reply to the latest unchanged preview
   as approval. Then run `approve-data-load-preview --input-stdin` and
   `verify-approved-data-load-archive --input-stdin --archive <artifact>`.
   Persist the returned `taskValidationEnvelope` and `archiveSha256` receipt.
5. Immediately before every live core-service mutation, rerun
   `verify-approved-data-load-archive` against the receipt inputs and exact
   artifact, and require its SHA-256 to match the persisted receipt. Before a
   UCM upload, also require the CSV bytes to match exactly one same-named member
   of the approved ZIP. A changed country, environment, business data, scope,
   creation semantics, or artifact bytes invalidates approval. Server-issued
   mapping numbers, activity IDs, document IDs, and an internally revalidated
   adapter-specific account representation do not require another confirmation
   when they leave the approved business effect and artifact bytes unchanged.

## Workflow

### Select the geography source

Resolve `geography_source` before country-specific execution:

- Choose `oracle_loqate` when the user explicitly requests Oracle-licensed or
  Loqate data, or asks for standard supported geography setup without supplying
  custom data.
- Choose `user_provided` when the user supplies or asks the agent to form a
  country structure, hierarchy, table, tree, or CSV from their own data.
- When neither rule is conclusive, default a plain country-setup request to
  Loqate and a request naming custom levels or geographies to user-provided
  data. Stop only when the requested business outcome itself is contradictory;
  never ask the user to choose between internal source or transport routes.

The numbered workflow immediately below is the existing `oracle_loqate` path.
The creation-only user-data workflow follows it.

### 1. Resolve the Loqate country

Match the trimmed input case-insensitively against
`ora-resource/ora_reference_lookups.md`. Accept either the documented country
name or its two-letter code. Return the documented name and uppercase code.

Stop before Fusion calls when the input is blank, contains more than one
country, is ambiguous, or is unsupported. When country is missing or ambiguous,
ask the user for one supported country name or two-letter code. When it is
unsupported, state that clearly, show close supported matches when available,
and ask the user to select one rather than ending with an unexplained blocker.

### 2. Verify DaaS and Loqate prerequisites

Invoke `core.fusion-api.apps-common` to read the configured `SITE` value for each
exact profile option:

- `ORA_HZ_ENABLE_DAAS_LOQATE`
- `ORA_HZ_DAAS_GEO_ENDPOINT`

Use each profile's `siteProfileOptionValues` child collection under
`profileOptions/{ProfileOptionName}`, request `ProfileOptionValue`, and require
`onlyData=true`. Require exactly one `SITE` record for each code:

```text
/fscmRestApi/resources/11.13.18.05/profileOptions/ORA_HZ_ENABLE_DAAS_LOQATE/child/siteProfileOptionValues
/fscmRestApi/resources/11.13.18.05/profileOptions/ORA_HZ_DAAS_GEO_ENDPOINT/child/siteProfileOptionValues
```

Trim both values. Compare `Y` case-insensitively. Treat any endpoint containing
at least one non-whitespace character as valid; do not compare it with a fixed
URL:

| Profile option | Expected `SITE` value |
|---|---|
| `ORA_HZ_ENABLE_DAAS_LOQATE` | `Y` |
| `ORA_HZ_DAAS_GEO_ENDPOINT` | Any non-null, non-empty value after trimming |

Record each profile validation internally. If the endpoint is missing or blank,
follow the configuration blocker below before preparing a change plan. If
Loqate enablement is missing or different and the endpoint is configured,
prepare a change plan for Loqate enablement only. If
`ORA_HZ_ENABLE_DAAS_LOQATE` is missing or not `Y`, show a line such as
`Loqate enablement: ORA_HZ_ENABLE_DAAS_LOQATE is <current state>; proposed
value: Y. This enables Oracle-licensed geography reference-data import for
<country>.` Do not hide or paraphrase this profile option. Keep the DaaS
endpoint value out of every user-facing response and redacted diagnostic,
including technical-detail requests. Keep REST details internal unless the
user explicitly requests them.

If both values already satisfy their required conditions, this is a pure
no-op profile path: do not call `POST` or `PATCH`, do not ask for confirmation,
and proceed to geography setup after reporting that both values were validated.

If `ORA_HZ_DAAS_GEO_ENDPOINT` is null, empty, whitespace-only, or has no `SITE`
record, tell the user that the site-level DaaS geography endpoint must be
configured in Fusion before a Loqate import can run. Ask them to configure
`ORA_HZ_DAAS_GEO_ENDPOINT`, then stop without changing either profile or
submitting the job. Do not propose a URL or accept a chat value as a substitute
for the configured Fusion value. Re-read the profile when the user resumes.
Preserve every existing nonblank endpoint exactly; never mutate this option.

After the single geography execution confirmation, use
`core.fusion-api.apps-common` to `POST` a missing
`SITE` record or `PATCH` an existing eligible `ORA_HZ_ENABLE_DAAS_LOQATE` item.
Never write `ORA_HZ_DAAS_GEO_ENDPOINT`. Before writing,
require the profile's site level to be enabled and updatable and require the
profile-value management privilege. Never retry a profile mutation
automatically. Read both profiles again after all approved writes and continue only when
`ORA_HZ_ENABLE_DAAS_LOQATE` is Y and `ORA_HZ_DAAS_GEO_ENDPOINT` is nonblank.
Retain each applied technical change in the audit record and summarize it to the
user only as prerequisite setup. If the user declines the single execution
preview, make no profile changes and do not submit the Loqate geography job.
Explain that the user can open **Setup and
Maintenance > Customer Data Management > Enterprise Profile > Manage
Geographies** to define the country structure and master geography hierarchy
manually, then leave the next action to the user.

### 3. Validate the environment

Resolve the target Fusion environment before any side effect. When exactly one
active configured environment is available, use it without asking the user to
repeat it and name it in the brief progress update. Ask one short question only
when the environment is missing or ambiguous, naming the available choices when
safe. Do not perform a separate role or ESS-access preflight check. If Fusion
rejects the authorized ESS submission, classify and report the response as
`authorization_or_privilege` without retrying.

### 4. Prepare the execution internally

Build and validate the fixed ESS request described in
`ora-resource/ora_rest_execution.md`. Do not show the REST path, payload, job
definition, application, parameter names, CLI command, or polling mechanics in
the normal user flow.

Require a live-run `project_id`. Before the ESS POST, create and persist a
unique correlation description using the resolved project, country code, and
run ID. Record the UTC submission-window start. Reserve these task-local paths:

```text
project/{project_id}/artifacts/pillars/cx/customer-data-management/enterprise-profile/manage-geographies/current/ess-submission-checkpoint.json
project/{project_id}/artifacts/pillars/cx/customer-data-management/enterprise-profile/manage-geographies/current/ess-execution-result.json
```

The checkpoint path must be passed to the core ESS process as `--output`; it is
the durable handoff between submission and polling.

Give the user an explanatory business-level update, such as:

> Prerequisite validation is complete for India in the selected Fusion
> environment. I am now submitting Oracle's Import Geography Data process. It
> will define the country geography structure and load the Loqate hierarchy
> master data; it does not configure geocoding or address cleansing.

Do not suppress the two profile validation results, profile changes, geography
structure and hierarchy status, or job ID. Reveal other technical request
details only when the user explicitly asks for a preview, payload, API, ESS
job, troubleshooting details, or audit evidence.

### 5. Build and approve the immutable execution preview

A direct imperative request such as "Set up geographies for India" or "Import
geographies for IN" authorizes validation and preview only. Gather the data,
complete all read-only prerequisite checks, and build the deterministic request
artifact before interrupting the user. Show one concise business preview with
the country, target environment, source, geography scope, creation-only effect,
and any prerequisite business change. When `ORA_HZ_ENABLE_DAAS_LOQATE` is
missing or not `Y`, end with exactly: `Do you want to use Loqate as the source
for geography data? If so, we need to enable ORA_HZ_ENABLE_DAAS_LOQATE by
setting it to Y. Do you want to proceed with enabling it and submitting the
reviewed archive?` Otherwise, ask the standard reviewed-archive
question once. A standalone affirmative reply authorizes the complete previewed
sequence, including eligible prerequisite remediation and one submission;
never ask a second profile, mapping, upload, or submission question.

If the request is advisory, hypothetical, ambiguous about whether to execute,
or does not resolve to one target environment, stop before submission. Ask at
most one short business-level question, without showing technical details.

### 6. Submit and monitor

Invoke the existing ESS skill using the fixed two-phase contract in
`ora-resource/ora_rest_execution.md`:

1. Verify the Task Hook receipt and artifact immediately before invocation,
   then validate the ESS `approved_submission` delegation contract described
   in that resource. Map only its approved request payload and execution options
   into the existing ESS adapter. Submit with `--submit-only` and the durable
   checkpoint path supplied through `--output`.
2. If the process returns a session handle instead of a terminal result, retain
   and poll that same process handle until it exits. Do not treat an empty first
   output chunk as an empty ESS response.
3. Read the checkpoint file and require a positive integer
   `execution_result.requestId`. Persist and report that ID immediately.
4. Start a separate tracking invocation using only `--request-id <captured-id>`,
   the polling options, and the durable execution-result path.

Separating submission from polling prevents a polling authentication refresh,
transport interruption, or output-session handoff from replaying the ESS POST.

Use default `wait_seconds=300` and `poll_interval=10` unless the caller supplies
valid positive values. Larger-country imports can take several hours.

If polling times out, tell the user that setup is still running. Retain the
`requestId`, last status, elapsed wait, and resume instructions internally.
Resume through the ESS skill's existing request-tracking path; do not submit a
second request. Always show the `requestId` as the job ID; show the remaining
mechanics only when the user asks.

If submission output is interrupted, inspect the checkpoint before doing
anything else. When it contains a request ID, continue tracking that request.
When it is missing or unreadable, do not submit again. Run the task-local
read-only recovery query using the exact correlation description, application,
job definition, submission window, and country parameter. Continue only when
exactly one matching request is found; zero or multiple matches are an
`approval_blocker` requiring manual reconciliation.

### 7. Report the outcome and offer another country

On terminal success, give an explanatory business-level confirmation naming
the country and environment. Describe what was checked and why, list both
profile validation results and any changes, identify the job ID, and report
these outcomes:

- `Define Geography Country Structure`: completed
- `Define Geography Hierarchy Master Data`: completed

Do not claim that geocoding or address cleansing was configured. Oracle's
post-import UI verification is the `Structure Defined` and `Hierarchy Defined`
indicators for the selected country.

Use a result format with this level of explanation:

> Geography setup completed successfully for `<country>` in `<environment>`.
>
> **Prerequisite validation**
>
> - `ORA_HZ_ENABLE_DAAS_LOQATE`: `<validated value and whether it was already
>   set or changed>` — this enables Oracle's Loqate geography import.
> - `ORA_HZ_DAAS_GEO_ENDPOINT`: validated as configured; its value is omitted
>   from the result.
>
> **Import result**
>
> - Job ID: `<requestId>`
> - Define Geography Country Structure: completed. The country now has the
>   structural geography levels used by master geographies.
> - Define Geography Hierarchy Master Data: completed. The supported Loqate
>   geography hierarchy was loaded for the country.
>
> This run did not configure geocoding or address cleansing; those are separate
> setup activities. In Manage Geographies, `Structure Defined` and `Hierarchy
> Defined` should now be selected for the country.

End every terminal success response with:

> Do you want to set up geographies for another country? If yes, provide one
> supported country name or two-letter country code.

When the user supplies a country, start a fresh run for that one country. Reuse
the already resolved environment only when it remains unambiguous, but always
repeat the country support check and both profile reads. Do not assume that the
previous job authorizes another submission. The new country reply is a direct
setup instruction for one new run; persist a new run ID, correlation
description, checkpoint, and job ID. Continue offering another country after
each successful run until the user declines or stops.

If the ESS process ends unsuccessfully but its safe error message, status
description, or process log unambiguously says that the selected country's
geography data already exists or was already imported, handle it as an
informational already-present outcome instead of a generic failure. Say:

> Geography data for `<country>` is already present in `<environment>`; Oracle
> reports that it was previously imported, so no new geography import was
> performed. Job ID: `<requestId>`.
>
> Do you want to set up geographies for another country? If yes, provide one
> supported country name or two-letter country code.

Do not claim that this run created or changed the country structure or
hierarchy. Do not recommend retrying the same country. Preserve the original
terminal status and safe diagnostic in project artifacts, but allow a supplied
next country to start the same fresh one-country flow used after success. Apply
this special handling only when the existing/already-imported condition is
unambiguous; otherwise follow the normal terminal-failure behavior below.

On terminal failure, state that geography setup did not complete, include the
job ID when submission occurred, summarize profile changes already completed,
identify the failed stage, provide a safe Fusion error summary, and give the
recommended next step. Apply the same proactive disclosure when a country or
profile lookup, profile write or verification, ESS submission, or polling call
fails. Never return only an internal failure classification or silently stop.
When recovery requires information only the user can provide, ask one focused
follow-up question—for example, which environment to use, whether access has
been restored, or whether they want to retry a read-only lookup. Do not ask for
credentials, tokens, or other secrets in chat.
Keep full status payloads, ECIDs, API paths, credentials, and other sensitive
implementation details internal unless the user asks for technical or
troubleshooting information. Require a new direct setup instruction before any
new ESS submission.

### User-provided creation-only workflow

Use this path only when `geography_source=user_provided`. It supports creating a
country structure, creating hierarchy geographies beneath an existing or newly
created structure, and adding explicitly requested alternate names or codes.
It does not update, delete, replace, or merge existing structures or geography
records.

#### 0. Resolve the execution phase

Resolve exactly one `execution_phase`:

- `mapping_only`: prepare the mapping or mappings selected by
  `requested_scope`, then stop after reporting that reusable import preparation
  is ready. Retain `MappingNumber` values internally.
  Do not require country data, generate a CSV, upload to UCM, create an import
  activity, or poll a job.
- `full_import`: render the reviewed mapping definitions as mapping CSVs and
  pass each stage to native Data Loader preflight, approval, upload, and initiation.
  Stop after initiation; check status only when the user explicitly requests it.

A direct request to prepare or register mappings selects `mapping_only`. A
request containing geography rows or asking to create the hierarchy selects
`full_import`. Resolve this internally, show the resulting business operation
in the one preview, and require one standalone affirmative reply before a
mapping POST or import. Do not ask the user to choose a phase or mapping route.

#### 1. Collect the requested scope and canonical model

Resolve exactly one `requested_scope`:

- `structure_only`
- `hierarchy_only`
- `structure_and_hierarchy`

For `mapping_only`, use the scope only to select the structure mapping, the
hierarchy mapping, or both. Skip the remaining canonical country and file model
in this subsection.

Accept a local CSV, an ordered list/table, or a hierarchy tree. Normalize it to
one internal model before forming files or payloads:

When the user asks the skill to create, source, or suggest the hierarchy, gather
the requested geography names and codes from the current approved country
reference source before preview. If the user requests a sample count such as
four states, select that many valid entries deterministically in alphabetical
order unless the request names them. Do not ask the user to prepare a CSV or
supply technical import data. Retain source citations in the audit artifact and
show the selected business names in the one confirmation preview. Never invent
real geographies for a live import; if authoritative data cannot be resolved,
stop with a business-data readiness message.

```yaml
country:
  code: AU
  name: Australia
structure:
  - level_number: 1
    geography_type: COUNTRY
  - level_number: 2
    geography_type: STATE
hierarchy:
  - source_id: "1"
    parent_source_id: null
    level_number: 1
    geography_type: COUNTRY
    primary_name: Australia
    record_type_code: 0
  - source_id: "2"
    parent_source_id: "1"
    level_number: 2
    geography_type: STATE
    primary_name: New State
    record_type_code: 1
```

When Source IDs are not supplied, assign deterministic positive integer strings
within the generated file, starting at `1` for the country anchor and traversing
parents before children. Do not reuse a generated Source ID for two primary
geographies. An alternate identifier row intentionally reuses its primary
geography's Source ID and Parent Source ID.

For `hierarchy_only`, require either a validated description of the existing
country structure or a reliable read-only result showing its levels. Use that
structure only for validation and do not import it. If the existing structure
cannot be established, stop rather than infer it.

#### 2. Validate the structure

The generated or supplied Country Structure data must use exactly these
columns:

```text
CountryCode,LevelNumber,GeographyType
```

Require all of the following:

1. Every row has the same explicit or locally resolved ISO two-letter country
   code. Do not call Fusion to preflight the country for a structure import.
2. Level 1 exists exactly once and has `GeographyType=COUNTRY`.
3. Level numbers are positive, unique, contiguous, and ordered from 1 through
   the lowest requested level.
4. Each geography type is nonblank and appears at only one level.
5. Normalize display labels to the canonical import code shown in the preview
   by trimming, uppercasing, and replacing internal spaces or hyphens with
   underscores (for example, `Postal Code` becomes `POSTAL_CODE`). Do not call
   Fusion metadata or lookup APIs to preflight geography types.
6. Use the creation-only import result as the authoritative target validation.
   If Fusion reports an invalid country/type or an existing country structure,
   preserve and report that diagnostic; do not delete, replace, retry, or append
   lower levels.

#### 3. Validate the hierarchy

Use this canonical column order when generating a Geography import file:

```text
GeographyIdentifierId,PrimaryGeographyCodeType,PrimaryGeographyName,RecordTypeCode,SourceId,StartDate,ParentGeographyType,CountryCode,EndDate,GeographyId,GeographyType,GeoDataProvider,IdentifierSubtype,IdentifierType,IdentifierValue,LanguageCode,LevelNumber,ParentSourceId,PrimaryGeographyCode
```

Require all of the following before side effects:

1. `CountryCode`, `PrimaryGeographyName`, `RecordTypeCode`, `SourceId`, and
   `LevelNumber` are present on every primary or anchor row. The country anchor
   has a blank `ParentSourceId`; every lower primary row has one.
2. Exactly one level-1 country anchor uses `RecordTypeCode=0`, has the resolved
   country name and code, and has no alternate identifier row.
3. A primary geography to create uses `RecordTypeCode=1`. Its level exists in
   the validated structure, its `GeographyType` matches that level, and its
   parent is present earlier in the same file.
4. Every child includes the complete parent chain needed by Oracle's Geography
   import. `ParentGeographyType`, when supplied, matches the parent's type.
5. Source IDs are unique across primary and anchor rows. Each
   `RecordTypeCode=2` alternate-name or alternate-code row is explicitly
   requested, is below country level, and reuses the exact Source ID, Parent
   Source ID, level, and primary geography name of one preceding primary row.
6. `IdentifierType`, `IdentifierSubtype`, and `IdentifierValue` are supplied
   together for type-2 rows and use current target-pod lookup values. Reject an
   alternate name already known to identify another geography.
7. `PrimaryGeographyCodeType` and `PrimaryGeographyCode` are both supplied on
   the type-1 row or both omitted; do not try to add them in a later import.
8. Reject any row or option that represents update, upsert, deletion, or a
   provider-specific unsupported identifier. Do not default `GeoDataProvider`
   to `LOQATE`; preserve it only when the user identifies the data provider and
   the target import object accepts that value.
9. Preserve user-provided names, identifier values, and language codes exactly
   after CSV parsing. Report validation errors rather than silently changing
   their semantics.

#### 4. Prepare the stage-specific Data Loader CX import

For full_import, use the [native execution contract](ora-resource/ora_rest_execution.md#native-data-loader-cx-import).
Generate one mapping CSV and one canonical data CSV per stage using a UTF-8 CSV
writer. Render all reviewed column pairs from
`references/import-mapping-definitions.json`; preserve names and identifiers
exactly. Keep request models, validation JSON, and audit manifests outside the
CX ZIP. Data Loader accepts CSV members only, with at most one mapping and at
least one data file. Never combine the structure and hierarchy objects into
one CX group. Use Data Loader's preflight envelope, exact retained ZIP, and
Task Hook validation against those final bytes before presenting approval.

For mapping_only, retain the exact technical mapping preview and the existing
Task Hook approval lifecycle. No data CSV, UCM upload, or initiation is required.

#### 5. Mapping-only preparation through the authorized REST core service

This subsection applies only to `mapping_only`. Full imports skip every mapping
GET/POST here and supply mapping CSVs to Data Loader instead.

The underlying Fusion resource is
`/crmRestApi/resources/11.13.18.05/importMappings`. Complete mandatory
`core.data-loader` task validation before using
`core.fusion-api.rest-api-client` with `REST-Framework-Version: 9` for read-only
mapping resolution. Finish this lookup before the user preview. Require the
single approval and artifact verification only before a missing mapping POST.
If Data Loader cannot authorize the central service, persist the internal
diagnostic and stop without exposing mapping mechanics.

For each selected mapping, in structure-then-hierarchy order:

1. Before confirmation, through the Data Loader-validated REST core service,
   GET the collection
   using the exact stable `Name` and `ObjectCode` query and expand all
   `ImportMappingColumns`; when needed, GET
   `/importMappings/{MappingNumber}/child/ImportMappingColumns`.
2. If exactly one result has the same object code and every exact
   `ColumnHeader`/`AttributeCode` pair with no duplicates or extras, reproject
   the response into the task-defined order and reuse its `MappingNumber`. Do
   not treat REST collection return order alone as drift.
3. If no result exists, verify the immutable approval again, obtain the
   configured access token through shared auth in memory, and use the authorized
   REST core service for one POST containing
   `Name`, `Description`, `ObjectCode`, and the complete nested
   `ImportMappingColumns` array. Require one nonblank `MappingNumber` in the
   response. Send `REST-Framework-Version: 9`; passing the token explicitly to
   the core call prevents its cache-refresh path from replaying the POST. Never
   print or persist that token.
4. If multiple results exist, or the one result has missing, extra, duplicate,
   or changed column pairs, stop as `catalog_or_metadata_mismatch`. Never PATCH,
   DELETE, overwrite, or silently version a mapping.
5. Persist the environment, stable name, object code, fingerprint,
   `MappingNumber`, outcome (`reused` or `created`), and redacted response
   reference before continuing.

Mapping creation is a live POST. Do not retry an uncertain result. Reconcile it
through the same exact Data Loader-authorized REST-service GET; continue only if exactly one
matching mapping is found. For `mapping_only`, report the selected mapping
results and stop here.

#### 6. Validate and submit through native Data Loader

Follow [Native Data Loader CX Import](ora-resource/ora_rest_execution.md#native-data-loader-cx-import)
for the exact preflight and approved commands. The helper owns account lookup,
immutable artifact retention, CRM upload, mapping-ID prefixing, and initiation.
Do not call `cx_import_export_job.py`, uploadFileToUCM, or importActivities.
Retain task validation and the saved preflight envelope until submission; the
approved command accepts no sources or CX routing overrides.

For structure_only, submit one structure load. For hierarchy_only, first require
compatible existing structure context, then submit one hierarchy load. For
structure_and_hierarchy, submit structure and leave hierarchy pending until an
explicit status request confirms successful completion without rejected rows.
Prepare a fresh hierarchy envelope and obtain its own stage approval at that
point. Submission does not demonstrate completion and does not authorize polling.

#### 7. Report initiation and requested status

Return Data Loader's `Data Load In Progress` result with Data Set Name, Load Type
(`Data Loader - CX Import`), Business Object Name, UCM Account, Content ID, and
Request ID. Do not claim Structure Defined or Hierarchy Defined at initiation.
Explain a pending hierarchy stage briefly when both were requested.

Use `core.data-loader` status guidance only when the user explicitly asks for
status, progress, results, counts, or errors. A successful structure status may
unlock the hierarchy preflight, but cannot approve that later load. Report stage
results independently and preserve structure success if hierarchy fails. Give
the Manage Geographies UI verification path for Structure Defined and Hierarchy
Defined; do not claim geocoding or address-cleansing setup.

## CSV and Bulk Boundary

The effective catalog marks both export/import and CSV export/import as `N`.
Those flags prohibit FSM setup export/import routing; they do not prohibit the
documented CX Import Management Country Structure and Geography objects.

For `oracle_loqate`, continue to reject CSV, spreadsheet, array, and
multi-country inputs. For `user_provided`, accept one-country CSV, table, tree,
or structured data and route full_import only through native `core.data-loader`;
retain the authorized REST core route solely for mapping_only. Reject files containing multiple
countries and never combine sequential countries into one import activity.

## Persistence

For full_import, retain prepared geography CSVs and business validation under
the project workspace before submission, and record the prescribed token usage.
Let Data Loader manage its internal envelopes and immutable artifacts: remove
internal preflight and Task Hook envelopes after accepted initiation, retain
them after partial/uncertain failure, and do not generate an additional local
submission report or run log. The following durable execution records apply to
Loqate and mapping_only, not native CX initiation:


When `project_id` is supplied, persist:

- the resolved source mode, execution phase, and requested scope, plus the
  canonical one-country request only for Loqate or full_import;
- the resolved execution phase and Data Loader import-authorization result;
- the immutable approval artifact SHA-256 and verified Task Hook receipt;
- each exact mapping preview, fingerprint, stable name, object code,
  `MappingNumber`, and `created` or `reused` outcome;
- user-provided source references, generated CSVs, checksums, local validation
  results, redacted payload previews, and exact execution approval when the
  user-data branch is selected;
- each UCM document name, Import Management activity ID, terminal or last-known
  status, record counters, report content IDs, and partial-success errors;
- validation and prerequisite results;
- the proposed, approved, and applied profile changes, including before and
  after values but excluding credentials and tokens;
- the internally validated request record, redacted from user-facing output;
- the unique ESS correlation description and submission window;
- the submission checkpoint written before polling begins;
- ESS request ID and terminal or last-known status;
- redacted diagnostics;
- a skill-run record; and
- the required token-usage record.

Use the manifest paths and register durable artifacts. Never persist
credentials, bearer tokens, token-cache contents, private keys, or sensitive
payloads.

## Error and Retry Policy

- Authenticate automatically through the configured Fusion authentication
  flow. Do not ask for permission before authentication or token refresh.
- Allow one cache-managed token refresh retry for a read-only GET that returns
  `401` or `403`.
- If automatic authentication or refresh still fails, report the safe error and
  recovery action; do not request credentials or tokens in chat.
- Do not retry an explicit access token silently.
- Do not retry profile-value `POST` or `PATCH` mutations automatically.
- Do not retry the live ESS `POST` automatically.
- Do not refresh and replay any mapping, upload, import-activity, profile, or
  ESS POST after `401` or `403`; report `auth/authz` with an uncertain mutation
  outcome when the request may have reached Fusion.
- Do not retry a user-data UCM upload or Import Management activity creation
  automatically. A lost or uncertain response is an `approval_blocker` until
  the uploaded document or activity is reconciled.
- Do not retry a Data Loader-authorized mapping POST automatically. Reconcile only
  through the exact authorized REST-service read using the stable name and object
  code. Zero, multiple, or drifted matches remain blocked.
- Retry a mapping lookup only when it is read-only and the failure is a bounded
  recoverable transport error or a cache-managed authentication refresh.
- For full_import, use Data Loader status only on an explicit status request.
  Its documented one-time initiation HTTP 400/action 27503 compatibility retry
  may omit Run Book fields while preserving content IDs and all CX fields;
  never reupload. No other upload or initiation replay is authorized.
- If structure completed and hierarchy failed, classify the run as partial
  `process_failed`, preserve the structure result, include an `errors` array,
  and do not roll back or automatically retry hierarchy.
- Never place live submission and polling in the same core ESS invocation.
- On interrupted or empty command output, inspect the durable submission
  checkpoint and then use read-only recovery; do not infer that Fusion failed.
- A polling authentication refresh may retry only the GET for the captured
  request ID; it must never replay the POST.
- On `process_timeout`, resume the same request ID.
- On `process_failed`, preserve diagnostics and require a new direct user
  instruction before another submission. When the process unambiguously says
  the geography data already exists or was already imported, the next-country
  prompt is allowed and the user's country reply is that new direct instruction.
- Classify failures using `governance/error-handling-guidelines.md`.

## Refusal Rules

For native full_import, core.data-loader's current approval, account disclosure,
artifact, and requested-status policies govern; references below to mapping
POSTs apply only to mapping_only, and ESS gates apply only to Loqate.

- Do not infer or substitute an unsupported Loqate country or an unverified
  user-data country code.
- On the Loqate branch, update `ORA_HZ_ENABLE_DAAS_LOQATE` only when the single
  business preview explicitly included its required change and received
  standalone execution confirmation.
- Never create or update `ORA_HZ_DAAS_GEO_ENDPOINT` through this skill. When it
  is missing or blank, ask the user to configure it and stop before import.
- Do not update `ORA_HZ_ENABLE_DAAS_LOQATE` from a missing or non-Y value unless
  the preview displayed that exact profile option and proposed `Y`, asked whether
  the user wants Loqate to supply the geography data, explained that this
  requires enabling the profile option, and received a standalone
  affirmative reply.
- On the Loqate branch, do not submit until both profiles have been re-read and verified after any
  approved changes.
- Do not submit without clear execution intent for the exact country and
  environment.
- Do not treat the initial execution request as approval of a Data Loader
  preview. For Loqate and mapping_only require a standalone affirmative reply;
  full_import follows core.data-loader's exact-load approval and auto-approval policy.
- Do not resubmit when the first request outcome is unknown.
- Do not delete or replace existing geography data.
- Do not import a structure over an existing structure or add lower structure
  levels through Country Structure import.
- Do not call a geography-structure, product-catalog, or Manage Geographies API
  as a prerequisite for user-provided structure creation. The sole object
  preflight is the required CX `objectMetadata/<ObjectCode>` UCM-account lookup.
- Do not generate update, upsert, or delete semantics for user-provided data.
- Do not accept caller-supplied import-mapping names, object codes, column
  pairs, mapping numbers, or Data Loader authorization overrides.
- Do not create or read a Fusion import mapping before `core.data-loader`
  authorizes the central REST service.
- Do not PATCH, DELETE, overwrite, or silently replace an existing mapping that
  differs from the reviewed task-owned definition.
- Do not accept a hierarchy child without its complete in-file parent chain.
- Do not start hierarchy import before a requested structure import completes
  without errors.
- Do not report success before a terminal successful ESS or Import Management
  status, as applicable.

## Golden Scenarios

| Scenario | Expected Result |
|---|---|
| User says "Set up geographies for India" and both profiles pass | Resolve IN, gather and validate the data and prerequisites internally, display one concise business preview without transport or metadata detail, ask the standard reviewed-archive question once, and after a standalone affirmative submit once and report the business outcome |
| ORA_HZ_ENABLE_DAAS_LOQATE is Y and ORA_HZ_DAAS_GEO_ENDPOINT is nonblank | Report both as validated, make no profile writes, ask no profile-change confirmation, and continue |
| Authentication is required or the cache-managed session expired | Start or refresh the configured authentication flow automatically without asking permission, then continue the interrupted read-only operation once |
| Country is us | Normalize to United States and US |
| Country is unsupported | Stop before Fusion execution and show supported or close values |
| Country is missing or ambiguous | Ask one concise question for a supported country name or two-letter code |
| Environment is missing or ambiguous | Ask which Fusion environment to use and show safe available choices when known |
| Country or profile lookup fails | State which lookup failed, provide a safe error summary and next action, and do not continue silently |
| Site-level ORA_HZ_ENABLE_DAAS_LOQATE is missing or not Y | Show `ORA_HZ_ENABLE_DAAS_LOQATE`, its safe current state, and proposed `Y`; explicitly ask whether the user wants Loqate as the source for geography data and explain that doing so requires enabling the profile option; only after a standalone affirmative change it to Y, re-read it, and continue without another prompt |
| Site-level ORA_HZ_DAAS_GEO_ENDPOINT is null, empty, whitespace-only, or missing | Ask the user to configure the site-level profile value in Fusion; make no profile change or import submission, then re-read it when the user resumes |
| Site-level ORA_HZ_DAAS_GEO_ENDPOINT contains any nonblank URL or value | Accept and preserve it exactly, report it as validated, do not include it in the change plan, and never write to it |
| Both profiles require changes | Ask the user to configure the endpoint first and stop; after a later read verifies it, show the `ORA_HZ_ENABLE_DAAS_LOQATE` current-to-Y decision in the execution preview |
| User declines the execution preview | Make no prerequisite changes, do not submit the geography job, and explain the manual Manage Geographies path |
| ESS succeeds | Verbosely report both structure and hierarchy outcomes as completed, include the job ID, and ask whether to set up another country |
| ESS reports that geography data already exists or was already imported | State that the country data is already present and no new import was performed, include the job ID, do not recommend retrying that country, and ask whether to set up another country |
| User supplies another country after success | Start a fresh single-country run, repeat all validation and profile reads, create a new durable execution identity, and submit at most one separately authorized job |
| Submission process yields an empty initial output chunk | Retain and poll the same process handle, then read the durable checkpoint; do not classify the ESS response as empty |
| Submission output is lost but the checkpoint exists | Read and persist its requestId, report the job ID, and track that request with a separate `--request-id` invocation |
| Submission output and checkpoint are both unavailable | Perform one read-only exact-correlation recovery query; continue only for exactly one match and never submit again automatically |
| Polling receives a cache-managed 401/403 | Refresh authentication once and resume GET tracking for the captured requestId; never repeat the POST |
| ESS polling times out | Report that setup is still running, include the job ID, and resume tracking internally without resubmitting |
| ESS fails | Include the job ID and completed profile-change summary, return a concise business-level failure and recommended action, and require a new direct instruction before resubmission |
| ESS submission or polling request fails | State the failed stage, safe Fusion error summary, job ID when assigned, and recommended next action; do not retry a mutation automatically |
| User supplies or requests an ordered AU structure with direct import intent | Resolve AU and validate levels locally; render reviewed mapping/data CSVs, return native stage preflight plus Task Hook approval, then initiate one Data Loader CX Import and stop |
| User supplies a hierarchy tree | Assign deterministic parent-first Source IDs when absent, generate required anchor/create rows, validate the full parent chain, and preview `GeographyInterface` |
| User supplies compatible structure and hierarchy CSV files | Parse both files, require one matching country and consistent levels, preserve semantic values, and produce redacted previews without uploading |
| User asks to prepare both Manage Geographies mappings | Resolve `mapping_only` plus `structure_and_hierarchy`, preview both stable definitions, complete Data Loader validation and authorization, reuse exact matches or create missing mappings through the authorized REST core service in structure-then-hierarchy order, persist both MappingNumber values, and perform no UCM upload or import activity |
| Mapping-only request has no country or CSV | Continue because mappings are reusable and not country-specific; still require exact environment, project persistence, preview authorization, requested scope, and Data Loader authorization |
| Data Loader cannot authorize the REST core service | Persist the complete mapping preview, stop as approval_blocker, and report the failed authorization gate; never implement task-local Fusion REST transport |
| One exact stable mapping already exists | Compare every reviewed column pair, persist its MappingNumber as reused, and continue without a POST |
| Mapping lookup returns duplicates or column drift | Stop as catalog_or_metadata_mismatch; do not select, patch, delete, overwrite, or create another similarly named mapping |
| Mapping POST response is uncertain | Perform only an exact reconciliation lookup through the Data Loader-authorized REST core service; never repeat the POST automatically |
| User requests structure and hierarchy live | Initiate the approved structure load and leave hierarchy pending. On explicit status request confirming success, prepare and obtain approval for the separate hierarchy load |
| Country structure already exists | Let the creation-only import activity report it, then stop the structure stage as already present; do not delete, replace, extend, retry, or continue to hierarchy unless a separate hierarchy-only request establishes compatibility |
| Hierarchy-only request lacks a verified existing structure | Stop before upload and ask for the structure definition or a reliable read-only verification result |
| Hierarchy row requests an update or deletion | Reject as input validation before generating a live payload |
| Type-2 alternate identifier row targets the country or lacks a matching primary row | Reject before upload; type 2 is additive only below country level and must reuse the primary row's source relationship |
| User omits an import-file destination | Let native Data Loader resolve and normalize exact-object UcmAccount before approval; include its required disclosure and never refresh it after approval |
| The internal import destination is missing or ambiguous | Stop before confirmation or upload, persist technical diagnostics, and give only a business-level readiness message unless technical details are requested |
| Internal file staging returns an ID that cannot be resolved to the required document name | Native CRM upload must return dDocName; retain partial IDs and stop before initiation when it is missing |
| Structure import succeeds and hierarchy import fails | Report partial failure, preserve the completed structure and both diagnostics, and do not roll back or retry automatically |
| User-data import polling times out | Only a requested status check can time out; retain the same data set and RequestId, leave hierarchy pending, and never reinitiate |

## Source Boundaries

- Supported countries:
  `https://docs.oracle.com/en/cloud/saas/customer-data-management/faicd/list-of-available-countries-with-loqate-geography-reference-data.html`
- Geography profile options:
  `https://docs.oracle.com/en/cloud/saas/customer-data-management/faicd/geography-profile-options.html`
- Site-level profile option REST contract:
  `core/fusion-api/apps-common/references/profile-options.md`
- Oracle-licensed geography import:
  `https://docs.oracle.com/en/cloud/saas/customer-data-management/fageo/import-geography-reference-data-licensed-by-oracle.html`
- User-provided Country Structure import:
  `https://docs.oracle.com/en/cloud/saas/customer-data-management/faicd/import-your-country-structure-data.html`
- Country Structure import example:
  `https://docs.oracle.com/en/cloud/saas/customer-data-management/faicd/example-of-importing-country-structure-data.html`
- User-provided Geography import:
  `https://docs.oracle.com/en/cloud/saas/customer-data-management/faicd/import-your-geography-data.html`
- Geography import example:
  `https://docs.oracle.com/en/cloud/saas/customer-data-management/faicd/example-of-importing-geography-data.html`
- CX import-file staging execution contract:
  `core/data-loader/SKILL.md`
- Fusion REST execution contract:
  `core/fusion-api/rest-api-client/SKILL.md`
- Task-owned import mapping definitions:
  `references/import-mapping-definitions.json`
- Import Mapping collection REST contract, invoked by the Data Loader-authorized REST core service:
  `https://docs.oracle.com/en/cloud/saas/sales/faaps/op-importmappings-get.html`
- Create Import Mapping REST contract, invoked by the Data Loader-authorized REST core service:
  `https://docs.oracle.com/en/cloud/saas/sales/faaps/op-importmappings-post.html`
- Import Mapping Columns REST contract, invoked by the Data Loader-authorized REST core service:
  `https://docs.oracle.com/en/cloud/saas/sales/faaps/op-importmappings-mappingnumber-child-importmappingcolumns-get.html`
- Import activity REST contract, owned by the core skill:
  `https://docs.oracle.com/en/cloud/saas/sales/faaps/op-importactivities-post.html`
- Manual geography overview:
  `https://docs.oracle.com/en/cloud/saas/financials/26c/faigl/overview-of-geographies.html`
- Scheduler REST contract:
  `https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-ess-rest-scheduler-v1-requests-post.html`
- Effective task catalog:
  `knowledge/setup-task-catalog/effective/setupTasksAll.json`

Use the parent skill
`cx.customer-data-management.enterprise-profile` for functional-area scope and
sequencing.

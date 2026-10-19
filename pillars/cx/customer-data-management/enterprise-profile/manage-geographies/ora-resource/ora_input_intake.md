# Input Intake

## Execution phase boundary

`full_import` uses only the native `core.data-loader` CX Import handoff in
[REST execution](ora_rest_execution.md#native-data-loader-cx-import). Its stage
mapping CSV replaces direct mapping lookup/create and MappingNumber requirements.
Its retained preflight envelope replaces direct UCM/import-activity payloads.
Return the loader's required preview/result fields, check status only on explicit
request, and use a fresh approved hierarchy load after confirmed structure success.
REST mapping lookup/create, reuse/drift rules, and mapping IDs below apply only
to `mapping_only`. Loqate ESS behavior remains under its own execution contract.

## Accepted Input Formats

| Input Format | What Must Be Provided | Applies To |
|---|---|---|
| Country name | One country name; Loqate requests resolve it against the Oracle Loqate list and user-data structure requests resolve it locally to an ISO two-letter code | Interactive requests |
| Country code | One two-letter code; Loqate requests require a documented Loqate code and user-data structure requests use the explicit ISO code without a Fusion preflight API | Interactive requests and structured callers |
| Structured request | country, optional fusion_environment_context when it cannot be resolved from one active configured environment, project_id for live execution, and optional wait_seconds and poll_interval | Automated orchestration |
| User-provided structure | One country plus an ordered list/table or CSV containing CountryCode, LevelNumber, and GeographyType | Creation-only Country Structure import |
| User-provided hierarchy | One country plus a parent-child tree/table or compatible Geography import CSV | Creation-only Geography hierarchy import |
| Agent-sourced hierarchy | One country, requested geography level, and optional sample count or named entries | Gather current valid names/codes from an approved country reference, select a requested sample deterministically, and form the hierarchy without asking the user for CSV or import mechanics |
| Combined user request | One country plus both structure and hierarchy definitions or CSV files | Sequential structure-then-hierarchy Import Management execution |
| Mapping preparation request | `execution_phase=mapping_only`, one requested scope, exact target environment, project_id, and direct mapping-preparation intent; country and CSV data are not required | Data Loader-authorized creation or reuse of the stable Manage Geographies import mappings without UCM upload or import activity |

## Dependency Inputs

| Field | Mandatory | Purpose | Send in Request Body? | Lookup Rule |
|---|---|---|---|---|
| country | Conditional | Resolve one country name/code for Loqate or a full user-data import; omit for mapping_only | Loqate only, after resolution as submit.argument1; full user data places the code in generated CSV | Use the source-specific country resolver in ora_reference_lookups.md; do not request a country for mapping_only |
| fusion_environment_context | Conditional | Identify the exact Fusion environment used for profile reads and ESS execution | No | Use the sole active configured environment when unambiguous; otherwise ask for the target environment before any live action |
| project_id | Yes for live execution | Persist the pre-submit correlation record, submission checkpoint, request ID, execution result, diagnostics, skill run, and token usage | No | Require a safe `project/{project_id}` workspace before the ESS POST |
| wait_seconds | No | Bound ESS polling | No | Use the standard default when omitted |
| poll_interval | No | Control the interval between ESS status reads | No | Use the standard default when omitted |
| execution_intent | Yes for live execution | Authorize validation and immutable preview generation for one Loqate ESS submission, mapping operation, or user-data import in the resolved environment | No | Every initial imperative stops at the current Data Loader preview; require a standalone affirmative reply before the first POST |
| task_context and task_sequence | Yes for live execution | Select the exact Data Loader Task Hook route | No | Resolve from the active implementation plan; stop if the task identity or sequence is missing or inconsistent |
| execution_confirmation | Yes before mutation | Authorize the exact business preview, including any eligible prerequisite remediation and all requested geography stages | No | Ask once after data gathering and internal preflight; when `ORA_HZ_ENABLE_DAAS_LOQATE` is not Y, show that profile option and proposed Y, ask whether the user wants Loqate as the source for geography data, and explain that doing so requires enabling the profile option; the standalone affirmative reply covers the complete unchanged business preview |
| geography_source | Internal | Resolve `oracle_loqate` or `user_provided` before source-specific validation | No | Select Loqate for standard supported-country setup without custom data; select user-provided for supplied, requested, or gathered custom data; never ask the user to choose a technical source route |
| execution_phase | Conditional | Select `mapping_only` or `full_import` | No | Required for `user_provided`; infer mapping_only only from an explicit mapping preparation/registration request and otherwise use full_import when geography data is supplied |
| requested_scope | Conditional | Select `structure_only`, `hierarchy_only`, or `structure_and_hierarchy`; during mapping_only it selects the mapping set | No | Required for `user_provided`; infer only when the supplied request or artifacts make exactly one scope clear |
| structure_definition_or_csv | Conditional | Supply ordered structure levels or the local Country Structure CSV | No | Required when user-provided scope includes structure; hierarchy-only may supply a structure model for validation without importing it |
| hierarchy_definition_or_csv | Conditional | Supply hierarchy nodes, identifiers, or the local Geography CSV | No | Required when user-provided scope includes hierarchy |
| ucm_account_resolution | Internal | Helper resolves the stage-specific account during preflight | No | Retain native Data Loader normalized account in the envelope, return its required disclosure, reject overrides, and never requery it after approval |
| import_mapping_definition | Internal | Select the reviewed stable mapping name, object code, and ordered column pairs | No | Load only `references/import-mapping-definitions.json`; never accept caller overrides |
| data_loader_import_authorization | Internal | Complete Task Hook validation, immutable preview, standalone approval, archive verification, and receipt persistence before invoking a mutating central service | No | Resolve through `core.data-loader.task-hook`; if authorization fails, retain the preview and stop without task-local REST fallback |

## Body Field Rules

| Situation | What Happens |
|---|---|
| Loqate country is provided as a supported name | Resolve its two-letter code and use only that code as submit.argument1 |
| Country is provided as a supported code | Trim whitespace and normalize only surrounding whitespace and code casing; preserve geography names and identifiers |
| More than one country is provided | Reject the request and require one country per skill run |
| Country is unsupported | Stop before profile reads and ESS submission, explain that it is unsupported, show close supported matches when available, and ask the user to choose one |
| Country is missing or ambiguous | Ask one concise source-aware question for a country name and two-letter code; never infer the answer |
| Fusion environment is missing or ambiguous | Ask which target environment to use and include safe configured choices when available |
| Live execution has no project_id | Stop before ESS submission and initialize or select a safe project workspace; the request ID checkpoint may not rely on chat or process output alone |
| Profile option values are supplied by the user | Do not trust them as proof; read the configured `SITE` values through core.fusion-api.apps-common |
| ORA_HZ_ENABLE_DAAS_LOQATE is missing or not Y | In the single business preview, show `ORA_HZ_ENABLE_DAAS_LOQATE`, its safe current state, and proposed `Y`, ask whether the user wants Loqate as the source for geography data, and explain that doing so requires enabling the profile option; do not split this into separate source, profile, and submission prompts |
| ORA_HZ_DAAS_GEO_ENDPOINT is missing or blank | Ask the user to configure its `SITE` value in Fusion; stop before the reviewed-archive preview and re-read and verify it when the user resumes; never display or propose an endpoint value |
| Both configured profile values match the expected conditions | Explain that Loqate import prerequisites are already ready, make no profile write, ask no Loqate/profile question, and continue |
| User supplies another country after a successful run | Start a new single-country run with fresh country and profile validation; never combine countries into one request |
| A caller supplies an ESS request body | Ignore unapproved extra fields and construct the request from the fixed job definition, application, and resolved country code |
| A caller requests combined submit-and-poll execution | Split it into submit-only with durable output, followed by request-ID-only tracking |
| User supplies custom geography data | Select `user_provided`; do not run Loqate profile reads or the Loqate ESS job |
| User explicitly asks to prepare or register mappings | Select `user_provided` plus `mapping_only`; require scope, environment, project_id, exact preview, and Data Loader authorization, but do not request country or CSV data |
| User provides inline structure or hierarchy | Normalize it to a canonical one-country model, validate it, then render deterministic CSV before any upload |
| User directly requests a user-provided structure import | Gather and validate geography rows, render the reviewed mapping CSV, and use native Data Loader stage preflight and approval before initiation; stop after the Data Load In Progress result |
| User provides local CSV files | Parse and validate the exact file contents; never treat the path alone as proof that the file is compatible |
| User requests both custom stages | Preview both, then execute structure first and hierarchy only after structure completes without errors |
| User requests hierarchy only | Require a validated existing structure definition or reliable read-only structure result; do not infer levels |
| User-data live execution has no caller-supplied import destination | Resolve and validate it internally before the preview; do not ask the user, render the resolver, or use a fallback |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GEO.COLLECT | step | 1 | collect_input | ok->GEO.VALIDATE;failure->GEO.FAILED | none | stop | Collect source, execution phase, requested scope, environment, project identity, and source-specific country or data inputs for every Manage Geographies request |

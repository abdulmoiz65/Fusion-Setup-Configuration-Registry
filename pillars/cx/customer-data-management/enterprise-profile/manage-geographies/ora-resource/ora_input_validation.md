# Input Validation

## Execution phase boundary

`full_import` uses only the native `core.data-loader` CX Import handoff in
[REST execution](ora_rest_execution.md#native-data-loader-cx-import). Its stage
mapping CSV replaces direct mapping lookup/create and MappingNumber requirements.
Its retained preflight envelope replaces direct UCM/import-activity payloads.
Return the loader's required preview/result fields, check status only on explicit
request, and use a fresh approved hierarchy load after confirmed structure success.
REST mapping lookup/create, reuse/drift rules, and mapping IDs below apply only
to `mapping_only`. Loqate ESS behavior remains under its own execution contract.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve |
|---|---|---|---|
| Country selection | country name and two-letter country code for Loqate or full_import; omitted for mapping_only | Stop before country-specific Fusion work | For Loqate, resolve the documented supported list; for user-provided structure creation, require an explicit or locally resolved ISO two-letter code without a Fusion preflight API; do not request country for mapping_only |
| Environment identity | one active configured Fusion environment or an explicit fusion_environment_context | Stop before any Fusion call | Use the sole active configured environment; otherwise ask which environment to use and show safe available choices when known |
| Durable live-run identity | project_id resolving under `project/{project_id}` | Stop before ESS submission or user-data upload | Initialize or select a project workspace so external IDs can be persisted before polling |
| Live authorization | clear execution intent plus standalone approval of the latest immutable Data Loader preview for one target environment | Stop before submission | Initial intent authorizes validation only; require the standard reviewed-archive prompt and an unchanged-artifact Task Hook receipt before the first POST |
| Single execution authorization | standalone yes to the latest business preview, including any prerequisite business remediation | Stop before profile mutation, mapping create, upload, or submission | Ask once after data gathering and all internal preflight; when `ORA_HZ_ENABLE_DAAS_LOQATE` is not Y, the combined prompt must show the profile option and proposed Y, ask whether the user wants Loqate as the source for geography data, and explain that doing so requires enabling the profile option; do not ask separate source, profile, and submission questions |
| Geography source | internally resolved `oracle_loqate` or `user_provided` | Stop only for contradictory business intent | Select Loqate for standard setup and user-provided for a custom hierarchy; never ask the user to select the internal route |
| User-data execution phase | `mapping_only` or `full_import` | Stop before mapping or file preview | Infer mapping_only only from an explicit mapping preparation/registration request; otherwise require full_import when geography data is supplied |
| User-data scope | `structure_only`, `hierarchy_only`, or `structure_and_hierarchy` | Stop before CSV generation | Require exactly one scope when geography_source is user_provided |
| User-data structure | ordered levels, Country Structure CSV, or verified existing structure model | Stop before payload preview | Require when importing structure and require as validation context for hierarchy-only execution |
| User-data hierarchy | parent-child nodes/table or Geography CSV | Stop before payload preview | Require when scope includes hierarchy |
| User-data upload target | internally resolved stage-specific destination | Stop before confirmation on missing or ambiguous metadata | Let upload_and_initiate.py resolve and normalize exact-object UcmAccount during preflight; use its retained value after approval and return the required account disclosure |
| Import mapping definition | exact task-owned stable name, object code, description, and ordered column pairs | Stop before mapping preview | Load and validate `references/import-mapping-definitions.json`; never accept a caller-supplied mapping definition or MappingNumber |
| Data Loader import authorization | completed Task Hook validation, immutable preview, standalone approval, archive verification, and persisted taskValidationEnvelope | Stop before invoking a mutating adapter operation | Preserve the preview and classify missing or mismatched authorization as approval_blocker without task-local Fusion REST fallback |
| User-data execution authorization | Data Loader approval of the stage-specific artifact | Stop before mapping/data upload | Use native stage preflight plus Task Hook validation of exact retained ZIP bytes; follow the core same-request auto-approval policy when applicable |

## Dependency-Aware Validation

| Applies When | Result | Next Action |
|---|---|---|
| Loqate country matches exactly one Oracle-supported name or code | Satisfied | Normalize the two-letter country code |
| Loqate country matches no supported value | Blocked | Report that Oracle Loqate reference data is unavailable for the requested country |
| ORA_HZ_ENABLE_DAAS_LOQATE returns exactly one `SITE` value equal to Y after trim and case normalization | Satisfied | Report the validated value and check ORA_HZ_DAAS_GEO_ENDPOINT |
| ORA_HZ_ENABLE_DAAS_LOQATE has no `SITE` record or its normalized value differs from Y | Loqate source decision required | Show `ORA_HZ_ENABLE_DAAS_LOQATE`, its safe current state, and proposed `Y`; explicitly ask whether the user wants Loqate as the source for geography data and explain that choosing it requires enabling the profile option |
| ORA_HZ_DAAS_GEO_ENDPOINT returns exactly one `SITE` value containing at least one non-whitespace character after trimming | Satisfied | Preserve the original value exactly, report it as validated, exclude it from every change plan, and continue to internal request validation |
| ORA_HZ_DAAS_GEO_ENDPOINT has no `SITE` record or its value is null, empty, or whitespace-only | Configuration required | Ask the user to configure the site-level value in Fusion; stop before profile writes or import and re-read it when the user resumes |
| Either site-level profile collection returns more than one record | Blocked | Stop as fusion_api_error; do not select or mutate an ambiguous record |
| User gives a standalone affirmative reply to the combined Loqate-and-submission prompt | Approved | Create or update an eligible `ORA_HZ_ENABLE_DAAS_LOQATE` `SITE` value, re-read both values, and continue only when the endpoint is configured |
| User declines or does not confirm the single business preview | Manual path | Make no profile changes, do not submit the geography job, and explain where the user can define the country structure and hierarchy manually |
| Post-change read returns ORA_HZ_ENABLE_DAAS_LOQATE as Y and ORA_HZ_DAAS_GEO_ENDPOINT as nonblank | Satisfied | Continue to internal request validation and ESS submission |
| Post-change read does not satisfy both required conditions | Blocked | Stop as fusion_api_error and report which approved change could not be verified |
| ORA_HZ_ENABLE_DAAS_LOQATE is Y and ORA_HZ_DAAS_GEO_ENDPOINT is nonblank | Satisfied, no-op | Do not create, update, or ask for confirmation; report both validations and continue |
| geography_source is user_provided | Satisfied for custom routing | Skip both Loqate profile resolvers and the Loqate ESS request; resolve execution_phase, then route to mapping-only validation or the full canonical model |
| execution_phase is mapping_only | Satisfied for mapping preparation | Validate only the selected task-owned mapping definitions, project path, environment, authorization, and applicable Data Loader gates; skip country, CSV, UCM, import activity, and polling requirements |
| mapping_only: Mapping lookup returns exactly one stable name/object match with the complete one-to-one column-pair set | Satisfied, reuse | Canonicalize into task-defined order, then persist the MappingNumber and fingerprint without a POST |
| mapping_only: Mapping lookup returns no exact name/object match | Create required | Verify the artifact again and POST the complete nested mapping once through the Data Loader-authorized REST core service with framework version 9 and an in-memory explicit token that disables mutation replay |
| mapping_only: Mapping lookup returns duplicates or a column mismatch | Blocked | Stop as catalog_or_metadata_mismatch; do not select, patch, delete, overwrite, or create another similarly named mapping |
| User-data structure has one country, one level-1 COUNTRY row, and unique contiguous levels | Satisfied | Generate or preserve the validated Country Structure CSV |
| Structure import reports that the structure already exists | Already present | Stop after the activity result; do not delete, replace, retry, or append levels through import |
| Hierarchy levels and types match the validated structure and every child has a complete in-file ancestor chain | Satisfied | Continue to identifier and payload validation |
| Hierarchy-only scope lacks a reliable existing structure model | Blocked | Ask for the existing structure definition or a supported read-only verification result |
| User-data row requests update, upsert, or deletion | Blocked | Reject before preview or upload |

## Field Validation

| Check | What Happens |
|---|---|
| country is a scalar string | Continue to country resolution |
| country is blank, an array, an object, or contains multiple comma-separated values | Reject as input_validation |
| country is blank or ambiguous in an interactive request | Ask for exactly one source-appropriate country name/code instead of returning only a validation code |
| country code length is two characters | For Loqate compare with the supported-country table; for user-provided structure creation uppercase the explicit or locally resolved ISO code and do not call Fusion for preflight validation |
| wait_seconds is absent | Apply the default from ora_defaulting_rules.md |
| wait_seconds is not a positive integer | Reject as input_validation |
| poll_interval is absent | Apply the default from ora_defaulting_rules.md |
| poll_interval is not a positive integer or exceeds wait_seconds | Reject as input_validation |
| project_id resolves outside project/{project_id} | Reject as artifact_persistence |
| live execution omits project_id | Reject before ESS submission or UCM upload as artifact_persistence; never run a live operation whose external ID exists only in process output |
| correlation description, UTC submission window, or checkpoint path is missing | Reject before ESS submission as artifact_persistence |
| tracking invocation omits request_id or still contains submission arguments | Reject before polling as input_validation; tracking must be request-ID-only |
| geography_source is absent | Infer it from standard-versus-custom business intent; reject only a contradictory resolved value as input_validation |
| execution_phase is missing or invalid for user_provided | Infer only from explicit mapping-only intent or supplied import data; otherwise reject as input_validation |
| requested_scope is missing or invalid for user_provided | Reject before file generation as input_validation |
| mapping_only omits country or CSV data | Continue; mappings are reusable and not country-specific |
| a caller supplies mapping Name, ObjectCode, ImportMappingColumns, MappingNumber, or Data Loader authorization override | Reject as input_validation; the task-owned definition and central authorization workflow are authoritative |
| task-owned mapping definition has duplicate headers, duplicate attributes, a missing required header, an unexpected object code, or a name over 100 characters | Reject as catalog_or_metadata_mismatch before any Data Loader call |
| Data Loader validation does not authorize read-only REST preflight | Stop before mapping GET as approval_blocker; persist the internal diagnostic and do not implement task-local Fusion REST |
| structure CSV headers differ from CountryCode,LevelNumber,GeographyType | Reject as input_validation; do not guess mappings |
| structure has mixed country codes, duplicate/gapped levels, or level 1 other than COUNTRY | Reject as input_validation |
| hierarchy has mixed countries, orphan children, level/type mismatches, duplicate primary Source IDs, or a missing country anchor | Reject as input_validation |
| RecordTypeCode is not 0, 1, or an explicitly allowed additive 2 | Reject as input_validation |
| RecordTypeCode 0 is used below the minimum required existing-parent chain | Reject as input_validation; anchors must represent existing parent records needed by new children |
| RecordTypeCode 2 targets country or does not match one preceding primary row's source relationship | Reject as input_validation |
| only one of PrimaryGeographyCodeType and PrimaryGeographyCode is supplied on a new geography | Reject as input_validation; create the pair together |
| ImportMode is DELETE_RECORD or represents update/upsert | Reject as input_validation |
| ImportMode is CREATE_RECORD without a reviewed target compatibility exception | Native helper exposes no ImportMode control; do not construct direct activity payloads or assume CREATE_ONLY. Block before approval if required additive semantics cannot be established for the target |
| caller omits ucm_document_account before live user-data upload | Let the native helper resolve exact-object UcmAccount before approval; use its normalized saved value and required disclosure, with no fallback |
| caller supplies a UCM account override | Reject as input_validation; the live CX object-metadata response bound to the current approval is authoritative |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GEO.VALIDATE | step | 2 | validate_input | ok->GEO.SOURCE;failure->GEO.FAILED | GEO.COLLECT | stop | Validate source, execution phase, requested scope, environment, project path, mapping contract, and source-specific country, data, or polling inputs |
| GEO.SOURCE | decision | 4 | evaluate_result | oracle_loqate->GEO.COUNTRY;user_provided->GEO.USER.NORMALIZE;failure->GEO.FAILED | GEO.VALIDATE | stop | Route exactly one source before Loqate lookups or user-data file processing |

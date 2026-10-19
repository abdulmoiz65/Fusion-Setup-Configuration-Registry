# Defaulting Rules

## Execution phase boundary

`full_import` uses only the native `core.data-loader` CX Import handoff in
[REST execution](ora_rest_execution.md#native-data-loader-cx-import). Its stage
mapping CSV replaces direct mapping lookup/create and MappingNumber requirements.
Its retained preflight envelope replaces direct UCM/import-activity payloads.
Return the loader's required preview/result fields, check status only on explicit
request, and use a fresh approved hierarchy load after confirmed structure success.
REST mapping lookup/create, reuse/drift rules, and mapping IDs below apply only
to `mapping_only`. Loqate ESS behavior remains under its own execution contract.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? |
|---|---|---|---|
| country_code | Uppercase documented two-letter code | Country is supplied as a supported name or lowercase code | Yes, replace only casing and surrounding whitespace |
| wait_seconds | 300 | Caller does not supply a polling window | Yes, caller may request a larger positive bounded value |
| poll_interval | 10 | Caller does not supply a polling interval | Yes, caller may request another positive value not greater than wait_seconds |
| ESS retries | 0 | Every new Import Geography Data submission | No automatic retry |
| job_definition_id | JobDefinition://oracle/apps/ess/fod/simplifiedsetup/geographies/SimplifiedGeoSetupJob | Every live run | No |
| application | CrmEss | Every live run | No |
| correlation_description | FDOS:manage-geographies:{project_id}:{country_code}:{run_id} | Every live run | Generate once and persist before POST |
| submission_checkpoint | project/{project_id}/artifacts/pillars/cx/customer-data-management/enterprise-profile/manage-geographies/current/ess-submission-checkpoint.json | Every live run | No |
| execution_result | project/{project_id}/artifacts/pillars/cx/customer-data-management/enterprise-profile/manage-geographies/current/ess-execution-result.json | Every live run | No |
| request_parameter_name | submit.argument1 | Every live run | No |
| request_parameter_type | STRING | Every live run | No |
| ORA_HZ_ENABLE_DAAS_LOQATE expected SITE value | Y | Every prerequisite validation | No |
| ORA_HZ_DAAS_GEO_ENDPOINT | No default | If the configured `SITE` value is missing or blank, ask the user to configure it in Fusion and stop before import | Preserve every existing nonblank value exactly; never create or update it through this skill |
| user-data execution_phase | full_import | The request supplies structure/hierarchy data and does not explicitly ask only to prepare mappings | mapping_only requires explicit mapping preparation or registration intent |
| structure mapping name | FDOS_MANAGE_GEOGRAPHIES_STRUCTURE_V1 | structure_only or structure_and_hierarchy mapping scope | Fixed task-owned value; do not accept a runtime override |
| hierarchy mapping name | FDOS_MANAGE_GEOGRAPHIES_HIERARCHY_V1 | hierarchy_only or structure_and_hierarchy mapping scope | Fixed task-owned value; do not accept a runtime override |
| mapping definition source | references/import-mapping-definitions.json | Every user-data mapping preview | Fixed reviewed source; do not infer columns from a runtime CSV |
| mapping_only transport | Data Loader-authorized REST core service with REST-Framework-Version 9 | Every live mapping lookup or create | Complete central orchestration gates; no task-local Fusion REST fallback |
| mapping_only create retry | 0 | Every mapping POST | Reconcile through exact authorized REST-core GET; never repeat an uncertain POST automatically |
| user-data SourceId | Deterministic positive integer string assigned parent-first within the generated file | A primary/anchor hierarchy row omits SourceId | Preserve supplied valid Source IDs; alternate rows reuse their primary row's IDs |
| user-data ImportMode | no caller control | Native CX full_import | Enforce additive geography row rules locally; never invent a helper ImportMode flag or claim it sets CREATE_ONLY |
| user-data Activate | owned by Data Loader backend | Native CX full_import | Do not send a direct importActivities payload |
| user-data HighVolume | omitted | Native CX full_import | Add --cx-import-high-volume-load only when explicitly requested before preflight; never add it after approval |
| user-data schedule | owned by Data Loader backend | Native CX full_import | Do not construct direct schedule or activation fields |
| user-data job names | helper-generated data set name | Native CX full_import | Reuse the retained preflight identity after approval |
| CX import-file destination | no default | Native CX full_import preflight | Helper resolves exact-object UcmAccount, normalizes to dollar-segment syntax, and retains it; return its required account disclosure and never refresh after approval |
| Data Loader approval prompt | `Do you want to proceed with submitting the reviewed archive?`; when `ORA_HZ_ENABLE_DAAS_LOQATE` is missing or not Y, use `Do you want to use Loqate as the source for geography data? If so, we need to enable ORA_HZ_ENABLE_DAAS_LOQATE by setting it to Y. Do you want to proceed with enabling it and submitting the reviewed archive?` | Every initial live request after immutable preview | Require a standalone affirmative reply to the latest unchanged preview before any POST |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GEO.DEFAULTS | step | 6 | apply_default | ok->GEO.PROFILES;failure->GEO.FAILED | GEO.COUNTRY | stop | Normalize Loqate country code and polling options without changing user intent |

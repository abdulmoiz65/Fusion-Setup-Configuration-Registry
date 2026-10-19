# Dependency Readiness

## Execution phase boundary

`full_import` uses only the native `core.data-loader` CX Import handoff in
[REST execution](ora_rest_execution.md#native-data-loader-cx-import). Its stage
mapping CSV replaces direct mapping lookup/create and MappingNumber requirements.
Its retained preflight envelope replaces direct UCM/import-activity payloads.
Return the loader's required preview/result fields, check status only on explicit
request, and use a fresh approved hierarchy load after confirmed structure success.
REST mapping lookup/create, reuse/drift rules, and mapping IDs below apply only
to `mapping_only`. Loqate ESS behavior remains under its own execution contract.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Supported Loqate country | Resolve one exact two-letter country code from ora_reference_lookups.md |
| 2 | Loqate import enablement | Read ORA_HZ_ENABLE_DAAS_LOQATE through core.fusion-api.apps-common and require Y |
| 3 | DaaS geography endpoint | Read ORA_HZ_DAAS_GEO_ENDPOINT through core.fusion-api.apps-common and require any non-null, non-empty value after trimming |
| 4 | Conditional prerequisite plan | If `ORA_HZ_DAAS_GEO_ENDPOINT` is missing or blank, ask the user to configure its site-level value and stop before import. Otherwise, if `ORA_HZ_ENABLE_DAAS_LOQATE` is missing or not Y, show that profile option, its safe current state, and proposed Y in one combined Loqate-and-submission prompt |
| 5 | Live execution intent | Require a direct imperative setup request for the resolved country and environment to begin validation; it does not approve a live POST |
| 6 | User-data request shape | For mapping_only, require only one mapping scope; for full_import, require one country, one scope, validated structure context, and hierarchy data when requested |
| 7 | Task-owned import mapping definitions | Load the selected stable mapping or mappings from `references/import-mapping-definitions.json` and validate their exact names, object codes, and ordered column pairs |
| 8 | Data Loader mutation authorization | Complete Task Hook routing, rule validation, the applicable immutable preview and approval policy, archive verification, and receipt persistence before invoking a mutation |
| 9 | Native Data Loader handoff | For full_import, require one stage mapping CSV and data CSV, retained immutable preflight artifact, approved Task Hook envelope, and native upload_and_initiate.py; no MappingNumber prerequisite |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| GEO.COUNTRY.SUPPORTED | Oracle Loqate supported country | Yes | geography_source=oracle_loqate | Verify | Oracle supported-country documentation represented in ora_reference_lookups.md | country_code_resolver | The Import Geography Data action is unavailable for unsupported countries | Provide one supported country name or code | country_name, country_code |
| GEO.LOQATE.ENABLED | ORA_HZ_ENABLE_DAAS_LOQATE | Yes for Loqate import | geography_source=oracle_loqate | Verify or include eligible remediation in the one execution preview | Configured site-level profile option value | loqate_enabled_profile_resolver | Loqate geography import must be enabled before the job runs | Always show `ORA_HZ_ENABLE_DAAS_LOQATE`, its safe current state, and proposed `Y` when remediation is needed, ask whether the user wants Loqate as the source for geography data, and explain that choosing it requires enabling the profile option | loqate_profile_value, loqate_profile_matches |
| GEO.DAAS.ENDPOINT | ORA_HZ_DAAS_GEO_ENDPOINT | Yes for Loqate import | geography_source=oracle_loqate | Verify; stop if missing or blank | Configured site-level profile option value | daas_endpoint_profile_resolver | A nonblank DaaS geography service endpoint is required before the job runs | Ask the user to configure the site-level value in Fusion; preserve every existing nonblank value exactly and never write this option through the skill | daas_geo_endpoint_value, daas_geo_endpoint_present |
| GEO.USER.STRUCTURE | Compatible country structure | 24 | geography_source=user_provided | Verify locally for structure creation; target result validates acceptance | User model/CSV; reliable existing-structure context only for hierarchy_only | local_structure_validator | Structure creation needs ordered levels; hierarchy creation needs established levels and types | Supply ordered levels or a compatible CSV; do not call a target preflight API for structure creation | structure_levels, structure_types, structure_import_required |
| GEO.USER.MAPPING.DEFINITION | Stable import mapping definition | Yes for mapping_only and full_import | geography_source=user_provided | Verify locally | `references/import-mapping-definitions.json` | import_mapping_definition_resolver | The skill owns the exact source-to-target mapping used by each import activity | Do not accept runtime overrides; update the reviewed definition through skill review | mapping_name, mapping_object_code, mapping_columns, mapping_fingerprint |
| GEO.USER.MAPPING.AUTHORIZATION | Data Loader validation and mutation authorization of the REST core service | Yes for mapping lookup/create | geography_source=user_provided | Resolve internally | `core.data-loader` validation and approval workflow | data_loader_import_authorization | Read-only lookup must pass task validation and a create must also have the single execution approval | Resolve internally; report only business readiness unless technical detail is requested | data_loader_authorized, data_loader_preview_reference |
| GEO.USER.MAPPING.NUMBER | Persisted Fusion MappingNumber | Only mapping_only | geography_source=user_provided and execution_phase=mapping_only | Reuse exact match or create once | Authorized REST core service result | import_mapping_resolver | Mapping-only result must retain the selected reusable mapping | Reconcile uncertain create; stop on duplicate or drift | mapping_number, mapping_outcome |
| GEO.USER.UCM | Data Loader-resolved import destination | Full_import preflight only | geography_source=user_provided and execution_phase=full_import | Resolve once before approval | Native Data Loader exact-object metadata lookup | cx_object_metadata_resolver | Retain normalized account in preflight; no metadata refresh after approval | Return required account disclosure; no override or fallback | ucm_document_account, ucm_account_source |
| GEO.USER.APPROVAL | Approval of the latest exact immutable stage preview | Yes for user-data live execution | geography_source=user_provided | Verify | User response plus Task Hook receipt and artifact SHA-256 | approval_gate | Mapping creation and imports change Fusion and may partially succeed | For full_import follow core.data-loader exact-load approval/auto-approval policy; require stage-specific Task Hook integrity and reject stale or changed-artifact approval | user_data_execution_approved, task_validation_envelope |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | All mandatory dependencies have verified expected values | Yes when the user's direct request clearly authorizes live setup |
| Satisfied, no-op | ORA_HZ_ENABLE_DAAS_LOQATE is Y and ORA_HZ_DAAS_GEO_ENDPOINT is nonblank | Continue without profile writes or a profile-change confirmation prompt |
| Verify | A runtime profile read must establish the dependency | Yes for the documented read-only resolver |
| Prerequisite remediation planned | The endpoint is configured and Loqate enablement differs; an eligible internal change plan is ready | Show the exact enablement profile option and proposed Y in a combined Loqate-and-submission question; mutate only after its approval |
| Manual path | The user declines the single business preview | No; leave both values unchanged and explain manual Manage Geographies setup |
| Blocked | A country is unsupported, the endpoint is missing or blank, profile results are ambiguous, or post-change verification fails | No; for a missing endpoint ask the user to configure it and re-read it on resumption |
| Intent blocker | The request is advisory or ambiguous about live setup | No |
| User-data ready | Canonical stage mapping/data CSVs pass local validation, native preflight succeeds, and exact retained artifact has Task Hook approval | Yes through native Data Loader approved-envelope submission; stop after initiation |
| Mapping ready | The reviewed definition, environment, project path, and authorization are present for mapping_only | Reuse/create via authorized REST, persist MappingNumber, and stop; full_import instead renders mapping CSVs locally |
| Mapping authorization blocked | Data Loader validation or approval did not authorize the REST core service | No; persist the preview, classify as approval_blocker, and do not implement task-local Fusion REST |
| User-data partial | Structure completed but hierarchy failed or timed out | No automatic continuation or rollback; preserve the structure and diagnostics |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GEO.READINESS | decision | 8 | resolve_dependency | ready->GEO.DESIGN;remediation_required->GEO.DESIGN;blocked->GEO.BLOCKED;failure->GEO.FAILED | GEO.PROFILES | stop | Validate exact profile values and carry any eligible remediation into the single business execution preview |

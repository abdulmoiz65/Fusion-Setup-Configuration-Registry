# Design Enforcement

## Execution phase boundary

`full_import` uses only the native `core.data-loader` CX Import handoff in
[REST execution](ora_rest_execution.md#native-data-loader-cx-import). Its stage
mapping CSV replaces direct mapping lookup/create and MappingNumber requirements.
Its retained preflight envelope replaces direct UCM/import-activity payloads.
Return the loader's required preview/result fields, check status only on explicit
request, and use a fresh approved hierarchy load after confirmed structure success.
REST mapping lookup/create, reuse/drift rules, and mapping IDs below apply only
to `mapping_only`. Loqate ESS behavior remains under its own execution contract.

## Enforcement Order

Sequences 1-8 apply to `oracle_loqate`; sequences 9-13 apply to
`user_provided`.

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate supported country | Resolve exactly one country in the Oracle Loqate list |
| 2 | Validate Loqate import enablement | Require ORA_HZ_ENABLE_DAAS_LOQATE to resolve to Y |
| 3 | Validate DaaS geography endpoint | Require ORA_HZ_DAAS_GEO_ENDPOINT to contain at least one non-whitespace character after trimming |
| 4 | Plan profile corrections | When Loqate enablement is missing or not Y, show `ORA_HZ_ENABLE_DAAS_LOQATE`, its safe current state, and proposed Y, ask whether the user wants Loqate as the source for geography data, and explain that choosing it requires enabling the profile option; keep the endpoint value internal |
| 5 | Verify corrections | Re-read both values after approved writes and require the exact expected values |
| 6 | Validate target | Confirm the environment identity |
| 7 | Persist submission identity | Require project_id, unique correlation description, UTC submission window, and task-local checkpoint path before POST |
| 8 | Enforce single submission | Submit-only once, capture requestId durably, and track only through a separate request-ID invocation |
| 9 | Validate user-data request | For mapping_only require one mapping scope; for full_import require one locally resolved ISO country code, one scope, structure-level integrity, hierarchy parent integrity, and creation-only record intent without target geography or metadata preflight APIs |
| 10 | Validate owned mappings | Require exact reviewed stable names, expected object codes, complete ordered column pairs, and canonical fingerprints from `references/import-mapping-definitions.json` |
| 11 | Gate Data Loader mapping persistence | Resolve mappings read-only before the business preview; after the single approval reuse one exact match or create once through the authorized REST core service, persist MappingNumber internally, and never implement task-local Fusion REST |
| 12 | Gate user-data handoff | For every phase/scope require project persistence, immutable artifact/checksum, verified Task Hook receipt, internal payload and destination preflight, environment, and one standalone business-preview approval |
| 13 | Enforce staged import | Submit native structure envelope first and stop; only explicit status confirming success unlocks a fresh hierarchy preflight and approval |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| GEO.COUNTRY.REQUIRED | Loqate requests | Blocker | country_code_resolver | Country does not match exactly one supported value | Provide one documented country name or code | Yes |
| GEO.LOQATE.REQUIRED | Loqate requests | Prerequisite plan gate | loqate_enabled_profile_resolver | ORA_HZ_ENABLE_DAAS_LOQATE is missing or does not resolve to Y | Show `ORA_HZ_ENABLE_DAAS_LOQATE`, its safe current state, and proposed `Y`; ask whether the user wants Loqate as the source for geography data and explain that choosing it requires enabling the profile option | Yes, only after the combined Loqate-and-submission confirmation |
| GEO.ENDPOINT.REQUIRED | Loqate requests | Blocker | daas_endpoint_profile_resolver | ORA_HZ_DAAS_GEO_ENDPOINT is missing, null, empty, or whitespace-only | Ask the user to configure its site-level value in Fusion; re-read it on resumption | No; never write this option through the skill |
| GEO.PROFILE.RESULT.UNAMBIGUOUS | Every profile read | Blocker | both profile resolvers | More than one `SITE` record is returned for either profile | Stop and correct the ambiguous Fusion configuration | No |
| GEO.PROFILE.CHANGES.VERIFIED | After approved profile writes | Blocker | both profile resolvers | Either re-read value does not exactly match its expected value | Stop and report the failed verification; do not submit ESS | No automatic retry |
| GEO.ENVIRONMENT.REQUIRED | Every request | Blocker | none | Target Fusion environment is missing or ambiguous | Confirm the exact environment | Yes |
| GEO.ONE.REQUEST | Before live execution | Blocker | none | Internal execution plan contains more than one country or introduces retries | Create one request with one country code and zero automatic retries | Yes |
| GEO.SUBMISSION.CHECKPOINT | Before live execution | Blocker | none | project_id, unique correlation description, UTC submission window, or checkpoint path is missing | Persist the submission identity before POST | Yes |
| GEO.REQUEST.ID.CAPTURED | After submit-only returns | Blocker | none | The checkpoint does not contain one positive integer requestId | Inspect the same process handle and checkpoint, then use exact read-only recovery; never resubmit | No automatic retry |
| GEO.POLL.BY.ID | During monitoring | Blocker | none | Polling invocation is capable of submitting a new request | Track only with the captured `--request-id` | Yes |
| GEO.USER.SOURCE.REQUIRED | Every user-data full_import request | Blocker | user_country_resolver | Country name/code cannot be resolved locally to one ISO alpha-2 code | Supply one exact country name and two-letter code | Yes |
| GEO.USER.STRUCTURE.VALID | User-data full_import scope includes structure or hierarchy | Blocker | geography_type_resolver | Missing level-1 COUNTRY, mixed country, gapped/duplicate levels, blank/duplicate normalized type, or unavailable existing-structure context for hierarchy_only | Correct or supply the ordered structure definition | Yes |
| GEO.USER.HIERARCHY.VALID | User-data full_import scope includes hierarchy | Blocker | none | Missing root anchor, orphan child, level/type mismatch, duplicate primary Source ID, or invalid identifier relationship | Correct the hierarchy and include all parents | Yes |
| GEO.USER.CREATE.ONLY | Every user-data full_import row model | Blocker | none | Update, upsert, delete, replacement, or ambiguous anchor/identifier semantics appear | Validate additive row rules locally; helper exposes no ImportMode flag; stop if target cannot establish required additive behavior | Yes |
| GEO.USER.MAPPING.DEFINITION | Every user-data mapping preview | Blocker | import_mapping_definition_resolver | Stable name, object code, ordered column pairs, mapping name length, or fingerprint differs from the reviewed definition | Restore the exact task-owned definition and submit changes through review | No runtime override |
| GEO.USER.MAPPING.AUTHORIZATION | Before mapping lookup/create | Blocker | data_loader_import_authorization | Data Loader validation has not authorized read-only lookup, or the mapping_only approval has not authorized create | Complete the applicable internal gate and do not expose mapping mechanics | No task-local REST fallback |
| GEO.USER.MAPPING.UNAMBIGUOUS | During mapping resolution | Blocker | import_mapping_resolver | More than one name/object match exists or one match has column drift | Reconcile the Fusion mappings through reviewed administration; do not patch, delete, select, or create automatically | No automatic mutation |
| GEO.USER.MAPPING.CAPTURED | After mapping create/reuse | Blocker | import_mapping_resolver | A nonblank MappingNumber, fingerprint, environment, or created/reused outcome was not durably persisted | Reconcile by exact authorized REST-core GET; never repeat an uncertain POST | No automatic retry |
| GEO.USER.EXISTING.STRUCTURE | User-data scope includes structure import | Import-result blocker | none | The creation-only import activity reports that the country structure exists | Stop; do not delete, replace, retry, or append through import | No |
| GEO.USER.UCM.ACCOUNT | Before native full_import approval only | Blocker | cx_object_metadata_resolver | Missing or ambiguous exact-object UcmAccount | Let Data Loader resolve, normalize, retain, and report it; no post-approval lookup | No runtime override |
| GEO.USER.PREVIEW.APPROVED | Before first user-data side effect | Approval blocker | data_loader_import_authorization | Stage preflight, exact artifact, or approved Task Hook envelope is absent/mismatched | Follow native Data Loader preview and approval policy, retaining required account disclosure | Yes |
| GEO.USER.ACTIVITY.MAPPING | Before native full_import preflight | Blocker | import_mapping_definition_resolver | Missing stage mapping CSV, changed column pairs, multiple objects, or competing object-code override | Use one reviewed two-table mapping CSV and its data CSV; IMPORT OBJECT is authoritative | Yes before preflight |
| GEO.USER.STAGE.ORDER | structure_and_hierarchy execution | Blocker | none | Hierarchy would start before confirmed structure completion without errors | Stop after structure initiation; check status only on explicit request and approve hierarchy separately | Yes |
| GEO.USER.ACTIVITY.CAPTURED | After native CX initiation | Blocker | none | Data Loader did not return an accepted data set identity and RequestId | Reconcile the same load; never initiate another automatically | No automatic retry |

## Design Lookup Requirements

| Rule ID | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|
| GEO.COUNTRY.REQUIRED | country_code_resolver | Every Loqate request | country_name, country_code | ora_reference_lookups.md |
| GEO.LOQATE.REQUIRED | loqate_enabled_profile_resolver | Every Loqate request and after approved writes | loqate_profile_value, loqate_profile_matches | ora_reference_lookups.md |
| GEO.ENDPOINT.REQUIRED | daas_endpoint_profile_resolver | Every Loqate request and after approved writes | daas_geo_endpoint_value, daas_geo_endpoint_present | ora_reference_lookups.md |
| GEO.USER.SOURCE.REQUIRED | user_country_resolver | Every user-data full_import request | country_name, country_code | ora_reference_lookups.md |
| GEO.USER.STRUCTURE.VALID | geography_type_resolver | Every user-data full_import structure model | validated_geography_types | ora_reference_lookups.md |
| GEO.USER.MAPPING.DEFINITION | import_mapping_definition_resolver | Every user-data mapping preview | mapping_name, mapping_object_code, mapping_columns, mapping_fingerprint | ora_reference_lookups.md |
| GEO.USER.MAPPING.AUTHORIZATION | data_loader_import_authorization | Every live mapping lookup/create | data_loader_authorized, data_loader_preview_reference | ora_reference_lookups.md |
| GEO.USER.MAPPING.CAPTURED | import_mapping_resolver | Before mapping-only completion or full import handoff | mapping_number, mapping_outcome | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GEO.DESIGN | decision | 10 | design_enforcement | passed->GEO.PREVIEW;blocked->GEO.BLOCKED;failure->GEO.FAILED | GEO.READINESS | stop | Apply all mandatory gates and carry eligible prerequisite remediation into the single business preview |

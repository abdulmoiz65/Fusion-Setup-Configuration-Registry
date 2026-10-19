# Bulk Intake

## Execution phase boundary

`full_import` uses only the native `core.data-loader` CX Import handoff in
[REST execution](ora_rest_execution.md#native-data-loader-cx-import). Its stage
mapping CSV replaces direct mapping lookup/create and MappingNumber requirements.
Its retained preflight envelope replaces direct UCM/import-activity payloads.
Return the loader's required preview/result fields, check status only on explicit
request, and use a fresh approved hierarchy load after confirmed structure success.
REST mapping lookup/create, reuse/drift rules, and mapping IDs below apply only
to `mapping_only`. Loqate ESS behavior remains under its own execution contract.

## Accepted Bulk Inputs

| Input Format | What Must Be Provided | How Rows Are Processed |
|---|---|---|
| Loqate request | One supported country | No CSV is accepted; run one country through the existing ESS path |
| Country Structure CSV | CountryCode, LevelNumber, GeographyType | Parse all rows as one ordered, contiguous country structure and reject mixed countries |
| Geography CSV | Compatible Geography import headers and one country | Parse parent-first anchor, create, and explicitly allowed alternate-identifier rows |
| Structure table/list | One country and ordered level/type pairs | Normalize to the canonical structure model and generate deterministic CSV |
| Hierarchy tree/table | One country, geography nodes, parents, levels/types, and optional identifiers | Normalize parents before children, assign missing Source IDs deterministically, and generate CSV |
| Mapping-only request | One requested mapping scope, target environment, project_id, and direct preparation intent | Select the reviewed stable mapping definition or definitions; do not require or synthesize country rows |

## Column Guidance

| Column Type | Allowed Fields | What Happens |
|---|---|---|
| Single-country Loqate input | country, fusion_environment_context, project_id, wait_seconds, poll_interval | Validate as one Loqate request |
| User structure fields | CountryCode, LevelNumber, GeographyType | Require level 1 COUNTRY plus unique contiguous levels |
| User hierarchy primary fields | PrimaryGeographyName, RecordTypeCode, SourceId, CountryCode, LevelNumber, ParentSourceId | Require one root anchor, create-only primary rows, valid levels, and complete parent chains |
| User hierarchy optional fields | GeographyType, ParentGeographyType, language, primary code pair, dates, additive identifier triplet, declared provider | Validate atomic field groups and target lookup values; never default a provider |
| CSV, spreadsheet, array, or table with multiple countries | None | Reject before Fusion calls and ask the caller to run one country at a time |
| Task-owned mapping columns | Exact ordered ColumnHeader/AttributeCode pairs from `references/import-mapping-definitions.json` | Validate and fingerprint the complete selected definition; never derive the persistent mapping from a partial runtime file |

## Execution Rules

| Gate | Requirement |
|---|---|
| Catalog support | Do not route this task to FSM CSV export or import because CSVExportImportSupportedFlag is N |
| Row count | Require exactly one country for Loqate or full_import; require no country rows for mapping_only |
| Live execution | Require a separate direct setup instruction for each country; after success, a user-supplied next country starts a fresh run and never joins a batch |
| Profile changes | When `ORA_HZ_ENABLE_DAAS_LOQATE` is missing or not Y, show that profile option and proposed Y, ask whether the user wants Loqate as the source for geography data, and explain that choosing it requires enabling the profile option in the single business preview; apply and verify eligible changes after approval without another question |
| Sequential continuation | After each successful country, ask whether to set up another; accept one country name or code and repeat every validation, persistence, and submission gate |
| User-data canonicalization | Parse the complete input before rendering; preserve geography names, identifiers, and language values exactly and report every validation error together when safe |
| User-data generation | Use a CSV writer with UTF-8 encoding and deterministic header/order; do not hand-concatenate unescaped cell values |
| Structure/hierarchy relationship | Every hierarchy level and type must match the validated structure; hierarchy_only still requires structure context |
| Parent ordering | Emit every anchor/parent before its children and include the complete ancestor chain required by the import |
| Creation-only records | Permit type 0 only for required existing anchors, type 1 for new geographies, and type 2 only for explicitly requested additive names/codes below country |
| Import ordering | For structure_and_hierarchy, initiate structure and leave hierarchy pending. Only an explicit status request confirming structure success unlocks a fresh hierarchy preflight and approval |
| Mapping ordering | Full_import renders one reviewed mapping CSV per object; never combine structure and hierarchy objects. Mapping_only retains structure-before-hierarchy REST mapping preparation |
| Mapping-only boundary | Stop after selected mappings are reused or created; never generate a CSV, upload to UCM, create an import activity, or poll status |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| GEO.USER.NORMALIZE | step | 18 | process_bulk | ok->GEO.USER.VALIDATE;failure->GEO.FAILED | GEO.SOURCE | stop | Resolve execution_phase and selected mapping definitions; for full_import also normalize one-country user structure, hierarchy, table, tree, or CSV into the canonical request model |
| GEO.USER.VALIDATE | step | 19 | validate_input | ok->GEO.USER.PREVIEW;blocked->GEO.BLOCKED;failure->GEO.FAILED | GEO.USER.NORMALIZE | stop | Validate task-owned mappings, project path, task context, environment, and authorization inputs; for full_import validate additive data, parent chains, reviewed mapping CSV, exact native retained artifact, and required Data Loader preflight fields |

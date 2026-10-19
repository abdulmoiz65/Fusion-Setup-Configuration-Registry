# Design Advisory

## Execution phase boundary

`full_import` uses only the native `core.data-loader` CX Import handoff in
[REST execution](ora_rest_execution.md#native-data-loader-cx-import). Its stage
mapping CSV replaces direct mapping lookup/create and MappingNumber requirements.
Its retained preflight envelope replaces direct UCM/import-activity payloads.
Return the loader's required preview/result fields, check status only on explicit
request, and use a fresh approved hierarchy load after confirmed structure success.
REST mapping lookup/create, reuse/drift rules, and mapping IDs below apply only
to `mapping_only`. Loqate ESS behavior remains under its own execution contract.

## Guidance Sources

| Source Mode | Allowed Sources | When Used |
|---|---|---|
| Product setup behavior | Oracle current Manage Geographies and geography import documentation | Explain geography structure, hierarchy, import availability, and completion indicators |
| Profile prerequisites | Oracle geography profile-option documentation and configured Fusion `SITE` profile reads | Explain what each profile controls, why Loqate must be Y, why the DaaS endpoint must be nonblank, and how the user's yes/no Loqate decision controls any correction |
| Execution contract | User-provided ESS job definition, application, and argument contract plus core.fusion-api.ess-job-submitter | Explain the automated import path |
| User-provided structure | Current Oracle Country Structure Import Management guidance plus the locally supplied country/level/type model | Explain local normalization, creation-only submission, import-result validation, existing-structure restrictions, and structure-first sequencing; do not call target preflight APIs |
| User-provided hierarchy | Current Oracle geography guidance, target lookup values, and native core.data-loader CX Import | Validate parent-first additive rows; supply mapping/data CSVs, stop after initiation, and retrieve results only on explicit request |
| Import mapping lifecycle | Task-owned mapping definitions plus native Data Loader CSV contract | Full_import renders two-table mapping CSVs; only mapping_only uses reviewed REST mapping lookup/create |

## Guidance Topics

| Topic | Advisory Level | What To Explain | Do Not Include |
|---|---|---|---|
| Geography country structure | Strong | The import defines the country structure used by master geographies | Do not claim address cleansing or geocoding is configured |
| Geography hierarchy master data | Strong | The import loads the supported master geography hierarchy for the country | Do not claim custom or third-party geography data was loaded |
| Shared usage | Strong | Geography structure and hierarchy are shared across product families | Do not duplicate setup separately for each consuming offering |
| Existing geography setup | Strong | Oracle may reject or disable import when structure or hierarchy already exists for the country | Do not invent a preflight endpoint; rely on source-backed checks and ESS diagnostics |
| Completion verification | Strong | A successful import should show Structure Defined and Hierarchy Defined for the country | Do not report Geocoding Defined or Address Cleansing Defined |
| User-data source separation | Strong | Custom data bypasses Loqate profiles and ESS and uses the existing CX import core | Do not label custom data as Loqate or duplicate transport in this pillar skill |
| Country Structure import | Strong | Import creates one complete ordered structure and fails for an existing structure | Do not delete, replace, or append levels through import |
| Geography row intent | Strong | Type 0 identifies required existing anchors, type 1 creates geographies, and type 2 additively creates alternate identifiers below country | Do not interpret type 0 as create or allow update/delete semantics |
| Partial completion | Strong | Structure can remain successfully created when the later hierarchy activity fails | Do not claim atomic rollback or automatically retry hierarchy |
| Mapping ownership | Strong | CX owns reviewed object codes and ordered column pairs; Data Loader owns CSV upload and initiation for full_import | Do not bypass the native helper or require MappingNumber for full_import |
| Mapping-only preparation | Strong | The reusable structure and hierarchy mappings can be created or reused without a country file, UCM upload, import activity, or polling | Do not imply that mapping completion imported geography data |
| Mapping drift | Strong | Duplicate names or changed column pairs block execution until reviewed | Do not patch, delete, overwrite, or choose an arbitrary mapping |

## Output Rules

| Situation | What Happens |
|---|---|
| User asks what the skill configures | Explain only country structure and hierarchy master data |
| User asks to enable DaaS or Loqate as part of this geography setup | Validate the two named profile values and, when needed, show `ORA_HZ_ENABLE_DAAS_LOQATE`, its safe current state, and proposed `Y`, then explicitly ask whether the user wants Loqate as the source for geography data and explain that choosing it requires enabling the profile option; do not configure unrelated DaaS features |
| User asks to configure geocoding or address cleansing | Explain that those are separate setup activities and do not perform them through this task |
| Profile validation completes | Report the validation result for both named profile options, explain what each controls, and when enablement is needed display `ORA_HZ_ENABLE_DAAS_LOQATE` and proposed `Y` in the Loqate question |
| Both required profile values already match | Report both as validated and continue without changing them or asking for confirmation |
| Approved profile changes complete | Report every applied current-to-new value change, either immediately or in the final summary |
| ESS submission succeeds | Report the requestId as the job ID immediately; do not wait for terminal completion to disclose it |
| ESS command yields process output | Retain and poll the same process handle, then read the durable submission checkpoint; an empty first chunk is not an empty Fusion response |
| ESS output is interrupted | Recover from the persisted checkpoint first, then from one exact read-only correlation query; never submit a replacement request automatically |
| ESS succeeds | Explain both requested geography outcomes, include the job ID, clarify that geocoding and address cleansing remain separate, and ask whether to set up another country |
| ESS is still running | Report pending status and job ID rather than claiming configuration is complete |
| Lookup or Fusion API call fails | Proactively state the failed stage, safe error summary, and recommended action; ask one focused follow-up question when user information is required |
| ESS fails | Report the job ID, safe ESS failure summary, completed profile changes, and recommended action without waiting for a troubleshooting request |
| Existing country data blocks the import | When the ESS diagnostic unambiguously says the data already exists or was already imported, state that plainly, include the job ID, say that no new import was performed, and ask whether to set up another country; do not retry, delete, or replace data |
| User declines Loqate after a mismatch | Make no profile changes, do not submit the import, and explain that the country structure and hierarchy can be defined manually in Manage Geographies |
| User provides another country after success | Start a fresh single-country run, repeat all prerequisite checks, and create separate persistence and job identifiers |
| User supplies custom structure/hierarchy | Explain the normalized levels, geography counts, parent coverage, identifiers, files, checksums, import order, and creation-only boundary before execution |
| User asks to prepare mappings | Show selected stable names, object codes, complete column pairs, fingerprints, target environment, Data Loader authorization, and create-or-reuse behavior; state that no geography data will be imported |
| Mapping is reused or created | Report each stable name, MappingNumber, fingerprint, and outcome, while keeping Data Loader credentials and wrapper details internal |
| Data Loader does not authorize the REST core service | State that the exact preview is ready but the authorization gate failed; do not say that Data Loader job submission/status is the blocker and do not implement task-local Fusion REST |
| Custom structure import reports that it already exists | Stop the structure stage and report already present; do not follow Oracle's destructive delete-and-reimport fallback because this skill is creation-only |
| Custom hierarchy succeeds | Report the ImportActivityId, completed stage, available record counters, and Manage Geographies verification path |
| Custom hierarchy partially fails | Preserve completed structure or rows, show an errors array and report IDs, and require a reconciled new instruction before any retry |

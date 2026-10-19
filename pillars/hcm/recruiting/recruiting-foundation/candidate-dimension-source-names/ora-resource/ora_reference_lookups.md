# Reference Lookups

## Fresh task export

After retrieval preflight, invoke `shared.setup-export.task-level-export` for
`ORA_MANAGE_CANDIDATE_DIMENSION_SOURCE_NAMES` in normal data-export mode.
For an all-sources request, supply no export criteria and do not use template
mode. Follow that skill's task discovery and CSV capability checks before
creation, then its shared FSM engine for create, poll, and download.

Use the existing task-level scripts from the repository root. For explicit
output paths, use `create_setup_task_csv_export.py` followed by
`get_setup_task_csv_export_result.py` from
`shared/setup-export/task-level-export/scripts/`. Pass the same selected
`--properties` and `--token-cache` to discovery, creation, and result retrieval;
bind the result request to the returned `ProcessId` and exact task code.
Use explicit filesystem-safe filenames under
`project/{project_id}/exports/recruiting/recruiting-foundation/candidate-dimension-source-names/`;
do not embed a raw environment URL in a filename.

Retain the process receipt before polling. Poll for at most 300 seconds at
15-second intervals. Download the completed package or failed process log.
A missing or uncertain process ID is a blocker, not permission to create a
second export. Stop on failure or timeout and preserve the original process
identity; do not automatically resubmit or start another polling window.
The authentication skill's token refresh is distinct from export resubmission.

## Verify and map export

Use the fresh export as the source of truth for retrieval and identity
resolution. Verify ZIP integrity, exact task and environment identity, and
completed export metadata before reporting rows. A CLI status of unknown does
not establish success; use the original process status and downloaded metadata.
Require both named CSV files and unambiguous required headers. Reject malformed
rows, duplicate base identities, unmatched base rows, and multiple matching
translations for the selected language instead of silently dropping or merging them.

| User-facing field | Export source | Rule |
| --- | --- | --- |
| Display Sequence | `ORA_IRC_DIMENSION_SOURCE_NAMES_B.csv` / `Sequence` | Preserve verbatim; blank means `Not populated in fresh export`. |
| Name | `ORA_IRC_DIMENSION_SOURCE_NAMES.csv` / `SourceDisplayName` | Use the explicit display language; otherwise require a unique `Language = SourceLang` row. |
| Source URL | `SourceUrlValue` | Treat as a displayed value; do not infer an editable contract. |

Join base and translation data through `SourceUrlValue` plus `SourceMedium`. Never use displayed Name as the join key. No other export columns are part of the user-facing task scope.

Report the exported base-row count and only Display Sequence, Name, and Source
URL. Keep blank values as documented by the defaulting rules. Preserve the
export order; do not invent a Display Sequence from row position. Say
"returned by the fresh export" rather than claiming unverified coverage of
every row in the UI. Export evidence alone does not establish that UI-only or
seeded rows are included. Keep process IDs and artifact paths in the project
run record unless the user requests metadata. Inspecting a supplied older
artifact must be labeled with its actual freshness, never presented as a new
live retrieval.

Select the display language established by the request or verified session context. Without an explicit language, retain the unique source-language rule. Several translations can legitimately have Language equal to their own SourceLang; this does not duplicate the base source. Never select the first translation or fall back silently when the selected language is absent. State the display language in the retrieval report.


## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_source_export | Retrieve, rename, Add Row or internal validate_import after shared export | The exact downloaded completed baseline; in validate_import use the preserved baseline and final candidate | Validate task/environment metadata; join SourceUrlValue and SourceMedium; select explicit display language or unique Language = SourceLang | Base rows, translation rows, current Name, URL, Sequence, language and package contract | BLOCKED or AMBIGUOUS_SOURCE; never select the first translation or fabricate an omitted source |

The graph resolves already downloaded evidence. Fresh export creation belongs to the
shared workflow described above; Task Hook validation never repeats it.

## Package contract

Require unique ZIP member names and valid CRCs, the two named CSVs and
ASM_SETUP_CSV_METADATA.xml. Metadata must identify this exact task, selected ProcessEnv,
ProcessType EXPORT and ProcessStatus COMPLETED. CSV headers must be unique and each
row must have the header width; preserve header order and encoding from the export.

| Member | Expected fields |
|---|---|
| ORA_IRC_DIMENSION_SOURCE_NAMES_B.csv | SourceUrlValue, SourceMedium, ModuleId, Priority, Sequence, SourceMediumUrlValue, SourceName, UrlHeaderRegex |
| ORA_IRC_DIMENSION_SOURCE_NAMES.csv | ORA_IRC_DIMENSION_SOURCE_NAMES_B.SourceUrlValue, ORA_IRC_DIMENSION_SOURCE_NAMES_B.SourceMedium, Language, SourceName, SourceLang, SourceDisplayName |

Base business identity is SourceUrlValue + SourceMediumUrlValue + SourceMedium.
The TL parent reference omits medium URL, so also require a unique base URL/medium
pair and unique URL/medium/language translation keys. Reject orphan translations.
For retrieval every base row must have exactly one selected-language translation.
For rename, use the unique source-language row (Language = SourceLang), not a display
translation from another language. If that is ambiguous, stop for exact language evidence.

## Product source references


Reviewed 2026-09-11 in the currently indexed FUSIONAPPS_PT.V2MIBHCMIRC_LINUX.X64 source. These references establish fields and defaults; they do not prove a particular target import completed.

- [Oracle Add a Candidate Source](https://docs.oracle.com/en/cloud/saas/talent-management/faimh/add-a-candidate-source.html) documents adding a Name through the setup task. It does not document a custom Source URL input or CSV creation recipe.
- [DimensionSetupBean.java, lines 146-157](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBHCMIRC_LINUX.X64/fusionapps/hcm/components/hcmRecruiting/sourceTracking/core/publicUi/src/oracle/apps/hcm/recruiting/sourcetracking/core/publicUi/bean/DimensionSetupBean.java#146) creates a direct-source row with ORA_DIRECTSOURCE, medium URL direct source, and next UI Sequence. Lines 97-102 derive a missing URL from trimmed lowercase Name and set SourceDisplayName; import with an explicitly supplied URL retains that URL rather than invoking this UI derivation.
- [DimensionDefinitionsEO.xml, lines 55-129 and 225-254](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBHCMIRC_LINUX.X64/fusionapps/hcm/components/hcmRecruiting/sourceTracking/core/publicModel/src/oracle/apps/hcm/recruiting/sourceTracking/core/publicModel/entity/DimensionDefinitionsEO.xml#55) exposes writable SourceUrlValue, SourceName and SourceDisplayName with precision 2000; requires SourceMedium and SourceMediumUrlValue; Sequence is nullable with precision 16. Lines 263-300 define the unique alternate key as SourceUrlValue plus SourceMediumUrlValue plus SourceMedium. Surrogate DimensionId is generated on insert.
- [SourceTrackingAMImpl.java, lines 281-336](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBHCMIRC_LINUX.X64/fusionapps/hcm/components/hcmRecruiting/setup/migrationService/src/oracle/apps/hcm/recruiting/setup/migrationService/applicationModule/SourceTrackingAMImpl.java#281) resolves alternate keys, imports MANAGE_DIMENSIONS.xml through MigratorHelper.readXML, and commits. Partial failures are permitted by that implementation, so accepted initiation cannot substitute for per-load result verification.
- [Migration DimensionDefinitionsVO.xml](https://codesearch.oraclecorp.com/source/xref/FUSIONAPPS_PT.V2MIBHCMIRC_LINUX.X64/fusionapps/hcm/components/hcmRecruiting/setup/migrationService/src/oracle/apps/hcm/recruiting/setup/migrationService/view/DimensionDefinitionsVO.xml#100) maps the base fields to the entity. The target's fresh ASM_SETUP_CSV_METADATA.xml supplies exact CSV columns and base/TL relationship; preserve it byte-for-byte.


## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CDSN.RESOLVE_EXPORT | step | 30 | reference_lookup | resolved->CDSN.APPLY_DEFAULTS;blocked->CDSN.HANDLE_ISSUES | CDSN.CHECK_DEPENDENCIES | stop | Read the existing verified artifact; translation guidance uses verified UI evidence and performs no export lookup |

# User-friendly output

Use these patterns for every Data Loader result. Return the complete Markdown report directly in chat. Inline HTML rendering is disabled; helper CLIs emit the complete Markdown report even when the deprecated `--inline-output` option is supplied.

## General rules

- Lead with the outcome and place result data in narrow two- or three-column tables where practical.
- Pair symbols with text so meaning never depends on color or an icon alone: `✅ Succeeded`, `🟡 In progress`, `❌ Failed`, and `❔ Not available yet`.
- Translate status codes such as `ORA_IN_ERROR` to a friendly status. Never show technical error codes in data-set diagnostics.
- Show zero when meaningful. Omit null, empty, duplicate, secret, and implementation-only fields.
- Preserve every actionable business diagnostic in the chat. Use numbered table rows for multiple diagnostics.
- Never expose credentials, authorization headers, Base64 content, raw API responses, or configured run IDs.
- A failed or active result ends with a concrete next-action table. A completed success does not add generic advice.
- Treat attribute-detail, sample, initiation, and status responses as complete Markdown result envelopes. Include direct links to every requested or generated local deliverable, including sample XLSX, explicit DAT, attribute-details workbooks, every successfully saved FSM ProcessLog, and every generated non-FSM Data Loader error log. Do not add technical narration, implementation details, authentication notes, or raw output.
- Keep working commentary to a required initial notice, a user action or approval, a genuine blocker, or one compact update during a long-running operation. Do not narrate internal retries, token-cache handling, command selection, temporary paths, authentication implementation details, or business-object alias and discriminator resolution.
- When an explicit load request includes `auto-approve`, `auto approve`, `auto confirmation`, `approve without asking`, `skip confirmation`, `skip approval`, or equivalent unambiguous wording, do not ask for submission confirmation. Otherwise, render the approval-required report only after source validation and, for a selected task, successful Task Hook validation and internal preview creation. Accept a clear contextual affirmative, such as `yes`, `go ahead`, or `submit it`, for the exact validated source; do not require a fixed approval keyword. A task-validation failure is a blocker report and must omit approval feedback. Continue only after all required validation gates pass; mapping and required-input prompts remain blockers, not approval prompts.
- After later approval, reuse the persisted approved artifact and verify only its internal integrity and bound execution context. Do not rerender validation, expose envelope paths or digests, reopen the original source, rebuild the artifact, refresh live findings, or add those internal checks to the initiation report.
- Multi-XLSX validation checkpoints are transient working updates written to `stderr` with immediate flushing. Keep them internal unless a long-running operation requires a compact progress update; consolidate rather than relaying every checkpoint. Do not include them in the final Markdown report or persisted files.
- Use the established Markdown report shapes for samples, attribute details, mandatory attributes, key attributes, initiation, validation, status, and failures.
- Never create or attach token-usage logs, project run records, diagnostic Markdown, audit files, manifests, auxiliary summaries, or other unrequested artifacts. Failures remain in the Markdown error report.

## Attribute details

Create only `<business-object>_attribute-details.xlsx` and return exactly the compact schema summary plus its single link:

| Item | Value |
|---|---|
| Business Object | `<UIName>` |
| Discriminator | `<BusObjTopDiscriminator>` |
| Sections | `<sectionCount>` |

| File | Link |
|---|---|
| Attribute details | `<local file link>` |

Do not create or link the editable sample or key-fields workbook for this request.

## Successful initiation

For one initiated load, use this compact shape and stop without polling:

`## Data Load In Progress`

`The data load for <friendly load type> Load Type was initiated successfully.`

| Item | Value |
|---|---|
| Data Set Name | `<dataSetName>` |
| Content ID(Request ID) | `<ContentId> (<RequestId>)` |

For CX Import and FBDI only, insert `Business Object Name` and `UCM Account` before `Content ID(Request ID)`. Use `Data Loader - CX Import`, `Data Loader - FBDI`, `Data Loader - FSM`, or `Data Loader` as the friendly load type in the success sentence. For multiple loads, show the friendly load type in each load heading. Render exact Run Book task names in progress rows; never show task action codes.

For ordinary CSV/XLSX sources with non-exact mappings, place `### Mapping verification` before the initiation table. Include `Source Header`, `Fusion Attribute`, `Match Rule`, and `Verification`; label deterministic mappings `✅ Verified`. Exact attribute headers remain implicit.

When a homogeneous DAT/XLSX group is submitted alongside one or more FSM ZIPs, render the same detail table under `### Load 1`, `### Load 2`, and so on for every independently accepted load, then stop without polling.

Return this initiation report verbatim as the complete final response. Do not
replace it with bullets, add a file citation, restate its values in prose, or
append an agent-authored summary. For a task-routed load, retain the helper's
Run Book progress table exactly as emitted.

## Sample XLSX and explicit DAT generation

Begin XLSX results with `This is the generated sample files:` and DAT results with `This is the generated sample file:`. Then show the generated artifacts:

| File | Link |
|---|---|
| Editable sample or DAT sample | `<local file link>` |
| Attribute details | `<local file link>` |
| Key fields | `<local file link, standard XLSX only>` |

Follow with a numbered sections table and one compact hierarchy preview:

| Section | Details |
|---|---|
| `<parent>` | `<two to four business-friendly label/value pairs>` |
| `<child or DFF>` | `<values or a clear headers-only statement>` |

Prefer user-facing labels and meaningful values. Omit technical IDs, `RestAction`, `ParentIdentifier`, source references, raw REST records, server-issued identifiers, the REST host, and schema implementation details.

Every XLSX sample, including a populated XLSX sample, creates exactly the editable, attribute-details, and key-fields workbooks. Population applies only to the editable workbook.

For a multi-RESTBO sample request, begin with `These are the generated sample files:`. Show one ordered file table with `Business Object`, `File`, and `Link`, followed by one `Business objects and sections` table. XLSX mode lists three files per object. Do not show server IDs, schema implementation details, staging paths, or authentication information.

## Status-only requests

Use `python3 scripts/get_data_load_info.py <request-id-or-ucm-content-id> --status-only`. The helper validates UCM Content IDs and sends them to Fusion as quoted string filters. When a matching data set exists, always return its data-set status and counts, including for successful loads:

| Data Set | Status | Total | Loaded | Failed |
|---|---|---:|---:|---:|
| `<DataSetName>` | `<status>` | `<ObjectTotalCount>` | `<ObjectLoadedCount>` | `<ObjectErrorCount>` |

Populate `Data Set` with the exact `DataSetName`, then fall back to `UIName`, `BusinessObject`, or `Unknown data set` only when Fusion omits it. When `dataSetErrors` returns one or more items, follow the counts with every returned error and one concrete corrective action. Do this regardless of the overall status or reported error counters. For a data set whose `SourceType` is exactly `FSM`, add parseable failed ProcessLog business objects to the same Diagnostics table after MsgText rows and provide only a readable UTF-8 ProcessLog attachment, with literal control-character escapes decoded and line endings normalized. For `SourceType: FBDI`, retrieve every distinct ESS process through `reviewProcessHierarchy`, download each available process-log attachment, add only useful business-readable error summaries to the Diagnostics table after MsgText rows, and link one readable complete log per process. Render `ORA_FBDI_IMPORT` as `FBDI Import` and `ORA_FBDI_LOAD` as `FBDI Load`. Aggregate repeated product errors with an occurrence count; exclude informational notes, polling/checkpoint messages, server identifiers, interface-limit tables, and stack traces. Do not display data-set, process, or attachment identifiers. Continue to query Failed Lines and Data Set Object Errors for FBDI as supplementary evidence. For a data set whose `SourceType` is exactly `ORA_CX_IMPORT`, retrieve its CX business objects and embedded error records; follow a paginated child-error `self` link when supplied. Create and link one readable CX error log only when at least one business object has errors or CX diagnostic retrieval fails. It must show business object and file context plus record number, error code, error type, and error message; warnings alone do not create a CX error log. For every other non-FSM data set, query the filtered Failed Lines and Data Set Object Errors child resources and keep those row-level details out of the Markdown report. Create and link a `.log` only when either resource returns diagnostics or its retrieval fails; do not show an empty error-log attachment. Format a qualifying log as a count summary followed by friendly numbered error records: use `MessageText` only when it is resolved; when it is blank, unavailable, `-1`, or contains any unresolved `{...}` placeholder, use a nonblank `Message`, retaining the original `MessageText` only when no usable `Message` exists. Preserve raw `FileLine` values only in a correlated Technical Details section. Save logs under `~/.codex/data-loader-status-logs/<request>/` unless `--diagnostic-log-output-dir` is supplied, and link every saved status log in the Markdown local-deliverable section. If a diagnostic endpoint or file write fails, preserve status and show a Markdown warning. If no matching data set exists yet, return only a compact two-column `Not available yet` status table. Continue to omit request IDs, data-set IDs, UCM IDs, and all other attachments.

## Status and progress details

Show the business-object outcome:

| Data Set | Status | Total | Loaded | Failed |
|---|---|---:|---:|---:|
| `<DataSetName>` | `<status>` | `<ObjectTotalCount>` | `<ObjectLoadedCount>` | `<ObjectErrorCount>` |

Do not infer missing counts. Do not show request IDs, data-set identifiers, processing-stage fields, file-line counts, timestamps, or other server metadata unless explicitly requested.

When `dataSetErrors` returns items, follow with:

| # | Business Object | Stage | Error |
|---:|---|---|---|
| 1 | `<UIName or BusinessObject>` | `<OriginatingProcessName>` | `<MsgText>` |

Render only a nonempty `MsgText` from each `dataSetErrors` item, preserving it exactly as Fusion returned it. Do not read `GroupByExprVal`, nested error details, or another error field; omit items with missing or blank `MsgText`, and omit the Errors/Diagnostics section when no rows remain. Display the error's `UIName`, then its `BusinessObject`, then a matched data set's `UIName` or `BusinessObject`; otherwise display `Unknown business object`. Do not display the ZIP data-set name in the Errors table. Follow a rendered error table with one concrete corrective action. If Fusion returns no error items, show a compact result table stating that Fusion returned no data-set errors.

When no matching data set exists, use a `Not available yet` status table followed by a next-action table explaining that error lookup becomes available only after Fusion returns a data set.

## Validation and API failures

When a CX Import ZIP or direct CSV group has no mapping CSV and no supplied business-object code, return only `What is the CX Business Object code for this file?` Treat this as an input prompt, not a failure: do not render a failure table, error icon, or generic next action. The CLI exits nonzero because the request is awaiting required input.

For unresolved CSV/XLSX review rows, render `## Mapping stage` followed directly by a `Source | Type` table, then `Source Header`, `Fusion Attribute`, `Match Rule`, and `Mapping confidence`. Include every non-exact automatic mapping as context and omit exact header matches. When any header is unmapped or has less than 100% confidence, stop before Task Hook validation, UCM upload, and initiation; do not link an archive at the mapping stage. Mapping input is required validation, not an approval prompt, including when auto-approval was requested. After resolution, complete task validation when a task is selected; request approval only if that validation also succeeds, without displaying an archive SHA-256.

Render every validation-only result as a Markdown envelope: `## Business Object Validation`, followed directly by a `Source | Type` table, and `### Validated upload` as an `Item | Value` table with a clickable `Validated ZIP` row when an archive is saved. Do not display a SHA-256 or ask for approval. For direct validation, show `### Automatic header corrections` only when an automatically mapped source header differs from its exact Fusion attribute; do not list exact matches. After Mapping stage, show `### User-approved attributes` containing only manual or approved-fuzzy mappings; do not list automatic or exact matches. Both tables use `Source Header` and `Fusion Attribute` columns. Show `### Column handling` only when ignored columns must be reported. For CX Import, add `### CX Import files` with one row per CSV in upload order and columns `CSV file`, `ZIP member`, and `Role`; show the mapping file first and label roles `Mapping` or `Data`. Follow it with one `### CX Import details` `Item | Value` table containing available `Object Name` and `UCM Account` rows, in that order. End with `### Validation complete` stating that no data was uploaded. A task-routed load request adds its approval feedback only after Task Hook validation succeeds; a Task Hook blocker omits that feedback. Do not repeat these tables after accepted initiation.

For a multi-DAT or multi-XLSX submission with one or more resolved business-object validation failures, report all failed and eligible objects and state that no data was uploaded. End with a plain-language confirmation question: the failed object could not be included, the eligible objects are ready, and ask whether to continue with only those ready objects. Keep `--skip-business-object` internal; never show command syntax to the user. Do not offer this option for unresolved source, duplicate-target, authorization, archive, upload, or initiation failures.

Use:

| Stage | Result | Details |
|---|---|---|
| `<friendly stage>` | ❌ Failed | `<HTTP status and actionable server message>` |

Then show:

| Next action | Details |
|---|---|
| Required | `<specific corrective action>` |

Preserve the request ID when available, while hiding data-set IDs, document IDs, business-object IDs, credentials, and Base64 content.

When a CX Import upload fails after one or more UCM documents were created, state that initiation did not occur and list the already-created CSV filename and UCM content ID pairs. Do not imply that those documents were retried or deleted.

## CLI Markdown contract

Every successfully saved FSM ProcessLog and qualifying non-FSM Data Loader error log is a required local deliverable and must be linked in the Markdown status report. Every saved FBDI ESS process log and qualifying CX Import error log follows the same rule. Do not create or link an error log when no applicable diagnostics were returned.

`generate_sample_dat.py`, `upload_and_initiate.py`, and `get_data_load_info.py` print these Markdown reports. Do not pass `--inline-output` for chat results; it remains a no-op compatibility option. Their Python functions may return structured dictionaries internally, but JSON is not a supported external output format.

Use `generate_sample_dat.py <business-object> --attribute-details-only --output-dir <directory>` for an attribute-details request. This mode creates exactly one workbook. Initiation helpers create no local output files; status creates only applicable FSM ProcessLogs and qualifying non-FSM Data Loader error logs. None of the helpers creates project workspaces, run records, diagnostic reports, or auxiliary summaries.

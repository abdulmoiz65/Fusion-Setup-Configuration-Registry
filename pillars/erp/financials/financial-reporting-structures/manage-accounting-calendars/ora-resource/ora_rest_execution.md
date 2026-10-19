# Accounting Calendar FSM Execution

## Runtime Sources

| Source | Purpose |
|---|---|
| Fetched template-only package or compatible project baseline | Authoritative metadata XML, CSV filenames, columns, and package structure; fetch once for the project's first run through `shared.setup-export.task-level-export`, then reuse while compatible; never obtain these through a Data Only Export |
| Documented calendar rules and user inputs | Provide technical codes, formats, flags, period geometry, and date values |
| core.data-loader | Mandatory import orchestrator for validation, immutable preview, approval, and execution-route authorization |
| shared.setup-import.task-level-import | FSM execution adapter invoked only by `core.data-loader`; workflow agents never invoke it directly |

## Execution Contract

| Situation | What Happens |
|---|---|
| Direct write REST route is not documented | Do not invent a POST, PATCH, or BOSS contract. Use FSM CSV submitted through the mandatory Data Loader workflow after readiness checks for both new-calendar creation and permitted existing-calendar edits. |
| LOV lookup is required | Use GET only for discovery and comparison; it is not a write contract. |
| Import request is not explicitly approved | Produce preview/readiness only and stop before live import. |
| Live import is approved | Route through `core.data-loader`; Data Loader alone invokes the FSM task-level adapter after its task validation, immutable preview, and approval gates authorize it. |
| Data Loader task context or approved-loader payload is unavailable | Stop before submission. Do not treat a chat approval or a prepared ZIP as a substitute for Data Loader authorization. |

## Endpoint

| Action | Method | Path |
|---|---|---|
| Calendar existence lookup | GET | /fscmRestApi/resources/11.13.18.05/accountingCalendarsLOV |
| Period comparison lookup | GET | /fscmRestApi/resources/11.13.18.05/accountingPeriodsLOV |
| Ledger association lookup | GET | /fscmRestApi/resources/11.13.18.05/ledgersLOV |
| Period lifecycle lookup (mandatory eligibility evidence for existing-period UI-core edits; diagnostics otherwise) | GET | /fscmRestApi/resources/11.13.18.05/accountingPeriodStatusLOV |
| FSM task import | `core.data-loader` | Adapter selected only through the Data Loader authorization workflow |
| FSM task current-data export for permitted update | `shared.setup-export.task-level-export` | Full `GL_MANAGE_ACCOUNTING_CALENDARS` export through `setupTaskCSVExports`; no criteria; isolate the exact LOV-resolved target |

Send `Authorization: Bearer <token>` and `REST-Framework-Version: 9` on every
`accountingPeriodStatusLOV` request. A convenience-client invocation with no
captured HTTP status or body is not proof of an empty result; retry the explicit
GET with both headers.

## Preview Pattern

| Step | Requirement |
|---:|---|
| 1 | List metadata XML, CSV files, required columns, generated values, default source evidence, unresolved values, and package approval status. |
| 1a | Query `accountingCalendarsLOV` for the exact `UserPeriodSetName`; require zero matches before generating a create package. |
| 1b | Check the project for a validated template baseline matching `GL_MANAGE_ACCOUNTING_CALENDARS`, the target environment, Fusion release, artifact fingerprint, members, and headers. Reuse it only when every check passes. |
| 1c | When no compatible baseline exists, automatically route one template fetch through `shared.setup-export.task-level-export` using `setupTaskCSVTemplateExports`; validate it and persist it as the project baseline. Treat this template acquisition as normal preflight and do not ask for separate conversational approval. Never substitute `setupTaskCSVExports` for template acquisition. |
| 1d | For creation, use the approved generic bootstrap profile and documented defaults with the validated template baseline. Derive business values from documented calendar rules and user inputs, record every selected code in the immutable preview, and never request or run a Data Only Export. |
| 1e | For a permitted update, resolve the current-value carrier before package authoring. Prefer a successfully loaded and post-load-verified FSCR creation package from the current project/session. Otherwise automatically run one full task data export without criteria, record its process and package hash, and isolate exactly one parent matching both LOV-resolved names plus only its children. Do not ask for separate export approval. Block if the exact target is absent, duplicated, ambiguous, or inconsistent. |
| 2 | Reject UI labels in code fields; use documented technical codes. |
| 3 | Confirm every technical lookup/default is resolved before ZIP creation. |
| 4 | For new-calendar CSV creation, confirm encoding, header order, parent linkage, and count reconciliation. For a permitted existing-calendar FSM update, confirm exact identity, immutable preview, explicit approval, and immutable `UserPeriodSetName`/`PeriodSetName`. Include one complete `GL_PERIOD_SET.csv` parent row that preserves all required existing header values; an identity-only parent row is invalid. For an existing-period edit, permit `PeriodNum`, `QuarterNum`, `StartDate`, `EndDate`, and `AdjustmentPeriodFlag`; preserve both period-name fields because a changed `PeriodName` is imported as a new row and an `EnteredPeriodName`-only change does not rename the displayed period. Retain original identities for lifecycle matching and preserve protected fields. When ledgers exist, call the status LOV with the required framework header, automatically paginate and reduce each full ledger history by exact affected `PeriodNameId`, retain all application rows, require `N` in every matching row, and proceed without a user prompt. A successful complete matchless or empty result for an individual ledger/period is `NO_STATUS_INSTANTIATED` and passes even when other ledgers return all-`N` rows; unrelated history is not a blocker. Otherwise use the exact zero-ledger/direct-status branch. Validate the resulting full calendar against every calendar rule. |
| 5 | Record package-review evidence proving nonblank, aligned `CalendarStartDate` and `LatestYearStartDate` values. |
| 6 | Record the selected UI naming format, `SamplePeriodName`, first non-adjusting period, and every adjustment name. Require each adjustment name to be `<two-digit PeriodNum>_<base name rendered for that adjustment row>`; e.g., `04_Mar-27` for a month-based format and `07_7-27` for a period-number format. For monthly `1_BEGIN_1_END`, assert opening adjustment / 1 at fiscal start, normal fiscal months / 2?13, and closing adjustment / 14 at fiscal year end; `FirstPeriod` and `SamplePeriodName` must match the first normal period generated from the selected format. Block period 0, a next-year first period, or any naming mismatch. |
| 7 | Immediately before submission, re-parse the immutable ZIP and confirm counts, date alignment, naming reconciliation, period continuity, adjustment overlap, and `PeriodSetName` linkage still match the approved preview. For an existing-period edit, rerun fully paginated ledger discovery. If ledgers exist, rerun every per-ledger status query with `REST-Framework-Version: 9`, automatically apply the same exact affected-`PeriodNameId` reduction, require `N` in every retained application row, preserve successful empty/matchless cells as `NO_STATUS_INSTANTIATED`, and compare the compact eligibility-matrix fingerprint with the approved evidence. If the result is still exactly zero ledgers, rerun every direct period-identity status query and returned-ledger ownership resolution and require no row attributable to the target. Any changed, ambiguous, inconsistent, truncated, inaccessible, or ineligible evidence stops submission. |
| 8 | For a batch, require an independently validated preview and approval fingerprint for every calendar. Do not submit a mixed batch with any invalid or unresolved calendar. |

## Live Pattern

| Step | Requirement |
|---:|---|
| 1 | Require explicit live-import approval after readiness passes. |
| 1a | Repeat the exact `accountingCalendarsLOV` query immediately before submission. Stop on any match or unavailable/ambiguous result. |
| 1b | A batch may generate and validate all calendar packages together. When two or more calendars can resolve to the same newly created period-type definition—same standard frequency, periods per fiscal year, and year-in-name semantics—submit their FSM imports serially and wait for each inner FSM process to reach a terminal state before starting the next. Do not rely on concurrent imports to coordinate creation of shared period-type metadata. |
| 2 | Use `core.data-loader` as the mandatory import orchestrator. Data Loader must invoke `shared.setup-import.task-level-import` through its FSM handoff; workflow agents must not invoke that adapter directly. Do not persist credentials or generated package artifacts in the skill. |
| 3 | Resolve the final outcome from the inner FSM import process and its ProcessLog. Retain any outer Data Loader request ID as diagnostic context only; do not report an outer no-dataset or failed status as the calendar-import outcome when the inner FSM process completed successfully. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| CAL.PREVIEW | decision | 8 | preview_gate | approved->CAL.APPROVAL;blocked->CAL.STOP_DEFAULTS | CAL.GENERATE_CSV | stop | Generated package is ready for review |
| CAL.APPROVAL | decision | 9 | approval_gate | approved->CAL.DONE_READY;declined->CAL.DONE_READY | CAL.PREVIEW | stop | Live import is requested |
| CAL.DONE_READY | terminal | 95 | terminal | none | CAL.APPROVAL | stop | Readiness complete; import is either approved for shared execution or withheld |
| CAL.UPDATE_PREVIEW | decision | 12 | preview_gate | approved->CAL.UPDATE_APPROVAL;blocked->CAL.STOP_DEFAULTS | CAL.GENERATE_UPDATE_CSV | stop | Existing-calendar FSM update package is ready for immutable review |
| CAL.UPDATE_APPROVAL | decision | 13 | approval_gate | approved->CAL.DONE_UPDATE_READY;declined->CAL.DONE_UPDATE_READY | CAL.UPDATE_PREVIEW | stop | Live existing-calendar FSM update is requested |
| CAL.DONE_UPDATE_READY | terminal | 94 | terminal | none | CAL.UPDATE_APPROVAL | stop | Existing-calendar update readiness complete; Data Loader may execute only after approval |

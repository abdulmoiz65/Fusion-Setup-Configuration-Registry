# Accounting Calendar Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required template column is unknown | Stop package generation. If the persisted project baseline is absent, stale, incomplete, or unverifiable, obtain a fresh approved template-only package through `shared.setup-export.task-level-export`, validate it, and replace the baseline. Do not request a Data Only Export. |
| A Data Only Export is suggested for creation, general lookup, or import-failure troubleshooting | Do not run it. Creation remains template-only, and an import failure does not authorize a new export. |
| A permitted update lacks a verified current-session FSCR source | Automatically run one full current-data export for `GL_MANAGE_ACCOUNTING_CALENDARS`; do not use criteria. Treat it only as the exact target's current-value carrier. |
| A full update-source export omits the exact target, returns more than one matching parent, or has inconsistent child linkage | Stop the update. Do not use a similar name, infer the missing header, retry with unsupported criteria, or use unrelated calendar rows. Report the export process and missing/ambiguous target evidence. |
| Import validation fails unexpectedly | Preserve the redacted process result, classify it, correct the definition, and rerun readiness. Do not run another Data Only Export as a troubleshooting response; refresh the update source only when independent evidence proves the retained source became stale. |
| Existing calendar differs | Show differences and require update-versus-new direction. |
| Import is declined | Keep only readiness output; do not submit a package. |
| Fusion reports a missing UserPeriodSetName despite a populated CSV | Inspect GL_PERIOD_SET.csv for a UTF-8 BOM; rebuild without BOM, rerun readiness, and obtain approval before retry. |
| Fusion skips child periods because the GL_PERIOD_SET parent row is missing | Stop. Add exactly one complete existing-calendar parent row, preserving its immutable identity, dates, counts, flags, frequency, adjustment policy, naming format, separator, total count, and sample period. Do not use a blank or identity-only parent row. Revalidate and obtain fresh approval before retry. |
| Fusion reports null `SamplePeriodName`, `PeriodNameSeparatorCode`, or `NonAdjPeriodFreqCode` for an existing-period update | Stop. The parent row is incomplete. Source and preserve the current immutable header values in `GL_PERIOD_SET.csv`; do not default, clear, or change those fields. Revalidate and obtain fresh approval before retry. |
| Fusion reports period-name or SamplePeriodName conversion errors | Recheck PeriodNameFormatCode, PeriodNameSeparatorCode, SamplePeriodName, and their compatibility with the selected frequency. |
| OTHER-frequency import reports a null separator or SamplePeriodName conversion error | Stop. Populate the reviewed `PeriodNameSeparatorCode` and first manual `SamplePeriodName`, rebuild the immutable ZIP, rerun readiness, and obtain fresh approval. |
| Fusion reports an adjustment-overlap or row-shape failure | Stop. Compare the selected adjustment frequency with the exact adjustment row count, period numbering, and overlap dates. For weekly `1_BEGIN_1_END`, require the reviewed 54-row opening/52-standard/closing pattern; do not retry a 52-standard-plus-one-adjustment package. |
| `LatestYearStartDate` is blank or Fusion reports `date must not be null` | Stop. Set `LatestYearStartDate` to the latest non-adjusting `YearStartDate`—equal to `CalendarStartDate` for a new single-year calendar—then rerun deterministic readiness validation and obtain fresh approval before retry. |
| Lookup endpoint fails | Report a runtime failure; do not treat it as proof that the calendar does not exist. |
| A request attempts deletion of a calendar or period | Return unsupported-operation status before lookup, package generation, UI navigation, or submission. |
| A request contains an unsupported calendar type, frequency, retail pattern, or adjustment policy | Return input-validation status with the allowed values. Do not default, substitute, or generate a near-match. |
| Fusion reports a context value is not in the list of values | Stop. Identify the header or period context/category/DFF column, clear the derived value, validate the template field map, rebuild the immutable package, and require fresh approval before retry. |
| `ReferencedByLedger` is unavailable through a LOV or omitted from a lookup response | Continue. It is not a readiness, approval, or submission prerequisite; retain the template field blank unless a reviewed template literal is required. |
| An Other-frequency calendar has a missing or nonpositive standard-period count | Stop. Require a positive whole-number standard-period count and complete manual rows, then rerun package validation before a fresh approval. |
| A generated calendar using Other adjustment frequency has an invalid adjustment count | Stop. Require a positive whole-number adjustment count, regenerate the appended adjustment rows, and rerun package validation before a fresh approval. Do not substitute the standard-period count. |
| A permitted existing-calendar update lacks approval, identity evidence, or immutable Data Loader preview | Stop the FSM/Data Loader update and request the missing evidence. Do not convert it into a create or bypass the approval workflow. |
| A display-name update is requested | Stop. Preserve `UserPeriodSetName`; do not generate or submit an FSM rename package. |
| A description update would alter `UserPeriodSetName`, `PeriodSetName`, parent linkage, or a period row | Stop and preserve the existing technical identity and periods. |
| A period-name-format update is requested without adding a fiscal year, uses a format not allowed for the frequency, or alters historical rows | Stop and require a compliant new-year update design. |
| An existing-period name change is requested | Stop before preview or submission. In this FSM CSV import, a changed `PeriodName` is treated as a new period and produces duplicate-period-number errors; changing only `EnteredPeriodName` does not rename the displayed period. Preserve both name fields. |
| An existing-period field outside the UI-editable core allow-list is requested | Stop before preview or submission and identify the protected field. The core allow-list is `PeriodNum`, `QuarterNum`, `StartDate`, `EndDate`, and `AdjustmentPeriodFlag`; period-name fields are blocked for existing rows in this FSM route. Additional Information/DFF edits require a separate validated context/segment contract. |
| A status lookup returns a ledger's full period history | Continue automatically. Complete pagination, reduce the response by exact affected `PeriodNameId`, retain every matching application row, ignore unrelated history, build the affected-period x ledger coverage matrix, and evaluate it. Do not report the full history as incomplete evidence, pause for user-assisted isolation, or require another conversational request to check it. |
| The convenience client returns no captured status response | Do not call it an endpoint failure or an empty result. Retry the explicit `accountingPeriodStatusLOV` GET with the same OAuth bearer token and `REST-Framework-Version: 9`. Block only if the explicit request remains inaccessible or incomplete. |
| A successful complete per-ledger status result has no affected-period match or no rows | Continue. Record `NO_STATUS_INSTANTIATED` for each affected ledger/period and treat it as eligible without synthesizing `ClosingStatus=N`. Apply this independently, so an empty result for one associated ledger may coexist with all-`N` rows from other ledgers. |
| Lifecycle evidence for an affected period is incomplete after deterministic reduction | Stop. For an associated calendar, stop only when an explicit request or page is inaccessible/truncated, identity is ambiguous, evidence is inconsistent, or a retained application row is not `ClosingStatus=N`. A successful complete empty or matchless ledger/period result is not incomplete evidence. For a calendar with a complete exact zero-ledger result, require direct period-identity status queries and resolve every returned LedgerId to prove no row belongs to the target. Do not treat an unavailable response or partial page as zero ledgers/no status. |
| An affected period has `O`, `C`, `F`, `P`, or `W` status | Stop. Do not generate or submit the period edit; one non-`N` row makes the affected period ineligible. |
| Period lifecycle evidence changes before submission | Invalidate the approval and stop. Do not upload unless a fresh complete check still proves either `N` everywhere for associated ledgers or the same zero-ledger/no-attributable-status condition. |
| Proposed period edits violate calendar rules | Stop. Add every genuinely changed row to the explicit request and lifecycle-check set, then validate name synchronization/uniqueness, dates, numbering, quarters, continuity, counts, adjustment policy/overlap, and protected fields. Reject the update when the valid result would require a protected header, year, frequency, policy, or DFF change. |
| A request changes a protected existing-calendar field | Return blocked-update status and identify the protected field. Do not convert the update into a create, delete, or FSM import attempt. |
| A batch has one or more invalid calendar definitions | Return an entity-specific error for each invalid definition and no aggregate success. Preserve valid definitions only as unsubmitted previews. |
| Outer Data Loader status conflicts with FSM process status | Retrieve the inner FSM import ProcessLog and report its terminal result as authoritative, while retaining the outer request as diagnostic context. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Names, dates, frequencies, or rows are invalid | Correct definition before artifact generation. |
| Template metadata gap | Required package member or column is unavailable | Fetch or refresh the approved template-only package, validate and persist the project baseline, or stop; never request a Data Only Export. |
| Approval blocker | Live mutation lacks explicit approval | Stop after preview. |
| Process failed | Shared FSM import reports failure | Retrieve redacted status/log, remediate, and rerun readiness. |
| Ambiguous match | Read-only lookup returns more than one matching calendar | Request calendar ID or more specific identifiers. |
| Unsupported operation | Delete request or protected existing-calendar structural change | Stop without package generation or side effects. |
| Partial failure | Multi-calendar validation or import has mixed entity outcomes | Return each entity outcome; do not report aggregate success. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Import readiness | Every required file, column, generated/defaulted value, evidence source, unresolved item, and approval state. |
| Failure | Environment, task code, process identifier when available, status, redacted diagnostic, and safe next action. |
| FSM calendar failure | Retrieve the setup-task CSV import `ProcessLog` as the authoritative General Ledger diagnostic; Data Loader status alone can omit the business error. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Period-status request | Do not open, close, future-enter, or permanently close periods. |
| Calendar or period deletion request | Do not delete, remove, drop, purge, navigate to a deletion UI, or generate an import package. |
| Protected existing-calendar update | Do not submit a change to calendar start date, frequency, adjustment policy, `UserPeriodSetName`, `PeriodSetName`, parent linkage, period year, header fields, or a period field outside the UI-editable core allow-list. A period-name-format change remains allowed only through FSM/Data Loader while adding a new fiscal year. |
| Unresolved technical defaults | Do not create or submit import ZIP. |
| Blank calendar header dates | Do not create or submit an import ZIP when `CalendarStartDate` or `LatestYearStartDate` is blank. |
| Secret-bearing request | Do not write credentials, headers, or tokens to skills or artifacts. |
| Import failure | Do not retry or alter package contents without user approval. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| CAL.DONE_EXISTS | terminal | 96 | terminal | none | CAL.LOOKUP_EXISTING | stop | Equivalent calendar already exists |
| CAL.STOP_DIFFERENCE | terminal | 97 | terminal | none | none | stop | Existing calendar differs and no decision is supplied |
| CAL.STOP_DEFAULTS | terminal | 98 | terminal | none | none | stop | Technical default is unresolved |
| CAL.STOP_INVALID | terminal | 99 | terminal | none | none | stop | Inputs violate required rules |

## Mandatory Log Review Before Outcome Reporting

Before quoting success or failure for any submitted calendar creation or update, use core.data-loader status/diagnostics to retrieve, persist and inspect the actual inner FSM ProcessLog matching the environment and request/process. Reconcile status with its processed counts, failures, warnings and available detailed error reports. An initiation receipt or loader summary alone is insufficient.

If the log is missing, incomplete or contradicts status, report the API status as provisional and the import outcome as unconfirmed, retaining the request/process IDs and discrepancy. Do not resubmit solely because logs are unavailable. Report mixed results per entity and distinguish log-confirmed processing from saved values verified through declared endpoint/framework routes.

For read-only lookups, validation, no-op or pre-submission rejection, inspect the actual response, diagnostics or evaluated rules before reporting the result; explicitly state when no import was submitted. Do not invent an FSM log for an unsubmitted operation. Include reviewed log counts, warnings/errors and the log link when reporting an import outcome.

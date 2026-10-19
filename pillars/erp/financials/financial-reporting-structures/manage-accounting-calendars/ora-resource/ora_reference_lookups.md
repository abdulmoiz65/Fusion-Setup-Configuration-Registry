# Accounting Calendar Reference Lookups

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| accounting-calendars-lov | Before create | calendar_name | /fscmRestApi/resources/11.13.18.05/accountingCalendarsLOV | UserPeriodSetName | Query `UserPeriodSetName='{calendar_name}'`; require exactly zero matches for a new calendar | Exact match count only | No match permits new-package path; one or more matches block duplicate creation. |
| accounting-periods-lov | Pre-extension validation, existing-period identity/baseline resolution, post-load verification for a new calendar, and verification of added-year or edited rows | calendar identity plus period identifiers | /fscmRestApi/resources/11.13.18.05/accountingPeriodsLOV | PeriodNameId, PeriodSetNameId, PeriodType, PeriodYear, PeriodNumber, StartDate, EndDate, EnteredPeriodName, AdjustmentPeriodFlag | Retrieve every page for the exact calendar. For an edit, resolve every original row, retain its original PeriodNameId, and compare it with the isolated exact-target current-value source; after load prove the requested changes and every unaffected row | Existing-row evidence and immutable original/proposed edit baseline | Block on missing, ambiguous, truncated, or structurally invalid evidence. The endpoint does not expose quarter assignment or complete parent values, so it cannot replace the controlled existing-update current-value source. |
| ledgers-lov | Contextual calendar-to-ledger discovery; mandatory only for an existing-period edit | immutable `PeriodSetName`; returned LedgerIds from direct status queries when the target has zero ledgers | /fscmRestApi/resources/11.13.18.05/ledgersLOV | LedgerId, PeriodSetName, AccountedPeriodType | Query the exact target `PeriodSetName` and retrieve every page. Retain every distinct associated `LedgerId`; do not select only one. A valid complete zero-row result establishes the unassigned-calendar branch. In that branch, resolve each LedgerId returned by direct status queries and prove its PeriodSetName is not the target | Complete target ledger set or verified zero-ledger result; returned-ledger ownership map | This is not a general readiness gate and does not expose a proven average-daily-balance flag. For a period edit, unavailable, ambiguous, or truncated evidence blocks, but a complete exact zero-ledger result selects the direct-status branch rather than blocking. Do not block description, creation, or add-year flows merely because this lookup is unavailable or returns references. |
| accounting-period-status-lov | Mandatory lifecycle eligibility check for an existing-period UI-core edit; otherwise read-only lifecycle diagnostics | Every associated LedgerId plus affected original identities; or each affected original identity when the calendar has zero ledgers | /fscmRestApi/resources/11.13.18.05/accountingPeriodStatusLOV | PeriodNameId, PeriodName, ApplicationId, LedgerId, ClosingStatus, StartDate, EndDate, EffectivePeriodNumber, PeriodYear, PeriodNumber, AdjustmentPeriodFlag | Send `Authorization: Bearer <token>` and `REST-Framework-Version: 9`. Ledger branch: for every associated ledger use `finder=ledgerIdFinder;BindLedgerId=<LedgerId>`, retrieve every page, then automatically reduce the full history by the immutable affected `PeriodNameId` set. Retain every matching `ApplicationId` row; use original name/year/number/start/end/adjustment identity only as an exact cross-check or fallback when the ID is unavailable. Zero-ledger branch: use fully paginated `q` filters on each affected period's original `PeriodNameId`, `PeriodYear`, `PeriodNumber`, `StartDate`, and `EndDate`; resolve every returned LedgerId through `ledgersLOV` | Compact ledger/application eligibility matrix containing all matching rows and explicit `NO_STATUS_INSTANTIATED` outcomes, plus pagination and required-header receipts; or direct-query receipts plus proof of no target-calendar status ownership | Ledger branch permits preview when every matching application row is `N`; a successful complete per-ledger query with no affected-period match, including zero rows for that ledger, is recorded as no status instantiated and is eligible. This is evaluated independently for each ledger, so empty and all-`N` ledger outcomes may coexist. Full unrelated history is expected and ignored after complete pagination; never pause for user-assisted row isolation. No captured HTTP status/body is a client/transport failure, not an empty result; retry the explicit GET with the required header. Zero-ledger branch permits preview only when exact target ledger discovery is zero and no direct-query row resolves back to the target calendar. Ambiguity, pagination gaps, inaccessible responses, inconsistent ledger ownership, or any target-calendar non-`N` row blocks. Repeat immediately before submission. |

`accountingPeriodStatusLOV.ClosingStatus` values are `O` Open, `C` Closed,
`F` Future Enterable, `N` Never Opened, `P` Permanently Closed, and `W` Close
Pending. Status rows are ledger- and application-specific. For a permitted
period edit with associated ledgers, retain complete pagination receipts plus
the compact affected-period matrix and require `N` everywhere in that matrix;
never treat one `N` row as overriding another application's or ledger's
status. For a calendar proven to have no associated
ledger, direct period-identity queries are a collision/anomaly check: an empty
result means no status is instantiated, not that a synthetic `N` row exists.
The conditionally editable core fields are `PeriodNum`, `QuarterNum`,
`StartDate`, `EndDate`, and `AdjustmentPeriodFlag`. Existing `PeriodName` and
`EnteredPeriodName`, `PeriodYear`, parent/header fields,
frequency, adjustment policy, and DFF values without a separately validated
context/segment contract remain protected.

## Associated-Ledger Status Reduction

1. Freeze the affected original periods and their `PeriodNameId` values before
   any proposed-value comparison.
2. For every associated `LedgerId`, retrieve all status-history pages and record
   the request, page count, item count, completion indicator, and retrieval time.
3. Filter locally by exact `PeriodNameId`. Retain every matching
   `ApplicationId` row and ignore unrelated historical rows. When an ID is not
   returned, use the complete original name/year/number/start/end/adjustment
   identity as an exact fallback; never use fuzzy name, partial date, or proposed
   values for matching.
4. Require `ClosingStatus=N` in every retained row. A ledger may legitimately
   contribute multiple application rows, all of which must pass. When a
   successful, fully paginated ledger response has no match for an affected
   period--including a response with zero rows--record
   `NO_STATUS_INSTANTIATED` for that cell and treat it as eligible without
   creating a synthetic `N` row. Evaluate this independently per ledger.
5. Persist the compact matrix containing `PeriodNameId`, period name,
   `LedgerId`, `ApplicationId`, `ClosingStatus`, original dates, and retrieval
   time together with the pagination receipts. Continue automatically to
   eligibility evaluation and package preparation; do not ask the user to run a
   separate check or manually isolate rows.
6. Stop only for a failed or incomplete response/page, ambiguous identity, or
   any retained non-`N` row. No captured HTTP status or body is a transport
   failure, not a successful empty result. Repeat this algorithm immediately
   before submission and invalidate approval when its evidence fingerprint
   changes.

For every `accountingPeriodStatusLOV` request, send both the cached OAuth bearer
token and `REST-Framework-Version: 9`. If a convenience client produces no
captured HTTP response or body, retry as an explicit GET with those headers.
Only a successful completed response with confirmed pagination may establish an
empty or matchless `NO_STATUS_INSTANTIATED` outcome.

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Required duplicate-check `accountingCalendarsLOV` is unavailable | Stop the create path because duplicate absence cannot be established; do not assume nonexistence. Unavailability of `ledgersLOV` or `accountingPeriodStatusLOV` is not a general creation/update gate, but it blocks an existing-period edit because lifecycle eligibility cannot be proven. A successful fully paginated zero-ledger result is not unavailability; use the direct-status branch. |
| A complete current parent is needed for a permitted update | First use a verified successful FSCR creation package only when it belongs to the current project/session and still matches the target environment, release, task, identity, and post-load state. Otherwise automatically run one full task Data Only Export. Isolate exactly one parent matching both names returned by `accountingCalendarsLOV` and only its linked children. Block if the exact target is absent, duplicated, or ambiguous. Do not use filtered criteria for this task or copy another calendar. |
| New calendar import is about to be submitted | Repeat the exact `UserPeriodSetName` query immediately before submission; block if a match now exists or the lookup is unavailable. |
| Period naming or row values are unclear | Stop for a user choice or documented-rule resolution. Do not use another calendar's periods as comparable evidence or as a default source. |
| Existing definition matches | Report idempotent result and do not create duplicate setup data. |
| Existing definition differs | Present the differences and require an update-versus-new decision. |
| Permitted existing-calendar FSM update is requested | Resolve exactly one existing calendar and record its immutable `UserPeriodSetName` and `PeriodSetName`. Resolve the complete current-value source through the verified current-session FSCR package or one full exact-task data export, then cross-check its isolated target rows against fully paginated LOV evidence. For a format change, validate history and the immediately preceding boundary before generating the added year. For an existing-period edit, build the immutable affected set and apply the complete all-`N` ledger branch or proven zero-ledger/direct-status branch before preview and again before submission. Verify the exact change and unaffected-row preservation after load. |

## New Calendar Duplicate Gate

1. Before package generation, call `accountingCalendarsLOV` with the exact
   `UserPeriodSetName` query and require exactly zero matches.
2. Immediately before submitting the immutable approved ZIP, repeat the same
   query. Do not reuse a prior lookup result.
3. On one or more matches, stop the create path and require an explicit
   update-versus-new decision. Do not inspect its rows to derive the new
   definition.
4. On an unavailable, unauthorized, malformed, or ambiguous LOV response, stop
   the create path. Do not treat an unavailable LOV as zero matches.

## LOV Evidence Boundaries

`accountingCalendarsLOV` can corroborate calendar identity, user and internal
period-set names, calendar type, and period type.
`accountingPeriodsLOV` can corroborate period names,
year and period numbers, start/end dates, and existing-row differences.

For creation, on the project's first run fetch the same-task template through
`shared.setup-export.task-level-export` in template-only mode, validate it, and
persist its metadata and fingerprint as the project baseline. On later runs,
reuse it only while task, environment, release, fingerprint, members, and
headers remain compatible. Use this evidence only for package members and
header order. Never use a Data Only Export to author a new calendar. A permitted
update separately follows the controlled current-value source rule. Use exact
`accountingCalendarsLOV` identity lookup only to prevent a duplicate. After a
successful load, `accountingPeriodsLOV` may verify the generated target rows;
it must not supply attributes for a new calendar. This environment exposes the
period-set filter as `PeriodSetNameId`, not `PeriodSetName`; use
`q=PeriodSetNameId='<calendar_name>'`. LOV rows can prove dates, numbering,
names, and adjustment placement. Use documented trusted codes/defaults and
user inputs for `GL_PERIOD_SET.csv` values; retain template metadata for
column order.

### Allowed LOV Inferences

Use `accountingCalendarsLOV` and `accountingPeriodsLOV` only to establish
facts present in their returned rows:

- Exact calendar-name duplicates, returned calendar/period-set identity, and
  exposed calendar or period-type attributes.
- Actual generated period names, entered names, start/end dates, period years,
  period numbers, and adjustment flags.
- Standard-versus-adjustment row counts from `AdjustmentPeriodFlag`,
  standard-period sequence and date continuity, and each returned adjustment
  row's placement or same-day/overlapping boundary with an adjacent standard
  period.
- Observed naming behavior, including CY-versus-FY year tokens, when comparing
  otherwise equivalent calendars. Treat this as output evidence tied to the
  supplied start date and naming format.

Use a known comparable calendar as a post-load acceptance baseline only when
its frequency, start-date alignment, naming option, and adjustment requirement
are independently known.

Do not infer undocumented behavior from LOV output. Use documented trusted
codes/defaults and the user-selected design for import header codes,
`SamplePeriodName`, and `AdjPeriodsNum`. An adjustment-row count is comparison
evidence only; it does not replace explicit design validation.

### LOV Validation Workflow

1. Query `accountingCalendarsLOV` for the exact requested calendar name before
   creation, solely to prevent a duplicate.
2. For an add-year operation, query all `accountingPeriodsLOV` pages for the
   exact calendar and validate the exposed history and boundary against the
   controlled exact-target update source.
3. Use the requested definition and documented rules to validate the package.
4. After a successful load, query `accountingPeriodsLOV` using the environment's
   `PeriodSetNameId` filter to verify the result.
5. Record reusable, non-secret observations as runtime evidence. Do not promote
   an inferred LOV pattern to a supported-option rule without documented Oracle
   source confirmation; never use UI for runtime verification.

Persist only reusable, non-secret LOV observations in the project baseline, with
the target environment and release context. LOV observations support comparison
and duplicate prevention; the validated fetched template or compatible project
baseline supplies CSV headers and package structure.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| CAL.LOOKUP_EXISTING | decision | 4 | reference_lookup | absent->CAL.DEFAULT;matching->CAL.DONE_EXISTS;existing_update->CAL.VALIDATE_UPDATE;different->CAL.STOP_DIFFERENCE;unavailable->CAL.STOP_DEFAULTS | CAL.RESOLVE_DEFAULTS | stop | Before create or existing-calendar package generation |

## Endpoint-Only Verification

All calendar workflows and delegates must use only declared endpoints and FSCR framework routes for discovery, duplicate checks, validation and saved-state verification. Never navigate Fusion task UI, inspect its DOM/network state, operate controls, scrape grids or obtain screenshots/user-assisted UI evidence. Historical UI observations describe packaged business rules; they do not require runtime UI access.

Complete pagination and exact environment/identity matching. Failed, partial or unauthorized reads do not prove absence or success. Report unavailable required evidence explicitly; do not invent an endpoint or use UI as a fallback. Core.auth may open login for the user to complete; this authentication handoff does not authorize task UI access.

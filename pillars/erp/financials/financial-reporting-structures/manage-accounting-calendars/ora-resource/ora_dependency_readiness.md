# Accounting Calendar Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---:|---|---|
| 1 | Input design | Validate business calendar definition. |
| 2 | Technical defaults | Derive internal values before creating CSV artifacts. |
| 3 | Existing calendar | Check calendar and period-row existence. |
| 4 | FSM metadata | Confirm package members and columns; apply documented code values and dates. |
| 5 | Import readiness | Resolve all technical gaps and obtain approval. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CAL.DEFAULTS | Documented technical defaults | Yes | Any FSM package | Validate | User inputs and documented calendar rules | Default validation | Avoid failed-import discovery | Provide any missing business input; never request a Data Only Export for code derivation | Calendar codes, defaults, date format |
| CAL.EXISTENCE | Exact calendar-name duplicate check | Yes | Before create | Lookup | Accounting Calendars LOV exact-name query | Read-only lookup | Avoid duplicate setup without using an existing definition as a source | Choose a unique name when a match exists | Exact match count only |
| CAL.METADATA | Package shape | Yes | Before ZIP generation | Fetch automatically on the project's first run; verify or reuse later | Same-environment, same-release template-only package fetched through `shared.setup-export.task-level-export`, or its compatible persisted project baseline | Template metadata inspection | CSV import must match the current target task without using populated setup data | Use `setupTaskCSVTemplateExports` automatically on the first project run or when the baseline is stale; do not ask for separate conversational approval and never use `setupTaskCSVExports` | Metadata XML, CSV structure, task/environment/release identity, and fingerprint |
| CAL.YEAR_START | Calendar header date completeness | Yes | Before ZIP generation and immediately before import | Verify | Approved calendar design plus generated non-adjusting rows | Calendar package review | Oracle requires a nonblank `LatestYearStartDate` and validates it against the generated calendar | Correct the dates; do not discover this requirement through a failed import | CalendarStartDate; LatestYearStartDate; latest non-adjusting YearStartDate |
| CAL.YEAR_EXTENSION | Existing calendar completeness | Yes | Before adding a fiscal year | Verify | Complete paginated `accountingPeriodsLOV` evidence plus local validation of the proposed package | Existing-calendar structural validation | Detects exposed structural problems without depending on exported setup data | Validate returned history and the new package; let Data Loader/FSM enforce product-side rules not exposed by LOV | Existing rows and counts; unique names/numbers; sequential numbering; continuous dates; adjustment placement; prior-year final boundary |
| CAL.UPDATE.SCOPE | Existing calendar update | Yes | Before FSM/Data Loader preview | Validate | Requested fields, lifecycle eligibility evidence when periods are edited, and frequency-format allow-list | Controlled-update validation | Limits edits to safe, evidenced actions | Permit description; a format change while adding a year; or edits to period number, quarter number, start/end dates, and adjustment flag when lifecycle eligibility and every calendar rule pass. Existing-period name changes and other protected-field changes remain blocked | Approved field list, status/zero-ledger evidence, format, changed rows, and added-year rows when applicable |
| CAL.UPDATE.CURRENT_VALUES | Complete existing-calendar carrier | Yes | Every permitted existing-calendar update | Resolve | Verified successful FSCR creation package from the current project/session; otherwise one full `GL_MANAGE_ACCOUNTING_CALENDARS` current-data export | Exact-target update-source validation | Fusion period updates require current parent attributes that LOVs do not expose, and partial parents can skip children or fail null validation | Prefer the current-session source when its environment, release, identity, successful load, package hash, and post-load state still match. Otherwise automatically export the full task, isolate exactly one LOV-matching parent and its children, and block if the target is absent or ambiguous | Source type and receipt; environment/release/task; exact parent; linked children; package hash; extraction timestamp |
| CAL.PERIOD.UPDATE.STATUS | Existing-period core-field edit | Yes | Before preview and repeated immediately before submission | Verify automatically after lookup | Fully paginated `ledgersLOV`, `accountingPeriodsLOV`, and `accountingPeriodStatusLOV` evidence | Period lifecycle eligibility validation | Prevents mutation after any affected period has entered a usable or closed lifecycle state | Ledger branch: call the status LOV with OAuth and `REST-Framework-Version: 9`, treat full ledger histories as normal, retrieve all pages, automatically reduce by immutable affected `PeriodNameId`, and require every matching application row to be `ClosingStatus=N`. A successful complete query with no affected match, including an entirely empty result for an individual ledger, records `NO_STATUS_INSTANTIATED` and passes independently of other ledgers. No captured HTTP response is not an empty result and must be retried explicitly with the required header. Zero-ledger branch: require a complete exact zero-ledger result, direct status queries for every affected original identity, and proof that every returned LedgerId belongs to another calendar. A truncated/inaccessible response, ambiguous identity, or target-calendar non-`N` status blocks | Immutable original/proposed affected-period list, ledger result, compact eligibility matrix including explicit empty outcomes, direct-query receipts, returned-ledger resolution, timestamps, required-header evidence, and per-ledger pagination receipts |
| CAL.TEMPLATE_ONLY | New calendar definition source | Yes | Before defaulting or package generation | Fetch on the project's first run; verify or reuse later | Validated project template baseline, documented rules, and user input | Template-only source review | Prevents an existing calendar or populated export from becoming an undocumented default source | Fetch the template-only carrier when no compatible project baseline exists; use approved template metadata and the requested business definition; never request a Data Only Export | Template receipt/baseline, documented rules, requested calendar definition |
| CAL.BATCH_ISOLATION | Multiple calendar request | Yes | Before package generation | Verify | Normalized request definitions | Per-calendar validation | Prevents one calendar's values or failure from contaminating another | Give each calendar a unique name and complete definition | Per-calendar validation and outcome record |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Evidence proves all dependencies | Lookup yes; create only after approval |
| Technical lookup gap | Required code or column is unknown | Lookup yes; create no |
| Business decision | Calendar purpose or naming convention is unresolved | Lookup no; create no |
| Unsupported existing-calendar operation | Delete or protected structural change is requested | Lookup no; create no |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| CAL.RESOLVE_DEFAULTS | step | 3 | resolve_dependency | ready->CAL.LOOKUP_EXISTING;blocked->CAL.STOP_DEFAULTS | CAL.VALIDATE | stop | Valid definition |

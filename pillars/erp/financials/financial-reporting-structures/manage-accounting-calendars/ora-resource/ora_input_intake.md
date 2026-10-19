# Accounting Calendar Input Intake

## Accepted Input Formats

| Input Format | What Must Be Provided | Applies To |
|---|---|---|
| Business scenario | Calendar purpose, fiscal start date, frequency, fiscal-year convention, adjustment policy, naming preference, and budgetary-control intent | Advisory or generated calendar |
| Structured calendar definition | Calendar name, start date, frequency, adjustment frequency, name format, separator, prefix, and explicit rows when frequency is Other | FSM generation |
| Project template baseline | On the project's first run, fetch and validate the template-only package for `GL_MANAGE_ACCOUNTING_CALENDARS`; on later compatible runs, reuse its persisted metadata XML, task CSV headers, and package structure | Package construction and new-calendar authoring only; use template-only mode. A permitted update resolves current values through its separate controlled source rule. |
| Manual period rows | Period name, dates, type, year, period number, entered name, adjustment flag, and quarter number for accounting calendars only | Other frequency or reviewed exceptions |

## Dependency Inputs

| Field | Mandatory | Purpose | Send in Request Body? | Lookup Rule |
|---|---|---|---|---|
| calendar_name | Yes | Identify the period set and prevent duplicates | Yes in CSV when template metadata requires it | Match against Accounting Calendars LOV; do not request exported calendar data |
| calendar_start_date | Yes | Generate and validate fiscal boundaries | Yes in CSV when export metadata requires it | Validate against requested fiscal design |
| latest_year_start_date | Yes for CSV generation | Supply Oracle's required latest generated fiscal-year boundary | Yes as `LatestYearStartDate` in `GL_PERIOD_SET.csv` | Use the latest non-adjusting `YearStartDate`; for a new single-year calendar this equals `calendar_start_date`. Never leave it blank. |
| period_frequency | Yes | Select generation pattern | Yes in CSV as a trusted code | Map the selected UI option to the documented code. |
| adjustment_frequency | Yes | Determine adjustment rows | Yes in CSV as a trusted code | Map the selected UI option to the documented code and matching rows. |
| number_of_adjusting_periods | Yes when adjustment frequency is Other | Define the number of generated adjustment rows | Yes as `AdjPeriodsNum` when template metadata requires it | Require a positive whole number. Keep this separate from the standard-period count used by budgetary-control-only calendars. |
| period_name_format | Conditional | Name generated non-Other periods | Yes in CSV as a trusted code | Use the frequency default when omitted. An alternate requires an explicit user request and frequency allow-list validation. |
| separator | Conditional | Compose generated period names | Yes in CSV as a trusted code | Map Dash, Slash, or None to its documented code; default to Dash when omitted. |
| manual_period_rows | Yes for Other | Define manual boundaries and names | Yes in GL_PERIOD_DEF.csv | Validate each row before generation |
| period_type | Yes for period rows | Identify the period type and support uniqueness checks | Yes when export metadata requires it | Match the calendar period type in the export or read-only lookup |
| user_period_name_prefix | No | Prefix generated period names | Yes when supplied and export metadata requires it | Preserve only reviewed/exported values |
| budgetary_control_only | Conditional | Select the separate budgetary-control calendar mode | Yes when supplied and template metadata requires it | When Yes, require number_of_periods and use the budgetary-control path. |
| number_of_periods | Yes for budgetary-control-only | Define the number of budget periods | Yes when template metadata requires it | Require a positive whole number; do not silently default it from an accounting-calendar frequency. |
| average_daily_balance_enabled | No; conditional validation signal | Enforce the 35-day maximum only when the calendar is known to be used by an average-daily-balance ledger | No unless the approved template contains the field | Accept an explicit reviewed Yes/No value or a reliable setup-derived value. Do not infer it from `ReferencedByLedger`, do not perform a ledger-reference lookup merely because it is absent, and do not block an otherwise valid flow when it is unknown. |
| existing_calendar_update | Conditional | Identify a permitted update action | Yes in the FSM update package when template metadata requires it | Allow only the documented description, period-name-format-with-new-year, or eligible existing-period actions after identity, current-value-source, validation, and approval checks. |
| existing_calendar_current_values | Yes for a permitted update | Supply the complete current parent carrier and exact target-period baseline | Use only the isolated exact-target rows in the update package | Prefer a successfully loaded and post-load-verified FSCR creation package from the current project/session. Otherwise automatically run one full `GL_MANAGE_ACCOUNTING_CALENDARS` data export and isolate exactly one parent whose user and internal names match the LOV identity. Block when the exact target is absent or ambiguous. |

## Template-Only Definition Boundary

| Source | Allowed Use | Prohibited Use |
|---|---|---|
| Validated fetched template or compatible project baseline | ZIP members, metadata XML, CSV header names, and header order | Copying populated values or defaults into a new calendar |
| Verified current-session FSCR creation package | Preserve the exact successfully created calendar's complete parent and rows for a later permitted update in the same project/session | Reuse after an environment/release mismatch, external change, failed load, missing post-load verification, or for another calendar |
| Full current-data task export | Existing-calendar update preflight only when the verified current-session source is unavailable; isolate the exact LOV-resolved parent and its children | Calendar creation, defaults, approximate-name matching, unrelated exported calendars, or retrying an import failure |
| User request and attached source rows | Calendar purpose, selected options, and explicit manual or CSV rows | Filling omitted business choices from another calendar |
| Documented calendar rules | Trusted codes, generated geometry, and validation | Inventing unsupported product options |
| Exact-name calendar lookup | Duplicate prevention and safe identity confirmation | Deriving the proposed calendar definition or using an existing calendar as a comparator |

## Body Field Rules

| Situation | What Happens |
|---|---|
| User requests period status management | Refuse this task scope and route to the appropriate period-status process. |
| Calendar is budgetary-control-only | Mark it explicitly and do not recommend it for standard GL ledger processing without confirmation. |
| Scenario requests a live create | Produce design and readiness output only until an export-compatible FSM package is reviewed and approved. |
| REST mutation is requested | Do not invent a REST contract. Route both new-calendar creation and permitted existing-calendar updates through FSM CSV and the mandatory Data Loader workflow. |
| User requests to delete, remove, drop, or purge a calendar or period | Stop as unsupported; do not open a UI path, create an FSM package, or invoke an API. |
| User requests an existing-calendar description edit | Permit the FSM/Data Loader update after exact identity resolution, immutable preview, and explicit update approval. Change description only; do not change `UserPeriodSetName`, `PeriodSetName`, parent linkage, or period rows. |
| User requests an existing-calendar display-name edit | Stop. `UserPeriodSetName` is immutable for an existing calendar; do not generate or submit an FSM rename package. |
| User requests an existing-calendar period-name-format edit | Permit only as part of adding a new fiscal year through FSM/Data Loader. Validate the requested value against the frequency allow-list, generate and validate only the added year's rows, and preserve all historical period names, dates, and boundaries. |
| User requests an existing-period edit | Resolve every exact existing row from fully paginated `accountingPeriodsLOV`. Permit only `PeriodNum`, `QuarterNum`, `StartDate`, `EndDate`, and `AdjustmentPeriodFlag`. Block existing-period `PeriodName` or `EnteredPeriodName` changes through FSM CSV: changing `PeriodName` is imported as a new row and changing only `EnteredPeriodName` does not change the displayed period name. Retain each original `PeriodNameId` for eligibility matching. Determine the complete affected set, including every row whose number, quarter, boundary, or adjustment flag must change. If ledgers exist, require fully paginated evidence proving every affected period is `ClosingStatus=N` across every ledger/application row. If an exact complete lookup proves zero associated ledgers, directly query status by each affected period's original identity and prove that no returned row belongs to the target calendar. Validate the complete proposed calendar, then route through FSM/Data Loader with immutable preview and explicit approval. |
| User requests another existing-calendar structural change | Stop when the request changes calendar start date, frequency, adjustment policy, `UserPeriodSetName`, `PeriodSetName`, parent linkage, period year, header counts/dates, or a period attribute outside the UI-editable core allow-list. Treat Additional Information/DFF values as a separate schema-governed update, not an unrestricted period edit. |
| User requests multiple calendars | Normalize each calendar into an independent definition, validate each independently, and return a per-calendar result; do not let one definition supply omitted values to another. |
| Budgetary control only is selected | Require an explicit number of periods; set the budgetary-control mode and Other frequency; do not ask for or generate an adjustment-period policy. Use the approved template's budget-period naming behavior rather than a normal accounting naming format. |
| User requests a non-default period-name format or separator | Record the explicit request and validate it against the frequency allow-list. |
| `CalendarStartDate` or `LatestYearStartDate` is blank | Stop before ZIP creation. Populate both fields from the reviewed fiscal design and rerun deterministic package validation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| CAL.COLLECT | step | 1 | collect_input | valid->CAL.VALIDATE;invalid->CAL.STOP_INVALID | none | stop | Any request |

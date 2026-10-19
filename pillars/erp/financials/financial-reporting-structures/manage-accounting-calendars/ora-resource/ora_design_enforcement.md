# Accounting Calendar Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---:|---|---|
| 1 | Validate design | Check names, dates, frequencies, format compatibility, and row constraints. |
| 2 | Resolve codes | Apply documented trusted codes and confirm columns from template metadata. |
| 3 | Check existence | Avoid duplicate create artifacts. |
| 4 | Review package | Verify readiness record before ZIP generation or import. |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| CAL.NAME.LENGTH | Any calendar or period | Blocker | None | Name exceeds 15 characters | Use a short import-safe name | Yes |
| CAL.FREQUENCY | Generated or manual calendar | Blocker | Documented calendar codes and normalized rows | Unsupported code, Daily frequency, or an `OTHER` design implementing a finer-than-weekly cadence | Select a documented supported frequency; Weekly is the finest allowed grain | Yes |
| CAL.SUPPORTED.TYPE | Any calendar definition | Blocker | Normalized calendar type and frequency | Calendar type, non-adjusting frequency, or adjustment policy is outside its documented allow-list | Stop before defaults, row generation, preview, or import; select a supported option | Yes |
| CAL.PERIOD.CONTINUITY | Non-adjusting rows | Blocker | Generated rows | Gaps, overlaps, reversed dates, nonsequential numbers, or more than 53 periods | Correct boundaries and numbering | Yes |
| CAL.PERIOD.FIRST.NUMBER | Every fiscal year | Blocker | Generated or manual rows | The earliest row by date and stable display/order sequence is not `PeriodNum=1` | Renumber the complete year sequentially, including an opening adjustment when present | Yes |
| CAL.PERIOD.NUMBER.MAX | Every fiscal year | Blocker | Header counts and generated or manual rows | A period number exceeds `NonAdjPeriodsNum + AdjPeriodsNum` | Reconcile counts and renumber the complete year | Yes |
| CAL.QUARTER.ASSIGNMENT | Accounting-calendar period rows | Blocker | Generated or manual rows and documented frequency mapping | A QuarterNum is blank, outside 1–4, calculated from inserted adjustment-row numbering, or differs from its overlapping standard period’s fiscal quarter | Regenerate fiscal-quarter assignments from standard-period ordinals; keep adjustment rows in the overlapped period’s quarter | Yes |
| CAL.QUARTER.FIRST | Accounting-calendar standard rows | Blocker | Date-sorted rows | The earliest standard period in a fiscal year is not Quarter 1 | Correct the fiscal-quarter assignment | Yes |
| CAL.QUARTER.SEQUENCE | Accounting-calendar period rows | Blocker | Date-sorted rows | Quarter values decrease, skip a quarter, re-enter an earlier quarter, or an adjustment differs from its overlapping standard period | Correct rows to progress only Q1 through Q4, allowing repeats within a quarter | Yes |
| CAL.COMMITMENT.NO_QUARTERS | Commitment-calendar period rows | Blocker | Generated or manual rows | Any row supplies `QuarterNum` | Leave the quarter field blank/not supplied on every commitment-calendar row | Yes |
| CAL.NAMING.COMPAT | Generated standard frequency | Blocker | Frequency-to-format allow-list | A non-Monthly generated frequency uses anything other than one of the four permitted `PRDNUM` formats, or a Monthly start day after 28 uses a month-based format | For Monthly, select any trusted format consistent with the start-day rule; otherwise select `PRDNUMYYCY`, `PRDNUMYYFY`, `PRDNUMYYYYCY`, or `PRDNUMYYYYFY` | Yes |
| CAL.PERIOD.COUNTS | Generated calendar | Blocker | Generated rows | More than 53 non-adjusting periods or more than 55 adjustment periods are generated for a fiscal year | Correct the design or obtain an approved exception outside this task guidance | Yes |
| CAL.FREQUENCY.EXACT_COUNT | Generated or supplied standard rows | Blocker | Requested frequency and normalized rows | Standard-row count does not exactly match Monthly 12, Weekly 52, Quarterly 4, Yearly 1, 4/4/5 12, 4/5/4 12, 5/4/4 12, or 4 Week 13; Other lacks explicit rows and count | Correct the definition before adding adjustments | Yes |
| CAL.OTHER.STANDARD.COUNT | Ordinary accounting calendar with Other frequency | Blocker | Requested count and reviewed manual rows | `NonAdjPeriodsNum` is not a positive whole number or differs from the number of manual non-adjustment rows | Correct the count or supply the complete matching manual rows | Yes |
| CAL.BUDGETARY.CONSISTENCY | Budgetary or federal calendar request | Blocker | Requested calendar type, count, and adjustment policy | The request contains contradictory period-count or adjustment requirements, or the template/documented rule does not establish the requested budgetary-control option | Correct the conflicting request or obtain documented template evidence | Yes |
| CAL.BUDGETARY.MODE | Budgetary control only request | Blocker | Request and template metadata | Calendar type is not COMMITMENT, frequency is not Other, number of budget periods is missing or nonpositive, or an accounting-calendar frequency is supplied | Use the dedicated budgetary-control-only definition | Yes |
| CAL.BUDGETARY.PERIOD_COUNT | Budgetary control only request | Blocker | Requested number of periods | Period count is zero, negative, fractional, nonnumeric, or missing | Require a positive whole-number count; do not impose an unproven fixed count | Yes |
| CAL.BUDGETARY.NO_ADJUSTMENTS | Budgetary control only request | Blocker | Request and normalized rows | An adjustment policy, count, or adjustment row is supplied | Remove adjustment input and rows; preserve only a template-required technical value | Yes |
| CAL.BUDGETARY.NAMING | Budgetary control only request | Blocker | Template-supported budget naming and budget-year number | An accounting-calendar name format is used, the budget-year number is blank, or generated names do not follow the template-supported budget shape | Generate budget-period names from the approved template and explicit count | Yes |
| CAL.RETAIL.5_4_4.ADJUSTMENTS | 5/4/4 with adjustments | Blocker | Selected policy and generated rows | Opening, midyear, quarterly, or closing adjustment placement does not match the reviewed 5/4/4 geometry, is not one day, overlaps zero or multiple standard periods, or breaks sequential numbering | Regenerate from the reviewed 5/4/4 adjustment shape | Yes |
| CAL.RETAIL.5_4_4.NONE | 5/4/4 with no adjustment | Blocker | Selected policy and generated rows | Any adjustment row is generated, or the standard row count is not exactly 12 | Preserve the explicit no-adjustment choice and generate only the twelve reviewed standard rows | Yes |
| CAL.WEEKLY.YEAR_END.COUNTS | Weekly calendar with `1_YEAR_END` adjustment | Blocker | Generated rows | Non-adjusting count is not exactly 52, adjustment count is not exactly 1, or a 53rd standard week is paired with an adjustment period | Generate 52 weekly periods and one reviewed year-end adjustment period | Yes |
| CAL.WEEKLY.QUARTERLY.GEOMETRY | Weekly calendar with `QUARTERLY` adjustments | Blocker | Generated rows | The definition does not contain 52 continuous seven-day standard weeks and four single-date adjustments after successive groups of 13 standard weeks, or numbering and quarter inheritance differ from the reviewed geometry | Regenerate from the canonical weekly quarterly geometry | Yes |
| CAL.ADJUSTMENT.OTHER.COUNT | Generated calendar with `OTHER` adjustment frequency | Blocker | Requested count, generated rows, and header counts | The adjustment count is missing or is not a positive whole number, the number of appended adjustment rows differs from the count, or an appended row does not use the final standard period's end date, year, and quarter | Correct the count and regenerate from the canonical generic adjustment geometry | Yes |
| CAL.ADJUSTMENT.FREQUENCY.COMPAT | Yearly or 4 Week calendar | Blocker | Provided UI validation evidence | `1_MID_1_END`, `1_MID_2_END`, or `QUARTERLY` is selected | Select another supported adjustment frequency | Yes |
| CAL.OTHER.MANUAL | Other frequency | Blocker | Reviewed manual rows | Period boundaries or names were inferred | Supply explicit rows | Yes |
| CAL.DEFAULT.EVIDENCE | Before package generation | Blocker | Documented calendar rules and template metadata | Any required user input, documented code, or template column is unresolved | Resolve the business input or obtain the task template metadata | Yes |
| CAL.EXISTENCE | Before create | Blocker | Exact accounting-calendars-lov name query | The requested name already exists or exact-name lookup is unavailable | Stop duplicate creation; do not use the matching definition as input | Yes |
| CAL.CSV.ENCODING | Before import | Blocker | Same-task template metadata | CSV has a UTF-8 BOM, differs from template column order, or uses an unreviewed date format | Rebuild UTF-8-without-BOM CSV in template order using yyyy/MM/dd dates | Yes |
| CAL.COUNT.RECONCILIATION | Before ZIP creation | Blocker | Generated rows | AdjPeriodsNum, NonAdjPeriodsNum, and TotalPeriodsNum do not reconcile with child rows | Correct header counts or rows | Yes |
| CAL.YEAR.START.REQUIRED | Before ZIP creation and import | Blocker | Generated calendar and period rows | `CalendarStartDate` or `LatestYearStartDate` is blank, unparseable, earlier than the calendar start, or differs from the latest non-adjusting `YearStartDate` | Populate the reviewed dates and repeat calendar-package validation | Yes |
| CAL.YEAR.EXTENSION.COMPLETE | Before adding a fiscal year | Blocker | Complete paginated `accountingPeriodsLOV` evidence, controlled exact-target current-value source, and locally validated proposed rows | Either source is incomplete or inconsistent; history has missing/duplicate/nonsequential rows, discontinuous standard dates, invalid adjustment placement, or a prior-year final standard end date other than the day before the proposed first standard start date | Resolve the discrepancy or stop the extension; do not infer missing values or use another calendar | No |
| CAL.ADJUSTMENT.OVERLAP | Adjustment periods | Blocker | Generated rows | Adjustment row overlaps zero or multiple non-adjusting periods | Place it on the intended adjacent period boundary | Yes |
| CAL.PERIOD.SET.LINKAGE | FSM calendar package | Blocker | Header and child CSV rows | `PeriodSetName` is blank on the parent or a child, or a child value differs from the parent | Populate the same reviewed `PeriodSetName` on the header and every child period row | Yes |
| CAL.BEGIN.END.MONTHLY.PATTERN | Monthly `1_BEGIN_1_END` | Blocker | Generated period rows and header | Opening is not period 1 on fiscal start, normal months are not periods 2?13, closing is not period 14 on fiscal year end, or `FirstPeriod` does not match the first normal period generated from the selected format | Regenerate the approved sequence; do not substitute an unreviewed adjustment prefix, period 0, or a next-year first period | Yes |
| CAL.UPDATE.DESCRIPTION | Existing calendar description update | Blocker | Exact identity | The request changes `UserPeriodSetName`, `PeriodSetName`, parent linkage, or any period row rather than only description | Submit only through the mandatory FSM/Data Loader workflow with immutable preview and explicit approval; preserve immutable identity and periods | Yes |
| CAL.UPDATE.FORMAT.NEW_YEAR | Existing calendar period-name-format update | Blocker | Exact identity, allowed-format list, and added-year rows | The requested format is not allowed for the frequency, no new fiscal year is being added, or a historical row/name/date/boundary would change | Validate the requested value, generate only the new fiscal year in the requested allowed format, then submit through FSM/Data Loader after immutable preview and approval; preserve history | Yes |
| CAL.UPDATE.PERIOD.NEVER_OPENED | Existing-period UI-editable core-field update | Blocker | Exact original calendar/period identity, complete affected-period set, complete per-ledger eligibility evidence or proven zero-ledger/direct-status evidence, complete existing-period baseline, and proposed rows | A per-ledger request/page is inaccessible or incomplete; matching application rows include a non-`N` status; identity is ambiguous; the zero-ledger branch is not a complete exact result or has a direct-query row attributable to the target; either period-name field, period year, parent, header, frequency, adjustment policy, count, or a non-UI-core field changes; or the resulting full calendar violates date, numbering, quarter, continuity, count, or adjustment rules. A successful complete empty or affected-period-matchless result is eligible as `NO_STATUS_INSTANTIATED` | Correct the proposed period rows or stop. Preview only the exact permitted delta; repeat the same complete eligibility branch immediately before submission and invalidate execution if any result changes | Yes |
| CAL.TEMPLATE_ONLY_SOURCE | New calendar package | Blocker | Validated template-only package or compatible persisted project baseline, plus normalized request | A Data Only Export, populated setup row, or existing calendar is used to derive a proposed value, row, format, or default; or the first project run proceeds without fetching and persisting the template-only carrier | Fetch or refresh the template-only carrier through the approved route, then rebuild from its metadata, documented rules, and the requested definition only | Yes |
| CAL.TEMPLATE.FIELD_MAP | Any FSM package | Blocker | Approved template headers and field classification | A CSV column is unclassified, or a request-derived value appears in a blank-only context, DFF, global-attribute, audit, status, or system field | Clear the invalid value and rebuild from the classified template map | Yes |
| CAL.REFERENCED_BY_LEDGER.NON_GATING | Any FSM package or existing-calendar update | Blocker | Approved template and request | `ReferencedByLedger` is used as a general lookup, approval, preview, or submission prerequisite | Keep the field blank unless the template requires a reviewed literal. The separate `ledgersLOV` lookup is mandatory only for a requested existing-period edit so every ledger's status can be checked; it does not reinstate `ReferencedByLedger` as a gate | Yes |
| CAL.ADB.MAX.DURATION | Reliable ADB signal is Yes | Blocker | Explicit reviewed input or reliable setup-derived ADB flag | Any period's inclusive duration exceeds 35 days | Shorten the period design or use a calendar compatible with the ADB ledger; do not infer ADB use from `ReferencedByLedger` | Yes |
| CAL.LEGACY.RULES.DEPENDENCY | Legacy rules are requested | Blocker | Requested/header flags | `LegacyRulesEnabledFlag=Y` while `LegacyCalendarFlag` is blank or `N` | Set legacy rules to `N`, or use `Y` only for a reviewed legacy calendar | Yes |
| CAL.TEMPLATE.NO_CONTEXT_YEAR | Any FSM package with a requested calendar year | Blocker | GL_PERIOD_SET and GL_PERIOD_DEF rows | The requested year appears outside CalendarStartDate, LatestYearStartDate, StartDate, EndDate, YearStartDate, QuarterStartDate, PeriodYear, or FiscalYear | Remove the misplaced value; never use a calendar year as a context/category value | Yes |
| CAL.BATCH.ISOLATION | Multiple calendar request | Blocker | Per-calendar normalized definitions | Any definition borrows values from another, has an unresolved error, or lacks an entity-specific result | Validate and preview each calendar independently | Yes |
| CAL.DELETE.UNSUPPORTED | Delete, remove, drop, or purge request | Blocker | Request intent | Any calendar or period deletion is requested | Stop as unsupported; do not create a package or execute an action | No |
| CAL.UPDATE.PROTECTED_FIELDS | Existing calendar request | Blocker | Request intent | Calendar start date, period frequency, adjustment policy, `UserPeriodSetName`, `PeriodSetName`, parent linkage, period year, either existing-period name field, header fields, or a period field outside number, quarter, start/end dates, and adjustment flag is changed | Stop; do not create, import, or execute the protected update. For permitted period fields, require either the associated-ledger/all-`N` branch or the exact zero-ledger/direct-status branch and enforce every calendar rule | No |

### Existing-period status-history enforcement

A full `accountingPeriodStatusLOV` ledger history is an expected response, not a
blocker. Send the OAuth bearer token with `REST-Framework-Version: 9`, complete
pagination, and automatically reduce the response by the immutable affected
`PeriodNameId` set, retaining every matching `ApplicationId` row and ignoring
unrelated history. Require `ClosingStatus=N` in every retained row. A successful
complete query with no affected match, including an entirely empty result for
one associated ledger, records `NO_STATUS_INSTANTIATED` and passes independently
of other ledgers. Persist the compact eligibility matrix and pagination/header
receipts and continue without asking the user to isolate rows or request another
check. A convenience-client call with no captured HTTP status/body is not an
empty result; retry the explicit request with the required header. Stop only for
an incomplete/inaccessible response, ambiguous identity, or a retained non-`N`
row. Repeat the same reduction before submission and invalidate approval if its
evidence fingerprint changes.

## Design Lookup Requirements

| Rule ID | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|
| CAL.DEFAULT.EVIDENCE | Documented calendar rules and same-task template metadata inspection | Every package | Codes, headers, formats, members | ora_defaulting_rules.md |
| CAL.EXISTENCE | accounting-calendars-lov and accounting-periods-lov | Before create | Existing calendar and rows | ora_reference_lookups.md |
| CAL.YEAR.EXTENSION.COMPLETE | accounting-periods-lov plus local package validation | Before adding a fiscal year | Complete exposed history from the LOV and proposed package counts, quarters, adjustments, and boundary | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| CAL.DESIGN_GATE | decision | 6 | design_enforcement | pass->CAL.GENERATE_CSV;blocked->CAL.STOP_INVALID | CAL.LOOKUP_EXISTING,CAL.DEFAULT | stop | Calendar does not already exist |

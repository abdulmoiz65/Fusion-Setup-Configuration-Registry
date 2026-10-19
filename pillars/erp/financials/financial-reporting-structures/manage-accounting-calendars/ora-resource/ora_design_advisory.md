# Accounting Calendar Design Advisory

## Guidance Sources

| Source Mode | Allowed Sources | When Used |
|---|---|---|
| Functional design | Oracle Accounting Calendar Options and validation documentation | Calendar design and constraint explanation |
| Data model | Oracle GL_CALENDARS, GL_PERIODS, GL_PERIOD_SETS, GL_DATE_PERIOD_MAP, and GL_PERIOD_TYPES EDM pages | Field meanings, relationships, and validation support |
| Technical import | Template-only package fetched on the project's first run or its compatible persisted project baseline | Package structure and new-calendar CSV decisions. A permitted existing update may separately use its controlled current-value source. |

## Guidance Topics

| Topic | Advisory Level | What To Explain | Do Not Include |
|---|---|---|---|
| Frequency design | Required | Monthly, weekly, quarterly, yearly, retail, 4 Week, and Other selection; 52/53-week and 13-week-quarter assumptions | Daily non-adjustment calendar generation |
| Period names | Required | UI option inventory, separator options, and frequency compatibility | Invented CSV codes |
| Adjustment periods | Required | Separate adjustment validation and allowed date sharing | Non-adjusting overlap exception |
| Budgetary-control-only mode | Required | It is a separate `COMMITMENT` / Other-frequency path with an explicit budget-period count, no adjustment selection, and template-supported budget-period names | Treating it as a Yearly, Federal, or ordinary Other accounting calendar |
| Period status boundary | Required | Calendar creation does not change period statuses | Any open/close/future-enter action |
| Calendar strategy | Strong recommendation | Reuse a corporate calendar where fiscal, close, and statutory needs permit; justify a separate calendar with a durable requirement and mapping impact | Creating calendars only for reporting labels |
| History and translation | Strong recommendation | Confirm historical-conversion horizon, first translation period, and first operational period before setting the start date | Treating go-live as the required calendar start date |
| Lifecycle governance | Strong recommendation | Assign owners for annual year extension, validation, and downstream reporting/cube impact review | Treating future-year generation as an emergency activity |
| Ledger alignment | Conditional recommendation | Document secondary-ledger, EPM, consolidation, tax, and reporting period mappings when calendars differ | Inferring that a valid source period automatically has a target mapping |
| Average daily balance | Conditional requirement | When a reliable explicit or setup-derived signal says the calendar is used by an average-daily-balance ledger, explain that every period is limited to 35 inclusive days | Treating `ReferencedByLedger` or a missing ADB signal as a general creation/update gate |

## Output Rules

| Situation | What Happens |
|---|---|
| Advisory scenario has no technical defaults | Give a design recommendation and list evidence still needed before FSM generation. |
| Weekly request supplies a start date but no explicit conflicting end date | Apply the canonical 52 continuous seven-day weeks automatically. The final standard period ends on start date plus 363 days; disclose that boundary in the preview without asking for confirmation. |
| Weekly request explicitly requires a different end date or a 53rd standard week | Stop and explain the conflict with the supported 52-week generated design; request direction only because the supplied requirements are incompatible. |

## UI Option Inventory

| Selection | Available Options | Authoring Rule |
|---|---|---|
| Period frequency | Monthly, Weekly, Quarterly, Yearly, 4/4/5, 4/5/4, 5/4/4, 4 Week, Other | Use the documented trusted codes; Other requires explicit manual period rows. |
| Adjustment frequency | Beginning/end year, midyear/end year, midyear/twice year-end, year end, twice year-end, None, Other, Quarterly | Treat every non-default selection as explicit. Other requires a positive whole-number adjustment count and appends that many rows at the final standard-period boundary. For Yearly and 4 Week, reject midyear/end, midyear/twice-end, and Quarterly; the provided UI evidence identifies these as the only disallowed combinations. |
| Separator | Dash (`SEP_DASH`), None (`SEP_NONE`), Slash (`SEP_SLASH`) | Default to Dash when omitted; use the documented code for an explicit selection. |
| Period format | MMMYY calendar year; MMMYY fiscal year; MMMYYYY calendar year; MMMYYYY fiscal year; MMYY calendar year; MMYY fiscal year; MMYYYY calendar year; MMYYYY fiscal year; Period numberYY calendar year; Period numberYY fiscal year; Period numberYYYY calendar year; Period numberYYYY fiscal year; YYMM calendar year; YYMM fiscal year; YYMMM calendar year; YYMMM fiscal year; YYYYMM calendar year; YYYYMM fiscal year; YYYYMMM calendar year; YYYYMMM fiscal year | Monthly permits every listed trusted format (subject to the day-1-through-28 rule for month-based formats). All other generated frequencies permit only Period numberYY/Period numberYYYY with calendar-year or fiscal-year suffixes. Other is manual; budgetary control uses template-supported budget names. |

## Calendar Data Model Guidance

| Object | Role | Authoring Boundary |
|---|---|---|
| GL_PERIOD_SETS | Stable named period-set identity and parent key. | Keep the period-set name consistent in the calendar header and every period row. Do not ask the user for the generated PeriodSetId. |
| GL_CALENDARS | Calendar behavior: type, frequencies, counts, naming, dates, and flags. | Derive values from user inputs and documented rules; keep CalendarStartDate, LatestYearStartDate, row counts, format, separator, and sample name consistent. Do not author Fusion-managed IDs, optimistic-locking values, enterprise/partition values, audit fields, or DFF values unless explicitly provided. |
| GL_PERIOD_TYPES | Periods-per-year and calendar-year or fiscal-year naming semantics. | Use as comparison evidence; do not invent a user-supplied PeriodTypeId. |
| GL_PERIODS | Child period rows with names, dates, year, number, conditional quarter, and adjustment flag. | Require unique names, unique number/year/type combinations, accounting-calendar quarter values or blank commitment-calendar quarters, and compatible parent keys. |
| GL_DATE_PERIOD_MAP | Fusion-managed accounting-date coverage for non-adjusting periods. | Use only as evidence for continuous, non-overlapping non-adjusting dates. Do not author it in the FSM package. |
| GL_PERIOD_STATUSES | Ledger or application period lifecycle. | Exclude from calendar creation; route open, close, future-enter, and permanently-close requests elsewhere. |

## Import-Relevant Attribute Guidance

| Attribute Group | Required Behavior |
|---|---|
| Identity | Keep USER_PERIOD_SET_NAME and PERIOD_SET_NAME import-safe, 15 characters or fewer where mapped to period-set fields, and identical across header and detail rows. |
| Calendar type | Use ACCOUNTING for ordinary GL calendars. Treat COMMITMENT or budgetary-control-only designs as an explicit scoped decision, not a default. |
| Frequency and adjustment | Use documented trusted NON_ADJ_PERIOD_FREQ_CODE and ADJ_PERIOD_FREQ_CODE values. Reconcile AdjPeriodsNum, NonAdjPeriodsNum, TotalPeriodsNum, and child rows. |
| Period-name fields | Keep PERIOD_NAME_FORMAT_CODE, PERIOD_NAME_SEPARATOR_CODE, USER_PERIOD_NAME_PREFIX, SAMPLE_PERIOD_NAME, PeriodName, and EnteredPeriodName mutually consistent. |
| Date fields | CalendarStartDate and LatestYearStartDate are required for generated imports. Each child row must have valid start/end dates and YearStartDate; accounting rows require quarter alignment while commitment rows keep quarter blank. |
| Flags and system fields | For a new calendar use `N` for SecurityFlag, LegacyCalendarFlag, and LegacyRulesEnabledFlag. Permit `LegacyRulesEnabledFlag=Y` only with `LegacyCalendarFlag=Y` in an explicit reviewed legacy-migration scenario. Do not request CalendarId, PeriodSetId, PeriodTypeId, ObjectVersionNumber, EnterpriseId, DefaultPartitionGroupCode, or audit values. Leave audit, descriptive-flexfield, and global-flexfield fields blank unless the scenario explicitly supplies a reviewed value. |

## Source Mapping

| Decision Area | Source of Truth |
|---|---|
| Frequency, adjustment, UI options, generated/manual behavior | Documented calendar rules and user-selected design |
| Name/number uniqueness, date continuity, sequence and quarter checks | Oracle calendar validation guidance and GL_PERIODS metadata |
| Non-adjusting date coverage | GL_DATE_PERIOD_MAP metadata |
| Package columns, encoding, and ZIP members | Validated fetched template-only package or compatible project baseline |
| Package codes and dates | Documented calendar rules and user-selected design |
| Existing-calendar identity checks | Accounting Calendars LOV |
| Extended period-name and adjustment option inventory | Documented calendar rules |

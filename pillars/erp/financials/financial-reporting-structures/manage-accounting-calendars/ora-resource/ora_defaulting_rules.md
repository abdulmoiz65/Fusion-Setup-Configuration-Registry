# Accounting Calendar Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? |
|---|---|---|---|
| CSV package members | ASM_SETUP_CSV_METADATA.xml, GL_PERIOD_SET.csv, and GL_PERIOD_DEF.csv from the validated template-only package persisted for the project | FSM package generation | Yes, only to match approved template metadata; fetch it on the first project run through `shared.setup-export.task-level-export`, never through a Data Only Export |
| Monthly period count | 12 non-adjusting periods | Normal monthly fiscal year | Yes, for a reviewed different pattern |
| Period naming | `MMMYYFY` for Monthly; `PRDNUMYYFY` for Weekly, Quarterly, Yearly, 4 Week, 4/4/5, 4/5/4, and 5/4/4 | Generated standard frequencies | Only when the user explicitly requests a different allowed format; otherwise use the stated default |
| Adjustment frequency | NONE | No adjustment policy provided | Yes |
| Adjustment code | `1_YEAR_END` | One year-end adjustment is requested | Yes |
| Separator code | `SEP_DASH` for Dash; `SEP_SLASH` for Slash; `SEP_NONE` for None | The user selects a separator; Dash is used when omitted | Yes |
| Period-format codes | `MMMYYFY` for Monthly; `PRDNUMYYFY` for Weekly, Quarterly, Yearly, 4 Week, 4/4/5, 4/5/4, and 5/4/4 | Generated calendars | No default changes; apply an alternate only when explicitly requested and allowed for the selected frequency |
| Non-adjustment frequency codes | `MONTH`, `WEEK`, `QUARTER`, `YEAR`, `4_4_5`, `4_5_4`, `5_4_4`, `4_WEEK`, `OTHER` | Map the selected documented UI frequency to its trusted code | Yes |
| New-calendar flags | `N` for `SecurityFlag`, `LegacyCalendarFlag`, and `LegacyRulesEnabledFlag` | Any new Fusion calendar | Yes, only for an explicit security or legacy-migration scenario |
| Latest year start date | Latest non-adjusting `YearStartDate`; for a new single-year generated calendar, the approved `CalendarStartDate` | `LatestYearStartDate` is required by the `GL_PERIOD_SET.csv` contract | Yes, when the user explicitly supplies a different reviewed latest generated year |
| Audit/system fields | Blank | New scenario-derived package | Yes, only if the repository task template requires a value |
| 4/4/5 pattern | Twelve non-adjusting periods in 4, 4, 5-week sequence per quarter | Standard 52-week retail design | Yes, for approved 53-week or other retail variant |
| New-calendar source | Validated project template baseline plus documented rules and requested inputs | Any new calendar | No Data Only Export or existing-calendar attribute may supply a default |
| Budgetary-control-only calendar type | `COMMITMENT` | Budgetary control only selected | No; do not default ordinary accounting calendars to this type |
| Budgetary-control-only frequency | `OTHER` | Budgetary control only selected | No; do not substitute Monthly, Weekly, Quarterly, Yearly, retail, or 4 Week |
| Budgetary-control-only period count | None | Budgetary control only selected | Yes; require an explicit positive whole-number count |
| Budgetary-control-only adjustment policy | Not user-selectable | Budgetary control only selected | No adjustment option or rows; use a technical value only if the template requires it |

## Defaulting Constraint

Apply the stated frequency default when the request is silent: `MMMYYFY` for Monthly and `PRDNUMYYFY` for Weekly, Quarterly, Yearly, 4 Week, 4/4/5, 4/5/4, and 5/4/4. For `OTHER`, ask the user for the period naming convention and do not generate names until it is supplied. Do not retain, copy, or infer a different `PeriodNameFormatCode` merely because it appears in a prior export. Treat any departure from the default as an explicit user override and align `PeriodNameFormatCode`, `SamplePeriodName`, `PeriodName`, and `EnteredPeriodName` before package generation.

`LatestYearStartDate` is not an audit/system field and must never inherit the blank audit-field default. Populate it before CSV or ZIP validation.

## Explicit-Selection Options (Not Defaults)

These values are available only when the user explicitly requests them. The listed `PeriodNameFormatCode` values are trusted FSM codes and do not require exported setup evidence. Never change a frequency default merely because an alternate appears in another calendar or prior artifact.

| Option Group | Reviewed Values | Selection Gate |
|---|---|---|
| Period-name formats | MMMYYCY, MMMYYFY, MMMYYYYCY, MMMYYYYFY, MMYYCY, MMYYFY, MMYYYYCY, MMYYYYFY, PRDNUMYYCY, PRDNUMYYFY, PRDNUMYYYYCY, PRDNUMYYYYFY, YYMMCY, YYMMFY, YYMMMCY, YYMMMFY, YYYYMMCY, YYYYMMFY, YYYYMMMCY, YYYYMMMFY | Match the selected UI option, frequency allow-list, and sample name. The listed values are trusted FSM codes and do not require export evidence. |
| Adjustment frequencies | NONE, 1_YEAR_END, 2_YEAR_END, 1_BEGIN_1_END, 1_MID_1_END, 1_MID_2_END, QUARTERLY, OTHER | Require an explicit adjustment policy and matching child adjustment rows. |
| Separators | Dash (`SEP_DASH`), Slash (`SEP_SLASH`), None (`SEP_NONE`) | Use the user's explicit selection; default to Dash when omitted. |

## Period-Name Selection Constraint

### Frequency-to-Period-Name-Format Allow-List

| Frequency | Allowed period-name formats |
|---|---|
| Monthly (`MONTH`) | All 20 trusted formats in the explicit-selection list. Default: `MMMYYFY`. |
| Weekly (`WEEK`), Quarterly (`QUARTER`), Yearly (`YEAR`), 4 Week (`4_WEEK`), 4/4/5 (`4_4_5`), 4/5/4 (`4_5_4`), 5/4/4 (`5_4_4`) | `PRDNUMYYCY`, `PRDNUMYYFY`, `PRDNUMYYYYCY`, `PRDNUMYYYYFY` only. Default: `PRDNUMYYFY`. |
| Other (`OTHER`) ordinary accounting | No generated format. Require reviewed manual period names and rows. |
| Other (`OTHER`) budgetary-control-only | No accounting-calendar format. Use the template-supported budget-period naming pattern. |

For Monthly, every trusted format is permitted, including month-, numeric-month,
period-number, and year-first formats. The fiscal start-day restriction still
applies: a month-based Monthly format requires a start day from 1 through 28.
For every non-Monthly generated frequency in the table, reject every
non-`PRDNUM` format.

Keep the stated defaulting behavior when the user is silent: Monthly uses `MMMYYFY`; Weekly, Quarterly, Yearly, 4 Week, 4/4/5, 4/5/4, and 5/4/4 use `PRDNUMYYFY`. For `OTHER`, require the user to select a naming convention and provide manual period names. Treat every other allowed format as an explicit override, not a replacement default.

### Calendar-Year and Fiscal-Year Naming

The `CY` or `FY` suffix affects the year token rendered in period names,
including adjustment-period names; it does not alter period boundaries,
period numbering, quarters, or adjustment placement. For `CY`, derive the
name's year token from the period's calendar date. For `FY`, derive it from the
calendar's fiscal-year designation. The values can differ whenever a fiscal
year crosses a calendar-year boundary. Apply the selected convention
consistently to `SamplePeriodName`, standard names, and every adjustment name.

### Generated Adjustment-Period Names

For generated frequencies, an adjustment-period name uses the Oracle UI default
shape below. This is distinct from the standard-period name.

```text
<two-digit sequential period number>_<base name rendered for that adjustment row>
```

The prefix is the adjustment row's own sequential `PeriodNum`, zero-padded to
two digits. The base name uses the selected `PeriodNameFormatCode`, the
adjustment row's period number, and its effective date/fiscal-year token. It
therefore reflects the selected format: month-based formats render the relevant
month, while period-number formats render the adjustment row number.

| Format family | Standard examples | Adjustment examples |
|---|---|---|
| `MMMYYFY` | `Jan-27`, `Feb-27`, `Mar-27` | `04_Mar-27`, `07_Jun-27`, `12_Sep-27` |
| `PRDNUMYYFY` | `1-27`, `2-27`, `3-27` | `07_7-27`, `14_14-27`, `15_15-27` |

Do not generate adjustment names by simply reusing the adjacent standard name.
The adjustment row's number must be both zero-padded in the prefix and used by
period-number formats in the base name. `SamplePeriodName` remains the first
non-adjusting period name; it is never an adjustment-period name.

## Calendar Flag Rules

`SecurityFlag`, `LegacyCalendarFlag`, and `LegacyRulesEnabledFlag` are one-character `Y`/`N` fields. They are sourced from the `GL_CALENDARS` calendar definition; `SecurityFlag` is also represented on the associated period-set definition.

| Field | `Y` Meaning | New-calendar rule |
|---|---|---|
| `SecurityFlag` | The calendar setup definition is secured. | Use `N` unless the user explicitly requests secured calendar-definition access. |
| `LegacyCalendarFlag` | The calendar is a legacy Oracle E-Business Suite calendar. | Use `N`; do not set `Y` for a new Fusion calendar. |
| `LegacyRulesEnabledFlag` | Legacy migration rules apply when this calendar is updated. | Use `N`; permit `Y` only when an explicit reviewed legacy-migration scenario also sets `LegacyCalendarFlag=Y`. Reject `Y` when `LegacyCalendarFlag` is blank or `N`. |

Calendar-type terminology can differ by surface: the data model describes Accounting and Budgetary Control, while the target LOV/FSM contract can expose `ACCOUNTING` and `COMMITMENT`. Use the exact target-supported technical code for the user-selected calendar type; default an ordinary GL calendar to `ACCOUNTING`.

## Quarter-Number Generation

For an `ACCOUNTING` calendar, `GL_PERIOD_DEF.csv.QuarterNum` is a required
fiscal-quarter assignment, not a running period count. Every generated or
manual row must contain exactly one of `1`, `2`, `3`, or `4`; never generate
`0`, `5`, a blank value, or a calendar quarter inferred from the Gregorian
month when the fiscal year starts in a different month. For a `COMMITMENT`
calendar, leave `QuarterNum` blank/not supplied on every row; do not reuse the
accounting-calendar quarter rules.

For an `ACCOUNTING` calendar, assign quarters from the **standard-period
ordinal within the fiscal year**, not from the sequential CSV `PeriodNum`.
Opening, midyear, quarterly, and closing adjustments insert rows and therefore
can shift `PeriodNum`, but they must not shift a normal period into the next
fiscal quarter.

| Non-adjusting frequency | Standard-period fiscal-quarter assignment |
|---|---|
| Monthly | Standard months 1–3 = Q1, 4–6 = Q2, 7–9 = Q3, 10–12 = Q4. |
| Weekly | Standard weeks 1–13 = Q1, 14–26 = Q2, 27–39 = Q3, 40–52 = Q4. A reviewed extra week, if supported, remains Q4. |
| Quarterly | Standard periods 1–4 = Q1–Q4 respectively. |
| Yearly | The single standard period is Q1. |
| 4 Week | Standard periods 1–3 = Q1, 4–6 = Q2, 7–9 = Q3, and 10–13 = Q4. A final extended day belongs to the Q4 period it extends. |
| 4/4/5, 4/5/4, 5/4/4 | The three standard periods in each pattern are Q1, Q2, Q3, and Q4 in order; the 12th standard period is Q4. |
| Other accounting calendar | Do not infer; require the user’s manual `QuarterNum` for every row, each in 1–4. |

An adjustment row takes the quarter of the one non-adjusting period it overlaps:
an opening adjustment is Q1; an adjustment at a quarter end remains in that
ending quarter; and a closing adjustment inherits the final standard period's
quarter. The closing quarter is Q4 for every generated frequency except Yearly,
whose single standard period and all overlapping adjustments are Q1. Reject a
row that does not overlap exactly one standard period before assigning its
quarter.

## Reusable Technical Evidence Baseline

Persist reviewed, non-secret technical evidence under
`project/{project_id}/baselines/erp/financials/manage-accounting-calendars/` so
later Codex sessions can reuse it. Record the task code, target environment
identity, Fusion release, collection timestamp, template-only export receipt,
template artifact path and fingerprint, and CSV member names and header order.

When this project has no compatible baseline, obtain one template-only package
for `GL_MANAGE_ACCOUNTING_CALENDARS` through
`shared.setup-export.task-level-export` automatically as normal preflight under
the user's calendar request. Do not ask for a separate conversational approval.
The route must use `setupTaskCSVTemplateExports`, not the populated
`setupTaskCSVExports` endpoint. Validate and persist the downloaded template
before generating a package.

Reuse this baseline only when the task code, target environment, Fusion
release, artifact fingerprint, and package requirements match. Fetch and
persist a fresh template-only package when the release changes, a required
package member or column is absent, the stored artifact cannot be verified, or
package validation detects a structural change. Do not request a Data Only
Export; documented codes and defaults remain valid without exported setup rows.

Do not treat a reusable baseline as duplicate-check evidence. Always run fresh
calendar and period LOV checks before package generation and immediately before
import.

## Generic Bootstrap Profile

Use this profile only after the newly fetched and validated template-only
package establishes the three required ZIP members and their header order. It
is a generic starter contract, not customer configuration data:

| Field | Bootstrap value |
|---|---|
| CalendarTypeCode | `ACCOUNTING` |
| SecurityFlag, LegacyCalendarFlag, LegacyRulesEnabledFlag | `N` |
| NonAdjPeriodFreqCode | `MONTH` for a monthly calendar |
| AdjPeriodFreqCode | `1_YEAR_END` for one closing adjustment; `1_BEGIN_1_END` for one opening and one closing adjustment |
| Parent linkage | Populate the same reviewed `PeriodSetName` on `GL_PERIOD_SET.csv` and every `GL_PERIOD_DEF.csv` row |
| Dates | Use `yyyy/MM/dd`; set `LatestYearStartDate` to the latest non-adjusting `YearStartDate`. When extending a calendar, derive the added fiscal-year start from the day after the preceding fiscal year's final non-adjusting period; do not default it to January 1. |

Before use, require fresh duplicate LOV checks, template-header equality,
period/count/date validation, naming resolution, an immutable Data Loader
preview, and explicit approval. Stop on any Fusion validation error; do not
retry a changed package without a new preview and approval.

### Exact Standard-Period Counts

Validate the non-adjusting rows against the selected frequency before adding
adjustments. These are validation contracts, not values to infer from a prior
calendar: Monthly has 12, Weekly 52, Quarterly 4, Yearly 1, 4/4/5 12, 4/5/4
12, 5/4/4 12, and 4 Week 13 standard periods. `OTHER` has only the explicit
user-supplied rows and count. Adjustment rows do not increase the standard
period count.

### Budgetary-Control-Only Calendar Defaults

Budgetary-control-only calendars are not ordinary `OTHER` accounting calendars.
Use calendar type `COMMITMENT`, `OTHER` frequency, and the explicit requested
number of budget periods. Do not infer the count from a fiscal frequency and do
not add adjustment rows. Apply the template-supported budget-period default
naming rather than `MMMYY*` or `PRDNUM*` formatting. The observed UI behavior
for budget year 1 uses `PRD_01-01`, `PRD_02-01`, and so on; this example shows
the naming shape, not a fixed 24-period default.

The approved UI examples show that a budgetary-control-only calendar accepts
both one and twelve standard periods. Treat the count as any positive integer;
do not impose a fixed 12- or 24-period default or maximum. A zero count is
invalid.

### Reviewed 5/4/4 Adjustment Geometry

For `5_4_4`, each fiscal quarter contains standard periods of five, four, and
four weeks, for 13 weeks per quarter and 52 standard weeks per fiscal year.
The reviewed `1_BEGIN_1_END` shape has 14 rows: opening adjustment period 1 on
the fiscal start date, standard periods 2 through 13 in the 5/4/4 sequence,
and closing adjustment period 14 on the final standard-period end date.

The reviewed `1_MID_2_END` shape inserts its one-day midyear adjustment after
the second fiscal quarter and appends two one-day adjustments on the final
standard-period end date. The reviewed `QUARTERLY` shape inserts one one-day
adjustment at each fiscal-quarter end. Every adjustment overlaps exactly one
standard period and uses its own sequential period number in the generated
name; the four-digit requested year is written only to date and period-year
fields, while any period-name year token is rendered through the selected
format.

The remaining reviewed `5_4_4` policies use these exact shapes:

| Policy | Reviewed shape |
|---|---|
| `NONE` | Twelve standard rows, numbered 1 through 12, with no adjustment rows. Fusion presents a recommendation to include a year-end adjustment but permits the explicitly selected no-adjustment definition; do not add one implicitly. |
| `1_YEAR_END` | Twelve standard rows followed by adjustment row 13 on the final standard-period end date. |
| `2_YEAR_END` | Twelve standard rows followed by adjustment rows 13 and 14, both on the final standard-period end date. |
| `1_MID_1_END` | Standard rows 1 through 6; one-day midyear adjustment row 7 at the end of fiscal quarter 2; standard rows 8 through 13; and one-day year-end adjustment row 14 on the final standard-period end date. |

For every reviewed `5_4_4` adjustment policy, retain the 5/4/4 standard-period
dates and fiscal-quarter assignments. An adjustment row is one day, shares the
overlapped standard period's fiscal quarter, and never replaces or shortens a
standard period.

### Generic Generated-Calendar Adjustment Geometry

Apply this model to every generated non-adjusting frequency (Monthly, Weekly,
4 Week, retail 4/4/5 variants, Quarterly, and Yearly) after first generating
its standard periods from the requested fiscal start and frequency. Do not use
it for `NonAdjPeriodFreqCode=OTHER`; that frequency requires explicit manual
rows.

| Adjustment policy | Generic row placement |
|---|---|
| `NONE` | Generate standard periods only. |
| `1_YEAR_END` / `2_YEAR_END` | Append one/two sequential adjusting rows on the final standard period's end date. |
| `1_BEGIN_1_END` | Put the first adjusting row on the fiscal start date, then number standard rows after it; append one closing adjusting row on the final standard period's end date. |
| `1_MID_1_END` / `1_MID_2_END` | Insert one adjusting row at the fiscal midyear boundary, then append one/two sequential adjusting rows at the final standard period's end date. |
| `QUARTERLY` | Insert one adjusting row at each fiscal-quarter-end boundary. |
| `OTHER` with explicit positive whole-number count *n* | Append *n* sequential adjusting rows on the final standard period's end date. |

Number all rows sequentially in display order. An opening adjustment overlaps
the first standard period; each midyear, quarterly, and closing adjustment
overlaps exactly one preceding standard period. Derive standard-period count,
fiscal midyear, and quarter boundaries from the chosen non-adjusting frequency,
not from a fixed monthly row number. Use the selected CY/FY convention when
rendering every row name; naming never changes these boundaries.

For `OTHER`, do not shorten, replace, or otherwise change the generated standard
rows. `AdjPeriodsNum` equals *n*, `NonAdjPeriodsNum` retains the frequency's
standard count, and `TotalPeriodsNum` is their sum. The appended rows inherit
the final standard row's year and quarter. This rule is target-confirmed for
both month-based and Yearly generated calendars and applies to every compatible
generated frequency.

Fusion UI evidence establishes two exceptions: for `YEAR` and `4_WEEK`, block
`1_MID_1_END`, `1_MID_2_END`, and `QUARTERLY`. Treat other
frequency/adjustment combinations as requiring the normal preview and
post-load validation; do not infer their technical codes from LOV output.

After load, use `accountingPeriodsLOV` to validate the generated standard and
adjustment counts, sequential numbering, standard-period continuity, dates,
and `AdjustmentPeriodFlag`. LOV validates the resulting shape; it does not
prove the saved adjustment-frequency configuration. Verify it through declared
endpoint/framework evidence; if unavailable, disclose the limit. Never use UI.

### Generic Monthly Calendar with Opening and Closing Adjustments

For a month-based fiscal calendar, use 12 continuous non-adjusting periods.
For `1_BEGIN_1_END`, derive every date, quarter, and name from the requested
fiscal start date and the chosen naming format:

| Row | Period name | Period number | Quarter | Dates | Adjusting |
|---|---|---:|---:|---|---|
| Opening adjustment | Generated opening-adjustment name | 1 | 1 | Fiscal start date only | Yes |
| Normal fiscal months | Generated from selected format | 2 through 13 | 1 through 4 | Each fiscal month | No |
| Closing adjustment | Generated closing-adjustment name | 14 | 4 | Final non-adjusting period end date only | Yes |

`FirstPeriod` and `SamplePeriodName` must be the first normal period in the
fiscal year. Each adjustment must overlap exactly one related non-adjusting
period. Do not use an unreviewed generic adjustment prefix, period number 0,
or a next-year first period. If the selected UI format does not produce this
pattern, stop and require target evidence rather than extrapolating it.

### Reviewed Weekly Calendar with Opening and Closing Adjustments

For a weekly calendar using `1_BEGIN_1_END`, retain the reviewed row shape:

| Row group | Period numbers | Dates | Adjusting |
|---|---|---|---|
| Opening adjustment | 1 | Fiscal-year start date only | Yes |
| Standard weeks | 2 through 53 | 52 continuous seven-day weeks beginning on the fiscal-year start date | No |
| Closing adjustment | 54 | Final standard week's end date only | Yes |

The final standard-week boundary is deterministic: fiscal start date plus 363
days. For example, a 2031/01/01 start ends on 2031/12/30. The fiscal-year label
does not require the 52-week calendar to extend through Gregorian December 31.
Do not ask the user to reconfirm this canonical boundary. Ask only when the
request explicitly requires a conflicting end date or a 53rd standard week.

Do not model this as 52 standard rows plus one adjustment. The two adjustment
rows must each overlap exactly one adjacent standard week. Treat this pattern
as a reviewed `1_BEGIN_1_END` contract; require a new target preview before
using a different naming format or adjustment code.

### Reviewed Weekly Calendar with Quarterly Adjustments

For a weekly calendar using `QUARTERLY`, retain 52 continuous seven-day
standard weeks and insert one single-date adjustment after each group of 13
standard weeks:

| Row group | Sequential period numbers | Quarter |
|---|---:|---:|
| Standard weeks 1 through 13 | 1 through 13 | 1 |
| First-quarter adjustment | 14 | 1 |
| Standard weeks 14 through 26 | 15 through 27 | 2 |
| Second-quarter adjustment | 28 | 2 |
| Standard weeks 27 through 39 | 29 through 41 | 3 |
| Third-quarter adjustment | 42 | 3 |
| Standard weeks 40 through 52 | 43 through 55 | 4 |
| Fourth-quarter adjustment | 56 | 4 |

Each adjustment uses the preceding standard week's end date as both its start
and end date. Derive those dates from the requested fiscal start rather than
from calendar-month or calendar-quarter boundaries.

### Generic Monthly Adjustment Shapes

For a 12-month fiscal calendar, use these row shapes. Every adjustment row is
one day and overlaps the indicated standard period; period numbers remain
sequential. Calculate dates from the fiscal start, fiscal midyear, quarter
ends, and final non-adjusting-period end date.

| Adjustment code | Standard rows | Adjustment rows |
|---|---:|---|
| `NONE` | 1–12 | None |
| `1_YEAR_END` | 1–12 | 13 on fiscal year end |
| `2_YEAR_END` | 1–12 | 13 and 14 on fiscal year end |
| `1_BEGIN_1_END` | 2–13 | 1 on fiscal start; 14 on fiscal year end |
| `1_MID_1_END` | 1–6 and 8–13 | 7 at fiscal midyear; 14 at fiscal year end |
| `1_MID_2_END` | 1–6 and 8–13 | 7 at fiscal midyear; 14 and 15 at fiscal year end |
| `QUARTERLY` | 1–3, 5–7, 9–11, 13–15 | 4, 8, 12, and 16 at the successive fiscal-quarter ends |
| `OTHER` with count *n* | 1–12 | 13 through 12 + *n*, all at fiscal year end |

These are target-proven generic patterns. For a different non-adjusting
frequency or naming format, use documented rules and declared endpoint/FSCR
evidence before generating the package; never obtain a live UI preview.

When applying these patterns with a `CY` format, render each row's name using
that row's calendar-year token. With an `FY` format, render all names using the
applicable fiscal-year token. The fiscal start/end and adjustment dates remain
unchanged.

### OTHER-Frequency Manual Naming Contract

For `OTHER`, manual names and dates remain authoritative, but the FSM header must still include a reviewed nonblank `PeriodNameSeparatorCode` and `SamplePeriodName`. Use `SEP_DASH` only when Dash is selected and evidenced. Set `SamplePeriodName` to the first reviewed manual period name. Do not leave either field blank merely because the UI hides the period-name-format region.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| CAL.DEFAULT | step | 5 | apply_default | ready->CAL.DESIGN_GATE;blocked->CAL.STOP_DEFAULTS | CAL.LOOKUP_EXISTING | stop | Calendar does not exist |

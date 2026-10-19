# Accounting Calendar FSM Bulk Intake

## Accepted Bulk Inputs

| Input Format | What Must Be Provided | How Rows Are Processed |
|---|---|---|
| GL_PERIOD_SET.csv and GL_PERIOD_DEF.csv | Same-task template-compatible headers plus documented codes and required values | Validate calendar row first, then validate non-adjusting rows and adjustment rows separately. |
| FSM ZIP | ASM_SETUP_CSV_METADATA.xml, GL_PERIOD_SET.csv, and GL_PERIOD_DEF.csv at ZIP root | Obtain metadata and package structure from the validated template-only project baseline. A permitted update may separately use its controlled current-value source; never use current-data export rows to define package shape or a new calendar. |

## Column Guidance

| Column Type | Allowed Fields | What Happens |
|---|---|---|
| Calendar | PERIOD_SET_NAME, `CalendarStartDate`, `LatestYearStartDate`, and template-required calendar attributes | Enforce the 15-character identifier, require both dates to be nonblank, and reconcile `LatestYearStartDate` to the latest non-adjusting `YearStartDate`. |
| Period | PERIOD_NAME, PERIOD_SET_NAME, START_DATE, END_DATE, PERIOD_TYPE, PERIOD_YEAR, PERIOD_NUM, QUARTER_NUM, ENTERED_PERIOD_NAME, ADJUSTMENT_PERIOD_FLAG when required | Reject gaps or overlap among non-adjusting rows; permit valid adjustment-date sharing. |
| Encoding and dates | UTF-8 without BOM; `yyyy/MM/dd` format | Preserve template-backed field order and date format; never substitute UI labels for documented code values. |
| Header reconciliation | AdjPeriodsNum, NonAdjPeriodsNum, TotalPeriodsNum | Reconcile counts with child period rows before ZIP creation. |
| Parent linkage | GL_PERIOD_SET.UserPeriodSetName and PeriodSetName | Populate child-row parent keys from the reviewed calendar header. |

## Preview and Execution Rules

| Gate | Requirement |
|---|---|
| ZIP creation | Do not generate a ZIP until template metadata is available, documented defaults and user inputs are resolved, and the source CSVs pass calendar-header, row, count, encoding, and linkage review. |
| Import | Do not submit the ZIP until the readiness record is complete, the final ZIP passes the same calendar-package review, and live approval is explicit. |
| Existing calendar update | Require a complete exact-target current-value source before package construction: a verified successful FSCR creation package from the current project/session, otherwise one automatically acquired full task data export. Description edits, period-name-format changes while adding a new fiscal year, and eligible period-number, quarter, start/end-date, or adjustment-flag edits remain permitted under their specific rules. Period edits also require lifecycle evidence. Require explicit approval only for the final FSM/Data Loader mutation, not for the read-only update-source export. |
| Multiple calendars | Create one isolated validation result and immutable preview per calendar. Do not produce a mixed ZIP or aggregate success when any calendar has an unresolved error. |
| Source derivation | Use a same-task template only for package shape and new-calendar authoring. For a permitted update, use the verified current-session FSCR package or exact target isolated from one full current-data export solely to preserve that calendar's current parent and period values. Never use unrelated exported calendars as defaults. |
| Template field map | Validate every emitted CSV value against the approved template-column classification. Request-derived values may populate only their documented calendar/period fields; blank-only context, DFF, global, audit, and system columns must remain blank. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| CAL.GENERATE_CSV | step | 7 | process_bulk | ready->CAL.PREVIEW;invalid->CAL.STOP_INVALID | CAL.DESIGN_GATE | stop | Approved-for-preview FSM definition |
| CAL.GENERATE_UPDATE_CSV | step | 11 | process_bulk | ready->CAL.UPDATE_PREVIEW;invalid->CAL.STOP_INVALID | CAL.VALIDATE_UPDATE | stop | Approved-for-preview permitted existing-calendar FSM update |

# Manage Calendar Events Defaulting Rules

## Source Basis

- Manage Calender Events Test Technical Design Document for FSCIR, Confluence page 21472672490, version 3
- calendar-events-ui-rest-mapping.md, developer-provided attachment
- Working Event and Allow shifts behavior, user-provided clarification
- Calendar Events payload date-time example, user-provided clarification
- Calendar flow UI and payload, user-provided request
- Calendar ID DAT-only derivation, user-provided clarification

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| AllDayFlag | true | Creating a calendar event and All Day is not explicitly selected | No; preserve an explicit user-provided boolean |  |
| CategoryCode | PH | Creating a calendar event and no category has been selected | No; a category remains required by the supplied UI contract and must resolve through the category lookup | resolve_calendar_event_category |
| AllowShiftFlag | true | Working Event is selected and Allow shifts has not been explicitly set | Yes; preserve an explicit user selection, including Not selected |  |
| Calendar event type | Event | Adding calendar events and no type is explicitly selected | No; preserve an explicit user selection | resolve_calendar_event_selector |
| Calendar event category | Public Holiday | The selected Calendar-page event type exposes Event Category and no category is explicitly selected | No; preserve an explicit user selection | resolve_calendar_event_category_filter |
| Calendar ID | A unique numeric DAT-only correlation value of no more than 18 digits | Creating a calendar through Data Loader | No; derive it internally and use the same value in the related parent and child DAT records |  |

## Defaulting Boundaries

| Situation | What Must Happen |
|---|---|
| All-day event dates | Users may select a multi-day range. Send the selected start date at 00:00:00 and the selected end date at 23:59:59 in YYYY-MM-DDTHH:mm:ss format without a time-zone suffix. Preserve the supplied date-time values without conversion. |
| Working event and Allow shifts | Selecting Working Event defaults Allow shifts to Selected. An explicit user selection of Not selected remains unchanged. |
| Calendar event category visibility | The Calendar-page Event Category selector is used only when the selected event type exposes category filtering. Its documented default is Public Holiday; do not apply a category filter when that selector is not in use. |
| Calendar ID for create | Derive the value only for DAT parent-child correlation. Keep it private, use it consistently for the calendar and its related events, and do not include it in the REST payload or Complete Summary. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCE.APPLY_DEFAULTS | step | 30 | apply_default | applied->MCE.ENFORCE_CALENDAR_EVENT_DESIGN;blocked->MCE.HANDLE_ERROR | MCE.RESOLVE_CATEGORY | stop | Required inputs and any category lookup have succeeded |
| MCAL.APPLY_DEFAULTS | step | 120 | apply_default | applied->MCAL.RESOLVE_EVENT_SELECTOR;blocked->MCE.HANDLE_ERROR | MCAL.VERIFY_UPDATE_CALENDAR_ID | stop | Creating a calendar or opening its event picker |

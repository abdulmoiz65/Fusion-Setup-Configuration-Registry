# Manage Calendar Events Input Validation

## Source Basis

- Manage Calender Events Test Technical Design Document for FSCIR, Confluence page 21472672490, version 3
- calendar-events-ui-rest-mapping.md, developer-provided attachment
- Calendar Events payload date-time example, user-provided clarification
- Calendar flow UI and payload, user-provided request
- REST date serialization, user-provided clarification
- Calendar ID Data Loader requirement, user-provided clarification and refreshed live metadata

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Calendar event identity | Calendar event name, category selection, calendar event code | Block before preview or write handoff | Supply all three values | Creating a calendar event | resolve_calendar_event_category |
| Calendar event date range | Start date and end date | Block before preview or write handoff | Supply both dates and validate their order | Creating or updating a calendar event |  |
| Calendar identity | Calendar name and calendar start date | Block before preview or write handoff | Supply both values; derive the DAT-only Calendar ID | Creating a calendar |  |
| Calendar event selection | Calendar event type and one or more selected calendar events | Block the event-picker action | Supply a type and one or more selected events | Adding events on a calendar | resolve_calendar_events_for_calendar |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A category selection is supplied | Continue only after its selected category resolves to one category code | Use the resolved category code for the request candidate | resolve_calendar_event_category |
| A mutation is requested | Continue only after the separate writable execution contract, target describe evidence, preview, and current approval are present | Hand off validated facts; do not construct or submit a write in this resource layer |  |
| A calendar is requested | Continue only after calendar name and start date pass validation | Route to the Calendar-only workflow |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Calendar event name | Require a nonblank value | Creating or updating |  |
| Calendar event code | Require a nonblank value | Creating or updating |  |
| Category | Require a selection and submit its resolved code rather than its display meaning | Creating or updating | resolve_calendar_event_category |
| Description | Accept as optional | Creating or updating |  |
| All day | Require a boolean value; initialize through the documented default when omitted | Creating or updating |  |
| Start and end date | Require both values and reject an end that is before the start | Creating or updating |  |
| Date-time serialization | Send each date-time as YYYY-MM-DDTHH:mm:ss without a time-zone suffix. The user may select any start date and any end date, provided the end is not before the start. For an all-day event, send the selected start date at 00:00:00 and the selected end date at 23:59:59; preserve the supplied date-time values without conversion | A request candidate contains dates |  |
| Half day for elapsed work schedules, Working event, Allow shifts | Accept boolean values when supplied; do not infer an undocumented server-side dependency | Creating or updating |  |
| Calendar name | Require a nonblank value | Creating or updating a calendar |  |
| Calendar ID in Data Loader source | Include the CalendarId column in every absenceCalendars DAT parent record. For create, derive one unique numeric DAT-only correlation value of no more than 18 digits and use that same value in every related parent and child record. Do not send it in the REST payload. For update or a follow-on event add, require only the Calendar ID fetched from the created or existing calendar, and retain that exact value in the parent and child records | Creating or updating a calendar through Data Loader | verify_calendar_id_for_update |
| Calendar start date | Require a date-only value in strict YYYY-MM-DD format | Creating or updating a calendar |  |
| Calendar end date | Accept as optional; when supplied, require strict YYYY-MM-DD format | Creating or updating a calendar |  |
| Date-only serialization | Serialize every date-only value, including Calendar Start Date and Calendar End Date when supplied, as strict YYYY-MM-DD in both the Data Loader source and any REST request. Do not use slash-separated dates, locale-specific dates, date-time values, or a time-zone suffix for a date-only value | A request candidate or Data Loader source contains a date-only value |  |
| Calendar description | Accept as optional | Creating or updating a calendar |  |
| Calendar event type | Accept the Calendar-page selection provider value; use the documented default only when omitted | Adding events on a calendar | resolve_calendar_event_selector |
| Calendar event category | Require a selected category only when the selected event type exposes category filtering; use its resolved category code only for filtering the event picker | Adding events by event category | resolve_calendar_event_category_filter |
| Selected calendar events | Require one or more selections for an event-picker add action; allow multiple selections and retain each selected event as a distinct child record | Adding events on a calendar | resolve_calendar_events_for_calendar |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCE.VALIDATE_INPUT | step | 10 | validate_input | valid->MCE.ROUTE_FLOW;invalid->MCE.HANDLE_ERROR | none | stop | Before defaulting, design enforcement, preview, or mutation handoff |
| MCE.ROUTE_FLOW | decision | 15 | evaluate_result | calendar_event->MCE.RESOLVE_CATEGORY;calendar->MCAL.VALIDATE_INPUT;invalid->MCE.HANDLE_ERROR | MCE.VALIDATE_INPUT | stop | A request identifies either Calendar Event maintenance or Calendar maintenance |
| MCAL.VALIDATE_INPUT | step | 110 | validate_input | valid->MCAL.VERIFY_UPDATE_CALENDAR_ID;invalid->MCE.HANDLE_ERROR | MCE.ROUTE_FLOW | stop | Creating or updating a calendar |

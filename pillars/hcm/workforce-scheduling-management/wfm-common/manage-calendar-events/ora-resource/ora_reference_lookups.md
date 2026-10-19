# Manage Calendar Events Reference Lookups

## Source Basis

- Manage Calender Events Test Technical Design Document for FSCIR, Confluence page 21472672490, version 3
- calendar-events-ui-rest-mapping.md, developer-provided attachment
- Workforce Scheduling Common Manage Common Lookups routing and lookup type, user-provided request
- Calendar flow UI and payload, user-provided request
- Calendar ID Data Loader requirement, user-provided clarification and refreshed live metadata

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_calendar_event_category | A category selection must be converted to the request category code | Selected category display meaning or selected code; LookupType=PER_CAL_EVENT_CATEGORY | Delegate to hcm.workforce-scheduling-management.workforce-scheduling-common.manage-common-lookups with LookupType=PER_CAL_EVENT_CATEGORY. Calendar Events must not invoke a Common Lookup REST endpoint directly. | Provider-returned LookupType, LookupCode, Meaning, and active/selectable-state evidence | Require exactly one active selectable provider result matching the selected category; LookupCode is the request key and Meaning is the display value | CategoryCode from provider-returned LookupCode; receipt-only category meaning | Zero or many matches, an absent matching lookup type, or unavailable provider evidence blocks the request candidate. |
| resolve_calendar_event_selector | An event-picker type is supplied or defaulted on the Calendar page | Selected type display meaning or selected code; LookupType=ORA_ANC_ORG_EVENT_SELECTOR | Inferred GET {FA_HOST}/fscmRestApi/resources/11.13.18.05/commonLookupsLOV with finder LookupTypeFinder;LookupType=ORA_ANC_ORG_EVENT_SELECTOR and onlyData=true | LookupCode, Meaning, and active/selectable-state evidence | Require exactly one active selectable result matching the selected type; retain its business meaning for display | Selected event-picker type | Zero or many matches, an absent lookup type, or unavailable provider evidence blocks the event-picker action. |
| resolve_calendar_event_category_filter | The selected Calendar-page event type exposes Event Category | Selected category display meaning or selected code; LookupType=PER_CAL_EVENT_CATEGORY | Inferred GET {FA_HOST}/fscmRestApi/resources/11.13.18.05/commonLookupsLOV with finder LookupTypeFinder;LookupType=PER_CAL_EVENT_CATEGORY and onlyData=true | LookupCode, Meaning, and active/selectable-state evidence | Require exactly one active selectable result matching the selected category; retain Meaning for display and use LookupCode only to filter the event provider | Selected event category and private category filter value | Zero or many matches, an absent lookup type, or unavailable provider evidence blocks the event-picker action. |
| resolve_calendar_events_for_calendar | One or more calendar events are selected for a calendar | Calendar start date as YYYY-MM-DD, selected event names or identifiers, optional event category, and event-name search text | Inferred paginated GET {FA_HOST}/hcmRestApi/resources/11.13.18.05/calendarEvents with orderBy StartDateTime,CalendarEventName. Keep the Calendar-page input date-only. Do not send a StartDateTime predicate: this provider rejects date-only input and does not reliably accept timestamp literals. When category filtering is selected, q is CategoryCode = '{resolved category}'; otherwise omit q. Do not send a lower(CalendarEventName) predicate. After retrieval, compare each returned event's YYYY-MM-DD StartDateTime portion to the Calendar-page start date and compare its CalendarEventName case-insensitively to the supplied search text. | CalendarEventId, CalendarEventName, CalendarEventCode, StartDateTime, EndDateTime, CategoryCode | Require every selected event to match one currently returned provider record, pass the date-only comparison, and uniquely match the requested event name; retain the display name for the user-facing result and the returned identifier privately for the child record | No match, duplicate match, unavailable provider evidence, or a date-only value sent directly to StartDateTime blocks the event-picker action. |
| verify_calendar_id_for_update | A calendar update or follow-on event add is requested through Data Loader | Calendar ID fetched from the existing or newly created calendar | GET {FA_HOST}/hcmRestApi/resources/11.13.18.05/absenceCalendars/{CalendarId} with fields CalendarId,Name | CalendarId and Name | Require the returned CalendarId to equal the fetched Calendar ID. Do not use a user-supplied, name-derived, or newly generated value | Verified Calendar ID for the update DAT parent and child records | A missing, unavailable, or nonmatching record blocks preview and update. Initial calendar create is not applicable to this verification. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Category is displayed or selected by meaning | Call hcm.workforce-scheduling-management.workforce-scheduling-common.manage-common-lookups with LookupType=PER_CAL_EVENT_CATEGORY, resolve the selected LookupCode, and do not submit the meaning as CategoryCode. |
| The common-lookups provider cannot verify the lookup type or active selectable result | Stop before a live write; do not fall back to a direct Common Lookup REST request from Calendar Events. |
| Authentication or authorization fails | Stop; do not interpret the failure as a missing category. |
| The Calendar-page event type is omitted | Apply the documented Event default, then resolve it through resolve_calendar_event_selector. |
| The Calendar-page event type is Event Category | Resolve the required Event Category through resolve_calendar_event_category_filter before retrieving events. |
| A Calendar-page start date or event-name search is used to retrieve events | Accept and retain only the supplied YYYY-MM-DD date. Retrieve category candidates without a StartDateTime or lower(CalendarEventName) predicate, then compare each returned StartDateTime's YYYY-MM-DD date portion and CalendarEventName locally. Never require a time from the user or send a date-only value to StartDateTime. |
| Calendar events are selected | Retrieve and verify them through resolve_calendar_events_for_calendar; do not use a display name as the child-record identifier. |
| A calendar update or follow-on event add is requested | Verify the fetched Calendar ID through verify_calendar_id_for_update and retain that same value in the update DAT parent and child records. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCE.RESOLVE_CATEGORY | step | 20 | reference_lookup | resolved->MCE.APPLY_DEFAULTS;blocked->MCE.HANDLE_ERROR;failure->MCE.HANDLE_ERROR | MCE.VALIDATE_INPUT | stop | A category selection is required for a calendar event |
| MCAL.RESOLVE_EVENT_SELECTOR | step | 130 | reference_lookup | event->MCAL.CHECK_EVENT_DEPENDENCY;event_category->MCAL.RESOLVE_EVENT_CATEGORY;blocked->MCE.HANDLE_ERROR;failure->MCE.HANDLE_ERROR | MCAL.APPLY_DEFAULTS | stop | The Calendar-page event picker is used |
| MCAL.RESOLVE_EVENT_CATEGORY | step | 140 | reference_lookup | resolved->MCAL.CHECK_EVENT_DEPENDENCY;blocked->MCE.HANDLE_ERROR;failure->MCE.HANDLE_ERROR | MCAL.RESOLVE_EVENT_SELECTOR | stop | The selected Calendar-page event type exposes Event Category |
| MCAL.RESOLVE_EVENTS | step | 160 | reference_lookup | resolved->MCAL.ENFORCE_CALENDAR_DESIGN;blocked->MCE.HANDLE_ERROR;failure->MCE.HANDLE_ERROR | MCAL.CHECK_EVENT_DEPENDENCY | stop | One or more calendar events are selected for a calendar |
| MCAL.VERIFY_UPDATE_CALENDAR_ID | step | 115 | reference_lookup | verified->MCAL.APPLY_DEFAULTS;not_applicable->MCAL.APPLY_DEFAULTS;blocked->MCE.HANDLE_ERROR;failure->MCE.HANDLE_ERROR | MCAL.VALIDATE_INPUT | stop | Updating a calendar through Data Loader; not applicable to create |

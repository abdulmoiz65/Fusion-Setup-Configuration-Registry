# Manage Calendar Events Design Enforcement

## Source Basis

- User-Facing Value Resolution Policy, user-provided authoring source, received 11 August 2026
- Manage Calender Events Test Technical Design Document for FSCIR, Confluence page 21472672490, version 3
- calendar-events-ui-rest-mapping.md, developer-provided attachment
- Workforce Scheduling Common Manage Common Lookups routing and lookup type, user-provided request
- Complete Summary and provider-owned approval handoff, user-provided request
- Working Event and Allow shifts behavior, user-provided clarification
- Calendar flow UI and payload, user-provided request

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Classification gate | Classify every value intended for a user-facing response as business-facing or internal |
| 2 | Resolution gate | Resolve each internal value privately from the highest-priority reliable source available |
| 3 | Meaning gate | Evaluate conditions and recommendations using the verified business meaning |
| 4 | Presentation gate | Present only verified labels, business names, meanings, descriptions, user-facing field labels, and intentionally displayed business codes |
| 5 | Sanitization gate | Confirm that no unresolved value, internal identifier, implementation detail, or real identifier in a technical URL remains |
| 6 | Complete Summary | Generate the required business-only summary from verified structured values after validation, lookup resolution, defaulting, and design enforcement, then hand off to the unchanged provider-owned approval process |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any user-facing response | Error |  | A lookup value, enumeration, record key, REST key, internal object or attribute name, service alias, endpoint identifier, finder value, bind value, or other implementation-only value would be exposed | Resolve the value privately and present only its verified business label, name, meaning, or description | Yes |
| A user supplied an internal value | Error |  | Confirmation, explanation, or recommendation repeats the raw value | Accept the value only as private processing input, verify its business meaning, and use only that meaning in the response | Yes |
| Both an internal value and display label were supplied | Error |  | The pair was not verified as one selection, or a conflict message would disclose the internal value | Verify the pair; when inconsistent, report inconsistent selection information using business language only | Yes |
| An internal value cannot be resolved | Error |  | The response guesses a label, exposes the raw value, or recommends an action based on it | Mark the selection unresolved or incomplete and request the displayed label or relevant lookup information | No |
| A field or attribute is mentioned to the user | Error |  | An internal field name is used when a verified user-facing label exists | Use the verified label; otherwise describe the field by business purpose without exposing the internal name | Yes |
| A code is proposed for display | Error |  | The UI does not explicitly present it as a meaningful business field, or it is only a lookup, enumeration, database, or implementation identifier | Omit it unless UI evidence confirms an intentionally displayed business code under a user-facing label | Yes |
| A technical URL is shown | Error |  | The URL contains a real record or implementation identifier | Replace the value with a descriptive placeholder such as `{RECORD_IDENTIFIER}` | Yes |
| Final response construction | Error |  | A recommendation uses unresolved or implementation-only values, an internal code-to-label mapping is exposed, or the response requires implementation knowledge | Resolve first, reason second, and present only the business meaning | Yes |
| Working event is selected and Allow shifts is explicitly deselected | Info |  | The default was incorrectly reapplied over the explicit selection | Preserve the explicit Not selected value; the Selected default applies only when Allow shifts was not explicitly set | Yes |
| A calendar-event write is proposed | Error |  | Read-only target describe evidence, exact date-time contract, preview, or current approval is absent | Complete the separate writable workflow; do not submit from ora-resource guidance | No |
| A calendar-event category is resolved | Error | resolve_calendar_event_category | Calendar Events directly invokes a Common Lookup REST endpoint or the provider cannot return one active selectable category | Delegate category resolution to Manage Common Lookups with LookupType=PER_CAL_EVENT_CATEGORY and use only its provider-returned LookupCode for the request | No |
| A provider-owned approval is about to begin | Error |  | The Complete Summary is absent; is not generated only from verified structured values; omits a user-provided business value or an actually applied default; includes blank, unused, metadata-only, diagnostic, or technical information; or presents a populated child record without business labels | Regenerate the Complete Summary using the required business-only format, then continue to the unchanged provider-owned approval process | Yes |
| A calendar is created or updated | Error |  | Calendar name or start date is missing | Supply the missing Calendar-page value | Yes |
| Calendar events are added | Error | resolve_calendar_events_for_calendar | A selected event is not a unique currently available Calendar-page event or is already associated | Correct the selected event before preview | No |
| Calendar event category filtering is used | Error | resolve_calendar_event_category_filter | The event category is not one active selectable category, or its private filter value is used as a user-facing value | Resolve one category, use its business meaning in the response, and use the private value only for filtering | No |

## User-Facing Resolution Source Order

| Priority | Verified Source | Required Use |
|---|---|---|
| 1 | Display label supplied with the selected value | Use after confirming that it represents the selected value |
| 2 | Name, Meaning, DisplayName, Label, or Description attribute | Use the verified display attribute, not its internal key |
| 3 | Active list of values or selection provider | Resolve against the active selectable result |
| 4 | Configured value and display attributes | Use the configured display attribute after verifying the mapping |
| 5 | Verified lookup-service result | Resolve privately and retain only sanitized evidence for the response |
| 6 | Verified REST response display attribute | Use a documented display attribute from the selected record |
| 7 | Verified metadata definition | Use the documented user-facing label or meaning |
| 8 | Verified static value-to-label mapping | Use only a checked and current mapping |
| 9 | Checked-in application source | Use only when higher-priority sources are unavailable and the mapping is explicit |

Do not derive a label by removing prefixes, replacing underscores, changing
capitalization, expanding abbreviations, or comparing similar internal values.

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_calendar_event_category | Before preview or mutation handoff when a calendar-event category is selected or defaulted | One active selectable category from hcm.workforce-scheduling-management.workforce-scheduling-common.manage-common-lookups using LookupType=PER_CAL_EVENT_CATEGORY; provider-returned LookupCode and receipt-only Meaning | ora_reference_lookups.md |
| resolve_calendar_event_selector | Before calendar-event selection when the Calendar-page event picker is used | One active selectable event-picker type | ora_reference_lookups.md |
| resolve_calendar_event_category_filter | Before calendar-event retrieval when the selected event type exposes Event Category | One active selectable category and its private filter value | ora_reference_lookups.md |
| resolve_calendar_events_for_calendar | Before preview or mutation handoff when calendar events are added | Every selected event's verified business name and private child-record identifier | ora_reference_lookups.md |

## Complete Summary Contract

Always generate the Complete Summary only after validation, lookup resolution, defaulting, and design enforcement have succeeded. Build it solely from verified structured values. Keep technical values internally for validation and provider execution.

- Include every user-provided business value and every default that was actually applied.
- Place actually applied defaults only in Defaults Applied.
- Omit blank, null, unused, and metadata-only values. Add a populated child section only when it has values, and use business labels for its records and values.
- Render resolved identifiers as business display names, resolved codes as verified business meanings, Boolean values as Selected or Not selected, Enabled or Disabled, or Yes or No, and statuses as business-friendly values such as Draft or Submitted.
- Never put IDs, codes, keys, internal identifiers, opaque links, request identifiers, fingerprints, REST or API details, import-file details, resolver names, rule identifiers, task-node names, internal statuses, diagnostics, warnings, or technical notes in the summary.

Use this exact user-facing structure and no additional user-facing content:

## Complete Summary

| Business Setting | Selected Value |
|---|---|
| <business label> | <verified business display value> |

## Defaults Applied

| Business Setting | Default Applied |
|---|---|
| <business label> | <verified default display value> |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCE.ENFORCE_CALENDAR_EVENT_DESIGN | decision | 40 | design_enforcement | passed->MCE.ENFORCE_USER_FACING_VALUES;blocked->MCE.HANDLE_ERROR | MCE.APPLY_DEFAULTS | stop | Before preview or mutation handoff for a calendar event |
| MCE.ENFORCE_USER_FACING_VALUES | decision | 50 | design_enforcement | passed->MCE.COMPLETE_SUMMARY;blocked->MCE.HANDLE_ERROR | MCE.ENFORCE_CALENDAR_EVENT_DESIGN | stop | Before returning any user-facing setup response |
| MCE.COMPLETE_SUMMARY | step | 55 | design_enforcement | generated->MCE.PROVIDER_APPROVAL_HANDOFF;blocked->MCE.HANDLE_ERROR | MCE.ENFORCE_USER_FACING_VALUES | stop | Generate the Complete Summary from verified structured user values and actually applied defaults before provider-owned approval |
| MCAL.ENFORCE_CALENDAR_DESIGN | decision | 170 | design_enforcement | passed->MCAL.ENFORCE_USER_FACING_VALUES;blocked->MCE.HANDLE_ERROR | MCAL.CHECK_EVENT_DEPENDENCY | stop | Before preview or mutation handoff for a calendar |
| MCAL.ENFORCE_USER_FACING_VALUES | decision | 180 | design_enforcement | passed->MCAL.COMPLETE_SUMMARY;blocked->MCE.HANDLE_ERROR | MCAL.ENFORCE_CALENDAR_DESIGN | stop | Before returning any user-facing Calendar response |
| MCAL.COMPLETE_SUMMARY | step | 190 | design_enforcement | generated->MCAL.PROVIDER_APPROVAL_HANDOFF;blocked->MCE.HANDLE_ERROR | MCAL.ENFORCE_USER_FACING_VALUES | stop | Generate the Complete Summary from verified structured Calendar values and actually applied defaults before provider-owned approval |

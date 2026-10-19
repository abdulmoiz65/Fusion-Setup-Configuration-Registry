# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate workbook input | Confirm the supplied workbook has a readable Time Slots worksheet and the required time-slot row fields. |
| 2 | Validate business purpose | Confirm that every proposed time slot or time-slot support has a documented customer-service window, booking, routing, assignment-ordering, or quota-management purpose. |
| 3 | Validate slot design | Evaluate naming, status, all-day scope, Activity Type eligibility, and the applicable quota or availability design. |
| 4 | Assess change impact | Before removing time-slot support or changing a required slot, assess appointment, booking, routing, quota, UI, and API impact. |
| 5 | Block or correct | Block preview on any Error rule failure; permit only the documented pre-preview correction. |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| TS.BUSINESS_PURPOSE | A time slot or time-slot support is proposed | Error | | No documented customer-service window, booking, routing, assignment-ordering, or quota-management purpose exists | Create slots only for a defined operating purpose; do not add slots merely because the feature is available | Yes, before preview |
| TS.NAMING_AND_STATUS | A time slot is created or changed | Error | | The label is not consistent and sortable, or a required slot is inactive | Use stable, API-friendly labels such as 08-10; keep slots required by UI, APIs, booking, or routing active | Yes, before preview |
| TS.ALL_DAY_SCOPE | An all-day slot is associated to work | Error | | The work is actually constrained to operating or promised service-window times | Use an all-day slot only when work may occur at any time; otherwise associate only valid operating slots | Yes, before preview |
| TS.ACTIVITY_TYPE_ELIGIBILITY | Slots are associated with Activity Types | Error | | A type is associated with a slot in which it must not be booked, routed, or promised to customers | Associate each Activity Type only with eligible slots that reflect priority, operational, and customer-commitment rules | Yes, before preview |
| TS.QUOTA_DESIGN | Slots are used for quota-based booking or capacity management | Error | | Slots overlap or intersect, are shorter than a typical activity, or do not align with capacity categories | Use slots at least as long as a typical activity, preferably longer; avoid overlaps and align capacity categories to the slots in which work may be booked | Yes, before preview |
| TS.AVAILABILITY_DESIGN | Slots are used for availability-based booking | Error | | Slot structure cannot represent the intended service levels or customer windows | Use flexible slots, including intentional overlaps where different service levels require different windows; document the booking effect | Yes, before preview |
| TS.CHANGE_IMPACT | Time-slot support is removed or a required slot is changed | Error | | The impact on existing appointment windows, booking, routing, quota, UI, and API consumers is unassessed | Assess downstream impact before removing support or changing a required slot; validate representative booking and routing scenarios | Yes, before preview |

## Workbook Evidence and Fail-Closed Evaluation

Treat the supplied `Time Slots` worksheet as the local task-context source for
the fields below. These fields are validation evidence only: no value in this
table is sent in the Time Slots PUT body or to an association endpoint. A
missing, blank, generic, or ambiguous required evidence value is an Error and
blocks preview. Do not infer evidence from a label, display name, or API
response.

| Rule ID | Workbook evidence | Evaluation | Not applicable only when |
|---|---|---|---|
| TS.BUSINESS_PURPOSE | `Business Purpose` | Require a row-specific, documented customer-service, booking, routing, assignment-ordering, capacity, or quota-management purpose. A generic statement such as `required`, `standard`, or `default` fails. | Never for a proposed slot. |
| TS.NAMING_AND_STATUS | `Time Slot Label`, `Status`, `Business Purpose` | Require a unique label in one consistent, lexically sortable time-range convention for all bounded slots (for example, `08-10`), and require `Active` when the documented purpose indicates UI, API, booking, routing, assignment-ordering, or quota use. | Never for a created or changed slot. |
| TS.ALL_DAY_SCOPE | A supplied all-day indicator and `Business Purpose` | The direct REST workbook contract supports bounded slots only. Any all-day indicator set to true fails until a documented bounded-slot contract is supplied; do not silently omit it. | No all-day indicator is supplied. |
| TS.ACTIVITY_TYPE_ELIGIBILITY | `Eligible Activity Types`, `Business Purpose` | When Activity Types are listed, require row-specific evidence that each listed type may be booked, routed, or promised in the stated window. A list alone is insufficient; record the eligibility rationale in `Business Purpose` or an explicit workbook evidence field. | No Activity Types are listed. |
| TS.QUOTA_DESIGN | `Booking Model`, Start Time, End Time, `Business Purpose` | When `Booking Model` is `Quota-based`, require explicit evidence of typical activity duration and capacity-category alignment, then reject intersecting slots or slots shorter than the typical activity. | Booking Model is blank or `None`. |
| TS.AVAILABILITY_DESIGN | `Booking Model`, `Business Purpose` | When `Booking Model` is `Availability-based`, require documentation of the service level/customer window and the intended booking effect; overlaps are permitted only when this evidence explains the distinct service level. | Booking Model is blank or `None`. |
| TS.CHANGE_IMPACT | `Change Impact` plus the existing-record lookup | When a required existing slot is changed or time-slot support is removed, require documented impact on appointment windows, booking, routing, quota, UI, and API consumers and representative validation scenarios. | The item lookup establishes that the proposed slot is new and no support is being removed. |

`Booking Model` is limited to `None`, `Quota-based`, or `Availability-based`.
For quota or availability use, the current template has no dedicated columns
for typical duration, capacity-category alignment, service level, or booking
effect. The authoring contract therefore requires those details in a clearly
labelled workbook evidence field before the applicable rule can pass; the
runner must fail closed rather than invent them.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TS.DESIGN_BUSINESS_PURPOSE | decision | 5 | design_enforcement | pass->TS.DESIGN_NAMING_AND_STATUS;not_applicable->TS.DESIGN_NAMING_AND_STATUS;fail->TS.DESIGN_BLOCKED | TS.LOOKUP | stop | A time slot or time-slot support is proposed. |
| TS.DESIGN_NAMING_AND_STATUS | decision | 6 | design_enforcement | pass->TS.DESIGN_ALL_DAY_SCOPE;not_applicable->TS.DESIGN_ALL_DAY_SCOPE;fail->TS.DESIGN_BLOCKED | TS.DESIGN_BUSINESS_PURPOSE | stop | A time slot is created or changed. |
| TS.DESIGN_ALL_DAY_SCOPE | decision | 7 | design_enforcement | pass->TS.DESIGN_ACTIVITY_TYPE_ELIGIBILITY;not_applicable->TS.DESIGN_ACTIVITY_TYPE_ELIGIBILITY;fail->TS.DESIGN_BLOCKED | TS.DESIGN_NAMING_AND_STATUS | stop | An all-day slot is associated to work. |
| TS.DESIGN_ACTIVITY_TYPE_ELIGIBILITY | decision | 8 | design_enforcement | pass->TS.DESIGN_QUOTA;not_applicable->TS.DESIGN_QUOTA;fail->TS.DESIGN_BLOCKED | TS.DESIGN_ALL_DAY_SCOPE | stop | Slots are associated with Activity Types. |
| TS.DESIGN_QUOTA | decision | 9 | design_enforcement | pass->TS.DESIGN_AVAILABILITY;not_applicable->TS.DESIGN_AVAILABILITY;fail->TS.DESIGN_BLOCKED | TS.DESIGN_ACTIVITY_TYPE_ELIGIBILITY | stop | Slots are used for quota-based booking or capacity management. |
| TS.DESIGN_AVAILABILITY | decision | 10 | design_enforcement | pass->TS.DESIGN_CHANGE_IMPACT;not_applicable->TS.DESIGN_CHANGE_IMPACT;fail->TS.DESIGN_BLOCKED | TS.DESIGN_QUOTA | stop | Slots are used for availability-based booking. |
| TS.DESIGN_CHANGE_IMPACT | decision | 11 | design_enforcement | pass->TS.DESIGN_PASSED;not_applicable->TS.DESIGN_PASSED;fail->TS.DESIGN_BLOCKED | TS.DESIGN_AVAILABILITY | stop | Time-slot support is removed or a required slot is changed. |

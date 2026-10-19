# Benefit Bill Calendars Contract Boundaries

The exact developer-selected HDL object is `benefitBillCalendars`. Resolve its
live Data Loader schema before generating headers or loading files. The facts
below describe the documented REST contract, not a verified HDL field mapping.

## Calendar and Period Semantics

| Resource | Identity | Relationship |
|---|---|---|
| benefitBillCalendars | BillCycleId | Parent calendar |
| benefitBillPeriods | BillCalendarId | Child period; BillCycleId references its calendar |

Do not reverse the two IDs despite their names. Do not assume the REST child
is a standalone registered HDL object or that its casing equals the DAT
discriminator. Let the live template and supported keys determine linkage.

## Documented REST Input Checks

Calendar creation lists CalendarName, BillingFrequency, DaysOverdue, and
PaymentDueDay as required. CalendarName is limited to 240 characters,
BillingFrequency to 200, Description to 400, and PeriodType to 30.
DaysOverdue and PaymentDueDay are integers. Do not interpret display meanings
as lookup codes or impose an undocumented minimum/maximum.

Period fields include BillingPeriod, BillYear, PeriodStartDate, PeriodEndDate,
PaymentDueDate, PaymentOverdueDate, and Comments. Use the bill-period date
contract below for DAT values, not the generic slash-separated HDL default.
Confirm required fields,
nullability, length limits, and foreign keys for the chosen loader operation.
Do not carry read-only audit fields or display meanings into writable input.

## Bill-Period Date Format

Use `YYYY-MM-DD` for `PeriodStartDate`, `PeriodEndDate`, `PaymentDueDate`,
and `PaymentOverdueDate` in `benefitBillPeriods` DAT rows. For example:
`2026-01-01`, `2026-01-31`, `2026-01-02`, and `2026-01-12`.
For no-file monthly period generation, use the first and last calendar days of
each corresponding month. Preserve supplied period dates in file-based workflows.

Runtime evidence on 2026-09-28: a calendar-and-period DAT passed template
validation but failed during load with the resolved diagnostic:
`Provide the value in the YYYY-MM-DD format for PeriodEndDate.`
This confirms the end-date requirement; using the same ISO date-only format
for the other three date fields aligns with their documented REST types.
A corrected end-to-end load has not yet been confirmed. This is a scoped
bill-period serialization rule, not evidence that all HDL objects use ISO dates.

## Sources and Evidence

Reviewed 2026-09-27:

- [Oracle calendar creation contract](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-benefitbillcalendars-post.html)
- [Oracle child-period creation contract](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-benefitbillcalendars-billcycleid-child-benefitbillperiods-post.html)

These references support field semantics only. They neither authorize direct
REST execution in this HDL workflow nor establish target loader registration.
Live HDL registration, template, and end-to-end upload testing remain pending.

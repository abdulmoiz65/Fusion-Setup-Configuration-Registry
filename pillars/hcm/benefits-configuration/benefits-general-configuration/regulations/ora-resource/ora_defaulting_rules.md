# Benefit Regulations Defaulting Rules

## Date-Effective Defaults

Apply the mapping only to a section whose current Data Loader sample confirms
date-effectivity, `effectiveOf` availability, and support for the requested
operation. Omit `effectiveOf` entirely from any included section that does not
expose it; stop when the section contract is missing or ambiguous.

Use only valid ISO source dates (`YYYY-MM-DD`). Serialize the date inserted
into each `RangeStartDate` or `RangeEndDate` component of `effectiveOf` as
`YYYY-MM-DD` with zero-padded month and day; reject invalid or ambiguous dates.

For a supported date-effective Create, Update, or Correction row whose current
section exposes `EffectiveEndDate`, default an omitted value to the
end-of-time calendar date `4712/12/31`. Write it in the ISO DAT field as
`4712-12-31`; preserve an explicitly supplied valid ISO end date. An End date
operation requires an explicit `EffectiveEndDate` and never receives this
default. Do not apply it to Delete changes or ZAP, or add the field to a
section that does not expose it.

| Requested operation | `effectiveOf` derivation | Required input | Default permitted? |
| --- | --- | --- | --- |
| Create | `RangeStartDate=<EffectiveStartDate as YYYY-MM-DD>` | Create start date | Only target current date after explicit confirmation |
| Update | `RangeMode=UPDATE;RangeStartDate=<EffectiveStartDate as YYYY-MM-DD>` | Explicit update effective date | No |
| Correction | `RangeMode=CORRECTION;RangeStartDate=<EffectiveStartDate as YYYY-MM-DD>` | Exact existing slice start date | No |
| End date | `RangeMode=END_DATE;RangeEndDate=<EffectiveEndDate as YYYY-MM-DD>` | Explicit end date | No |
| Delete changes | `RangeMode=DELETE_CHANGES;RangeStartDate=<EffectiveStartDate as YYYY-MM-DD>` | Explicit date and scope | No |
| ZAP | `RangeMode=ZAP` | Explicit destructive intent | No |

`RangeMode` is part of `effectiveOf`; do not emit it as a separate DAT column.
Do not default an identity, non-create operation date, range, deletion scope,
or destructive choice. The EffectiveEndDate field default above does not
select an operation date. Apply only operations the current sample supports.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BEN_REG.APPLY_DEFAULTS | step | 20 | apply_default | applied->BEN_REG.CHECK_READINESS;blocked->BEN_REG.HANDLE_ISSUE | BEN_REG.VALIDATE_REQUEST | stop | Derive operation-specific YYYY-MM-DD effectiveOf only for sections that expose it, omit it elsewhere, apply the confirmed create start-date default, and default an omitted supported Create, Update, or Correction EffectiveEndDate to 4712-12-31 |

# Benefit Balances Defaulting Rules

## Date-Effective HDL Operation Mapping

Apply this mapping only after the current Data Loader sample confirms, for
each included section independently, that it is date-effective, exposes
effectiveOf, and supports the requested row operation. Omit effectiveOf
entirely from a section that does not expose it; stop if metadata is missing
or ambiguous.
Derive effectiveOf independently for each row's exact operation; never accept a
caller-authored range string. Do not default an operation effective date, range,
deletion scope, or destructive decision for a non-create operation. The
EffectiveEndDate field default below does not select an operation date. RangeMode is a
component of effectiveOf, not a separate DAT column.

Before interpolating `EffectiveStartDate` or `EffectiveEndDate` into `effectiveOf`,
parse the required source date using its documented input format and serialize
the calendar date as `YYYY-MM-DD` with zero-padded month and day. Reject an
invalid or ambiguous source date rather than guessing its format. Every
`RangeStartDate` and `RangeEndDate` component in the final `effectiveOf` must
use `YYYY-MM-DD` (for example, `RangeMode=UPDATE;RangeStartDate=2026-10-05`).

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EffectiveEndDate | 4712/12/31 | A supported date-effective Create, Update, or Correction row omits EffectiveEndDate and the current section exposes that field | No; preserve an explicit valid user value | |
| effectiveOf | RangeStartDate=<EffectiveStartDate as YYYY-MM-DD> | Create a date-effective row | No; require EffectiveStartDate, except where current metadata permits a documented create default | |
| effectiveOf | RangeMode=UPDATE;RangeStartDate=<EffectiveStartDate as YYYY-MM-DD> | Update a date-effective row | No; require selected effective-dated identity and explicit EffectiveStartDate | |
| effectiveOf | RangeMode=CORRECTION;RangeStartDate=<EffectiveStartDate as YYYY-MM-DD> | Correct a date-effective row | No; require selected effective-dated identity and explicit EffectiveStartDate | |
| effectiveOf | RangeMode=END_DATE;RangeEndDate=<EffectiveEndDate as YYYY-MM-DD> | End-date a date-effective row | No; require exact identity and explicit EffectiveEndDate | |
| effectiveOf | RangeMode=DELETE_CHANGES;RangeStartDate=<EffectiveStartDate as YYYY-MM-DD> | Delete changes for a date-effective row | No; require selected effective-dated identity, explicit EffectiveStartDate, and explicit DELETE_CHANGES scope | |
| effectiveOf | RangeMode=ZAP | ZAP a date-effective row | No; require exact identity, explicit destructive intent, and immutable Data Loader approval | |

Treat `4712/12/31` as the end-of-time calendar date. Serialize the defaulted
`EffectiveEndDate` in the current section's required DAT date format, for
example `4712-12-31` where ISO `YYYY-MM-DD` is required. Do not add the field
to a section that does not expose it. An End date operation requires an
explicit `EffectiveEndDate` and never receives the end-of-time default;
Delete changes and ZAP do not receive it either.

Verify the final immutable DAT contains the derived effectiveOf for every
included date-effective row. Do not add effectiveOf to a section for which the
current sample does not expose it, and do not copy an UPDATE or CORRECTION
RangeMode from a parent row onto a newly created child row.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_BAL.DERIVE_EFFECTIVE_OF | step | 25 | apply_default | derived->BEN_BAL.ENFORCE_DESIGN;invalid->BEN_BAL.HANDLE_ISSUE | BEN_BAL.LOOKUP_CURRENCY | stop | Default an omitted supported Create, Update, or Correction EffectiveEndDate to 4712/12/31; derive and verify YYYY-MM-DD effectiveOf per supported row and omit it from unsupported sections |

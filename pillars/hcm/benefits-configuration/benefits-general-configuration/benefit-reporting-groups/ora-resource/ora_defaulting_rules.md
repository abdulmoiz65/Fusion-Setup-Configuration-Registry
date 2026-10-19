# Benefit Reporting Groups Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Optional reference fields | No default | Any of the nine requested reference fields is absent | No | |
| Child collections | Preserve absent as absent; do not synthesize empty or default child rows | A child collection is absent | No | |
| Lookup comparison | Exact equality | A named reference field is supplied | No | |
| reportingGroupForProgramsOrPlans.CompensationObjectType | PLN | PlanName is supplied and ProgramName is absent in the same child row | No; reject a conflicting supplied value | |
| reportingGroupForProgramsOrPlans.CompensationObjectType | PGM | ProgramName is supplied and PlanName is absent in the same child row | No; reject a conflicting supplied value | |
| Date-effective child EffectiveEndDate | 4712/12/31 | A create, update, or correction row under regulations, regulatoryBodies, regulatoryPurposes, or reportingGroupForProgramsOrPlans omits EffectiveEndDate | Yes; preserve a supplied value | |
| HDL operation and parent keys | No default until current selected-environment metadata confirms an operation-specific contract | Artifact preparation | No | |

## Date-Effective Defaults

Apply these derivations independently to each supplied `regulations`, `regulatoryBodies`, `regulatoryBodies.regulatoryPurposes`, and `reportingGroupForProgramsOrPlans` row only when current metadata confirms that its section is date-effective, exposes `effectiveOf`, and supports the requested operation. Derive `effectiveOf` from that row's operation and date; never copy a date from a parent or sibling. Omit `effectiveOf` entirely from any section that does not expose it, including `translations` unless current metadata explicitly confirms support. Stop if the section contract is missing or ambiguous.

Before inserting a row's `EffectiveStartDate` or `EffectiveEndDate` into
`effectiveOf`, parse the source date using its documented input format and
serialize the calendar date as `YYYY-MM-DD` with zero-padded month and day.
Reject an invalid or ambiguous source date rather than guessing its format.
Every `RangeStartDate` and `RangeEndDate` component in the final `effectiveOf`
must use `YYYY-MM-DD` (for example,
`RangeMode=END_DATE;RangeEndDate=2026-10-05`).

| Requested operation | `effectiveOf` derivation | Required input |
|---|---|---|
| Create | `RangeStartDate=<EffectiveStartDate as YYYY-MM-DD>` | That row's EffectiveStartDate |
| Update | `RangeMode=UPDATE;RangeStartDate=<EffectiveStartDate as YYYY-MM-DD>` | That row's EffectiveStartDate |
| Correction | `RangeMode=CORRECTION;RangeStartDate=<EffectiveStartDate as YYYY-MM-DD>` | That row's exact existing slice start date |
| End date | `RangeMode=END_DATE;RangeEndDate=<EffectiveEndDate as YYYY-MM-DD>` | That row's EffectiveEndDate |
| Delete changes | `RangeMode=DELETE_CHANGES;RangeStartDate=<EffectiveStartDate as YYYY-MM-DD>` | That row's EffectiveStartDate and scope |
| ZAP | `RangeMode=ZAP` | Explicit destructive intent |

`RangeMode` is part of `effectiveOf`; do not emit it as a separate DAT column. An End date operation requires an explicit EffectiveEndDate and never uses the 4712/12/31 default. Do not default an identity, a non-create date, a range, deletion scope, or destructive choice. A lookup result confirms a supplied value; it does not fill a missing one. A 403 does not trigger a fallback default.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_RPTG.APPLY_DEFAULTS | step | 20 | apply_default | applied->BEN_RPTG.DERIVE_EFFECTIVE_OF | BEN_RPTG.VALIDATE_INPUT | stop | Preserve absent fields and child collections; derive CompensationObjectType and default an omitted create, update, or correction EffectiveEndDate to 4712/12/31 |
| BEN_RPTG.DERIVE_EFFECTIVE_OF | step | 23 | apply_default | derived->BEN_RPTG.CHECK_READINESS | BEN_RPTG.APPLY_DEFAULTS | stop | Derive YYYY-MM-DD effectiveOf per supported date-effective child row from its own operation and date; omit it from sections that do not expose it |

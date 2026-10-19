# Benefit Reporting Groups Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Enforce program or plan choice | Require exactly one ProgramName or PlanName per reportingGroupForProgramsOrPlans row and confirm the derived CompensationObjectType. |
| 2 | Preserve effective dates and child scope | Keep every supplied child in its correct parent record, default an omitted create, update, or correction EffectiveEndDate to 4712/12/31, and derive effectiveOf from that row's operation and effective date. |
| 3 | Confirm reference status | Require successful validation of each supplied reference before a live load; a 403 is an unverified result, not a value mismatch. |
| 4 | Confirm execution route | Use only the selected HDL contract and core.data-loader approval workflow for a mutation. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any child collection is supplied | Blocker | | A child row would be omitted, moved to another parent, or flattened incorrectly | Preserve the input tree and confirm its HDL section in current metadata | Yes, before artifact construction |
| reportingGroupForProgramsOrPlans is supplied | Blocker | | The row contains both PlanName and ProgramName, neither is supplied, or CompensationObjectType conflicts with the derived PLN or PGM value | Correct the association to one supplied reference and use the matching derived type | Yes, before artifact construction |
| A date-effective child row is supplied | Blocker | | effectiveOf cannot be derived from that row's operation and required effective date, contains a date component other than valid YYYY-MM-DD, or an End date operation omits EffectiveEndDate | Supply the required date and operation, serialize effectiveOf dates as YYYY-MM-DD, and inspect the final DAT; for create, update, and correction an omitted EffectiveEndDate defaults to 4712/12/31 | Yes, before artifact construction |
| Any included section | Blocker | | Its date-effectivity or effectiveOf availability is unconfirmed, or effectiveOf appears on a section that does not expose it | Confirm the current per-section contract before derivation and omit effectiveOf from unsupported sections | Yes, before artifact construction |
| Any supplied reference is unverified_forbidden | Blocker for load | | A live load would proceed with a reference that was not verified | Resolve access or use another approved authoritative check; retain the field-level 403 result | Yes, after verification |
| Mutation is requested | Blocker | | Current HDL metadata, active Run Book, immutable artifact, or loader approval is missing | Complete the declared loader workflow | Yes, before submission |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_RPTG.ENFORCE_DESIGN | decision | 105 | design_enforcement | compliant->BEN_RPTG.EVALUATE;blocked->BEN_RPTG.HANDLE_ISSUE | BEN_RPTG.LOOKUP_SOURCE_LANGUAGE | stop | Enforce one program or plan per association, derived CompensationObjectType and effectiveOf, and preserved child rows; for live load only, block unresolved references or missing metadata, Run Book, or loader approval; a validation-only 403 continues to results |

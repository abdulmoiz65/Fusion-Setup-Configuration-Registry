# Benefit Regulations Design Enforcement

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
| --- | --- | --- | --- | --- | --- |
| Every request | Blocking |  | The request names an object other than `benefitRegulations` or a substitute route | Use the mapped HDL object and `core.data-loader` | Yes |
| Any mutation | Blocking |  | Current sample validation is absent or the artifact differs from that sample | Rebuild from the current sample | Yes |
| Any date-effective row | Blocking |  | `effectiveOf` is caller-authored, missing, malformed, contains a date component other than valid `YYYY-MM-DD`, or does not match the selected operation | Derive it with the operation mapping and inspect the final DAT | Yes |
| A date-effective Create, Update, or Correction row exposes EffectiveEndDate | Blocking |  | An omitted end date was not emitted as 4712-12-31, a supplied value was overwritten, or the final DAT date is not valid ISO | Apply the end-of-time default only when omitted and preserve valid supplied dates | Yes |
| End date, Delete changes, or ZAP | Blocking |  | The 4712-12-31 EffectiveEndDate default was applied; or an End date operation lacks an explicit end date | Remove the inapplicable default and require the requested end date for End date | Yes |
| Any included section | Blocking |  | Its date-effectivity or effectiveOf availability is unconfirmed, or effectiveOf appears on a section that does not expose it | Confirm the current per-section contract before derivation and omit effectiveOf from unsupported sections | Yes |
| Non-create operation | Blocking |  | Identity, slice date, or operation support is missing or ambiguous | Resolve exactly one supported target row | Yes |
| End date, Delete changes, or ZAP | Blocking |  | Deletion/end-date scope or destructive intent is not explicit | Obtain explicit scope and current approval | Yes |
| Before approval | Blocking |  | The final immutable DAT member was not inspected for each date-effective row | Inspect and re-preflight the exact archive | Yes |
| Every request | Blocking |  | CSV export/import is proposed | Use HDL only | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BEN_REG.ENFORCE_DESIGN | decision | 40 | design_enforcement | compliant->BEN_REG.GATE_EXECUTION;blocked->BEN_REG.HANDLE_ISSUE | BEN_REG.CHECK_READINESS | stop | Enforce object scope, current-sample contract, date-effective derivation, immutable artifact inspection, and destructive-operation controls |

# Benefit Balances Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Scope | Restrict the request to the Benefit Balances task and benefitBalances HDL business object. |
| 2 | Live schema | Obtain the current Data Loader sample and validate its DAT structure before any artifact is approved. |
| 3 | Identity and prerequisites | Confirm the exact balance name, legal employer, source identity, and all current-sample-required configuration facts. |
| 3a | Reference values | Record each supplied lookup field's exact-match result; a 403 is unverified_forbidden, not an invalid value. |
| 4 | Date-effective operation | Derive effectiveOf independently for every included date-effective row from its exact operation and explicit required input. |
| 5 | Mutation gate | Require a reviewed immutable artifact and current Data Loader approval; treat Delete as destructive. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Blocking | | The request names another object or substitute route | Use benefitBalances through HDL only | Yes |
| Create or merge, Update, or Delete | Blocking | | The artifact has not passed current-schema core.data-loader validation | Generate a current sample and validate the immutable DAT | Yes |
| Create or merge, Update, or Delete | Blocking | | A required source identity or prerequisite is missing, ambiguous, or inconsistent with the sample | Correct authoritative source data; do not infer an identity or field value | Yes |
| A supplied lookup field has zero or multiple distinct exact matches | Blocking | Its declared REST LOV | The supplied value is invalid or ambiguous | Correct the value or resolve its identity; preserve the original input until reviewed | Yes |
| A supplied lookup field is unverified_forbidden | Load readiness blocker only; field validation continues | Its declared REST LOV | The value has not been authoritatively verified after a 403 | Resolve access or use another workflow-approved authoritative check before live load | Yes |
| Update or Delete | Blocking | | Current schema does not support the requested action or its required identity values are missing | Use a documented supported action or correct the source data | Yes |
| A date-effective benefitBalances section is included | Blocking | | effectiveOf is caller-authored, omitted, differs from the exact row-operation mapping, or contains a date component other than valid YYYY-MM-DD | Derive it from ora_defaulting_rules.md, format source dates as YYYY-MM-DD, and inspect the final immutable DAT; do not use inferred or sample values | Yes |
| A date-effective Create, Update, or Correction row exposes EffectiveEndDate | Blocking | | An omitted end date was not defaulted to 4712/12/31, a supplied value was overwritten, or the emitted date violates the section's DAT format | Apply the end-of-time default only when omitted, preserve valid supplied dates, and inspect the final DAT | Yes |
| End date, Delete changes, or ZAP | Blocking | | The 4712/12/31 EffectiveEndDate default was applied; or an End date operation lacks an explicit end date | Remove the inapplicable default and require the requested end date for End date | Yes |
| Any included section | Blocking | | Its date-effectivity or effectiveOf availability is unconfirmed, or the DAT includes effectiveOf on a section that does not expose it | Confirm the current per-section contract and omit effectiveOf from unsupported sections before preflight | Yes |
| Delete | Blocking | | The target effect is not explicitly approved | Use the core.data-loader approval workflow for the exact delete artifact | Yes |
| Every request | Blocking | | FSM CSV export/import is proposed | Use the selected HDL route; CSV support is not catalog-supported | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_BAL.ENFORCE_DESIGN | decision | 30 | design_enforcement | compliant->BEN_BAL.GATE_EXECUTION;blocked->BEN_BAL.HANDLE_ISSUE | BEN_BAL.DERIVE_EFFECTIVE_OF | stop | Enforce object scope, current schema, identities, prerequisites, and mutation approval |

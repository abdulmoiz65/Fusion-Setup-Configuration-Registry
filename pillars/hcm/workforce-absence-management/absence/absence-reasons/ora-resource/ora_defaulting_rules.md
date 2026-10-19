# Absence Reasons Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Search as-of date | Current system date in YYYY-MM-DD format | An AC1 read request omits its search date; this is not EffectiveStartDate for a mutation | No |  |
| Search status | Active | An AC1 read request omits status; an explicit all-status request omits the filter instead | No | resolve_absence_reason_status |
| Search legislation | No legislation restriction | An AC1 read request omits legislation; never apply the create-only US default | No |  |
| LegislationCode | US | A create request omits LegislationCode and a legislation display name was not supplied | No | resolve_absence_reason_legislation |
| Status | Active | A create request omits Status and a status display meaning was not supplied | No | resolve_absence_reason_status |
| EffectiveStartDate | Current date in YYYY-MM-DD format | A create request omits EffectiveStartDate | No |  |
| EffectiveEndDate | Fusion server default 4712-12-31 | An ordinary create request omits EffectiveEndDate | No; omit the field and let Fusion default it |  |
| effectiveOf | `RangeStartDate=<EffectiveStartDate>` | A create request has a resolved EffectiveStartDate | No; derive it from the resolved operation and date | normalize_absence_reason_effective_of |
| ManagementTypeCd | Fusion server default UD | An ordinary create request omits ManagementTypeCd | No; omit the field and let Fusion default it |  |
| Language | Derived by Fusion from the authenticated login context | Every create request | Not applicable; omit Language from create input |  |

LegislationCode defaults to US and Status defaults to Active only when the user omits the corresponding value. Both defaults must still resolve through their documented lookup before Data Loader preparation. Language is not a task input: Fusion derives it from the authenticated login context, so the create workflow neither requests nor validates it.

## Date-Effective Operation Mapping

Derive `effectiveOf` for the parent and every included flexfield row. Do not ask
the caller to supply a free-form value, and do not default the effective date,
range span, deletion scope, or ZAP decision for a non-create operation.

| Requested operation | RestAction | effectiveOf | Required input |
|---|---|---|---|
| Create | POST | `RangeStartDate=<EffectiveStartDate>` | EffectiveStartDate, defaulted only when omitted |
| Update | PATCH | `RangeMode=UPDATE;RangeStartDate=<EffectiveStartDate>` | Explicit EffectiveStartDate |
| Correction | PATCH | `RangeMode=CORRECTION;RangeStartDate=<EffectiveStartDate>` | Explicit EffectiveStartDate |
| End date | PATCH | `RangeMode=END_DATE;RangeEndDate=<EffectiveEndDate>` | Explicit EffectiveEndDate |
| Delete changes | DELETE | `RangeMode=DELETE_CHANGES;RangeStartDate=<EffectiveStartDate>` | Explicit EffectiveStartDate; an optional range end or span requires explicit scope validation |
| ZAP | DELETE | `RangeMode=ZAP` | Explicit destructive intent and the Data Loader approval that binds it |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AR.APPLY_DEFAULTS | step | 30 | apply_default | applied_or_not_needed->AR.NORMALIZE_EFFECTIVE_OF;unresolved->AR.HANDLE_ISSUE | AR.LOOKUP_REASON | stop | After duplicate checking and before date-effective operation normalization |

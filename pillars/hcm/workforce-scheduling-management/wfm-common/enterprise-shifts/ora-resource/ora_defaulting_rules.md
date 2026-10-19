# Enterprise Shifts Defaulting Rules

## Source Basis

- Enterprise Shifts Rest Describe, Confluence page 21451526148, version 3
- Enterprise Shifts Test Technical Design Document for FSCIR, Confluence page 21452837175, version 4
- Enterprise Shift name, field-value precedence, and default-origin display rules, user-provided, received 19 August 2026

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ActiveFlag | true | Creating a shift and the caller omits ActiveFlag | No; preserve an explicit user-provided value |  |
| ShiftName | Population or Purpose [Nonregular Shift Type] Shift Start-End Unpaid-Break-Duration | Creating a shift without an explicit Shift Name when start time, end time, and unpaid-break duration are available from supplied values, applicable current-conversation or selected-configuration values, and configured defaults; retain both Population and Purpose in supplied order when both are available, and include Shift Type only when the supplied type is not a regular working shift | No; preserve an explicit user-provided Shift Name. When construction is not possible, ask for Shift Name directly; do not request missing naming inputs |  |

Do not default StartTime, WorkDurationMinutes, BreakDurationMinutes,
ShiftCategory, EndTime, time offsets, or EndPlusDays. A derived ShiftName must
preserve the user-supplied business wording and wall-clock times; do not add
environment labels, uniqueness suffixes, or other traceability text. ShiftId
and ShiftCode have server-side default expressions that are not exposed by
describe; do not invent or precompute them. The FSCIR source does not locally
declare the create default for ActiveFlag, so retain the live describe default
as the source of authority.

## Defaulting Boundaries

| Situation | What Must Happen |
|---|---|
| Shift Name is evaluated on create | First attempt construction from all valid explicit, current-conversation, selected-configuration, and configured-default inputs. A derived name includes start time, end time, and unpaid-break duration; it includes Population or Purpose when supplied and a Shift Type only when it is nonregular. Preserve an explicit Shift Name instead of the constructed result. When construction cannot occur, ask for Shift Name directly; do not request missing naming inputs. |
| A field value is resolved | Use this precedence: explicit user value; still-applicable current-conversation or selected-configuration value; configured default; then ask only when the field is required and no valid value or default exists. |
| A documented default applies | Apply it without asking the user. In proposed or final Enterprise Shift details, label it Default. Do not label a value Default when the user explicitly supplied it, even when it equals the default. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ES.APPLY_DEFAULTS | step | 20 | apply_default | applied->ES.RESOLVE_REFERENCES;blocked->ES.HANDLE_ERROR | ES.VALIDATE_INPUT | stop | Derive the Shift Name before exact-name lookup, then apply other documented defaults |

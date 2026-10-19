# Manage Receivables System Options Defaulting Rules

## Standard Defaults

These defaults are confirmed entity-creation defaults. Apply them only when the supported FSM import path creates a row and the user/package value is blank; never overwrite an explicit value or assume that a blank CSV field is defaulted before Data Loader preview proves it.

| Field | Default Value | Applies When | Override User Value? | Resolver | Source IDs |
|---|---|---|---|---|---|
| `AccountingMethod` | `ACCRUAL` | New entity row and field omitted | No |  | SRC-CODE-EO |
| `AccrueInterest` | `N` | New entity row and field omitted | No |  | SRC-CODE-EO |
| `UnearnedDiscount` | `N` | New entity row and field omitted | No |  | SRC-CODE-EO |

## No-Default Boundaries

| Situation | Required Behavior | Source IDs |
|---|---|---|
| Any of the other package fields lacks confirmed default evidence | Preserve blank/TBD and require review; do not infer from the current-data export | SRC-FSM-PACKAGE |
| Lookup-dependent field is blank | Do not choose the first or common reference value | SRC-CODE-AM-IMPL |
| Existing setup row | Preserve its current value unless the requested change is explicit and included in the immutable preview | SRC-FSM-PACKAGE; SRC-HELP-RSO-26C |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RSO.APPLY_DEFAULTS | step | 40 | apply_default | applied->RSO.ENFORCE_DESIGN;not_applicable->RSO.ENFORCE_DESIGN;blocked->RSO.HANDLE_ERROR | RSO.CHECK_DEPENDENCIES | stop | After dependencies are ready |

<!-- E2E-DISCOVERY:RSO-E2E-DISC-004 -->
## FSM create-view defaults

For create only, serialize the `SystemParameterCreateUIVO` defaults that the FSM `SystemParameterVO` import path does not apply: `CerSplitAmount=0`, `CerDsoDays=0`, `PostingDaysPerCycle=0`, `AutoSiteNumbering=N`, `GenerateCustomerNumber=N`, and `PopulateGlSegmentsFlag=N`. Never overwrite an explicit user value. Evidence: SRC-CODE-CREATE-UI-VO and SRC-E2E-RSO-CREATE-COMPLETE-20260904.

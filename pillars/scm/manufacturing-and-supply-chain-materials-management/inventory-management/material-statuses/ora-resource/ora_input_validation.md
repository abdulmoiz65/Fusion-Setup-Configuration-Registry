# Material Statuses Input Validation

## Source Evidence

| Source | Used For |
|---|---|
| Live Data Loader metadata for inventoryMaterialStatuses | Confirms the eight parent attributes and child IsTransactionAllowed accept canonical values 1 or 2 |
| Redwood Material Statuses manage-page form and submit action chain | Confirms parent checkbox controls are submitted as 1 or 2 |
| Redwood Material Statuses transaction drawer action chain | Confirms child IsTransactionAllowed is submitted as 1 for Allowed and 2 for Disallowed |
| User-approved normalization rule | Defines friendly-value normalization before Data Loader handoff |

## Scope Boundary

| Boundary | What Happens |
|---|---|
| Local validation ownership | Normalize only the documented friendly 1/2 values and reject unsupported or conflicting supplied values |
| Backend-owned validation | Data Loader and Fusion own required fields, lengths, uniqueness, keys, defaults, and all remaining domains |
| REST execution | Do not create direct REST write guidance; core.data-loader owns execution |

## Value Normalization

| Field | Friendly Values for 1 | Friendly Values for 2 | Canonical Output | Applies When | Invalid or Conflicting Input |
|---|---|---|---|---|---|
| StatusEnabled | Yes, Y, 1 | No, N, 2 | 1 or 2 | Value is supplied | Stop and request one allowed value |
| ReservableType | Yes, Y, 1 | No, N, 2 | 1 or 2 | Value is supplied | Stop and request one allowed value |
| IncludeInATP | Yes, Y, 1 | No, N, 2 | 1 or 2 | Value is supplied | Stop and request one allowed value |
| Nettable | Yes, Y, 1 | No, N, 2 | 1 or 2 | Value is supplied | Stop and request one allowed value |
| SubinventoryControl | Yes, Y, 1 | No, N, 2 | 1 or 2 | Value is supplied | Stop and request one allowed value |
| LocatorControl | Yes, Y, 1 | No, N, 2 | 1 or 2 | Value is supplied | Stop and request one allowed value |
| LotControl | Yes, Y, 1 | No, N, 2 | 1 or 2 | Value is supplied | Stop and request one allowed value |
| SerialControl | Yes, Y, 1 | No, N, 2 | 1 or 2 | Value is supplied | Stop and request one allowed value |
| statusTransactionControls.IsTransactionAllowed | Allowed, Yes, Y, 1 | Disallowed, No, N, 2 | 1 or 2 | Child value is supplied | Stop and request one allowed value |

## Normalization Rules

| Rule | What Happens |
|---|---|
| Match behavior | Trim outer whitespace and match supplied friendly values case-insensitively and exactly |
| Blank value | Preserve the blank value; do not locally apply a default |
| Single recognized value | Replace it with the documented canonical string 1 or 2 before Data Loader handoff |
| Multiple or conflicting values | Stop; do not select a value automatically |
| Unsupported value | Stop; do not fuzzy-match, infer, or coerce an undocumented value |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MSTAT.VALIDATE_INPUT | step | 10 | validate_input | valid->MSTAT.CHECK_READINESS;invalid->MSTAT.HANDLE_ERROR | none | stop | Before Data Loader preparation, normalize all supplied documented 1/2 fields |

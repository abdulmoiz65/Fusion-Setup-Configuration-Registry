# Remit-to Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| AR_REMIT_TO_ADDRESS.Status | A | New active receipt-from criterion and user omitted status; explicitly serialize because service VO does not use UI create row implementation | No | |

## Default Ownership Boundaries

| Value | Ownership and behavior | Source |
|---|---|---|
| Destination country | No unconditional package default. UI may use applicable Receivables System Options Default Country; establish applicability and disclose before use. FSM hook copies supplied TerritoryCode | SRC-REMIT-HELP-26C; SRC-REMIT-AM-IMPL |
| SetCode | No COMMON default. User-selected existing exact set; unknown set yields import error | SRC-REMIT-AM-IMPL |
| OrigSystemReference | Service derives missing value from newly allocated LocationId only when creating shared location. Do not synthesize a customer ID or require an invented value | SRC-REMIT-AM-IMPL |
| CreatedByModule | Internal service assignment, not a CSV input; UI TCA_FORM_WRAPPER and import module differ | SRC-REMIT-AM-IMPL; SRC-REMIT-UI-CREATE-BINDING |
| Location StatusFlag | Commented assignment is not executable default; never copy it into criteria defaults | SRC-REMIT-AM-IMPL |
| Audit history | Service-owned history; retain baseline evidence, do not serialize historical user inputs as changes | SRC-REMIT-LOCATION-VO; SRC-REMIT-CRITERIA-VO |
| Blank state/postal restrictions | Country-only criteria have whole-country business meaning. No inferred narrowing or destination-country copying | SRC-REMIT-HELP-26C |

Only the Standard Defaults table defines a literal package default. Remaining
entries describe ownership boundaries, not values to insert automatically.
Record each applied default in the normalized preview without overwriting an
explicit business value; an invalid explicit value needs clarification.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RMT_DEFAULTS | step | 40 | apply_default | done->RMT_DESIGN;issues->RETURN_ISSUES | RMT_DEPENDENCIES | stop | Omitted source-backed defaultable fields |

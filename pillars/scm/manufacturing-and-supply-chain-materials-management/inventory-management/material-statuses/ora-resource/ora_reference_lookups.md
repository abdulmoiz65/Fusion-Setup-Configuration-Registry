# Material Statuses Reference Lookups

## Source Evidence

| Source | Used For |
|---|---|
| Redwood Material Statuses flow | The Transaction Types drawer uses invStatusEnabledTransactionTypesLOV for child-row UI selection |
| User decision | Do not add a Transaction Types LOV resolver to this task skill |

## Lookup Decision

| Candidate | Decision | Reason |
|---|---|---|
| Transaction Types | Not selected | The user did not require display-value-to-ID resolution for statusTransactionControls |

No local or live lookup resolver is defined for this task. Data Loader validates supplied canonical keys and values.

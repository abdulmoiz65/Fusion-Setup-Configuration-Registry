# Balance Exceptions defaulting rules

Defaults are provisional until the selected target pod confirms the comparison-type codes and FSM contract. A supplied explicit value is never overwritten.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ComparisonValue | 0 | Current Month, Current Period, Current Quarter, or Current Year has been confirmed by target-pod evidence; the HAR directly shows 0 only for MC and PC | No | resolve_comparison_type_code |
| ComparisonValue | 1 | Previous Period or Previous Month has been confirmed by target-pod evidence; this value was not exercised in the HAR | No | resolve_comparison_type_code |
| ComparisonValue | No default | Average in Months or another comparison type requiring an entered value | No | resolve_comparison_type_code |
| VarianceValue | No default | Amount or percent variance is selected | No |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BE.APPLY_DEFAULTS | step | 40 | apply_default | applied->BE.ENFORCE_DESIGN;skipped->BE.ENFORCE_DESIGN | BE.RESOLVE_REFERENCES | stop | Reference resolution completed |

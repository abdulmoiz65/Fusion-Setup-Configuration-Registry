# Defaulting Rules

Apply only the documented defaults. A caller-supplied value takes precedence unless a design rule explicitly prohibits the combination.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| CreditLineFlag | false | Create and the field is absent | No | |
| ProductTypeCode | GOODS | Create and the field is absent | No | |
| PurchaseBasisCode | GOODS | Create and the field is absent | No | |
| ProductTypeCode | Same value as PurchaseBasisCode | Create with PurchaseBasisCode supplied and ProductTypeCode absent | No | |
| DefaultMatchApprovalLevelCode | 2-Way | Create with CreditLineFlag true and the field is absent | No | |
| DefaultInvoiceMatchOptionCode | P | Create with CreditLineFlag true and the field is absent | No | |
| DefaultReceiptCloseTolerancePercent | 100 | Create with CreditLineFlag true and the field is absent | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PLT.APPLY_DEFAULTS | step | 30 | apply_default | defaulted->PLT.ENFORCE_DESIGN;not_applicable->PLT.ENFORCE_DESIGN | PLT.VALIDATE_INPUT | stop | Every validated create or update request |

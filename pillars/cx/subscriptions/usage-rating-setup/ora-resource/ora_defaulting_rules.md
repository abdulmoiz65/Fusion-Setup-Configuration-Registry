# Quantity Allowance Defaulting Rules

## Source Basis

Oracle feature overview: `2978639.1-BALANCEMANAG-Allowance_Management_-_Quantity-1.pdf` (Manage Allowances for Consumption-based Subscription Models, release 23B).

## Standard Defaults

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_BALANCE_PROFILES | Manage Balance Profiles | Billing-related attributes | Subscription profile billing attributes | Billing-related attributes are not entered on the balance profile | No |  |

## Defaulting Guidance

| Task Code | Task Name | Situation | What Happens |
|---|---|---|---|
| CUSTOM_MANAGE_BALANCE_PROFILES | Manage Balance Profiles | Billing-related attributes are omitted | The source states that they default from the subscription profile. Align Billing From remains mandatory and is not defaulted by this guidance. |

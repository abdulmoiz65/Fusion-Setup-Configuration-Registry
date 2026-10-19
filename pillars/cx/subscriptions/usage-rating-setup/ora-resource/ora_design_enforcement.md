# Quantity Allowance Design Enforcement

## Source Basis

Oracle feature overview: `2978639.1-BALANCEMANAG-Allowance_Management_-_Quantity-1.pdf` (Manage Allowances for Consumption-based Subscription Models, release 23B). This resource records source-backed implementation practices only; it does not authorize a Fusion write.

## Enforcement Order

| Task Code | Task Name | Sequence | Step | What Must Happen |
|---|---|---|---|---|
| CUSTOM_MANAGE_BALANCE_CODES | Manage Balance Codes | 1 | Synchronize metadata | Run the Sync Balance Object Metadata ESS job before balance-management setup. |
| CUSTOM_MANAGE_BALANCE_CODES | Manage Balance Codes | 2 | Define the balance | Choose the balance type and its matching UOM or currency, then define applicable charges and conditions. |
| CUSTOM_MANAGE_BALANCE_CODES | Manage Balance Codes | 3 | Set consumption order | Configure the consumption rule so rollover balances are used in the intended order. |
| CUSTOM_MANAGE_BALANCE_PROFILES | Manage Balance Profiles | 1 | Define pooling | Select grouping criteria that match the intended shared-balance population. |
| CUSTOM_MANAGE_BALANCE_PROFILES | Manage Balance Profiles | 2 | Align billing | Set Align Billing From before pooling subscriptions with different start dates. |
| CUSTOM_MANAGE_BALANCE_PROFILES | Manage Balance Profiles | 3 | Map charges and balances | Include the allowance-granting recurring charge, the measured usage charge, and the corresponding balance code. |

## Design Rules

| Task Code | Task Name | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_BALANCE_CODES | Manage Balance Codes | Before any balance-management setup | Error |  | Sync Balance Object Metadata has not completed | Run the ESS job before configuring balance codes, profiles, or entitlement plans | Yes |
| CUSTOM_MANAGE_BALANCE_CODES | Manage Balance Codes | Defining a quantity-based allowance | Error |  | Quantity balance has no UOM or the selected charge does not measure the intended usage | Use a quantity-based balance code with the business UOM and associate the usage charge being measured | Yes |
| CUSTOM_MANAGE_BALANCE_CODES | Manage Balance Codes | Defining quantity rounding | Warning |  | Rounding factor or direction does not reflect the allowance policy | Use Up, Down, or Standard rounding deliberately and document the factor | Yes |
| CUSTOM_MANAGE_BALANCE_CODES | Manage Balance Codes | Qualifying balances with a custom usage-event attribute | Error |  | The condition value cannot be supplied when the subscription is created | Add the custom attribute to Subscription Usage Event Object and ensure the required value is passed during subscription creation | Yes |
| CUSTOM_MANAGE_BALANCE_CODES | Manage Balance Codes | Rollover balance should be consumed before the current-period allocation | Error |  | Consumption order does not use Rollover End Date ascending | Configure the consumption rule as Rollover End Date with ascending sort order | Yes |
| CUSTOM_MANAGE_BALANCE_PROFILES | Manage Balance Profiles | Defining pooled allowances or usage | Error |  | Group criteria do not identify the intended pooling population | Use Subscription, Subscription Product, or documented custom attributes that match the pooling policy | Yes |
| CUSTOM_MANAGE_BALANCE_PROFILES | Manage Balance Profiles | Grouping subscriptions with different start dates | Error |  | Align Billing From is missing | Set Align Billing From so billing periods are aligned before allowances are mapped to the shared balance register | Yes |
| CUSTOM_MANAGE_BALANCE_PROFILES | Manage Balance Profiles | Adding charges to a profile | Error |  | Allowance-granting recurring charge, measured usage charge, or its balance-code mapping is missing | Enable Allowance Grant for the contributing recurring charge, add the usage charge, and map its balance code | Yes |
| CUSTOM_MANAGE_BALANCE_PROFILES | Manage Balance Profiles | One profile tracks multiple balances | Warning |  | Multiple balance codes do not reflect an intentional business design | Keep multiple balance codes in one profile only when the shared grouping and charge design support that business need | Yes |

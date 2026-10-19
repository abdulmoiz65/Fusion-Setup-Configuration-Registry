# Costing of Payrolls Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| payroll_name_search | A single percent sign, meaning no name restriction. | Search with no payroll name filter. | No; preserve supplied search text. | |
| costing_filter | all | Search with no costing-state filter. | No; preserve the requested state using its documented wire mapping. | |
| effective_date | Current calendar date in the active workflow timezone, formatted YYYY-MM-DD. Resolve it once before the first lookup and show the applied date in the result. | Search with no effective date; developer-confirmed default. | No; preserve an explicit valid date and reuse the same resolved date on every page. | |
| SourceType | PAY | Create/Update parent and account rows; End Date parent row; Zap parent and account DELETE rows. | No; reject conflicting input. | |
| Create EffectiveEndDate | 4712/12/31 | Create CostAllocationV3 parent only. | No; a different requested business end date belongs to End Date. | |
| Create account EffectiveDate | Parent EffectiveStartDate, rendered YYYY/MM/DD. | Every Create CostAllocationAccountV3 row. | No; reject a conflicting supplied date. | |
| SubTypeSequence | Consecutive positive integers starting at 1. | Create and effective-dated Update CostAllocationAccountV3 account collections. | No; ignore a user-supplied value, assign 1 to the first supplied account row, and increase by 1 for each following row. | |
| Proportion | User percentage divided by 100, as a decimal fraction from 0 through 1. | Create and effective-dated Update account rows. | No; convert once with decimal arithmetic. | |
| Update EffectiveEndDate | Omitted from the parent METADATA and MERGE. | Verified latest open-ended interval Update only. | No; a business end date belongs to End Date. | |
| Update future changes | SET PURGE_FUTURE_CHANGES N at the beginning of both DAT members. | Every supported effective-dated Update. | No | |
| Update account EffectiveDate | Requested new parent EffectiveStartDate, rendered YYYY/MM/DD. | Every Update account row, including unchanged accounts carried forward. | No | |
| ReplaceLastEffectiveEndDate | Y | End Date of the selected latest parent; render once in METADATA and MERGE. | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COP.SEARCH.APPLY_DEFAULTS | decision | 3 | apply_default | applied->COP.SEARCH.RESOLVE_LDG;skipped->COP.SEARCH.RESOLVE_LDG;invalid->COP.HDL.HANDLE_ERROR | COP.SEARCH.VALIDATE_INPUT | stop | Search: apply only Search defaults and normalize costing-state labels using the lookup wire mapping; do not apply HDL account defaults. |
| COP.HDL.APPLY_DEFAULTS | decision | 19 | apply_default | applied->COP.HDL.CHECK_DEPENDENCIES;skipped->COP.HDL.CHECK_DEPENDENCIES;invalid->COP.HDL.HANDLE_ERROR | COP.HDL.VALIDATE_INPUT | stop | Apply operation-scoped defaults only after that branch has resolved identity, current state, KFF and segment validation. Create requires its four lookup nodes; Update requires its three lookup nodes. Never apply the Create end-date default to Update. |
| COP.END_DATE.APPLY_DEFAULTS | decision | 23 | apply_default | applied->COP.END_DATE.VALIDATE_SOURCE;invalid->COP.HDL.HANDLE_ERROR | COP.END_DATE.CHECK_STATE | stop | Set only PAY, canonical keys and ReplaceLastEffectiveEndDate=Y for the parent-only End Date contract; preserve both resolved dates. |
| COP.ZAP.APPLY_DEFAULTS | decision | 36 | apply_default | applied->COP.ZAP.VALIDATE_SOURCE;invalid->COP.HDL.HANDLE_ERROR | COP.ZAP.CHECK_DEPENDENCIES | stop | Apply only SourceType PAY and resolved canonical keys. Preserve earliest history start, latest history end and all bound physical identities. No open-end default, percentage conversion, account sequence or SET instruction applies. |

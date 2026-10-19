# Department Costing Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Search costing filter | all | A Department search does not request with_costing or without_costing. | Yes, only to documented filter values. | search_department_costing |
| Search text | percent wildcard | A Department list has no literal typed search string. | Yes, with a supplied literal search string. | search_department_costing |
| Active control | Omitted | The user does not explicitly request an Active-only list. | Yes, only when Active is explicitly requested. | search_department_costing |
| SourceType | ORG | Every Department HDL row. | No | |
| Create EffectiveEndDate | 4712/12/31 | CostAllocationV3 Create row. | No | |
| Update future changes | SET PURGE_FUTURE_CHANGES N at the beginning of both Update DAT members. | Every effective-dated Update. | No | |
| ReplaceLastEffectiveEndDate | Y | End Date of the selected last CostAllocationV3 parent; render as a METADATA attribute with its matching MERGE value. | No | |
| SubTypeSequence | Consecutive positive integers starting at 1. | Create and effective-dated Update CostAllocationAccountV3 account collections. | No; ignore a user-supplied value, assign 1 to the first supplied account row, and increase by 1 for each following row. | |
| Proportion | User percentage divided by 100, as a decimal fraction from 0 through 1. | Create and effective-dated Update account rows. | No; convert once with decimal arithmetic. | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DCP.APPLY_DEFAULTS | decision | 40 | apply_default | applied->DCP.ENFORCE_DESIGN;skipped->DCP.ENFORCE_DESIGN;invalid->DCP.HANDLE_ERROR | DCP.CHECK_DEPENDENCIES | stop | Apply documented HDL defaults before package preview. |

# Location Costing Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| SourceType | LOC | Every Location Costing parent or child action. | No; reject a conflicting value. | |
| SourceSubType | COST | Create or Update account MERGE when the value is absent. | No; reject a conflicting Create or Update value. Correct and Zap preserve the returned value. | |
| Parent EffectiveEndDate | Blank | Create or ordinary effective Update. | Yes, only when the active governed workflow validates an explicit value. | |
| SubTypeSequence | Consecutive positive integers beginning at 1 | Create or effective-dated Update account collection. | No; assign from supplied row order and ignore a supplied sequence for these two operations. | |
| Future-change directive | SET PURGE_FUTURE_CHANGES N | Update parent member. | No | |
| ReplaceLastEffectiveEndDate | Y | End Date of the exact latest effective parent. | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LCP.APPLY_DEFAULTS | decision | 710 | apply_default | applied->LCP.ENFORCE_DESIGN;skipped->LCP.ENFORCE_DESIGN;invalid->LCP.HANDLE_ERROR | LCP.CHECK_DEPENDENCIES | stop | Apply only the defaults valid for the selected mutation; never default LocationSetCode, Correct sequence, or Zap child data. |

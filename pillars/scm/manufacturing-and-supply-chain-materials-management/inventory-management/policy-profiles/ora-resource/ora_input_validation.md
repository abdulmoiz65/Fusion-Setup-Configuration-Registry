# Policy Profiles Input Validation

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Policy Type mapping | Accept PolicyType only when it is exact static code 1 or 2. Preserve the supplied code; code 1 maps to the Min-Max Planning UI option and code 2 maps to the PAR UI option. | PolicyType is supplied. | resolve_policy_type_ui_mapping |
| Max Qty Calculation Method | Accept a trimmed, case-insensitive exact LookupCode or Meaning and resolve the canonical backend value to LookupCode. | MaxCalcMethod is supplied. | resolve_max_qty_calculation_method |
| Safety Stock Calculation Method | Accept a trimmed, case-insensitive exact LookupCode or Meaning and resolve the canonical backend value to LookupCode. The Redwood control is read-only; do not default, clear, or conditionally set SsCalcMethod. | SsCalcMethod is supplied. | resolve_safety_stock_calculation_method |
| Selected mapping or lookup request | Select the no-selected-value path when PolicyType, MaxCalcMethod, and SsCalcMethod are all absent. Otherwise process each supplied field in sequence and explicitly skip each omitted field. | Before evaluating the selected task-local behavior. |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PP.SELECT_REQUEST | decision | 2 | validate_input | selected->PP.MAP_POLICY_TYPE;no_selected_value->PP.COMPLETE_NOT_APPLICABLE | PP.CHECK_METADATA | stop | Before evaluating the supplied PolicyType, MaxCalcMethod, and SsCalcMethod values |
| PP.MAP_POLICY_TYPE | decision | 3 | validate_input | mapped_or_not_supplied->PP.LOOKUP_MAX_QTY_METHOD;invalid->PP.STOP_LOOKUP | PP.SELECT_REQUEST | stop | A selected task-local mapping or lookup request is processed |

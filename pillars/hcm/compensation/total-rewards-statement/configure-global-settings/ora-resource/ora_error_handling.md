# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| compensationGlobalSettings describe metadata cannot be read | Stop before validation, preview, or mutation. Do not infer a field contract. |
| A supplied field is outside the five allowed fields | Stop and identify the disallowed field. |
| A supplied value does not meet the current type, format, precision, length, or LOV contract | Stop and identify the field that must be corrected. |
| StockCurrencyCode does not resolve to exactly one currency | Stop and request a valid currency code. |
| currenciesLOV metadata does not declare the required finder, or its response does not contain the requested exact CurrencyCode | Stop as a query-contract failure; do not claim the currency is missing or retry with inferred finder syntax. |
| A read-only Fusion call fails outside authentication handling | Do not retry automatically; report the failure class and safe next action. |
| A user asks to change Fusion data | Route only through the task's separate approved execution workflow after validation completes. |
| A create, update, or import reaches the handoff gate | Invoke core.data-loader with the validated task context and immutable source; Core owns preview, approval, and submission. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| REST metadata validation gap | compensationGlobalSettings metadata is unavailable or incomplete | Restore readable metadata; do not infer fields or defaults. |
| Allowed-field scope gap | A field other than the five permitted fields is supplied | Remove the field or use the owning task. |
| Input validation gap | A supplied allowed value violates its current field contract | Correct the supplied value and validate again. |
| Currency lookup validation gap | A supplied StockCurrencyCode has no exact currency match | Provide a valid currency code. |
| Query-contract failure | currenciesLOV finder metadata is unavailable or returned records do not match the requested CurrencyCode | Restore a verified finder contract; do not infer query syntax or report a false missing prerequisite. |
| Fusion API failure | A read-only metadata or currency lookup request fails | Stop and report the failure without exposing credentials. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Current metadata is unavailable | Do not infer field names, defaults, payloads, or write behavior. |
| A supplied field is outside the allowed scope | Do not validate, preview, or submit that field through this task. |
| A read-only Fusion request fails outside 401 or 403 handling | Do not retry automatically. |
| A mutation is requested | Do not mutate through these resources; require the separate approved execution workflow. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCSGS.ROUTE | decision | 50 | execution_gate | validated_only->TCSGS.DONE_VALIDATED;create_or_update_or_import_ready->TCSGS.LOADER_READY;mutation_blocked->TCSGS.HANDLE_ISSUE | TCSGS.CHECK_DEPENDENCIES | stop | Select validation completion or the Core Data Loader handoff |
| TCSGS.HANDLE_ISSUE | step | 60 | error_handler | handled->TCSGS.RETURN_ISSUES | none | stop | Any metadata, scope, input, currency, or Fusion API issue |
| TCSGS.RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | A blocking issue was classified and disclosed |
| TCSGS.DONE_VALIDATED | terminal | 80 | terminal | none | TCSGS.ROUTE | continue | Allowed Configure Global Settings values are validated; no mutation was requested |
| TCSGS.LOADER_READY | terminal | 90 | terminal | none | TCSGS.ROUTE | continue | Mutation rules passed; invoke core.data-loader and follow it through immutable ZIP preview |

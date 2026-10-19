# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| read_compensation_global_settings_metadata | Before validating any supplied field | Business object: compensationGlobalSettings | /hcmRestApi/resources/latest/compensationGlobalSettings/describe | Attribute name, type, format, updatable, mandatory, precision, max length, default value, LOV, and description | Require readable metadata for MaximumStatementPeriods, StockPrice, StockCurrencyCode, WatchlistStatementFlag, and WatchlistStatementDays | Current allowed-field contract | Stop as a REST metadata validation gap; do not infer fields, defaults, or payload shape |
| describe_stock_currency_lov | Before querying currenciesLOV for StockCurrencyCode | currenciesLOV | /fscmRestApi/resources/11.13.18.05/currenciesLOV/describe | Declared finder names, parameters, return fields, and pagination controls | Require the current describe contract to declare CurrencyCodeFinder and its required parameters before constructing the lookup request. | Validated currency endpoint contract | Stop as a query-contract failure; do not infer finder syntax or parameters. |
| resolve_stock_currency_code | StockCurrencyCode is supplied after describe_stock_currency_lov succeeds | Supplied StockCurrencyCode; CurrenciesLOVVO declared by compensationGlobalSettings metadata | Declared currenciesLOV CurrencyCodeFinder using its describe-confirmed parameter contract | CurrencyCode and Name | Require exactly one currency record whose CurrencyCode exactly equals the supplied value. Returned records with a different code are a query-contract failure, not a missing currency. | StockCurrencyCode: CurrencyCode | Stop and request one valid currency code, or report a query-contract failure when the response is unrelated. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCSGS.READ_METADATA | step | 10 | reference_lookup | metadata_ready->TCSGS.DESCRIBE_STOCK_CURRENCY_LOV;metadata_gap->TCSGS.HANDLE_ISSUE | none | stop | Before validating any Configure Global Settings value |
| TCSGS.DESCRIBE_STOCK_CURRENCY_LOV | step | 15 | reference_lookup | contract_ready->TCSGS.RESOLVE_STOCK_CURRENCY;not_supplied->TCSGS.VALIDATE_INPUT;contract_gap->TCSGS.HANDLE_ISSUE | TCSGS.READ_METADATA | stop | Before querying currenciesLOV for a supplied StockCurrencyCode |
| TCSGS.RESOLVE_STOCK_CURRENCY | step | 20 | reference_lookup | resolved->TCSGS.VALIDATE_INPUT;not_supplied->TCSGS.VALIDATE_INPUT;invalid->TCSGS.HANDLE_ISSUE | TCSGS.DESCRIBE_STOCK_CURRENCY_LOV | stop | Before validating a supplied StockCurrencyCode |

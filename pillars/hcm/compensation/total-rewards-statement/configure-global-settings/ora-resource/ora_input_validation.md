# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Current Compensation Global Settings metadata | One or more supplied fields returned by the current compensationGlobalSettings describe metadata | Stop | Read current REST metadata before accepting values | Every create, update, or validation request | read_compensation_global_settings_metadata |
| Allowed field scope | MaximumStatementPeriods, StockPrice, StockCurrencyCode, WatchlistStatementFlag, WatchlistStatementDays | Stop | Remove or correct every field outside this task's allowed scope | Every request containing configuration values |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Exact field scope | Accept only MaximumStatementPeriods, StockPrice, StockCurrencyCode, WatchlistStatementFlag, and WatchlistStatementDays | Every supplied value |  |
| MaximumStatementPeriods | Accept an updatable BigInt-compatible value of up to 18 digits that starts at 0 or greater | MaximumStatementPeriods is supplied |  |
| StockPrice | Accept an updatable BigDecimal-compatible value | StockPrice is supplied |  |
| StockCurrencyCode | Accept an updatable string of up to 30 characters that resolves through CurrenciesLOVVO | StockCurrencyCode is supplied | resolve_stock_currency_code |
| WatchlistStatementFlag | Accept an updatable Boolean-compatible Yes or No value | WatchlistStatementFlag is supplied |  |
| WatchlistStatementDays | Accept an updatable BigInt-compatible value of up to 18 digits that starts at 0 or greater | WatchlistStatementDays is supplied |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCSGS.VALIDATE_INPUT | step | 30 | validate_input | valid->TCSGS.CHECK_DEPENDENCIES;invalid->TCSGS.HANDLE_ISSUE | TCSGS.READ_METADATA,TCSGS.RESOLVE_STOCK_CURRENCY | stop | After current metadata and any supplied stock currency resolve |

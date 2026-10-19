# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Current Compensation Global Settings metadata | Read the current REST describe metadata. |
| 2 | Stock currency endpoint contract | Describe currenciesLOV and confirm the declared finder contract. |
| 3 | Stock currency | Resolve a supplied StockCurrencyCode through the describe-confirmed currency LOV finder. |
| 4 | Supplied values | Validate every supplied value against the allowed field scope and current field contract. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| compensation_global_settings_metadata | Current compensationGlobalSettings metadata | Yes | Every create, update, or validation request | Lookup | compensationGlobalSettings describe metadata | read_compensation_global_settings_metadata | Establishes the task's live field contract | Wait for current metadata before providing or processing fields | Validated allowed-field contract |
| stock_currency_endpoint_contract | currenciesLOV endpoint contract | Conditional | StockCurrencyCode is supplied | Lookup | currenciesLOV describe metadata | describe_stock_currency_lov | Prevents inferred finder requests against this LOV resource | Wait for the current describe contract before currency validation | Declared finder and parameter contract |
| stock_currency_code | Stock currency code | Conditional | StockCurrencyCode is supplied | Lookup | CurrenciesLOVVO declared by current compensationGlobalSettings metadata | resolve_stock_currency_code | Validates the selected currency for the default stock price | Provide a valid currency code or omit StockCurrencyCode | StockCurrencyCode |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Current metadata is readable and every supplied allowed value validates | Lookup only; continue to the separate approved execution workflow |
| Blocked | Metadata is unavailable, a disallowed field is supplied, or a supplied currency does not resolve | Read-only lookup only; stop before preview or mutation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCSGS.CHECK_DEPENDENCIES | decision | 40 | resolve_dependency | ready->TCSGS.ROUTE;blocked->TCSGS.HANDLE_ISSUE | TCSGS.VALIDATE_INPUT | stop | After supplied values pass input validation |

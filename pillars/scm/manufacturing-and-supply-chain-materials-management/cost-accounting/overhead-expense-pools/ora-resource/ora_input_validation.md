# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Expense pool identity | ExpensePoolCode | Reject the request | Provide a non-empty ExpensePoolCode string | Create | |
| Expense pool delete identity | ExpensePoolCode, with optional SetName and ExpensePoolTypeCode qualifiers | Reject the request | Provide a non-empty ExpensePoolCode; optionally provide supported qualifiers that resolve and agree with one existing target | DELETE | resolve_delete_target |
| Expense pool type selection | ExpensePoolTypeCode as free-text expense-pool type meaning | Reject the request | Provide one value that resolves through resolve_expense_pool_type | Create | resolve_expense_pool_type |
| Reference data set selection | SetName; do not accept SetId or SetCode from the user | Reject the request | Provide a valid SetName that resolves through resolve_reference_set | Create | resolve_reference_set |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A Create request has all required values present and valid | Continue to dependency resolution | If InactiveFlag is supplied, normalize it; then resolve both reference values | |
| A PATCH request omits an unchanged field | Continue | Preserve the field; do not default, resolve, or add it to the change payload | |
| A DELETE request has a non-empty ExpensePoolCode and only supported optional qualifiers | Continue | Do not default mutable attributes; resolve supplied qualifiers and then resolve one existing target | resolve_delete_target |
| A DELETE target is resolved | Continue to standard Data Loader source validation and approval | Preserve the verified target identity and validate the supplied source through core.data-loader | |
| A prepared Data Loader source is proposed | Continue only when every operation-required field and the intent-derived RestAction are populated | Inspect the generated workbook row; for Create require code, resolved type, resolved set, and POST; normalize InactiveFlag to `Y` or `N` only when supplied. For PATCH require code, at least one validated change, and PATCH; for DELETE require verified code and DELETE only | |
| A required Create or DELETE value, or any supplied PATCH value, is null, empty, invalid, unresolved, or ambiguous | Blocked | Return the validation issue; do not construct a payload | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| ExpensePoolCode is a non-empty string | Preserve the supplied value unchanged after basic validation | Create, DELETE, or PATCH when ExpensePoolCode is supplied | |
| ExpensePoolCode is omitted | Preserve the existing value; do not add it to the change payload | PATCH | |
| ExpensePoolCode is omitted | Reject the request | DELETE | |
| ExpensePoolTypeCode is supplied as a non-empty value | Treat the supplied value as an expense-pool type meaning. Resolve one exact normalized Meaning from the fixed lookup-type result and use its returned LookupCode in the payload or only to qualify a DELETE target. | Create, DELETE, or PATCH when ExpensePoolTypeCode is supplied | resolve_expense_pool_type |
| ExpensePoolTypeCode is omitted | Preserve the existing value; do not resolve it or add it to the change payload | PATCH | |
| SetName is supplied as a non-empty value | Search SetName and use the returned SetId in the Create payload, or only to qualify a DELETE target. | Create or DELETE when SetName is supplied | resolve_reference_set |
| SetName is supplied | Reject the request; the set is immutable after Create. | PATCH | |
| SetId or SetCode is supplied by the user | Reject the request; final payload uses only SetId returned by a SetName resolution. | Create, DELETE, or PATCH | resolve_reference_set |
| A DELETE request supplies ExpensePoolName, ExpensePoolDescription, ExpensePoolType, InactiveFlag, or another mutable attribute | Reject the request; DELETE payloads cannot carry mutable attributes. ExpensePoolTypeCode is allowed only as a target qualifier. | DELETE | |
| RestAction is `DELETE` | Accept it as the standard Data Loader operation field when the source is a DELETE; it must not be accompanied by mutable attributes. | DELETE | |
| RestAction is blank or is not `DELETE` | Reject the DELETE request. | DELETE | |
| RestAction matches the requested operation | Require `POST` for Create, `PATCH` for PATCH, and `DELETE` for DELETE in every prepared JSON and generated source row. | Create, PATCH, or DELETE | |
| RestAction is missing, blank, or mismatched | Reject the source before preview; do not infer a different user intent from the source action. | Create, PATCH, or DELETE | |
| InactiveFlag is omitted | Accept the omission; do not default or add the field | Create | |
| InactiveFlag is omitted | Preserve the existing value; do not add it to the change payload | PATCH | |
| InactiveFlag is explicitly null | Reject the request | Create or PATCH when the field is present with null | |
| InactiveFlag is supplied | The only accepted stored values are uppercase `Y` and `N`. Normalize `Y`/`y`, `true`, or `inactive` to `Y`; normalize `N`/`n`, `false`, or `active` to `N`. | Create, or PATCH when the field is present and non-null | |
| InactiveFlag cannot be unambiguously parsed | Reject the request | Create or PATCH when the supplied value is not `Y`/`N` or one of the accepted terms | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| OEP.VALIDATE_INPUT | decision | 1 | validate_input | valid->OEP.RESOLVE_DEPENDENCIES;invalid->OEP.HANDLE_ISSUE | none | stop | An Expense Pool Create, DELETE, or PATCH request is received |

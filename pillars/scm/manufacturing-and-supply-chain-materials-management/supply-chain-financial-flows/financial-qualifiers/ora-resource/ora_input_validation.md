# Input Validation

Source: User request, supplied Business Object registration screenshot, selected Data Loader REST route, supplied LOV endpoints, and a successfully validated Financial Qualifiers Data Loader workbook.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Qualifier request | Qualifier name; business process type | Blocked | Provide both requested business values | Every Financial Qualifiers request | |
| Business flow type | Requested business flow value | Blocked | Resolve it through the documented Business Flow LOV and store its LookupCode | Every Financial Qualifiers request | resolve_financial_orchestration_business_flow_type |
| User defined catalog | Requested user defined catalog value | Blocked | Resolve it through the documented User Defined Catalog LOV | A user defined catalog is supplied or required by the Data Loader REST schema | resolve_financial_orchestration_user_catalog |
| Qualifier parameter | Requested qualifier parameter value | Blocked | Resolve it through the flow-specific documented Parameter LOV | A qualifier parameter is supplied or required by the Data Loader REST schema | resolve_financial_orchestration_parameter |
| Operator | Requested qualifier operator | Blocked | Resolve it through the documented FOS qualifier-operator LOV | An operator is supplied or required by the Data Loader REST schema | resolve_financial_orchestration_operator |
| Conjunction | Requested qualifier conjunction | Blocked | Resolve it only for a rule with more than one condition | A qualifier conjunction is supplied | resolve_financial_orchestration_conjunction |
| Delete eligibility | Exact qualifier ID or exact qualifier name | Blocked | Retrieve the selected qualifier and require UsedInFlow to be JSON null | A qualifier delete is requested | check_financial_orchestration_qualifier_delete_eligibility |
| Registered business object | Resource Name = financialOrchestrationQualifiers; BO Short Name = ORA_FOS_QUALIFIER_RULE_SET; REST Context = ORA_FSCM_REST; surrogate key = QUALIFIER_RULE_SET_ID | Blocked | Require the exact registered business object | Before import preparation or live execution | |
| Qualifier execution contract | Validated Financial Qualifiers Data Loader workbook and generated archive | Blocked | Revalidate the exact source through core.data-loader before approval | Before preview, import preparation, or live execution | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The requested business flow type is not resolved through the documented LOV | Blocked | Resolve one matching Business Flow LOV record | resolve_financial_orchestration_business_flow_type |
| The requested user defined catalog is not resolved through the documented LOV | Blocked | Resolve one matching User Defined Catalog LOV record | resolve_financial_orchestration_user_catalog |
| The requested qualifier parameter is not resolved through the documented LOV | Blocked | Resolve one matching Parameter LOV record | resolve_financial_orchestration_parameter |
| The requested operator is not resolved through the documented LOV | Blocked | Resolve one matching Operator LOV record | resolve_financial_orchestration_operator |
| The requested conjunction is not resolved through the documented LOV | Blocked | Resolve one matching Conjunction LOV record only for a multi-condition rule | resolve_financial_orchestration_conjunction |
| A qualifier delete does not return UsedInFlow as JSON null | Blocked | Do not prepare, approve, or submit a delete | check_financial_orchestration_qualifier_delete_eligibility |
| The workbook fails live Data Loader schema validation | Blocked | Stop before preview or live execution and correct the source | |
| The Oracle qualifier execution contract is documented and all required request values are present | Continue | Evaluate execution-contract readiness | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Qualifier schema | Require a live-validated Financial Qualifiers Data Loader workbook, exact LOV codes, at least one qualifierRules child, and an exact-name duplicate check before approval | Every supplied qualifier value | |
| Delete eligibility | Permit deletion only when the selected qualifier returns UsedInFlow as JSON null; do not treat blank, false, missing, or unreadable as null | Every qualifier delete request | check_financial_orchestration_qualifier_delete_eligibility |
| Registered business object identity | Use the user-supplied registered resource identity financialOrchestrationQualifiers with BO short name ORA_FOS_QUALIFIER_RULE_SET, REST context ORA_FSCM_REST, and surrogate key QUALIFIER_RULE_SET_ID; do not substitute another business object | Every import or execution request | |
| Execution route | Use the selected Data Loader REST route with financialOrchestrationQualifiers. Do not infer fields, request mapping, lookup behavior, or a direct REST operation | Every preview or live execution request | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FOS.FQ.VALIDATE_INPUT | step | 10 | validate_input | validated->FOS.FQ.RESOLVE_BUSINESS_FLOW;blocked->FOS.FQ.HANDLE_ISSUE | none | stop | Every Financial Qualifiers request |

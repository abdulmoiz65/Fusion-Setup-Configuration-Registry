# Dependency Readiness

Source: User request, supplied Business Object registration screenshot, selected Data Loader REST route, supplied LOV endpoints, and a successfully validated Financial Qualifiers Data Loader workbook.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Qualifier Data Loader REST contract | Confirm the generated sample/schema contract before preview or execution |
| 2 | Business flow type | Resolve the requested business flow through the documented LOV after its Data Loader REST target field is confirmed |
| 3 | User defined catalog | Resolve a requested user defined catalog through the documented LOV after its Data Loader REST applicability and target field are confirmed |
| 4 | Qualifier parameter | Resolve a requested qualifier parameter through the documented LOV after its Data Loader REST applicability and target field are confirmed |
| 5 | Operator | Resolve a requested operator through the documented LOV after its lookup type, Data Loader REST applicability, and target field are confirmed |
| 6 | Conjunction | Resolve a requested conjunction through the documented LOV after its lookup type, Data Loader REST applicability, and target field are confirmed |
| 7 | Delete eligibility | Confirm the selected qualifier returns UsedInFlow as JSON null before a delete preview or submission |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| qualifier_execution_contract | Oracle Financial Qualifiers Data Loader REST contract | Yes | Every Financial Qualifiers request | Verify | Successfully validated financialOrchestrationQualifiers workbook and generated archive | | The live schema accepted the exact workbook structure for the registered business object | Revalidate the exact source before approval | Registered business object: financialOrchestrationQualifiers; source: validated workbook; archive: immutable ZIP |
| business_flow_type | Oracle Financial Orchestration Business Flow Type | Yes | A business process type is supplied | Lookup | User-supplied Business Flow LOV endpoint | resolve_financial_orchestration_business_flow_type | The requested business flow must be an exact LOV result | Provide an exact business flow display value or code | AgreementType: LookupCode; AgreementTypeSearch: LookupCode |
| user_defined_catalog | Oracle Financial Orchestration User Defined Catalog | Conditional | A user defined catalog is supplied or required by the Data Loader REST schema | Lookup | User-supplied User Defined Catalog LOV endpoint | resolve_financial_orchestration_user_catalog | A catalog must be an exact LOV result when applicable | Provide an exact catalog code | Schema-mapped catalog field: CatalogCode |
| qualifier_parameter | Oracle Financial Orchestration Parameter | Conditional | A qualifier parameter is supplied or required by the Data Loader REST schema | Lookup | User-supplied Parameter LOV endpoint | resolve_financial_orchestration_parameter | A parameter must be an exact result from the selected business-flow LOV | Provide an exact parameter display value or code | qualifierRules.QualifierCode: QualifierCode; qualifierRules.QualifierMeaning: QualifierMeaning |
| operator | Oracle standard lookup operator | Conditional | An operator is supplied or required by the Data Loader REST schema | Lookup | User-supplied FOS_QUALIFIER_OPERATORS endpoint | resolve_financial_orchestration_operator | An operator must be an exact result from the FOS qualifier-operator lookup | Provide an exact operator display value or code | qualifierRules.QualifierOperator: LookupCode |
| conjunction | Oracle standard lookup conjunction | Conditional | A rule has more than one condition and a conjunction is supplied | Lookup | User-supplied standard lookup LOV endpoint | resolve_financial_orchestration_conjunction | A conjunction is required only for a multi-condition rule and must resolve exactly | Provide an exact conjunction display value or code | qualifierRules.Conjunction: LookupCode |
| delete_eligibility | Financial Qualifier delete eligibility | Yes | A qualifier delete is requested | Verify | User-supplied financialOrchestrationQualifiers search endpoint | check_financial_orchestration_qualifier_delete_eligibility | A qualifier in use by a flow must not be deleted | Select one exact qualifier ID or name | UsedInFlow: JSON null required for delete |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Execution-contract gap | The import or write contract is undocumented | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FOS.FQ.CHECK_EXECUTION_CONTRACT | step | 20 | resolve_dependency | ready->FOS.FQ.CHECK_DELETE_ELIGIBILITY;blocked->FOS.FQ.HANDLE_ISSUE | FOS.FQ.RESOLVE_BUSINESS_FLOW | stop | After the requested business flow is resolved |

# Error Handling

Source: User request, supplied Business Object registration screenshot, selected Data Loader REST route, supplied LOV endpoints, and successfully validated Financial Qualifiers create and delete workbooks.

## Error Situations

| Situation | What Should Happen |
|---|---|
| The Financial Qualifiers Data Loader REST sample or schema is unavailable | Stop before preview, import preparation, or any Fusion mutation. Generate or request a validated Financial Qualifiers Data Loader REST sample. |
| The supplied Business Flow LOV cannot be matched to a documented Financial Qualifiers Data Loader REST field | Stop before import preparation. Do not infer the field mapping or substitute a business flow value. |
| The supplied User Defined Catalog LOV cannot be matched to a documented Financial Qualifiers Data Loader REST field | Stop before import preparation. Do not infer its applicability, field mapping, or substitute a catalog code. |
| The supplied Parameter LOV cannot be matched to a documented Financial Qualifiers Data Loader REST field | Stop before import preparation. Do not infer its applicability, field mapping, or substitute a qualifier parameter. |
| The supplied Operator LOV cannot be matched to a documented Financial Qualifiers Data Loader REST field | Stop before import preparation. Do not infer its lookup type, applicability, field mapping, or substitute an operator. |
| The supplied Conjunction LOV cannot be matched to a documented Financial Qualifiers Data Loader REST field | Stop before import preparation. Do not infer its lookup type, applicability, field mapping, or substitute a conjunction. |
| The execution route does not target the registered qualifier resource | Stop and reconcile it with financialOrchestrationQualifiers, BO short name ORA_FOS_QUALIFIER_RULE_SET, REST context ORA_FSCM_REST, and surrogate key QUALIFIER_RULE_SET_ID. |
| A request contains values outside the documented qualifier schema | Stop and request a source-backed field definition; do not infer a field or value mapping. |
| A Fusion mutation is requested without a completed contract and approval | Do not submit a write. |
| A delete eligibility lookup returns UsedInFlow with any value other than JSON null | Do not prepare, approve, or submit a delete. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Execution-contract gap | The required Financial Qualifiers Data Loader REST contract is not documented | Supply the approved sample/schema, then regenerate and validate the task guidance. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Execution blocker | The missing contract detail and the safe next action; never credentials, tokens, or raw authorization headers. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| The Data Loader REST execution contract is TBD | Do not invent a field mapping, lookup behavior, uniqueness check, or direct REST action. |
| A Fusion write outcome is unknown | Do not repeat the write automatically. |
| UsedInFlow is blank, false, missing, unreadable, or non-null | Do not treat it as delete eligible. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FOS.FQ.HANDLE_ISSUE | step | 30 | error_handler | handled->FOS.FQ.RETURN_ISSUES | FOS.FQ.VALIDATE_INPUT | stop | An input or execution-contract blocker occurs |
| FOS.FQ.RETURN_ISSUES | terminal | 40 | terminal | none | FOS.FQ.HANDLE_ISSUE | stop | A blocker was disclosed |
| FOS.FQ.DONE | terminal | 50 | terminal | none | FOS.FQ.CHECK_DELETE_ELIGIBILITY | stop | A source-backed qualifier execution contract and all required request values are validated |

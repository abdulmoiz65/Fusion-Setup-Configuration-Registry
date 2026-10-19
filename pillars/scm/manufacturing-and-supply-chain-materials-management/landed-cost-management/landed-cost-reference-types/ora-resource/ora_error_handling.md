# Landed Cost Reference Types Error Handling

Source: Oracle, [Manage Landed Cost Reference Types](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/manage-landed-cost-reference-types.html) (26C), the task's core.data-loader route, and user-supplied lookup contracts.

## Error Situations

| Situation | What Should Happen |
|---|---|
| The published landedCostReferenceTypes Data Loader contract is unavailable or no longer validates | Stop before preview or submission. Regenerate and validate the Data Loader sample; do not substitute a direct REST route. |
| A reference data set or data type lookup has no exact match or more than one match | Stop before preview and request a corrected SetCode, SetName, or DataType meaning. |
| An existing reference type Code or Name lookup has no exact match or more than one match | Stop before preview and request a corrected Code or Name. Do not guess ChargeReferenceTypeId for an update or delete. |
| A reference type load or delete is requested through anything other than core.data-loader | Stop before preview or submission. Route the request through core.data-loader using landedCostReferenceTypes. |
| InactiveFlag is missing, Boolean True or False, or a value other than Y or N in the prepared Data Loader source | Default an omitted value to false and write N; otherwise correct the source to its literal Y or N value, regenerate the archive, and validate again. |
| A live Data Loader request fails or has an indeterminate outcome | Preserve sanitized diagnostics and stop before retrying or issuing another create request. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Supplied reference type data does not conform to the registered Data Loader contract | Correct the data and validate again. |
| Input validation | InactiveFlag is not represented as literal Y or N in the Data Loader source | Convert true to Y and false to N, regenerate the Data Loader archive, and validate again. |
| Lookup mismatch | A SetCode, SetName, or DataType meaning lookup returns zero or multiple exact matches | Correct the supplied value and re-run the documented read-only lookup. |
| Lookup mismatch | A Code or Name lookup for an existing reference type returns zero or multiple exact matches for an update or delete | Correct the supplied identity and re-run resolve_landed_cost_reference_type_id. |
| Contract blocker | The published landedCostReferenceTypes create contract cannot be validated | Regenerate the registered sample through core.data-loader and correct the confirmed discrepancy. |
| Process failed | Fusion rejects a submitted request | Preserve the returned diagnostic and correct the confirmed issue before a new approved attempt. |
| Process timeout | Submission status is indeterminate | Stop and reconcile through an approved read path before any retry. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before a live import or delete | Exact target environment, registered business object, validated reference type identity and data, intended operation, and the approval requirement. |
| After a failed or indeterminate import | Environment, operation, known status, sanitized diagnostic, and safe next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Published Data Loader create contract is unavailable | Do not construct a direct REST path or submit an unvalidated artifact. |
| A resolver has no unique exact match | Do not guess SetId, DataType, or ChargeReferenceTypeId. |
| An existing reference type Code or Name lookup has no unique exact match | Do not guess ChargeReferenceTypeId or prepare a Data Loader update or delete. |
| InactiveFlag is omitted | Do not leave the field blank; apply the documented false default and write N before preview. |
| The selected load route is not core.data-loader | Do not load Landed Cost Reference Types through a direct REST request, database update, or another executor. |
| Approval is absent or no longer matches the preview | Do not create, update, or delete a reference type. |
| A create, update, or delete outcome is indeterminate | Do not retry the operation automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LANDED_COST_REFERENCE_TYPES.EXECUTION_GATE | step | 60 | execution_gate | preview-ready-and-approved->RETURN_SUCCESS;contract-missing-or-approval-absent->RETURN_ISSUES | LANDED_COST_REFERENCE_TYPES.ENFORCE_DATA_LOADER_ROUTE | stop | The Data Loader contract and reference type input have passed validation, and a live import or delete is requested. |
| RETURN_SUCCESS | terminal | 70 | terminal | none | LANDED_COST_REFERENCE_TYPES.EXECUTION_GATE | continue | The validated reference type request is ready for its separate explicit import approval. |
| RETURN_ISSUES | terminal | 80 | terminal | none | none | continue | An input, lookup, contract, preview, approval, or execution gate failed. |

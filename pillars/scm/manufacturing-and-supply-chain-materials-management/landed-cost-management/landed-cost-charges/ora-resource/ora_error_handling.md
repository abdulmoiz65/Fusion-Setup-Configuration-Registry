# Landed Cost Charges Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required lookup has no match, more than one match, or fails | Stop before preview or routed execution; retain only redacted diagnostics and request a distinct selection. |
| An optional-child lookup is unresolved | Report that child association as unresolved without treating it as a primary-charge failure. |
| A routed create or child-association operation fails | Do not retry a mutation automatically; reconcile the primary record through the approved route before any new attempt. |
| A delete of an analysis-code association is requested | Require the exact ChargeAnalysisCodeId and the task route's current approval before the mutation. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required primary values or a conditional UOM are missing. | Correct the input, then revalidate. |
| Reference lookup | A required primary LOV has no exact selected result, multiple candidates, or an unavailable response. | Correct the selection, then revalidate. |
| Optional child resolution | A selected default reference type, analysis group, or analysis code cannot resolve uniquely. | Report the child issue; keep an otherwise valid primary charge eligible. |
| Child deletion identity | A requested analysis-association deletion lacks one exact ChargeAnalysisCodeId. | Resolve the existing child association before a new preview. |
| Parent-child payload contract | A child is attempted before the primary charge exists or the current workbook cannot serialize its required child fields. | Create or identify the primary charge, then regenerate and validate through core.data-loader. |
| Process failed | A routed parent or child mutation returns a failure. | Preserve redacted diagnostics; reconcile the target before any new approved attempt. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Primary lookup failure | The supplied business value, match-count category, and required correction; never select the first result. |
| Optional child lookup failure | The unresolved child selection and that primary-charge creation is unaffected. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Primary LOV resolution is incomplete | Do not invent, fuzzy-match, or select the first SetId, currency, conversion type, charge basis, allocation basis, or UOM. |
| Optional child selection is unresolved | Do not submit that child association or use a supplied display value as an identifier. |
| Analysis association deletion lacks ChargeAnalysisCodeId | Do not use AnalysisGroupId or AnalysisCodeId as a substitute delete key. |
| Routed mutation is uncertain or failed | Do not automatically retry a POST or DELETE. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LCC.DONE_PRIMARY_READY | terminal | 120 | terminal | none | LCC.ENFORCE_PRIMARY_FIRST | stop | The request passed validation, lookup, and design gates and is ready for the approved execution route. |
| LCC.DONE_PRIMARY_READY_NO_ALLOCATION_UOM | terminal | 115 | terminal | none | LCC.ENFORCE_PRIMARY_FIRST_NO_ALLOCATION_UOM | stop | The request without an applicable allocation UOM passed validation, lookup, and design gates and is ready for the approved execution route. |
| RETURN_ISSUES | terminal | 130 | terminal | none | none | stop | A required validation, lookup, dependency, or design gate cannot be satisfied. |

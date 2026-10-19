# Cost Component Mapping Groups Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required parent or child mapping field is missing | Stop and show the missing fields; do not generate a Data Loader package |
| The mapping-group set cannot be resolved from the UI-selectable cost set LOV | Stop before preview and request one unambiguous returned SetName |
| A child-only request lacks ComponentGroupId, or a master-details child lacks the new parent's ComponentGroupCode or SetName | Stop and identify the existing parent or populate the exact new-parent surrogate keys before retrying the complete package |
| Oracle rejects a create request | Show the affected mapping group or child record and stop before retrying |
| Oracle rejects an update or delete request | Show the affected parent or child mapping and stop before retrying |
| A mapping group is used in a cost profile | Reject its update or deletion |
| A landed-cost mapping controls capitalization | Reject a CapitalizationFlag update when the control lookup returns isUsedinCTC=Y |
| A non-default child mapping is requested before the default predefined component is mapped | Show the nonblocking default-component readiness message and continue when all other validation passes |
| A documented child duplicate preflight returns a row | Stop and show the existing mapping; do not generate the ZIP |
| Current element type evidence conflicts with an existing child-row display label | Stop with TYPE_CONFLICT; do not reinterpret or update that mapping silently |
| A master-details Data Loader ZIP partially loads | Read every affected parent and child collection, preserve the failure evidence, and correct the complete master-details draft before a new validation and approval cycle. Do not split the requested create into partial batches or retry the same submission, except for the documented ComponentSource-missing fallback after reconciliation. |
| A completed combined child package reports You must provide a value for the Cost Component Source attribute, but every submitted component-code DAT row has a nonblank canonical ComponentSource | Preserve the failed dataset status and the returned diagnostic. Use reconcile_component_source_failure_effects to compare every requested mapping with readback; classify as RECONCILED_PARTIAL only if every requested source, destination, set, type, and flag value is present exactly once. Do not call this a clean load or retry automatically. |
| A user proceeds after RECONCILED_PARTIAL ComponentSource-missing evidence | Build fresh, independently validated artifacts: parent update first, predefined component child second, and landed-cost plus cost-element children third. Obtain approval for each immutable artifact. Verify the parent request succeeds before initiating the two child requests; those two requests may then run in parallel. |
| A generated child row has blank ComponentSource or an unresolved source cost element | Reject the workbook before ZIP creation. Rebuild the row from a template-compatible accepted mapping or the required LOV result; do not submit a code-only or generic-element fallback |
| Any row in a requested Data Loader package fails pre-submit template or LOV validation | Reject the whole package before ZIP creation. Correct the draft and generate one complete validated ZIP; do not submit only the rows that currently pass |
| A preflight finds one invalid row in an executable dependency batch | Stop and correct the complete draft before submission; do not use a partial import or row-by-row retry as the normal execution path |
| A generated component-code worksheet row has a blank or noncanonical ComponentSource, missing required companion field, or an unexpected row count | Reject the whole package before ZIP creation. Correct the source lookup or workbook mapping, then regenerate and inspect the complete package |
| A Data Loader parent DELETE is requested while the target has child mappings | Read and disclose the children, then submit the parent-only DELETE. If Fusion rejects it specifically because children remain, stop; prepare a separate child-cleanup ZIP only after that rejection and require a fresh validation and approval cycle. |
| A parent DELETE targets a mapping group where isUsedInCostProfile=Y | Reject the request; the group is in use and must not be deleted |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required input, selectable set, existing parent ComponentGroupId, new-parent surrogate keys, or required source/destination is absent | Request the exact missing value or dependency evidence |
| FAILED | The Data Loader operation is rejected or the result does not match a declared transition | Preserve sanitized evidence and correct the input or contract before another attempt |
| RECONCILED_PARTIAL | Fusion reports the exact ComponentSource-missing dataset message, submitted component-code rows all contain nonblank canonical ComponentSource, and exact readback confirms every requested mapping effect | Preserve the failed dataset result and reconciliation evidence; do not retry automatically. Require an explicit user decision before any further test, correction, or rollback. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before a write is authorized | The normalized mapping-group intent, intended parent and child resource effects, the preview result, and the approval scope |
| Before retrying a rejected or uncertain write | The failure category, affected record, and need for read-only verification or corrected input |
| After ComponentSource-missing reconciliation | The failed dataset counts and message, submitted ComponentSource evidence, exact requested-versus-returned mapping comparison, and that RECONCILED_PARTIAL is not clean success |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A Data Loader import has failed or its outcome is uncertain | Do not automatically retry or recreate the mapping group |
| A Data Loader child workbook was assembled from incomplete fields | Do not submit it: populate every template field marked required or for-new-records, including mapping type, display names, element IDs, type codes, and RestAction |
| Parent and child DELETE rows are combined in one Data Loader package | Do not submit it: use a parent-only DELETE package. Do not preemptively create a child-delete package solely because child mappings exist. |
| A partial Data Loader load is used as the planned customer execution path | Do not present or use it as success. Correct the preflight logic and require one fully validated master-details package for the customer operation. |
| A ComponentSource-missing dataset result is returned | Do not ignore, relabel as success, or automatically retry it solely because some or all requested mappings appear in readback. Reconcile every requested value first and retain the dataset failure evidence. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCM.EXECUTION_GATE | step | 60 | execution_gate | approved_preview->CCM.READY_FOR_RUNBOOK;blocked->RETURN_ISSUES | CCM.DESIGN_ENFORCEMENT | stop | The task is otherwise ready for an external preview-and-approval workflow |
| CCM.READY_FOR_RUNBOOK | terminal | 70 | terminal | none | CCM.EXECUTION_GATE | stop | A documented execution contract, current preview, and explicit approval are available |
| CCM.DONE_FIND_BY_CODE | terminal | 71 | terminal | none | CCM.FIND_BY_CODE | stop | A mapping group finder by code completed |
| CCM.DONE_FIND_BY_NAME | terminal | 72 | terminal | none | CCM.FIND_BY_NAME | stop | A mapping group finder by name completed |
| CCM.DONE_FIND_BY_SET | terminal | 73 | terminal | none | CCM.FIND_BY_SET | stop | A mapping group finder by set completed |
| CCM.DONE_FIND_BY_DESCRIPTION | terminal | 74 | terminal | none | CCM.FIND_BY_DESCRIPTION | stop | A mapping group finder by description completed |
| CCM.DONE_LIST | terminal | 75 | terminal | none | CCM.LIST_MAPPING_GROUPS | stop | A mapping-group list completed |
| CCM.DONE_READ_GROUP | terminal | 76 | terminal | none | CCM.READ_MAPPING_GROUP | stop | A mapping-group read completed |
| CCM.DONE_READ_PREDEFINED | terminal | 77 | terminal | none | CCM.READ_PREDEFINED_MAPPINGS | stop | A predefined mapping read completed |
| CCM.DONE_READ_LANDED | terminal | 78 | terminal | none | CCM.READ_LANDED_MAPPINGS | stop | A landed-cost-management mapping read completed |
| CCM.DONE_LANDED_PREFLIGHT | terminal | 79 | terminal | none | CCM.CHECK_LANDED_DUPLICATE | stop | A landed-cost duplicate preflight found no existing mapping |
| CCM.DONE_PREDEFINED_PREFLIGHT | terminal | 80 | terminal | none | CCM.CHECK_PREDEFINED_DUPLICATE | stop | A predefined component duplicate preflight contract is complete and clear |
| CCM.DONE_CAPITALIZATION_CHECK | terminal | 81 | terminal | none | CCM.CHECK_CAPITALIZATION_CONTROL | stop | The capitalization control check permits the requested change |
| CCM.DONE_READ_ELEMENTS | terminal | 82 | terminal | none | CCM.READ_COST_ELEMENT_MAPPINGS | stop | A cost-element mapping read completed |
| CCM.DONE_RESOLVE_COST_SET | terminal | 83 | terminal | none | CCM.RESOLVE_COST_SET | stop | A cost set lookup resolved exactly one value |
| CCM.DONE_RESOLVE_PREDEFINED_COMPONENT | terminal | 84 | terminal | none | CCM.RESOLVE_PREDEFINED_SOURCE_COMPONENT | stop | A predefined source component lookup resolved exactly one value |
| CCM.DONE_RESOLVE_LANDED_COMPONENT | terminal | 85 | terminal | none | CCM.RESOLVE_LANDED_SOURCE_COMPONENT | stop | A landed-cost-management source component lookup resolved exactly one value |
| CCM.DONE_RESOLVE_COST_ELEMENT | terminal | 86 | terminal | none | CCM.RESOLVE_COST_ELEMENT_FOR_SET | stop | A destination cost element lookup resolved exactly one value |
| CCM.DONE_RESOLVE_PROFIT_SOURCE_ELEMENT | terminal | 87 | terminal | none | CCM.RESOLVE_PROFIT_SOURCE_ELEMENT | stop | A PROFIT_IN_INVENTORY source or destination element lookup resolved exactly one value |
| CCM.DONE_VALIDATE_DESTINATION_SET_SCOPE | terminal | 88 | terminal | none | CCM.VALIDATE_DESTINATION_SET_SCOPE | stop | Destination set scope validation resolved exactly one permitted set |
| CCM.DONE_RESOLVE_SOURCE_COST_ELEMENT | terminal | 89 | terminal | none | CCM.RESOLVE_SOURCE_COST_ELEMENT_FOR_SET | stop | A source cost element lookup resolved exactly one value |
| CCM.DONE_RECONCILED_COMPONENT_SOURCE_FAILURE | terminal | 91 | terminal | none | CCM.RECONCILE_COMPONENT_SOURCE_FAILURE | stop | Exact readback reconciled every requested mapping after the ComponentSource-missing dataset error |
| RETURN_ISSUES | terminal | 90 | terminal | none | none | stop | Any validation, lookup, dependency, design, or approval gate fails |

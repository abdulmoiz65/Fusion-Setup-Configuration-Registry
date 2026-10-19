# Error Handling

Source: Oracle Fusion Cloud Sales, Manage Identifier Types — https://docs.oracle.com/en/cloud/saas/sales/oacdm/manage-identifier-types.html#Create-Additional-Identifier-Types

## Error Situations

| Situation | What Should Happen |
|---|---|
| Party Type, short name, descriptive name, or unique-name selection is missing for a create request | Stop before preview and request only the missing field. |
| Short name is not unique | Stop before preview and request a different short name. |
| Edit request has no target identifier type or no editable field | Stop before preview and request the missing target or change. |
| Approved archive, target environment, or Task Hook envelope does not match | Stop before the POST and rebuild the immutable approval preview. |
| Fusion rejects the native import process creation request | Preserve a redacted response and stop; do not retry the POST automatically. |
| Import process times out or fails | Preserve the `ProcessId`, retrieve the available process log, and resume only that process on a later status request. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Required create or edit information is missing | Correct the request and revalidate. |
| design_blocker | A required Party Type, unique short name, descriptive name, or multiplicity decision is absent | Provide the missing design decision and rerun design enforcement. |
| adapter_capability_gap | The approved native FSM adapter or its required response contract is unavailable | Stop before POST and restore the adapter contract. |
| fusion_api_error | Fusion rejects the native setup-task CSV import request | Preserve redacted diagnostics and stop without retry. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Create preview | Party Type, short name, Additional Identifier descriptive name, optional Description, and unique-name selection. |
| Execution readiness | The fixed native `setupTaskCSVImports` adapter, immutable path/hash, target environment, and approval envelope. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AIT.EXECUTION_GATE | decision | 3 | execution_gate | ready->AIT.READY;blocked->AIT.RETURN_ISSUES | AIT.DESIGN_REVIEW | stop | Before execution; approved path/hash/envelope and native adapter must match. |
| AIT.READY | terminal | 4 | terminal | none | AIT.EXECUTION_GATE | continue | The native FSM adapter and all preview gates are ready. |
| AIT.RETURN_ISSUES | terminal | 5 | terminal | none | none | continue | Input, design, approval, or adapter validation is blocked. |

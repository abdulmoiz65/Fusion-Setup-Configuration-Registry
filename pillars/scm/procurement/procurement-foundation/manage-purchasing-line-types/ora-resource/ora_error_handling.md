# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required create field is absent or invalid | Stop and request the missing or valid value. |
| A uniqueness, reserved-code, or design rule fails | Stop before preview and correct the request; do not silently substitute a value. |
| The Data Loader or REST execution cannot resolve LineTypeId for PATCH | Preserve the server diagnostic and correct the identifier; client-side validation does not issue a lookup or substitute another item. |
| A request changes a field prohibited by the update rules | Stop and remove the prohibited field from the request. |
| The Data Loader business object rejects a DFF context, attribute, or segment value | Preserve the server diagnostic. For a deployed global context, retain supplied segment data and parent linkage, then let the Data Loader converter derive the context from the DFF header rather than placing its display value in `__FLEX_Context`; client-side validation does not perform a live DFF lookup. |
| A preview or live operation fails | Preserve sanitized diagnostics and stop before retrying, changing the operation, or issuing a direct REST write. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required request data, dependency evidence, DFF context, or approval is absent | Collect the missing evidence and revalidate. |
| FAILED | Lookup, validation, design, preview, or live-operation result fails | Correct the documented issue and rerun the applicable preview; never automatically retry a mutation. |
| UNSUPPORTED | The requested change is not allowed by the documented task contract | Remove the unsupported change or use the supported setup route. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Design or preview block | Requested operation, validated line-type identity, applicable defaults, blocking rule, and safe correction. |
| Live failure | Intended operation, LineTypeId when applicable, sanitized response, verified side effects, and safe next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A required field is unresolved | Do not construct a substitute payload. Defer unique-identity and existing-item resolution to the Data Loader or REST execution. |
| A credit-line, seeded-data, or DFF gate fails | Do not ignore the restriction or silently remove user-supplied business data. A redundant deployed global-context display value in the converter-managed technical `__FLEX_Context` field is not business data and may be omitted. |
| A write outcome is uncertain | Do not automatically retry POST or PATCH. |
| A request reaches the task guidance without current approval | Do not perform a direct REST write. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PLT.READY_FOR_APPROVAL | decision | 50 | execution_gate | create_ready->PLT.DONE_CREATE;update_ready->PLT.DONE_UPDATE;missing_approval->RETURN_ISSUES | PLT.ENFORCE_DESIGN | stop | A valid create or update request reaches its approval gate |
| PLT.DONE_CREATE | terminal | 60 | terminal | none | PLT.READY_FOR_APPROVAL | stop | The validated create request has current approval |
| PLT.DONE_UPDATE | terminal | 70 | terminal | none | PLT.READY_FOR_APPROVAL | stop | The validated update request has current approval |
| PLT.DONE_LIST | terminal | 16 | terminal | none | PLT.VALIDATE_INPUT | stop | Client-side validation completed; no external read is performed by this task route |
| RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | Any validation, lookup, design, or approval gate blocks the request |

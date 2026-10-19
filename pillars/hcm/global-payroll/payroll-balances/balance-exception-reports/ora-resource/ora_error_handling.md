# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required input is blank, invalid, ambiguous, duplicated, or incompatible | Return a field-specific result and stop before preview, import preparation, or live execution. |
| Task-specific FSM template/export evidence is missing | Classify as catalog mismatch or artifact-persistence blocker;do not infer filenames, headers, keys, actions, or child-row syntax. |
| Target-pod lookup, capability, privilege, or environment evidence is absent or conflicting | Classify as auth/authz, catalog mismatch, or transport/environment;stop and capture only redacted diagnostics. |
| An FSM import process fails or times out | Retrieve and persist redacted status and ProcessLog when available;do not retry the import without idempotency or explicit approval. |
| FSM ProcessLog reports a null child logical row | Treat as a child-relationship validation failure; compare the child view instance and grouping key to a current task export before preparing a replacement package. |
| FSM ProcessLog reports `HRC_FK_ATTR_UNABLE_TO_RESOLVE2` for `ConsolidationSetId` or `PayrollId` | Treat as an FSM null-encoding failure when no corresponding restriction was requested; replace empty identifier fields with `#null` and prepare a newly approved package. |
| FSM ProcessLog reports `HRC_FK_ATTR_UNABLE_TO_RESOLVE2` for `BalExceptionId` | Treat as an exception-identity binding failure. Re-run the seeded-reference evaluator using the user-supplied name, report LDG, and legislation context; preserve `BaseBalExceptionName` and apply its child binding. Do not substitute an existing-report export or ask the user to supply an ID. Obtain fresh approval for any replacement package. |
| An internal UI endpoint is proposed as a substitute for FSM | Refuse the operation unless a separately approved custom-API route and target-pod contract exist. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | Supplied report name, LDG, references, or included exceptions fail validation | Correct the field-specific issue and rerun validation. |
| catalog mismatch | Task-specific FSM schema or capability does not match the requested operation | Obtain current task template/export evidence and reconcile the mismatch. |
| auth/authz | Read, export, import, or status access lacks the required role or privilege | Obtain the appropriate access and repeat only the approved read-only check. |
| transport/environment | Pod identity, connectivity, or environment evidence is unavailable | Confirm the target environment and capture redacted diagnostic evidence. |
| process failed | An FSM process returns a failure | Preserve redacted ProcessLog/status and correct the underlying data or artifact before a newly approved submission. |
| process timeout | An FSM process does not complete in the permitted interval | Record task code, ProcessId, last status, elapsed wait, and next-check path;do not resubmit automatically. |
| approval blocker | The live import lacks approval bound to the exact target and immutable ZIP | Obtain explicit approval immediately before submission. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before live FSM import | Exact target environment, task code, operation, immutable ZIP/hash, preview/validation result, and approval requirement. |
| On failed or timed-out process | Environment, task code, ProcessId/requestId when available, last status, elapsed time, redacted ProcessLog reference, and safe next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Current template schema is unavailable | Do not hand-build an import ZIP or reuse PAY_MANAGE_BALANCE_EXCEPTIONS artifacts. |
| Approval is missing or stale | Do not submit, retry, or replay an FSM import. |
| Reference match is unresolved | Do not choose a match automatically or put a display name in an ID/code field. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEXR.EXECUTION-GATE | decision | 11 | execution_gate | ready->RETURN-SUCCESS;blocked->RETURN-ISSUES | BEXR.ENFORCE-FSM-DESIGN | stop | A live FSM import is requested after all preceding checks |
| RETURN-SUCCESS | terminal | 12 | terminal | none | BEXR.EXECUTION-GATE | stop | All applicable gates passed |
| RETURN-ISSUES | terminal | 13 | terminal | none | none | stop | Any blocking validation, lookup, design, execution, or approval result occurs |

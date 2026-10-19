# Balance Exceptions error handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required input, lookup result, or compatibility rule is missing or invalid | Stop, identify the affected field, and return the safe corrective action |
| FSM task capability or template ZIP does not match the selected pod | Stop as a catalog mismatch; do not infer headers, keys, action values, or delete behavior |
| Read-only lookup is unauthorized or unavailable | Stop as auth/authz or transport/environment failure and retain redacted evidence |
| FSM export/import process fails | Persist redacted ProcessLog and status evidence under the implementation project when a project workflow is active; do not retry an import automatically |
| FSM polling times out | Stop with environment, operation, task code, process ID, last status, elapsed wait, and next-check path |
| An internal Payroll Generic endpoint is proposed for mutation | Refuse that route unless a separately approved custom REST action has target-pod contract and privilege evidence |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required user input, exact lookup result, target-pod evidence, or explicit approval is absent | Request the precise missing item |
| FAILED | Validation, catalog, auth/authz, transport/environment, Fusion API, process, or artifact persistence failure occurs | Preserve redacted diagnostics and follow the documented recovery path |
| UNSUPPORTED | Requested action would infer a public endpoint, hidden UI contract, or unsupported FSM layout | Use task-level FSM evidence or obtain a separately approved workflow |
| ALL_GOOD | Validation and design gates pass and the request is ready for the selected FSM execution workflow | Continue only through the selected task-level FSM workflow |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before live FSM import | Exact target pod, task code PAY_MANAGE_BALANCE_EXCEPTIONS, immutable ZIP/hash, intended operation, validation result, and explicit-approval request |
| After a failed or timed-out FSM process | Environment, task code, process ID, last status, elapsed wait, artifact references, redacted ProcessLog/status evidence, and next safe action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Display-name lookup has zero or many matches | Do not automatically select a candidate or populate an identifier/code field |
| FSM template/schema is unavailable | Do not manufacture a CSV, ZIP, payload, action value, or key syntax |
| Live import approval is absent or stale | Do not submit or retry an import |
| Report execution is requested without separately approved payroll-flow workflow | Do not submit Run Balance Exception Report |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BE.EXECUTION_GATE | decision | 60 | execution_gate | ready->BE.READY_FOR_FSM;missing->BE.RETURN_ISSUES | BE.ENFORCE_DESIGN | stop | Design enforcement passed |
| BE.READY_FOR_FSM | terminal | 70 | terminal | none | BE.EXECUTION_GATE | stop | FSM execution is selected and all gates pass |
| BE.RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | Any validation, lookup, dependency, design, or execution gate returns an issue |

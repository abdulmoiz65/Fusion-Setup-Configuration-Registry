# Error Handling

## Source

- Oracle readiness: Streamline the Import and Export of Messaging Setup Data, 26C, https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/sccv26c/26C-sccv-wn-f46531.htm

## Error Situations

| Situation | What Should Happen |
|---|---|
| `ORA_CMK_B2B_DOCUMENT_SETUP` returns `EnabledFlag: N` on the selected host | Show "Simplified Collaboration Messaging Configuration export/import is blocked in {environment}: go to Navigator > My Enterprise > Offerings, select Procurement > Opt In Features, enable Simplify Configuration and Processing for B2B Messaging (`ORA_CMK_B2B_DOCUMENT_SETUP`), and wait for opt-in processing to complete. Then retry this operation." Stop before creating an export process or approving an import |
| A task-CSV upload or import has an uncertain response | Preserve every returned request/process ID; use Core Data Loader's status route to reconcile the same submission. Do not replay the write |
| Task-CSV import reaches terminal failure or warnings | Retrieve and retain Core Data Loader's ProcessLog or task-level result report, then correct the reported issue before a new approved import |
| Caller-requested task-CSV status checks reach ten minutes at intervals of at least thirty seconds | Stop polling; record environment, task code, request/process ID, last status, elapsed wait, and a status-only next check. Do not resubmit |
| Configuration-package export, upload, or import reports an error | Review that route's Export and Import Process Results page and stop before retrying |
| The execution contract is unresolved | Return the missing contract fields; do not use a browser, direct REST call, or substitute route |
| Feature or task-CSV ZIP, target, preview, or approval is incomplete | Return the blocker and required corrective action before import submission |
| Configuration-package project, package, or task scope is incomplete | Return the blocker and required corrective action on that route |

## Opt-In Recovery Steps

1. Navigate to **Navigator → My Enterprise → Offerings**.
2. Select the **Procurement** offering, then select **Opt In Features**.
3. Find **Simplify Configuration and Processing for B2B Messaging**.
4. Select its enable icon and complete the opt-in flow.
5. Wait for the opt-in migration or background processing to finish.
6. Rerun the Simplified Collaboration Messaging Configuration export or import.

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | Route-specific operation, task ZIP, target, project scope, or package information is missing | Provide the missing information for the selected route |
| approval blocker | The task-specific execution contract or required approval is missing | Obtain the approved contract or approval |
| process failed | FSM export, upload, or import reports terminal errors | Retain ProcessLog/result evidence and correct the reported error before a new approved attempt |
| process timeout | The same returned process remains nonterminal after the bounded caller-requested status window | Preserve last status and continue status retrieval for that ID only |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before task-CSV import approval | Exact target environment and Run Book, task code, immutable ZIP path and SHA-256, export provenance, Task Hook result, and Core Data Loader preview |
| Accepted task-CSV import | Returned request/process ID and status-only check path; record a diagnostic under the project workspace |
| On process failure or timeout | Task code, request/process ID, last status, elapsed wait when timed out, ProcessLog/result path when available, and a safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Public documentation lacks an execution contract | Do not infer a writable API, payload, browser automation, or retry |
| A process result is incomplete or failed | Do not claim completion or retry automatically |
| ZIP bytes, target, task, or preview differ from approval | Do not upload; rerun preflight and obtain approval for the exact artifact |
| Import response is uncertain or a process ID exists | Do not submit a duplicate task-CSV import; reconcile status through Core Data Loader |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CMKSC.GATE_EXECUTION | decision | 50 | execution_gate | ready->CMKSC.DONE;blocked->CMKSC.RETURN_ISSUES | CMKSC.ENFORCE_DESIGN | stop | Before live execution |
| CMKSC.RETURN_ISSUES | terminal | 60 | terminal | none | none | continue | Any blocking condition |
| CMKSC.DONE | terminal | 70 | terminal | none | CMKSC.GATE_EXECUTION | continue | Execution gate passed |

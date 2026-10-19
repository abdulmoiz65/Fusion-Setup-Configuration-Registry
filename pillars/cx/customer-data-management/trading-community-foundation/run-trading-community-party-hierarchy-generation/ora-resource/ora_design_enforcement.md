# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Resolve business identity | Require one exact hierarchy type and flattening method; map bare partner wording to Partner Hierarchy and show the full option list when a required value remains unresolved. |
| 2 | Resolve scope | Preserve exact hierarchy-name and Version text; use null for omitted values; display all-hierarchy scope and active/default version in the consolidated confirmation. |
| 3 | Confirm Force intent | Accept Force Flattening or full mode language and display its impact prominently in the consolidated confirmation. |
| 4 | Enforce execution contract | Require a documented hierarchy type and method, exact payload shape, retries 0, one POST, separate requestId polling, and one current consolidated approval covering all execution details. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Hierarchy type contains bare partner wording | Information |  |  | Normalize it to Partner Hierarchy; require Trading Community Party wording for that separate type | Yes |
| Live execution uses a hierarchy type outside CUSTOMER, DUNS_AND_BRADSTREET, PARTNER, or TRADING_COMMUNITY_PARTY | Error |  | No declared argument1 transport value exists for the selected type | Select one documented hierarchy type or add source-backed transport evidence and tests for a future option | No |
| hierarchy_name is omitted | Warning |  | The consolidated approval does not visibly state all hierarchies of the selected type | Transport null, show the broad scope warning, and let the single consolidated confirmation authorize scope and submission | Yes |
| hierarchy_version is supplied | Error |  | The supplied Version is altered or replaced before argument3 is built | Preserve and pass the exact user-supplied Version value | Yes |
| FORCE is selected | Error |  | Force intent is implicit rather than explicitly requested | Explicitly select Force Flattening and include its full-reflatten warning in the consolidated approval | Yes |
| Live execution is requested | Error |  | Target environment, supported mapping, immutable payload, or consolidated authorization is missing | Complete intake and target resolution, then present one business-facing approval containing the job name, environment, business parameters, and warnings; keep payload and transport identifiers internal | Yes |
| A new run or rerun is requested | Error |  | The response substitutes an older completed run, request ID, preview, payload, parameters, or approval for the new request | Start a fresh intake and create a new run ID, immutable preview, payload, and consolidated approval checkpoint | Yes |
| More than one business approval is planned | Error |  | Parameters, scope, environment, and submission are split into separate confirmation prompts | Resolve all inputs first and replace them with one consolidated approval immediately before submission | Yes |
| Execution plan contains retries or more than one POST | Error |  | retries is not 0 or the plan can resubmit automatically | Set retries to 0, submit once, checkpoint requestId, and poll separately | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PHG.DESIGN_GATE | decision | 4 | design_enforcement | pass->PHG.EXECUTION_GATE;fail->PHG.RETURN_ISSUES | PHG.DEPENDENCY_READINESS | stop | Before presenting the single consolidated approval or tracking an existing request as this task. |

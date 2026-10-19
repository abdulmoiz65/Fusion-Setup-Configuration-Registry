# Time Rules Error Handling

Source: Requested Time Rule matching, approval, creation, and verification behavior.

## Error Situations

| Situation | What Should Happen | Next Action |
|---|---|---|
| Required normalized behavior is missing | Stop before lookup | Obtain and validate the missing requirement |
| Current export is missing, stale, unreadable, or internally inconsistent | Stop without creating anything | Refresh all five objects and rerun lookup |
| Multiple exact matches exist | Block automatic selection | Present all candidates and require user selection |
| Compatible but non-exact matches exist | Block automatic reuse and creation | Disclose differences and require user selection |
| Missing rule creation is not approved or has no supported writable contract | Keep the dependency blocked | Obtain approval and a documented execution contract |
| Rule creation fails | Stop dependent preparation | Show the failure and correct it before retrying |
| Newly created rule cannot be verified in a refreshed export | Do not reference the rule | Investigate creation status and verify explicitly |
| Import result is uncertain | Do not resubmit automatically | Reconcile status and verify authoritative state first |

## Error Classifications

| Error Type | Classification | Retry Allowed | Notes |
|---|---|---|---|
| Invalid or incomplete requirement | Input | After correction | No lookup or create handoff occurs |
| Missing or ambiguous match | Lookup | After refresh or user selection | Ambiguity is never resolved automatically |
| Compatible-only match | Decision required | After user selection | Differences must be disclosed |
| Missing contract or approval | Dependency | After authorization | Do not invent an action, endpoint, or payload |
| Failed creation or verification | Execution | After diagnosis and explicit retry | Never treat submission as verification |
| Uncertain import result | Reconciliation | After status verification | Never automatically resubmit |

## Disclosure Rules

| Situation | What Must Be Shown |
|---|---|
| Exact match selected | RuleName, RuleType, normalized matched behavior, and verification source |
| Multiple or compatible candidates | Every candidate and every material behavioral difference |
| Conditional creation proposed | Complete normalized specification, unresolved contract fields, and approval status |
| Creation or verification failure | Submitted identity, known result, missing evidence, and safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| RuleName matches but behavior does not | Do not reuse the rule by name alone |
| Candidate selection is ambiguous | Do not choose automatically |
| Lookup fails | Do not create or prepare dependent Rule Set members |
| Writable contract is undocumented | Do not invent an action type, endpoint, payload, or execution result |
| Verification is incomplete | Do not expose the proposed rule as ready |
| Import status is uncertain | Do not automatically resubmit |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| TIMERULE.REUSE_READY | terminal | 4 | terminal | none | TIMERULE.FIND_MATCH | stop | Exactly one verified exact match exists |
| TIMERULE.SELECTION_REQUIRED | terminal | 5 | terminal | none | none | stop | Multiple exact or compatible candidates exist |
| TIMERULE.INPUT_ERROR | terminal | 6 | terminal | none | TIMERULE.VALIDATE_REQUIREMENTS | stop | Input validation fails |
| TIMERULE.LOOKUP_ERROR | terminal | 7 | terminal | none | TIMERULE.FIND_MATCH | stop | Export lookup fails |
| TIMERULE.DEPENDENCY_ERROR | terminal | 8 | terminal | none | TIMERULE.CREATE_DEPENDENCY | stop | Conditional creation cannot proceed |
| TIMERULE.CONTRACT_GATE | decision | 9 | execution_gate | contract_ready->TIMERULE.CREATION_HANDOFF_READY;contract_missing->TIMERULE.CONTRACT_BLOCKED | TIMERULE.CREATE_DEPENDENCY | TIMERULE.CONTRACT_BLOCKED | Conditional creation reaches the execution boundary |
| TIMERULE.CREATION_HANDOFF_READY | terminal | 10 | terminal | none | TIMERULE.CONTRACT_GATE | stop | An approved creation handoff contract is available; live creation remains external to this task graph |
| TIMERULE.CONTRACT_BLOCKED | terminal | 11 | terminal | none | TIMERULE.CONTRACT_GATE | stop | Live Time Rule creation is not authorized by a documented contract |

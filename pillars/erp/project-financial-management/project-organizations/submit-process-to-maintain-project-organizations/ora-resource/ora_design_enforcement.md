# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Fixed payload | Prepare only OrgDenormJob, FscmEss, PJF; omit requestParameters |
| 2 | Approval | Display exact target and payload; bind approval to canonical JSON hash |
| 3 | Submission | Freeze approved payload in memory and submit once through core functions |
| 4 | Receipt | Save and verify returned ID before polling |
| 5 | Monitoring | Poll same ID to terminal status; resume supplied ID without POST |
| 6 | Failure | Preserve diagnostics and never automatically replay |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Blocker | | Any payload field conflicts with the fixed three-field contract or requestParameters is present | Reject supplied parameters and conflicting fields | No automatic fix |
| Submit | Blocker | verify_ess_approval | Explicit target/payload approval missing or mismatched | Show exact preview and obtain approval | Yes |
| Any execution | Blocker | verify_ess_execution | Receipt path occupied or acceptance cannot be saved and verified | Preserve evidence and allocate a fresh path for resume | No automatic fix |
| Resume | Blocker | track_existing_ess_request | Request ID or returned job identity mismatches | Stop and reconcile the saved identity | No automatic fix |
| Completion claim | Blocker | track_existing_ess_request | Only HTTP acceptance or nonterminal status exists | Monitor same request; terminal success alone completes this task | Yes |
| Failure, timeout or uncertain submission | Blocker | | Automatic replay or token-refresh POST retry is proposed | Preserve ID; resume or reconcile through active workflow | No automatic fix |
| Execution route | Blocker | | Generic retrying core main or another job is selected | Use task wrapper delegating to core functions | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_ess_approval | Submit | Exact target, payload and approval hash | ora_reference_lookups.md |
| verify_ess_execution | Every execution | Unused output paths and saved ID | ora_reference_lookups.md |
| track_existing_ess_request | Resume or monitoring | Same request ID, job identity and status | ora_reference_lookups.md |

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPO.ENFORCE_DESIGN | decision | 5 | design_enforcement | pass->MPO.EXECUTION_GATE;blocked->MPO.RETURN_REFUSAL;failure->MPO.RETURN_ISSUES | MPO.RESOLVE_DEPENDENCIES | stop | Before submission, resumed polling, or a completion claim |

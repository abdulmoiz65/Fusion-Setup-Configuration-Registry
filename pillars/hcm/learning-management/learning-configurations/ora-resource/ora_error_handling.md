# Learning configuration errors and execution boundary

Source: FDD GB-10–16 and governance/error-handling-guidelines.md. Task nodes
validate readiness only; the selected runbook/provider must separately own any
approved mutation and reconciliation. No endpoint or payload is authored here.

## Error Situations

| Task Code | Task Name | Situation | What Should Happen |
|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Missing user information | Ask a focused question for the affected attribute; preserve accepted inputs and independent work |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Required execution contract absent | TBD: supported read/write adapter, operation schema, exact privileges and readback binding; report contract unresolved and no side effect |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Uncertain prior mutation | Reconcile the original operation through its approved reader; never automatically resubmit |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Missing user information | Ask a focused question for the affected attribute; preserve accepted inputs and independent work |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Required execution contract absent | TBD: supported read/write adapter, operation schema, exact privileges and readback binding; report contract unresolved and no side effect |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Uncertain prior mutation | Reconcile the original operation through its approved reader; never automatically resubmit |

## Error Classifications

| Task Code | Task Name | Result Category | When Used | Next Action |
|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | input_validation | Missing, invalid, duplicate-conflicting or unreadable input | Identify row/field and correction; exclude invalid delta |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | catalog_or_metadata_mismatch | Missing task contract or unsupported export/import | Record exact owner gap; no alternative route |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | auth_expired_or_invalid; authorization_or_privilege | Expired session or denied operation | Follow selected provider refresh once where allowed; otherwise require authentication or privilege evidence |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | transport_or_environment; fusion_api_error | Read/service failure | Preserve sanitized status; bound read-only retries; never infer absent configuration |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | process_timeout; process_failed | Approved process handoff nonterminal or failed | Stop at timeout; report job/request/status/elapsed/next check; retrieve permitted ProcessLog on failure |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | artifact_persistence; approval_blocker | Unsafe output or missing exact approval | Stop affected operation; preserve sanitized progress and request corrective action |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | input_validation | Missing, invalid, duplicate-conflicting or unreadable input | Identify row/field and correction; exclude invalid delta |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | catalog_or_metadata_mismatch | Missing task contract or unsupported export/import | Record exact owner gap; no alternative route |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | auth_expired_or_invalid; authorization_or_privilege | Expired session or denied operation | Follow selected provider refresh once where allowed; otherwise require authentication or privilege evidence |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | transport_or_environment; fusion_api_error | Read/service failure | Preserve sanitized status; bound read-only retries; never infer absent configuration |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | process_timeout; process_failed | Approved process handoff nonterminal or failed | Stop at timeout; report job/request/status/elapsed/next check; retrieve permitted ProcessLog on failure |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | artifact_persistence; approval_blocker | Unsafe output or missing exact approval | Stop affected operation; preserve sanitized progress and request corrective action |

## Disclosure Rules

| Task Code | Task Name | Gate | What Must Be Shown |
|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Execution readiness | Task/environment; full inventory then exact delta; provider-resolved create/update/unchanged counts or unresolved counts; validation gaps; approval of exact target/operation/payload or immutable artifact; no success without readback |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Execution readiness | Task/environment; full inventory then exact delta; provider-resolved create/update/unchanged counts or unresolved counts; validation gaps; approval of exact target/operation/payload or immutable artifact; no success without readback |

## Refusal Rules

| Task Code | Task Name | Situation | What Must Not Happen |
|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | Missing contract, failed preflight, stale approval or uncertain mutation | No invented endpoint/version/field/privilege/business object; no direct REST/browser/loader fallback; no unapproved mutation retry; no sensitive outputs in reusable skill |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | Missing contract, failed preflight, stale approval or uncertain mutation | No invented endpoint/version/field/privilege/business object; no direct REST/browser/loader fallback; no unapproved mutation retry; no sensitive outputs in reusable skill |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | LC.DEFAULTS.GATE | step | 6 | execution_gate | pass->LC.DEFAULTS.DONE;fail->RETURN_ISSUES | LC.DEFAULTS.DESIGN | stop | Return contract validation results; not permission to mutate |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | LC.DEFAULTS.DONE | terminal | 7 | terminal | none | LC.DEFAULTS.GATE | stop | Return validated task-rule evidence only; never claim a completed configuration mutation |
| CUSTOM_CONFIGURE_LEARNING_DEFAULTS | Configure Learning Defaults | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Report affected input/contract, impact, owner and one safe next action |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | LC.BACKGROUND.GATE | step | 6 | execution_gate | pass->LC.BACKGROUND.DONE;fail->RETURN_ISSUES | LC.BACKGROUND.DESIGN | stop | Return contract validation results; not permission to mutate |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | LC.BACKGROUND.DONE | terminal | 7 | terminal | none | LC.BACKGROUND.GATE | stop | Return validated task-rule evidence only; never claim a completed configuration mutation |
| CUSTOM_CONFIGURE_BACKGROUND_PROCESSING | Configure Background Processing | RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Report affected input/contract, impact, owner and one safe next action |

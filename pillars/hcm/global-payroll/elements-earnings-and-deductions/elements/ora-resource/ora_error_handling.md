# Elements Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Missing or invalid required input | Identify the exact field and value; stop before LDG lookup or HDL preparation. |
| LDG lookup yields zero or multiple exact names | Report no match or ambiguity; do not infer legislation from the LDG label. |
| Questionnaire has no matching combination or multiple matches | Report the four matching keys and request current target template evidence; do not choose a different template. |
| User has not confirmed every selected answer | Display missing questions; do not copy the catalog's example responses silently. |
| Data Loader live metadata or task validation fails | Report the exact supported header, attribute or response problem and stop before upload. |
| Fusion GET fails with auth/authz or transport error | Record environment and stage with redacted diagnostics. Refresh a cached token once only when the active workflow permits it. |
| Loader or Fusion process fails | Preserve available redacted status and ProcessLog through the routed project workflow. Do not replay an uncertain import without the Data Loader workflow's idempotency or approval rule. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Missing, malformed or unconfirmed user input. | Request the exact missing or corrected value. |
| Catalog mismatch | LDG, template selector or questionnaire has no unique match. | Supply current target evidence or correct the selector. |
| Auth/authz | Tenant lookup lacks an authorized session or privilege. | Use the active workflow's auth handling; stop if unresolved. |
| Transport/environment | Tenant unavailable or wrong environment. | Report environment and stage; use the workflow's safe retry policy. |
| Fusion API or process failed | Documented GET or routed loader reports failure. | Preserve redacted diagnostics and stop before another mutation. |
| Artifact persistence or approval blocker | Import artifact, project state, Run Book or approval is missing. | Complete the routed gate before submission. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Questionnaire confirmation | Selected LDG and legislation, classification/category combination, all nine applicable questions for the supplied example, and the user's proposed answers. |
| Loader handoff | Exact target environment, operation, validated immutable HDL artifact, unresolved metadata if any, and the Data Loader workflow's own approval state. |
| Failure | Stage, failure class, affected field or question, sanitized message and safe next action; do not expose tokens, credentials, opaque URLs or sensitive payloads. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| No questionnaire match | Do not synthesize RuleCode, Rule or Response. |
| Missing current metadata | Do not assert that the supplied example proves universal field requiredness, accepted values or update semantics; require the Data Loader live preflight. |
| Missing routed submission preflight | Do not use a direct REST write, browser workaround or raw HDL upload as a substitute. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ELE.HDL_GATE | decision | 8 | execution_gate | ready->ELE.RETURN_PREPARED;blocked->ELE.HANDLE_ERROR | ELE.CHECK_DESIGN | stop | Require confirmed answers and active Run Book, then hand off to core.data-loader for live metadata preflight and exact-artifact approval. This gate does not submit HDL. |
| ELE.HANDLE_ERROR | step | 9 | error_handler | reported->ELE.RETURN_ISSUES | none | stop | Classify missing input, no-match, ambiguity, auth/transport, metadata and approval blockers with redacted guidance. |
| ELE.RETURN_ISSUES | terminal | 10 | terminal | none | none | stop | Return blocking issue and one safe next action. |
| ELE.RETURN_PREPARED | terminal | 11 | terminal | none | ELE.HDL_GATE | stop | Return a validated handoff to core.data-loader; only that workflow may approve and submit HDL. |

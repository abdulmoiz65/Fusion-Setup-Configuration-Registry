# Policy Profiles Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Policy Profiles metadata preflight is unavailable, fails, or identifies another business object | Stop before preparing a Data Loader operation. Report the sanitized preflight status and rerun the metadata preflight after correcting the reported issue. |
| PolicyType is not static value 1 or 2 | Stop and request PolicyType 1 for the Min-Max Planning UI option or 2 for the PAR UI option. |
| Max Qty Calculation Method returns no active exact match or multiple active exact matches | Stop and request an exact active LookupCode or Meaning from ORA_MSC_ROP_MAX_CALC_METHOD. |
| Safety Stock Calculation Method returns no active exact match or multiple active exact matches | Stop and request an exact active LookupCode or Meaning from ORA_MSC_ROP_SS_METHOD. |
| Authentication or authorization fails during a calculation-method lookup | The selected REST client may refresh a rejected cached token once for HTTP 401 or 403; otherwise stop and report the sanitized failure. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Auth/Authz | Authentication or authorization prevents the metadata preflight or live lookup. | Correct the configured authentication or privileges; do not retry beyond the REST client's one 401 or 403 refresh. |
| Fusion API | The live lookup returns a non-success response after authentication. | Stop and capture the sanitized response status and endpoint. |
| Input Validation | PolicyType, MaxCalcMethod, or SsCalcMethod has no unique documented match. | Request one valid exact value. |
| Approval Blocker | Metadata preflight is unavailable before a Data Loader operation. | Rerun the preflight; do not use a direct REST write fallback. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Metadata preflight failure | Business object minMaxPolicyProfiles, target-environment preflight status, and the safe corrective action; never disclose credentials or tokens. |
| Lookup failure | Lookup type ORA_MSC_ROP_MAX_CALC_METHOD or ORA_MSC_ROP_SS_METHOD, whether the result was zero or ambiguous, and the requested exact business value. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Metadata preflight is unavailable or fails | Do not prepare a Data Loader operation or bypass it with a direct REST write. |
| Policy Type, Max Qty Calculation Method, or Safety Stock Calculation Method lacks a unique documented match | Do not infer a value, default it, clear another value, or apply conditional UI behavior. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PP.STOP_METADATA | step | 6 | error_handler | handled->PP.BLOCKED_METADATA | none | stop | PP.CHECK_METADATA returns unavailable |
| PP.STOP_LOOKUP | step | 7 | error_handler | handled->PP.BLOCKED_LOOKUP | none | stop | A PolicyType mapping, MaxCalcMethod lookup, or SsCalcMethod lookup returns invalid, not_found_or_ambiguous |
| PP.COMPLETE | terminal | 8 | terminal | none | PP.LOOKUP_SAFETY_STOCK_METHOD | stop | Every supplied selected mapping or lookup succeeds, and omitted fields were explicitly skipped |
| PP.COMPLETE_NOT_APPLICABLE | terminal | 9 | terminal | none | PP.SELECT_REQUEST | stop | PolicyType, MaxCalcMethod, and SsCalcMethod are all absent |
| PP.BLOCKED_METADATA | terminal | 10 | terminal | none | PP.STOP_METADATA | stop | Metadata preflight is unavailable |
| PP.BLOCKED_LOOKUP | terminal | 11 | terminal | none | PP.STOP_LOOKUP | stop | A supplied mapping or lookup value is invalid, missing, or ambiguous |

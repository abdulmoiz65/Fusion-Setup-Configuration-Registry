# Benefit Reporting Groups Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Optional LOV request returns 403 | Do not throw a field-validation error; record unverified_forbidden for that supplied field and continue other independent checks. |
| Optional LOV returns no exact match or multiple distinct matches | Record invalid or ambiguous against the precise field and child-row index; do not select a near match. |
| A reportingGroupForProgramsOrPlans row contains both ProgramName and PlanName | Classify as input_validation and stop that row before resolving either LOV. |
| A date-effective row lacks its required date or effectiveOf cannot be derived | Classify as input_validation; default an omitted create, update, or correction EffectiveEndDate to 4712/12/31, but require an explicit end date for an End date operation. |
| A date-effective lookup cannot be evaluated as of its row's EffectiveStartDate | Classify as catalog_mismatch or fusion_api, preserve the row-specific failure, and do not use a current-date lookup. |
| Parent or child shape is malformed | Classify as input_validation and stop artifact preparation. |
| Current HDL schema, child section, key, or operation is unconfirmed | Classify as catalog mismatch; keep the load blocked until metadata confirms the contract. |
| A live submission or job has an uncertain outcome | Preserve redacted status evidence and stop; do not retry a mutation automatically. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | Malformed record tree or known invalid value | Correct the exact field and rerun preflight. |
| catalog_mismatch | Object, child section, field, or loader support differs from current metadata | Resolve against selected-environment metadata before artifact construction. |
| auth/authz | A lookup returns 403, or a 401 persists after one permitted cached-token refresh | Retain unverified_forbidden for a 403 field; resolve privilege or use another workflow-approved authoritative verification before load. |
| transport/environment | The selected endpoint or environment is unavailable | Stop the affected lookup and retain its unknown status. |
| fusion_api | Fusion returns a non-auth API error | Capture sanitized response details and correct the request or source. |
| process_timeout | A submitted job exceeds bounded polling | Report environment, operation, task code, process ID, last status, elapsed wait, and next-check path. |
| process_failed | A submitted job fails | Retrieve and persist available ProcessLog and status; report partial successes and errors. |
| artifact_persistence | Required project output or diagnostic cannot be written | Stop before submission and repair the workspace path. |
| approval_blocker | Run Book or loader approval is absent, stale, or tied to a different target or artifact | Do not submit. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation result | Each supplied field's path, child-row index, status, and safe correction; distinguish invalid from unverified_forbidden. |
| Live readiness | Exact environment, operation, immutable artifact, active Run Book state, metadata result, unresolved references, and loader approval state. |
| Failure diagnostic | Status, stage, failure class, message, recommended action, environment, artifact references, and external IDs under the project workspace; redact secrets and sensitive payloads. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| 403 from a conditional lookup | Do not throw a validation error, treat it as no match, or claim that the value was verified. |
| Unsupported or uncertain HDL contract | Do not hand-build or submit a guessed HDL file, replace the route with direct REST, or discard a child collection. |
| Live mutation fails or its outcome is uncertain | Do not retry without idempotency or new explicit approval under the loader workflow. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_RPTG.HANDLE_ISSUE | step | 120 | error_handler | handled->BEN_RPTG.RETURN_ISSUES | none | stop | A field is invalid or a blocking preflight condition occurs |
| BEN_RPTG.RETURN_RESULT | terminal | 130 | terminal | none | BEN_RPTG.EVALUATE | stop | Return field-level validation results and unresolved 403 statuses; this is not load approval |
| BEN_RPTG.RETURN_ISSUES | terminal | 140 | terminal | none | BEN_RPTG.HANDLE_ISSUE | stop | Return blocking issues and safe next actions |

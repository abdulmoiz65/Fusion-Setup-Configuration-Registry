# Enrollment Authorizations Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| The operation is missing, unsupported, or mapped to an object other than benefitLegalDisclaimers | Classify as input_validation and stop before preflight. |
| The current sample does not support the requested action, identity, schema, or date behavior | Classify as catalog_or_metadata_mismatch and stop; do not infer a replacement header, user key, or RestAction. |
| The DAT or ZIP is empty, malformed, changed, unvalidated, or named with an unsupported discriminator | Classify as input_validation and stop before upload or initiation. |
| A supplied StartDate or EndDate cannot be represented as a date-only YYYY-MM-DD value | Classify as input_validation and stop before artifact preparation; obtain an unambiguous date-only value. |
| A conditional ProgramName or PlanName LOV returns 403 | Record unverified_forbidden only for that row and field; do not throw a field-validation error or mark it invalid. Continue independent checks; require authoritative verification before live load. |
| A conditional name LOV returns zero or multiple distinct exact matches | Record invalid or ambiguous for the affected field; do not choose a candidate or rewrite the supplied name. |
| Authentication or authorization fails during preflight, upload, or initiation | Classify as auth_authz; refresh a cached token once only for an allowed read, and do not retry a write without new approval. |
| Upload or initiation has an uncertain outcome | Classify as approval_blocker; preserve sanitized evidence, reconcile through the selected read-only status route, and do not retry automatically. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | The operation, object route, identity, filename, schema, or artifact is invalid | Correct the identified source input and rerun preflight. |
| catalog_or_metadata_mismatch | The live sample does not support the selected action or source shape | Resolve the current metadata gap; do not infer a replacement route. |
| auth_authz | Authentication or privileges prevent the selected action | Confirm environment access and required privileges before a new request. |
| unverified_forbidden | A conditional ProgramName or PlanName lookup returned 403 | Keep field validation nonfailing; verify the name authoritatively before live load. |
| approval_blocker | Approval is missing, stale, or the prior write outcome is uncertain | Do not upload, initiate, or retry without current approval for the exact artifact. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preflight failure | Failure class, failed stage, selected operation, selected HDL object, and corrective action. |
| Reference validation | Each supplied ProgramName or PlanName field's row reference, status, and safe correction; distinguish invalid, ambiguous, and unverified_forbidden. |
| Any diagnostic | Sanitized artifact references and external identifiers only; never credentials, tokens, private keys, or full payload values. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| The request uses a task label, guessed REST resource, or another object in place of benefitLegalDisclaimers | Do not remap or submit it. |
| The live sample does not establish the requested action, identity, or schema | Do not invent a DAT header, key, date format, or RestAction. |
| An update or delete has an ambiguous identity | Do not submit a broad or guessed mutation. |
| A mutation fails or has an uncertain outcome | Do not automatically retry the upload or initiation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ENROLL_AUTH.GATE_EXECUTION | decision | 20 | execution_gate | approved->ENROLL_AUTH.READY_FOR_EXECUTION;blocked->ENROLL_AUTH.HANDLE_ISSUE | ENROLL_AUTH.LOOKUP_PLAN | stop | Confirm approval is bound to the environment, operation, benefitLegalDisclaimers object, and preflighted immutable artifact; unverified_forbidden must be authoritatively resolved before live load |
| ENROLL_AUTH.HANDLE_ISSUE | step | 90 | error_handler | handled->ENROLL_AUTH.RETURN_ISSUES | none | stop | A validation, metadata, authentication, approval, or load failure blocks progress |
| ENROLL_AUTH.READY_FOR_EXECUTION | terminal | 100 | terminal | none | ENROLL_AUTH.GATE_EXECUTION | stop | Every documented gate passed; ready for the selected core.data-loader workflow |
| ENROLL_AUTH.RETURN_ISSUES | terminal | 110 | terminal | none | none | stop | A blocking issue was safely disclosed |

# Job Requisition Descriptive Flexfields Error Handling

Classify task-local failures, preserve sanitized diagnostics, and stop before retry. This guidance does not authorize setup execution, imports, REST writes, or production access.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Request targets another FSM page | Stop and route to the correct task |
| DFF identity, requested operation, or change scope is ambiguous | Stop and request the exact missing detail |
| Task catalog does not confirm the exact offering, functional area, or task code | Stop; do not substitute a generic DFF task or alternate route |
| LOV or value-set contract is undocumented | Stop before preview, import, export, activation, or Fusion access |
| Exact Fusion privilege is undocumented | Keep the privilege unresolved and route access verification to the security owner; read-only task export may continue only when the selected workflow already has authorized access |
| Access is missing or a 401 or 403 occurs | Stop and route to the security owner; allow one cached-token refresh only when the selected workflow permits it |
| A transport or environment failure occurs | Stop and preserve sanitized diagnostics; retry only through the selected workflow when the failure is known to be recoverable |
| An import fails | Preserve the process log and row errors; correct the source and obtain a new preview and approval before resubmission |
| A mutation outcome is uncertain | Do not retry automatically; reconcile through the approved task workflow |
| Automated post-import verification is requested without a documented action | Report the verification contract as unresolved; use approved manual setup verification until a supported action is documented |
| A fresh read-only task CSV export cannot be created, downloaded, extracted, or validated | Return BLOCKED with the exact failed export stage; do not use an older export or fall back to a browser, direct REST, or DFF API |
| A Global segment result includes context-sensitive rows | Remove the contextual rows, retain only Global Data Elements rows, and revalidate the result before presentation |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| INPUT_VALIDATION | Another page is targeted or operation, DFF identity, or change scope is missing or ambiguous | Correct the exact request scope |
| CATALOG_MISMATCH | The catalog does not confirm the exact offering, functional area, or task code | Correct the catalog or generated task context; do not substitute another route |
| LOOKUP_CONTRACT | The LOV or value-set authority is undocumented or unresolved | Obtain the authoritative contract |
| AUTH_AUTHZ | A required privilege is unknown, access is missing, or a 401 or 403 occurs | Route to the security owner |
| TRANSPORT_ENVIRONMENT | The selected workflow cannot reach or use the target environment | Preserve diagnostics and route to the environment owner |
| PROCESS_FAILED | The FSM import reports failure | Preserve the process log and row errors; correct, re-preview, and obtain new approval |
| EXECUTION_BLOCKER | A mutation result is uncertain or the selected execution workflow is unconfirmed | Reconcile through the approved task workflow without retry |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input or catalog rejection | Exact task identity, missing or mismatched scope, and one safe correction |
| Lookup blocker | Resolver, missing authoritative contract fields, and the functional-owner next action |
| Authorization or transport failure | Sanitized failure class, selected workflow stage, responsible owner, and safe next action |
| Import failure | Environment, task, import request identifier when available, total, loaded, and failed counts, process-log reference, and correction path |
| Uncertain mutation | Exact target, operation, last known status, sanitized evidence, and reconciliation action |
| Verification | Exact DFF, context, segment, expected attributes, approved manual evidence, and any unresolved verification item |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A generic Common DFF task or another FSM page is proposed | Do not substitute it for Job Requisition Descriptive Flexfields |
| Direct REST transport or an alternate import path is proposed | Do not bypass core.fusion-api.apps-common.descriptive-flexfields or Core Data Loader |
| Unrelated DFF attributes, inferred contexts, or inferred segments are proposed | Do not add them to the requested change |
| Required privileges or automated post-import verification remain undocumented | Do not invent them; keep them unresolved and use the named owner or manual verification path |
| Inspect or list is requested without a valid fresh task export | Do not return stale, cached, reconstructed, browser-scraped, direct REST, or direct DFF API data |
| Approval is absent, stale, or bound to another preview | Do not mutate Fusion |
| Import failed or the mutation outcome is uncertain | Do not retry automatically |
| Credentials, tokens, customer data, personal data, or production-only values are observed | Do not persist or disclose them |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JOB_REQ_DFF.APPROVAL_GATE | decision | 50 | execution_gate | approved->JOB_REQ_DFF.EXECUTE;not_required->JOB_REQ_DFF.EXECUTE;missing->JOB_REQ_DFF.RETURN_ISSUES;stale->JOB_REQ_DFF.RETURN_ISSUES | JOB_REQ_DFF.ENFORCE_DESIGN | stop | Require approval bound to the current immutable preview immediately before a state-changing handoff; read-only inspection, planning, export, and validation use not_required |
| JOB_REQ_DFF.EXECUTE | decision | 60 | execution_gate | completed->JOB_REQ_DFF.RETURN_SUCCESS;failed->JOB_REQ_DFF.RETURN_ISSUES;uncertain->JOB_REQ_DFF.RETURN_ISSUES;unsupported->JOB_REQ_DFF.RETURN_ISSUES | JOB_REQ_DFF.APPROVAL_GATE | stop | Complete a supported read-only action from validated evidence, or hand an approved immutable FSM archive to Core Data Loader; never bypass the selected route or retry an uncertain mutation |
| JOB_REQ_DFF.RETURN_SUCCESS | terminal | 90 | terminal | none | JOB_REQ_DFF.EXECUTE | stop | A supported non-mutating action completed with verified evidence |
| JOB_REQ_DFF.RETURN_ISSUES | terminal | 99 | terminal | none | none | stop | Any failure, refusal, missing input, ambiguity, authorization failure, blocked dependency, stale approval, or uncertain result |

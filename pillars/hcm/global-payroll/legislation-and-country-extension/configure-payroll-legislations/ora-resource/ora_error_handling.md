# Configure Payroll Legislations Error Handling

## Evidence Matrix

| Claim or Contract | Source | Source Type | Evidence Status | Release or Date | Limitation |
|---|---|---|---|---|---|
| FSM template contract | Configure Payroll Legislations FSM template package and metadata | Target-environment FSM template | Observed | Fusion release 11.13.26.10.0; exported 2026-08-12 | Does not include a task-specific import ProcessLog or error response. |
| Stop-before-retry and approval gate | User implementation direction and core.data-loader | Implementation policy | Confirmed | 2026-08-13 | Does not authorize a retry or an import. |

## Error Situations

| Situation | What Should Happen |
|---|---|
| Requested FSM operation is not specified | Return MISSING_OPERATION and request export or import. |
| A value or data transformation has no explicit functional source | Return MISSING_FUNCTIONAL_INPUT and stop package preparation. |
| A requested HCM-product default set differs from the documented baseline | Return DEFAULT_SET_MISMATCH and stop package preparation. |
| A requested payroll-relationship-rule default set differs from the documented baseline | Return DEFAULT_SET_MISMATCH and stop package preparation. |
| A requested balance-dimension default set differs from the documented baseline | Return DEFAULT_SET_MISMATCH and stop package preparation. |
| A requested balance-type default set differs from the documented baseline or populates a confirmed blank CurrencyCode cell | Return DEFAULT_SET_MISMATCH and stop package preparation. |
| A requested component-group default set differs from the documented baseline | Return DEFAULT_SET_MISMATCH and stop package preparation. |
| A requested element-classification default set differs from the documented baseline | Return DEFAULT_SET_MISMATCH and stop package preparation. |
| A requested payment-type default set differs from the documented baseline | Return DEFAULT_SET_MISMATCH and stop package preparation. |
| A CSV filename, header, order, or data type differs from the task template | Return PACKAGE_CONTRACT_MISMATCH and do not create an immutable preview. |
| Metadata identifies a different task or lacks the required task identity | Return TASK_CONTRACT_MISMATCH and do not reuse a cross-task package. |
| An attempted import alters values beyond explicit user-supplied source content and documented defaults | Return UNSUPPORTED_TRANSFORMATION and request explicit functional direction. |
| A REST query or mutation is proposed | Return UNSUPPORTED_REST_ROUTE; the selected route is FSM only. |
| Final archive changes after its validation or preview | Return STALE_ARCHIVE and restart package validation, Task Hook validation, hash display, and approval. |
| Approval is missing or is not the later standalone message exactly approve | Return APPROVAL_REQUIRED and stop before upload or initiation. |
| FSM import reports a failure | Preserve sanitized process status and ProcessLog when available; stop before retry and correct the documented source issue. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING_OPERATION | The FSM export or import action is unclear | Specify one FSM action. |
| MISSING_FUNCTIONAL_INPUT | Supplied values or requested transformation have no functional source | Provide the missing source or functional decision. |
| DEFAULT_SET_MISMATCH | A documented default set does not match its required row count, values, blank cells, or source SHA-256 when one is documented | Restore the confirmed baseline or supply explicit user rows. |
| PACKAGE_CONTRACT_MISMATCH | File structure or fields differ from the target template | Restore the exact template contract. |
| TASK_CONTRACT_MISMATCH | Metadata targets another task | Export or regenerate the target task package. |
| UNSUPPORTED_TRANSFORMATION | Source values would be inferred, cloned, filtered, renamed, or replaced without authority | Provide explicit functional direction or an authoritative FSM archive. |
| UNSUPPORTED_REST_ROUTE | A REST route is selected | Use the FSM workflow only. |
| STALE_ARCHIVE | A reviewed or approved archive changed | Revalidate and obtain a new approval. |
| APPROVAL_REQUIRED | Import approval has not been received in the required form | Show the immutable archive hash and wait for exactly approve. |
| PROCESS_FAILED | Fusion reports import failure | Review the sanitized process diagnostic; do not retry automatically. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Package contract failure | Missing, unexpected, or mismatched file, header, type, or task identity; never expose credentials or source row values unnecessarily. |
| Functional blocker | The missing source or transformation authority and why the package cannot be prepared. |
| Immutable approval gate | Final ZIP location, SHA-256, validation result, and the required standalone approval text. |
| FSM process failure | Environment identity, operation, task code, process or request identifier when available, last status, sanitized ProcessLog or error, and safe next action. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| No functional source supports a value or transformation | Do not invent a value, default, operation, business key, dependency, or row transformation. |
| A package differs from the target task template | Do not normalize, map, or substitute another task's files. |
| REST is proposed | Do not call or document REST as an execution or lookup route. |
| Approval is absent or archive bytes changed | Do not upload, initiate, retry, or re-use approval. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CPL.COMPLETE | terminal | 5 | terminal | none | CPL.ENFORCE_FSM_CONTRACT | continue | The selected FSM operation has passed every applicable validation, readiness, defaulting, and FSM design gate |
| RETURN_ISSUES | terminal | 6 | terminal | none | none | continue | Any validation, readiness, contract, design, or approval issue |

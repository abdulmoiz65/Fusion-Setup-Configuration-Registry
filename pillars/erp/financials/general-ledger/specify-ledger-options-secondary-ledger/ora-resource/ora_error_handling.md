# Specify Ledger Options Secondary-Ledger Error Handling

Failures are classified at the stage where they occur, disclosed without secrets, and stopped before an unsafe retry. A read error never becomes a not-found result, and an uncertain import never becomes permission to submit again.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Mandatory period, future count, retained earnings, or confirmation is absent | Stop before preview and name the exact missing value or confirmation. |
| AccountingMethodName is omitted or names Standard Accrual | Continue without a method code/type or language question, retain STANDARD_ACCRUAL and S, and resolve the controlled English language default to Fusion's authoritative enabled code. |
| Fusion returns GL-781444 because journal description language is blank while a subledger accounting method is assigned | Preserve the failed process/package, reconcile partial mutation, and consume the approval. Apply the controlled English business default, resolve the unique enabled English base-language row through languagesLOV, write its returned code, rebuild, re-preview, and require fresh approval. Never write literal EN or US unless returned by Fusion. |
| AccountingMethodName explicitly names another method | Keep Standard Accrual in the FSCR package, disclose the manual change in this UI, and block Review and Submit readiness until re-export verifies it. |
| User supplies physical accounting-method fields | Reject unsupported direct tuple intake and preserve the controlled create policy. |
| A conditional option trigger lacks its dependent account or setup | Block that requested feature and state whether baseline can continue with a required UI handoff. |
| Exact lookup returns zero or many eligible rows | Report not found or ambiguity with resolver, exact supplied raw business key, eligibility filter, and safe correction. |
| Lookup returns 401 or 403 | Refresh an existing cached token once when permitted and retry the identical GET once; if still failing, report auth or authz. |
| Read returns timeout, 429, or 5xx | Retry only the idempotent GET with bounded backoff, then report transport or Fusion API failure. |
| HTTP 400 or Oracle 29140 | Classify a resolver-contract or input-validation failure from the actual response, preserve the sanitized q and response, and stop. Invalid attributes and malformed expressions are not value-not-found outcomes; never retry the identical invalid q. |
| Client, paging, serialization, or other HTTP failure | Preserve original class and sanitized response; never report value not found. |
| Oracle rejects retained earnings or another account | Report account role, combination, semantic predicate, and product code or message, then request a role-valid account. |
| Secondary-to-primary parent evidence is absent or ambiguous | Stop before export and request the exact primary-secondary pair or a valid Manage Secondary Ledgers relationship receipt. Never infer the parent from shared COA, calendar, currency, or similar names. |
| Scoped GL_SPECIFY_LEDGER_OPTIONS export criteria are missing or rejected | Stop before package editing and show the resolved SourcePrimaryLedgerId plus the required GL_PRIMARY_LEDGER, Set1, PRIMARY_LEDGER_ID criterion. Do not scope by SecondaryLedgerId or fall back to a template-only, unscoped, or project-owned create package. |
| Scoped populated export is header-only, overbroad, stale, wrong-parent, or missing the target secondary | Classify input validation, catalog mismatch, or Fusion process failure as observed; preserve the export receipt and reacquire only through the same exact parent-primary scope. |
| accountCombinationsLOV response cannot expose the complete dynamic segment values | Classify a response-contract gap and stop. Do not trigger a value-set or other export, infer equality from CCID alone, or use a partial account match. |
| accountCombinationsLOV returns zero exact retained-earnings rows after complete COA-scoped pagination | Pause Specify Ledger Options and route GL_MANAGE_ACCOUNT_COMBINATIONS through Import Account Combinations FBDI under core.data-loader. That workflow must create its own immutable artifact, validation, preview, and approval gate. After terminal success, rerun the identical LOV query; do not continue from an import request ID alone. |
| Manage Account Combinations FBDI load or import fails, warns, times out, or has an uncertain result | Keep Specify Ledger Options blocked, preserve the Data Loader result, and follow the FBDI workflow's diagnostic and resume contract. Never submit another combination file from this task. |
| Post-creation accountCombinationsLOV re-query still returns zero or many exact rows | Report verification failure and keep options authoring blocked; do not synthesize or reuse an expected CCID. |
| Fusion returns `GL_ASM_INVALID_RET_EARN_TYPE` although exact lookup evidence proves an eligible balance-sheet retained-earnings account | Preserve the failed package and process evidence, re-export to prove whether any partial options mutation occurred, then inspect the physical `RetEarnCcidSegments` vector. Treat CCID, hyphen display, literal `\n`, CRLF, wrong slot count, missing terminal LF, reordered segments, or alias divergence as serialization failure; never replay the package. Rebuild, preview, and obtain fresh approval. |
| Package scope, context, member, header, alias, or manifest differs | Stop as input validation or catalog mismatch and obtain a fresh populated task export scoped by the parent PrimaryLedgerId. |
| Preview changes a relationship, rule, root, BSV, unrelated ledger, or inherited field | Reject the package and rebuild the secondary-row-only delta. |
| Explicit approval is absent or stale | Stop as approval blocker; do not import. |
| Import request or process fails | Do not retry automatically; preserve sanitized status, log, partial successes, errors, and resume stage. |
| Process status is unknown or polling times out | Stop and report environment, operation, task code, process or request identity, last status, elapsed wait, and next-check path. |
| Re-export does not prove the intended option delta | Report process failed or verification failure and do not claim readiness. |
| Diagnostic or artifact persistence fails | Report artifact persistence with safe intended path; do not disclose credentials or sensitive payloads. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Missing, unconfirmed, malformed, out-of-range, invalid account segment shape, missing exact CCID, incomplete dynamic LOV response, role-invalid, ambiguous English resolver, or trigger-incomplete input | Correct the exact field, complete the routed account-combination workflow, or resolve the environment ambiguity and rerun. |
| Catalog mismatch | Wrong task context, export criterion, package, release, alias, scope, primary-secondary relation, or schema | Acquire matching authoritative evidence and rerun the parent-primary-scoped export. |
| Auth or authz | Token or privilege failure | Correct identity or privilege; do not reinterpret as missing value. |
| Transport or environment | Network, timeout, target identity, or environment failure | Verify target and retry only safe idempotent reads. |
| Fusion API | Oracle read or import rejects the request | Preserve sanitized code and message and stop. |
| Process timeout | Polling bound expires without final state | Use read-only reconciliation with recorded resume facts. |
| Process failed | Fusion process fails or re-export cannot prove the semantic delta | Preserve logs and fix root cause before new preview and approval. |
| Artifact persistence | Package, preview, diagnostics, or re-export cannot be stored safely | Correct the safe destination without exposing sensitive data. |
| Approval blocker | Exact preview has no current accountable approval | Obtain approval for the unchanged preview fingerprint. |

## Package Execution Gate

| Gate | What Must Happen |
|---|---|
| Acquire | Resolve the target secondary's parent, then use one fresh populated GL_SPECIFY_LEDGER_OPTIONS export scoped by that parent PrimaryLedgerId; block if unavailable. |
| Preflight | Validate environment identity, privileges, task context, exact GL_PRIMARY_LEDGER and PRIMARY_LEDGER_ID criterion, parent-secondary relation, package source, release, eleven members, headers, aliases, ZIP shape, safe paths, and approval requirements. |
| Preview | Show exact secondary row field deltas in both aliases, mandatory confirmations, field source classes, preserved values, UI handoffs, warnings, and zero relationship or rule mutations. |
| Approve | Bind accountable approval to the exact raw business scope, separately canonicalized numeric fields, and preview fingerprint. |
| Submit | Use the authorized task CSV executor once. No Task Node in this resource performs a direct REST write. |
| Monitor | Poll the external process to final state, retaining sanitized status and logs. |
| Verify | Re-export identical scope and compare option semantics, alias equality, inherited and optional preservation, service-generated values, and status. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation failure | Exact task context, secondary, field, trigger, supplied raw value, any separately documented numeric canonical form, violated rule, and correction. |
| Lookup failure | Resolver, business key, match count or failure class, eligibility criteria, and safe next action without credentials or protected payloads. |
| Preview | Exact changed members and fields, mandatory confirmations, source class, optional-family disposition, UI handoffs, and approval fingerprint. |
| Timeout or process failure | Environment, operation, task code, process or request identity, last status, elapsed time, sanitized log and status, partial successes, errors, and resume path. |
| Verification | Intended versus observed semantic delta, alias comparison, preserved relationship and rule state, and unresolved differences. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Mandatory value is only exported or displayed | Do not silently accept it without explicit confirmation. |
| Required input or exact identity is missing | Do not guess a value, select the first LOV row, or borrow another ledger's option. |
| Authorization, paging, HTTP, or client call fails | Do not say the value was not found. |
| Optional family was not requested | Do not ask for it, enable it, or overwrite the existing or disabled baseline. |
| Accounting method is omitted or another method is desired | Do not leave the newly created secondary tuple blank, copy the primary method, directly author the alternative tuple, or request its technical fields. |
| Retained-earnings CCID is absent | Do not synthesize an identifier, populate a nonexistent combination, call a direct create from this task, bypass the routed GL_MANAGE_ACCOUNT_COMBINATIONS FBDI preview and approval, or continue without the post-success LOV re-query. |
| Retained earnings needs existence validation | Do not trigger GL_MANAGE_CHART_OF_ACCOUNTS_VALUE_SETS or another export; use accountCombinationsLOV directly with the resolved StructureInstanceNumber and complete local segment matching. |
| Posting cutoff is requested without exact timezone contract | Do not author Y with blank timezone or assume UTC. |
| Package delta touches relationship or rules | Do not import from this task; route to Complete Primary to Secondary Ledger Mapping. |
| Preview is unapproved or live status is uncertain | Do not import, replay, activate, submit, enable conversion, or open a period. |
| Review and Submit is requested | Do not mutate lifecycle state; boundary GL-07 remains open. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SLOS-060-EXECUTION-GATE | decision | 60 | execution_gate | verified->SLOS-080-RETURN-VERIFIED;blocked->SLOS-070-HANDLE-ERROR;failed->SLOS-070-HANDLE-ERROR | SLOS-050-ENFORCE-DESIGN | stop | Always |
| SLOS-070-HANDLE-ERROR | step | 70 | error_handler | stopped->SLOS-090-RETURN-ISSUES | none | stop | A prior node returns an invalid, unresolved, blocked, or failed outcome |
| SLOS-080-RETURN-VERIFIED | terminal | 80 | terminal | none | SLOS-060-EXECUTION-GATE | stop | Identical-scope re-export proves the approved secondary-option delta |
| SLOS-090-RETURN-ISSUES | terminal | 90 | terminal | none | SLOS-070-HANDLE-ERROR | stop | Error handling has produced an actionable stop record |

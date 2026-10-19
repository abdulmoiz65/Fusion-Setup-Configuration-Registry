# Specify Ledger Options Primary-Ledger Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required or triggered input is missing or invalid | Identify the exact primary scope, retained-earnings, first-period, alternative-method display receipt, or triggered-family field and stop only the affected path; an omitted method is valid |
| Another accounting method is explicitly requested | Keep Standard Accrual in the FSCR package, disclose the manual post-create Specify Ledger Options change, and block Review and Submit readiness until same-scope re-export verifies the requested method |
| Fusion returns GL-781444 because journal description language is blank while a subledger accounting method is assigned | Preserve the failed package/process, reconcile partial mutation, and mark the approval consumed. Apply the controlled English business default, resolve the unique enabled English base-language row through languagesLOV, write its returned code, rebuild, re-preview, and require fresh approval. Never write literal EN or US unless Fusion returned that code |
| Scoped GL_SPECIFY_LEDGER_OPTIONS export criteria are missing or rejected | Stop before package editing and show the resolved PrimaryLedgerId plus the required GL_PRIMARY_LEDGER, Set1, PRIMARY_LEDGER_ID criterion. Do not fall back to a template-only, unscoped, or project-owned create package |
| Scoped populated export is header-only, overbroad, stale, or contains the wrong ledger | Classify input validation, catalog mismatch, or Fusion process failure as observed; preserve the export receipt and reacquire only through the same exact primary scope |
| accountCombinationsLOV response cannot expose the complete dynamic segment values | Classify a response-contract gap and stop. Do not trigger a value-set or other export, infer equality from CCID alone, or use a partial account match |
| accountCombinationsLOV returns zero exact retained-earnings rows after complete COA-scoped pagination | Pause Specify Ledger Options and route GL_MANAGE_ACCOUNT_COMBINATIONS through Import Account Combinations FBDI under core.data-loader. That workflow must create its own immutable artifact, validation, preview, and approval gate. After terminal success, rerun the identical LOV query; do not continue from an import request ID alone |
| Manage Account Combinations FBDI load or import fails, warns, times out, or has an uncertain result | Keep Specify Ledger Options blocked, preserve the Data Loader result, and follow the FBDI workflow's diagnostic and resume contract. Never submit another combination file from this task |
| Post-creation accountCombinationsLOV re-query still returns zero or many exact rows | Report verification failure and keep options authoring blocked; do not synthesize or reuse an expected CCID |
| Retained-earnings or optional role account fails semantic validation | Show the failed role predicates separately from structural validity and request a valid exact account |
| Fusion returns `GL_ASM_INVALID_RET_EARN_TYPE` after the account-combination lookup proved an eligible balance-sheet account | Preserve the failed package and process evidence, reconcile the target row to prove no partial options mutation, and inspect `RetEarnCcidSegments` encoding before blaming the business account. A CCID, hyphen-delimited display, literal `\n`, CRLF, wrong slot count, missing terminal LF, or reordered segment vector is a physical serialization failure. Never replay the package; rebuild, preview, and obtain fresh approval |
| Catalog, package, header, alias, multiline, or metadata mismatch | Classify catalog mismatch and re-acquire or rebase; do not repair physical shape by guess |
| No exact authoritative match after a successful complete read | Report value not found for the exact business value and resolver |
| Multiple exact matches | Report ambiguity and required disambiguation; never choose the first result |
| HTTP 401 or 403 | Classify auth or authorization, refresh an approved cached token once when applicable, retry the read once, and stop if still denied |
| HTTP 400 or Oracle 29140 | Classify a resolver-contract or input-validation failure from the actual response, preserve the sanitized q and response, and stop. Invalid attributes and malformed expressions are not value-not-found outcomes; never retry the identical invalid q |
| HTTP 429, 5xx, timeout, DNS, TLS, pagination, or client transport failure | Classify transport or Fusion API, use only bounded safe read retries, and disclose final status |
| Unsupported optional direct-CSV customization | Preserve the safe baseline, record the named UI handoff, and block Review readiness until re-export verifies completion |
| Preview changes a nonowning member, unrequested option, alias-only field, lifecycle field, or multiline serialization | Block approval and rebuild the smallest symmetric delta |
| Approval is absent or stale | Stop before import and request approval bound to the exact current preview |
| Import has an uncertain result | Do not resubmit; reconcile process status and identical-scope re-export first |
| Import polling times out | Report environment, GL_SPECIFY_LEDGER_OPTIONS, primary context, process or request identity, last status, elapsed wait, and safe next-check path |
| Import fails | Retrieve available ProcessLog and status evidence, preserve partial successes with an errors array and nonzero status, and stop before retry |
| Re-export differs | Show field-level semantic differences, alias parity, and UI-handoff state; metadata-only change is not proof |
| Artifact persistence fails | Stop and report the intended project artifact path without exposing protected data |
| Review, submit, activate, enable conversion, or open periods is requested | Classify approval blocker and stop under open item GL-07 |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Missing retained earnings, malformed account segment count/order, missing exact CCID, incomplete dynamic LOV response, triggered period, ambiguous English language resolver, malformed alternative-method display receipt, user-supplied physical method tuple/code, invalid range, or invalid cross-field combination | Correct the exact input or complete the routed account-combination workflow, then rerun validation; do not ask for method code/type or language when the controlled English resolver succeeds |
| Catalog mismatch | Task context, export criterion, package, member, header, alias, metadata, release, environment, or scope differs | Obtain a correct primary-scoped populated export; do not patch by assumption |
| Auth or authorization | Token is absent or expired, principal lacks privilege, or a read is denied | Refresh an approved cached token once for 401 or 403 when applicable, otherwise obtain privilege |
| Transport or environment | Timeout, DNS, TLS, connectivity, pagination transport, or wrong environment | Correct the condition and rerun only the safe read or validation stage |
| Fusion API | Oracle returns a service rejection, malformed response, or nontransient server failure | Preserve sanitized evidence and correct the documented cause |
| Process timeout | Import polling reaches the bounded wait without terminal state | Record last status and use the safe next-check path; do not submit again |
| Process failed | Import fails or verification proves a missing or partial requested result | Retrieve logs, preserve partial success, diagnose, and obtain fresh approval before a new import |
| Artifact persistence | Preview, diagnostic, registry, or verification cannot be saved safely | Correct the destination and persist before proceeding |
| Approval blocker | Approval is missing or stale, UI handoff is incomplete, or forbidden lifecycle mutation is requested | Stop and obtain the exact approval or complete the named UI flow |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Lookup failure | Resolver, non-sensitive scope and requested value, match count when available, failed role predicates, HTTP or client class, retries, and corrective action |
| Package preview | Environment, release, task and primary context, member inventory, checksums, row adds, updates and deletes, field source classes, account-role evidence, warnings, UI handoffs, and open-item scope |
| Approval | Exact preview fingerprint, package artifact, environment, release, primary scope, intended option changes, and approval invalidation rule |
| Import | Authorized executor, task and primary context, sanitized process or request identity, and submission time; no tokens or credentials |
| Timeout or failure | Environment, operation, task, context, process or request identity, last or final status, elapsed time, ProcessLog reference, partial-success errors, and safe next action |
| Re-export verification | Identical scope, requested option semantic diff, alias parity, preserved fields, UI completion, unintended changes, and final verdict |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Mandatory or triggered business input is absent | Guess retained earnings, first period, timezone, criteria set, legal entity, balancing value, or option account |
| Accounting method is omitted or another method is desired for the new ledger | Leave code/type blank, author the alternative tuple directly, request technical code/type/language code, or leave the options language blank instead of resolving the controlled English default |
| Retained-earnings CCID is absent | Synthesize an identifier, populate a nonexistent combination, call a direct create from this task, bypass the routed GL_MANAGE_ACCOUNT_COMBINATIONS FBDI preview and approval, or continue without the post-success LOV re-query |
| Retained earnings needs existence validation | Do not trigger GL_MANAGE_CHART_OF_ACCOUNTS_VALUE_SETS or another export; use accountCombinationsLOV directly with the resolved StructureInstanceNumber and complete local segment matching |
| Optional family is not requested | Ask it as a baseline question, enable it, or reset an existing value |
| Lookup or client fails | Return value not found for HTTP, authorization, pagination, parse, or transport failure |
| Account is structurally valid only | Accept it without required semantic role predicates |
| Posting cutoff requested | Enable it with a blank timezone or invent UTC |
| Automatic tax requested | Fabricate an internal legal-entity ID or bypass external prerequisites |
| Package shape differs | Reorder headers, omit aliases, flatten multiline fields, substitute a CCID or hyphen display for a segment vector, delete header-only members, rename the product-spelled member, or hand-invent metadata |
| Live import fails or is uncertain | Automatically retry or replay without idempotency evidence and fresh approval |
| Sensitive material is present | Persist or disclose tokens, credentials, private keys, protected payloads, or customer data |
| Review and Submit is requested | Author lifecycle state or submit, activate, enable conversion, or open periods |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SLOP.EXECUTION_GATE | decision | 60 | execution_gate | ready->SLOP.DONE;blocked->SLOP.HANDLE_ERROR;failure->SLOP.HANDLE_ERROR | SLOP.ENFORCE_DESIGN | stop | Require exact preview, current approval, authorized import, terminal monitoring, completion of every triggered UI handoff, and identical-scope re-export verification. |
| SLOP.HANDLE_ERROR | step | 70 | error_handler | disclosed->SLOP.FAILED | none | stop | Any validation, lookup, dependency, defaulting, design, UI-handoff, preview, approval, import, persistence, or verification stage fails or blocks. |
| SLOP.DONE | terminal | 80 | terminal | none | SLOP.EXECUTION_GATE | continue | The approved import and any triggered UI handoff completed, and re-export verified the requested primary options with no unintended change. |
| SLOP.FAILED | terminal | 90 | terminal | none | SLOP.HANDLE_ERROR | continue | The task stopped safely with an actionable classified error, UI requirement, or approval blocker. |

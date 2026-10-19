# Manage Primary Ledgers Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required user input is missing or invalid | Identify only the exact missing or invalid business fields, preserve the raw input for review, and stop before lookup or preview |
| Catalog, package, header, alias, or metadata mismatch | Classify catalog mismatch, show the expected and observed non-sensitive shape, and re-acquire or rebase instead of repairing by guess |
| No exact authoritative LOV match | Report the business value and resolver as value not found only after a successful complete read with zero exact eligible matches |
| Multiple exact authoritative matches | Report ambiguity and the safe disambiguation needed; never select the first match |
| Duplicate ledger exists | Report the exact non-sensitive conflicting ledger identity and stop before searching for reusable CoA evidence, submitting a CoA export, or submitting the Primary Ledger template export |
| Existing CoA export is stale, from another environment or release, header-only, or lacks the exact selected StructureInstanceCode | Reject that candidate, continue checking the current export inventory, and if no candidate qualifies route exactly one populated GL_MANAGE_CHARTS_OF_ACCOUNTS_STRUCTURE_INSTANCES export |
| CoA export role join fails | Report the exact member, missing or duplicate composite key, selected StructureInstanceCode, label cardinality, and missing ColumnName or instance ValueSetCode; never fall back to segment sequence, DefaultValueSetCode, REST describe, or an assumed SEGMENT position |
| Manage Primary Ledgers template is populated or has the wrong task identity | Reject it as an authoring carrier and route the exact template-only GL_MANAGE_PRIMARY_LEDGERS acquisition path after all reference dependencies pass |
| Export request returned no caller receipt but may have been accepted | Reconcile the known process inventory and persisted artifacts before another submission. If acceptance cannot be ruled out, classify the state as uncertain and stop rather than create a duplicate export job |
| Export-operation approval is absent or stale | Stop before the CoA populated export or Primary Ledger template export. Show the exact environment, task, mode, and purpose and obtain new explicit approval for that export only |
| Export process times out | Stop and report environment, exact task code, export mode, ProcessId when available, last status, elapsed wait, and safe next-check path. Do not submit a replacement job automatically |
| Export process fails | Retrieve and persist ProcessLog or status evidence when available, classify the failure, and stop before a new export request |
| AccountingMethodName is omitted or names Standard Accrual | Continue without a method question and author STANDARD_ACCRUAL, S, and blank language |
| AccountingMethodName explicitly names another method | Do not reject or directly author the alternative. Disclose that FSCR will create Standard Accrual, retain the requested display name for the manual Specify Ledger Options handoff, and require re-export verification before Review and Submit |
| User supplies physical accounting-method fields | Reject the unsupported direct tuple intake, name the accepted optional display-name input, and keep the controlled Standard Accrual create tuple |
| GL-781333 duplicate-name or relationship-namespace rejection | Show the exact raw Name, the broader ledger/data-access-set/relationship namespace rule, scoped conflict evidence, and the requirement for a new unique name; do not weaken uniqueness to ledgersLOV alone |
| HTTP 401 or 403 | Classify auth or authorization, refresh an approved cached token once when applicable, retry the read once, and stop if still denied |
| HTTP 400 or Oracle 29140 | Classify a resolver-contract or input-validation failure from the actual response, persist the sanitized q and error, and stop. Invalid fields and malformed expressions are not value-not-found outcomes; never retry the identical invalid q |
| HTTP 429, 5xx, timeout, DNS, TLS, pagination, or client transport failure | Classify transport or Fusion API, use only bounded safe read retries, and disclose the final failure |
| Preview shows a row delete, nonowning member change, alias divergence, or undocumented field population | Block approval and rebuild the smallest delta from a validated package |
| An intentional blank contains whitespace, a control character, escaped control text such as `\\n`, or a textual null sentinel | Classify input validation or package serialization failure, stop before preview or import, and rebuild it as a true zero-character CSV field |
| Approval is missing or stale | Stop before import and request explicit approval for the exact current preview |
| Import returns an uncertain outcome | Do not resubmit; reconcile with process status and an identical-scope re-export first |
| Import process times out | Stop and report environment, GL_MANAGE_PRIMARY_LEDGERS, process or request identity, last status, elapsed wait, and a safe next-check path |
| Import process fails | Retrieve available ProcessLog and status evidence, preserve partial successes with an errors array and nonzero status, and stop before retry |
| Import failure identifies malformed blank serialization | Preserve the failed package and ProcessLog as evidence, reconcile the exact object name to determine whether any row was created, and never replay the failed package. After proving no unintended object or partial result exists, rebuild a new package with true empty fields and require a new preview fingerprint and fresh explicit approval |
| Re-export verification differs | Report field-level semantic differences and classify process failed or Fusion API as supported by evidence; metadata-only change does not prove success |
| Artifact persistence fails | Stop, retain safe in-memory findings if possible, and report the exact intended project artifact location without exposing sensitive payloads |
| Review, submit, activate, enable conversion, or open periods is requested | Classify approval blocker and stop under open item GL-07 |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Malformed alternative AccountingMethodName, user-supplied physical method fields, overlength value, invalid conditional choice, or unsafe free text | Correct only the identified user input and rerun validation; an omitted method is valid and defaults to Standard Accrual |
| Catalog mismatch | Task, package, member, header, alias, metadata, environment, release, or scope does not match | Acquire a correct package or authoritative export; do not patch the mismatch by assumption |
| Auth or authorization | Token is absent or expired, principal lacks access, or a read is denied | Refresh an approved cached token once for 401 or 403 when applicable, otherwise obtain the required privilege |
| Transport or environment | Timeout, DNS, TLS, connectivity, pagination transport, or wrong environment | Correct the environment or transport issue and rerun only the safe read or validation stage |
| Fusion API | Oracle returns a service rejection, malformed response, or nontransient server failure | Preserve the sanitized response and correct the documented cause before another attempt |
| Process timeout | A CoA export, template export, import, or verification-export poll reaches the bounded wait without a terminal status | Record task, mode, ProcessId or request identity, last status, and safe next-check path; never submit a replacement process automatically |
| Process failed | An export or import reaches failure, or re-export proves the requested business result absent or partial | Retrieve logs, preserve safe partial evidence, diagnose, and satisfy the owning workflow's approval gate before any new live request |
| Artifact persistence | Required preview, diagnostic, registry, or verification artifact cannot be safely saved | Correct the destination and persist before proceeding |
| Approval blocker | Preview approval is absent or stale, design gate is unresolved, or forbidden lifecycle mutation is requested | Stop and request the exact missing approval or use the documented UI handoff |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Lookup failure | Resolver, supplied non-sensitive identity, match count when available, HTTP or client class, retry count, and corrective action |
| Export-operation approval | Exact environment, task code, populated or template-only mode, business purpose, expected artifact, and statement that the approval authorizes only that single export submission |
| CoA export decision | Every candidate considered, environment and release agreement, selected StructureInstanceCode containment, populated-versus-header-only result, selected artifact or reason one new routed export is required, and accepted ProcessId when submitted |
| CoA role result | Structure-instance composite identity; balancing and optional management SegmentCode, Name, ColumnName, SequenceNumber, and instance ValueSetCode; exact source members and row cardinalities |
| Primary template export | Environment, release, GL_MANAGE_PRIMARY_LEDGERS, template-only mode, ProcessId, terminal status, selected artifact, ten-member inventory, metadata identity, header-only row counts, and duplicate-request reconciliation result |
| Package preview | Environment and release identity, task code, exact member inventory, checksums, row adds, updates and deletes, field source classes, warnings, UI handoffs, open-item scope, and semantic alias diff |
| Approval | Exact preview fingerprint, package artifact, environment, release, scope, expected business effect, and statement that any material change invalidates approval |
| Import submission | Authorized executor, task code, sanitized process or request identity, submission time, and no credential or token values |
| Poll timeout | Environment, operation, task code, process or request identity, last status, elapsed wait, and safe next-check path |
| Process failure | Final status, available ProcessLog reference, partial-success summary, errors array, and nonzero result status |
| Re-export verification | Identical export scope, semantic business diff, alias parity, service-generated values, unintended changes, and verification verdict |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Mandatory business value absent | Guess a ledger name, chart of accounts, calendar, or currency |
| Exact ledger conflict exists | Continue to a CoA export, Primary Ledger template export, package build, or automatic rename |
| A current populated CoA export qualifies | Submit another GL_MANAGE_CHARTS_OF_ACCOUNTS_STRUCTURE_INSTANCES export for convenience |
| A CoA role row is missing or ambiguous | Infer Company, SEGMENT1, another physical position, or a value set from DefaultValueSetCode or another chart of accounts |
| A same-task export may already have been accepted | Submit another export merely because the caller lost ProcessId, polling timed out, or artifact persistence was delayed |
| Export-operation approval is missing or applies to another task, mode, environment, or request | Submit the CoA populated export or Primary Ledger template export |
| Primary Ledger carrier is needed | Use a populated GL_MANAGE_PRIMARY_LEDGERS export, another task package, or an authored package from another ledger instead of the exact current template-only artifact |
| AccountingMethodName is omitted | Ask for a method or leave the new ledger's physical method tuple blank |
| Another AccountingMethodName is supplied | Put that alternative tuple into the create package, request its technical tuple, or claim the manual UI handoff is already complete |
| Retained earnings or another ledger option is supplied | Resolve, create, or serialize it in Manage Primary Ledgers; it remains a dependent-task receipt until this task imports and verifies successfully |
| Optional option family unrequested | Ask baseline questions or enable the family |
| Lookup fails | Return value not found for HTTP, auth, pagination, parse, or client failure |
| Package shape differs | Reorder headers, rename members, omit aliases, flatten multiline values, delete header-only members, or hand-invent metadata |
| Live import fails or is uncertain | Automatically retry or replay the import without idempotency evidence and fresh explicit approval |
| A field is intentionally blank | Serialize whitespace, a line break, escaped control text such as `\\n`, or a textual null sentinel instead of a true empty CSV field |
| Sensitive material is present | Persist or disclose tokens, credentials, private keys, protected payloads, or customer data |
| Review and Submit requested | Author writable lifecycle fields or submit, activate, enable conversion, or open periods |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MPL.EXECUTION_GATE | decision | 60 | execution_gate | ready->MPL.DONE;blocked->MPL.HANDLE_ERROR;failure->MPL.HANDLE_ERROR | MPL.ENFORCE_DESIGN | stop | Require the exact package preview, explicit current approval, authorized loader route, terminal import monitoring, and identical-scope re-export verification. |
| MPL.HANDLE_ERROR | step | 70 | error_handler | disclosed->MPL.FAILED | none | stop | Any validation, lookup, dependency, defaulting, design, preview, approval, import, monitoring, persistence, or verification stage fails or blocks. |
| MPL.DONE | terminal | 80 | terminal | none | MPL.EXECUTION_GATE | continue | The approved import completed and identical-scope re-export verified the requested primary-ledger shell with no unintended change. |
| MPL.FAILED | terminal | 90 | terminal | none | MPL.HANDLE_ERROR | continue | The task stopped safely with an actionable classified error or approval blocker. |

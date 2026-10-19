# Payroll Flow Patterns Error Handling and Execution Gate

## Source Basis

- Oracle Help Center functional sources listed in the companion Payroll Flow Patterns resource files.
- Repository Data Loader approval, execution, status, and retry controls apply to every ProcessFlows import.
- Developer instruction received 16 September 2026: always use the Data Loader route for setup mutations.
- Developer-provided FSCR DAT generation workflow received 22 September 2026 defines all-or-nothing JSON validation-error behavior for processFlows DAT generation.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required business information is missing | Report every currently missing business-facing value together and stop before mapping or preview |
| ProcessFlows metadata or generated sample is missing or stale | Regenerate the current sample, attribute-details workbook, and key-fields workbook through core.data-loader; do not infer columns |
| Existing flow-pattern lookup returns no update target or multiple targets | Stop and request the exact displayed pattern name and LDG context; do not select by similarity |
| A predefined pattern is targeted for update | Stop and require a user-defined copy |
| A referenced task, parameter source, lookup, value set, LDG, or connected flow is unavailable | Identify the unresolved dependency and stop before preview |
| Fusion read-only lookup returns 401 or 403 | Classify as authentication or authorization failure, not absence |
| Data Loader validation rejects an artifact | Preserve the immutable artifact identity, report sanitized row and field diagnostics, correct the source, and generate a new preview |
| Data Loader import fails or is partial | Retrieve and persist available sanitized status and diagnostics; stop without automatic resubmission |
| Import status times out or is uncertain | Report target environment, ProcessFlows operation, request identifier, last status, and elapsed wait; reconcile status before considering another submission |
| Post-load read-back differs from the approved preview | Classify as verification failure and stop; do not report success or replay the import |
| DAT validation finds one or more missing, invalid, ambiguous, or unresolved values | Generate no partial DAT content; return only one JSON validation-error object containing every currently known error |
| A required reference lookup returns no match or multiple matches | Identify the attribute, object, reason, and required clarification; do not guess a code or ID and do not generate the DAT content |
| A child record has an invalid temporary ID, duplicate ID, or BaseFlowId other than 101 | Identify the affected FlowTask or FlowParameter attribute and stop before generation |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required values, supported formats, a missing mandatory Connector Status, or invalid supplied parameter relationships are missing or invalid | Correct the affected input set and revalidate; do not require Start Flow, End Flow, a complete task sequence, Parameter Basis, or Basis Value when not supplied |
| Catalog or metadata mismatch | ProcessFlows is unregistered, stale, or inconsistent with the proposed mapping | Refresh Data Loader metadata and remap |
| Auth or authz | Fusion returns 401, 403, or hides required secured patterns | Refresh authorized access once when the active workflow permits; otherwise stop |
| Fusion API | Read-only lookup returns an unexpected service error | Preserve sanitized diagnostics and stop |
| Process failed | Data Loader reaches a failed or partial terminal status | Retrieve diagnostics, preserve partial outcomes, and stop |
| Process timeout | Data Loader doesn't reach a terminal status within the allowed wait | Record the last status and safe next-check path |
| Approval blocker | The immutable preview or explicit Data Loader approval is absent or stale | Re-preview and obtain approval through core.data-loader |
| Verification failed | Persisted flow configuration doesn't match the approved business design | Report the mismatch and require a new corrective plan |
| DAT validation error | One or more ProcessFlows input, hierarchy, identifier, derivation, enum, metadata, lookup, or supplied-parameter checks fail | Return the complete JSON validation-error result and request the listed required inputs |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before preview | Exact target environment, operation, pattern name, LDG scope, requested task-composition summary, parameter summary, mandatory Connector Status, derived DefaultFlowFlag, and unresolved items |
| Before approval | Immutable Data Loader artifact identity, business-object name ProcessFlows, row counts, create or update intent, defaults applied, warnings, and validation status |
| After failure | Failure class, affected business record or field, sanitized Oracle diagnostics, partial-success state, and one safe next action |
| After completion | Terminal Data Loader status and read-only business-facing verification against the approved configuration |
| DAT validation failure | Show status validation_error and an errors array; each error contains attribute, object, reason, and requiredInput, with no Markdown, comments, explanatory text, or partial DAT arrays |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A direct REST setup mutation is requested | Do not POST, PATCH, or DELETE setup through a direct REST client; route the setup change through core.data-loader |
| A public flowPatterns attribute appears writable by name | Do not treat read-only API attributes as ProcessFlows import columns without current registered metadata |
| Approval is missing, stale, or bound to another artifact | Do not submit the import |
| A prior submission has an uncertain result | Do not retry until read-only reconciliation proves the prior outcome |
| A destructive change is proposed | Do not proceed without exact target, effect, rollback plan, and the Data Loader workflow's explicit approval |
| Credentials or protected values are present | Do not persist or disclose tokens, secrets, private keys, opaque URLs, or sensitive payload data |
| DAT validation has failed | Do not emit Flow, FlowTask, or FlowParameter content, and do not continue to Data Loader preview or submission |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PFP.EXECUTION_GATE | decision | 60 | execution_gate | ready->PFP.READY_FOR_DATA_LOADER;blocked->PFP.HANDLE_ERROR | PFP.ENFORCE_DESIGN | stop | After validation, reference resolution, dependencies, defaults, and design enforcement; this gate hands an approved preview candidate to core.data-loader and does not itself perform a Fusion write |
| PFP.HANDLE_ERROR | step | 70 | error_handler | handled->PFP.RETURN_ISSUES | none | stop | Any validation, lookup, dependency, defaulting, design, approval, process, or verification failure |
| PFP.RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | Return all blocking items and one safe next action |
| PFP.READY_FOR_DATA_LOADER | terminal | 90 | terminal | none | PFP.EXECUTION_GATE | stop | The task-local requirements are complete and the request is ready to enter the separate core.data-loader preview and approval workflow |

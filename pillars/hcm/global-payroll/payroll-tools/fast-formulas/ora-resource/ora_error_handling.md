# Fast Formulas Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required HDL identity, formula type, effective date, scope decision, or text file is missing | Classify as input validation, return every affected field, and stop before DAT or ZIP preparation. |
| FormulaText isn't a filename for one file under ClobFiles | Classify as input validation and stop before ZIP preparation. |
| DELETE or an action other than MERGE is requested | Classify as unsupported because the supplied HDL sources establish only MERGE. |
| FormulaId or GUID is supplied for a new record, or FormulaCode is changed on update | Classify as input validation and preserve the exported identity and immutability rules. |
| Formula text has invalid statement order, syntax, assignment, alias, default, context, operator, or data-type usage | Return the compilation category and affected source location when available; correct and compile again before use. |
| Formula execution encounters an uninitialized variable, divide by zero, missing or multiple database rows, null data, invalid number, range overflow, invalid array access, incompatible called-formula types, recursion, or excessive calls | Classify as process failed, preserve sanitized execution evidence, and correct the formula or its data assumptions before another test. |
| A required database item isn't available to the formula type | Stop and verify the formula type and contexts; don't reinterpret it as a local variable. |
| A required flexfield database item hasn't been generated | Stop and complete flexfield deployment and database-item generation before compile. |
| Authentication, Data Exchange access, or LDG data security fails | Classify as auth or authz; don't reinterpret denial as absence or expose credentials. |
| HDL rejects the archive or record | Classify as process failed, return the object, redacted record identity, loader phase, and confirmed message, and require a corrected new archive. |
| A loader request times out | Classify as process timeout and report the environment, FastFormula business object, request ID, last status, elapsed wait, and safe status-check path. |
| Preview or explicit approval is missing for a live HDL handoff | Classify as approval blocker and stop before upload or submission. |
| A live upload, import, or load has an uncertain result | Reconcile using read-only loader status; don't upload or submit again automatically. |
| A reference or LOV name returns no match | Return a validation error with the field and sanitized invalid value; don't prepare the import field. |
| A reference or LOV name returns multiple matches | Return an ambiguity error and don't select a value automatically. |
| A reference or LOV lookup endpoint or response contract is incomplete | Classify as catalog mismatch and stop before claiming the task is ready. |
| A reference lookup has no active session | Establish or refresh the configured authorized session and retry only the read-only lookup once. |
| FormulaTypeCode or LegislativeDataGroupName is absent or blank in a generated FastFormula DAT record | Classify as input validation and stop before preview; populate both fields before preparing a new archive. |
| FormulaName or FormulaId doesn't resolve to exactly one effective persisted formula before a content or compilation action | Return not found or ambiguity as applicable and don't call the custom action. |
| getFormulaContent fails or returns no result | Classify as process failed, preserve the sanitized response status, and don't substitute supplied, cached, or generated formula text. |
| submitCompileJob fails or its result omits formulaId, essJobId, essJobState, or effectiveDate | Classify as process failed, preserve the accepted identifiers that were returned, and don't poll or resubmit automatically. |
| Compiled remains N after compilation submission | Wait 5 seconds, then retrieve the formula through the primary endpoint using FormulaName or FormulaId; repeat until Compiled is Y or the workflow timeout is reached. |
| Compiled is Y and CompileStatus is I or E | Call getFormulaCompileMsg with the resolved formulaId and effectiveDate, then display the returned compiler message. |
| Compilation polling reaches the workflow timeout | Classify as process timeout and report the formula identity, ESS job identifier and last state when available, elapsed wait, Compiled, CompileStatus, and a safe next-check path; don't submit another compile job. |
| getFormulaCompileMsg fails or returns no result | Classify as process failed and report that compiler diagnostics couldn't be retrieved; don't invent or suppress a compiler message. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| INPUT_VALIDATION | Required values, file shape, source keys, scope, formula contract, or effective dates are missing or invalid | Correct all reported fields and validate again. |
| CATALOG_MISMATCH | A target HDL export conflicts with the supplied FastFormulasExport.xls contract | Stop and reconcile the action, keys, attributes, lengths, requiredness, and CLOB rule before preparing a new archive. |
| AUTH_AUTHZ | Authentication, Data Exchange access, functional privilege, or LDG security fails | Correct access through the authorized environment owner. |
| TRANSPORT_ENVIRONMENT | The authorized loader workflow can't safely reach the target | Preserve sanitized diagnostics and retry only after the environment issue is resolved. |
| PROCESS_TIMEOUT | The loader or compilation flow doesn't reach terminal status in the allowed wait | Report the last confirmed state and use the safe next-check path. |
| PROCESS_FAILED | Compilation, execution, import, load, or record processing reaches a confirmed failure | Correct the formula or source archive and prepare a newly reviewed run. |
| APPROVAL_BLOCKER | Exact preview or explicit approval is missing or stale | Regenerate the preview and obtain approval bound to it. |
| UNSUPPORTED | Supplied evidence doesn't establish the requested action, formula-type contract, field, or scope | Stop and obtain current target evidence. |
| NOT_FOUND | A reference or LOV input returns no exact match | Report the field and sanitized invalid value and request a valid reference. |
| AMBIGUOUS | A reference or LOV input returns more than one exact match | Request a more precise reference value; don't choose automatically. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input validation | Business object, operation, affected fields, sanitized supplied values, and required corrections. |
| Metadata readiness | Environment, FastFormula metadata source/date, selected operation and key strategy, FormulaText filename, and affected DAT header. |
| HDL handoff | Environment, archive identity and fingerprint, operation, source-key strategy, formula code/type/name, effective date, scope, business effect, unresolved risks, and approval status. |
| Compilation or loader failure | Environment, formula identity, phase, request ID when available, sanitized messages, and one safe next action. |
| Formula content retrieval | Environment, resolved formula identity and effective date, retrieval outcome, and returned persisted formula text; don't expose credentials or raw response wrappers. |
| Formula compilation | Environment, formula identity and effective date, ESS job ID and state when returned, Compiled, CompileStatus, sanitized compiler message when required, elapsed wait, and approval status. |
| Sensitive evidence | Confirm that credentials, tokens, private keys, customer data, protected identifiers, formula contents, and sensitive payloads weren't exposed or persisted in diagnostics. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Target FastFormula metadata conflicts with the supplied export | Don't present a production HDL archive as ready until the contract is reconciled. |
| Formula type, LDG scope, database item, or called-formula contract is unresolved | Don't infer or select a value automatically. |
| A route other than HCM Data Loader is proposed for setup-data mutation | Don't perform the mutation; route through core.data-loader. |
| Preview or approval is absent or changed | Don't upload or submit the archive. |
| A mutation fails or its outcome is uncertain | Don't retry without safe reconciliation and fresh approval where required. |
| A formula hasn't compiled successfully | Don't present it as ready for payroll or other application use. |
| Backend behavior is undocumented | Don't fabricate fields, keys, formula-type semantics, CLOB handling, error payloads, or retry behavior. |
| A reference or LOV lookup is unresolved | Don't send the unresolved name in a field that requires a code or ID. |
| A formula-content or compilation action target is unresolved | Don't guess formulaId or effectiveDate and don't call the custom action. |
| Formula compilation lacks current task-specific mutation approval or an authorized executor | Don't call submitCompileJob. |
| A compile submission is pending, timed out, failed, or uncertain | Don't call submitCompileJob again until the existing outcome is reconciled and a fresh approval is obtained when another submission is required. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| FF.EXECUTION_GATE | decision | 6 | execution_gate | hdl_preparation_ready->FF.DONE_HDL_PREPARATION;guidance_ready->FF.DONE_GUIDANCE;blocked->FF.HANDLE_ERROR | FF.ENFORCE_DESIGN | stop | Validation, dependency, reference resolution, defaulting, and design checks completed |
| FF.HANDLE_ERROR | step | 7 | error_handler | disclosed->RETURN_ISSUES | none | continue | A prior node reports invalid, blocked, unsupported, unauthorized, failed, or uncertain |
| FF.DONE_HDL_PREPARATION | terminal | 8 | terminal | none | FF.EXECUTION_GATE | continue | The HDL contract is validated for handoff to a separately authorized core.data-loader workflow; no Fusion write is authorized here |
| FF.DONE_GUIDANCE | terminal | 9 | terminal | none | FF.EXECUTION_GATE | continue | Source-backed Fast Formula guidance is ready for return; no Fusion write occurred |
| RETURN_ISSUES | terminal | 10 | terminal | none | none | continue | Blocking, unsupported, or failure details are safely classified and disclosed |

## Sources

- Developer-provided /scratch/share/FastFormulaAll.dat, accessed 2026-08-17.
- Developer-provided /scratch/share/FastFormula.dat, accessed 2026-08-17.
- Developer-provided /scratch/share/FastFormulasExport.xls, accessed 2026-08-17.
- Developer-provided standard reference and LOV instructions, received 2026-08-17.
- Developer-provided Fast Formula reference endpoint and session instructions, received 2026-08-17.
- Developer-provided mandatory FastFormula DAT population instruction for LegislativeDataGroupName and FormulaTypeCode, received 2026-08-18.
- Developer-provided persisted formula-content and formula-compilation custom-action contracts, received 2026-08-18.
- Oracle Fusion Cloud HCM, Formula Compilation Errors: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/formula-compilation-errors.html
- Oracle Fusion Cloud HCM, Formula Execution Errors: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/formula-execution-errors.html
- Oracle Fusion Cloud HCM, Formula Compilation: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/formula-compilation.html
- Oracle Fusion Cloud HCM, Improve Formula Performance: https://docs.oracle.com/en/cloud/saas/human-resources/oapff/improve-formula-performance.html

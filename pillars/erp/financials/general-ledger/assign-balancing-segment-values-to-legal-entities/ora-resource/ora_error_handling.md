# Assign Balancing Segment Values to Legal Entities Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required input is missing or invalid | Name the exact field, row position, raw value, violated shape rule, and safe correction; do not start package acquisition or a live import |
| Value set or value lookup returns zero | Report the exact ValueSetCode or value, endpoint, filter, resolved parent ID when applicable, and match count zero |
| Resolver returns many | Report ambiguity with safe candidate business keys and require a more precise target or input |
| Authentication, authorization, client, timeout, or malformed response | Report the actual failure class and safe diagnostics; never convert it to value not found |
| Package task, scope, release, member, header, or manifest mismatch | Reject before ZIP authoring and list every mismatch |
| A changed CSV contains literal line-ending escape text, merges its header with a data row, fails CSV parsing, or has an unexpected field count | Classify as a package defect. Rebuild the changed member with a CSV serializer, preserve the selected carrier's header and member order, re-run the parser-based final-ZIP check, and obtain fresh checksum-bound approval; never submit the package to discover the CSV contract |
| Package was created for an earlier request, test case, preview, or import | Reject it even when environment, release, task, and ledger match; submit a new populated ledger-scoped export for the current create or update execution, or follow the classified template fallback if that new export has an eligible carrier failure |
| Initial task export is unscoped or completes with warnings because GL_LEDGER_BSV.xml exceeds the Fusion size limit | Download and read the original ProcessLog, reject the incomplete package, resolve the exact PRIMARY LedgerId, and start one new read-only task export with SetupTaskCSVExportCriteria set to GL_PRIMARY_LEDGER / Set1 / PRIMARY_LEDGER_ID / {LedgerId} |
| High-level task export wrapper cannot accept LedgerId criteria | Do not create a workflow blocker, submit an unscoped export, or select template fallback. Use the pillar-documented `core.fusion-api.rest-api-client` POST with SetupTaskCSVExportCriteria, then poll and download the returned ProcessId through the existing shared result helper |
| New ledger-scoped populated export cannot return a usable carrier | Preserve the original process and safe diagnostic evidence. After bounded read-only handling, classify size limit, HTTP 413, completed-with-warning or incomplete carrier, transient 429 or 5xx, timeout, and result-download/transport failure as template-fallback eligible; invoke one current same-task template export and retain both receipts |
| Populated export fails for an excluded reason | Stop without template fallback for invalid task or scope criteria, HTTP 400, final 401 or 403, missing privilege, unresolved ledger or legal entity, business conflict, corrupt downloaded content, or user cancellation; show the exact safe remediation |
| Template export succeeds but current business-state evidence is incomplete | Report the missing parent, ledger-role, legal-entity ownership, or direct-ledger ownership evidence and stop before authoring; never interpret header-only rows as absence |
| Assignment conflict | Report the exact value-set and segment-value key, current legal-entity or ledger owner, requested owner, and required UI/accounting review; do not reassign implicitly |
| Technical default is not proven | Identify the field and missing export, manifest, or documented metadata evidence; stop before import rather than submit a discovery attempt |
| FSM validation or import fails | Capture process identity, object or member, row semantic key, stage, exact safe message, timestamps, partial successes, and error-file or process-log availability |
| Approved Data Loader invocation times out or is interrupted before returning ContentId or RequestId | Classify the outcome as unknown, preserve the recovery anchor, and do not retry. Query the exact DataSetName and submission window through recover_data_loader_submission_exact; if unavailable or unauthorized, compare the exact task process collection with the captured pre-submit baseline through recover_fsm_import_process_delta |
| Import process times out | Stop and report environment, task, operation, process identity, last status, elapsed wait, and next-check path; do not resubmit |
| Verification differs | Keep completion blocked and show missing assignments, wrong owners or dates, unexpected unrelated rows, or metadata-only noise |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input validation | Missing, invalid, overlength, duplicate, ambiguous, or conditionally required input | Correct input and revalidate |
| catalog or package mismatch | Task, release, scope, member, header, field graph, or manifest does not match current authoritative evidence | Obtain a fresh exact task export; use a template only if the populated-export failure is separately classified as eligible |
| export carrier fallback eligible | A current ledger-scoped populated export has a proven size, 413, incomplete-carrier, transient 429 or 5xx, timeout, or result-download/transport failure after bounded read-only handling | Submit one current same-task template export, then require separate current parent and ownership evidence before authoring |
| dependency readiness | Parent legal entity, value set, value eligibility, assignment state, or approval is unresolved | Complete the named prerequisite and rerun read-only resolution |
| auth or authz | Final 401/403 or insufficient export, lookup, import, UI, or report privilege | Refresh eligible cached authentication once, then obtain the correct access |
| transport or environment | Timeout, 429, 5xx, network, wrong environment, client, or malformed response | Use bounded handling for eligible read-only operations; only a classified populated-carrier failure may select template export, and it never authorizes import |
| Fusion process failed | Terminal CSV validation or import failure | Retrieve process log and object errors; correct the source and obtain a new checksum-bound approval before retry |
| submission response unknown | The approved adapter invocation ended before returning identifiers and server acceptance is not proven | Run only the documented exact-name and process-delta read-only recovery; one exact recovered identity resumes normal monitoring, while zero or many remains blocked without retry |
| process timeout | No known terminal state within the polling budget | Continue checking the original process identity; do not resubmit |
| artifact persistence | Baseline, preview, ZIP, receipt, error details, or verification evidence cannot be stored safely | Stop and repair the project artifact path without exposing credentials |
| verification mismatch | Import reported success but identical-scope business state does not match the approved delta | Preserve evidence, report the mismatch, and keep the task incomplete |
| approval blocker | Approval is absent or invalidated by any input, lookup, package, or checksum change | Stop before import and issue a fresh preview |

## Retry Policy

| Operation | Retry Contract |
|---|---|
| Read-only REST GET | Bounded retry for 429, transient 5xx, or timeout; refresh eligible cached authentication once for 401; no retry for 400 or final 403 |
| Task export status check | Continue polling the original export process under the shared export policy; never create duplicate populated exports merely because download is delayed |
| Unscoped task export | A verified missing-scope or unscoped size-limit ProcessLog authorizes one new read-only populated export with the exact ledger criterion; it does not authorize an import retry and the incomplete ZIP is never a baseline |
| Ledger-scoped populated carrier failure | After bounded read-only handling, a classified eligible failure authorizes one current same-task template export through shared.setup-export.task-level-export template-only mode. Do not repeat template export automatically and do not carry populated-export criteria to the template endpoint |
| Template carrier acquired | Continue only when current supported read-only Fusion evidence proves the exact parent, balancing role, and both legal-entity and direct-ledger ownership paths; otherwise stop without package generation |
| CSV validation | Correct deterministic package errors locally, regenerate the preview, and revalidate; do not weaken a rule |
| FSM import submit | No automatic retry; first establish the original terminal state and retrieve logs, then require a corrected final preview and new approval |
| Data Loader submission response timeout | Never replay the upload or initiation request. Recover by exact unique DataSetName and, when necessary, the exact-task process delta captured before submission; if neither yields one identity, keep the result unknown and require reconciliation before a separately previewed attempt |
| Verification export or report | Bounded retry only for retrieval; never treat an unavailable report as proof of success |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before import | Exact target, task, scope, legal entity, value set, values, dates, resolver receipts, carrier mode, populated-export and template provenance when applicable, fallback reason, business-state evidence coverage, package checksums, member validation, row-level diff, conflicts, exclusions, and approval identity |
| During import | Original process identity, submitter, timestamps, current stage, status, completed/error counts when exposed, and error-file or process-log availability |
| After import | Terminal status, safe process messages, identical-scope verification receipt, expected versus actual assignments, unrelated changes, and no-op or partial-success classification |
| Resolver failure | Raw input, endpoint or export source, exact filter or key, requested fields, match count when available, safe HTTP/client/correlation details, and remediation |
| Timeout | Original process identity, last state, elapsed wait, next-check path, and explicit no-resubmit warning |
| Timeout before identifiers | Exact DataSetName, package checksum, task code, submitter, submission window, caller elapsed time, whether exact dataset lookup was authorized, task-process delta count, and explicit no-resubmit warning |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| No exact current-run carrier | Do not build a ZIP from memory, a sample inventory, an unscoped or incomplete-warning export, an unrelated task export, an earlier test case's export, or a previous-release manifest; submit the exact populated ledger-filtered export first, then use only the classified current template fallback when eligible |
| Template exists without current state evidence | Do not use the template to resolve a legal-entity parent, infer no existing legal-entity assignment, infer no direct-ledger assignment, or copy current ownership from a previous populated export |
| Fallback failure is excluded or ambiguous | Do not invoke template export for invalid criteria, 400, final 401 or 403, missing privilege, unresolved identity, business conflict, corrupt content, cancellation, or an unclassified failure |
| Missing or ambiguous parent | Do not create a ledger, legal entity, or journal-configuration parent through this assignment skill |
| Lookup failure | Do not choose the first or fuzzy result or relabel authentication, authorization, transport, or client failure as absence |
| Existing assignment conflict | Do not delete or reassign a value implicitly and do not bypass posted-use constraints |
| Unproven technical field | Do not guess, copy from an unrelated row, or use a failed live import as the normal default-discovery mechanism |
| Changed package after approval | Do not import; invalidate approval and show a fresh checksum-bound preview |
| Import already submitted | Do not auto-resubmit until the original process identity and terminal state are known |
| Submission may have reached Fusion but returned no identifier | Do not rerun core.data-loader, rename and resubmit the same approved package, choose the newest process, or treat zero currently visible processes as proof that no upload occurred |
| Credentials or restricted data are present | Do not persist tokens, passwords, cookies, private keys, database connection details, or unrelated customer data in resources, logs, packages, or project artifacts |

## Verification

| Check | Pass Condition |
|---|---|
| Target | Verification uses the same environment, release, task, and ledger scope |
| Assignment | Every approved exact ValueSetCode and FlexSegmentValue is owned by the expected LegalEntityIdentifier with expected dates |
| Exclusivity | No approved value is simultaneously assigned to another legal entity or directly to the ledger in the same accounting context |
| Package closure | Unrelated assignment rows and all other task members remain unchanged apart from expected service-owned metadata noise |
| Evidence | First use a new post-import populated identical-scope task export. If the same eligible carrier failure recurs, a current task UI result or Balancing Segment Value Assignment Report may supply business-state proof only when it covers the exact owner and dates; otherwise verification remains incomplete. The pre-import package and import status alone are not enough |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ABSV.ERROR_POLICY | step | 60 | error_handler | handled->ABSV.PREVIEW_GATE | ABSV.ENFORCE | stop | Preview and execution errors must use the classified policy |
| ABSV.PREVIEW_GATE | decision | 70 | execution_gate | approved->ABSV.READY;issues->ABSV.RETURN_ISSUES | ABSV.ERROR_POLICY | stop | Exact final preview is complete |
| ABSV.READY | terminal | 80 | terminal | none | ABSV.PREVIEW_GATE | continue | Approved import and verification may proceed through shared and core execution skills |
| ABSV.RETURN_ISSUES | terminal | 90 | terminal | none | none | continue | Validation, dependency, lookup, design, preview, approval, execution, or verification issues remain |

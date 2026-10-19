# Assign Balancing Segment Values to Ledger Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Final ZIP has literal line-ending escape text, merged header/data records, malformed CSV quoting, an unexpected physical record or field count, unsafe member paths, duplicate members, or executable content | Classify as a package-integrity defect. Do not upload. Rebuild with a CSV serializer, parse every changed CSV, validate archive safety, and obtain a new preview and approval for the rebuilt ZIP. |
| Required export, manifest, or source evidence is missing, stale, or unreadable | Stop before package generation; classify as input validation or artifact persistence and request a fresh scoped export |
| A scoped export request lacks the exact task code at the request root, any criterion, or the process item; uses a display ledger name as the scope value; or contains competing scope criteria | Classify as input validation. Do not submit it. Rebuild the request from the resolved numeric ledger ID and one internally consistent scope criterion. |
| Scoped FSM export completes with a `Ledger Segment Value Assignment` warning that `GL_LEDGER_BSV.xml` exceeds the 10 MB limit | Treat the export as incomplete, not as evidence that no assignments exist. Preserve the log detail and use the Balancing Segment Value Assignments Report or the scoped UI assignment grid as the read-only assignment check. Do not retry the same export expecting assignment rows. |
| UI-equivalent task-export criterion `GL_PRIMARY_LEDGER` / `Set1` / `PRIMARY_LEDGER_ID=<target numeric ledger ID>` is accepted but the package is empty | The criterion expects the resolved numeric `LedgerId`, not the UI display name. Resolve the ID first, then rerun the read-only export. |
| UI-equivalent task-export criterion using the resolved numeric `PRIMARY_LEDGER_ID` still yields a `GL_LEDGER_BSV.xml` size warning | Record both the accepted scope metadata and the expansion warning. Do not infer that the ledger has no assignments; use the report or UI grid for assignment existence evidence. |
| A completed scoped export returns an empty process-result collection | This is not yet a blocker or evidence that no package exists. Run the standard result helper with the retained ProcessId and persist its retrieval receipt before any disclosure. If bytes are returned, validate the ZIP and continue. Only if the receipt evidences unavailable or invalid FileContent, retrieve and preserve the process log, then classify the result. Do not report “no downloadable FileContent” or post a replacement export solely because the result collection is empty. |
| Ledger or balancing-segment value resolution returns zero, multiple, or conflicting results | Stop as a dependency blocker; request a precise supported identifier or authoritative scoped evidence |
| A Company Value is supplied without LedgerName | Stop before value validation or package generation and ask for the exact target ledger. Do not treat the Company Value as globally assignable. |
| A Company Value and target name are supplied with no Legal Entity signal | Resolve the target through the exact ledger lookup. If it resolves as one ledger, continue as a direct ledger assignment; do not ask the user to repeat the word "ledger" or collect value-maintenance fields. |
| The request explicitly names a Legal Entity or says to assign to a Legal Entity | Stop the direct-ledger workflow and route to Assign Balancing Segment Values to Legal Entities. If the Legal Entity is unnamed, ask for its exact name; do not treat the supplied ledger as that Legal Entity or use this task's direct-ledger package contract. |
| An existing-value assignment flow asks for Summary, Allow Posting, Allow Budgeting, hierarchy, or another value-definition attribute | Correct the route before continuing. Those are value creation/maintenance fields, not inputs to a ledger BSV assignment; resolve the exact value's enabled, effective, non-summary status from its ledger-specific value set instead. |
| The supplied ledger resolves as SECONDARY but no owning primary ledger was supplied | Ask directly for the exact owning primary ledger. Do not try to discover it by submitting the secondary LedgerId as PRIMARY_LEDGER_ID, guessing a relationship, or making an unscoped export. |
| Ledger-only preview returns no enabled, effective, non-summary values | Return an empty preview with the resolved value-set identity; do not treat it as an error and do not create an import package |
| A ledger-only request is about to reuse a Company Value or dates from prior conversation, export evidence, or a project run record | Classify as input validation. Discard the stale assignment intent and return the ledger-only Company Value preview; do not duplicate-check, package, or import the reused value. |
| Current assignment evidence is missing during a Company Value preview | Show candidate values without an availability claim and state that assignment status is unknown. Block any later import until a successful scoped assignment export is available. |
| A selected Company Value already has an overlapping direct assignment | Return the existing ledger/value/date evidence as a duplicate and stop before package generation or import |
| A direct ledger value is assigned to a legal entity | Stop as a design blocker; do not reclassify it or retry the same import |
| A scoped export contains unrelated populated CSV rows | Treat those rows as a pre-import package-review finding. Preserve required ZIP structure and the assignment's exact parent chain, but exclude unrelated setup data rather than re-importing it by default. |
| The final package omits the matching `GL_LEDGER` or `GL_SECONDARY_LEDGER` parent row | Stop before upload. The direct assignment is a child record and Fusion can skip it when its required parent chain is absent. Rebuild from the exact current parent rows. |
| No retained-earnings account is configured on the target ledger | Stop before upload. Configure the retained-earnings account, obtain a fresh scoped export, and rebuild the package; do not retry with stale parent-row evidence. |
| A prerequisite changes after the scoped export or immutable approval preview was created | Invalidate the package and approval. Refresh the scoped export, repeat package validation, and obtain new explicit approval before import. |
| An approved Data Loader invocation is still running after the normal command-response window | Keep the same invocation alive with an outer command budget of at least 300 seconds and wait in intervals no longer than 60 seconds. Do not terminate it, replay the upload, or report that the response was lost while it is still running. |
| An approved Data Loader invocation ends without a retained UCM Content ID, Data Loader Request ID, or FSM import Process ID | Classify the outcome as unknown, preserve the DataSetName, package SHA-256, submitted-by identity, task code, environment, bounded submission window, and any pre-submit task-process baseline. Do not ask the user for server-generated IDs and do not retry. Recover first through the exact DataSetName/dataLoaderDataSets lookup, then through a unique exact-task process delta only if dataset recovery yields no identity. |
| Exact recovery after a Data Loader response timeout returns zero or multiple candidates | Keep the outcome unknown and stop. Preserve the recovery receipts and reconcile with read-only status/process-log evidence before any separately previewed and approved import attempt. |
| An FSM import process reports completed or successful status | Retrieve and read the underlying process log. Do not report success until the relevant Ledger Segment Value Assignment object shows the intended row as processed successfully with no errors or unreviewed warnings. Do not require a follow-up FSM export solely to confirm the import. |
| An FSM import log is unavailable, unreadable, reports zero intended rows, errors, or warnings affecting the Ledger Segment Value Assignment object | Classify as process failed or artifact persistence. Do not claim assignment success and do not retry or resubmit automatically; preserve the sanitized log/process evidence and resolve the discrepancy first. |
| An import diagnostic names GL_LEDGERS.BAL_SEG_VALUE_OPTION_CODE while the source export has BalSegValueOptionCode A | Do not classify A itself as an assignment blocker or introduce a manual A-to-I parent-row change. Read the complete log and diagnose the actual process failure separately; a direct specific-value assignment is valid from source value A. |
| Preview or import reports an unexpected FSM validation error | Preserve the sanitized diagnostic and package hash; stop and update the documented lookup/default contract before another attempt |
| Fusion creates an export or import process, but the local wrapper fails while writing its artifact because the configured environment identifier is not a portable filename | Use a pre-created, verified absolute project artifact path for every response and retain the returned ProcessId before invoking a result helper. For an export, if both response persistence and ProcessId recovery fail, one identical validated scoped-export retry is permitted because it is read-only; retain and verify the retry ProcessId. For an import, do not resubmit automatically. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Before import-package generation | Resolved ledger context, eligible segment-value evidence, every derived default, intentional blank, and any preserved parent-ledger fields |
| Before live import | Validated package inventory, release/environment match, preview result, and the explicit approval required by the selected import workflow |
| Immediately after Data Loader submission | Immutable DataSetName, package SHA-256, UCM Content ID, Data Loader Request ID, and FSM import Process ID when returned; if any identifier is unavailable, disclose the exact recovery stage rather than asking the user for it |
| Before reporting import success | Import process status, reviewed underlying log for Ledger Segment Value Assignment, intended processed/success count, and error/warning assessment |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A required technical default is unknown | Do not invent a value or use a failed live import to learn it |
| The user supplies database table information only | Do not generate SQL or treat a table column as proof of an accepted FSM import code |
| An unsupported field or package member is proposed | Do not add it to the package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BSVL-060-RETURN-SUCCESS | terminal | 60 | terminal | none | BSVL-050-ENFORCE-DESIGN | stop | All validations and design gates pass |
| BSVL-065-RETURN-PREVIEW | terminal | 65 | terminal | none | BSVL-020-RESOLVE-REFERENCES | stop | Ledger-only Company Value preview is complete |
| BSVL-070-RETURN-ISSUES | terminal | 70 | terminal | none | none | stop | Any blocking outcome |

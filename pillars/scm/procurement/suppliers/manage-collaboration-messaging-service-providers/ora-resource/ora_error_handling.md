# Service Providers FSM Task-CSV Import Gates and Error Handling

Oracle's task-CSV import flow starts an import with the task code, monitors the
returned process identifier, and retrieves the process log after completion.
The process log is the evidence for whether the import contains the required
setup data. [S1]

## Error Situations

| Situation | What Should Happen |
|---|---|
| `ORA_CMK_B2B_DOCUMENT_SETUP` returns `EnabledFlag: N` on the operation's exact host | Show "Service Providers export/import is blocked in {environment}: go to Navigator > My Enterprise > Offerings, select Procurement > Opt In Features, enable Simplify Configuration and Processing for B2B Messaging (`ORA_CMK_B2B_DOCUMENT_SETUP`), and wait for opt-in processing to complete. Then retry this operation." Stop before creating a template/data export process or uploading/importing a task ZIP |
| `ORA_CMK_B2B_DOCUMENT_SETUP` is absent, stale, ambiguous, or unreadable on the operation's exact host | Stop before creating a template/data export process or uploading/importing a task ZIP; report the specific lookup problem and selected host without saying the feature is disabled. Recheck only through the declared read-only resolver |

## Opt-In Recovery Steps

1. Navigate to **Navigator → My Enterprise → Offerings**.
2. Select the **Procurement** offering, then select **Opt In Features**.
3. Find **Simplify Configuration and Processing for B2B Messaging**.
4. Select its enable icon and complete the opt-in flow.
5. Wait for the opt-in migration or background processing to finish.
6. Rerun the Service Providers export.
| ZIP is unreadable, not FSM setup data, or does not identify this task | Stop before upload and use a completed exported ZIP for ORA_CMK_COLLAB_MESG_SERVICE_PROVIDER |
| Preflight target differs from the intended environment | Stop before upload; select the intended target and repeat preflight for the same immutable ZIP |
| Data Loader preflight or Task Hook validation fails | Stop before approval; correct the reported validation issue and rerun the affected read-only gate |
| Upload or import submission has an uncertain result | Do not replay the write; retain the returned identifiers and reconcile through the selected import-status route |
| Import process completes with errors or warnings | Retrieve and retain the ProcessLog or result report; correct the documented errors before a new approved import |
| Import process polling times out | Stop polling, report the task code, process identifier, last status, and elapsed wait; resume status retrieval only when requested |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Catalog mismatch or auth/authz | The exact feature item is absent, malformed, or unauthorized | Stop before side effects; verify release, feature identity, configured host, and read privileges through the declared route |
| Input validation | Archive shape, task identity, export provenance, or target binding fails | Correct the source or target and repeat preflight |
| Authorization | Fusion rejects the supported Data Loader operation | Obtain the required task-import and Data Loader privileges; do not guess role assignments |
| Process failed | The import process completes with errors | Retrieve ProcessLog, correct the reported data issue, and obtain approval for a new import |
| Process timeout | The import process has no completion result within the polling window | Preserve the process identifier and use the status retrieval path; do not resubmit |
| Approval blocker | The immutable ZIP, target binding, or task validation envelope is absent or changed | Repeat preflight and obtain approval for the exact validated ZIP |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Preflight result | Exact task identity, source ZIP, validated target, and whether upload is approved or blocked |
| Accepted import | Returned request or process identifier and the next status-check path |
| Completed import | Process status and ProcessLog or result-report outcome |
| Failure or timeout | Failure class, redacted evidence, identifiers available for reconciliation, and one safe next action |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| The target opt-in state is not freshly verified as enabled | Do not start an export process, upload a package, initiate import, infer enabled state from prior exports, or enable the feature implicitly |
| A ZIP was changed after preflight | Do not reuse approval or submit the changed bytes |
| Target identity is different from preflight | Do not upload or initiate the import |
| Import outcome is uncertain | Do not submit a duplicate import |
| Process log reports errors | Do not claim configuration was imported successfully |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CMKSP.IMPORT_GATE | step | 20 | execution_gate | ready_for_approval->CMKSP.READY_FOR_APPROVAL;blocked->RETURN_ISSUES | CMKSP.CHECK_DEPENDENCIES | stop | Before upload or import initiation |
| CMKSP.READY_FOR_APPROVAL | terminal | 30 | terminal | none | CMKSP.IMPORT_GATE | continue | All read-only import gates have passed |
| RETURN_ISSUES | terminal | 40 | terminal | none | none | continue | A validation or execution gate blocks import |

## Sources

[S1]: https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/Task_CSV_Import.html

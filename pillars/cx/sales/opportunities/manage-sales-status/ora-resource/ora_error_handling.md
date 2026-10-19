# Manage Sales Status Error Handling

## FSM Task Identity Policy

Require exact task code/name, selected task `SKILL.md`, target environment, and
immutable archive SHA-256 throughout review, export, package preparation, and
validation.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  `TaskCode`, `TaskName`, offering, and functional area.

The persisted context may come from a project setup-task plan without creating
an Oracle Run Book. Never hand-author, infer, or synthesize it solely to satisfy
Data Loader.

Stop before any undocumented write, automatic retry, or interpretation of a
runtime opportunity field as setup metadata.

## Error Situations

| Situation | What Should Happen |
| --- | --- |
| A status code or display value is blank or duplicated | Show the conflicting value and stop before package preparation |
| Fresh export, task identity and persisted Data Loader task context, ASM identity, member/header receipt, reviewed delta, state lock, unrelated-content receipt, final path, or reopened SHA-256 validation fails | Classify as package readiness, show every exact mismatch, and stop before Core Data Loader handoff |
| Data Loader fails before acceptance and returns neither a Content ID nor an import Request ID | Disclose the failure, refresh the exact task baseline, confirm the requested OPTY_STATUS LookupCode and values were not applied, rebuild and revalidate the immutable package, and hand it to Data Loader for a new Task Hook preview and later standalone `approve` |
| Data Loader returned an external identifier or the prior outcome is uncertain | Retrieve available status and reconcile the exact OPTY_STATUS row through a fresh task baseline before proposing any new mutation; do not start another import route |
| Data Loader submission, polling, ProcessLog retrieval, or verification fails or times out | Stop without replay, preserve the ProcessId and available sanitized evidence, state whether configuration may have changed, and require a newly validated immutable package before a new Data Loader-owned Task Hook preview and later standalone `approve` lifecycle |
| Accepted Data Loader initiation is followed by automatic polling, ProcessLog retrieval, result retrieval, or verification | Stop; accepted initiation is terminal for that request and those steps require a later explicit status or results request |

## Error Classifications

| Result Category | When Used | Next Action |
| --- | --- | --- |
| Design validation | A status violates predefined-category, uniqueness, or active-Open rules | Correct the design and rerun validation |
| Package readiness | The baseline is not a fresh completed exact-target and release export, the task or ZIP contract differs, the reviewed state lock drifted, unrelated content changed, or reopened bytes do not match the recorded hash | Refresh the exact task export, rebuild only the reviewed delta, and rerun `verify_sales_status_package_readiness` |
| Pre-acceptance Data Loader failure | Data Loader failed before acceptance with no external identifier and a fresh exact task baseline confirms the requested status was not applied | Build and validate a new immutable package, show the exact environment, task, proposed status row, path, and SHA-256, and hand it to Data Loader; Data Loader creates a new Task Hook preview and requests the later standalone `approve` |
| Import or process failure | Data Loader submission, polling, process execution, result retrieval, or verification did not complete successfully | Retrieve and preserve ProcessLog and status details when available, report partial or uncertain side effects, and do not retry; after reconciliation, hand only a newly validated package to Data Loader for a new preview-and-approval lifecycle |

## Disclosure Rules

| Gate | What Must Be Shown |
| --- | --- |
| Any Data Loader failure, timeout, uncertain response, process failure, result failure, or verification failure | Exact environment, task code and name, failed stage, failure classification, immutable package path and SHA-256, Content ID, import Request ID, ProcessId, request or ESS ID, last status, elapsed wait, processed and succeeded and failed and warning counts, source CSV and status LookupCode, message code and exact sanitized error text, ProcessLog and status artifact references, verified partial successes, whether configuration may have changed, what was not retried, corrective action, and one safe next step; mark unavailable values explicitly |

## Refusal Rules

| Situation | What Must Not Happen |
| --- | --- |
| No exact immutable-package handoff exists, or Data Loader has not completed its own Task Hook preview and later standalone approval | Do not perform or simulate a live Fusion mutation |
| A caller proposes shared.setup-import.task-level-import, a direct setupTaskCSVImports call, or another import adapter | Do not bypass core.data-loader; it is the only import orchestration route for this task |
| The executable package-readiness node has not returned `ready` for the exact immutable ZIP | Do not hand off, upload, initiate, or manufacture Data Loader-owned preview or approval evidence |
| Data Loader acceptance is uncertain, fresh exact task-baseline reconciliation is missing, the ZIP changed, or Data Loader's new Task Hook preview and later standalone approval are absent | Do not submit or retry the package; this child may only rebuild, validate, and hand off a new immutable package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.SALES_STATUS.GATE | decision | 4 | execution_gate | handoff_ready->OPP.SALES_STATUS.RETURN_READY;accepted_initiation->OPP.SALES_STATUS.RETURN_ACCEPTED;missing->OPP.SALES_STATUS.RETURN_MISSING;failed->OPP.SALES_STATUS.RETURN_FAILED | OPP.SALES_STATUS.PACKAGE | stop | Hand the package to Core Data Loader only after executable package readiness returns `ready`, without child approval, or route Data Loader's accepted initiation to its terminal result |
| OPP.SALES_STATUS.RETURN_READY | terminal | 5 | terminal | none | OPP.SALES_STATUS.GATE | continue | The unchanged immutable package and task identity and persisted Data Loader task context are ready for Core Data Loader Task Hook validation and preview generation; no import approval or execution has occurred |
| OPP.SALES_STATUS.RETURN_ACCEPTED | terminal | 6 | terminal | none | OPP.SALES_STATUS.GATE | continue | Core Data Loader returned accepted initiation; end this request without polling, ProcessLog retrieval, result retrieval, or verification |
| OPP.SALES_STATUS.RETURN_MISSING | terminal | 7 | terminal | none | none | continue | Required information, design evidence, package evidence, or reconciliation is missing |
| OPP.SALES_STATUS.RETURN_FAILED | terminal | 8 | terminal | none | none | continue | Validation, package reconciliation, or execution handoff failed |

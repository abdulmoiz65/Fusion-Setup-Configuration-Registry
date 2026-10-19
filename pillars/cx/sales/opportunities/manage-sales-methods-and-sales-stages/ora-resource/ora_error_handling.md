# Manage Sales Methods and Sales Stages Error Handling

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
| Required method or stage information is missing at initial intake | Populate a complete review-only proposal, label every assumption, and ask once for review; stop only before import if assumptions remain unreviewed |
| SetId/SetCode is malformed, unknown in exact-target evidence, conflicts with another selector or package row, confirmed Common Set resolves elsewhere, or the package uses a different environment's set | Classify as input or package identity validation, show sanitized supplied/baseline/package identities, and stop before set-dependent draft completion or handoff |
| PhaseCd is blank on one or more MOO_SALES_STAGE.csv rows | Classify as input validation, list every affected stage row and source file, stop before Core Data Loader handoff, correct and revalidate the immutable package, and recalculate its SHA-256 |
| StageNumber is blank, duplicated, or Fusion reports a stage uniqueness constraint | Classify as input validation or later-reported import failure as applicable; disclose the constraint, affected CSV rows, and stage numbers; reconcile possible partial changes on a later explicit results request, then require a corrected immutable package and a new Core Data Loader preview lifecycle before any retry |
| Fusion reports that no data was found for Sales Method or that export failure left no data in the configuration package | Classify as package-contract failure; on a later explicit results request retrieve the ProcessLog, stop before retry, re-export the same task from the same target, preserve its complete metadata/member/header graph, rebuild only reviewed rows, validate, recalculate SHA-256, and restart the Core Data Loader preview lifecycle |
| Validation, export, package creation, submission, polling, process execution, result retrieval, or verification fails | Stop at the failed stage and return the detailed failure disclosure; preserve available logs and partial-success evidence, state whether Fusion may have changed, and do not automatically retry a mutation |
| Accepted Data Loader initiation is followed by automatic polling, ProcessLog retrieval, result retrieval, or verification | Stop; accepted initiation is terminal and those steps require a later explicit status or results request |
| This child skill requests package approval before Core Data Loader handoff | Stop the child-level approval flow; validate the immutable package and hand it off so Core Data Loader can create the Task Hook-bound upload preview and later request standalone approve |
| Executable package readiness lacks exact TaskCode/TaskName, target/release/task export, ASM ObjectShortName/member/header receipt, reviewed delta/state lock/preservation, immutable final path, or matching reopened SHA-256 | Stop before handoff, list every missing or inconsistent receipt value, and rebuild and rerun verify_sales_methods_final_package |
| A read-only FSM export has null or absent MigrationProcessTaskCSVMetadata | Continue export validation from the fixed task metadata and ASM ObjectShortName, but do not treat that archive metadata as Data Loader task context |
| TaskContextPath is blank or TaskSequence is nonpositive | Stop before handoff, classify as an approval/task-binding blocker, generate or refresh the persisted project task context from its resolved setup-task plan, and rerun package validation |
| Persisted task context resolves to a different skill path, TaskCode, TaskName, offering, or functional area | Stop before handoff, classify as an approval/task-binding blocker, correct the project task mapping, and rerun package validation; never hand-author or synthesize a context entry |

## Error Classifications

| Result Category | When Used | Next Action |
| --- | --- | --- |
| Review required | Initial input is incomplete but a complete synthetic proposal can be produced | Show the complete proposal and accept approval or corrections; do not import until all assumptions are reviewed |
| Input validation | PhaseCd or another required immutable-package value is missing or invalid | Show all affected files and stage rows, correct the package, recalculate its SHA-256, rerun validation, and then hand it to Core Data Loader without requesting child-level approval |
| Import or process failure | A later explicit status, process, result, or verification request reports failure | Retrieve and preserve ProcessLog and status details when available, report partial success and uncertain side effects, and require reconciliation plus a new Core Data Loader preview lifecycle before another attempt |
| Approval blocker | The child tries to approve a package, or Core Data Loader's Task Hook-bound preview and later standalone approve are absent, changed, or stale | Before handoff, remove the child approval gate; after handoff, let Core Data Loader rebuild and own its approval lifecycle |

## Disclosure Rules

| Gate | What Must Be Shown |
| --- | --- |
| Any failed validation, export, package, import, polling, process, result, or verification step | Exact environment, task code and name, operation, failed stage, failure classification, immutable package path and SHA-256 when applicable, process ID, request or ESS ID, last status, elapsed wait, processed and succeeded and failed and warning and external-loading object and row counts, source CSV file, business or detail object, stage or entity identifier, message code and exact sanitized error text, ProcessLog and status artifact references, partial successes, whether configuration may have changed, what was not retried, corrective action, and one safe next step; mark unavailable values explicitly |

## Refusal Rules

| Situation | What Must Not Happen |
| --- | --- |
| No supported execution contract or validated immutable package exists | Do not perform or simulate a live Fusion mutation or handoff |
| Set identity is missing, wrong, conflicting, or cross-environment | Do not substitute Common Set, select a close match, rewrite the package row, or continue under a different scope |
| The user approved a design proposal | Do not treat design review as package approval or live-import authorization; complete package validation and hand off to Core Data Loader |
| The child package is valid but Core Data Loader hasn't created and received standalone approval for its immutable Task Hook-bound preview | Do not upload or initiate; the child must not manufacture or replace that approval |
| A live import failed or its outcome is uncertain | Do not retry automatically, reuse stale approval, or claim that Fusion is unchanged; reconcile available status and read-only evidence first on a later explicit request |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.SALES_METHODS.GATE | decision | 5 | execution_gate | package_validated->OPP.SALES_METHODS.RETURN_DATALOADER;accepted_initiation->OPP.SALES_METHODS.RETURN_ACCEPTED;missing->OPP.SALES_METHODS.RETURN_MISSING;failed->OPP.SALES_METHODS.RETURN_FAILED | OPP.SALES_METHODS.PACKAGE_READY | stop | Route an executable package-readiness receipt to Core Data Loader without child approval, or an accepted Data Loader initiation to its terminal result |
| OPP.SALES_METHODS.RETURN_READY | terminal | 6 | terminal | none | OPP.SALES_METHODS.DESIGN | continue | The design proposal is reviewed and ready for fresh-baseline package preparation; no live-import or package approval has been granted |
| OPP.SALES_METHODS.RETURN_DATALOADER | terminal | 7 | terminal | none | OPP.SALES_METHODS.GATE | continue | The exact immutable package passed executable validation for fixed task identity, target/release/task export, ASM/member/header receipt, reviewed delta/state lock/preservation, persisted TaskContextPath, positive TaskSequence, exact context resolution, final path, and reopened SHA-256 and is ready for Core Data Loader preview ownership |
| OPP.SALES_METHODS.RETURN_ACCEPTED | terminal | 8 | terminal | none | OPP.SALES_METHODS.GATE | continue | Core Data Loader returned accepted initiation; end this request without polling, ProcessLog retrieval, result retrieval, or verification |
| OPP.SALES_METHODS.RETURN_MISSING | terminal | 9 | terminal | none | none | continue | The user requested design changes or required executable package/handoff evidence is missing; regenerate and revalidate without a child approval gate |
| OPP.SALES_METHODS.RETURN_FAILED | terminal | 10 | terminal | none | none | continue | Validation, review, package readiness, handoff, initiation, later process/result retrieval, or verification failed; return the detailed failure disclosure and safe next action |

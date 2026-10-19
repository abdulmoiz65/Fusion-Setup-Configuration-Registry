# Manage Sales Status Fresh Export and Package Readiness

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

Verify the final package locally after design validation and before Core Data
Loader handoff. This node validates evidence only; it does not create a Task
Hook preview, request approval, upload, or initiate an import.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Exact export baseline | Require a fresh completed `MOO_MANAGE_SALES_STATUS` task export from the exact target and release, with ProcessId, completion status, export time, baseline path, and baseline SHA-256 |
| 2 | Exact task identity and persisted Data Loader task context | Bind exact `TaskName` `Manage Sales Status` and `TaskCode` `MOO_MANAGE_SALES_STATUS` to the target/release; bind persisted `TaskContextPath` plus positive `TaskSequence`, resolved to the exact skill path, `TaskCode`, `TaskName`, offering, and functional area for the persisted Data Loader task context |
| 3 | Export-derived package contract | Preserve the exact `ASM_SETUP_CSV_METADATA.xml` task identity, member inventory, member paths, filenames, CSV header spelling and order, and row counts from the fresh export |
| 4 | Reviewed delta and state lock | Require every changed status row to have a reviewed operation, exact `OPTY_STATUS` identity, before state or absent-create lock, after state, and a same-target state lock that still matches immediately before handoff |
| 5 | Unrelated-content preservation | Prove all metadata, members, headers, rows, fields, and values outside the reviewed delta remain unchanged |
| 6 | Immutable final artifact | Reopen the final package at `PackagePath`, calculate SHA-256 from those exact bytes, bind `PackageSha256` to the task identity and persisted Data Loader task context and validation receipt, and hand off without child approval |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| sales_status_export_baseline | Fresh completed exact-target task export | Yes | Every FSM package handoff | Verify | Completed `shared.setup-export.task-level-export` result and retained baseline ZIP | verify_sales_status_package_readiness | Package shape and current status state must come from the exact environment and release | Re-export when target, release, task identity, completion, freshness, or baseline bytes cannot be proven | TargetEnvironment; FusionRelease; ExportProcessId; ExportStatus; ExportedAt; BaselinePackagePath; BaselinePackageSha256; TaskCode |
| sales_status_task_context | Exact task identity and persisted Data Loader task context | Yes | Every Core Data Loader mutation handoff | Verify | Catalog-fixed task identity and persisted project task context | verify_sales_status_package_readiness | Prevent wrong-task execution by requiring exact context resolution | Supply persisted `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`; resolve the context to the exact skill path, `TaskCode`, offering, and functional area | SkillPath; TaskCode; TaskName; TaskContextPath; TaskSequence; Offering; FunctionalArea |
| sales_status_package_contract | ASM, member, header, and unrelated-content receipt | Yes | Every FSM package handoff | Verify | Fresh baseline and final package local inspection | verify_sales_status_package_readiness | Prevent hand-authored metadata, invented members, normalized headers, or unrelated edits | Preserve the exact export-derived contract and report every mismatch | AsmTaskIdentity; BaselineMembers; FinalMembers; HeaderReceipt; RowCounts; UnrelatedContentReceipt |
| sales_status_row_delta | Reviewed status-row delta and current-state lock | Yes | Every FSM package handoff | Verify | Fresh baseline rows, proposed rows, and immediate pre-handoff state evidence | verify_sales_status_package_readiness | Import safety depends on an exact reviewed delta whose before state remains current | Rebuild when a code, operation, before state, after state, or state lock differs | ReviewedRowDelta; StateLock; ChangedRowCount |
| sales_status_immutable_handoff | Reopened immutable final package | Yes | Package is ready for Core Data Loader | Verify | Reopened final ZIP and completed task-local validation | verify_sales_status_package_readiness | Data Loader must receive the exact validated bytes | Reopen, hash, and bind the package to the task identity and persisted Data Loader task context; do not request approval in this child | PackagePath; PackageSha256; PackageValidationResult; HandoffStatus |

## Package Readiness Rules

| Check | Ready Condition | Blocked Condition |
|---|---|---|
| Target, release, and export | Export is completed, retrievable, current for the exact target and release, and identifies only `MOO_MANAGE_SALES_STATUS` | Target or release is ambiguous, status is not completed, task code differs, bytes are unavailable, or freshness is unproven |
| Task identity and persisted Data Loader task context | `TaskName` and `TaskCode` are exact; persisted `TaskContextPath` and positive `TaskSequence` resolve to the exact skill path, `TaskCode`, `TaskName`, offering, and functional area | Task identity or context is missing, inconsistent, or resolves to another skill, task, offering, or functional area |
| ASM, members, and headers | Baseline and final ZIPs are readable and safe; each has exactly one case-sensitive `ASM_SETUP_CSV_METADATA.xml` with the exact task identity; member inventory and CSV headers match exactly | ZIP is unsafe, corrupt, encrypted, ambiguous, missing metadata, wrong-task, or differs in member/header contract |
| Delta and state lock | Every changed `OPTY_STATUS` row has one reviewed before/after delta or absent-create lock and the pre-handoff state still matches | An unreviewed row changed, identity is ambiguous, state drifted, or the delta cannot be reproduced |
| Unrelated content | Every nonselected row and every field outside the reviewed delta matches the fresh baseline | A row, field, member, metadata value, or header changed without review |
| Final bytes | Reopening `PackagePath` reproduces `PackageSha256` and all bound task, receipt, delta, and state-lock evidence | Path is missing, bytes changed, hash differs, or evidence refers to another package |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| READY_FOR_DATA_LOADER | Every readiness rule passes for the same immutable package and task identity and persisted Data Loader task context | Handoff only; no upload authorization |
| MISSING | Required export, context, receipt, delta, state-lock, path, or hash evidence is absent | No |
| BLOCKED | Evidence is present but inconsistent, stale, wrong-target, wrong-task, or contains unrelated changes | No |
| FAILED | A package cannot be opened, inspected, or hashed safely | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.SALES_STATUS.PACKAGE | step | 3 | resolve_dependency | ready->OPP.SALES_STATUS.GATE;missing->OPP.SALES_STATUS.RETURN_MISSING;blocked->OPP.SALES_STATUS.RETURN_MISSING;failed->OPP.SALES_STATUS.RETURN_FAILED | OPP.SALES_STATUS.DESIGN | stop | Verify the fresh export, exact task identity and persisted Data Loader task context, export-derived contract, reviewed status delta, current-state lock, unrelated-content preservation, and reopened immutable SHA-256 before Data Loader handoff |

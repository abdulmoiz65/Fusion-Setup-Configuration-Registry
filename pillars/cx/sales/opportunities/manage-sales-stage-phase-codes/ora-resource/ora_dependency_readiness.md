# Manage Sales Stage Phase Codes Fresh Export and Package Readiness

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

Verify route-aware evidence after fresh standard-parent/code resolution and
before final design enforcement or Core Data Loader handoff. This node validates evidence only; it does not create a Task
Hook preview, request approval, upload, or initiate an import. Delete remains
unsupported because no task-specific deletion semantic is documented.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Exact export baseline | Require a fresh completed `MOO_MANAGE_SALES_STAGE_PHASE_CODES` task export from the exact target and release, with ProcessId, completion status, export time, baseline path, and baseline SHA-256 |
| 2 | Exact task identity and persisted Data Loader task context | Bind exact `TaskName` `Manage Sales Stage Phase Codes` and `TaskCode` `MOO_MANAGE_SALES_STAGE_PHASE_CODES` to the target/release; bind persisted `TaskContextPath` plus positive `TaskSequence`, resolved to the exact skill path, `TaskCode`, `TaskName`, offering, and functional area for the persisted Data Loader task context |
| 3 | Export-derived package contract | Preserve the exact `ASM_SETUP_CSV_METADATA.xml` task identity, member inventory, member paths, filenames, CSV header spelling and order, and disclose before/after row counts including reviewed child changes and unchanged support parent from the fresh export schema |
| 4 | Reviewed delta and state lock | Require every changed `MOO_STAGE_PHASE_CD` row to use Create, Update, or Disable, with exact code identity, before state or absent-create lock, after state, and a same-target state lock that still matches immediately before handoff |
| 5 | Unrelated-content preservation | Prove all metadata, members, headers, other phase-code rows, and fields outside the reviewed delta remain unchanged; reject every Delete row |
| 6 | Immutable final artifact | Reopen the final package at `PackagePath`, calculate SHA-256 from those exact bytes, bind `PackageSha256` to the task identity and persisted Data Loader task context and validation receipt, and hand off without child approval |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| stage_phase_export_baseline | Fresh completed exact-target task export | Yes | Every FSM package handoff | Verify | Completed `shared.setup-export.task-level-export` result and retained baseline ZIP | verify_stage_phase_package_readiness | Package shape comes from the current export; live state comes from exact standard lookup reads in the same environment | Re-export when target, release, task identity, completion, freshness, or baseline bytes cannot be proven; valid header-only data uses the documented unchanged-parent recovery | TargetEnvironment; FusionRelease; ExportProcessId; ExportStatus; ExportedAt; BaselinePackagePath; BaselinePackageSha256; TaskCode |
| stage_phase_task_context | Exact task identity and persisted Data Loader task context | Yes | Every Core Data Loader mutation handoff | Verify | Catalog-fixed task identity and persisted project task context | verify_stage_phase_package_readiness | Prevent wrong-task execution by requiring exact context resolution | Supply persisted `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`; resolve the context to the exact skill path, `TaskCode`, offering, and functional area | SkillPath; TaskCode; TaskName; TaskContextPath; TaskSequence; Offering; FunctionalArea |
| stage_phase_package_contract | ASM, member, header, and unrelated-content receipt | Yes | Every FSM package handoff | Verify | Fresh baseline and final package local inspection | verify_stage_phase_package_readiness | Prevent hand-authored metadata, invented members, normalized headers, unrelated edits, or hidden deletes | Preserve the exact export-derived contract and report every mismatch | AsmTaskIdentity; BaselineMembers; FinalMembers; HeaderReceipt; RowCounts; UnrelatedContentReceipt |
| stage_phase_row_delta | Reviewed Create, Update, or Disable delta and current-state lock | Yes | Every FSM package handoff | Verify | Fresh baseline schema, unchanged live parent, proposed children, and fresh standard-code state evidence | verify_stage_phase_package_readiness | Only explicitly supported lifecycle changes may enter the package | Replace a Delete request with a separately reviewed Disable (`Enabled=No`) or end-date Update only when supported by the export; rebuild on state drift | LookupType; LookupCode; Operation; BeforeState; AfterState; ReviewedRowDelta; StateLock |
| stage_phase_immutable_handoff | Reopened immutable final package | Yes | Package is ready for Core Data Loader | Verify | Reopened final ZIP and completed task-local validation | verify_stage_phase_package_readiness | Data Loader must receive the exact validated bytes | Reopen, hash, and bind the package to the task identity and persisted Data Loader task context; do not request approval in this child | PackagePath; PackageSha256; PackageValidationResult; HandoffStatus |

## Standard Parent and Fallback Readiness

| Check | Ready Condition | Blocked Condition |
|---|---|---|
| Standard parent closure | Retain or add one unchanged live MOO_STAGE_PHASE_CD parent row in the current FND_APP_STANDARD_LOOKUP.csv; every changed ORA_FND_APP_STANDARD_LOOKUP_CODE.csv row joins it through FND_APP_STANDARD_LOOKUP.LookupType; added audit fields blank | Parent missing/conflicting/duplicated, child-only package, guessed standard schema or any set-enabled member/selector substituted |
| Final fallback route | Applicable CSV recovery exhausted with same-target receipt and complete reconciliation; REST_FALLBACK proceeds only as fallback_candidate to dedicated verification, without native ZIP/context | Repairable CSV, missing identity/input/context/approval/auth facts, pending/uncertain jobs, partial changes or explicit FSM-only constraint |
| Read-only or Export | Inventory/Read requires exact fresh evidence without a mutation ZIP; full-task Export needs a valid baseline but no changed code/context | Treating read/Export evidence as mutation approval or inferring absence from an empty baseline |

## Package Readiness Rules

| Check | Ready Condition | Blocked Condition |
|---|---|---|
| Target, release, and export | Export is completed, retrievable, current for the exact target and release, and identifies only `MOO_MANAGE_SALES_STAGE_PHASE_CODES` | Target or release is ambiguous, status is not completed, task code differs, bytes are unavailable, or freshness is unproven |
| Task identity and persisted Data Loader task context | `TaskName` and `TaskCode` are exact; persisted `TaskContextPath` and positive `TaskSequence` resolve to the exact skill path, `TaskCode`, `TaskName`, offering, and functional area | Task identity or context is missing, inconsistent, or resolves to another skill, task, offering, or functional area |
| ASM, members, and headers | Baseline and final ZIPs are readable and safe; each has exactly one case-sensitive `ASM_SETUP_CSV_METADATA.xml` with the exact task identity; member inventory and CSV headers match exactly | ZIP is unsafe, corrupt, encrypted, ambiguous, missing metadata, wrong-task, or differs in member/header contract |
| Operation and delta | Every changed row has fixed `LookupType=MOO_STAGE_PHASE_CD` and one reviewed Create, Update, or Disable operation; Create has an absent-code lock, Update has an exact mutable delta, and Disable changes `Enabled` to `No` with any end date explicitly reviewed | Operation is Delete, code identity changes, Create already exists, Update has no delta, Disable does not set `Enabled=No`, or an end date is inferred |
| State lock | Immediate pre-handoff evidence equals every packaged before state or absent-create lock | State is stale, missing, ambiguous, or differs from the reviewed lock |
| Unrelated content | Every nonselected row, metadata value, member, header and field outside reviewed child deltas/unchanged parent linkage matches the baseline | Any unrelated content changed, disappeared, or was added without review |
| Final bytes | Reopening `PackagePath` reproduces `PackageSha256` and all bound task, receipt, delta, and state-lock evidence | Path is missing, bytes changed, hash differs, or evidence refers to another package |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| READY_FOR_DATA_LOADER | Every native FSM readiness rule passes for the same immutable package and task identity and persisted Data Loader task context | Handoff only; no upload authorization |
| MISSING | Required export, context, receipt, delta, state-lock, path, or hash evidence is absent | No |
| BLOCKED | Evidence is inconsistent, stale, wrong-target, wrong-task, contains unrelated changes, or encodes Delete | No |
| FAILED | A package cannot be opened, inspected, or hashed safely | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.STAGE_PHASE.PACKAGE | step | 4 | resolve_dependency | ready->OPP.STAGE_PHASE.DESIGN;not_applicable->OPP.STAGE_PHASE.DESIGN;fallback_required->OPP.STAGE_PHASE.RETURN_FALLBACK_REQUIRED;fallback_candidate->OPP.STAGE_PHASE.VERIFY_FALLBACK;missing->OPP.STAGE_PHASE.RETURN_MISSING;blocked->OPP.STAGE_PHASE.RETURN_MISSING;failed->OPP.STAGE_PHASE.RETURN_FAILED | OPP.STAGE_PHASE.RESOLVE_STATE | stop | Verify native CSV including valid header-only baseline, unchanged standard parent/child closure, exact context/hash/state/impact. Documented final exhaustion alone returns fallback_required; REST_FALLBACK returns fallback_candidate without ZIP/context; reads are not_applicable and Export/Import stay FSM-only |

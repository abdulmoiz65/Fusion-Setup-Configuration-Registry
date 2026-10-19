# Manage Sales Methods and Sales Stages Package Readiness

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

After business design review, require an executable final-package receipt
before Core Data Loader handoff. This dependency creates no preview or
approval and performs no Fusion mutation.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Reviewed design and explicit set choice | Preserve the reviewed sales-method and stage design, provenance, and the user's confirmation to use Common Set or a different exact Set ID/Set Code |
| 2 | Fresh target baseline | Bind a completed MOO_MANAGE_SALES_METHODS_AND_SALES_STAGES export to the exact target environment and release |
| 3 | Exact Data Loader task context | Require TaskCode MOO_MANAGE_SALES_METHODS_AND_SALES_STAGES, TaskName exactly Manage Sales Methods and Sales Stages, matching ASM ObjectShortName, persisted TaskContextPath, positive TaskSequence, and context resolution to this exact skill path, offering, and functional area |
| 4 | Final package contract | Reopen the immutable ZIP and validate exact ASM task identity, complete member graph, exact headers and order, reviewed delta, latest state lock, dependency and unrelated-row preservation, final path, and SHA-256 |
| 5 | Data Loader boundary | Return only handoff-ready evidence; Core Data Loader owns Task Hook preview, later standalone approve, upload, and initiation |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| sales_methods_final_package | Executable exact-task FSM package | Yes | A reviewed design has a final package candidate | Verify | Fresh exact-target task export, reviewed design with explicit set choice, reopened final ZIP, fixed task metadata, persisted TaskContextPath, and positive TaskSequence | verify_sales_methods_final_package | Prevent inferred Common Set, stale, cross-target, wrong-task, structurally altered, state-mismatched, context-mismatched, or hash-mismatched handoff | Confirm Common Set or provide a different exact Set ID/Set Code, then rebuild from the fresh exact-task export and rerun the resolver when any receipt value changes; generate or refresh persisted task context from the resolved project setup-task plan and require exact context resolution before handoff | SetSelectionDecision, SetId, SetCode, target, release, skill path, TaskCode, TaskName, TaskContextPath, TaskSequence, resolved context identities, export receipt, ASM ObjectShortName identity, members, headers, reviewed delta, state lock, preservation result, final path, reopened SHA-256, handoff status |

## Dependency Classification

| Result Category | When Used | Can Continue? |
|---|---|---|
| Ready | Every executable receipt value is exact and the reopened SHA-256 matches | Core Data Loader handoff only |
| Missing | One or more required task-context, export, package, delta, lock, preservation, path, or hash values are absent | No |
| Failed | The final candidate conflicts with the reviewed design, fresh export, resolved task context, or recomputed package evidence | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.SALES_METHODS.PACKAGE_READY | step | 4 | resolve_dependency | ready->OPP.SALES_METHODS.GATE;missing->OPP.SALES_METHODS.RETURN_MISSING;failed->OPP.SALES_METHODS.RETURN_FAILED | OPP.SALES_METHODS.DESIGN | stop | After design review and immediately before immutable package handoff to Core Data Loader |

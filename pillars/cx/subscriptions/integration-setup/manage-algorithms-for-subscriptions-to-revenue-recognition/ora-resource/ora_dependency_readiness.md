# RMCS Algorithm Dependency Readiness

## Scope

Owns this task's phase-specific prerequisites, not companion invocation or downstream process execution. Resolve evidence only through [reference lookups](ora_reference_lookups.md). The manifest owns the primary/companion relationship and saved-stage continuation.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Current input evidence | Pass the current pair's preflight before dependent analysis |
| 2 | Proposal evidence | Resolve affected source, action and target questions before presenting an actionable proposal |
| 3 | Approved local change | Obtain exact persisted proposal/approval and safe artifact scope before local XML preparation |
| 4 | Actual output evidence | Validate the already-created artifact before handing it off |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| RMCSALG.DEP.CONTRACT | Current algorithm and mapping preflight | Yes | Every checkpoint | Verify | Current request's supplied files and local preflight | resolve_rmcs_algorithm_contract | Earlier versions and stale pairs cannot substitute for the requested inputs | Supply the corrected current pair when preflight fails | Current preflight evidence |
| RMCSALG.DEP.MAPPING | Source and configuration decisions | Conditional | proposal, approved_change or artifact_result uses business sources | Verify | Current source-resolution records and recorded user decisions | resolve_rmcs_mapping_contract | A name or physical column alone does not resolve exposure, binding or acceptance | Caller obtains only the affected companion findings/decisions | Matched source decision and outstanding prerequisite references |
| RMCSALG.DEP.APPROVAL | Exact approved local change | Conditional | approved_change or artifact_result | Verify | Persisted current proposal, explicit approval reference and permitted destination | verify_rmcs_approval_evidence | Draft acceptance or an older proposal does not authorize this XML change | Resolve exact approval/persistence gaps through the XML guide | Approval linkage and permitted change scope |
| RMCSALG.DEP.RESULT | Actual local output | Conditional | artifact_result | Verify | Already-created approved local artifact and comparison findings | verify_rmcs_artifact_result | Local XML preparation is not complete until its actual contents match approval | Supply the output for read-only comparison or correct an unauthorized delta | Artifact comparison and final handoff references |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Phase-applicable evidence is current and matches its local resolver | Local checks only; no creation by these nodes |
| Needs decision | A new source/target choice or code-treatment decision is pending | No implicit acceptance; caller obtains the named choice |
| Prerequisite pending | Exposure, runtime semantics or supported structural preparation needed by the proposal is unresolved | No fabricated configuration or XML; return the affected prerequisite |
| Blocked | Identity, authority, approval or artifact evidence fails | No fallback to older input or a live route |

## Integration handoff context

The documented downstream sequence remains reference context only. It is not required to analyze a local file or draft supported Groovy. If the user asks to execute or verify these operations, report the [unsupported live contract](ora_reference_lookups.md#unsupported-live-contracts) and route separately; do not mark it completed.

| Stage | Documented process | Scope |
|---|---|---|
| Source transfer | Send Subscription Revenue Information to Oracle Revenue Management Cloud | Subscription Management |
| Target validation | Validate Customer Contract Source Data | Revenue Management |
| Target identification | Identify Customer Contracts | Revenue Management |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RMCSALG.CHECK_DEPENDENCIES | step | 30 | resolve_dependency | satisfied->RMCSALG.ENFORCE_DESIGN;blocked->RMCSALG.REPORT_ISSUES | RMCSALG.RESOLVE_EVIDENCE | stop | Evaluate phase-applicable local prerequisites only; source questions return to the primary caller rather than crossing task edges. |

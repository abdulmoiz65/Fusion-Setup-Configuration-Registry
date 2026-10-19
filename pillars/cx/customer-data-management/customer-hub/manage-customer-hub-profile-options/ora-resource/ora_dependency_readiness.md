# Dependency Readiness

Preserve the site-only profile contract, shared whole-task FSM export route, Core Data Loader-owned import route, and explicit target-state verification.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Exact target and task | Resolve one configured target environment and the fixed Customer Hub task identity |
| 2 | Current SITE profile state | Read the exact definition and configured SITE value for every requested or changed option |
| 3 | Option-specific prerequisite | Satisfy the documented guardrail for a guarded option before preview |
| 4 | Immutable authorization | Bind approval to the exact direct-update preview or Core Data Loader Task Hook-validated import preview |
| 5 | Execution and verification | Submit once through the declared core route, then verify by read without automatic replay |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| CHP.ENV | Exact Fusion target | Yes | Live export, import, update, or status | Satisfied | One configured target environment selected by the runbook | | Bind the live operation to the intended target | Select one named target environment | Target environment identity and role |
| CHP.SITE_PROFILE_STATE | Current definition and SITE value | Yes | View, update, default request, or changed import row | Verify | Read-only Apps Common profileOptions response | read_customer_hub_profile_definition | Prevent invalid level, stale-value, or unsupported-value changes | Show definition eligibility and current-to-proposed value before preview | ProfileOptionName, current SITE value, SITE flags, level key, validation metadata |
| CHP.GUARDED_OPTION | Guarded option prerequisite | Conditional | Requested code starts with ORA_ZCH_ | Blocked until evidenced | Current Oracle documentation, live definition, and option-specific user evidence | | Guarded options can affect data integrity, logging, survivorship, or enrichment mappings | Satisfy the exact guardrail stated in the enclosing skill before approval | Guardrail evidence and intended business effect |
| CHP.DIRECT_APPROVAL | Exact direct-update approval | Yes | Live update | Blocked until approved | Fingerprint-bound update preview | | Bind target, code, SITE key, current value, proposed value, and warning | Approve the unchanged exact preview immediately before execution | Approval fingerprint and approved change |
| CHP.DATA_LOADER | Immutable Data Loader authorization | Yes | Live import | Blocked until approved | Core Data Loader preview and Task Hook validation envelope | | Bind exact ZIP, environment, task, and validated impact | Complete Data Loader validation and approve its immutable preview | Approved artifact, validation envelope, and fingerprint |
| CHP.PROCESS_RECONCILIATION | Accepted process or uncertain submission evidence | Yes | After import submission attempt | Verify | Returned ProcessId, status, and ProcessLog when available | | Avoid duplicate imports after an uncertain response | Poll or retrieve the existing process; never resubmit automatically | ProcessId, last status, ProcessLog reference |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact target, task, profile membership, and supported operation are present | Continue only to the declared lookup, preview, or status step |
| Verify | Current SITE state, guarded evidence, or accepted process must be reconciled | Read-only verification only |
| Blocked until evidenced | A guarded option prerequisite has not been demonstrated | No preview or mutation |
| Blocked until approved | Exact direct-update or immutable import approval is missing | No live write or import POST |
| Blocked | A mandatory dependency is missing, stale, ambiguous, ineligible, or rejected | Stop and report one corrective action |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CHP.DEPENDENCY_READINESS | decision | 3 | resolve_dependency | satisfied->CHP.APPLY_DEFAULT;blocked->CHP.ERROR | CHP.READ_PROFILE_OPTION | stop | Before default evaluation, design review, immutable preview, approved execution, or status continuation |

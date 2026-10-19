# Benefit Groups Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Run Book | Create or select the project Run Book and confirm it is active before a data-changing action |
| 2 | Data Loader preflight | Validate the immutable Benefit Groups HDL artifact with core.data-loader |
| 3 | Supplied legal employer | Validate LegalEmployer through the workflow-selected read-only LOV; retain unverified_forbidden on 403 |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| active_runbook | Active Run Book | Yes | Create, Update, or Delete | Verify | Project Run Book state | | Associates the approved data load with the implementation task | Create or select a Run Book and confirm active status | Active Run Book context |
| validated_hdl_artifact | Validated HDL artifact | Yes | Create, Update, or Delete | Verify | core.data-loader preflight | | Prevents submission of a changed or malformed artifact | Validate the immutable Benefit Groups HDL artifact | Approved artifact checksum and path |
| supplied_legal_employer | benefitGroups.LegalEmployer | Conditional | An included row supplies LegalEmployer | Verify | Selected read-only legalEmployersLov or another workflow-approved authoritative check | | Distinguishes an invalid value from an access-denied check | Record the field status; 403 is unverified_forbidden and does not fail field validation | Per-row LegalEmployer validation status |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | All mandatory dependencies are verified | No |
| Missing | A mandatory dependency is absent or stale | No |
| Approval blocker | A data-changing action lacks current approval | No |
| unverified_forbidden | The LegalEmployer lookup returned 403 | Continue field validation; obtain authoritative verification before live load |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_GRP.CHECK_READINESS | decision | 30 | resolve_dependency | ready->BEN_GRP.LOOKUP_LEGAL_EMPLOYER;missing->BEN_GRP.HANDLE_ISSUE | BEN_GRP.APPLY_DEFAULTS | stop | Verify active Run Book and immutable Data Loader preflight readiness |

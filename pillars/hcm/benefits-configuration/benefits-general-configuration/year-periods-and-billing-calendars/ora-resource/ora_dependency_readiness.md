# Benefit Year Periods Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Task context | Confirm the selected task and target environment |
| 2 | Immutable artifact | Complete core.data-loader validation and retain the exact resulting artifact |
| 2a | Period type meaning | Validate supplied PeriodTypeMeaning through the workflow-selected read-only LOV; retain unverified_forbidden on 403 |
| 3 | Approval | Obtain the selected Data Loader workflow approval before upload or initiation |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| task_context | Task and target context | Yes | Every import request | Verify | Routed task context | | Binds validation and approval to the correct task and environment | Select the task and target environment | Task code and environment |
| validated_artifact | Immutable HDL artifact | Yes | Every import request | Verify | core.data-loader validation result | | Prevents a changed or malformed source from reaching approval | Validate the exact benefitYearPeriods artifact | Artifact path and integrity evidence |
| period_type_meaning | benefitYearPeriods.PeriodTypeMeaning | Conditional | An included row supplies PeriodTypeMeaning | Verify | Selected read-only commonLookupsLOV or another workflow-approved authoritative check | | Distinguishes an invalid meaning from an access-denied check | Record the field status; 403 is unverified_forbidden and does not fail field validation | Per-row PeriodTypeMeaning validation status |
| approved_load | Current Data Loader approval | Yes | Upload or initiation | Verify | core.data-loader approval record | | Binds the side effect to the validated artifact and environment | Approve the exact validated artifact through the Data Loader workflow | Approval and preview fingerprint |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | All dependencies are verified | No |
| Missing | A required context, artifact, or approval is absent or stale | No |
| Approval blocker | Upload or initiation lacks approval for the exact artifact and target | No |
| unverified_forbidden | The PeriodTypeMeaning lookup returned 403 | Continue field validation; obtain authoritative verification before live load |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_YR.CHECK_READINESS | decision | 20 | resolve_dependency | ready->BEN_YR.LOOKUP_PERIOD_TYPE;missing->BEN_YR.HANDLE_ISSUE | BEN_YR.VALIDATE_REQUEST | stop | Verify target context, immutable Data Loader validation artifact, and approval readiness |

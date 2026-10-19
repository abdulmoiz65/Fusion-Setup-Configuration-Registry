# Pick Slip Grouping Rules Dependency Readiness

## Dependency Boundary

| Dependency | Owner | Local behavior |
|---|---|---|
| Registered business object and live metadata availability | Core Data Loader | Do not persist a visibility assertion. Core Data Loader validates the selected `pickSlipGroupingRules` object during its own execution workflow. |
| Fusion and Data Loader field validation | Fusion and Core Data Loader | Do not duplicate backend validation locally. |
| User clarification for incomplete or ambiguous dates | This task skill | Block the local handoff until the user provides or confirms an unambiguous calendar date. |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---:|---|---|
| 1 | Local normalization | Normalize only supplied grouping flags, catalog code, and unambiguous dates. |
| 2 | Clarification | Resolve missing-year or ambiguous supplied dates without guessing. |
| 3 | Core handoff | Hand the normalized source to `core.data-loader`; that workflow owns current metadata verification, immutable artifact preparation, approval, and submission. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | User Guidance |
|---|---|---|---|---|---|---|---|
| pick_slip_grouping_date_clarification | Unambiguous supplied active date | Conditional | StartDateActive or EndDateActive is supplied | Required when date information is incomplete or ambiguous | User-provided date and clarification | | Supply or confirm the year for a month-and-day date; use an unambiguous calendar date for ambiguous numeric input. |
| pick_slip_grouping_core_handoff | Core Data Loader validation | Yes | After local normalization succeeds | Runtime-owned | Core Data Loader | | Use the selected registered business object `pickSlipGroupingRules`; do not record session-specific metadata visibility here. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| PICKSLIPGROUPING.CHECK_HANDOFF_READINESS | decision | 20 | resolve_dependency | ready->PICKSLIPGROUPING.DATALOADER_HANDOFF;blocked->PICKSLIPGROUPING.RETURN_ISSUES | PICKSLIPGROUPING.NORMALIZE_INPUT | stop | Local normalization and any required date clarification have completed. |

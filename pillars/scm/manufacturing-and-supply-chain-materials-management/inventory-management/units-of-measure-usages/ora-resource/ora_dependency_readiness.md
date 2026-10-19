# Units of Measure Usages Dependency Readiness

## Source Evidence

| Source | Used For |
|---|---|
| Developer-provided BO registration record | unitOfMeasureUsages registration is completed |
| Live Data Loader metadata check in the configured target environment | unitOfMeasureUsages is visible to Data Loader |

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Registered Data Loader business object | Confirm unitOfMeasureUsages remains the governed execution route. |
| 2 | Data Loader metadata visibility | Confirm the selected environment exposes unitOfMeasureUsages before execution planning. |
| 3 | Core Data Loader handoff | Hand the validated setup data to core.data-loader for its normal validation, preview, approval, and import workflow. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| unit_of_measure_usages_bo | Registered Data Loader business object | Yes | Before Data Loader execution | Satisfied | Developer-provided registration record |  | The registered BO is the governed execution route. | Use unitOfMeasureUsages as the Data Loader business object. | businessObject |
| unit_of_measure_usages_loader_visibility | Data Loader metadata visibility | Yes | Before Data Loader execution | Satisfied | Live metadata check in the configured target environment |  | Live metadata exposed unitOfMeasureUsages. | Recheck BO registration and environment access if a future metadata request fails. | Data Loader metadata visibility |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The registered BO and current metadata visibility are available. | Continue to core.data-loader. |
| Blocked | BO registration or metadata visibility is unavailable. | No. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UOMUSAGES.CHECK_DATALOADER_READINESS | decision | 20 | resolve_dependency | ready->UOMUSAGES.DATALOADER_HANDOFF;blocked->UOMUSAGES.RETURN_ISSUES | UOMUSAGES.VALIDATE_EXECUTION_ROUTE | stop | The execution route has passed validation. |

# Dependency Readiness

## Import Readiness

Confirm that the target environment is identified and the operator has the
Functional Setup Manager and Data Loader privileges required by the active
workflow. When the target is the source environment, require an explicit user
confirmation that this is an intended same-environment restore; do not infer it
from an export request.

Require the current task catalog or live task lookup to confirm
`CSVExportImportSupportedFlag=Y`. Treat a fresh archive or changed export,
task identity, target environment, or validation outcome as a new validation
cycle.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| HRPR.DEPENDENCY | decision | 2 | resolve_dependency | satisfied->HRPR.DESIGN_GATE; blocked->HRPR.BLOCKED | HRPR.VALIDATE | stop | After archive validation and before an import preview. |

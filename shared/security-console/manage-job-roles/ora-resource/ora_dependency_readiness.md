# Dependency Readiness

## Import Readiness

Confirm that the target environment is identified and the operator has the
Functional Setup Manager and Data Loader privileges required by the active
workflow. When the target is the source environment, require an explicit user
confirmation that this is an intended same-environment restore; do not infer it
from an export request.

Require the current task catalog or live task lookup to confirm
`CSVExportImportSupportedFlag=Y`. Treat a changed archive, task identity,
target environment, or validation outcome as a new validation cycle.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| MJR.DEPENDENCY | decision | 2 | resolve_dependency | satisfied->MJR.DESIGN_GATE; blocked->MJR.BLOCKED | MJR.VALIDATE | stop | After archive validation and before an import preview. |

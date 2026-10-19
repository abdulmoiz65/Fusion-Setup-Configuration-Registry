# Dependency Readiness

## Import Readiness

Confirm that the target environment is identified and the operator has the
Functional Setup Manager and Data Loader privileges required by the active
workflow. For an actual restore to its source environment, require explicit
user confirmation. Template-based creation, updates and redesign in the target
are intentional configuration changes, not same-environment restores.

Require the current task catalog or live task lookup to confirm
`CSVExportImportSupportedFlag=Y`. Treat a changed archive, task identity,
target environment, or validation outcome as a new validation cycle.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| HLUO.DEPENDENCY | decision | 2 | resolve_dependency | satisfied->HLUO.DESIGN_GATE; blocked->HLUO.BLOCKED | HLUO.VALIDATE | stop | After archive validation and before an import preview. |

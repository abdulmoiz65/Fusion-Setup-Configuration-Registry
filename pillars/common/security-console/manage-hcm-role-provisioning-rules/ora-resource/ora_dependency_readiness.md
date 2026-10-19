# Dependency Readiness

## Import Readiness

Confirm that the target environment is identified and the operator has the
Functional Setup Manager and Data Loader privileges required by the active
workflow. For an actual restore to its source environment, require explicit
user confirmation. Template-based creation, updates and redesign in the target
are intentional configuration changes, not same-environment restores.

Require the current task catalog or live task lookup to confirm
`CSVExportImportSupportedFlag=Y`. Treat a fresh archive or changed export,
task identity, target environment, or validation outcome as a new validation
cycle.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| HRPR.DEPENDENCY | decision | 2 | resolve_dependency | satisfied->HRPR.DESIGN_GATE; blocked->HRPR.BLOCKED | HRPR.VALIDATE | stop | After archive validation and before an import preview. |

# Dependency Readiness

## Import Readiness

Confirm the target environment and required Functional Setup Manager and Data
Loader privileges. Require explicit user confirmation for a same-environment
restore. Confirm from the current task catalog or live lookup that
`CSVExportImportSupportedFlag=Y`. A changed archive, task identity, target, or
validation outcome starts a new validation cycle.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| MDSP.DEPENDENCY | decision | 2 | resolve_dependency | satisfied->MDSP.DESIGN_GATE; blocked->MDSP.BLOCKED | MDSP.VALIDATE | stop | After archive validation and before an import preview. |

# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Validated Data Loader REST artifact | Prepare an immutable XLSX and validated ZIP for workDefinitionDataSecurityObjects through core.data-loader. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| SEC.DEP.ARTIFACT | Validated Data Loader REST artifact | Yes | Every update request | Verify | Immutable ZIP and validation result from core.data-loader | | Submission must use the same live-schema-validated artifact shown in the approval preview. | Validate the prepared workbook with core.data-loader and do not change it after validation. | Validated ZIP name and SHA-256 |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The immutable validated ZIP is confirmed | Yes |
| Blocked | The validated artifact is absent or changed | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SEC.DEPENDENCIES | step | 3 | resolve_dependency | ok->SEC.DESIGN;failure->SEC.FAILED | SEC.DEFAULT | stop | Every Data Loader REST update run |

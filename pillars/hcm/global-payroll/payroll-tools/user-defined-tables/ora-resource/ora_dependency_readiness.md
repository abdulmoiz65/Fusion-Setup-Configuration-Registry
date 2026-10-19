# User-Defined Tables Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Approved table design | Confirm whether the table uses matched or range rows, and approve its table, column, row, and cell-value design. |
| 2 | Effective-date design | Confirm that the intended row and cell values have compatible effective dates. |
| 3 | HDL source validation | Validate the UserDefinedTable hierarchy and source fields before preparation for import. |
| 4 | Core Data Loader handoff | Use core.data-loader as the sole route for the HDL archive validation, preview, approval, upload, and initiation workflow. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| UDT_TABLE_DESIGN | Approved table design | Yes | Every HDL load | Verify | User-approved functional requirements | | The row mode determines the required row attributes and the column design determines the cell matrix. | Confirm the intended table purpose, matched or range row model, columns, and values. | RangeOrMatch, UserRowTitle, UserColumnCode, UserColumnName |
| UDT_EFFECTIVE_DATES | Effective-date design | Yes | Every HDL load | Verify | User-approved functional requirements | | Rows and cell values are date effective. | Provide the effective dates for the table rows and column instances. | EffectiveStartDate, EffectiveEndDate |
| UDT_HDL_ROUTE | Core Data Loader route | Yes | Every Fusion load | Satisfied | Task skill metadata and user instruction | | Setup data must be loaded through the Data Loader route. | Route the validated HDL source to core.data-loader; do not use a direct Fusion API or a manual UI data-entry route to load it. | dataloader_import_mode=HDL, businessObject=UserDefinedTable |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The confirmed source has a complete table design, effective-date design, and Core Data Loader route. | No |
| Blocked | Any required design value or the Core Data Loader route is missing or replaced by another execution route. | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UDT.DEPENDENCY_GATE | step | 3 | resolve_dependency | ready->UDT.DESIGN_GATE;blocked->UDT.RETURN_ISSUES | UDT.APPLY_DEFAULTS | stop | Confirm the approved table design, effective-date design, and Core Data Loader route. |

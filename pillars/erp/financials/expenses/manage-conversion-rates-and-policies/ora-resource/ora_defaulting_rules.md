# Manage Conversion Rates and Policies Defaulting Rules

The same-task blank template establishes package shape. It does not establish values for a new policy. Existing export values are observations from one environment, not universal defaults. No source-proven package default has been identified (`SRC-CODE-EXM-ROOT-EO`, `SRC-CODE-EXM-CHILD-EO`, `SRC-ORACLE-26C-EXPENSE-POLICIES`).

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver | Evidence |
|---|---|---|---|---|---|
No business defaults are established. The table intentionally has no field rows; do not interpret an explanatory placeholder as a CSV field.

The package fields `BuName`, `UserConversionType`, `CurrencyCode`, `DfltExchangeRateFlag`, `DispWarningToUser`, `WarningTolerance`, and `ErrorTolerance` have no established default. Audit fields `CreationDate`, `CreatedBy`, `LastUpdateDate`, `LastUpdatedBy`, and `LastUpdateLogin` retained their headers with empty cells in the observed parent/child creates and updates; Fusion populated or maintained them. Explicit caller overrides are untested (SRC-FSM-EXM-PARENT-20261014; SRC-FSM-EXM-CHILD-20261014). The exact C1 parent-create values are observed inputs, not defaults (`SRC-FSM-EXM-C1-20261001`).

For workbook intake only, an empty field value cell on an existing row is an update instruction to preserve that field's exported value. This is a local merge rule, not a Fusion or FSM default. It requires a fresh, uniquely matching destination export row. Blank values on a new row cannot be filled from source-backed defaults, so the workbook candidate builder blocks them. There is no workbook syntax for clearing an existing value.

The parent and child UI handlers clear **Display warning to user** when the corresponding Warning Tolerance is removed, and the page disables the checkbox while warning is empty (`SRC-CODE-EXM-UI-RULES-20261001`). This is an interactive UI dependency, not a package default or proof that FSM import normalizes `DispWarningToUser`.

<!-- E2E-DISCOVERY:DISC-EXM-CONTRACTS-20261014 -->
## Observed existing-row raw CSV blanks

SRC-FSM-EXM-BLANK-20261014: parent warning/error/display and child warning/error blank cells cleared values; parent type blank preserved the existing type in one case; parent default and child default/display blanks failed FND_CMN_REQ_ATTRIB_API_SERV without observed changes. These are existing-row, full-header observations. New-row omissions and omitted columns remain unproved. Workbook blanks preserve exported values through explicit merge (SRC-FSM-EXM-WORKBOOK-20261014), regardless of raw CSV blank behavior.

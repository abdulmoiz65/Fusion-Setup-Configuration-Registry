# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Task identity | Task code ORA_WIS_MANAGE_DATA_SECURITY_CONTROLS and task name Manage Data Security Controls for Manufacturing | Stop | Select the matching Setup and Maintenance task before preparing the Data Loader REST artifact. | Every update request | |
| Prepared Data Loader REST artifact | A current immutable XLSX source and its Data Loader-validated ZIP for workDefinitionDataSecurityObjects | Stop | Generate or prepare the XLSX from the live registered Data Loader schema, validate it through core.data-loader, and use the resulting ZIP unchanged. | Before Data Loader submission | |
| Supported operation | Update the existing WORK_DEFINITION control only | Stop before execution | Change only DataSecurityEnabledFlag on the existing control; creation and deletion are unsupported. | Every update request | |
| Requested state | Explicit enable or disable instruction, or DataSecurityEnabledFlag=Y or N in the validated Data Loader workbook | Stop before execution | State whether to enable or disable data security, or provide Y or N in the workbook. | Every update request | |
| Supported object identity | DataSecurityObjectCode=WORK_DEFINITION | Stop before preparation | Supply WORK_DEFINITION only. | Every control-data row | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| The Data Loader REST artifact is immutable, validates against workDefinitionDataSecurityObjects, and contains exactly one valid WORK_DEFINITION update row | Satisfied | Continue to Data Loader review and approval. | |
| The workbook or validated ZIP is absent, changed after validation, has zero or multiple control rows, duplicate headers, missing expected headers, or unsupported headers | Blocked | Correct the workbook from the current live schema, rerun core.data-loader validation, and create a new approval preview. | |
| The request attempts to create or delete a control row | Blocked | Remove the create or delete request; this task updates only the existing WORK_DEFINITION control. | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Business object and schema | Accept the artifact only when core.data-loader validates it against the current registered workDefinitionDataSecurityObjects schema. | Before Data Loader submission | |
| Workbook layout preservation | Preserve the supplied worksheet name, headers, and columns from the live Data Loader sample or validated source. Populate only supported fields; do not introduce a worksheet or header. | Preparing the workbook | |
| Workbook encoding and size | Preserve the validated XLSX format and ensure the submitted ZIP is the exact non-empty ZIP produced by core.data-loader validation. | Before Data Loader submission | |
| Artifact-to-task match | Submit only the immutable validated ZIP for Manage Data Security Controls for Manufacturing through core.data-loader. | Before Data Loader submission | |
| The prepared workbook does not contain exactly one control row | Reject it before approval preview. | Preparing the workbook | |
| The input includes Operation, RowAction, RestAction other than PATCH, or another create/delete instruction | Reject it; this task is update-only. | Every request | |
| DataSecurityObjectCode is not WORK_DEFINITION | Reject the unsupported object code. | Every control-data row | |
| DataSecurityEnabledFlag is not Y or N after approved intent defaulting | Reject the requested state. | Every update request | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SEC.VALIDATE | step | 1 | validate_input | ok->SEC.DEFAULT;failure->SEC.FAILED | none | stop | Every Data Loader REST update run |

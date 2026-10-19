# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Customer item source | Confirm a supplied source or prebuilt FBDI ZIP is readable. |
| 2 | Current public Oracle template | Fetch `ItemImportTemplate.xlsm` and bind its source, digest, sheet sequence, filenames, and export columns to the run. |
| 3 | Normalized item mapping | Resolve required or ambiguous business values and disclose unsupported facts. |
| 4 | Generated Item Import ZIP | Validate members, relative order, rows, Batch ID, and digest against the current workbook. |
| 5 | Core Data Loader handoff | Provide the unchanged ZIP and read-only validation evidence to `core.data-loader` with registered business object `item`. |

## Dependency Rules

| Dependency ID | Mandatory | Applies When | Failure action |
|---|---|---|---|
| customer_item_source | Yes | Always | Stop until readable source evidence is supplied. |
| item_import_template_mapping | Yes | Always | Stop until the current public workbook is fetched and recorded. |
| normalized_item_mapping | Yes | For non-ZIP input | Stop until mappings are complete and unambiguous. |
| generated_item_import_zip | Yes | Before handoff | Stop until the ZIP passes local template-driven validation. |
| core_data_loader_handoff | Yes | After validation | Stop until the handoff identifies `core.data-loader` and business object `item`. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ITEM_IMPORT.CONFIRM_LOADER_ROUTE | step | 2 | resolve_dependency | ready->ITEM_IMPORT.HANDOFF_GATE;blocked->ITEM_IMPORT.FAILED | ITEM_IMPORT.VALIDATE_FBDI | stop | Before handing the approved immutable Item Import ZIP unchanged to `core.data-loader`. |
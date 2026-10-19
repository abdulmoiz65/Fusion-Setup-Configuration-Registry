# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Customer Change Order source | Confirm a supplied source or prebuilt FBDI ZIP is readable. |
| 2 | Current public Oracle template | Fetch one current `ChangeOrderImportTemplate.xlsm` workbook/control-file set and bind its source, digest, sheet sequence, filenames, and export columns to the run. Reuse that set for the remaining local cycle. |
| 3 | Normalized Change Order mapping | Resolve required or ambiguous business values and disclose unsupported facts. |
| 4 | Generated or supplied Change Order Import ZIP | Validate members, relative order, rows, Batch ID, and digest against the current workbook. |
| 5 | Core Data Loader handoff | Provide the unchanged ZIP and read-only validation evidence to `core.data-loader` with task business object `Change Order`. |

## Dependency Rules

| Dependency ID | Mandatory | Applies When | Failure action |
|---|---|---|---|
| customer_change_order_source | Yes | Always | Stop until readable source evidence is supplied. |
| change_order_import_template_mapping | Yes | Always | Stop until one current public workbook/control-file set is fetched and recorded; do not fall back to an older template. |
| normalized_change_order_mapping | Yes | For non-ZIP input | Stop until mappings are complete and unambiguous. |
| generated_change_order_import_zip | Yes | Before handoff | For source-data input, generate one ZIP; for a supplied ZIP, retain it unchanged. Stop until that one ZIP passes local template-driven validation; reuse it unchanged unless an input, bound template/control file, or ZIP digest changes. |
| core_data_loader_handoff | Yes | After validation | Stop until the handoff identifies `core.data-loader`, task business object `Change Order`, and its live routing boundary. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CHANGE_ORDER_FBDI.READY | step | 2 | resolve_dependency | ready->CHANGE_ORDER_FBDI.HANDOFF;blocked->CHANGE_ORDER_FBDI.FAILED | CHANGE_ORDER_FBDI.VALIDATE | stop | Before handing the validated Change Order Import ZIP unchanged to `core.data-loader`. |

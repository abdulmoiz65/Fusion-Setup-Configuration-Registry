# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Customer item-structure source | Confirm a supplied source or prebuilt FBDI ZIP is readable. |
| 2 | Latest compatible public Oracle template | Fetch ItemStructureImportTemplate.xlsm and bind its release, source, digest, sheet sequence, filenames, and export columns to the run. |
| 3 | Normalized item-structure mapping | Resolve required or ambiguous business values and validate relationships and effectivity dates. |
| 4 | Generated Item Structure Import ZIP | Validate members, relative order, rows, Batch ID, and digest against the current workbook. |
| 5 | Core Data Loader handoff | Provide the unchanged ZIP and read-only validation evidence to core.data-loader with registered business object item. |

## Dependency Rules

| Dependency ID | Mandatory | Applies When | Failure action |
|---|---|---|---|
| customer_item_structure_source | Yes | Always | Stop until readable source evidence is supplied. |
| item_structure_template_mapping | Yes | Always | Stop until the current compatible workbook is fetched and recorded. |
| normalized_item_structure_mapping | Yes | For non-ZIP input | Stop until mappings, relationships, and dates are complete and unambiguous. |
| generated_item_structure_import_zip | Yes | Before handoff | Stop until the ZIP passes local template-driven validation. |
| core_data_loader_handoff | Yes | After validation | Stop until the handoff identifies core.data-loader and business object item. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ITEM_STRUCTURE_IMPORT.CONFIRM_LOADER_ROUTE | step | 2 | resolve_dependency | ready->ITEM_STRUCTURE_IMPORT.HANDOFF_GATE;blocked->ITEM_STRUCTURE_IMPORT.FAILED | ITEM_STRUCTURE_IMPORT.VALIDATE_FBDI | stop | Before handing the approved immutable Item Structure Import ZIP unchanged to core.data-loader. |

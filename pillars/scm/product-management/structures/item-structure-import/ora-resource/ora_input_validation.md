# Input Validation

Validate customer item-structure data or a prebuilt Item Structure Import FBDI
ZIP against the latest release-compatible public Oracle template before the
immutable handoff to `core.data-loader`.

| Requirement | Validation gate | Failure action |
|---|---|---|
| Source or ZIP | Readable customer source or a readable ZIP is present | Stop before mapping. |
| Current template | Public ItemStructureImportTemplate.xlsm, Oracle release, URLs, retrieval time, digest, and sheet sequence are recorded | Stop; never use a remembered or cross-release layout. |
| Mapping | Every required source fact maps to the current template | Stop for missing or ambiguous values. |
| Structure integrity | Component dates do not overlap; reference-designator dates match their component; parent components accompany substitutes and reference designators | Stop and correct the source. |
| CSV and ZIP shape | Headerless CSVs, exact filenames, ordered root-level members, safe paths, and exact field counts | Stop and regenerate. |
| Data validity | Current-template types, constraints, relationships, and one numeric Batch ID pass | Stop and correct the source. |
| Immutable evidence | ZIP digest, member manifest, row counts, template provenance, and mapping preview are present | Stop before handoff. |
| Data Loader route | Handoff identifies registered FBDI Data Loader business object item | Stop and correct the task configuration. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ITEM_STRUCTURE_IMPORT.VALIDATE_FBDI | step | 1 | validate_input | valid->ITEM_STRUCTURE_IMPORT.CONFIRM_LOADER_ROUTE;invalid->ITEM_STRUCTURE_IMPORT.FAILED | none | stop | Validate source, latest compatible template, prerequisites, package, and immutable evidence before handoff. |

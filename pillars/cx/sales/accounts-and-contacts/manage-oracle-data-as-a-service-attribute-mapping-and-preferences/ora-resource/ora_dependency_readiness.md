# Dependency Readiness

The selected-row package depends on the sanitized complete seeded catalog and a
fresh task-level export. Mapping-field changes additionally depend on complete,
fresh target-environment Fusion object metadata.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---:|---|---|
| 1 | Complete seeded-row catalog | Validate the tracked catalog manifest, SHA-256, 268-row count, 20-column schema, and unique composite keys |
| 2 | Fresh pod export | Validate the task metadata, CSV member names, member schemas, and current rows before applying changes |
| 3 | Live Fusion attribute metadata | For mapping-field changes, retrieve and completely validate `AttributeCode` values for every distinct effective object |
| 4 | Immutable prepared ZIP | Build only selected rows, compute SHA-256, and retain the preview for Data Loader |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| complete_seeded_rows | Complete Oracle-seeded DaaS row catalog | Yes | Package preparation | Satisfied when manifest, hash, schema, row count, and unique keys validate | assets/seeded-attribute-mappings.csv and assets/seeded-attribute-mappings.json | | Supplies rows omitted from a normal export because they remain seeded and unchanged | Correct the source asset through reviewed skill authoring if validation fails | Baseline row by AttributeCategory and DaasAttributeName |
| fresh_task_export | Current task-level FSM export | Yes | Package preparation and import | Satisfied when the export process and package validation succeed | shared.setup-export.task-level-export result | | Preserves current changed values plus pod-specific metadata and ZIP structure | Export the fixed task from the selected environment | Current row when present, metadata, member headers, ZIP structure |
| live_fusion_attributes | Complete target-pod object metadata | Conditional | A requested change includes `FusionObjectName` or `FusionAttributeName` | Satisfied when every distinct nonblank effective object has one complete current response and every nonblank attribute exactly matches one `AttributeCode` | `core.fusion-api.rest-api-client` GET through `validate_fusion_mapping_attributes` | validate_fusion_mapping_attributes | Prevents invalid or environment-incompatible object/attribute mappings from reaching FSM import | Correct the object/attribute pair or restore metadata access; never use a hardcoded or documentation-only list | Effective object name, exact attribute code, response hash, count, sanitized target identity |
| immutable_import_package | Selected-row import ZIP | Yes | Import | Satisfied when the package preview and SHA-256 match the exact ZIP | Local package builder output | | Binds validation and Data Loader approval to one artifact | Rebuild preview after any byte or requested-value change | ZIP path and SHA-256 |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | All required local, export, and conditional live-metadata artifacts validate | Run only the declared read-only attribute lookup when a mapping field changes; otherwise continue locally |
| Blocked | Catalog, export, schema, live metadata, mapping pair, or fingerprint validation fails | No additional lookup or write; stop and correct the named artifact or access gap |
| Fusion rejection | Approved import returns authorization or business validation errors | No automatic retry; preserve the process result and stop |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| DAAS.RESOLVE_ROW_SOURCE | step | 2 | resolve_dependency | ready->DAAS.RESOLVE_FUSION_ATTRIBUTES;blocked->DAAS.ERROR | DAAS.VALIDATE_REQUEST | stop | Before selected-row package preparation |

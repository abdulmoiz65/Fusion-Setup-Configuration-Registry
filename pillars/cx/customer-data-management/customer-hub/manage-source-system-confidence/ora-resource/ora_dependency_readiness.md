# Manage Source System Confidence Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Seeded source-system catalog | Resolve each confidence OrigSystem against assets/source-systems.json |
| 2 | Custom source-system export | For only the values unresolved at sequence 1, require the Manage Trading Community Source Systems dependency and resolve against its HZ_ORIG_SYSTEMS_B.csv |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| seeded_confidence_orig_system | Seeded source-system catalog | Yes | For every nonblank confidence OrigSystem before an import preview | Verify | ORA_ZCH_CONFIDENCE_LEVEL.csv and assets/source-systems.json | resolve_seeded_source_system | A seeded source-system value can be validated without a dependency task export | Use an exact seeded value or continue unresolved values to custom source-system resolution; do not change the catalog | Per confidence row: OrigSystem and seeded match status |
| custom_confidence_orig_system | Manage Trading Community Source Systems | Conditional | Only when resolve_seeded_source_system leaves one or more confidence OrigSystem values unresolved | Verify | The complete dependency task export containing HZ_ORIG_SYSTEMS_B.csv | resolve_custom_source_system | A non-seeded confidence value must reference a custom source system defined by the dependency task | Supply the dependency task export and an exact custom source-system row, or correct the confidence value | Per unresolved confidence row: OrigSystem and matching HZ_ORIG_SYSTEMS_B.csv row |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every nonblank confidence OrigSystem is resolved first by the seeded catalog or, when unresolved there, by exactly one row in the custom source-system CSV | Continue to success; no source-system value is created |
| Conditional dependency required | At least one confidence OrigSystem is absent from the seeded catalog | Require the complete Manage Trading Community Source Systems export and run resolve_custom_source_system |
| Blocked | A mandatory artifact is missing or malformed, a confidence OrigSystem is blank, the conditional export is unavailable when required, or a value has no exact custom match | No; correct the applicable artifact evidence and restart validation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SSC.CHECK_DEPENDENCY | decision | 20 | resolve_dependency | ready->SSC.CLASSIFY_ATTRIBUTE_NAME;blocked->SSC.HANDLE_ERROR | SSC.VALIDATE_INPUT | stop | The confidence CSV and seeded catalog are available; the custom source-system export is required only for unresolved values, and successful resolution continues to object-attribute validation |

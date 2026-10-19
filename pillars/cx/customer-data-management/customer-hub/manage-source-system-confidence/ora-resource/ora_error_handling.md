# Manage Source System Confidence Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| The confidence CSV, its OrigSystem header, or the seeded source-system catalog is missing or malformed | Classify input_validation, identify the missing or malformed artifact or header, and stop before preview |
| A confidence OrigSystem is blank | Classify input_validation, identify the confidence CSV row, and stop before preview |
| A confidence OrigSystem is absent from the seeded catalog and the complete Manage Trading Community Source Systems export containing HZ_ORIG_SYSTEMS_B.csv is unavailable | Classify dependency_not_ready, identify the confidence row and value, require the conditional dependency export, and stop before preview |
| A confidence OrigSystem is absent from the seeded catalog and has zero or multiple exact matches in HZ_ORIG_SYSTEMS_B.csv | Classify dependency_not_ready, identify the confidence row and value, and stop before preview |
| ObjectName or AttributeName is blank | Classify input_validation, identify the affected confidence request, and stop before preview |
| A standard ObjectName or AttributeName has zero or multiple exact matches in assets/object-attributes.json, or its aligned column mapping is invalid | Classify object_attribute_catalog_mismatch, disclose the unresolved pair and catalog identity, and stop before preview |
| A custom ObjectName cannot map to Account or Contact | Classify attribute_metadata_mismatch, disclose the unsupported ObjectName, and stop before the metadata request |
| Custom attribute metadata is unavailable, incomplete, duplicated, from another target or object, lacks an exact AttributeCode match, or returns a blank AttrColumn | Classify attribute_metadata_mismatch, disclose the sanitized metadata gap, and stop before preview |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| input_validation | The confidence CSV, its OrigSystem header, the seeded catalog, or a required confidence OrigSystem value is missing or invalid | Supply or correct the mandatory local artifact and rerun validation |
| dependency_not_ready | A value unresolved by the seeded catalog cannot be validated from exactly one row in the conditionally required custom source-system export | Supply or correct the dependency task export, confidence value, or custom source-system row and rerun validation |
| object_attribute_catalog_mismatch | A standard ObjectName or AttributeName has zero or multiple exact catalog matches, or attr_names cannot supply one aligned column_names value | Correct the exact object-attribute pair or reviewed catalog; do not continue to preview |
| attribute_metadata_mismatch | A custom ObjectName cannot map, the metadata response is incomplete or inconsistent, AttributeCode has zero or multiple exact matches, or AttrColumn is blank | Correct ObjectName or AttributeName, or restore complete target metadata access; do not continue to preview |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Dependency failure | Confidence CSV row number, supplied OrigSystem value, resolver result, applicable reference checked, and one correction path |
| Dependency success | Number of confidence OrigSystem values checked, seeded versus custom resolution counts, and confirmation that every value has an exact match |
| Object-attribute failure | Supplied ObjectName and AttributeName, standard or custom branch, applicable catalog or sanitized target evidence, failure reason, and one correction path |
| Object-attribute success | Validated ObjectName and AttributeName, validation branch, resolved output mappings, and catalog or sanitized metadata evidence |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Dependency evidence is missing or fails | Do not create a confidence import preview or submit an import |
| A near match exists in an applicable source | Do not silently trim, case-normalize, infer, or create a source-system value |
| A standard object-attribute pair is absent or ambiguous in the local catalog | Do not fall back to objectMetadata or substitute a similar, normalized, custom, or caller-asserted value |
| A custom object-attribute validation fails | Do not fall back to attr_names, accept a blank AttrColumn, or substitute a similar, normalized, documented, or caller-asserted value |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SSC.HANDLE_ERROR | step | 60 | error_handler | handled->SSC.ISSUES | none | continue | Input validation, source-system dependency validation, or object-attribute validation fails |
| SSC.ISSUES | terminal | 70 | terminal | none | none | continue | The request has unresolved source-system or object-attribute validation issues |
| SSC.DONE_STANDARD | terminal | 80 | terminal | none | SSC.VALIDATE_OBJECT_ATTRIBUTE | continue | SourceSystem, ObjectName, and standard AttributeName validation passed |
| SSC.DONE_CUSTOM | terminal | 90 | terminal | none | SSC.RESOLVE_ATTRIBUTE_NAME_METADATA | continue | SourceSystem, ObjectName, custom AttributeName, and AttrColumn validation passed |

# Manage Source System Confidence Input Validation

Validate the confidence CSV, object-attribute input, and seeded source-system
catalog before preview. Require the source-system export only when one or more
confidence values are absent from the seeded catalog. Source-system matching
belongs to the local lookup and dependency rules; object-attribute lookup
mechanics belong to the reference lookup rules.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Confidence data | A readable ORA_ZCH_CONFIDENCE_LEVEL.csv with an OrigSystem header | Block before dependency validation | Supply the proposed confidence CSV with its unchanged rows | Before a confidence import preview | |
| Seeded source-system catalog | A readable, structurally valid task-local assets/source-systems.json catalog | Block before dependency validation | Restore or correct the task-local seeded catalog | Before resolving any confidence OrigSystem | resolve_seeded_source_system |
| Custom source-system reference data | A complete Manage Trading Community Source Systems export containing a readable HZ_ORIG_SYSTEMS_B.csv with an OrigSystem header | Block custom source-system resolution | Supply or regenerate the dependency task export | Only when resolve_seeded_source_system leaves one or more confidence OrigSystem values unresolved | resolve_custom_source_system |
| Object-attribute input | Nonblank ObjectName and AttributeName | Block before object-attribute validation | Supply an exact object name and a nonblank standard or custom attribute name | Before adding or modifying a confidence row | |
| Object-attribute catalog | A readable, structurally valid task-local assets/object-attributes.json catalog | Block before object-attribute validation | Restore or correct the task-local object catalog | Before validating any standard or custom AttributeName | validate_object_attribute_reference |
| Custom attribute metadata | One complete target-environment objectMetadata response for the ObjectCode mapped from ObjectName | Block before confidence import preview | Route the documented read-only lookup through validate_attribute_name_metadata | AttributeName ends with the case-sensitive suffix _c | validate_attribute_name_metadata |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| AttributeName does not end with _c | Continue only when ObjectName matches exactly one object_name and AttributeName matches exactly one aligned attr_names entry for that object in assets/object-attributes.json | Retain the validated object, attribute, and output-column values from the catalog | validate_object_attribute_reference |
| AttributeName ends with _c | Continue only when ObjectName maps to Account or Contact and AttributeName matches exactly one AttributeCode with a nonblank AttrColumn in complete target-environment metadata | Retain the validated object, AttributeCode, AttrColumn, and sanitized metadata evidence | validate_attribute_name_metadata |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Confidence CSV identity | Require the exact basename ORA_ZCH_CONFIDENCE_LEVEL.csv | Always | |
| Confidence OrigSystem header | Require exactly one OrigSystem header in ORA_ZCH_CONFIDENCE_LEVEL.csv | Always | |
| Confidence OrigSystem value | Reject a blank OrigSystem value in any ORA_ZCH_CONFIDENCE_LEVEL.csv data row | Always | |
| Seeded source-system catalog | Require assets/source-systems.json to be readable and to contain the expected catalog identity, schema version, and orig_systems array | Always | resolve_seeded_source_system |
| Custom CSV identity | Require the exact basename HZ_ORIG_SYSTEMS_B.csv from the complete dependency task export | Only when at least one value is unresolved by resolve_seeded_source_system | resolve_custom_source_system |
| Custom OrigSystem header | Require exactly one OrigSystem header in HZ_ORIG_SYSTEMS_B.csv | Only when at least one value is unresolved by resolve_seeded_source_system | resolve_custom_source_system |
| ObjectName and AttributeName presence | Reject a blank ObjectName or AttributeName | Before adding or modifying a confidence row | |
| AttributeName classification | Classify a case-sensitive _c suffix as custom and every other nonblank value as standard; do not trim, case-fold, or normalize ObjectName or AttributeName | Before object-attribute validation | |
| Standard object-attribute validity | Require exactly one case-sensitive ObjectName match in object_name and one case-sensitive AttributeName match in that object's attr_names; use the aligned column_names entry | AttributeName does not end with _c | validate_object_attribute_reference |
| Custom object-attribute validity | Map exact ObjectName Organization to Account or Person to Contact; require exactly one case-sensitive AttributeCode match with a nonblank AttrColumn in complete target-environment metadata | AttributeName ends with _c | validate_attribute_name_metadata |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SSC.VALIDATE_INPUT | step | 10 | validate_input | valid->SSC.CHECK_DEPENDENCY;invalid->SSC.HANDLE_ERROR | none | stop | Before resolving seeded and, when required, custom source-system references |
| SSC.CLASSIFY_ATTRIBUTE_NAME | decision | 30 | validate_input | standard->SSC.VALIDATE_OBJECT_ATTRIBUTE;custom->SSC.RESOLVE_ATTRIBUTE_NAME_METADATA;invalid->SSC.HANDLE_ERROR | SSC.CHECK_DEPENDENCY | stop | The source-system dependency passed and nonblank ObjectName and AttributeName must be classified |
| SSC.VALIDATE_OBJECT_ATTRIBUTE | step | 40 | validate_input | valid->SSC.DONE_STANDARD;invalid->SSC.HANDLE_ERROR | SSC.CLASSIFY_ATTRIBUTE_NAME | stop | AttributeName does not end with _c and the exact object-attribute pair must be evaluated against assets/object-attributes.json |

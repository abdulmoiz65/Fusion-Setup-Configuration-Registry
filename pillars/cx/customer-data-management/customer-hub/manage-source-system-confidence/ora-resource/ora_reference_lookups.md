# Manage Source System Confidence Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_seeded_source_system | The confidence CSV and structurally valid seeded catalog are available | Each nonblank ORA_ZCH_CONFIDENCE_LEVEL.csv OrigSystem and assets/source-systems.json orig_system values | Require a case-sensitive, character-for-character equal value in the seeded catalog; do not trim, case-fold, normalize, infer, or create a value | Per confidence row: OrigSystem and matching catalog entry | Pass an unmatched value to resolve_custom_source_system; block if the catalog is missing or malformed, or if the exact value occurs more than once |
| resolve_custom_source_system | resolve_seeded_source_system leaves one or more values unresolved | Each unresolved confidence OrigSystem and all OrigSystem values in HZ_ORIG_SYSTEMS_B.csv from the complete Manage Trading Community Source Systems export | Require exactly one case-sensitive, character-for-character equal CSV value; do not trim, case-fold, normalize, infer, or create a value | Per unresolved confidence row: OrigSystem and matching HZ_ORIG_SYSTEMS_B.csv row | Block the dependency; record the confidence row number and supplied value when the required export is missing or when zero or multiple exact CSV matches exist |
| validate_object_attribute_reference | AttributeName is nonblank and does not end with _c | Exact ObjectName, exact AttributeName, and assets/object-attributes.json | Require exactly one case-sensitive object_name match to ObjectName and exactly one case-sensitive attr_names match to AttributeName within that object; use the column_names value at the same array position and do not trim, case-fold, or normalize either input | For new rows: TableName from table_name, AttributeName from attr_names, ColumnName from aligned column_names, ObjDef from object_def, and ObjName from object_type; for existing rows: validated object-attribute evidence only | Missing or duplicate object or attribute matches, unequal attr_names and column_names lengths, or a missing aligned column blocks before preview; do not use live metadata as a fallback |
| resolve_object_name_metadata_code | AttributeName ends with _c | Exact ObjectName and assets/object-attributes.json | Require exactly one case-sensitive object_name match, then map Organization to Account or Person to Contact | ObjectCode for the live metadata request; TableName from table_name, ObjDef from object_def, and ObjName from object_type | Any unsupported, missing, or duplicate ObjectName blocks before the live lookup |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| validate_attribute_name_metadata | AttributeName ends with _c after ObjectName resolves to a supported ObjectCode | Exact ObjectName, ObjectCode from resolve_object_name_metadata_code, exact nonblank AttributeName, limit=1000, offset=0, onlyData=true, and totalResults=true | /crmRestApi/resources/11.13.18.05/objectMetadata/{ObjectCode}/child/attributes through the Data Loader read-only validation route | AttributeCode, AttrColumn, count, totalResults, and hasMore | Require one complete response for the mapped object with hasMore=false and count=totalResults=items.length; require exactly one case-sensitive AttributeCode match to AttributeName and require that item's AttrColumn to be nonblank | For new rows: AttributeName from AttributeCode, ColumnName from AttrColumn, and the locally resolved TableName, ObjDef, and ObjName; for existing rows: validated AttributeCode and AttrColumn evidence only; retain sanitized target identifier, response SHA-256, and attribute count | Stop before preview when metadata is unavailable, incomplete, duplicated, from a different target or object, has zero or multiple exact AttributeCode matches, or returns a blank AttrColumn; do not fall back to the local attribute list |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A confidence OrigSystem value exactly matches one seeded catalog value | Record the catalog match as local validation evidence; do not require the dependency task export for that value |
| A confidence OrigSystem value has no exact seeded catalog match | Mark the value unresolved and invoke resolve_custom_source_system |
| One or more values require custom resolution | Require the complete Manage Trading Community Source Systems export containing HZ_ORIG_SYSTEMS_B.csv before checking those values |
| An unresolved confidence OrigSystem exactly matches one custom CSV value | Record the CSV row as local validation evidence |
| A confidence OrigSystem differs only by case, whitespace, or another character from every applicable reference value | Treat it as no match; report the supplied value without changing the confidence CSV, custom CSV, or seeded catalog |
| Standard AttributeName validation is required | Match exact ObjectName to object_name and exact AttributeName to attr_names, then obtain ColumnName from the aligned column_names entry; do not call objectMetadata |
| Custom AttributeName validation is required | Resolve exact ObjectName through the local catalog, map Organization to Account or Person to Contact, then call only the documented read-only objectMetadata lookup |
| A custom AttributeCode match is found | Set AttributeName from AttributeCode and ColumnName from the matching nonblank AttrColumn when constructing a new row; preserve existing output columns when modifying an existing row |
| ObjectName or AttributeName differs only by case, whitespace, or another character from its applicable reference | Treat it as no match; do not normalize, infer, or substitute a value |
| A branch-specific lookup fails | Stop before preview; do not fall back between the standard local catalog and custom live metadata branches |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SSC.RESOLVE_ATTRIBUTE_NAME_METADATA | step | 50 | reference_lookup | resolved->SSC.DONE_CUSTOM;blocked->SSC.HANDLE_ERROR;failure->SSC.HANDLE_ERROR | SSC.CLASSIFY_ATTRIBUTE_NAME | stop | AttributeName ends with _c and exact ObjectName maps to a supported objectMetadata ObjectCode |

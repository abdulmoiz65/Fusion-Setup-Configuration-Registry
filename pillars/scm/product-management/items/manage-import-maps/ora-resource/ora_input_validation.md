# Manage Import Maps Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Conditional import-map format values | Delimiter, FileType, DateFormat, EncodingType, TimestampFormat as an explicit LookupCode or as a display value | Apply the documented create default when a field is missing, null, or whitespace-only; preserve an omitted update field; block a supplied or defaulted display value that is not resolved | Apply create-only defaults, then resolve each supplied or defaulted display value through its named standard-lookup resolver | A create or update request is prepared |  |
| Destination attribute selection | A lookup selection or destination attribute identity sufficient to identify exactly one current importMapAttributes item | Block the destination child row | Resolve and validate all destination payload values through one exact importMapAttributes item | A destination mapping is requested | resolve_import_map_destination_attributes |
| Source-to-destination mapping | SourceColumn for every requested destination mapping | Reject the mapping request | Supply the corresponding SourceColumn; a source-only mapping is accepted | A destination mapping is requested |  |
| Transformation source | SourceColumn for every supplied transformation or expression | Reject the transformation | Supply the source column that owns the destination child and transformation | A transformation or expression is supplied on the REST Data Loader route |  |
| Transformation destination | A destination mapping containing the transformation child | Return MISSING without preparing a workbook or DAT | Ask for and resolve the destination mapping; transformations are children of destination resources | A transformation or expression is supplied without a destination mapping on the REST Data Loader route |  |
| Transformation expression | A nonblank ExpressionCode containing the full expression syntax | Reject the transformation | Supply ExpressionCode so its function can be validated through importMapFunctions | A transformation child is supplied on the REST Data Loader route | resolve_import_map_transformation_function |
| Transformation return attribute | The transformation's resolved destination mapping | Block the transformation when the destination item is unresolved | Build ReturnAttributeName from the same exact importMapAttributes item as EntityName.AttributeGroupName.AttributeCode and append .LanguageCode only when LanguageCode is non-null | A transformation child is supplied on the REST Data Loader route | resolve_import_map_transformation_return_attribute |
| Transformation source columns | The current SourceColumn and all participating source-column names in supplied order | Reject the transformation | Derive SourceColumns as current SourceColumn + $!$ + all participating source-column names joined by $&#124;$, including the current source again in the suffix | A transformation child is supplied on the REST Data Loader route |  |
| Source IgnoreFlag | Destination-child presence for each source child | Normalize the payload | Set IgnoreFlag to Y when the source child has no destination child; otherwise set IgnoreFlag to N | A source child is prepared |  |
| Import route | An explicit REST Data Loader or FSM task-level ZIP operation | Stop for a route choice | Select REST for itemImportMaps workbook or DAT work; select FSM for an exported task-level ZIP | Before route-specific validation |  |
| FSM task-level ZIP | An immutable ZIP for task code EGI_MANAGE_IMPORT_MAPS with readable task CSV files | Block Data Loader approval and upload | Supply an intact task-level ZIP; preserve every CSV and expression record unchanged for the core.data-loader Task Hook workflow | The FSM task-level ZIP route is selected |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A listed import-map field has an explicit LookupCode | Satisfied | Preserve the supplied code; the display-value resolver is not applicable |  |
| A create request omits a defaultable field or supplies it as null or whitespace-only | Default | Apply the documented create default before lookup resolution |  |
| An update request omits a defaultable field or supplies no replacement value | Satisfied | Preserve the existing record value; do not apply a create default |  |
| A listed import-map field has a supplied or defaulted display value | Lookup | Resolve exactly one LookupCode before workbook preparation |  |
| A destination mapping is requested | Lookup | Validate one exact current importMapAttributes item and derive every applicable destination payload field from it, including LanguageCode when non-null | resolve_import_map_destination_attributes |
| Source columns are supplied and destination columns are omitted | Satisfied | Accept the source-only mapping; no destination-attribute lookup is applicable |  |
| A destination mapping is requested without its corresponding SourceColumn | Invalid | Reject the request before lookup, preview, or Data Loader handoff |  |
| A REST transformation or expression is supplied without a destination mapping | Missing | Return MISSING and ask for the destination mapping before function lookup, preview, or Data Loader handoff |  |
| A REST transformation has a destination mapping and a nonblank ExpressionCode | Lookup | Validate the parsed function through importMapFunctions, then derive ReturnAttributeName and SourceColumns | resolve_import_map_transformation_function |
| No REST transformation or expression is supplied | Satisfied | Do not synthesize a transformation child or derive transformation-only attributes |  |
| The operation or artifact identifies the REST Data Loader route | Satisfied | Continue directly to MIM.VALIDATE_INPUT |  |
| The operation or artifact identifies an FSM task-level ZIP | Validate | Continue to MIM.VALIDATE_FSM_ZIP without applying REST transformation validation |  |
| The import route is absent or ambiguous | Missing | Stop at MIM.AWAIT_ROUTE and request an explicit REST Data Loader or FSM task-level ZIP choice |  |
| An FSM ZIP contains transformations or expressions | Satisfied | Preserve the immutable ZIP and expression data unchanged; Fusion FSM performs semantic validation |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Delimiter is a resolved lookup code | A supplied or defaulted display value alone is not written to the Data Loader field; resolve it with lookup type ORA_EGI_IMP_MAP_DELIMITER | Delimiter is supplied or defaulted without an explicit LookupCode | resolve_import_map_delimiter |
| FileType is a resolved lookup code | A supplied or defaulted display value alone is not written to the Data Loader field; resolve it with lookup type ORA_EGI_IMP_MAP_FILE_TYPE | FileType is supplied or defaulted without an explicit LookupCode | resolve_import_map_file_type |
| DateFormat is a resolved lookup code | A supplied or defaulted display value alone is not written to the Data Loader field; resolve it with lookup type DATE_FORMAT | DateFormat is supplied or defaulted without an explicit LookupCode | resolve_import_map_date_format |
| EncodingType is a resolved lookup code | A supplied or defaulted display value alone is not written to the Data Loader field; resolve it with lookup type EGI_ENCODING_TYPE | EncodingType is supplied or defaulted without an explicit LookupCode | resolve_import_map_encoding_type |
| TimestampFormat is a resolved lookup code | A supplied or defaulted Timestamp display value alone is not written to the Data Loader field; resolve it with lookup type EGI_TIME_STAMP | TimestampFormat is supplied or defaulted without an explicit LookupCode | resolve_import_map_timestamp_format |
| Destination payload comes from one REST result | Copy EntityName to DestinationEntity, AttributeGroupName to AttributeGroupName, AttributeCode to DestinationColumn, AttributeName to AttributeName, and non-null LanguageCode to LanguageCode from the same exact current importMapAttributes item | A destination mapping is requested | resolve_import_map_destination_attributes |
| Destination response shape is complete | Block when the matched item lacks EntityName, AttributeGroupName, AttributeCode, or AttributeName; permit LanguageCode omission only when the matched response value is null | A destination mapping is requested | resolve_import_map_destination_attributes |
| Destination LanguageCode preserves the resolved value | When the matched item has a non-null LanguageCode, require the destination child to contain that exact value; do not infer, normalize, omit, or retain a conflicting independently supplied value | A destination mapping is requested and the matched importMapAttributes item has a non-null LanguageCode | resolve_import_map_destination_attributes |
| Destination entity is not a root-node lookup code | Do not populate DestinationEntity from ORA_EGI_IMPORT_MAP_ROOT_NODES; use EntityName from the matched importMapAttributes item | A destination mapping is requested | resolve_import_map_destination_attributes |
| Source-only mappings are valid | A SourceColumn may be supplied when DestinationColumn is omitted; do not require destination metadata for that row | A SourceColumn is supplied and DestinationColumn is omitted |  |
| Destination mappings require source columns | Reject the request when any requested destination mapping lacks its corresponding SourceColumn | A destination mapping is requested |  |
| Transformations are destination children | Preserve each supplied transformation under its destination child; return MISSING when only a transformation or expression is supplied | A transformation or expression is supplied on the REST Data Loader route |  |
| Transformation function is resolver-validated | Parse the candidate function name from trimmed ExpressionCode before the first opening parenthesis, or use the whole trimmed value when no opening parenthesis exists, and require one exact case-sensitive trimmed FunctionName match | A transformation child is supplied on the REST Data Loader route | resolve_import_map_transformation_function |
| Transformation syntax mismatch is advisory | Compare trimmed ExpressionCode with trimmed FunctionSyntax; when they differ, continue with the supplied ExpressionCode and disclose FunctionSyntax and Examples | A transformation function resolves exactly once but its syntax differs | resolve_import_map_transformation_function |
| Transformation return attribute is resolver-owned | Build ReturnAttributeName from EntityName.AttributeGroupName.AttributeCode and append .LanguageCode only for a non-null LanguageCode from the same exact destination item | A transformation child is supplied on the REST Data Loader route | resolve_import_map_transformation_return_attribute |
| Transformation SourceColumns are derived | Set SourceColumns to current SourceColumn + $!$ + all participating source-column names joined by $&#124;$ in supplied order, including the current source again in the suffix | A transformation child is supplied on the REST Data Loader route |  |
| Optional transformation values are preserved | Preserve supplied optional transformation attributes other than resolver-owned ReturnAttributeName and derived SourceColumns; omit an optional value only when absent | A transformation child is prepared on the REST Data Loader route |  |
| Source IgnoreFlag is payload-normalized | Set IgnoreFlag to Y when no destination child exists; set it to N whenever at least one destination child exists, overriding a conflicting supplied value | A source child is prepared |  |
| Loader-owned fields are not lookup outputs | DestinationId, MapSourceId, RestAction, and other loader identity or operation fields are not populated from importMapAttributes; LanguageCode is the documented conditional exception | A destination child row is prepared |  |
| FSM archive identity is valid | Require an immutable task-level ZIP for task code EGI_MANAGE_IMPORT_MAPS and retain its archive identity through validation and handoff | The FSM task-level ZIP route is selected |  |
| FSM expressions are preserved | Do not reject, remove, interpret, or rewrite transformation and expression records | The FSM task-level ZIP contains transformations or expressions |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MIM.SELECT_IMPORT_ROUTE | decision | 1 | evaluate_result | rest->MIM.VALIDATE_INPUT;fsm_zip->MIM.VALIDATE_FSM_ZIP;ambiguous->MIM.AWAIT_ROUTE;invalid->MIM.HANDLE_ISSUE | none | stop | Before any route-specific validation; select REST Data Loader or FSM task-level ZIP from the explicit operation and artifact type |
| MIM.VALIDATE_FSM_ZIP | decision | 6 | validate_input | valid->MIM.RESOLVE_FSM_DESTINATION_ATTRIBUTES;invalid->MIM.HANDLE_ISSUE | MIM.SELECT_IMPORT_ROUTE | stop | The FSM task-level ZIP route is selected; validate archive identity and CSV readability while preserving transformations and expressions unchanged |
| MIM.VALIDATE_INPUT | decision | 10 | validate_input | valid->MIM.APPLY_DEFAULTS;missing_transformation_mapping->MIM.AWAIT_TRANSFORMATION_MAPPING;invalid->MIM.HANDLE_ISSUE | MIM.SELECT_IMPORT_ROUTE | stop | On the REST Data Loader route, validate parent, source, destination, and supplied transformation structure before preparing itemImportMaps source data |

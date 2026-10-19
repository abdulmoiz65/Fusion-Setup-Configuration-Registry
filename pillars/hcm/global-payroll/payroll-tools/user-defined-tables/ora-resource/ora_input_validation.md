# User-Defined Tables HDL Input Validation

## Functional Summary

User-defined tables are date-effective structures of rows, columns, and cell values. A row can match one exact value or cover a range; each cell value is loaded for the effective combination of a row and column. HDL supports the UserDefinedTable, UserDefinedTableColumn, UserDefinedTableRow, and UserDefinedTableColumnInstance business objects.

User Defined Table is also referred to as UDT.

## FDOS UDT Creation-Approach Rules

These FDOS interaction rules apply when a user asks to create a UDT. They
govern how creation information is collected and derived; the existing HDL
validation rules continue to validate the resulting source before preview.

| Situation | What Happens |
|---|---|
| A UDT creation request includes context information | Use the with-context approach strictly. Derive the column name, column code, data type, and cell value solely from the supplied context. Do not ask the user for any of those details. |
| A UDT creation request contains no context information | Ask exactly: Would you like to create the UDT using the with-context approach or the without-context approach? |
| The user chooses the with-context approach after a request without context | Request the required context information before proceeding. Once context is supplied, apply the with-context rule and do not ask for column name, column code, data type, or cell value. |
| The user chooses the without-context approach after a request without context | Proceed using the without-context approach. |
| A UDT creation request omits Row Title or UserRowTitle | Do not enforce Row Title as a required user input and do not block creation solely because it is absent. |

## Optional Design Labels

| Label | Status | Guidance |
|---|---|---|
| UserRowTitle | Optional design label | It may be documented as the business label for the row dimension, but its absence must not block UDT creation or HDL preparation. |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Table identity | LegislativeDataGroupName, UserTableCode, UserTableName | Block preparation | Supply a unique business table code and name with the target legislative data group name | Every HDL load | |
| Table structure | RangeOrMatch, UserKeyUnits | Block preparation | Select M for matched rows or R for range rows, then provide the key-unit choice | Every HDL load | |
| Columns | UserColumnCode, UserColumnName, DataType | Block preparation | Supply one column definition for each required result dimension | Every HDL load | |
| Rows | DisplaySequence, EffectiveStartDate, EffectiveEndDate, RowLowRangeOrName, RowHighRange when RangeOrMatch is R | Block preparation | Provide dated row definitions; use a row name for matched rows and low/high bounds for range rows | Every HDL load | |
| Cell values | EffectiveStartDate, EffectiveEndDate, Value, UserColumnCode, RowLowRangeOrName, UserTableCode, LegislativeDataGroupName | Block preparation | Provide a value for every intended row and column combination | Every HDL load | |
| Column validation formula | FormulaName and a User Table Validation fast formula contract | Block preparation | Supply the formula only when entry validation is required; its ENTRY_VALUE input is text and it must return FORMULA_STATUS | A column requires entry validation | |
| User-defined table name | UserTableName or Name | Block preparation | Supply the user-defined table name | Every UserDefinedTable create, update, correct, or import request | |
| Range-or-match selection | RangeOrMatch | Block preparation | Supply the reviewed range-or-match code or display value | Every UserDefinedTable create, update, correct, or import request | resolve_range_or_match_lov |
| Unit of measure | UserKeyUnits or Unit of Measure | Block preparation | Supply the reviewed unit-of-measure code or display value | Every UserDefinedTable create, update, correct, or import request | resolve_user_key_units_lov |
| Range-row bounds | RowLowRangeOrName and RowHighRange | Block preparation | Supply both the low range and high range | A UserDefinedTableRow record is created for a table whose RangeOrMatch is R | |
| Match-row exact value | RowLowRangeOrName or Exact | Block preparation | Supply the exact match value | A UserDefinedTableRow record is created for a table whose RangeOrMatch is M | |
| User-defined table code derivation | UserTableName or Name | Do not block for a missing UserTableCode and do not prompt for it | Copy the supplied UserTableName or Name exactly into UserTableCode without abbreviation, formatting, transformation, lookup, or confirmation | Every UserDefinedTable DAT record is prepared | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| RangeOrMatch consistency | Reject a row model that mixes exact-name rows with range bounds; matched rows use RowLowRangeOrName and range rows require both low and high range values | Every HDL load | |
| Effective dating consistency | Reject a row or column-instance date interval that is missing or inconsistent with the intended table values | Every dated row or cell-value load | |
| Formula contract | Reject a supplied validation formula that lacks text ENTRY_VALUE or a required FORMULA_STATUS result of S or E | FormulaName is supplied | |
| HDL business-object hierarchy | Reject a source that omits the required table parent or refers to an unsupported business object; use UserDefinedTable, UserDefinedTableColumn, UserDefinedTableRow, and UserDefinedTableColumnInstance | Every HDL load | |
| Flex-context declaration | Reject a flex-context row when UserTableAttributeCategory, FLEX:FF_USER_ROWS_DFF, and the context-qualified segment column do not identify the same context | A row flex context is loaded | |
| Operation evidence | Allow MERGE through the reviewed HDL route; block any other requested data operation until its support is confirmed from current metadata or Oracle guidance | Every HDL load | |
| Range unit of measure | Reject the source unless UserKeyUnits resolves to N, meaning Number | RangeOrMatch resolves to R | resolve_user_key_units_lov |
| Flex-segment context membership | Reject every supplied flex field that is not defined as a segment of the selected FF_USER_ROWS_DFF context; validate each field, not only the context syntax and agreement | One or more context-qualified row flex fields are supplied | verify_user_row_flex_segments |
| UserTableCode exact-name derivation | Set UserTableCode to the supplied UserTableName or Name exactly. Do not invent, abbreviate, format, derive a pattern, request the code from the user, or resolve it from Fusion. A separately supplied UserTableCode is usable only when it exactly equals the corresponding supplied name; otherwise use the supplied name so the final DAT satisfies UserTableCode = UserTableName. | Every UserDefinedTable DAT record is prepared | |
| Source-system field omission | Omit SourceSystemOwner and SourceSystemId from the generated DAT header and data records, or leave them unpopulated when omission is not possible | Every component in the generated DAT file | |
| Source-value preservation | Reject fabrication of any value absent from the source data. Preserve every source value exactly unless an explicit authored transformation applies; UserTableCode = UserTableName is such an explicit transformation. | Every populated DAT attribute | |
| Final DAT integrity | Before handoff, verify every populated UserTableCode exactly equals its corresponding supplied UserTableName or Name and verify that SourceSystemOwner and SourceSystemId are absent or unpopulated | Every generated DAT file | |
| User-defined-table REST metadata completeness | Block REST field mapping until the userDefinedTables describe response has been captured completely, including every returned attribute, data type, required or optional status, validation, accepted value, format, length restriction, reference or LOV dependency, and finder definition | REST table data is mapped for HDL preparation or export | describe_user_defined_tables_metadata |
| User-defined-row REST metadata completeness | Block REST field mapping until the userDefinedRows describe response has been captured completely, including every returned attribute, data type, required or optional status, validation, accepted value, format, length restriction, reference or LOV dependency, and finder definition | REST row data is mapped for HDL preparation or export | describe_user_defined_rows_metadata |
| Contextual row-flex metadata | Validate every supplied row-flex field against the attributes returned by the polymorphic describe call for the resolved context | A UserDefinedRowsDFF context is selected | verify_user_row_flex_segments |
| Row-flex LOV metadata | Treat a contextual flex field as an LOV only when its describe metadata contains lov information; derive the finder expression from the filter in that attribute's lov.lovResourcePath | A supplied contextual flex field contains lov metadata | resolve_user_defined_row_flex_value_set |

## HDL Variant and Operation Matrix

| Variant | Source Components | Control Record | Source-Confirmed Data Operation | Scope Limit |
|---|---|---|---|---|
| Without flex context | UserDefinedTable, UserDefinedTableColumn, UserDefinedTableRow, UserDefinedTableColumnInstance | METADATA | MERGE | The four local CSV files define attributes, key types, requiredness, and lookups but do not enumerate operations. MERGE is retained from the existing Oracle HDL examples referenced by this resource. Additional operations are outside this reviewed resource contract. |
| With row flex context | UserDefinedTable and UserDefinedTableRow | METADATA, including FLEX:FF_USER_ROWS_DFF on the row | MERGE | The supplied DAT demonstrates a table and row load only. It does not demonstrate flex segments on UserDefinedTableColumn or UserDefinedTableColumnInstance, and it does not confirm any operation other than MERGE. |

## Without-Flex-Context Attribute Catalog

The following tables summarize the developer-provided HDL metadata CSV files. Attributes marked for new records are required only when creating a new record. Application-generated surrogate IDs and GUIDs are reference-only for existing records.

### UserDefinedTable

| Business Label | HDL Attribute | Data Type | Key Type | Required | Lookup | Attribute Use |
|---|---|---|---|---|---|---|
| User-Defined Table ID | UserTableId | Number | Surrogate ID | Yes | | Application-generated identifier; reference existing records only. |
| Legislative Data Group Name | LegislativeDataGroupName | String | User Key | No | | Legislative data group name. |
| User-Defined Table Code | UserTableCode | String | User Key | For new records | | Unique within the legislative data group; uppercase with underscores instead of spaces. |
| Row Flexfield Context Code | UserTableAttributeCategory | String | | No | | Context code for the configurable user-defined-table row flexfield. Omit for the no-flex variant. |
| Legislative Data Group ID | LegislativeDataGroupId | Number | Foreign Object Reference | No | | Reference to LegislativeDataGroups. |
| Name | UserTableName | String | | For new records | | Starts with a letter and contains uppercase letters, digits, or underscores. |
| Range or Match | RangeOrMatch | String | | For new records | FF_USER_TABLE_RANGE_OR_MATCH | Selects exact-match or numeric-range rows. |
| Row Title | UserRowTitle | String | | No | | Business title for the row dimension. |
| Unit of Measure | UserKeyUnits | String | | For new records | FF_USER_TABLE_USER_KEY_UNITS | Date, number, or text; use number for a range table. |
| Source System ID | SourceSystemId | String | Source Key | No | | Unique with SourceSystemOwner for the component. |
| Source System Owner | SourceSystemOwner | String | Source Key | No | | Source system that owns SourceSystemId. |
| Globally Unique ID | GUID | String | Globally Unique ID | No | | Reference existing records only; cannot be supplied for new records. |
| Reference Context | SourceRefTableName | String | | No | | Declare the reference context in the METADATA header, not as a data value. |
| References 1 through 10 | SourceRef001 through SourceRef010 | String | | No | | Staging-only reconciliation values named in the METADATA header; not stored in the application. |

### UserDefinedTableColumn

| Business Label | HDL Attribute | Data Type | Key Type | Required | Lookup | Attribute Use |
|---|---|---|---|---|---|---|
| User-Defined Table Column ID | UserColumnId | Number | Surrogate ID | Yes | | Application-generated identifier; reference existing records only. |
| Column Code | UserColumnCode | String | User Key | For new records | | Uppercase code with underscores instead of spaces. |
| Legislative Data Group Name | LegislativeDataGroupName | String | User Key | No | | Legislative data group name. |
| User-Defined Table Code | UserTableCode | String | User Key | No | | Parent table code. |
| User-Defined Table ID | UserTableId | Number | Parent Surrogate ID | Yes | | Parent UserTable reference. |
| Column Name | UserColumnName | String | | For new records | | Starts with a letter and contains uppercase letters, digits, or underscores. |
| Data Type | DataType | String | | For new records | FF_USER_TABLE_USER_KEY_UNITS | Column value type, such as date, number, or text. |
| Formula Code | FormulaName | String | User Key | No | | Code of the formula used to validate column values. |
| Formula ID | FormulaId | Number | Foreign Object Reference | No | | Reference to Formula. |
| Legislative Data Group ID | LegislativeDataGroupId | Number | Foreign Object Reference | No | | Reference to LegislativeDataGroups. |
| Source System ID | SourceSystemId | String | Source Key | No | | Unique with SourceSystemOwner for the component. |
| Source System Owner | SourceSystemOwner | String | Source Key | No | | Source system that owns SourceSystemId. |
| Globally Unique ID | GUID | String | Globally Unique ID | No | | Reference existing records only; cannot be supplied for new records. |
| Reference Context | SourceRefTableName | String | | No | | Declare the reference context in the METADATA header, not as a data value. |
| References 1 through 10 | SourceRef001 through SourceRef010 | String | | No | | Staging-only reconciliation values named in the METADATA header; not stored in the application. |

### UserDefinedTableRow

| Business Label | HDL Attribute | Data Type | Key Type | Required | Lookup | Attribute Use |
|---|---|---|---|---|---|---|
| User-Defined Table Row ID | UserRowId | Number | Surrogate ID | Yes | | Application-generated identifier; reference existing records only. |
| Legislative Data Group Name | LegislativeDataGroupName | String | User Key | No | | Legislative data group name. |
| Low Range or Exact | RowLowRangeOrName | String | User Key | For new records | | Low bound for range rows or exact value for match rows. |
| User-Defined Table Code | UserTableCode | String | User Key | No | | Parent table code. |
| User-Defined Table ID | UserTableId | Number | Parent Surrogate ID | Yes | | Parent UserTable reference. |
| Effective End Date | EffectiveEndDate | Date | | No | | End of the date-effective change; omission is handled by ora_defaulting_rules.md. |
| Effective Start Date | EffectiveStartDate | Date | | Yes | | Start of the record or date-effective change. |
| High Range | RowHighRange | String | | No | | Required for a range table. |
| Legislative Data Group ID | LegislativeDataGroupId | Number | Foreign Object Reference | No | | Reference to LegislativeDataGroups. |
| Row Name | RowName | String | | For new records | | Translatable row name. |
| Sequence | DisplaySequence | Number | | No | | Optional row display sequence. |
| Source System ID | SourceSystemId | String | Source Key | No | | Unique with SourceSystemOwner for the component. |
| Source System Owner | SourceSystemOwner | String | Source Key | No | | Source system that owns SourceSystemId. |
| Globally Unique ID | GUID | String | Globally Unique ID | No | | Reference existing records only; cannot be supplied for new records. |
| Reference Context | SourceRefTableName | String | | No | | Declare the reference context in the METADATA header, not as a data value. |
| References 1 through 10 | SourceRef001 through SourceRef010 | String | | No | | Staging-only reconciliation values named in the METADATA header; not stored in the application. |

### UserDefinedTableColumnInstance

| Business Label | HDL Attribute | Data Type | Key Type | Required | Lookup | Attribute Use |
|---|---|---|---|---|---|---|
| Column Instance ID | UserColumnInstanceId | Number | Surrogate ID | Yes | | Application-generated identifier; reference existing records only. |
| Column Code | UserColumnCode | String | User Key | No | | Column whose cell value is being defined. |
| Legislative Data Group Name | LegislativeDataGroupName | String | User Key | No | | Legislative data group name. |
| Low Range or Exact | RowLowRangeOrName | String | User Key | No | | Row identity: low bound for a range table or exact value for a match table. |
| User-Defined Table Code | UserTableCode | String | User Key | For new records | | Parent table code. |
| User-Defined Table Row ID | UserRowId | Number | Parent Surrogate ID | Yes | | Parent UserRow reference. |
| Effective End Date | EffectiveEndDate | Date | | No | | End of the date-effective change; omission is handled by ora_defaulting_rules.md. |
| Effective Start Date | EffectiveStartDate | Date | | Yes | | Start of the record or date-effective change. |
| Legislative Data Group ID | LegislativeDataGroupId | Number | Foreign Object Reference | No | | Reference to LegislativeDataGroups. |
| User Table ID | UserTableId | Number | Foreign Object Reference | For new records | | Reference to UserTable. |
| User-Defined Table Column ID | UserColumnId | Number | Foreign Object Reference | For new records | | Reference to UserDefinedTableColumn. |
| Value | Value | String | | For new records | | Cell value for the selected row and column. |
| Source System ID | SourceSystemId | String | Source Key | No | | Unique with SourceSystemOwner for the component. |
| Source System Owner | SourceSystemOwner | String | Source Key | No | | Source system that owns SourceSystemId. |
| Globally Unique ID | GUID | String | Globally Unique ID | No | | Reference existing records only; cannot be supplied for new records. |
| Reference Context | SourceRefTableName | String | | No | | Declare the reference context in the METADATA header, not as a data value. |
| References 1 through 10 | SourceRef001 through SourceRef010 | String | | No | | Staging-only reconciliation values named in the METADATA header; not stored in the application. |

## With-Flex-Context DAT Attribute Use

The supplied DAT demonstrates one range table and one row with the FF_USER_ROWS_DFF context UDRCON. Empty values in the sample remain empty; this resource does not infer defaults for them.

### UserDefinedTable Record

| HDL Attribute | Sample Value | Attribute Role in the Supplied DAT |
|---|---|---|
| UserTableCode | SM_UDT_3 | Table business code. |
| LegislationCode | | Present in the METADATA header and empty in the sample. |
| LegislativeDataGroupId | | Present in the METADATA header and empty in the sample. |
| RangeOrMatch | R | Selects a range-row table. |
| UserKeyUnits | N | Row key unit used by the supplied range table. |
| UserRowTitle | Test Row | Row-dimension title. |
| UserTableId | | Present in the METADATA header and empty in the sample. |
| UserTableName | SM_UDT_3 | Table name. |
| LegislativeDataGroupName | USA LDG | Legislative data group user key. |
| UserTableAttributeCategory | UDRCON | Selects the row flexfield context used by the row record. |

### UserDefinedTableRow Record

| HDL Attribute | Sample Value | Attribute Role in the Supplied DAT |
|---|---|---|
| DisplaySequence | 1 | Row display sequence. |
| EffectiveEndDate | 4712/12/31 | End date supplied by the sample. |
| EffectiveStartDate | 2026/01/01 | Start date supplied by the sample. |
| RowHighRange | 600 | Upper range bound. |
| RowLowRangeOrName | 200 | Lower range bound and row user key. |
| UserTableCode | SM_UDT_3 | Parent table user key. |
| LegislativeDataGroupName | USA LDG | Legislative data group user key. |
| RowName | 200 | Translatable row name. |
| FLEX:FF_USER_ROWS_DFF | UDRCON | Declares the flexfield and selected context. |
| r1(FF_USER_ROWS_DFF=UDRCON) | A | Context-qualified row flexfield segment and its supplied value. |

## Flex-Context Validation Rules

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Context agreement | Require UserTableAttributeCategory, the FLEX:FF_USER_ROWS_DFF value, and each context-qualified segment suffix to identify the same context | A flex-context row is supplied | |
| Segment qualification | Require each flex segment column to use the form segment(FF_USER_ROWS_DFF=context) shown by the supplied DAT | A flex-context row is supplied | |
| Demonstrated component scope | Block claims that the sample proves column or column-instance flex support; the supplied DAT demonstrates flex data only on UserDefinedTableRow | Flex support is being mapped | |
| Empty sample values | Preserve blank LegislationCode, LegislativeDataGroupId, and UserTableId as sample observations; do not convert them into defaults or required-value rules | The supplied flex DAT is used as a mapping reference | |

## Reference and LOV Validation

These rules are additive. They do not replace the existing field, flex-context, operation, defaulting, dependency, or Data Loader instructions.

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Legislative data group reference | If LegislativeDataGroupName is supplied, resolve exactly one LegislativeDataGroupId and LegislationCode from Name; if valid resolved values are already supplied, reuse them without another lookup. | LegislativeDataGroupName, LegislativeDataGroupId, or LegislationCode is supplied for create, update, or import | resolve_legislative_data_group |
| Formula reference and type | If FormulaName or FormulaId is supplied and has not already been validated, resolve exactly one fast formula through the captured FormulaTypeName=User Table Validation endpoint. Match FormulaId or FormulaName exactly and require the returned FormulaTypeName to equal User Table Validation. If a valid code or ID whose formula type has already been validated is supplied, reuse it without another lookup. | FormulaName or FormulaId is supplied | resolve_user_table_validation_formula |
| Range-or-match LOV | If Meaning is supplied, resolve exactly one LookupCode M or R; if a valid code is already supplied, reuse it without another lookup. | RangeOrMatch is supplied | resolve_range_or_match_lov |
| Unit-of-measure and data-type LOV | If Meaning is supplied, resolve exactly one LookupCode N, T, or D; if a valid code is already supplied, reuse it without another lookup. | UserKeyUnits or DataType is supplied | resolve_user_key_units_lov |
| Predefined LOV | If Meaning is supplied, resolve exactly one LookupCode Y or N; if a valid code is already supplied, reuse it without another lookup. | Predefined is supplied | resolve_predefined_lov |
| Row flex context reference | If a context Name is supplied, resolve exactly one ContextCode; if a valid ContextCode is already supplied, reuse it without another lookup. | UserTableAttributeCategory, FLEX:FF_USER_ROWS_DFF, or a context-qualified row segment is supplied | resolve_user_row_flex_context |
| Parent table reference | If a table name or display value is supplied where an ID is required, resolve exactly one UserTableId through the captured userDefinedTables endpoint and finder variants; if a valid UserTableCode or UserTableId is already supplied, reuse it without another lookup. | A child record requires its UserTable parent reference | resolve_user_defined_table |
| Parent column reference | Resolve the parent UserTableId first, retrieve its expanded userDefinedColumns collection, and match UserColumnName or UserColumnId exactly to one column. Use the returned UserColumnId where an ID is required. Reuse a valid supplied UserColumnCode only when the selected HDL attribute accepts it; do not derive UserColumnCode from UserColumnName or BaseUserColumnName because the captured endpoint does not return UserColumnCode. | A column-instance record requires its column reference | resolve_user_defined_table_column |
| Parent row reference | If a row name or display value is supplied where an ID is required, resolve exactly one UserRowId through the captured versioned userDefinedRows endpoint using findByUserTableId and the parent UserTableId; if a valid RowLowRangeOrName or UserRowId is already supplied, reuse it without another lookup. | A column-instance record requires its row reference | resolve_user_defined_table_row |

## REST Describe Attribute Inventory

Captured on 2026-09-02 from the authenticated, read-only `GET /hcmRestApi/resources/latest/userDefinedTables/describe` and `GET /hcmRestApi/resources/latest/userDefinedRows/describe` responses. The pod resolved `latest` to resource version `11.13.18.05`.

`Metadata Mandatory` and `Input Required` are recorded separately. A server-managed attribute can be mandatory in the resource representation while not being required from the caller. When `inputRequired` or a separate format was absent from the response, the inventory records that fact instead of inferring a requirement or format. All returned root and generic child attributes are queryable. The returned annotation descriptions were not used to override the task's established functional rules because several descriptions did not correspond to their attributes.

| Resource | Attribute | Data Type | Metadata Mandatory | Input Required | Updatable | Allow Changes | Precision / Max Length | Validation or LOV Metadata |
|---|---|---|---|---|---|---|---|---|
| userDefinedTables | UserTableId | integer | No | Not returned | No | never | Precision 18 | Queryable; no LOV metadata returned |
| userDefinedTables | BaseUserTableName | string | No | Not returned | No | never | Precision 80; max length not returned | Queryable; no LOV metadata returned |
| userDefinedTables | LegislativeDataGroupId | integer | No | Not returned | No | never | Precision 18 | Queryable; no LOV metadata returned |
| userDefinedTables | LegislationCode | string | No | Not returned | No | never | Precision 30; max length not returned | Queryable; no LOV metadata returned |
| userDefinedTables | RangeOrMatch | string | No | Not returned | Yes | always | Precision 30; max length 30 | Choice control; accepted codes are M and R under the existing lookup rule. `LookupCode` maps to `RangeOrMatch`; display attribute is `Meaning`; LOV resource is `commonLookupsLOV` with `LookupType=FF_USER_TABLE_RANGE_OR_MATCH` |
| userDefinedTables | RangeOrMatchMeaning | string | No | Not returned | No | never | Precision 80; max length not returned | Meaning paired with `RangeOrMatch`; no independent LOV metadata returned |
| userDefinedTables | UserKeyUnits | string | No | Not returned | Yes | always | Precision 30; max length 30 | Choice control; accepted codes are N, T, and D under the existing lookup rule. `LookupCode` maps to `UserKeyUnits`; display attribute is `Meaning`; LOV resource is `commonLookupsLOV` with `LookupType=FF_USER_TABLE_USER_KEY_UNITS` |
| userDefinedTables | UserKeyUnitsMeaning | string | No | Not returned | No | never | Precision 80; max length not returned | Meaning paired with `UserKeyUnits`; no independent LOV metadata returned |
| userDefinedTables | UserRowTitle | string | No | Not returned | Yes | always | Precision 80; max length not returned | Queryable; no LOV metadata returned |
| userDefinedTables | UserTableName | string | No | Not returned | Yes | always | Precision 80; max length not returned | Queryable; no LOV metadata returned |
| userDefinedTables | LegislativeDataGroupName | string | No | Not returned | No | never | Precision 240; max length not returned | Queryable; no LOV metadata returned; use the captured legislative-data-group resolver when a name must be converted to ID and legislation code |
| userDefinedTables | CreatedBy | string | No | Not returned | No | never | Precision 64; max length not returned | Server-managed; no LOV metadata returned |
| userDefinedTables | CreationDate | datetime | No | Not returned | No | never | Not returned | Server-managed; no separate datetime format returned |
| userDefinedTables | LastUpdateDate | datetime | No | Not returned | No | never | Not returned | Server-managed; no separate datetime format returned |
| userDefinedTables | LastUpdatedBy | string | No | Not returned | No | never | Precision 64; max length not returned | Server-managed; no LOV metadata returned |
| userDefinedTables | ModuleId | string | No | Not returned | No | never | Precision 32; max length not returned | Queryable; no LOV metadata returned |
| userDefinedTables | UserTableAttributeCategory | string | No | Not returned | Yes | always | Precision 30; max length not returned | Queryable; no LOV metadata returned at the root attribute; resolve and validate the row-flex context through the captured context resolver |
| userDefinedRows | UserTableId | integer | Yes | Yes | Yes | inCreate | Precision 18 | Parent table identifier; no LOV metadata returned |
| userDefinedRows | UserRowId | integer | Yes | Not returned | Yes | inCreate | Precision 18 | Has a default-value expression and is marked globally unique; do not treat it as a required caller input |
| userDefinedRows | EffectiveStartDate | date | Yes | Yes | Yes | always | Not returned | No separate date format or LOV metadata returned |
| userDefinedRows | EffectiveEndDate | date | Yes | Yes | Yes | always | Not returned | No separate date format or LOV metadata returned |
| userDefinedRows | DisplaySequence | integer | No | Not returned | Yes | always | Precision 5 | No LOV metadata returned |
| userDefinedRows | RowLowRangeOrName | string | Yes | Yes | Yes | always | Precision 80; max length 80 | No LOV metadata returned; apply the existing range-versus-match conditional rules |
| userDefinedRows | LegislativeDataGroupId | integer | No | Not returned | Yes | inCreate | Precision 18 | No LOV metadata returned; use the captured legislative-data-group resolver when a name is supplied |
| userDefinedRows | RowHighRange | string | No | Not returned | Yes | always | Precision 80; max length 80 | No LOV metadata returned; apply the existing range-versus-match conditional rules |
| userDefinedRows | RowName | string | Yes | Yes | Yes | always | Precision 80; max length not returned | Exact-row display attribute in the captured mapping; no LOV metadata returned |
| userDefinedRows | CreatedBy | string | Yes | Not returned | No | never | Precision 64; max length not returned | Server-managed; not a required caller input |
| userDefinedRows | CreationDate | datetime | Yes | Not returned | No | never | Not returned | Server-managed; not a required caller input; no separate datetime format returned |
| userDefinedRows | LastUpdateDate | datetime | Yes | Not returned | No | never | Not returned | Server-managed; not a required caller input; no separate datetime format returned |
| userDefinedRows | LastUpdatedBy | string | Yes | Not returned | No | never | Precision 64; max length not returned | Server-managed; not a required caller input |

`LegislativeDataGroupName` was not returned as a root `userDefinedRows` attribute by this describe response. Preserve the previously supplied response mapping as a version- or projection-specific observation, but do not assume the field is available in the captured root resource contract.

The root `userDefinedRows` describe response also returned the `UserDefinedRowsDFF` child metadata below. These are the generic child attributes; concrete context segment attributes still require the existing polymorphic describe call with the resolved context code.

| Child Resource | Attribute | Data Type | Metadata Mandatory | Input Required | Updatable | Allow Changes | Precision / Max Length | Validation or LOV Metadata |
|---|---|---|---|---|---|---|---|---|
| userDefinedRows.UserDefinedRowsDFF | UserRowId | integer | Yes | Not returned | Yes | inCreate | Precision 18 | Has a default-value expression and is marked globally unique |
| userDefinedRows.UserDefinedRowsDFF | EffectiveStartDate | date | Yes | Yes | Yes | always | Not returned | No separate date format returned |
| userDefinedRows.UserDefinedRowsDFF | EffectiveEndDate | date | Yes | Yes | Yes | always | Not returned | No separate date format returned |
| userDefinedRows.UserDefinedRowsDFF | __FLEX_Context | string | No | Not returned | Yes | always | Precision 30; max length 30 | Choice control. `ContextCode` maps to `__FLEX_Context`; display attribute is `Name`; LOV resource is `FlexFndDffDescriptiveFlexfieldContexts` with Application ID 802 and flexfield code `FF_USER_ROWS_DFF` |
| userDefinedRows.UserDefinedRowsDFF | __FLEX_Context_DisplayValue | string | No | Not returned | Yes in the resource metadata; flex property marks it read-only | always | Not returned | Has a default-value expression. `Name` maps to this display attribute and `ContextCode` is derived into `__FLEX_Context`; use the same context LOV resource |

## REST Describe Finder Inventory

No additional root finders beyond those listed below were returned by either describe response.

| Resource | Finder | Attribute | Data Type | Required | Input Required | Queryable | Allow Changes | Precision |
|---|---|---|---|---|---|---|---|---|
| userDefinedTables | PrimaryKey | UserTableId | integer | No | Not returned | Yes | never | 18 |
| userDefinedTables | findByFilterCriteria | LegislationCode | string | Optional | Not returned | Not returned | always | Not returned |
| userDefinedTables | findByFilterCriteria | LegislativeDataGroupId | integer | Optional | Not returned | Not returned | always | Not returned |
| userDefinedTables | findByFilterCriteria | RangeOrMatch | string | Optional | Not returned | Not returned | always | Not returned |
| userDefinedTables | findByFilterCriteria | UserKeyUnits | string | Optional | Not returned | Not returned | always | Not returned |
| userDefinedTables | findByFilterCriteria | UserTableName | string | Optional | Not returned | Not returned | always | Not returned |
| userDefinedTables | findByUserTableId | UserTableId | integer | Optional | Not returned | Not returned | always | Not returned |
| userDefinedRows | PrimaryKey | EffectiveEndDate | date | Yes | Yes | Yes | always | Not returned |
| userDefinedRows | PrimaryKey | EffectiveStartDate | date | Yes | Yes | Yes | always | Not returned |
| userDefinedRows | PrimaryKey | UserRowId | integer | Yes | Not returned | Yes | inCreate | 18 |
| userDefinedRows | findByUserTableId | SysEffectiveDate | object | Optional | Not returned | Not returned | always | Not returned |
| userDefinedRows | findByUserTableId | UserTableId | integer | Optional | Not returned | Not returned | always | Not returned |

The `UserDefinedRowsDFF` child collection returned only its `PrimaryKey` finder with `EffectiveEndDate`, `EffectiveStartDate`, and `UserRowId`, using the same metadata shown for those child attributes above.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UDT.VALIDATE_INPUT | step | 1 | validate_input | valid->UDT.APPLY_DEFAULTS;invalid->UDT.RETURN_ISSUES | none | stop | Validate the UserDefinedTable HDL source before preview or import routing. |

## Sources

- /scratch/UDT/UserDefinedTable.csv (SHA-256 f8ead2ff6c3ab862eae19ee045208e32fd3482bd02d3fec3a608158b14506b27)
- /scratch/UDT/UserDefinedTableColumn.csv (SHA-256 1cac7497b66b80fbdac0f3ad690f98edb9af6159f1204a660cb3ad39963b4910)
- /scratch/UDT/UserDefinedTableRow.csv (SHA-256 2f7f39ffc2768e12b0cd5b8f5240f6bebe903b67986381a0b9ad86f2ae1f0f98)
- /scratch/UDT/UserDefinedTableColumnInstance.csv (SHA-256 9b74ba8df057f97cb7bad91a21f41dd8541ff3ec40d55e32909e76fea7604f2f)
- /scratch/UDT/UserDefinedTable.dat (SHA-256 567a33904ce657b04789cfdb6cb7c8dc1af7824367a35d9f68031a6972455f57)
- https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/overview-of-loading-user-defined-tables.html
- https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/example-of-loading-user-defined-tables-for-matched-row-values.html
- https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/example-of-loading-user-defined-tables-for-a-range-of-row-values.html
- https://docs.oracle.com/en/cloud/saas/human-resources/faigp/user-table-validation-formula-type.html
- Developer-provided UDT general and field-level validation instructions in the current request.
- Developer-provided Resolve code from name and Strict Instructions for UserTableCode and source-system fields in the current request.
- Developer-provided primary REST endpoints, describe endpoints, finder variants, response mappings, contextual-flex describe flow, and flex value-set LOV contract in the current request.
- Authenticated read-only `GET /hcmRestApi/resources/latest/userDefinedTables/describe` capture from environment `cptctugqy` on 2026-09-02; `latest` resolved to `11.13.18.05`.
- Authenticated read-only `GET /hcmRestApi/resources/latest/userDefinedRows/describe` capture from environment `cptctugqy` on 2026-09-02; `latest` resolved to `11.13.18.05`.
- Developer-provided Fast Formula type-validation endpoint `/hcmRestApi/resources/latest/fastFormulas?&q=FormulaTypeName=User Table Validation` and its authenticated read-only capture from environment `cptctugqy` on 2026-09-02.
- Developer-provided expanded User Defined Tables endpoint `/hcmRestApi/resources/latest/userDefinedTables?expand=userDefinedColumns&finder=findByUserTableId%3BUserTableId=<UserTableId>` and its authenticated read-only capture from environment `cptctugqy` on 2026-09-02.

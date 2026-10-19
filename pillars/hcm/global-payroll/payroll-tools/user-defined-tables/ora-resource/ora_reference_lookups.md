# User-Defined Tables Reference and LOV Lookups

This file adds reference and LOV resolution rules without removing, replacing, or changing any existing User-Defined Tables behavioral instructions. All lookups are read-only. Contracts not supplied by the developer remain blocking authoring gaps.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_legislative_data_group | LegislativeDataGroupName is supplied and LegislativeDataGroupId or LegislationCode is required; skip when valid resolved values are already provided | LegislativeDataGroupName, LegislativeDataGroupId, or LegislationCode | /hcmRestApi/resources/latest/legislativeDataGroupsLOV | Name, LegislativeDataGroupId, LegislationCode | Match the provided LDG name exactly against Name and require one result; reuse caller-validated LegislativeDataGroupId and LegislationCode directly | LegislativeDataGroupId, LegislationCode; retain LegislativeDataGroupName when supported by the HDL component | Zero matches: validation error naming LegislativeDataGroupName and the invalid value. Multiple matches: ambiguity error; do not select automatically. |
| resolve_user_table_validation_formula | FormulaName or FormulaId is supplied and has not already been validated as a User Table Validation formula; skip only when the supplied code or ID is already valid and its formula type has already been validated | FormulaName or FormulaId | /hcmRestApi/resources/latest/fastFormulas?&q=FormulaTypeName=User Table Validation | FormulaId, FormulaName, FormulaTypeId, FormulaTypeName, BaseFormulaName, EffectiveStartDate, EffectiveEndDate, LegislativeDataGroupId, LegislativeDataGroupName, LegislationCode | The endpoint candidate set must contain only records whose FormulaTypeName is exactly User Table Validation. For a supplied FormulaId, match FormulaId exactly; for a supplied formula name or display value, match FormulaName exactly. Require exactly one matching record and do not treat BaseFormulaName as the input display name. | FormulaId and FormulaName, according to the reviewed HDL attribute selection; retain FormulaTypeId, FormulaTypeName, effective dates, and legislative scope as validation context | Zero matches: validation error naming FormulaName or FormulaId and stating that the value is not a valid User Table Validation formula. Multiple matches: ambiguity error; do not select automatically. A returned record whose FormulaTypeName is not exactly User Table Validation is invalid. |
| resolve_range_or_match_lov | A RangeOrMatch name or display value is supplied; skip when a valid M or R code is already provided | RangeOrMatch Meaning or LookupCode | /fscmRestApi/resources/latest/commonLookupsLOV?finder=LookupTypeFinder;LookupType=FF_USER_TABLE_RANGE_OR_MATCH&q=LookupCode='R' or LookupCode='M' | LookupCode, Meaning | Match the input exactly to Meaning and require one result; use LookupCode M or R in the HDL data. For direct-code validation, query the supplied M or R code. | RangeOrMatch=LookupCode | Zero matches: validation error naming RangeOrMatch and the invalid value. Multiple matches: ambiguity error; do not select automatically. |
| resolve_user_key_units_lov | A UserKeyUnits or DataType name or display value is supplied; skip when a valid N, T, or D code is already provided | UserKeyUnits or DataType Meaning or LookupCode | /fscmRestApi/resources/latest/commonLookupsLOV?finder=LookupTypeFinder;LookupType=FF_USER_TABLE_USER_KEY_UNITS&q=LookupCode='T' or LookupCode='N' or LookupCode='D' | LookupCode, Meaning | Match the input exactly to Meaning and require one result; use LookupCode N, T, or D in the HDL data. For direct-code validation, query the supplied code. | UserKeyUnits or DataType=LookupCode, according to the target HDL component | Zero matches: validation error naming the field and invalid value. Multiple matches: ambiguity error; do not select automatically. |
| resolve_predefined_lov | A Predefined name or display value is supplied; skip when a valid Y or N code is already provided | Predefined Meaning or LookupCode | /fscmRestApi/resources/latest/commonLookupsLOV?finder=LookupTypeFinder;LookupType=YES_NO&q=LookupCode='Y' or LookupCode='N' | LookupCode, Meaning | Match the input exactly to Meaning and require one result; use LookupCode Y or N in the import data. For direct-code validation, query the supplied code. | Predefined=LookupCode | Zero matches: validation error naming Predefined and the invalid value. Multiple matches: ambiguity error; do not select automatically. |
| resolve_user_row_flex_context | A row-flex Context name or display value is supplied; skip when a valid ContextCode is already provided | Context Name or ContextCode | /fscmRestApi/resources/latest/FlexFndDffDescriptiveFlexfieldContexts?finder=ValidValuesFinder;Bind_ApplicationId=802,Bind_DescriptiveFlexfieldCode=FF_USER_ROWS_DFF | ContextCode, Name | With the fixed finder, match the supplied name exactly against Name and require one result. For direct-code validation, use q=ContextCode='<provided code>'; the observed example is q=ContextCode='UDRCON'. | UserTableAttributeCategory=ContextCode and FLEX:FF_USER_ROWS_DFF=ContextCode | Zero matches: validation error naming Context and the invalid value. Multiple matches: ambiguity error; do not select automatically. |
| verify_user_row_flex_segments | One or more context-qualified FF_USER_ROWS_DFF flex fields are supplied | ContextCode and every supplied flex-field or segment name | /hcmRestApi/resources/latest/userDefinedRows/describe?polymorphicType=userDefinedRows.UserDefinedRowsDFF:{context} | All returned attribute metadata for the selected context, including attribute name, data type, required or optional status, validations, accepted values, formats, lengths, and lov metadata when present | Substitute the resolved ContextCode for {context}; require every supplied flex field to match exactly one returned attribute for that context | Verified context membership and captured metadata for every supplied flex field | Zero matches for any field: validation error naming the field and context. Multiple matches: ambiguity error; do not select automatically. |
| resolve_user_defined_table | A table name or display value is supplied where UserTableId is required; skip when a valid UserTableCode or UserTableId is already provided | LegislativeDataGroupName or LegislativeDataGroupId plus UserTableName, UserTableCode, or UserTableId | /hcmRestApi/resources/latest/userDefinedTables | UserTableId, UserTableName, LegislationCode, LegislativeDataGroupId, RangeOrMatch, RangeOrMatchMeaning, UserKeyUnits, UserKeyUnitsMeaning, UserRowTitle, LegislativeDataGroupName, BaseUserTableName | Use the applicable captured finder and require exactly one response whose UserTableName exactly matches within the supplied legislative-data-group scope; use findByUserTableId for a supplied ID; reuse a caller-validated code or ID directly | UserTableId and the mapped table attributes needed by the reviewed operation | Zero matches: validation error naming the table field and invalid value. Multiple matches: ambiguity error; do not select automatically. |
| resolve_user_defined_table_column | UserColumnName or UserColumnId must be resolved or validated for a known parent UserTableId; skip when a valid UserColumnId is already provided, or when a valid UserColumnCode is already supplied for an HDL attribute that accepts the code | UserTableId plus UserColumnName or UserColumnId; a caller-validated UserColumnCode can be reused directly | /hcmRestApi/resources/latest/userDefinedTables?expand=userDefinedColumns&finder=findByUserTableId%3BUserTableId={UserTableId} | Parent UserTableId and UserTableName; expanded userDefinedColumns fields UserColumnId, BaseUserColumnName, UserColumnName, UserTableId, LegislativeDataGroupId, LegislationCode, DataType, DataTypeMeaning, FormulaId, FormulaName | Substitute the resolved parent UserTableId and require exactly one parent table. Within its expanded userDefinedColumns collection, match a supplied UserColumnId exactly against UserColumnId or a supplied name exactly against UserColumnName, and require exactly one column. Do not treat BaseUserColumnName as UserColumnCode: the captured response does not return UserColumnCode. | UserColumnId and the returned column context. Reuse a caller-validated UserColumnCode directly only when the selected HDL attribute accepts it; this endpoint cannot derive a missing UserColumnCode. | Zero parent or column matches: validation error naming UserTableId and the supplied column value. Multiple parent or column matches: ambiguity error; do not select automatically. If UserColumnCode is required but was not supplied, return a missing-value error because this endpoint does not return it. |
| resolve_user_defined_table_row | A row name or display value is supplied where UserRowId is required; skip when a valid RowLowRangeOrName or UserRowId is already provided | UserTableId plus RowName, RowLowRangeOrName, EffectiveStartDate, or UserRowId | /hcmRestApi/resources/11.13.18.05/userDefinedRows?finder=findByUserTableId;UserTableId={userTableId} | UserRowId, RowName, LegislativeDataGroupId, DisplaySequence, RowLowRangeOrName, LegislativeDataGroupName, RowHighRange, EffectiveStartDate, EffectiveEndDate | Substitute the resolved UserTableId; within that table require exactly one row matching the supplied row identity and effective-date scope; reuse a caller-validated user key or ID directly | UserRowId and the mapped row attributes needed by the reviewed operation | Zero matches: validation error naming the row field and invalid value. Multiple matches: ambiguity error; do not select automatically. |
| describe_user_defined_tables_metadata | REST attribute, validation, or finder metadata for user-defined tables is required | userDefinedTables resource | /hcmRestApi/resources/latest/userDefinedTables/describe | All returned resource attributes and finders, including each attribute's data type, required or optional status, validations, accepted values, format, length restriction, and reference or LOV metadata | Capture every returned attribute and finder without filtering or inferring omitted metadata | Complete userDefinedTables REST metadata inventory; the authenticated capture on 2026-09-02 resolved `latest` to `11.13.18.05` and returned 17 root attributes and 3 finders | Missing or incomplete future describe content: stop REST mapping and report the unavailable metadata item without inferring it. |
| describe_user_defined_rows_metadata | REST attribute, validation, or finder metadata for user-defined rows is required | userDefinedRows resource | /hcmRestApi/resources/latest/userDefinedRows/describe | All returned resource attributes and finders, including each attribute's data type, required or optional status, validations, accepted values, format, length restriction, and reference or LOV metadata | Capture every returned attribute and finder without filtering or inferring omitted metadata | Complete userDefinedRows REST metadata inventory; the authenticated capture on 2026-09-02 resolved `latest` to `11.13.18.05` and returned 13 root attributes, the generic `UserDefinedRowsDFF` child metadata, and 2 root finders | Missing or incomplete future describe content: stop REST mapping and report the unavailable metadata item without inferring it. |
| resolve_user_defined_row_flex_value_set | A contextual row-flex attribute's describe metadata contains lov information | Flex attribute input value, metadata-derived finder expression, and metadata lov.lovResourcePath | /fscmRestApi/resources/latest/userDefinedRows/FlexFndPvsCharacterIdCharacterValues?finder={finderexpression} | Id, Value, Description | Derive {finderexpression} only from the attribute metadata filter in lov.lovResourcePath; match the supplied display value exactly against Value and require one result. Supported query keys are fields, finder, q, limit, and offset. Send no request Content-Type and expect application/vnd.oracle.adf.resourcecollection+json. | Id or Value for the flex attribute as directed by its describe metadata; retain Description for display context | Zero matches: validation error naming the flex field, context, and invalid value. Multiple matches: ambiguity error; do not select automatically. Missing lov metadata or filter: stop without inventing a finder. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A reference name or display value is provided | Use the applicable read-only resolver and place its resolved code or ID into the reviewed HDL attribute. |
| A valid code or ID is already provided | Use it directly and do not perform an additional lookup. |
| A provided name returns exactly one match | Use the resolved code or ID when preparing the HDL import source. |
| A provided name returns no match | Return a validation error that identifies the field and invalid input value. |
| A provided name returns multiple matches | Return an ambiguity error and do not choose a result automatically. |
| A name remains unresolved for a code-or-ID field | Do not include the unresolved name in the HDL source or import payload. |
| The same reference value appears more than once in one operation | Reuse the resolved value from the operation-scoped lookup cache. |
| A lookup endpoint, requested field, match contract, or output mapping is missing, incomplete, or unresolved | Stop before payload preparation and report the missing lookup contract. |
| No active Fusion session exists | Obtain a fresh session through the configured authentication workflow, then call only the captured read-only reference endpoint. |
| Export data contains only a resolved code or ID and a display value is required | Use the same captured endpoint to map the code or ID back to Name or Meaning, require exactly one result, and reuse the result within the operation. |
| A REST describe contract is required | Call the applicable describe resolver and capture every returned attribute, its metadata, and every finder before treating the resource mapping as complete. |
| A contextual flex attribute contains lov metadata | Read the filter from the attribute metadata in lov.lovResourcePath and derive the finder expression from that metadata only; never invent or reuse a finder from a different flex field. |
| A contextual flex attribute has no lov metadata | Treat it as a non-LOV field for this lookup flow and do not call the value-set LOV endpoint. |

## Captured Query Variants

| Reference Attribute | Lookup Scope | Query Variant | Use |
|---|---|---|---|
| Legislative Data Group | legislativeDataGroupsLOV | /hcmRestApi/resources/latest/legislativeDataGroupsLOV | Match input against Name; map LegislativeDataGroupId and LegislationCode. |
| Predefined | YES_NO | /fscmRestApi/resources/latest/commonLookupsLOV?finder=LookupTypeFinder;LookupType=YES_NO&q=LookupCode='Y' or LookupCode='N' | Retrieve the complete Y/N candidate set, match Meaning, and map LookupCode. |
| Predefined | YES_NO | q=LookupCode='Y' or q=LookupCode='N' | Validate one directly supplied code when needed. |
| Range or Match | FF_USER_TABLE_RANGE_OR_MATCH | /fscmRestApi/resources/latest/commonLookupsLOV?finder=LookupTypeFinder;LookupType=FF_USER_TABLE_RANGE_OR_MATCH&q=LookupCode='R' or LookupCode='M' | Retrieve the complete R/M candidate set, match Meaning, and map LookupCode. |
| Range or Match | FF_USER_TABLE_RANGE_OR_MATCH | q=LookupCode='R' or q=LookupCode='M' | Validate one directly supplied code when needed. |
| Unit of Measure | FF_USER_TABLE_USER_KEY_UNITS | /fscmRestApi/resources/latest/commonLookupsLOV?finder=LookupTypeFinder;LookupType=FF_USER_TABLE_USER_KEY_UNITS&q=LookupCode='T' or LookupCode='N' or LookupCode='D' | Retrieve the complete T/N/D candidate set, match Meaning, and map LookupCode. |
| Unit of Measure | FF_USER_TABLE_USER_KEY_UNITS | q=LookupCode='N', q=LookupCode='T', or q=LookupCode='D' | Validate one directly supplied code when needed. |
| Context | FF_USER_ROWS_DFF with ApplicationId 802 | /fscmRestApi/resources/latest/FlexFndDffDescriptiveFlexfieldContexts?finder=ValidValuesFinder;Bind_ApplicationId=802,Bind_DescriptiveFlexfieldCode=FF_USER_ROWS_DFF&q=ContextCode='<provided code>' | Validate a supplied ContextCode; the observed example uses UDRCON. |
| Formula | User Table Validation | /hcmRestApi/resources/latest/fastFormulas?&q=FormulaTypeName=User Table Validation | Return formulas of the required type, then match the supplied FormulaId or FormulaName exactly and require one result. |
| User-defined table columns | Expanded child collection by parent table | /hcmRestApi/resources/latest/userDefinedTables?expand=userDefinedColumns&finder=findByUserTableId%3BUserTableId={UserTableId} | Resolve one parent by UserTableId, then match UserColumnId or UserColumnName exactly within its userDefinedColumns collection. |
| User-defined tables | findByFilterCriteria | /hcmRestApi/resources/latest/userDefinedTables?finder=findByFilterCriteria;LegislativeDataGroupId={legislativeDataGroupId} | Return tables within the supplied legislative data group. |
| User-defined tables | findByFilterCriteria | /hcmRestApi/resources/latest/userDefinedTables?finder=findByFilterCriteria;LegislativeDataGroupId={legislativeDataGroupId},UserTableName={searchText} | Search a table name within the supplied legislative data group, then require an exact response match for identity resolution. |
| User-defined tables | findByFilterCriteria | /hcmRestApi/resources/latest/userDefinedTables?finder=findByFilterCriteria;UserTableName={searchText} | Search by table name across the finder scope, then apply exact-match and ambiguity rules. |
| User-defined tables | findByUserTableId | /hcmRestApi/resources/latest/userDefinedTables?finder=findByUserTableId;UserTableId={userTableId} | Resolve one table by its ID. |
| User-defined rows | findByUserTableId | /hcmRestApi/resources/11.13.18.05/userDefinedRows?finder=findByUserTableId;UserTableId={userTableId} | Retrieve rows for the required parent UserTableId. |
| User-defined tables metadata | describe | /hcmRestApi/resources/latest/userDefinedTables/describe | Capture all table attributes, metadata, and finders. |
| User-defined rows metadata | describe | /hcmRestApi/resources/latest/userDefinedRows/describe | Capture all row attributes, metadata, and finders. |
| User-defined row context metadata | polymorphic describe | /hcmRestApi/resources/latest/userDefinedRows/describe?polymorphicType=userDefinedRows.UserDefinedRowsDFF:{context} | Capture and validate all flex attributes defined for the selected context; example context AUDRCON. |
| User-defined row flex value set | metadata-derived finder | /fscmRestApi/resources/latest/userDefinedRows/FlexFndPvsCharacterIdCharacterValues?finder={finderexpression} | Resolve a flex LOV display Value to Id using only the finder expression derived from that attribute's describe metadata. |

## Finder Inventory

| Resource | Finder | Finder Attributes | Requirement |
|---|---|---|---|
| userDefinedTables | findByFilterCriteria | LegislativeDataGroupId | Observed variant for legislative-data-group-scoped retrieval |
| userDefinedTables | findByFilterCriteria | LegislativeDataGroupId, UserTableName | Observed variant for name search within a legislative data group |
| userDefinedTables | findByFilterCriteria | UserTableName | Observed variant for name search |
| userDefinedTables | findByUserTableId | UserTableId | Observed ID-resolution variant |
| userDefinedRows | findByUserTableId | UserTableId | Required finder pattern for row retrieval |
| FlexFndPvsCharacterIdCharacterValues | Metadata-defined finder | finderexpression derived from the flex attribute metadata filter in lov.lovResourcePath | Required only when the selected contextual flex attribute contains lov metadata |
| userDefinedTables | PrimaryKey | UserTableId | Returned by the authenticated describe response |
| userDefinedTables | findByFilterCriteria | LegislationCode, LegislativeDataGroupId, RangeOrMatch, UserKeyUnits, UserTableName | Every finder attribute is optional in the describe response |
| userDefinedTables | findByUserTableId | UserTableId | Finder attribute is optional in the describe response |
| userDefinedRows | PrimaryKey | EffectiveEndDate, EffectiveStartDate, UserRowId | All are metadata-mandatory; the two effective dates are input-required, while UserRowId has a default-value expression |
| userDefinedRows | findByUserTableId | SysEffectiveDate, UserTableId | Both finder attributes are optional in the describe response |

## REST Response Mappings

| Resource | Response Attribute | Mapping Role |
|---|---|---|
| fastFormulas | FormulaId | Formula identifier used for the FormulaId HDL reference when selected |
| fastFormulas | FormulaName | Formula name used for exact input matching and the FormulaName HDL reference when selected |
| fastFormulas | FormulaTypeId | Formula-type identifier retained as validation context |
| fastFormulas | FormulaTypeName | Required type discriminator; must equal User Table Validation |
| fastFormulas | BaseFormulaName | Base formula name for context only; do not use it as the supplied formula-name match field |
| fastFormulas | EffectiveStartDate | Formula effective-start context |
| fastFormulas | EffectiveEndDate | Formula effective-end context |
| fastFormulas | LegislativeDataGroupId | Legislative data group scope returned for the formula |
| fastFormulas | LegislativeDataGroupName | Legislative data group display scope returned for the formula |
| fastFormulas | LegislationCode | Legislation scope returned for the formula |
| userDefinedTables.userDefinedColumns | UserColumnId | Column ID attribute |
| userDefinedTables.userDefinedColumns | BaseUserColumnName | Base column name for context only; it is not documented or mapped as UserColumnCode |
| userDefinedTables.userDefinedColumns | UserColumnName | Column display name and exact name-match attribute |
| userDefinedTables.userDefinedColumns | UserTableId | Parent user-defined-table ID |
| userDefinedTables.userDefinedColumns | LegislativeDataGroupId | Legislative data group ID |
| userDefinedTables.userDefinedColumns | LegislationCode | Legislation code |
| userDefinedTables.userDefinedColumns | DataType | Column data-type code |
| userDefinedTables.userDefinedColumns | DataTypeMeaning | Column data-type meaning |
| userDefinedTables.userDefinedColumns | FormulaId | Validation formula ID when assigned |
| userDefinedTables.userDefinedColumns | FormulaName | Validation formula name when assigned |
| userDefinedTables | UserTableId | ID attribute |
| userDefinedTables | UserTableName | Name attribute |
| userDefinedTables | LegislationCode | Legislation code |
| userDefinedTables | LegislativeDataGroupId | Legislative data group ID |
| userDefinedTables | RangeOrMatch | Range-or-match code |
| userDefinedTables | RangeOrMatchMeaning | Range-or-match meaning |
| userDefinedTables | UserKeyUnits | Unit-of-measure code |
| userDefinedTables | UserKeyUnitsMeaning | Unit-of-measure meaning |
| userDefinedTables | UserRowTitle | Row title |
| userDefinedTables | LegislativeDataGroupName | Legislative data group name |
| userDefinedTables | BaseUserTableName | Base user-defined-table name |
| userDefinedRows | UserRowId | ID attribute |
| userDefinedRows | RowName | Exact attribute |
| userDefinedRows | LegislativeDataGroupId | Legislative data group ID |
| userDefinedRows | DisplaySequence | Sequence |
| userDefinedRows | RowLowRangeOrName | Low range or exact user key |
| userDefinedRows | LegislativeDataGroupName | Legislative data group name |
| userDefinedRows | RowHighRange | High range |
| userDefinedRows | EffectiveStartDate | Date-effective start |
| userDefinedRows | EffectiveEndDate | Date-effective end |
| FlexFndPvsCharacterIdCharacterValues | Id | ID attribute |
| FlexFndPvsCharacterIdCharacterValues | Value | Display attribute |
| FlexFndPvsCharacterIdCharacterValues | Description | Description |

## Reference Attribute Coverage

| Reference Attribute | Resolver | Name or Display Attribute | Code or ID Used for Import or Export Data |
|---|---|---|---|
| User Table Validation formula | resolve_user_table_validation_formula | FormulaName | FormulaId or FormulaName, according to the reviewed UserDefinedTableColumn HDL attribute selection |
| Context | resolve_user_row_flex_context | Name | ContextCode in UserTableAttributeCategory and FLEX:FF_USER_ROWS_DFF |
| Context flex fields | verify_user_row_flex_segments | Flexfield segment name | Verified membership in the selected FF_USER_ROWS_DFF ContextCode |
| Range or Match | resolve_range_or_match_lov | Meaning | LookupCode in RangeOrMatch |
| Unit of Measure | resolve_user_key_units_lov | Meaning | LookupCode in UserKeyUnits or DataType |
| Predefined | resolve_predefined_lov | Meaning | LookupCode in Predefined |
| Legislative Data Group | resolve_legislative_data_group | Name | LegislativeDataGroupId and LegislationCode |
| User-defined table | resolve_user_defined_table | UserTableName | UserTableId and mapped table attributes |
| User-defined table column | resolve_user_defined_table_column | UserColumnName | UserColumnId; UserColumnCode must already be supplied and valid when the selected HDL attribute requires it |
| User-defined table row | resolve_user_defined_table_row | RowName or RowLowRangeOrName | UserRowId and mapped row attributes |
| Row-flex value set | resolve_user_defined_row_flex_value_set | Value | Id or Value as directed by the flex attribute metadata |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UDT.RESOLVE_REFERENCES | step | 5 | reference_lookup | resolved_or_not_needed->UDT.EXECUTION_GATE;blocked->UDT.RETURN_ISSUES | UDT.DESIGN_GATE | stop | Resolve reference names and LOV display values through the captured read-only Fusion endpoints before preparing import or export data. |

## Sources

- Developer-provided Standard Instructions in the current request.
- /scratch/UDT/UserDefinedTable.csv (SHA-256 f8ead2ff6c3ab862eae19ee045208e32fd3482bd02d3fec3a608158b14506b27)
- /scratch/UDT/UserDefinedTableColumn.csv (SHA-256 1cac7497b66b80fbdac0f3ad690f98edb9af6159f1204a660cb3ad39963b4910)
- /scratch/UDT/UserDefinedTableRow.csv (SHA-256 2f7f39ffc2768e12b0cd5b8f5240f6bebe903b67986381a0b9ad86f2ae1f0f98)
- /scratch/UDT/UserDefinedTableColumnInstance.csv (SHA-256 9b74ba8df057f97cb7bad91a21f41dd8541ff3ec40d55e32909e76fea7604f2f)
- Developer-provided UDT general and field-level validation instructions in the current request.
- Developer-provided primary REST endpoints, describe endpoints, finder variants, response mappings, contextual-flex describe flow, and flex value-set LOV contract in the current request.
- Developer-provided Fast Formula type-validation endpoint `/hcmRestApi/resources/latest/fastFormulas?&q=FormulaTypeName=User Table Validation` in the current request.
- Authenticated read-only capture of that Fast Formula endpoint from environment `cptctugqy` on 2026-09-02; the response confirmed the FormulaId, FormulaName, FormulaTypeId, FormulaTypeName, BaseFormulaName, effective-date, and legislative-scope attributes used by this resolver.
- Developer-provided expanded User Defined Tables endpoint `/hcmRestApi/resources/latest/userDefinedTables?expand=userDefinedColumns&finder=findByUserTableId%3BUserTableId=<UserTableId>` in the current request.
- Authenticated read-only capture of that expanded endpoint from environment `cptctugqy` on 2026-09-02; the response confirmed the parent-scoped `userDefinedColumns` collection and its UserColumnId, UserColumnName, BaseUserColumnName, data-type, formula, and legislative attributes. The response did not contain UserColumnCode.

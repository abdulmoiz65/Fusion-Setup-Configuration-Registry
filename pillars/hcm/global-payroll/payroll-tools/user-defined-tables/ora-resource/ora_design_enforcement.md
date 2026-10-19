# User-Defined Tables Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Select the row model | Use matched rows for exact values and range rows only when a low and high range define the business condition. |
| 2 | Define the table matrix | Define columns, dated rows, and cell values as one coherent table design. |
| 3 | Apply optional entry validation | Attach a User Table Validation formula to a column only when it enforces the intended value rule. |
| 4 | Enforce the import route | Load setup data into Fusion only through core.data-loader using HDL for UserDefinedTable. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every table design | Blocker | | The source does not declare one consistent matched or range row model. | Choose M with exact row names or R with complete low and high row bounds before preparing HDL. | Yes |
| A validation formula is assigned | Blocker | resolve_user_table_validation_formula | The supplied FormulaName or FormulaId does not resolve to exactly one formula whose FormulaTypeName is User Table Validation, or the formula does not use text ENTRY_VALUE or does not return FORMULA_STATUS. | Resolve the formula through the captured Fast Formula endpoint and use the documented User Table Validation formula contract; FORMULA_MESSAGE is optional and FORMULA_STATUS returns S or E. | Yes |
| A no-flex HDL source is prepared | Blocker | | UserTableAttributeCategory or a FLEX:FF_USER_ROWS_DFF column is supplied even though the selected variant is without flex context. | Remove the flex-context attributes and retain only the selected business-object attributes. | Yes |
| A row flex context is prepared | Blocker | | UserTableAttributeCategory, FLEX:FF_USER_ROWS_DFF, and context-qualified segment columns do not agree on one context code. | Use one reviewed context code consistently and qualify each row segment with that context. | Yes |
| An HDL operation other than MERGE is requested | Blocker | | The provided metadata and DAT do not establish support for the requested operation. | Keep the request outside this reviewed resource contract until current metadata or Oracle guidance confirms and authors that operation. | No |
| Every Fusion data load | Blocker | | The proposed route is direct REST, manual UI entry, or another non-Data-Loader mechanism. | Use core.data-loader to validate, preview, approve, upload, and initiate the HDL archive for UserDefinedTable. | Yes |
| Financial-services user-defined-tables reference | Informational | | The source is from Oracle Financial Services Lending and Leasing, not Oracle Fusion HCM Payroll. | Do not use its field or setup semantics to author the HCM HDL contract. | Yes |
| An update or correct action is requested for a non-predefined UserDefinedTable | Blocker | | UserTableName or Name, LegislativeDataGroupName or its resolved identity, RangeOrMatch, UserKeyUnits, or UserTableAttributeCategory or Context differs from the existing table | Preserve the existing table name, legislative data group, range-or-match value, unit of measure, and context. Only UserRowTitle or Row Title can be changed at the UserDefinedTable level. | Yes |
| Any action targets a predefined UserDefinedTable | Blocker | resolve_predefined_lov | Predefined resolves to Y | Do not prepare or execute any action for a predefined user-defined table. | No |

## FDOS UDT Creation Enforcement

| Applies When | Blocking Condition | What Must Happen |
|---|---|---|
| A UDT is created with supplied context information | The flow asks for a column name, column code, data type, or cell value instead of deriving it from the supplied context | Stop the intake flow and derive those details solely from the supplied context. |
| A UDT creation request has no context information | The flow proceeds without first obtaining the user's with-context or without-context choice | Ask the required creation-approach confirmation before collecting or deriving creation details. |
| A UDT is created without Row Title or UserRowTitle | The flow blocks or requests Row Title solely because it is absent | Continue without enforcing Row Title; it is optional for UDT creation. |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_user_table_validation_formula | Before accepting FormulaName or FormulaId for a UserDefinedTableColumn validation formula | FormulaId, FormulaName, FormulaTypeName=User Table Validation | ora_reference_lookups.md |
| resolve_predefined_lov | Before evaluating whether any action is permitted for the selected UserDefinedTable | Predefined=LookupCode | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UDT.DESIGN_GATE | decision | 4 | design_enforcement | pass->UDT.RESOLVE_REFERENCES;blocked->UDT.RETURN_ISSUES | UDT.DEPENDENCY_GATE | stop | Enforce a coherent user-defined-table model and the required HDL Data Loader route. |

## Sources

- https://docs.oracle.com/en/cloud/saas/human-resources/faisa/create-a-user-defined-table.html
- https://docs.oracle.com/en/cloud/saas/human-resources/faigp/user-table-validation-formula-type.html
- https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/overview-of-loading-user-defined-tables.html
- https://docs.oracle.com/en/industries/financial-services/financial-lending-leasing-cloud-service/14.12.0.0.0/losga/user-defined-tables.html
- Developer-provided UDT general and field-level validation instructions in the current request.
- Developer-provided Fast Formula type-validation endpoint `/hcmRestApi/resources/latest/fastFormulas?&q=FormulaTypeName=User Table Validation` in the current request.

# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Existing editable setting | Code and Value | Stop | Supply the immutable Code of an existing setting and the desired Value. | Every request | read_collaboration_parameter_by_code |
| External catalog | Code=ORA_VCS_DEFAULT_CATALOG_EXTERNAL and Value=CategorySetName | Stop | Supply one exact category-set name. | External catalog is changed | resolve_external_catalog_by_name |
| VMI requester | Code=VMI_DEFAULT_REQUISITION_REQUESTER and Value=Username | Stop | Supply one exact username. | VMI requester is changed | resolve_user_account_by_username |
| Boundary days | Code=COLLAB_BOUNDARY_DAYS and Value | Stop | Supply a non-negative whole number. | COLLAB_BOUNDARY_TYPE is ORA_VCS_BOUNDARY_DAYS | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Code is not in EditableParameterList | Invalid | Reject the request as a non-editable parameter. | |
| Code is ORA_VCS_SP_DWNLD_MEASURES and Value contains ORA_VCS_COMMIT_REASON_CODE | Verify | Confirm SHOW_REASON_CODES is Y before accepting the value. | read_collaboration_parameter_by_code |
| Code is SHOW_REASON_CODES and Value is N | Verify | Confirm ORA_VCS_SP_DWNLD_MEASURES does not contain ORA_VCS_COMMIT_REASON_CODE. | read_collaboration_parameter_by_code |
| Code is a download horizon, aggregation level, or view type | Verify | Evaluate the three-setting compatibility rule before accepting the value. | read_collaboration_parameter_by_code |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Immutable fields | Reject changes to Code, Description, DataType, LastUpdatedBy, LastUpdateDate, and ObjectVersionNumber. | Every request | |
| Required Value | Reject a null or empty Value; the REST contract marks Value required. | Every request | |
| Editable-code allowlist | Reject every code not in EditableParameterList with VCS_INVD_PARAM_CODE. | Every request | |
| Non-negative integer | Require a whole number greater than or equal to zero. | A code uses NonNegIntegerValidator. | |
| Integer and bounded ranges | Require an integer in the code-specific range: 1-9999, 0-9999, 0-999, 0-1825, or 1-999. | A code uses an IntegerRange validator. | |
| Yes or No | Require the exact LookupCode `Y` or `N` and retain it unchanged in Value. Reject display meanings such as `Yes` or `No`. | A code uses YesNoValidator. | resolve_vcs_lookup_code |
| Generic lookup code | Require an exact allowed LookupCode; retain each validated code unchanged in Value and validate every comma-separated token when multiple values are allowed. Reject a Meaning or lookup identifier. | A code uses LookupValidator or DownloadMeasuresValidator. | resolve_vcs_lookup_code |
| External catalog input mapping | Validate the supplied category-set name and retain that exact name in Value. The service resolves its stored identifier after validation. | Code is ORA_VCS_DEFAULT_CATALOG_EXTERNAL. | resolve_external_catalog_by_name |
| Requester input mapping | Validate the supplied username and retain that exact username in Value. The service resolves its stored person identifier after validation. | Code is VMI_DEFAULT_REQUISITION_REQUESTER. | resolve_user_account_by_username |
| Null sentinel conversion | Convert null to -1; convert -1 back to null for display. | Code is ORA_VCS_SP_DWNLD_MEASURES or ORA_VCS_SP_DWNLD_COMMIT_QTY. | |
| Server-only validators | Let the service validate UOM, planning-calendar, planning-time-level, and integer values where no source-provided REST lookup contract exists. | The applicable Java validator is selected. | |

## Validator Coverage Matrix

All codes in this matrix are editable-code allowlist members. A code not listed
here must still pass the allowlist and its service-selected validator; it is not
safe to infer a validation rule from its seed value or display label.

| Validation family | Setting Codes | Value Contract |
|---|---|---|
| Yes/No | ORA_VCS_UPDATE_EXT_ORG_ON_HAND; ORA_VCS_CM_INITIATE_SUPPLY_DATA_ESS_JOB; VMI_ALLOW_FULL_DATA_ACCESS; VMI_ENABLE_ACCESS_DATA_SECURITY; ALLOW_FULL_DATA_ACCESS; ENABLE_ACCESS_DATA_SECURITY; CREATE_MISSING_AGGREGATED_FORECAST_BUCKETS; ENABLE_EXTERNAL_COLLAB_SOURCE_SYSTEM; ORA_VCS_SP_DWNLD_COMMIT_QTY_LCK_FLAG; ORA_VCS_SP_DWNLD_HORIZON_LCK_FLAG; ORA_VCS_SP_DWNLD_MEASURES_LCK_FLAG; ORA_VCS_SP_DWNLD_TIME_AGGR_LEVEL_LCK_FLAG; ORA_VCS_SP_DWNLD_VIEW_TYPE_LCK_FLAG; ORA_VCS_SCC_SCP_MEASURE_MAPPING; SHOW_ENTERPRISE_USERNAMES_SUPPLIER_PORTAL_SC; SHOW_ENTERPRISE_USERNAMES_SUPPLIER_PORTAL_VMI; SHOW_PURCHASE_ORDERS_SUPPLIER_PORTAL_SC; SHOW_ENTERPRISE_ON_HAND_QUANTITIES_SUPPLIER_PORTAL_SC; ORA_VCS_SP_DWNLD_REF_NUMBERS; ORA_VCS_SP_DWNLD_REF_NUMBERS_LCK_FLAG; SHOW_ADDL_INFO_FIELDS; SHOW_ADDL_INFO_FIELDS_SP; ENABLE_SUPPLY_COLLABORATION_NOTES; ORA_VCS_SP_CONTROL_B2B_PUBLISH; ORA_VCS_SP_EXCLD_UNPUB_ZERO_QTYS; ENABLE_CUSTOMER_ITEM_COLLABORATION_DC; ORA_VCS_SP_CALCULATE_FORECAST_CHANGES_MISMATCHES; ORA_VCS_SP_CALCULATE_COMMIT_MISMATCHES; ORA_VCS_SP_CALCULATE_ITEM_MAPE; ORA_VCS_ENABLE_CMK_EVALUATION | Submit `Y` or `N` unchanged. SHOW_REASON_CODES also uses `Y` or `N`, with its separate reason-code dependency rule. |
| Non-negative integer | MARK_REP_REQUESTS_AS_DELIVERED_SCHEDULE; FORECAST_DOWNLOAD_ONLINE_LIMIT; UNMANAGED_PUBLISH_CYCLE; PURGE_VMI_REL_INT_SCHEDULE; COLLAB_BOUNDARY_DAYS; SUPPLY_PLANNING_FORECASTS_INTERFACE_DATA_RETENTION_DAYS; SUPPLY_PLANNING_COMMITS_INTERFACE_DATA_RETENTION_DAYS; SUPPLY_PLANNING_UPLOAD_FILE_RETENTION_DAYS; VMI_REP_REQUESTS_UPLOAD_FILE_RETENTION_DAYS; VMI_MIN_MAX_UPLOAD_FILE_RETENTION_DAYS; UPLOAD_SUPPLIER_ON_HAND_FILE_RETENTION_DAYS; VMI_ITEMS_UPPER_LIMIT; SUPPLY_PLANNING_CONVERTED_CANDIDATES_RETENTION_DAYS; SUPPLY_PLANNING_UNPROCESSED_RETENTION_DAYS; SUPPLY_PLANNING_DATA_REQUESTS_RETENTION_DAYS; VMI_REQUESTS_UPPER_LIMIT; VMI_REPL_REQ_UPPER_LIMIT; SP_FORECASTS_UPPER_LIMIT; SP_DETAILS_UPPER_LIMIT; SP_RELATIONSHIPS_UPPER_LIMIT; SP_UNPROCESSED_FORECASTS_UPPER_LIMIT; SP_EXCEPTIONS_UPPER_LIMIT; CUSTOMER_DEMAND_INTERFACE_RETENTION_DAYS; UPLOAD_CUSTOMER_DEMAND_FILE_RETENTION_DAYS; PURGE_DELETED_COLLAB_DOCS_SCP_SCHEDULE | Submit a base-10 whole number greater than or equal to zero. |
| Integer | VMI_ITEMS_TOTAL_COUNT | Submit a base-10 whole number. |
| Bounded integer | CUSTOMER_DEMAND_DEFAULT_HORIZON; FORECAST_DL_HORIZONTAL_DAYS_UPPER_LIMIT | Submit an integer from 1 through 9999. |
| Bounded integer | CUSTOMER_DEMAND_DEFAULT_HISTORY; SUPPLY_PLANNING_PREVIOUS_FORECAST_RETENTION_DAYS | Submit an integer from 0 through 9999. |
| Bounded integer | DEFAULT_COMMIT_HORIZON; DEFAULT_FORECAST_HORIZON | Submit an integer from 0 through 1825. |
| Bounded integer | CUSTOMER_DEMAND_MULTI_DELETE_UPPER_LIMIT; CUSTOMER_DEMAND_MULTI_EDIT_UPPER_LIMIT; CUSTOMER_DEMAND_MULTI_DOWNLOAD_UPPER_LIMIT; ORA_VCS_SC_CALENDAR_HISTORY_BOUNDARY | Submit an integer from 1 through 999. |
| Boundary type | COLLAB_BOUNDARY_TYPE | Resolve an exact `ORA_VCS_COLLAB_BOUNDARY_TYPE` LookupCode and submit it unchanged. |
| Plan-edit option | ORA_VCS_SP_DWNLD_COMMIT_QTY | Resolve an exact `ORA_VCS_PLAN_EDIT_OPTIONS` LookupCode and submit it unchanged. Reject ORA_VCS_INPUT_VAL. |
| Download horizon, aggregation, and layout | ORA_VCS_SP_DWNLD_HORIZON; ORA_VCS_SP_DWNLD_TIME_AGGR_LEVEL; ORA_VCS_SP_DWNLD_VIEW_TYPE | Resolve an exact LookupCode from, respectively, ORA_VCS_CP_DL_HORIZON, ORA_VCS_CP_DL_AGGR_LEVEL, or ORA_VCS_CP_DL_LAYOUT; submit it unchanged and satisfy the three-setting compatibility rule. |
| Download measures | ORA_VCS_SP_DWNLD_MEASURES | Resolve each comma-separated exact `ORA_VCS_COLLAB_ORDER_TYPES` LookupCode; retain the comma-separated codes. If ORA_VCS_COMMIT_REASON_CODE is present, SHOW_REASON_CODES must be `Y`. |
| Displayed measures | ORA_VCS_SC_DISPLAYED_MEASURES | Resolve each comma-separated exact `ORA_VCS_COLLAB_MEASURES_TYPES` LookupCode and retain the comma-separated codes. |
| CSV number formatting | ORA_VCS_SP_CSV_NUMBER_FORMATTING; ORA_VCS_VMI_CSV_NUMBER_FORMATTING | Resolve each comma-separated exact `ORA_VCS_NUM_FORMAT` LookupCode and retain the codes. |
| CSV delimiter | ORA_VCS_SP_CSV_DELIMITER; ORA_VCS_VMI_CSV_DELIMITER | Resolve each comma-separated exact `ORA_VCS_FILE_DELIMITER` LookupCode and retain the codes. |
| External catalog | ORA_VCS_DEFAULT_CATALOG_EXTERNAL | Submit the validated category-set name; the service converts it internally. |
| VMI requester | VMI_DEFAULT_REQUISITION_REQUESTER | Submit the validated username; the service converts it internally. |
| Planning calendar | ORA_VCS_SCC_SCP_DEFAULT_PLANNING_CALENDAR | Submit `-1` or a valid numeric planning-calendar identifier. This is service-validated; no public REST lookup is asserted by this task. |
| Planning time level | ORA_VCS_SCC_SCP_DEFAULT_PLANNING_TIME_LEVEL | Submit `-1` or a valid numeric planning-time-level identifier. This is service-validated; no public REST lookup is asserted by this task. |
| UOM | ORA_MSC_BP_DEFAULT_WEIGHT_UOM; ORA_MSC_BP_DEFAULT_VOLUME_UOM | Submit a source-system-recognized unit-of-measure code unchanged. This is service-validated; no public REST lookup is asserted by this task. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCS.VALIDATE_INPUT | step | 20 | validate_input | valid->CCS.RESOLVE_DEPENDENCIES;invalid->CCS.HANDLE_ERROR | CCS.REFERENCE_PARAMETERS | stop | A setting update is prepared. |

# Defaulting Rules

These are seed-data baseline values. They are
comparison defaults only: Value remains mandatory in a REST update and no row
is silently applied to an incomplete request. Baseline-only values are
technical counters, timestamps, or system-maintained execution state.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ALLOW_FULL_DATA_ACCESS | Y | Seed baseline | No - review before override | |
| COLLAB_BOUNDARY_DAYS | 0 | Seed baseline | No - review before override | |
| COLLAB_BOUNDARY_TYPE | ORA_VCS_BOUNDARY_DAYS | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| CREATE_MISSING_AGGREGATED_FORECAST_BUCKETS | N | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| CUSTOMER_DEMAND_DEFAULT_HISTORY | 0 | Seed baseline | No - review before override | |
| CUSTOMER_DEMAND_DEFAULT_HORIZON | 550 | Seed baseline | No - review before override | |
| CUSTOMER_DEMAND_INTERFACE_RETENTION_DAYS | 10 | Seed baseline | No - review before override | |
| CUSTOMER_DEMAND_MULTI_DELETE_UPPER_LIMIT | 25 | Seed baseline | No - review before override | |
| CUSTOMER_DEMAND_MULTI_DOWNLOAD_UPPER_LIMIT | 250 | Seed baseline | No - review before override | |
| CUSTOMER_DEMAND_MULTI_EDIT_UPPER_LIMIT | 25 | Seed baseline | No - review before override | |
| DEFAULT_COMMIT_HORIZON | 730 | Seed baseline | No - review before override | |
| DEFAULT_FORECAST_HORIZON | 730 | Seed baseline | No - review before override | |
| ENABLE_ACCESS_DATA_SECURITY | Y | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ENABLE_EXTERNAL_COLLAB_SOURCE_SYSTEM | Y | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ENABLE_SUPPLY_COLLABORATION_NOTES | N | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| FORECAST_DL_HORIZONTAL_DAYS_UPPER_LIMIT | 90 | Seed baseline | No - review before override | |
| FORECAST_DOWNLOAD_ONLINE_LIMIT | 250 | Seed baseline | No - review before override | |
| MARK_REP_REQUESTS_AS_DELIVERED_LAST_RUN | 20180905163411 | System-maintained baseline | No - baseline-only | |
| MARK_REP_REQUESTS_AS_DELIVERED_SCHEDULE | 24 | Seed baseline | No - review before override | |
| ORA_MSC_BP_DEFAULT_VOLUME_UOM | -1 | Seed baseline | No - review before override | |
| ORA_MSC_BP_DEFAULT_WEIGHT_UOM | -1 | Seed baseline | No - review before override | |
| ORA_VCS_CM_INITIATE_SUPPLY_DATA_ESS_JOB | Y | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_DC_IDENTITY_TOTAL_COUNT | -1 | System-maintained baseline | No - baseline-only | |
| ORA_VCS_DEFAULT_CATALOG_EXTERNAL | 10150 stored baseline; submit an exact category-set name for Value | Seed baseline | No - review before override | resolve_external_catalog_by_name |
| ORA_VCS_OTBI_WATERFALL_DASHBOARD | /analytics/saw.dll?Dashboard&PortalPath={PORTAL_PATH}&page={PORTAL_PAGE} | Seed baseline | No - review before override | |
| ORA_VCS_SCC_SCP_DEFAULT_PLANNING_CALENDAR | -1 | Seed baseline | No - review before override | |
| ORA_VCS_SCC_SCP_DEFAULT_PLANNING_TIME_LEVEL | -1 | Seed baseline | No - review before override | |
| ORA_VCS_SCC_SCP_MEASURE_MAPPING | Y | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SC_CALENDAR_HISTORY_BOUNDARY | 100 | Seed baseline | No - review before override | |
| ORA_VCS_SC_DISPLAYED_MEASURES | ORA_VCS_PREVIOUS_FORECAST,ORA_VCS_PREVIOUS_COMMIT,ORA_VCS_CURRENT_FORECAST,ORA_VCS_CURRENT_COMMIT,ORA_VCS_CUMULATIVE_FORECAST,ORA_VCS_CUMULATIVE_COMMIT,ORA_VCS_OPEN_PUR_ORD,ORA_VCS_PUR_REQ,ORA_VCS_SHIP_IN_RECEIVING,ORA_VCS_IN_TRANSIT_SHIP,ORA_VCS_ON_HAND_QTY,ORA_VCS_SUP_ON_HAND_QTY,ORA_VCS_COMMIT_MIS_REASON_CODE | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_CALCULATE_COMMIT_MISMATCHES | Y | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_CALCULATE_FORECAST_CHANGES_MISMATCHES | Y | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_CALCULATE_ITEM_MAPE | Y | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_CONTROL_B2B_PUBLISH | N | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_CSV_DELIMITER | ORA_VCS_COMMA | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_CSV_NUMBER_FORMATTING | ORA_VCS_DECIMAL_NO_THOUS_SEP | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_DWNLD_COMMIT_QTY | -1 | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_DWNLD_COMMIT_QTY_LCK_FLAG | N | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_DWNLD_HORIZON | ORA_VCS_CP_DL_FORECAST | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_DWNLD_HORIZON_LCK_FLAG | N | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_DWNLD_MEASURES | ORA_VCS_PO,ORA_VCS_PR,ORA_VCS_IN_TRANSIT,ORA_VCS_IN_RECEIVING | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_DWNLD_MEASURES_LCK_FLAG | N | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_DWNLD_REF_NUMBERS | N | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_DWNLD_REF_NUMBERS_LCK_FLAG | N | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_DWNLD_TIME_AGGR_LEVEL | ORA_VCS_CP_AGGR_DAY | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_DWNLD_TIME_AGGR_LEVEL_LCK_FLAG | N | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_DWNLD_VIEW_TYPE | ORA_VCS_CP_DL_VERTICAL | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_DWNLD_VIEW_TYPE_LCK_FLAG | N | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_SP_EXCLD_UNPUB_ZERO_QTYS | N | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_UPDATE_EXT_ORG_ON_HAND | Y | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_VMI_CSV_DELIMITER | ORA_VCS_COMMA | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| ORA_VCS_VMI_CSV_NUMBER_FORMATTING | ORA_VCS_DECIMAL_NO_THOUS_SEP | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| PURGE_DELETED_COLLAB_DOCS_SCP_LAST_RUN | 20200423095134 | System-maintained baseline | No - baseline-only | |
| PURGE_DELETED_COLLAB_DOCS_SCP_SCHEDULE | 12 | Seed baseline | No - review before override | |
| PURGE_VMI_REL_INT_SCHEDULE | 7 | Seed baseline | No - review before override | |
| SHOW_ADDL_INFO_FIELDS | N | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| SHOW_ADDL_INFO_FIELDS_SP | N | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| SHOW_ENTERPRISE_ON_HAND_QUANTITIES_SUPPLIER_PORTAL_SC | Y | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| SHOW_ENTERPRISE_USERNAMES_SUPPLIER_PORTAL_SC | N | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| SHOW_ENTERPRISE_USERNAMES_SUPPLIER_PORTAL_VMI | N | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| SHOW_PURCHASE_ORDERS_SUPPLIER_PORTAL_SC | Y | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| SHOW_REASON_CODES | N | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| SP_DETAILS_TOTAL_COUNT | -1 | System-maintained baseline | No - baseline-only | |
| SP_DETAILS_UPPER_LIMIT | 1000000 | Seed baseline | No - review before override | |
| SP_EXCEPTIONS_TOTAL_COUNT | -1 | System-maintained baseline | No - baseline-only | |
| SP_EXCEPTIONS_UPPER_LIMIT | 500000 | Seed baseline | No - review before override | |
| SP_FORECASTS_TOTAL_COUNT | -1 | System-maintained baseline | No - baseline-only | |
| SP_FORECASTS_UPPER_LIMIT | 100000 | Seed baseline | No - review before override | |
| SP_RELATIONSHIPS_TOTAL_COUNT | -1 | System-maintained baseline | No - baseline-only | |
| SP_RELATIONSHIPS_UPPER_LIMIT | 200000 | Seed baseline | No - review before override | |
| SP_UNPROCESSED_FORECASTS_TOTAL_COUNT | -1 | System-maintained baseline | No - baseline-only | |
| SP_UNPROCESSED_FORECASTS_UPPER_LIMIT | 100000 | Seed baseline | No - review before override | |
| SUPPLY_PLANNING_COMMITS_INTERFACE_DATA_RETENTION_DAYS | 30 | Seed baseline | No - review before override | |
| SUPPLY_PLANNING_CONVERTED_CANDIDATES_RETENTION_DAYS | 7 | Seed baseline | No - review before override | |
| SUPPLY_PLANNING_DATA_REQUESTS_RETENTION_DAYS | 10 | Seed baseline | No - review before override | |
| SUPPLY_PLANNING_FORECASTS_INTERFACE_DATA_RETENTION_DAYS | 30 | Seed baseline | No - review before override | |
| SUPPLY_PLANNING_PREVIOUS_FORECAST_RETENTION_DAYS | 1825 | Seed baseline | No - review before override | |
| SUPPLY_PLANNING_UNPROCESSED_RETENTION_DAYS | 120 | Seed baseline | No - review before override | |
| SUPPLY_PLANNING_UPLOAD_FILE_RETENTION_DAYS | 30 | Seed baseline | No - review before override | |
| UNMANAGED_PUBLISH_CYCLE | 15 | Seed baseline | No - review before override | |
| UPLOAD_CUSTOMER_DEMAND_FILE_RETENTION_DAYS | 14 | Seed baseline | No - review before override | |
| UPLOAD_SUPPLIER_ON_HAND_FILE_RETENTION_DAYS | 30 | Seed baseline | No - review before override | |
| VMI_ALLOW_FULL_DATA_ACCESS | N | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| VMI_DEFAULT_REQUISITION_REQUESTER | -1 stored baseline; submit an exact username for Value | Seed baseline | No - review before override | resolve_user_account_by_username |
| VMI_ENABLE_ACCESS_DATA_SECURITY | Y | Seed baseline | No - review before override | resolve_vcs_lookup_code |
| VMI_ITEMS_TOTAL_COUNT | -1 | System-maintained baseline | No - baseline-only | |
| VMI_ITEMS_UPPER_LIMIT | 100000 | Seed baseline | No - review before override | |
| VMI_MIN_MAX_UPLOAD_FILE_RETENTION_DAYS | 30 | Seed baseline | No - review before override | |
| VMI_REPL_REQ_TOTAL_COUNT | 0 | System-maintained baseline | No - baseline-only | |
| VMI_REPL_REQ_UPPER_LIMIT | 5000 | Seed baseline | No - review before override | |
| VMI_REP_REQUESTS_UPLOAD_FILE_RETENTION_DAYS | 30 | Seed baseline | No - review before override | |
| ORA_VCS_ENABLE_CMK_EVALUATION | Y | Seed baseline | No - review before override | resolve_vcs_lookup_code |

## Configuration Description Index

Use this source-derived index when an integrator identifies a setting by its
business purpose rather than `ConfigParameterCode`. The code remains the
authoritative lookup, validation, and import key; descriptions are
informational and are not accepted as REST identifiers.

| Field | Configuration Description |
|---|---|
| ALLOW_FULL_DATA_ACCESS | Allows full access to all collaboration planners when data access security is enabled and no collaboration planner is assigned to the relationship. |
| COLLAB_BOUNDARY_DAYS | Number of days in the past open for current order forecast and commit collaboration; used only when COLLAB_BOUNDARY_TYPE is ORA_VCS_BOUNDARY_DAYS. |
| COLLAB_BOUNDARY_TYPE | Collaboration date boundary for updating past buckets: days, current week, or current period. |
| CREATE_MISSING_AGGREGATED_FORECAST_BUCKETS | Allows creation of aggregated buckets for missing collaboration order forecast quantities. |
| CUSTOMER_DEMAND_DEFAULT_HISTORY | Default number of past days open for customer demand when measure history is unspecified. |
| CUSTOMER_DEMAND_DEFAULT_HORIZON | Default number of future days open for customer demand when measure horizon is unspecified. |
| CUSTOMER_DEMAND_INTERFACE_RETENTION_DAYS | Number of days customer demand and request errors are retained in interface tables. |
| CUSTOMER_DEMAND_MULTI_DELETE_UPPER_LIMIT | UI upper limit for selecting multiple collaboration documents to delete. |
| CUSTOMER_DEMAND_MULTI_DOWNLOAD_UPPER_LIMIT | UI upper limit for selecting multiple collaboration documents to download. |
| CUSTOMER_DEMAND_MULTI_EDIT_UPPER_LIMIT | UI upper limit for selecting multiple collaboration documents to edit. |
| DEFAULT_COMMIT_HORIZON | Default collaboration relationship commit horizon. |
| DEFAULT_FORECAST_HORIZON | Default collaboration relationship forecast horizon. |
| ENABLE_ACCESS_DATA_SECURITY | Enables enterprise data access security for Supply Planning Collaboration. |
| ENABLE_EXTERNAL_COLLAB_SOURCE_SYSTEM | Allows collaboration using supply plans created with Supply Chain Planning external source systems. |
| ENABLE_SUPPLY_COLLABORATION_NOTES | Allows collaboration planners and suppliers to share notes about an order forecast. |
| FORECAST_DL_HORIZONTAL_DAYS_UPPER_LIMIT | Upper limit for downloading order forecasts with horizontal layout and daily aggregation. |
| FORECAST_DOWNLOAD_ONLINE_LIMIT | Number of collaboration order forecasts permitted for real-time download before a scheduled process is used. |
| MARK_REP_REQUESTS_AS_DELIVERED_LAST_RUN | Read-only last time fully delivered historical replenishment requests were marked delivered. |
| MARK_REP_REQUESTS_AS_DELIVERED_SCHEDULE | Frequency, in hours, for marking fully delivered historical replenishment requests delivered. |
| ORA_MSC_BP_DEFAULT_VOLUME_UOM | Default volume unit of measure code used in buyer planning. |
| ORA_MSC_BP_DEFAULT_WEIGHT_UOM | Default weight unit of measure code used in buyer planning. |
| ORA_VCS_CM_INITIATE_SUPPLY_DATA_ESS_JOB | Initiates collections automatically when supply data is received for externally managed organizations. |
| ORA_VCS_DC_IDENTITY_TOTAL_COUNT | Total number of active demand collaboration identities. |
| ORA_VCS_DEFAULT_CATALOG_EXTERNAL | Default external catalog name used when returning external source-system collaboration order forecasts. |
| ORA_VCS_OTBI_WATERFALL_DASHBOARD | Read-only relative URL for SCC contextual OTBI reports launched from Manage Order Forecasts and Commits. |
| ORA_VCS_SCC_SCP_DEFAULT_PLANNING_CALENDAR | Planning calendar default for Receive Collaboration Customer Demand; use -1 to set null. |
| ORA_VCS_SCC_SCP_DEFAULT_PLANNING_TIME_LEVEL | Planning time-level default for Receive Collaboration Customer Demand; use -1 to set null. |
| ORA_VCS_SCC_SCP_MEASURE_MAPPING | Identifies whether demand collaboration measures can be received only by specified seeded Supply Chain Planning measures. |
| ORA_VCS_SC_CALENDAR_HISTORY_BOUNDARY | Default number of past days for which calendar buckets are created when data is processed into Supply Collaboration. |
| ORA_VCS_SC_DISPLAYED_MEASURES | Measures displayed in the Edit Order Forecast Details grid. |
| ORA_VCS_SP_CALCULATE_COMMIT_MISMATCHES | Whether commit mismatches are calculated during a commit process. |
| ORA_VCS_SP_CALCULATE_FORECAST_CHANGES_MISMATCHES | Whether forecast-change mismatches are calculated during Supply Planning Collaboration Decomposition. |
| ORA_VCS_SP_CALCULATE_ITEM_MAPE | Whether item MAPEs are calculated during Supply Planning Collaboration Decomposition; not calculated if forecast-change mismatches are disabled. |
| ORA_VCS_SP_CONTROL_B2B_PUBLISH | Whether the B2B publish process is initiated by the Publish B2B Outbound Messages for Order Forecasts process. |
| ORA_VCS_SP_CSV_DELIMITER | Delimiter used when downloading and uploading Supply Planning Collaboration CSV files. |
| ORA_VCS_SP_CSV_NUMBER_FORMATTING | Number formatting used when downloading and uploading Supply Planning Collaboration CSV files. |
| ORA_VCS_SP_DWNLD_COMMIT_QTY | Forecast-download default for commit quantities; can be current forecast, previous commit, or null. |
| ORA_VCS_SP_DWNLD_COMMIT_QTY_LCK_FLAG | Whether the forecast-download default for commit quantities is locked. |
| ORA_VCS_SP_DWNLD_HORIZON | Forecast-download default for horizon; accepted values are in lookup type ORA_VCS_CP_DL_HORIZON. |
| ORA_VCS_SP_DWNLD_HORIZON_LCK_FLAG | Whether the forecast-download default horizon is locked. |
| ORA_VCS_SP_DWNLD_MEASURES | Forecast-download default measures; multiple measures may be selected, or the setting may be null. |
| ORA_VCS_SP_DWNLD_MEASURES_LCK_FLAG | Whether the forecast-download default for measures is locked. |
| ORA_VCS_SP_DWNLD_REF_NUMBERS | Whether forecast downloads include reference numbers. |
| ORA_VCS_SP_DWNLD_REF_NUMBERS_LCK_FLAG | Whether the forecast-download default for reference numbers is locked. |
| ORA_VCS_SP_DWNLD_TIME_AGGR_LEVEL | Forecast-download default aggregation level: day or week. |
| ORA_VCS_SP_DWNLD_TIME_AGGR_LEVEL_LCK_FLAG | Whether the forecast-download default aggregation level is locked. |
| ORA_VCS_SP_DWNLD_VIEW_TYPE | Forecast-download default layout: horizontal or vertical. |
| ORA_VCS_SP_DWNLD_VIEW_TYPE_LCK_FLAG | Whether the forecast-download default layout is locked. |
| ORA_VCS_SP_EXCLD_UNPUB_ZERO_QTYS | Whether to exclude previously unpublished zero-quantity order forecasts during Supply Planning Collaboration Decomposition. |
| ORA_VCS_UPDATE_EXT_ORG_ON_HAND | Updates supplier-provided on-hand quantities for externally managed organizations from the most recently published order forecasts. |
| ORA_VCS_VMI_CSV_DELIMITER | Delimiter used when downloading and uploading VMI CSV files. |
| ORA_VCS_VMI_CSV_NUMBER_FORMATTING | Number formatting used when downloading and uploading VMI CSV files. |
| PURGE_DELETED_COLLAB_DOCS_SCP_LAST_RUN | Read-only last time the Purge Deleted Collaboration Documents ESS job ran. |
| PURGE_DELETED_COLLAB_DOCS_SCP_SCHEDULE | Frequency, in hours, for purging deleted collaboration documents from the Supply Chain Planning data repository. |
| PURGE_VMI_REL_INT_SCHEDULE | Number of days Vendor-Managed Inventory relationships are retained in interface tables. |
| SHOW_ADDL_INFO_FIELDS | Whether to show additional information fields in Supply Collaboration. |
| SHOW_ADDL_INFO_FIELDS_SP | Whether to show additional information fields in Supplier Portal for Supply Collaboration. |
| SHOW_ENTERPRISE_ON_HAND_QUANTITIES_SUPPLIER_PORTAL_SC | Whether to show enterprise on-hand quantities in Supplier Portal for Supply Collaboration. |
| SHOW_ENTERPRISE_USERNAMES_SUPPLIER_PORTAL_SC | Whether to show enterprise usernames in Supplier Portal for Supply Collaboration. |
| SHOW_ENTERPRISE_USERNAMES_SUPPLIER_PORTAL_VMI | Whether to show enterprise usernames in Supplier Portal for Vendor-Managed Inventory. |
| SHOW_PURCHASE_ORDERS_SUPPLIER_PORTAL_SC | Whether to show purchase orders in Supplier Portal for Supply Collaboration. |
| SHOW_REASON_CODES | Whether to show supplier commit reason codes in Supply Collaboration. |
| SP_DETAILS_TOTAL_COUNT | Total number of active Forecast Details. |
| SP_DETAILS_UPPER_LIMIT | Total Forecast Details supported for high-cost features. |
| SP_EXCEPTIONS_TOTAL_COUNT | Total number of active Exceptions. |
| SP_EXCEPTIONS_UPPER_LIMIT | Total Exceptions supported for high-cost features. |
| SP_FORECASTS_TOTAL_COUNT | Total number of active Forecasts. |
| SP_FORECASTS_UPPER_LIMIT | Total Forecasts supported for high-cost features. |
| SP_RELATIONSHIPS_TOTAL_COUNT | Total number of active Relationships. |
| SP_RELATIONSHIPS_UPPER_LIMIT | Total Relationships supported for high-cost features. |
| SP_UNPROCESSED_FORECASTS_TOTAL_COUNT | Total number of Relationship Candidates. |
| SP_UNPROCESSED_FORECASTS_UPPER_LIMIT | Total Relationship Candidates supported for high-cost features. |
| SUPPLY_PLANNING_COMMITS_INTERFACE_DATA_RETENTION_DAYS | Number of days Supply Planning Collaboration commits are retained in interface tables. |
| SUPPLY_PLANNING_CONVERTED_CANDIDATES_RETENTION_DAYS | Number of days converted relationship candidates are retained in the unprocessed-data table. |
| SUPPLY_PLANNING_DATA_REQUESTS_RETENTION_DAYS | Number of days supply data requests are retained in the VCS_IMPORT_DATA_REQUESTS table. |
| SUPPLY_PLANNING_FORECASTS_INTERFACE_DATA_RETENTION_DAYS | Number of days Supply Planning Collaboration forecasts and request-status details are retained in interface tables. |
| SUPPLY_PLANNING_PREVIOUS_FORECAST_RETENTION_DAYS | Number of days previous forecasts are retained and potentially visible in Manage Order Forecasts and Commits. |
| SUPPLY_PLANNING_UNPROCESSED_RETENTION_DAYS | Number of days unprocessed records are retained in the unprocessed-data table. |
| SUPPLY_PLANNING_UPLOAD_FILE_RETENTION_DAYS | Number of days Supply Planning Collaboration upload files are retained in tables. |
| UNMANAGED_PUBLISH_CYCLE | Number of days before the B2B-only cycle expires. |
| UPLOAD_CUSTOMER_DEMAND_FILE_RETENTION_DAYS | Number of days customer demand upload files are retained in tables. |
| UPLOAD_SUPPLIER_ON_HAND_FILE_RETENTION_DAYS | Number of days supplier on-hand quantity upload files are retained in tables. |
| VMI_ALLOW_FULL_DATA_ACCESS | Allows full access to VMI analysts when data access security is enabled and no analyst is assigned to the VMI relationship. |
| VMI_DEFAULT_REQUISITION_REQUESTER | Username for the default requisition requester for VMI relationships without a defined requisition requester. |
| VMI_ENABLE_ACCESS_DATA_SECURITY | Enables enterprise data access security for Vendor-Managed Inventory. |
| VMI_ITEMS_TOTAL_COUNT | Total number of active VMI replenishment items. |
| VMI_ITEMS_UPPER_LIMIT | Total VMI replenishment items supported for run-time analytical features. |
| VMI_MIN_MAX_UPLOAD_FILE_RETENTION_DAYS | Number of days VMI minimum and maximum quantity upload files are retained in tables. |
| VMI_REPL_REQ_TOTAL_COUNT | Read-only total number of active VMI replenishment requests. |
| VMI_REPL_REQ_UPPER_LIMIT | Total VMI replenishment requests supported for run-time analytical features. |
| VMI_REP_REQUESTS_UPLOAD_FILE_RETENTION_DAYS | Number of days VMI replenishment request upload files are retained in tables. |
| ORA_VCS_ENABLE_CMK_EVALUATION | Whether CMK (B2B) messaging is enabled for Supply Planning and Demand Collaboration; Y or null enables it and N disables it. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCS.REVIEW_DEFAULT_BASELINE | step | 40 | apply_default | reviewed->CCS.ENFORCE_DESIGN | CCS.RESOLVE_DEPENDENCIES | stop | A requested value is compared with the seed baseline; no missing Value is filled. |

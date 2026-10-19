# Manage Order Management Parameters Input Validation

Oracle documents this task as the place to set parameters that affect behavior across all of Order Management. Configure only documented parameter values.

## Oracle Guidance Source

Use Oracle's [Manage Order Management Parameters — 26c](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faiom/manage-order-management-parameters.html#Order-Management-Parameters) guide as the source for parameter behavior, defaults, and documented ranges.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Parameter change decision | Parameter name, intended value, and approval evidence | Stop before changing setup | Provide the approved parameter decision | Any parameter change request | resolve_order_management_parameter |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| PATCH parameter-value payload | Require nonblank `ParameterValueId` and `ParameterId`. Set `ParameterId` to the canonical parent `ParameterId` returned by `resolve_order_management_parameter`; reject a missing or different value. Do not derive the parent identifier from `ParameterValueId`. | A `PATCH` row for `qpParameterValues` is prepared. | resolve_order_management_parameter |
| Days to Retry Recovery for Business Events | Accept an integer from 0 through 30. Oracle documents 5 as the predefined value. A value of 0 disables recovery retry. | The parameter is changed | |
| Number of Processes for Order Import | Accept no more than 60. Oracle documents 4 as the default and recommends changing it only for observed import-performance issues, ideally after Oracle Support consultation. | The parameter is changed | |
| Response Time in Seconds or Response Time in Seconds for Copy Action | When supplied, accept an integer from 5 through 240 seconds. An unset value has the Oracle-documented behavior for the applicable action. | Either parameter is changed | |
| Use Pricing Algorithms to Calculate Totals for Sales Order | Accept Yes or No. Yes uses a pricing algorithm to calculate each imported sales-order total; No uses predefined logic that Oracle documents as tuned for performance. | The parameter is changed | |
| Notify Frequency | Accept an integer greater than or equal to 0. A value of 0 sends each notification when its event occurs instead of consolidating notifications. | The parameter is changed | |
| Source order system level | For a parameter whose ParameterLevelCode is source order system, accept either All or nonblank source-system text. Resolve a specific source system exactly once before preparing the parameter value. | A source order system is supplied for a source-order-system-level parameter. | resolve_pricing_source_order_system |
| Site level | Require exactly one parameter-value row with a null ParameterLevelValue. | A parameter whose ParameterLevelCode is SITE is prepared or validated. | |
| Business unit level | For a parameter whose ParameterLevelCode is BUSINESS_UNIT, accept OrgId -1 for all business units or a specific business unit that resolves exactly once; use its BusinessUnitId as OrgId and set ParameterLevelValue to `LOV_ParameterLevelValue`. | A business unit is supplied for a business-unit-level parameter. | resolve_fin_business_unit |
| Item Validation Organization | Require nonblank organization input and resolve it exactly once before preparing the Item Validation Organization parameter value. | The Item Validation Organization parameter is changed. | resolve_inventory_organization |
| QP_COVERAGE_START_DATE | Require a nonblank coverage-item start-date value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_COVERAGE_START_DATE. | resolve_coverage_start_date_lookup_code |
| QP_FROM_EMAIL | Require a syntactically valid email address: exactly one @ sign, nonblank local and domain parts, no whitespace, and a domain containing at least one dot. Reject the parameter value before preparing the archive when any check fails. | The resolved parameter code is QP_FROM_EMAIL. | |
| QP_RETRY_PAUSE | Require a whole number from 1 through 50 inclusive. Reject decimals, nonnumeric text, and values outside the range before preparing the archive. | The resolved parameter code is QP_RETRY_PAUSE. | |
| QP_SELLING_PROFIT_CENTER_BU | Require a nonblank selling-profit-center business-unit value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_SELLING_PROFIT_CENTER_BU. | resolve_selling_profit_center_business_unit_lookup_code |
| YES_NO parameter codes | Require a nonblank value and resolve it exactly once for QP_ACTIVATE_CREDIT_CHK_SUBMIT, QP_CHANGE_PROCESS_MODE, QP_USE_ALG_TO_CALCULATE_TOTALS, QP_ORIG_PRJ_VALUE_REF_RTN, QP_EXTERNALLY_FUSION_PRICED, QP_PROCESS_INVENTORY_TRX, QP_INVENTORY_TRX_ORDER, QP_HALT_CONFIG_VAL, QP_SALES_AGREEMENT_DEFAULT, QP_FILTER_SHIP_TO_ADDRESS, QP_CANCEL_B2B_SUPPLY, QP_UI_ENABLE_SAVE_OFFLINE, QP_VALIDATE_LOTS_SERIALS, QP_ENABLE_COMPLIANCE_SCREENING, QP_SEND_DISCOUNTS_TO_BILLING, QP_START_ORD_APPROVALS, QP_KEEP_OVERRIDE_SCH, or QP_ALLOW_CHANGES_THRO_CON before preparing the parameter value. | The resolved parameter code is one of the listed YES_NO parameter codes. | resolve_yes_no_lookup_code |
| QP_QTY_INVOICE_OVERSHIP | Require a nonblank parameter value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_QTY_INVOICE_OVERSHIP. | resolve_qty_invoice_overship_lookup_code |
| QP_SHIP_TOLERANCE_SOURCE | Require a nonblank parameter value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_SHIP_TOLERANCE_SOURCE. | resolve_ship_tolerance_source_lookup_code |
| QP_INVENTORY_TRX_DATE | Require a nonblank parameter value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_INVENTORY_TRX_DATE. | resolve_inventory_transaction_date_lookup_code |
| QP_CUSTOMER_REL_TYPE | Require a nonblank parameter value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_CUSTOMER_REL_TYPE. | resolve_customer_relationship_type_lookup_code |
| QP_PREPARER_FOR_PROC | Require a nonblank preparer name and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_PREPARER_FOR_PROC. | resolve_preparer_worker |
| QP_DEFAULT_TAX_DETERMINANTS | Require a nonblank parameter value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_DEFAULT_TAX_DETERMINANTS. | resolve_default_tax_determinants_lookup_code |
| QP_CASCAD_HDR_ATTR_TO_LNE | Require a nonblank parameter value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_CASCAD_HDR_ATTR_TO_LNE. | resolve_cascade_header_attributes_to_line_lookup_code |
| QP_PRICING_IN_CONFIGURATOR | Require a nonblank parameter value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_PRICING_IN_CONFIGURATOR. | resolve_pricing_in_configurator_lookup_code |
| QP_INCL_ITEM_EXPLOSION_DATE | Require a nonblank parameter value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_INCL_ITEM_EXPLOSION_DATE. | resolve_include_item_explosion_date_lookup_code |
| QP_CREDIT_CK_FAILURE_AT_SUBMIT | Require a nonblank parameter value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_CREDIT_CK_FAILURE_AT_SUBMIT. | resolve_credit_check_failure_at_submit_lookup_code |
| QP_DUOM_RETURN_QTY_TYPE | Require a nonblank parameter value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_DUOM_RETURN_QTY_TYPE. | resolve_duom_return_quantity_type_lookup_code |
| QP_AUTH_CC_AMT | Require a nonblank parameter value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_AUTH_CC_AMT. | resolve_authorize_credit_card_amount_lookup_code |
| QP_CONFIG_EFFECTIVE_DATE | Require a nonblank parameter value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_CONFIG_EFFECTIVE_DATE. | resolve_config_effective_date_lookup_code |
| QP_RELATIONSHIP_SHIP_TO_CUST | Require a nonblank parameter value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_RELATIONSHIP_SHIP_TO_CUST. | resolve_relationship_ship_to_customer_lookup_code |
| QP_ITEM_DETAILS_IN_OFFERS | Require a nonblank parameter value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_ITEM_DETAILS_IN_OFFERS. | resolve_item_details_in_offers_lookup_code |
| QP_CONFIG_EFF_CASCADE | Require a nonblank parameter value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_CONFIG_EFF_CASCADE. | resolve_config_effective_cascade_lookup_code |
| QP_VALIDATE_TRX_SIGN_AMT | Require a nonblank parameter value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_VALIDATE_TRX_SIGN_AMT. | resolve_validate_transaction_sign_amount_lookup_code |
| QP_PROCESS_DS_TOLERANCE | Require a nonblank parameter value and resolve it exactly once before preparing the parameter value. | The resolved parameter code is QP_PROCESS_DS_TOLERANCE. | resolve_process_drop_ship_tolerance_lookup_code |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ORDER_MANAGEMENT_PARAMETERS.VALIDATE_INPUT | step | 10 | validate_input | valid->ORDER_MANAGEMENT_PARAMETERS.RESOLVE_PARAMETER;invalid-or-incomplete->RETURN_ISSUES | none | stop | Before preparing a parameter change. |

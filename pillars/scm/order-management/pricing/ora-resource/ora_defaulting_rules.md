# Manage Pricing Bases Defaulting Rules

Source: Oracle Fusion Cloud SCM REST API, Get all pricing bases (26B).

## Standard Defaults

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | BasisUsageCode | ADJUSTMENT | Creating or importing a pricing basis and Usage is omitted | No | |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | AppliesToCode | PRICE | Creating a charge definition and Applies To is omitted | No | |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | PricePeriodicityUOMClass | Current Site value of `RCS_DEFAULT_UOM_CLASS_CODE_FOR_SVC_DURATION` | Creating a recurring charge definition when the user omits the periodicity UOM class and the profile option resolves to a nonblank value | No | resolve_recurring_frequency_uom_class |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | UsageUOMClass | Sole eligible Usage UOM Class | Creating a usage charge definition when the user omits the Usage UOM Class and exactly one eligible value resolves | No | resolve_single_usage_uom_class |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | TaxChargeTypeCode | Matching enabled ZX_CHARGE_TYPE code; null is permitted | Creating or updating a charge definition when the user omits Tax Charge Type | No | resolve_tax_charge_type |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | RefundableFlag | false | Creating a charge definition and Refundable is omitted | No | |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | SetupEnabledFlag | true | Creating a charge definition and Setup Enabled is omitted | No | |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | ActiveFlag | true | Creating a charge definition and Active is omitted | No | |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | CalculateMarginFlag | true | Creating a charge definition and Calculate Margin is omitted | No | |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | AssignmentTypeCode | ORA_QP_ALL | Creating or updating a customer pricing definition and AssignmentTypeCode is omitted | No | |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | Name | Customer Pricing Definition for Validation | Creating or updating a customer pricing definition when Name is omitted and the resulting AssignmentTypeCode is ORA_QP_ALL | No | |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | pricingStrategies.<child>.AssociationStartDate | Current date and time at default application, formatted as YYYY-MM-DDTHH:MI:SS.sss+hh:mm | Associating any child under a pricing strategy and AssociationStartDate is omitted | No | |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| ORA_QP_MANAGE_PRICING_BASES | Manage Pricing Bases | QP.PB.DEFAULT | decision | 2 | apply_default | applied->QP.PB.PRICE_ELEMENT_LOOKUP;not_applicable->QP.PB.PRICE_ELEMENT_LOOKUP;failed->QP.PB.ISSUES | QP.PB.VALIDATE | stop | Creating or importing a pricing basis |
| ORA_QP_MANAGE_PRICING_CHARGE_DEFINITIONS | Manage Pricing Charge Definitions | QP.PCD.DEFAULT | decision | 3 | apply_default | applied->QP.PCD.DESIGN;not_applicable->QP.PCD.DESIGN;failed->QP.PCD.ISSUES | QP.PCD.DEPENDENCY | stop | Creating or updating a pricing charge definition |
| CUSTOM_CUSTOMER_PRICING_DEFINITIONS | Manage Customer Pricing Definitions | CPD.APPLY_DEFAULTS | decision | 3 | apply_default | applied->CPD.CHECK_GLOBAL_ASSIGNMENT;not_applicable->CPD.CHECK_GLOBAL_ASSIGNMENT;failed->CPD.ISSUES | CPD.VALIDATE | stop | Creating or updating a customer pricing definition; default AssignmentTypeCode to ORA_QP_ALL and Name to Customer Pricing Definition for Validation when omitted for a global definition, and default child AssociationStartDate in Fusion ISO timestamp format when applicable |

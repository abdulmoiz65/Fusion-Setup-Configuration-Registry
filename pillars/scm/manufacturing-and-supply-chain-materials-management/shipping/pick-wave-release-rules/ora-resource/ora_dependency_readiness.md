# Pick Wave Release Rules Dependency Readiness

Source: Redwood Pick Wave Release Rules dynamic layout.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Processing-option combinations | Normalize the checkbox flags before evaluating dependent controls. |
| 2 | Approved display-value lookups | Resolve any supplied Release Status, Destination Type, Order Type, or Shipment Priority display value to its backend code before evaluating dependent controls. |
| 3 | Shipment options | Evaluate the UI-only flag dependencies before preview. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PWR.AUTO_CONFIRM_AUTO_SHIP | Auto Confirm Picks and Automatically Ship on Pick Confirmation | Conditional | Either flag is selected | Blocked when both are Y; Satisfied otherwise | Supplied normalized flag values | | The Redwood UI disables either option when the other is selected. | Select at most one of Auto Confirm Picks and Automatically Ship on Pick Confirmation. | AutoPickConfirmFlag; AutoShipOnPickConfirmFlag |
| PWR.CREATE_SHIPMENTS | Shipment creation options | Conditional | CreateShipmentsFlag is not Y | Blocked when ShipmentCreationCriteriaCode, AppendShipmentsFlag, or AutomaticallyPackFlag is supplied; Satisfied otherwise | Supplied normalized flag values and shipment-option values | | The Redwood UI disables shipment-creation options until Create Shipments is selected. | Select Create Shipments before supplying shipment-creation criteria, append shipments, or automatically pack. | CreateShipmentsFlag; ShipmentCreationCriteriaCode; AppendShipmentsFlag; AutomaticallyPackFlag |
| PWR.AUTO_SHIP_OPTIONS | Automatic ship options | Conditional | AutomaticallyPackFlag or ShipConfirmRuleId is supplied | Blocked when the documented UI condition is not met; Satisfied otherwise | Supplied normalized flag values and TradeComplianceMethod | | Automatically Pack requires Create Shipments and Automatically Ship on Pick Confirmation. Ship Confirm Rule is enabled only for the UI-supported processing combination. | For Automatically Pack, select Create Shipments and Automatically Ship on Pick Confirmation. For Ship Confirm Rule, use the supported combination and Trade Compliance Method NONE. | CreateShipmentsFlag; AutoShipOnPickConfirmFlag; AutomaticallyPackFlag; AutoPickConfirmFlag; TradeComplianceMethod; ShipConfirmRuleId |
| PWR.RELEASE_STATUS_CODE | Release Status display value | Conditional | ReleaseStatus is supplied | Lookup | Supplied ReleaseStatus and optional ReleaseStatusCode | resolve_release_status_code | The Redwood radio group displays Meaning and stores LookupCode. | Provide an exact Release Status display value or matching ReleaseStatusCode. | ReleaseStatusCode: LookupCode |
| PWR.DESTINATION_TYPE_CODE | Destination Type display value | Conditional | DestinationType is supplied | Lookup | Supplied DestinationType and optional DestinationTypeCode | resolve_destination_type_code | The Redwood selector displays Meaning and stores LookupCode. | Provide an exact Destination Type display value or matching DestinationTypeCode. | DestinationTypeCode: LookupCode |
| PWR.ORDER_TYPE_CODE | Order Type display value | Conditional | OrderType is supplied | Lookup | Supplied OrderType and optional OrderTypeCode | resolve_order_type_code | The Redwood selector displays Meaning and stores one of the supported LookupCode values. | Provide an exact UI-supported Order Type display value or matching OrderTypeCode. | OrderTypeCode: LookupCode |
| PWR.SHIPMENT_PRIORITY_CODE | Shipment Priority display value | Conditional | ShipmentPriority is supplied | Lookup | Supplied ShipmentPriority and optional ShipmentPriorityCode | resolve_shipment_priority_code | The Redwood selector displays Meaning and stores LookupCode. | Provide an exact Shipment Priority display value or matching ShipmentPriorityCode. | ShipmentPriorityCode: LookupCode |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Blocked | A UI-only flag dependency is violated | No; correct the supplied values. |
| Satisfied | The applicable UI-only flag dependency is met | No lookup required. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PWR.VALIDATE_DEPENDENCIES | decision | 60 | resolve_dependency | ready->PWR.DONE;blocked->RETURN_ISSUES;failed->RETURN_ISSUES | PWR.RESOLVE_SHIPMENT_PRIORITY | stop | Processing options are supplied |

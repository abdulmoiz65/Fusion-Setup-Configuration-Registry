# Ship Confirm Rules Dependency Readiness

Source: Ship Confirm Rules Redwood page and dynamic layout.

## Dependency Rules

| Dependency | Mandatory | Applies When | Status When Input Present | Status When Missing | Resolver | Values to Fill | User Guidance |
|---|---|---|---|---|---|---|---|
| Backend value for ship quantity option | Conditional | ShipWith is S and ShipQuantityNotSpecifiedOption is supplied as a display value | Lookup | Blocked | resolve_ship_quantity_not_specified_option_code | ShipQuantityNotSpecifiedOption: LookupCode | Provide an exact Ship Quantity display value or backend code. |
| Backend value for packing slip status | Conditional | PackingSlipStatus is supplied as a display value | Lookup | Blocked | resolve_packing_slip_status_code | PackingSlipStatus: LookupCode | Provide an exact Packing Slip Status display value or backend code. |
| Backend value for ship method | Conditional | ShipMethodCode is supplied as a display value | Satisfied when the backend code is supplied | Blocked | | ShipMethodCode | Provide the backend code until a complete approved resolver contract is available. |
| Backend value for shipping document job set | Conditional | JobSetName is supplied as a display value | Lookup | Blocked | resolve_shipping_document_job_set_name | JobSetName: JobSetName | Provide an exact Shipping Document Job Set display value or backend value. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SCR.VALIDATE_DEPENDENCIES | decision | 60 | resolve_dependency | ready->SCR.DONE;blocked->RETURN_ISSUES;failed->RETURN_ISSUES | SCR.RESOLVE_SHIPPING_DOCUMENT_JOB_SET | stop | Creating or updating a Ship Confirm Rule |

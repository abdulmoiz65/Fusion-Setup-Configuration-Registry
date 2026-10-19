# Ship Confirm Rules Reference Lookups

Source: Ship Confirm Rules Redwood page and dynamic layout.

## Lookup Readiness

| UI Field | VBC Service Alias | Complete Fusion REST Path or URL | Status | Required Input Until Verified |
|---|---|---|---|---|
| Ship Quantity | oracle_scm_shippingsetupUI:standardLookupsLOV/getall_standardLookupsLOV | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='WSH_SCR_SHIP_UNSPEC_QTY'&fields=Meaning,LookupCode,LookupType&onlyData=true | Approved resolver contract | Exact display value or backend code |
| Packing Slip Status | oracle_scm_shippingsetupUI:standardLookupsLOV/getall_standardLookupsLOV | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='ORA_WSH_PACK_STATUS'&fields=Meaning,LookupCode,LookupType&onlyData=true | Approved resolver contract | Exact display value or backend code |
| Ship Method | oracle_scm_shippingsetupUI:shippingShipMethodsLOV/getall_shippingShipMethodsLOV | TBD | No resolver contract is authorized | ShipMethodCode backend code |
| Shipping Document Job Set | oracle_scm_shippingsetupUI:shippingDocumentJobSetsLOV/getall_shippingDocumentJobSetsLOV | /fscmRestApi/resources/11.13.18.05/shippingDocumentJobSetsLOV?finder=findByProductCode;bindProductCode=WSH&fields=JobSetName,JobSetDisplayName,ProductCode&onlyData=true | Approved resolver contract | Exact display value or backend value |

Do not call a VBC service alias directly. Add a resolver only after its complete read-only Fusion REST path or URL, requested fields, display-to-backend mapping, context dependency, and exact-match contract are verified and approved.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_ship_with_code | A ShipWith display value is supplied and the code is blank, or both values are supplied for reconciliation | ShipWith display value | /fscmRestApi/resources/11.13.18.05/shipConfirmRules?fields=ShipWith,ShipWithMeaning&onlyData=true | ShipWith, ShipWithMeaning | Trim and case-insensitive exact match on ShipWithMeaning. Deduplicate identical ShipWithMeaning and ShipWith pairs, then require exactly one distinct pair. When both display value and code are supplied, require the code to equal the returned ShipWith. | ShipWith: ShipWith | Zero matches, differing codes for one display value, or a supplied conflicting code blocks preview. Do not fuzzy-match or select the first record. |
| resolve_ship_quantity_not_specified_option_code | ShipWith is S and a ShipQuantityNotSpecifiedOption display value is supplied and the code is blank, or both values are supplied for reconciliation | ShipQuantityNotSpecifiedOption display value | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='WSH_SCR_SHIP_UNSPEC_QTY'&fields=Meaning,LookupCode,LookupType&onlyData=true | Meaning, LookupCode, LookupType | Trim and case-insensitive exact match on Meaning. Require exactly one returned row. When both display value and code are supplied, require the code to equal the returned LookupCode. | ShipQuantityNotSpecifiedOption: LookupCode | Zero or multiple matches, a value used when ShipWith is A, or a supplied conflicting code blocks preview. Do not fuzzy-match or select the first record. |
| resolve_packing_slip_status_code | A PackingSlipStatus display value is supplied and the code is blank, or both values are supplied for reconciliation | PackingSlipStatus display value | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='ORA_WSH_PACK_STATUS'&fields=Meaning,LookupCode,LookupType&onlyData=true | Meaning, LookupCode, LookupType | Trim and case-insensitive exact match on Meaning. Require exactly one returned row. When both display value and code are supplied, require the code to equal the returned LookupCode. | PackingSlipStatus: LookupCode | Zero or multiple matches, or a supplied conflicting code blocks preview. Do not fuzzy-match or select the first record. |
| resolve_shipping_document_job_set_name | A JobSetName display value is supplied and the backend value is blank, or both values are supplied for reconciliation | JobSetName display value | /fscmRestApi/resources/11.13.18.05/shippingDocumentJobSetsLOV?finder=findByProductCode;bindProductCode=WSH&fields=JobSetName,JobSetDisplayName,ProductCode&onlyData=true | JobSetName, JobSetDisplayName, ProductCode | Trim and case-insensitive exact match on JobSetDisplayName, scoped to ProductCode WSH. Require exactly one returned row. When both display value and backend value are supplied, require the value to equal the returned JobSetName. | JobSetName: JobSetName | Zero or multiple matches, or a supplied conflicting backend value blocks preview. Do not fuzzy-match or select the first record. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SCR.RESOLVE_SHIP_WITH | step | 20 | reference_lookup | resolved->SCR.RESOLVE_SHIP_QUANTITY;not-applicable->SCR.RESOLVE_SHIP_QUANTITY;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | SCR.VALIDATE_INPUT | stop | A ShipWith display value or code is supplied |
| SCR.RESOLVE_SHIP_QUANTITY | step | 30 | reference_lookup | resolved->SCR.RESOLVE_PACKING_SLIP_STATUS;not-applicable->SCR.RESOLVE_PACKING_SLIP_STATUS;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | SCR.RESOLVE_SHIP_WITH | stop | ShipWith is S and a Ship Quantity display value or code is supplied |
| SCR.RESOLVE_PACKING_SLIP_STATUS | step | 40 | reference_lookup | resolved->SCR.RESOLVE_SHIPPING_DOCUMENT_JOB_SET;not-applicable->SCR.RESOLVE_SHIPPING_DOCUMENT_JOB_SET;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | SCR.RESOLVE_SHIP_QUANTITY | stop | A Packing Slip Status display value or code is supplied |
| SCR.RESOLVE_SHIPPING_DOCUMENT_JOB_SET | step | 50 | reference_lookup | resolved->SCR.VALIDATE_DEPENDENCIES;not-applicable->SCR.VALIDATE_DEPENDENCIES;blocked->RETURN_ISSUES;failure->RETURN_ISSUES | SCR.RESOLVE_PACKING_SLIP_STATUS | stop | A Shipping Document Job Set display value or backend value is supplied |

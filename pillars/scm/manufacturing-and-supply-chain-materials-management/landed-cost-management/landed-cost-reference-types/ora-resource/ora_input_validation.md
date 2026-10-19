# Landed Cost Reference Types Input Validation

Source: Oracle, [Manage Landed Cost Reference Types](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/manage-landed-cost-reference-types.html) (26C); user-supplied Data Loader sample and lookup contracts.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Reference type identity | Business reference type code and name | Stop before Data Loader preparation | Ask the business user for the code and name | A reference type create is requested | |
| Existing reference type identity | ChargeReferenceTypeId, Code, or Name | Stop before Data Loader preparation | Ask for ChargeReferenceTypeId, Code, or Name; resolve a supplied Code or Name through resolve_landed_cost_reference_type_id | A reference type update or delete is requested | resolve_landed_cost_reference_type_id |
| Reference data set | SetId, or SetCode or SetName that resolves to one SetId | Stop before Data Loader preparation | Ask for SetId, SetCode, or SetName; resolve a supplied SetCode or SetName through resolve_costing_set_for_charge_reference_type | A reference type create is requested | resolve_costing_set_for_charge_reference_type |
| Reference data type | DataType code, or DataType meaning that resolves to one DataType code | Stop before Data Loader preparation | Ask for a DataType code or meaning; resolve a supplied meaning through resolve_charge_reference_data_type | A reference type create is requested | resolve_charge_reference_data_type |
| Reference type availability | InactiveFlag, Active or inactive status | Default to false | When no value is supplied, set InactiveFlag to false and prepare the stored value N | A reference type create is requested | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Functional input format | Accept business-user prose, a form, or a spreadsheet row. Do not require JSON or implementation attribute names from the business user. Map confirmed values through core.data-loader to SetId, Code, Name, Description, DataType, and InactiveFlag. | Before preparing a Data Loader request | |
| Reference data set | Use SetId when supplied. When SetId is absent, resolve exactly one SetId from the supplied SetCode or SetName through resolve_costing_set_for_charge_reference_type. | Before preparing a Data Loader request | resolve_costing_set_for_charge_reference_type |
| Reference data type | Use the supplied DataType code. When a business DataType meaning is supplied instead, resolve exactly one DataType code through resolve_charge_reference_data_type. | Before preparing a Data Loader request | resolve_charge_reference_data_type |
| Existing reference type identity | Use ChargeReferenceTypeId when supplied. When it is absent, resolve exactly one ChargeReferenceTypeId from the supplied Code or Name through resolve_landed_cost_reference_type_id. | Before preparing a Data Loader update or delete request | resolve_landed_cost_reference_type_id |
| Reference type availability | InactiveFlag is mandatory in the Data Loader source. Accept a supplied boolean or stated active or inactive status. If neither is supplied, default InactiveFlag to false. Convert true to the literal stored value Y and false to the literal stored value N before generating the Data Loader source; never send Boolean True or False as the field value. | Before preparing a Data Loader request | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LANDED_COST_REFERENCE_TYPES.VALIDATE_INPUT | step | 10 | validate_input | create-request->LANDED_COST_REFERENCE_TYPES.DEFAULT_INACTIVE_FLAG;update-request->LANDED_COST_REFERENCE_TYPES.RESOLVE_REFERENCE_TYPE_ID;delete-request->LANDED_COST_REFERENCE_TYPES.RESOLVE_REFERENCE_TYPE_ID;invalid->RETURN_ISSUES | none | stop | Before preparing a Landed Cost Reference Types Data Loader request from functional business input. |

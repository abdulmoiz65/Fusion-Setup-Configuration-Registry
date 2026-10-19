# Landed Cost Reference Types Dependency Readiness

Source: Oracle, [Manage Landed Cost Reference Types](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/manage-landed-cost-reference-types.html) (26C); and the user-supplied Data Loader and lookup contracts.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Inactive flag default and conversion | Default an omitted InactiveFlag to false, then convert true to Y and false to N. |
| 2 | Reference data set resolution | Use SetId when supplied; otherwise resolve SetId from exactly one supplied SetCode or SetName. |
| 3 | Reference data type resolution | Use DataType when supplied; otherwise resolve DataType from exactly one supplied DataType meaning. |
| 4 | Existing reference type resolution | For an update or delete, use ChargeReferenceTypeId when supplied; otherwise resolve it from exactly one supplied Code or Name. |
| 5 | Data Loader execution contract | Use core.data-loader with the registered landedCostReferenceTypes top business object and validate the source fields against its generated sample. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| landed_cost_reference_types_set_id | SetId for the reference data set | Yes | A reference type create is requested | Lookup | User-supplied SetCode or SetName when SetId is absent | resolve_costing_set_for_charge_reference_type | Data Loader requires SetId when creating the reference type. | Provide SetId, or provide one SetCode or SetName that uniquely identifies a costing set. | SetId from the unique SetCode or SetName match |
| landed_cost_reference_types_data_type | DataType code | Yes | A reference type create is requested | Lookup | User-supplied DataType meaning when DataType code is absent | resolve_charge_reference_data_type | Data Loader requires the DataType code. | Provide the DataType code, or provide one data-type meaning that uniquely identifies it. | DataType from the unique Meaning match |
| landed_cost_reference_types_existing_identity | ChargeReferenceTypeId for an existing reference type | Yes | A reference type update or delete is requested | Lookup | User-supplied Code or Name when ChargeReferenceTypeId is absent | resolve_landed_cost_reference_type_id | The existing reference type must be identified before its Data Loader update or delete is prepared. | Provide ChargeReferenceTypeId, or provide one Code or Name that uniquely identifies the reference type. | ChargeReferenceTypeId from the unique Code or Name match |
| landed_cost_reference_types_data_loader_contract | Registered landedCostReferenceTypes Data Loader contract | Yes | A reference type create, update, or delete is requested | Satisfied | Task metadata and the generated core.data-loader sample | | Landed Cost Reference Types must be loaded only through core.data-loader using landedCostReferenceTypes. | Generate and validate the Data Loader sample before preparing the immutable import artifact. Do not use a direct REST route. | Top business object: landedCostReferenceTypes; create fields: InactiveFlag, SetId, Code, Name, Description, DataType; update or delete identity: ChargeReferenceTypeId derived from a unique Code or Name match when not supplied; delete uses the generated Data Loader DELETE operation. InactiveFlag is mandatory for a create and must contain literal Y or N, with false to N and true to Y |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Blocked | The registered Data Loader contract is unavailable or the source data does not conform to the generated sample | No |
| Lookup mismatch | A SetCode, SetName, DataType meaning, Code, or Name returns zero or multiple exact matches | No |
| Satisfied | The registered Data Loader contract has been reviewed and the requested reference type data conforms to it | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LANDED_COST_REFERENCE_TYPES.CHECK_EXECUTION_CONTRACT | step | 40 | resolve_dependency | contract-ready->LANDED_COST_REFERENCE_TYPES.ENFORCE_DATA_LOADER_ROUTE;contract-missing->RETURN_ISSUES | none | stop | After the applicable create, update, or delete identity-resolution path and before preparing a Landed Cost Reference Types Data Loader request. |

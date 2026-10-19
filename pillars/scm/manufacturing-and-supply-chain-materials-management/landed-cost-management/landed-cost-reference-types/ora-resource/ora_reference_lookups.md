# Landed Cost Reference Types Reference Lookups

Source: User-supplied read-only lookup contracts. Both requests use the REST-Framework-Version header with value 9.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_costing_set_for_charge_reference_type | SetId is absent and the user provides SetCode or SetName | SetCode or SetName | /fscmRestApi/resources/11.13.18.05/costingSetsLOV?finder=IntentFinder;Intent=CML_MANAGE_CHARGE_REFERENCE_TYPE_DATA&q=SetCode='<SetCode>' or SetName='<SetName>'; Header: REST-Framework-Version: 9 | SetId; SetCode; SetName | Require exactly one returned record whose SetCode or SetName exactly equals the user-provided value | SetId from the unique SetCode or SetName match | No match: stop and report that the costing set was not found. Many matches: stop and report the costing-set lookup is ambiguous; do not select a record. |
| resolve_charge_reference_data_type | DataType code is absent and the user provides a DataType meaning | DataType meaning | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType in 'CML_CHARGE_REF_DATATYPES' and Meaning='<Meaning>'; Header: REST-Framework-Version: 9 | LookupCode; Meaning | Require exactly one returned record whose Meaning exactly equals the user-provided DataType meaning within LookupType CML_CHARGE_REF_DATATYPES | DataType from the unique LookupCode match | No match: stop and report that the DataType meaning was not found. Many matches: stop and report the DataType lookup is ambiguous; do not select a record. |
| resolve_landed_cost_reference_type_id | ChargeReferenceTypeId is absent and an existing reference type is identified by Code or Name | Code or Name | /fscmRestApi/resources/11.13.18.05/landedCostReferenceTypes?q=Code='<Code>' or /fscmRestApi/resources/11.13.18.05/landedCostReferenceTypes?q=Name='<Name>'; Header: REST-Framework-Version: 9 | ChargeReferenceTypeId; Code; Name | Use only the supplied predicate and require exactly one returned record whose Code or Name exactly equals the user-provided value | ChargeReferenceTypeId from the unique Code or Name match | No match: stop and report that the reference type was not found. Many matches: stop and report the reference-type lookup is ambiguous; do not select a record. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| SetId is supplied | Do not call the costing-set lookup; continue to DataType resolution. |
| SetId is absent and exactly one SetCode or SetName lookup match is returned | Use the returned SetId only to prepare the Data Loader request; keep core.data-loader as the only Fusion load executor. |
| DataType code is supplied | Do not call the data-type lookup; continue to the Data Loader execution-contract check. |
| DataType code is absent and exactly one DataType meaning lookup match is returned | Use the returned LookupCode as DataType only to prepare the Data Loader request; keep core.data-loader as the only Fusion load executor. |
| ChargeReferenceTypeId is supplied for an existing reference type | Do not call the existing-reference-type lookup; retain the supplied identifier for the Data Loader update or delete workflow. |
| ChargeReferenceTypeId is absent and exactly one Code or Name lookup match is returned | Use the returned ChargeReferenceTypeId only to identify the existing reference type for the Data Loader update or delete workflow; keep core.data-loader as the only Fusion load executor. |
| Either lookup has no exact match or more than one match | Stop before preview, preserve sanitized lookup evidence, and request a corrected identifier or meaning. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LANDED_COST_REFERENCE_TYPES.RESOLVE_SET_ID | decision | 20 | reference_lookup | resolved->LANDED_COST_REFERENCE_TYPES.RESOLVE_DATA_TYPE;not-required->LANDED_COST_REFERENCE_TYPES.RESOLVE_DATA_TYPE;unresolved->RETURN_ISSUES | LANDED_COST_REFERENCE_TYPES.DEFAULT_INACTIVE_FLAG | stop | SetId is absent and a SetCode or SetName is provided. |
| LANDED_COST_REFERENCE_TYPES.RESOLVE_REFERENCE_TYPE_ID | decision | 25 | reference_lookup | resolved->LANDED_COST_REFERENCE_TYPES.CHECK_EXECUTION_CONTRACT;not-required->LANDED_COST_REFERENCE_TYPES.CHECK_EXECUTION_CONTRACT;unresolved->RETURN_ISSUES | LANDED_COST_REFERENCE_TYPES.VALIDATE_INPUT | stop | An update or delete is requested and ChargeReferenceTypeId is absent while Code or Name is provided. |
| LANDED_COST_REFERENCE_TYPES.RESOLVE_DATA_TYPE | decision | 30 | reference_lookup | resolved->LANDED_COST_REFERENCE_TYPES.CHECK_EXECUTION_CONTRACT;not-required->LANDED_COST_REFERENCE_TYPES.CHECK_EXECUTION_CONTRACT;unresolved->RETURN_ISSUES | LANDED_COST_REFERENCE_TYPES.RESOLVE_SET_ID | stop | DataType code is absent and a DataType meaning is provided. |

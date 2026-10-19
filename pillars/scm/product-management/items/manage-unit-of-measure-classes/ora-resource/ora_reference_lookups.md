# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_uom_class_by_exact_code | A UOM class creation is requested after local validation | ClassCode | /fscmRestApi/resources/11.13.18.05/unitOfMeasureClasses?finder=ClassCodeFinder;ClassCode={ClassCode}&fields=ClassCode,ClassId,ClassName,ClassDescription,BaseUnitOfMeasure,BaseUOMCode&onlyData=true | ClassCode, ClassId, ClassName, ClassDescription, BaseUnitOfMeasure, BaseUOMCode | Use the documented ClassCodeFinder with the exact requested ClassCode. | Existing class identity and base-UOM attributes | No match permits design enforcement to consider creation. One match is an existing class. More than one match is ambiguous and blocks preview. |

## Source

Oracle public REST documentation: https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/fasrp/op-unitofmeasureclasses-get.html

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UMC.FIND_EXISTING | decision | 3 | reference_lookup | not_found->UMC.ENFORCE;found->UMC.ENFORCE;ambiguous->UMC.HANDLE_ISSUE;failed->UMC.HANDLE_ISSUE | UMC.ASSESS_CLASS_SEMANTICS | stop | Creation after semantic class-role assessment |

# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_units_of_measure_by_class | Operation is Create or Update and one or more validated request rows share the same exact UOMClass | Request Row ID, Operation, UOMClass | /fscmRestApi/resources/11.13.18.05/unitsOfMeasure?finder=UomFinder;UOMClass={UOMClass}&fields=UOMCode,UOMClass,BaseUnitFlag,StandardConversion,BaseUOMCode;intraclassConversions:IntraclassConversion,InverseConversionFlag&onlyData=true | UOMCode, UOMClass, BaseUnitFlag, StandardConversion, BaseUOMCode, intraclassConversions:IntraclassConversion, InverseConversionFlag | Group Create and Update rows by exact UOMClass; issue one request per distinct class and apply the result to every Request Row ID in that group | Existing class units, conversion facts, affected Request Row IDs | Create with no match: classify that class group as new. Update with no match: stop because the class must already exist. Many matches: evaluate the complete class group. Failure: stop only the affected class group. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Child conversion data is needed | Use the documented child-field projection in the request. Do not add expand because Oracle documents that fields and expand cannot be combined. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UOM.LOOKUP-CLASS | decision | 20 | reference_lookup | class_found->UOM.ENFORCE-CONVERSION-DESIGN;class_not_found->UOM.DONE-NEW-CLASS;lookup_failed->UOM.HANDLE-LOOKUP-ERROR | UOM.VALIDATE-INPUT | stop | Operation is Create or Update |

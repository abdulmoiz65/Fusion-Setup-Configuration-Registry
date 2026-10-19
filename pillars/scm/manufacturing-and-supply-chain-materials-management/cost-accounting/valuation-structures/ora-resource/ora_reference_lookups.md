# Reference Lookups

## Source

| Source | Location | Used For |
|---|---|---|
| Developer-provided valuation structure type lookup | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType = 'CST_VALUATION_STRUCTURE_TYPES';Meaning = '&lt;User Specified Valuation Structure Type&gt;' | Resolve the user-supplied Valuation Structure Type to its Oracle type code with an exact query |
| Developer-provided valuation structure mode lookup | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType = 'CST_VALUATION_STRUCTURE_MODES';Meaning = '&lt;User Specified Valuation Structure Mode&gt;' | Resolve the user-supplied Valuation Structure Mode to its Oracle mode code with an exact query |
| Developer-provided Cost Valuation Granularity lookup | /fscmRestApi/resources/11.13.18.05/costingFlexFieldStructuresLOV?q=KeyFlexfieldCode = 'CONS' or 'VALU';Name = '&lt;Supplied Cost Valuation Granularity&gt;' | Resolve the type-dependent Cost Valuation Granularity flexfield structure and instance number |
| Developer-provided valuation structure set lookup | /fscmRestApi/resources/11.13.18.05/costingSetsLOV?q=SetName = '&lt;Set Name&gt;' | Resolve an exact Valuation Structure Set Name to the returned set identifiers |

## Live Lookups

| Resolver | Runs When | Lookup Source Values | Service Path or URL | Query or Match Rule | Fields to Request | Values to Fill | If No Exact Query Match or Multiple Exact Matches |
|---|---|---|---|---|---|---|---|
| resolve_valuation_structure_type | A Valuation Structure Type is supplied for a create or update | User-supplied Valuation Structure Type | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType = 'CST_VALUATION_STRUCTURE_TYPES';Meaning = '&lt;User Specified Valuation Structure Type&gt;' | Query LookupType and Meaning using the exact user-supplied type value. | LookupCode | Valuation Structure Type Code from LookupCode | Block when the exact query returns zero or multiple rows. Do not broaden or partially match the query. |
| resolve_valuation_structure_mode | A Valuation Structure Mode is supplied for a create or update | User-supplied Valuation Structure Mode | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType = 'CST_VALUATION_STRUCTURE_MODES';Meaning = '&lt;User Specified Valuation Structure Mode&gt;' | Query LookupType and Meaning using the exact user-supplied mode value. | LookupCode | Valuation Structure Mode Code from LookupCode | Block when the exact query returns zero or multiple rows. Do not broaden or partially match the query. |
| resolve_cost_valuation_granularity | A Cost Valuation Granularity is supplied after the Valuation Structure Type Code is resolved | Resolved Valuation Structure Type Code, supplied Cost Valuation Granularity | /fscmRestApi/resources/11.13.18.05/costingFlexFieldStructuresLOV?q=KeyFlexfieldCode = 'CONS';Name = '&lt;Supplied Cost Valuation Granularity&gt;' when Type Code is CONSIGNED; otherwise /fscmRestApi/resources/11.13.18.05/costingFlexFieldStructuresLOV?q=KeyFlexfieldCode = 'VALU';Name = '&lt;Supplied Cost Valuation Granularity&gt;' | Use KeyFlexfieldCode CONS when the resolved type code is CONSIGNED; otherwise use VALU. In either case, query the supplied Name exactly. | KeyFlexfieldCode, StructureInstanceNumber, StructureInstanceCode, EnabledFlag, Name | Cost Valuation Granularity Key Flexfield Code from KeyFlexfieldCode; Structure Instance Number from StructureInstanceNumber; FlexFieldStructure from Name; Structure Instance Code from StructureInstanceCode for lookup evidence only; Enabled Flag from EnabledFlag; Cost Valuation Granularity Name from Name | Block when the selected exact query returns zero or multiple rows. Do not broaden or partially match the Name. |
| resolve_valuation_structure_set | A Valuation Structure Set Name is supplied for a create or update | User-supplied Set Name | /fscmRestApi/resources/11.13.18.05/costingSetsLOV?q=SetName = '&lt;Set Name&gt;' | Query SetName using the exact user-supplied set name. | SetId, SetCode, SetName | Valuation Structure Set Id from SetId; Valuation Structure Set Code from SetCode; Valuation Structure Set Name from SetName | Block when the exact query returns zero or multiple rows. Do not broaden or partially match the query. |

## Lookup Execution Rules

| Rule | Requirement |
|---|---|
| Operation scope | These resolvers are read-only and may call only the documented standardLookupsLOV, costingFlexFieldStructuresLOV, and costingSetsLOV lookups. They must not create, update, delete, upload, or initiate setup data. |
| Query literal syntax | In every `q` filter, express string attribute values with single quotes. Shell quoting is separate and must preserve those literals. |
| Environment identity | Join the relative request path to the active, approved Fusion restBaseUrl. Stop if restBaseUrl is absent or the environment selection is not approved. |
| Result handling | Use the LookupCode from the single row returned by the exact type query. Do not broaden the Meaning predicate or infer a type code. |
| Mode result handling | Use the LookupCode from the single row returned by the exact mode query. Do not broaden the Meaning predicate or infer a mode code. |
| Granularity result handling | Select the KeyFlexfieldCode from the resolved type code: CONS for CONSIGNED and VALU otherwise. Use the returned StructureInstanceNumber for StructureInstanceNumber and the returned Name for FlexFieldStructure. Retain StructureInstanceCode as lookup evidence only; do not populate FlexFieldStructure with it. |
| Set result handling | Use SetId, SetCode, and SetName from the single row returned by the exact set-name query. Do not broaden the SetName predicate or infer a set identifier. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VS.RESOLVE_VALUATION_STRUCTURE_TYPE | step | 2 | reference_lookup | resolved->VS.RESOLVE_COST_VALUATION_GRANULARITY;blocked->VS.HANDLE_ISSUE;failure->VS.HANDLE_ISSUE | VS.VALIDATE_INPUT | stop | A Valuation Structure Type is supplied for a Valuation Structure create or update |
| VS.RESOLVE_COST_VALUATION_GRANULARITY | step | 3 | reference_lookup | resolved->VS.RESOLVE_VALUATION_STRUCTURE_MODE;not_applicable->VS.RESOLVE_VALUATION_STRUCTURE_MODE;blocked->VS.HANDLE_ISSUE;failure->VS.HANDLE_ISSUE | VS.RESOLVE_VALUATION_STRUCTURE_TYPE | stop | A Cost Valuation Granularity is supplied for a Valuation Structure create or update |
| VS.RESOLVE_VALUATION_STRUCTURE_MODE | step | 4 | reference_lookup | resolved->VS.RESOLVE_VALUATION_STRUCTURE_SET;not_applicable->VS.RESOLVE_VALUATION_STRUCTURE_SET;blocked->VS.HANDLE_ISSUE;failure->VS.HANDLE_ISSUE | VS.RESOLVE_COST_VALUATION_GRANULARITY | stop | A Valuation Structure Mode is supplied for a Valuation Structure create or update |
| VS.RESOLVE_VALUATION_STRUCTURE_SET | step | 5 | reference_lookup | resolved->VS.DEFAULT_CONSIGNED_MODE;not_applicable->VS.DEFAULT_CONSIGNED_MODE;blocked->VS.HANDLE_ISSUE;failure->VS.HANDLE_ISSUE | VS.RESOLVE_VALUATION_STRUCTURE_MODE | stop | A Valuation Structure Set Name is supplied for a Valuation Structure create or update |

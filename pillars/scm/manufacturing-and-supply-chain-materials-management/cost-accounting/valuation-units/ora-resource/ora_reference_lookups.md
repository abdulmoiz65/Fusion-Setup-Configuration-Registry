# Reference Lookups

## Source

- Oracle Fusion Cloud SCM, Valuation Units, https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/valuation-units.html

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_cost_organization | CostOrganizationId is absent and CostOrganizationName or CostOrganizationCode is supplied | CostOrganizationName or CostOrganizationCode | /fscmRestApi/resources/11.13.18.05/costOrganizationsLOV?q=upper(CostOrganizationName) like upper('%&lt;CostOrganizationName&gt;%') or upper(CostOrganizationCode) like upper('%&lt;CostOrganizationCode&gt;%') | CostOrganizationId, CostOrganizationName, CostOrganizationCode | Use only the supplied name or code predicate and require exactly one returned cost organization | CostOrganizationId | Stop and request a more precise name or code |
| resolve_cost_book | CostBookId is absent after CostOrganizationId is resolved and CostBookCode is supplied | CostOrganizationId, CostBookCode | /fscmRestApi/resources/11.13.18.05/costOrgBooksLOV?finder=findByCostOrganization;bindCostOrgId=&lt;CostOrganizationId&gt;&amp;q=UPPER(CostBookCode) like UPPER('%&lt;CostBookCode&gt;%') | CostBookId, CostBookCode | Require exactly one returned cost book for the bound cost organization | CostBookId | Stop and request a more precise CostBookCode |
| resolve_valuation_structure | ValuationStructureId is absent after CostOrganizationId is resolved and ValuationStructureCode is supplied | CostOrganizationId, ValuationStructureCode | /fscmRestApi/resources/11.13.18.05/costAccountingValuationStructures?finder=searchByCostOrg;bindCostOrgId=&lt;CostOrganizationId&gt;&amp;q=ValStructureModeCode&lt;&gt;'AUTO' AND (UPPER(ValStructureCode) like UPPER('%&lt;ValuationStructureCode&gt;%')) | Full response: ValStructureId, ValStructureCode, ValStructureModeCode, ValStructureSetId, ValStructureSetName | Require exactly one non-Auto valuation structure for the bound cost organization | ValuationStructureId from ValStructureId; SetId from ValStructureSetId; SetName from ValStructureSetName; ValStructureModeCode | Stop and request a more precise ValuationStructureCode |
| resolve_structure_instance_number | A detail is supplied after ValuationStructureId is available | ValuationStructureId | /fscmRestApi/resources/11.13.18.05/costAccountingValuationStructures?q=ValStructureId=&lt;ValuationStructureId&gt; | StructureInstanceNumber | Require exactly one returned nonblank structure instance number | StructureInstanceNumber | Stop before preview |
| validate_valuation_unit_segment_combination | A detail is supplied after StructureInstanceNumber is available | StructureInstanceNumber, SegmentValues | POST /fscmRestApi/resources/11.13.18.05/FlexFndKffApi/action/validateCombination with REST-Framework-Version: 9, Content-Type: application/vnd.oracle.adf.action+json, and the documented body below | Returned value | Treat a returned value as valid; treat no returned value as invalid | Validated SegmentValues and ValuationUnitCombinationId from the returned value | Stop before preview; validation-only action must not create or update data |
| resolve_valuation_unit_master | Adding details, updating, or deleting an existing valuation unit | ValuationUnitCode, CostOrganizationId, CostBookId, ValuationStructureId | /fscmRestApi/resources/11.13.18.05/costAccountingValuationUnits?q=ValuationUnitCode='&lt;ValuationUnitCode&gt;' AND CostOrganizationId=&lt;CostOrganizationId&gt; AND CostBookId=&lt;CostBookId&gt; AND ValuationStructureId=&lt;ValuationStructureId&gt; | ValuationUnitCode, ValuationUnitId, ValuationStructureId, CostOrganizationId, CostBookId | Require exactly one returned master with a nonblank ValuationUnitId in the requested cost-organization, cost-book, and valuation-structure scope | ValuationUnitId | Stop before detail preparation |

## Lookup Execution Rules

The valuation-structure resolver must request the full response, without a
`fields` projection. Map `ValStructureId` to `ValuationStructureId`,
`ValStructureSetId` to `SetId`, and `ValStructureSetName` to `SetName` in the
valuation-unit master and Data Loader source. This derives the reference-data
set context from the selected valuation-structure code; it does not make a
user-supplied set name or set ID a universal valuation-unit input requirement.

| Situation | What Happens |
|---|---|
| CostOrganizationId is supplied | Do not run resolve_cost_organization. |
| CostBookId is supplied | Do not run resolve_cost_book. |
| ValuationStructureId is supplied | Do not run resolve_valuation_structure. |
| A detail is supplied | Run resolve_structure_instance_number, then validate_valuation_unit_segment_combination for each SegmentValues value. |
| Details are added after a master exists | Resolve the master in the requested cost-organization, cost-book, and valuation-structure scope first, then use `/fscmRestApi/resources/11.13.18.05/costAccountingValuationUnits/<ValuationUnitId>/child/costAccountingValuationUnitDetails` only as a read-only parent-child mapping reference. |
| A lookup returns no match or more than one match | Stop before Data Loader source preparation. |

## Detail Combination Validation Action

Use `REST-Framework-Version: 9` for every REST request declared in this
reference, including all GET lookups and the validation action. For the validation
action, also use
`Content-Type: application/vnd.oracle.adf.action+json`. For every supplied
`SegmentValues` value, submit this validation-only request after deriving
`StructureInstanceNumber`:

```json
{
  "consumerId": "oracle.apps.scm.costing.coreSetup.valuationUnits.restModel.view.ValuationUnitDetailsVO#ValUnitKff",
  "structureInstanceNumber": "<StructureInstanceNumber>",
  "combination": "<SegmentValues>"
}
```

`combination` is the supplied `SegmentValues` value. This ADF custom action is
allowed solely to validate the combination; it must not be used to create,
update, or delete setup data. A returned value means the combination is valid.
No returned value means the combination is invalid and blocks Data Loader
preview and upload.

The ADF media type is exclusive to this custom action POST. Identifier and
structure lookups use their documented GET headers, and Data Loader uses its
own standard request headers.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VU.RESOLVE_COST_ORGANIZATION | decision | 2 | reference_lookup | resolved->VU.RESOLVE_COST_BOOK;not_applicable->VU.RESOLVE_COST_BOOK;blocked->VU.HANDLE_ISSUE | VU.VALIDATE_INPUT | stop | CostOrganizationId is absent and a CostOrganizationName or CostOrganizationCode is supplied. |
| VU.RESOLVE_COST_BOOK | decision | 3 | reference_lookup | resolved->VU.RESOLVE_VALUATION_STRUCTURE;not_applicable->VU.RESOLVE_VALUATION_STRUCTURE;blocked->VU.HANDLE_ISSUE | VU.RESOLVE_COST_ORGANIZATION | stop | CostBookId is absent and a CostBookCode is supplied. |
| VU.RESOLVE_VALUATION_STRUCTURE | decision | 4 | reference_lookup | resolved->VU.RESOLVE_STRUCTURE_INSTANCE;not_applicable->VU.RESOLVE_STRUCTURE_INSTANCE;blocked->VU.HANDLE_ISSUE | VU.RESOLVE_COST_BOOK | stop | ValuationStructureId is absent and a ValuationStructureCode is supplied. |
| VU.RESOLVE_STRUCTURE_INSTANCE | decision | 5 | reference_lookup | resolved->VU.VALIDATE_SEGMENT_VALUES;not_applicable->VU.VALIDATE_SEGMENT_VALUES;blocked->VU.HANDLE_ISSUE | VU.RESOLVE_VALUATION_STRUCTURE | stop | A detail is supplied after ValuationStructureId is available. |
| VU.VALIDATE_SEGMENT_VALUES | decision | 6 | reference_lookup | valid->VU.ROUTE_OPERATION;not_applicable->VU.ROUTE_OPERATION;blocked->VU.HANDLE_ISSUE | VU.RESOLVE_STRUCTURE_INSTANCE | stop | One or more detail SegmentValues values are supplied. |
| VU.RESOLVE_VALUATION_UNIT_MASTER | decision | 8 | reference_lookup | resolved_for_details->VU.ENFORCE_EXISTING_MASTER_DETAILS;resolved_for_update->VU.DONE_EXISTING_MASTER_UPDATE;resolved_for_delete->VU.DONE_EXISTING_MASTER_DELETE;blocked->VU.HANDLE_ISSUE | VU.ROUTE_OPERATION | stop | Details are added after a master exists, an existing master is updated, or an existing master is deleted. |

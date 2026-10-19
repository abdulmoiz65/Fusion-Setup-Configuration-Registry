# Input Validation

## Source

- Oracle Fusion Cloud SCM, Valuation Units, https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/valuation-units.html
- Developer-provided master-and-detail payload example for the Data Loader business object.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Create, update, delete, or add details | Stop | Identify the intended Data Loader operation | Always | |
| Valuation unit identity | ValuationUnitCode | Stop | Provide the valuation unit code | Always | |
| Valuation structure | ValuationStructureId or ValuationStructureCode plus CostOrganizationId | Stop | Derive the identifier with resolve_valuation_structure | Creating a valuation unit | resolve_valuation_structure |
| Cost organization | CostOrganizationId, CostOrganizationName, or CostOrganizationCode | Stop | Derive the identifier with resolve_cost_organization | Creating a valuation unit | resolve_cost_organization |
| Cost book | CostBookId or CostBookCode plus CostOrganizationId | Stop | Derive the identifier with resolve_cost_book | Creating a valuation unit | resolve_cost_book |
| Costing attribute values | costAccountingValuationUnitDetails[].SegmentValues | Stop | Provide each segment combination defined by the valuation structure; validate it with validate_valuation_unit_segment_combination | Creating or adding details | validate_valuation_unit_segment_combination |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| ValuationUnitCode is blank | Stop and request the valuation unit code | Always | |
| CostOrganizationId is blank | Resolve it only when CostOrganizationName or CostOrganizationCode is supplied; otherwise stop | Creating a valuation unit | resolve_cost_organization |
| CostBookId is blank | Resolve it only when CostBookCode and CostOrganizationId are supplied; otherwise stop | Creating a valuation unit | resolve_cost_book |
| ValuationStructureId is blank | Resolve it only when ValuationStructureCode and CostOrganizationId are supplied; otherwise stop | Creating a valuation unit | resolve_valuation_structure |
| SetId or SetName is absent after valuation-structure resolution | Stop before Data Loader source preparation and resolve the valuation structure again without a `fields` projection | Creating a valuation unit from ValuationStructureCode | resolve_valuation_structure |
| A manual-create source has no `costAccountingValuationUnitDetails` row | Stop before preview; create a master-and-detail source with at least one validated segment association | Creating a manual valuation unit | validate_valuation_unit_segment_combination |
| A create-with-details source has blank, nonnumeric, mismatched, or reused local surrogate keys | Stop before preview; assign one new numeric master `ValuationUnitId`, repeat it in every child `ValuationUnitId`, and assign a distinct numeric `ValuationUnitDetailId` to each child | Creating a manual valuation unit | |
| SegmentValues is blank | Stop and request the missing costing-attribute value | A detail is supplied | |
| SegmentValues does not represent a valid key-flexfield combination | Stop before preview | Creating or adding details | validate_valuation_unit_segment_combination |

## Operation Routing

| Request Shape | Outcome | What Happens |
|---|---|---|
| A new master and one or more detail rows are supplied | create_with_details | Validate the live Data Loader template linkage using the shared ValuationUnitCode, then enforce the create-with-details design rules. |
| Details are supplied for an existing master | add_details_to_existing_master | Resolve exactly one existing master before enforcing the existing-master detail rules. |
| An existing master is supplied with one or more changed master fields and no details | update_existing_master | Resolve exactly one existing master before enforcing the existing-master update rules. |
| An existing master is supplied for deletion and no details or changed master fields are supplied | delete_existing_master | Resolve exactly one existing master before enforcing the existing-master deletion rules. |
| A master is supplied without details | create_master_only | Enforce the create design rules. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VU.VALIDATE_INPUT | decision | 1 | validate_input | valid->VU.RESOLVE_COST_ORGANIZATION;invalid->VU.HANDLE_ISSUE | none | stop | A Valuation Units Data Loader request is prepared. |
| VU.ROUTE_OPERATION | decision | 7 | evaluate_result | create_with_details->VU.ENFORCE_CREATE_DESIGN;add_details_to_existing_master->VU.RESOLVE_VALUATION_UNIT_MASTER;update_existing_master->VU.RESOLVE_VALUATION_UNIT_MASTER;delete_existing_master->VU.RESOLVE_VALUATION_UNIT_MASTER;create_master_only->VU.ENFORCE_CREATE_DESIGN;invalid->VU.HANDLE_ISSUE | VU.VALIDATE_SEGMENT_VALUES | stop | Identifier and applicable detail validation are complete. |

# Manage Assignment Flexfield Mapping Input Validation

## Purpose

Defines required inputs, dependency-aware checks, and field validation for
Manage Assignment Flexfield Mapping before lookup, preview, or routing.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | list, details, create, edit, or delete | Block | Provide one supported mapping operation | Every request |  |
| Target environment | Connected target environment | Block | Use the authenticated environment context | Every request |  |
| Mapping selector | Source and destination context and segment, or another exact current business selector | Block | Provide sufficient user-visible values to filter or resolve the mapping | details, edit, or delete | read_assignment_flex_mappings |
| Create values | PositionContext, PositionSegment, AssignmentContext, and AssignmentSegment | Block | Provide all four business values | create | resolve_assignment_flex_context_segment |
| Update values | Exact current mapping and at least one changed PositionContext, PositionSegment, AssignmentContext, or AssignmentSegment | Block | Provide one current selector and the requested mapping delta | edit | read_assignment_flex_mappings |
| Delete target | One exact current mapping | Block | Resolve one mapping | delete | read_assignment_flex_mappings |
| Live CUD template | Current raw UCM DAT template for AssignmentFlexfieldsMapping | Block | Fetch the registered template and retain its non-SourceRef columns and section order | create, edit, or delete | fetch_assignment_flex_mapping_loader_template |
| Delete action values | DeleteFlexSegmentMappingIdList equal to the exact current mapping ID | Block | Reuse the fetched ID in the Delete-row field | delete | read_assignment_flex_mappings |
| Legal-employer input | No legal-employer name, identifier, addition, removal, or association delta | Block | Remove the legal-employer input; this task supports only Position Segment to Assignment Segment mappings | Every request |  |
| Child CUD grouping | For each independent create, edit, or delete request, one root AssignmentFlexfieldsMapping row and its matching child action row or rows with a fresh nonblank FlexSegmentMappingGroupKey unique within the DAT source | Block | Create a separate root group for each independent request; repeat that group's key only in its own child rows. Data Loader omits the key from the custom-method payload | create, edit, or delete through a child business object |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Mapping collection is fully paged | Satisfied | Continue with applicable reference resolution | read_assignment_flex_mappings |
| An exact edit or delete selector returns zero or multiple mappings | Invalid | Provide a unique current business selector | read_assignment_flex_mappings |
| Create finds an existing source and destination mapping | Invalid | Stop the duplicate create | read_assignment_flex_mappings |
| A supplied context or segment is zero-match, multiple-match, or has an invalid scope pairing | Invalid | Correct the supplied value | resolve_assignment_flex_context_segment |
| The registered Data Loader business object is unavailable | Unsupported | Restore the registered business object before a mutation |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Read completeness | Page the mapping collection before matching | Every read and mutation precheck | read_assignment_flex_mappings |
| Details matching | Apply every supplied predicate conjunctively; return all matches and a count | list or details | read_assignment_flex_mappings |
| Mutation cardinality | Require exactly one current mapping for edit or delete | edit or delete | read_assignment_flex_mappings |
| Create uniqueness | Require zero existing mappings with the intended source and destination | create | read_assignment_flex_mappings |
| Context and destination preflight | Require both requested segments to be exposed by the current action, reject a context-specific source mapped to a global destination, and require that the destination is not mapped by another current source | create or edit | resolve_assignment_flex_context_segment; read_assignment_flex_mappings |
| Type, precision, and value-set validation | Do not block preflight when the current action does not expose this metadata. Preserve the exact requested values and let the submitted Fusion Data Loader operation validate compatibility | create or edit | Core Data Loader / Fusion |
| Legal-employer exclusion | Reject any legal-employer name, identifier, addition, removal, or association delta; legal-employer operations and lookups are unsupported in this task | Every request |  |
| CUD attributes | Collect only the action attributes required by the selected operation; preserve omitted edit values from the fresh read | create, edit, or delete |  |
| Parent-child grouping | For each independent request, emit one non-mutating root AssignmentFlexfieldsMapping MERGE row with a blank RestAction and a fresh FlexSegmentMappingGroupKey; repeat that key only in the matching child action row or rows. Multiple independent requests in one DAT require separate root groups and distinct keys | every child CUD source |  |
| Create grouping key | Generate one fresh numeric FlexSegmentMappingGroupKey per independent create request, using current UTC epoch milliseconds and incrementing on a same-source collision; repeat it only in that request's root and create rows, and leave FlexSegmentMappingId ungenerated | create through a child business object |  |
| Existing mapping ID | Use the exact FlexSegmentMappingId fetched by read_assignment_flex_mappings in every update child row; do not use it as the root grouping key | edit through a child business object | read_assignment_flex_mappings |
| CUD template shape | Start from the current raw UCM template, omit only SourceRefTableName and SourceRef001 through SourceRef010, retain every other template column, and retain unused action sections as headers only | create, edit, or delete | fetch_assignment_flex_mapping_loader_template |
| Update child row | Use MERGE for the update row; retain the raw-template update-column order; set FlexSegmentMappingId to the exact current mapping ID; use only the unique FlexSegmentMappingGroupKey of its matching root group; preserve the update RestAction column with an empty value | edit | read_assignment_flex_mappings |
| Delete child row | Use MERGE for the Delete row; set DeleteFlexSegmentMappingIdList to the fetched current mapping ID, use only the unique FlexSegmentMappingGroupKey of its matching root group, and retain the RestAction column with a blank value | delete | read_assignment_flex_mappings |
| Mutation route | Hand CUD source preparation to core.data-loader for AssignmentFlexfieldsMapping; do not submit a direct REST mutation | create, edit, or delete |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AFM.INPUT | decision | 1 | validate_input | valid->AFM.MAPPINGS;missing->AFM.ERROR;invalid->AFM.ERROR;unsupported->AFM.ERROR | none | stop | Every Manage Assignment Flexfield Mapping request |

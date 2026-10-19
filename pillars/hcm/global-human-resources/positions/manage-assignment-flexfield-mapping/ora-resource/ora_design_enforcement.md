# Manage Assignment Flexfield Mapping Design Enforcement

## Purpose

Defines the mandatory mapping compatibility, row-scope, template, parent-child
grouping, and approval gates evaluated before routing.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Read-state check | Fully page the current mapping collection |
| 2 | Compatibility preflight | Confirm the requested source and destination segments are currently exposed, reject a context-specific source mapped to a global destination, and require destination uniqueness. Defer datatype, precision, and value-set compatibility to Fusion Data Loader when the action does not expose it |
| 3 | Row-scope check | Require zero duplicate mappings for create and one exact mapping for edit or delete |
| 4 | CUD-template check | For every CUD operation, preserve the raw live template except SourceRef fields and use the selected action's current contract |
| 5 | Parent-child grouping check | Require each independent request to have its own non-mutating root grouping row and unique FlexSegmentMappingGroupKey; only that request's child CUD rows may carry its key. Child updates and deletes also carry their actual FlexSegmentMappingId separately |
| 6 | Execution boundary | Preview the exact business effect, revalidate current state, obtain approval, and invoke only core.data-loader for CUD |
| 7 | Disclosure check | Omit internal synchronization configuration, routes, and transient identifiers from normal results |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| create or edit | Error | resolve_assignment_flex_context_segment; read_assignment_flex_mappings | A requested segment is unavailable, the source is context-specific while the destination is global, or another current mapping uses the requested destination | Correct the source, destination, or scope pairing before preview | Yes |
| every request | Error |  | The request supplies a legal-employer name, identifier, addition, removal, or association delta | Remove the legal-employer input. This task supports only Position Segment to Assignment Segment mappings and does not fetch or manage Legal Employer data | Yes |
| every request | Error | read_assignment_flex_mappings | Runtime contract or fully paged current state is unavailable | Rediscover and reread current resources | Yes |
| create, edit, or delete | Error | read_assignment_flex_mappings | Duplicate create key, ambiguous selector, or a requested delta outside one exact mapping | Correct the selector or requested values | Yes |
| child create, update, or delete | Error |  | The source omits an independent request's root AssignmentFlexfieldsMapping grouping row, sets a root RestAction, has a blank or mismatched FlexSegmentMappingGroupKey, reuses a key across independent requests, or exposes the grouping key in the custom-method payload | Rebuild the source with one non-mutating root grouping row and one fresh unique FlexSegmentMappingGroupKey for each independent request | Yes |
| child update | Error | read_assignment_flex_mappings | The child row omits the exact fetched FlexSegmentMappingId, uses that ID as the root grouping key, or uses a grouping key other than its matching independent request root | Rebuild the child row with the fetched mapping ID and its matching unique FlexSegmentMappingGroupKey | Yes |
| delete | Error | read_assignment_flex_mappings | The Delete row omits the exact fetched DeleteFlexSegmentMappingIdList, includes FlexSegmentMappingId, uses a grouping key different from its matching root row, or reuses a key assigned to another independent request | Rebuild the Delete row with the fetched delete-list ID and its matching unique FlexSegmentMappingGroupKey | Yes |
| create, edit, or delete | Error | fetch_assignment_flex_mapping_loader_template | The source is based on a generated compact sample, removes any non-SourceRef live template column, changes the live section order, or uses an action row that does not match the selected live-template action contract | Rebuild from the current raw template; omit only SourceRef fields and retain unused action sections as headers only | Yes |
| edit | Error | read_assignment_flex_mappings | The update row omits the exact fetched FlexSegmentMappingId, changes the live update-column order, uses a directive other than MERGE, or sets a nonblank update RestAction | Rebuild the update row from the raw template with MERGE, the fetched ID, and blank RestAction | Yes |
| create, edit, or delete | Error |  | Target or current state differs from preview, approval is missing, or a route other than core.data-loader is selected | Rebuild and approve the exact business delta; use the registered Data Loader business object | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| read_assignment_flex_mappings | Every request | Current mappings and mapping identity | ora_reference_lookups.md |
| fetch_assignment_flex_mapping_loader_template | create, edit, or delete | Current raw DAT sections, headers, action-section order, and allowed SourceRef omission set | ora_reference_lookups.md |
| resolve_assignment_flex_context_segment | Create or edit supplies source or destination values | Current context and segment values with a valid scope pairing | ora_reference_lookups.md |
| Fusion Data Loader validation | A submitted create or edit requires datatype, precision, or value-set compatibility | Fusion acceptance or actionable load diagnostic | core.data-loader |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable design rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AFM.DESIGN | decision | 7 | design_enforcement | passed->AFM.ROUTE;not_required->AFM.ROUTE;blocked->AFM.ERROR | AFM.DEFAULTS | stop | After validation, dependencies, read-only resolution, and defaulting |

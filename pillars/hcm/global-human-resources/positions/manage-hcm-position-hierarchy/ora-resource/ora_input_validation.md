# Input Validation

## Purpose

Defines required inputs, dependency-aware checks, and field validation for
Manage HCM Position Hierarchy before lookup, preview, or routing.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Operation | view_hierarchy, build_hierarchy, add_existing_child, move_position, remove_from_hierarchy, create_child_position, duplicate_position, edit_position, or delete_position | Block | Ask for one supported operation | Every request |  |
| Hierarchy root | Exact Position code or a Position name/search fragment | Block | Provide a Position selector before the ancestor lookup | Hierarchy read or relationship request | find_position_hierarchy_ancestor |
| View date | Explicit unambiguous date, or no date | Default only a view to today's date | Normalize to YYYY-MM-DD for REST | view_hierarchy |  |
| Mutation date | Explicit unambiguous effective start date | Block | Provide the effective date; never default it | Every mutation |  |
| Selected Position | Exact Position code, ID, or uniquely resolvable name | Block | Resolve one effective Position in the displayed full hierarchy | Node action | resolve_position_hierarchy_members |
| Parent or destination | Exact Position code, ID, or uniquely resolvable name | Block | Select one Position through positionsLov; validate its effective details later | Build, add, create child, duplicate, move, or edit with parent change | find_position_hierarchy_ancestor |
| Move mode | with_children or without_children | Block | Ask the user to choose; never infer the mode | move_position |  |
| New Position identity | Unique Position name and Position code | Block | Delegate uniqueness and Position field validation to Manage Positions | create_child_position or duplicate_position | resolve_position_hierarchy_members |
| Source-key provenance | No source keys, or both SourceSystemOwner and SourceSystemId explicitly supplied by the user | Block | Omit source keys or provide the explicit pair | Position Hierarchy XLSX authoring |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| An ancestor or affected Position has zero effective matches | Blocked | Request a corrected exact selector | find_position_hierarchy_ancestor |
| An ancestor or affected Position has multiple matches | Blocked | Show at most five candidates and require one selection | resolve_position_hierarchy_members |
| A new-child or duplicate Position does not yet exist | Ready for combined create | Have Manage Positions author Position.xlsx, author PositionHierarchy.xlsx with matching new-Position keys, and submit both through one core.data-loader preview and ZIP | resolve_position_hierarchy_members |
| A relationship mutation refers to a Position not yet effective for the full relationship range | Blocked | Change the effective range or complete Position setup first | resolve_position_hierarchy_members |
| Live Position Hierarchy metadata differs from the authored workbook | Blocked | Regenerate the sample XLSX from current metadata | inspect_position_hierarchy_loader_contract |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Loader Boolean value | For an included attribute declared by current loader metadata as Boolean or Flag, write true or Yes as Y and false or No as N; preserve Y or N; do not add an omitted attribute or change REST read values | A Data Loader mutation includes the attribute |  |
| REST date format | Normalize an unambiguous input to YYYY-MM-DD; reject an ambiguous date | A REST as-of or verification date is supplied |  |
| Data Loader date format | Write YYYY/MM/DD values in PositionHierarchy cells | Authoring the XLSX |  |
| Relationship user keys | Require PositionCode with BusinessUnitName or BusinessUnitId for the child and ParentPositionCode with ParentBusinessUnitName or ParentBusinessUnitId for the parent unless confirmed Position IDs or explicit source keys are used; for a new Position, require exact equality with its reviewed Position workbook values | Authoring a relationship row | resolve_position_hierarchy_members |
| Business Unit alternatives | Resolve each supplied Business Unit ID or name from the effective Position row; when both are supplied, require them to identify the same Business Unit | A child or parent Business Unit ID or name is supplied | resolve_position_hierarchy_members |
| Effective range | Require both Positions to be effective for the complete relationship range; use fresh REST rows for existing Positions and the reviewed Position workbook for a new Position, then bound the relationship end date to the earliest applicable Position boundary | Authoring a relationship row | resolve_position_hierarchy_members |
| Source keys | Reject partial, inferred, copied, or invented SourceSystemOwner and SourceSystemId values | Either source-key field is populated |  |
| Surrogate identifiers | Leave PositionHierarchyId and GUID blank when confirmed user keys identify the row; when either is supplied for an existing relationship, require an exact current parentPosition match and reject it when that attribute is unavailable | Authoring the XLSX | resolve_position_hierarchy_members |
| Move row set | With children uses only the selected Position row; without children also contains exactly one row per fresh direct child | move_position | read_position_hierarchy_descendants |
| Remove row set | Terminate the selected relationship using the removal-date rule; when direct children exist, add exactly one reparent row per child to the grandparent | remove_from_hierarchy | read_position_hierarchy_descendants |
| Remove date | Reject a date before the earliest relationship start; use MERGE with an end date one day earlier when later, or DELETE when equal | remove_from_hierarchy | resolve_position_hierarchy_members |
| Position versus relationship | Reject Position attributes in PositionHierarchy rows and reject relationship-only changes in a Position workbook | Every mutation | inspect_position_hierarchy_loader_contract |
| Authored mutation source | Require a reviewed XLSX generated from the live business-object template before core.data-loader generates DAT internally | Agent-authored relationship mutation | inspect_position_hierarchy_loader_contract |
| Combined create source | Require reviewed Position.xlsx and PositionHierarchy.xlsx sources, unique resolved business objects, matching new-Position Business Unit/code, and one immutable combined-ZIP preview | create_child_position or duplicate_position | inspect_position_hierarchy_loader_contract |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POSH.INPUT | decision | 1 | validate_input | valid->POSH.DEFAULTS;invalid->POSH.ERROR | none | stop | Validate operation, Position selectors, effective context, move mode, key provenance, and combined Position plus Position Hierarchy source requirements |

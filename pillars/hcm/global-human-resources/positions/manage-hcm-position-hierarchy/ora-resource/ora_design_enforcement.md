# Manage HCM Position Hierarchy Design Enforcement

## Purpose

Defines the mandatory hierarchy graph, relationship, source-set, key, preview,
and verification design gates. It does not perform lookups, apply defaults, or
change an underlying Position implicitly.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm graph | When required, complete every page and validate all parent links. |
| 2 | Confirm operation identities | Resolve selected, parent, destination, child, and new Position identities for one effective context. |
| 3 | Prevent invalid design | Reject a self-parent, cycle, duplicate edge, no-op, missing original parent, and range gap. |
| 4 | Select the owning object | Use Position Hierarchy only for relationship rows; delegate Position attributes and Position lifecycle actions to Manage Positions. |
| 5 | Build the exact source set | Apply the build, add, move, remove, or combined Position plus Position Hierarchy create algorithm without extra rows. |
| 6 | Apply Data Loader keys | Prefer confirmed user keys; never invent source keys or surrogate identifiers. |
| 7 | Preview and approve | Bind the immutable operation-specific source set and complete assertions to one standalone approval. |
| 8 | Revalidate and verify | Recheck fresh state before upload and prove all relationships after completion. |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| GRAPH | View, build, existing-child add, move, removal, Position delete, or parent edit | Blocking | read_position_hierarchy_descendants | Required pagination is incomplete, or the graph has duplicate IDs, cycles, multiple parents, or unresolved or disconnected nodes | Correct access or hierarchy data and rebuild the graph | Lookup fix |
| MEMBERS | Every mutation | Blocking | resolve_position_hierarchy_members | A required Position or effective row is missing, ambiguous, inaccessible, or outside range, or a new child or duplicate lacks reviewed Position source in the combined load | Supply exact Position codes, a valid effective date, and any required reviewed Position source | Input fix |
| RELATIONSHIP | Build, add, move, or create link | Blocking | resolve_position_hierarchy_members | Child equals parent, destination is a descendant, the edge exists, or the relationship range exceeds either Position range | Select a valid parent and bounded range | Input fix |
| MOVE_MODE | move_position | Blocking | read_position_hierarchy_descendants | Move mode is absent, inferred, or not with_children or without_children | Supply one explicit supported mode | Input fix |
| MOVE_WITH_CHILDREN | move_position with children | Blocking | read_position_hierarchy_descendants | The workbook contains direct-child rows or changes a child relationship | Keep exactly one selected-Position relationship row | Source rebuild |
| MOVE_WITHOUT_CHILDREN | move_position without children | Blocking | read_position_hierarchy_descendants | Original parent is absent, the direct-child snapshot is stale or incomplete, or a direct child is omitted, duplicated, or assigned away from the original parent | Rebuild one XLSX with the selected row and exactly one row per direct child | Source rebuild |
| REMOVE | remove_from_hierarchy | Blocking | read_position_hierarchy_descendants | The selected node has no parent, its earliest relationship start is unknown, removal precedes that start, MERGE is not used for a later date, DELETE is not used for the same date, or children are not reassigned to the grandparent | Refresh the relationship history and rebuild the required removal and reparent rows | Source rebuild |
| COMBINED_CREATE | create_child_position or duplicate_position | Blocking | resolve_position_hierarchy_members | Position.xlsx or PositionHierarchy.xlsx is absent, their Business Unit or code differs, live validation fails, DAT members are not named Position.dat and PositionHierarchy.dat, or separate submissions are planned | Rebuild both reviewed sources and one immutable combined ZIP | Source rebuild |
| DELETE_POSITION | delete_position | Blocking | resolve_position_hierarchy_members | The Position has an incumbent or child, or deletion is attempted through Position Hierarchy | Remove dependencies, then use Manage Positions for the leaf Position delete | No |
| XLSX_SOURCE | Agent-authored relationship mutation | Blocking | inspect_position_hierarchy_loader_contract | Source is not a fresh reviewed Position Hierarchy XLSX, headers differ, or another sheet has data | Regenerate from live metadata and retain only required relationship rows | Source rebuild |
| KEYS | Any Data Loader row | Blocking | inspect_position_hierarchy_loader_contract | Source keys are partial or invented, PositionHierarchyId or GUID is unverified, a Business Unit ID conflicts with its name, or a required key alternative is incomplete | Use one confirmed Business Unit name-or-ID plus PositionCode pair for each side, confirmed Position IDs, or one complete explicit source-key strategy | Source rebuild |
| PREVIEW | Before load | Blocking | verify_position_hierarchy_result | Preview omits an affected row, old or new parent, effective range, environment alias, source identity, combined-ZIP fingerprint, dependency order, or verification assertion, or standalone approval is absent or stale | Rebuild the complete immutable preview and obtain standalone approval | Re-preview |
| VERIFY | After load | Blocking | verify_position_hierarchy_result | Affected relationships are not observed in fresh applicable reads | Return failed, reconcile current state, and do not retry automatically | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| read_position_hierarchy_descendants | An operation requires descendants or cycle evidence | Complete parent map, descendant set, direct children, and page completeness | ora_reference_lookups.md |
| resolve_position_hierarchy_members | Every operation-specific Position or relationship | Exact identity, Business Unit, effective range, old parent, and later split | ora_reference_lookups.md |
| inspect_position_hierarchy_loader_contract | Every relationship mutation | Current section, headers, key alternatives, and source fingerprint | ora_reference_lookups.md |
| verify_position_hierarchy_result | Before approval assertion design and after load | Expected and observed child-parent relationships | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POSH.DESIGN | decision | 9 | design_enforcement | passed->POSH.ROUTE;not_required->POSH.ROUTE;blocked->POSH.ERROR | POSH.DEPENDENCIES | stop | After validation, dependencies, lookups, and defaulting are complete |

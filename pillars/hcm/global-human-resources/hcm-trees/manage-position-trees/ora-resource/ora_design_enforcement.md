# Manage Position Trees Design Enforcement

## Purpose

Enforces the fixed Position Tree structure, current member identity resolution, and internal creation parameters before common Trees execution.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Select route | Use core.fusion-api.apps-common.trees for every operation |
| 2 | Confirm structure | Retain PER_POS_TREE_STRUCTURE for the entire request |
| 3 | Resolve hierarchy members | Convert every supplied position name to one current PositionId and preserve the requested parent graph |
| 4 | Bind creation parameters | Bind both seeded position-tree parameter tuples internally for a create |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Blocking |  | The request bypasses core.fusion-api.apps-common.trees | Route the complete operation to the common Trees skill | Yes |
| Every request | Blocking |  | TreeStructureCode is not PER_POS_TREE_STRUCTURE | Correct the structure code before planning | Yes |
| A hierarchy is supplied by position name | Blocking | resolve_position_members_by_name | Any position name has zero or multiple exact matches, or a resolved ID is substituted with another value | Stop for a unique current position identity; form the common Trees request from the resolved IDs and requested parent graph | Yes |
| Create tree | Blocking |  | The task does not bind the complete seeded data-source parameter collection | Bind the complete seeded parameter collection unchanged; never request it from the user | Yes |
| Update a version | Blocking | resolve_position_tree_version_by_identity | A creation-only EffectiveEndDate default would overwrite an existing version value | Rebuild the update from the freshly resolved current version and only explicit changes | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_position_members_by_name | A hierarchy supplies position names | One PositionId for every supplied name and the preserved parent graph | ora_reference_lookups.md |
| resolve_position_tree_version_by_identity | An existing version is read or updated | Exact Draft version identity and current values to preserve | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POSTREE.DESIGN | decision | 5 | design_enforcement | pass->POSTREE.CORE_HANDOFF;blocked->POSTREE.ERROR | POSTREE.DEFAULTS | stop | Every request |

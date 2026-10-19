# Manage Department Trees Design Enforcement

## Purpose

Enforces the fixed Department Tree structure, current member identity resolution, and internal creation parameters before common Trees execution.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Select route | Use core.fusion-api.apps-common.trees for every operation |
| 2 | Confirm structure | Retain PER_DEPT_TREE_STRUCTURE for the entire request |
| 3 | Resolve hierarchy members | Convert every supplied department name to one current DepartmentId and preserve the requested parent graph |
| 4 | Bind creation parameters | Bind both seeded department-tree parameter tuples internally for a create |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Blocking |  | The request bypasses core.fusion-api.apps-common.trees | Route the complete operation to the common Trees skill | Yes |
| Every request | Blocking |  | TreeStructureCode is not PER_DEPT_TREE_STRUCTURE | Correct the structure code before planning | Yes |
| A hierarchy is supplied by department name | Blocking | resolve_department_members_by_name | Any department name has zero or multiple exact matches, or a resolved ID is substituted with another value | Stop for a unique current department identity; form the common Trees request from the resolved IDs and requested parent graph | Yes |
| Create tree | Blocking |  | The task does not bind the complete seeded data-source parameter collection | Bind the complete seeded parameter collection unchanged; never request it from the user | Yes |
| Update a version | Blocking | resolve_department_tree_version_by_identity | A creation-only EffectiveEndDate default would overwrite an existing version value | Rebuild the update from the freshly resolved current version and only explicit changes | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_department_members_by_name | A hierarchy supplies department names | One DepartmentId for every supplied name and the preserved parent graph | ora_reference_lookups.md |
| resolve_department_tree_version_by_identity | An existing version is read or updated | Exact Draft version identity and current values to preserve | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DEPTTREE.DESIGN | decision | 5 | design_enforcement | pass->DEPTTREE.CORE_HANDOFF;blocked->DEPTTREE.ERROR | DEPTTREE.DEFAULTS | stop | Every request |

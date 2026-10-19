# Manage Organization Trees Dependency Readiness

## Purpose

Defines the dependency order for Organization Tree identity, version state, member resolution, and internal data-source parameters.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Request identity | Validate the requested tree operation and PER_ORG_TREE_STRUCTURE |
| 2 | Common Trees route | Hand the operation only to core.fusion-api.apps-common.trees |
| 3 | Organization member resolution | Resolve every supplied organization name to one current OrganizationId |
| 4 | Data source parameters | For tree creation, the task binds the complete seeded parameter collection internally |
| 5 | Existing version state | For a version update, resolve one current Draft version and preserve all unrequested values |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| common_trees_route | Common Trees execution route | Yes | Every request | Satisfied | Task contract |  | Centralizes tree planning, validation, execution, and verification | Do not use another tree client or a direct task-local route | core skill: core.fusion-api.apps-common.trees |
| organization_member_resolution | Organization member identities | Yes | A hierarchy names one or more organizations | Lookup | Current organizationsLov response | resolve_organization_members_by_name | Converts business names into the source identities required by the common Trees skill | Resolve every distinct name exactly; do not select a first row | OrganizationName to OrganizationId and requested parent relationship |
| organization_tree_parameters | Organization tree data source parameters | Yes | Create tree | Satisfied | Seeded task configuration |  | Tree creation requires the complete data-source parameter collection | Bind both parameter tuples internally; never ask the user for data-source or parameter identifiers | DataSourceId: 6565DB26E88AFBFAE04044987CF0426B; ParameterId: 6DB2F4C9CFC98AC6E040578C485D5FBF; ParameterValue: #{treeVersion.effectiveEndDate}; ParameterId: 6DB2F4C9CFCA8AC6E040578C485D5FBF; ParameterValue: #{treeVersion.effectiveStartDate} |
| organization_tree_version | Existing Organization Tree version | Conditional | Update a version | Lookup | Current fndTreeVersions response | resolve_organization_tree_version_by_identity | Prevents creation defaults from overwriting an existing version | Supply one exact tree version identity and requested changes | TreeVersionId, current dates, and Draft status |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Ready | The task request and every applicable dependency are complete | Yes, only through core.fusion-api.apps-common.trees |
| Missing | A required business request value is absent | No |
| Blocked | A direct, unsupported, or task-local tree route is requested | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ORGTREE.CORE_READY | decision | 2 | resolve_dependency | ready->ORGTREE.RESOLVE_MEMBERS;missing->ORGTREE.ERROR;blocked->ORGTREE.ERROR | ORGTREE.VALIDATE | stop | Every request |

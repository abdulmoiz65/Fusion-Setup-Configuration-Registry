# Manage HCM Position Hierarchy Dependency Readiness

## Purpose

Defines the conditional hierarchy configuration, Position-member, graph, and
Position-staging references used by Manage HCM Position Hierarchy. The task
checks existing evidence only and never creates or changes a Position implicitly.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Hierarchy configuration | Confirm that HCM Position Hierarchy is enabled for the requested hierarchy work |
| 2 | Position visibility | Confirm the selected ancestor and affected Positions are visible through the applicable security profile |
| 3 | Effective Position members | Resolve every supplied parent and child Position in the requested effective context |
| 4 | Current hierarchy graph | Read the complete graph only when descendants or cycle evidence is required |
| 5 | Position Hierarchy schema | Resolve the live Position Hierarchy section, headers, keys, and parent links for a relationship mutation |
| 6 | Position staging evidence | For a new child or duplicate, require reviewed Position source in the same combined load; handle other Position maintenance separately |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| hierarchy_configuration | HCM Position Hierarchy enabled state | Conditional | A hierarchy read or relationship request is made | Verify | Current Enterprise HCM configuration |  | Prevents hierarchy processing when the selected feature context is unavailable | Confirm the hierarchy feature through its owning setup when needed | Enabled state evidence |
| hierarchy_access | Position hierarchy visibility | Conditional | An ancestor or parent reference is requested | Lookup | Positions LOV | find_position_hierarchy_ancestor | Prevents an unresolved hierarchy reference caused by security filtering | Use an authorized role and applicable Position security profile | Visible ancestor or parent evidence |
| position_members | Effective parent and child Positions | Conditional | A hierarchy relationship or member is requested | Lookup | Positions resource or reviewed Position source in the same combined load | resolve_position_hierarchy_members | Requires each relationship Position to exist or be supplied in the same combined load and to be effective for the requested range | Provide one exact selector for each existing Position or the reviewed new-Position source | Position IDs and codes, Business Unit IDs and names, current parent identity, and effective bounds |
| hierarchy_graph | Complete current parent-child graph | Conditional | A view, build, existing-child add, move, removal, Position delete, or parent edit requires descendants or cycle evidence | Lookup | Position Searches and Positions resource | read_position_hierarchy_descendants | Prevents decisions based on an incomplete or stale graph | Provide one exact ancestor and effective context | Parent map, direct children, descendants, and completeness evidence |
| loader_contract | Position Hierarchy live schema | Conditional | A relationship mutation is requested | Lookup | Current Position Hierarchy business-object metadata | inspect_position_hierarchy_loader_contract | Prevents guessed headers, keys, and business-object identity | Regenerate the Position Hierarchy source from current metadata when the contract changes | PositionHierarchy section, headers, keys, and parent-link metadata |
| manage_positions_staging | Underlying Position staging evidence | Conditional | A new child, duplicate, Position attribute edit, inactivation, or Position delete is requested with hierarchy work | Verify | Separately reviewed Manage Positions result |  | PositionHierarchy rows cannot create, edit, inactivate, or delete the underlying Position | For a new child or duplicate, provide reviewed Position source for the same combined preview; complete other Position operations separately | Position source and identity or completed Position-operation evidence |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Every applicable dependency has exact authoritative evidence | No |
| Lookup | A documented resolver can resolve an applicable dependency | Read-only lookup only |
| Verify | Existing evidence must be confirmed without creating setup | No |
| Not Applicable | A dependency condition is false | No |
| Needs Input | A required selector or scope value is missing | No |
| Unresolved | Resolution returns no match, multiple matches, unavailable evidence, or an incompatible value | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POSH.DEPENDENCIES | decision | 8 | resolve_dependency | ready->POSH.DESIGN;not_required->POSH.DESIGN;needs_input->POSH.ERROR;unresolved->POSH.ERROR | POSH.LOADER_CONTRACT | stop | After applicable hierarchy reference lookups and before design enforcement |

# Manage Position Trees Input Validation

## Purpose

Defines the business inputs needed to route Position Tree work to the common Trees skill without asking users for internally defaulted version end dates.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Tree request | Operation, TreeCode or exact existing tree identity, and requested scope | Blocked | Provide the requested tree operation and its exact target or creation identity | Every request |  |
| Position tree structure | TreeStructureCode = PER_POS_TREE_STRUCTURE | Blocked | Use the position-tree structure code only | Every request |  |
| New tree version | TreeVersionName and EffectiveStartDate | Blocked | Provide the Draft version identity and effective start date; bind EffectiveEndDate internally as 4712-12-31 when omitted | Create a version |  |
| Existing tree version | Exact existing version identity and requested changes | Blocked | Resolve the current Draft version, retain every unrequested current value, and require only the requested changes | Update a version |  |
| Position nodes | Existing position source values and parent relationships | Blocked | Provide each intended position member and parent relationship | Add, move, or remove nodes |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Required fields are complete and the structure code is exact | Valid | Route the request to core.fusion-api.apps-common.trees |  |
| A required field is missing or the structure code differs | Blocked | Stop and request the missing or corrected value |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Tree structure code | Accept only PER_POS_TREE_STRUCTURE | Every request |  |
| Tree code and version identity | Require exact values; do not use a display name as a substitute for a tree code | Existing-tree operation |  |
| New-version dates | Require a valid EffectiveStartDate; bind EffectiveEndDate internally as 4712-12-31 only when it is omitted, then validate the resulting interval | Create a version |  |
| Existing-version dates | Validate every explicitly changed date against freshly read current values; preserve an omitted EffectiveEndDate | Update a version |  |
| Node membership | Treat source position identities as source records, not generated tree-node identifiers | Node operation |  |
| Named hierarchy members | Resolve every supplied position name to exactly one current PositionId and preserve each requested parent relationship | Create or change nodes from names | resolve_position_members_by_name |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| POSTREE.VALIDATE | decision | 1 | validate_input | valid->POSTREE.CORE_READY;missing->POSTREE.ERROR;invalid->POSTREE.ERROR | none | stop | Every request |

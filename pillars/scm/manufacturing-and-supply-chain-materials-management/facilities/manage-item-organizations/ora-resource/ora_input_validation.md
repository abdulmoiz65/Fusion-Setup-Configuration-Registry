# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Creation record | OrganizationName, OrganizationCode, MasterOrganizationName or MasterOrganizationCode, ItemGroupingCode, and ItemDefinitionOrganizationName | Block | Provide the missing value, then rerun local defaulting and validation | Creation |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| OrganizationCode <= 18 and OrganizationName <= 240 characters | Return correction; do not query Fusion | Values are present |  |
| InventoryFlag is null or true after defaulting | Stop; an inventory organization cannot be the item master, and the flag must be explicitly resolved to false | Creation |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| MIO.VALIDATE | decision | 2 | validate_input | valid->MIO.DESIGN_GATE;invalid->MIO.HANDLE_ISSUE | MIO.APPLY_DEFAULTS | stop | Creation |

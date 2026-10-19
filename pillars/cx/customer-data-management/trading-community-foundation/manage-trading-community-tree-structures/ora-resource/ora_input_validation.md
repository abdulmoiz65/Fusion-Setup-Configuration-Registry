# Input Validation

Source: Oracle Fusion Cloud Financials, Guidelines for Managing Tree Structures — https://docs.oracle.com/en/cloud/saas/financials/26c/faigl/guidelines-for-managing-tree-structures.html#s20030940

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested lifecycle action | Create, edit, delete, copy, or status change, plus the tree-structure identity and affected scope | Stop before preview | Provide the intended action and the exact tree structure to be affected | Any request |  |
| Status selection | Draft, Active, or Inactive | Stop before preview when a status change is requested without one of the documented statuses | Provide one documented status | Status change |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Tree-structure status | Accept only Draft, Active, or Inactive as documented lifecycle statuses | Status change |  |
| Active-structure edit impact | Treat the tree structure and all associated trees and tree versions as changing to Draft | Edit of an Active tree structure |  |

## FSM Import Contract

Before an import preview, require one unchanged ZIP with a valid ZIP signature,
exactly one `ASM_SETUP_CSV_METADATA.xml` member, and exactly one
`ObjectShortName` value of `ORA_HZ_MANAGE_TREE_STRUCTURES`. Bind the absolute
ZIP path, SHA-256, target environment, `executionRoute=data-loader`, and the
task-local native FSM adapter to the approval envelope.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCS.VALIDATE_INPUT | step | 1 | validate_input | valid->TCS.DESIGN_REVIEW;invalid->TCS.RETURN_ISSUES | none | stop | Before any create, edit, delete, copy, or status-change preview. |

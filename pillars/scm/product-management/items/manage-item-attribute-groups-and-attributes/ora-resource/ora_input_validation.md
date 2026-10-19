# Input Validation

Source: developer-provided Oracle UI captures for this setup task and the
developer-provided FSM CSV export dated 2026-09-14. This resource contains
only Items-specific functional rules. EFF CSV transport, Value Set mechanics,
and deployment are owned by the shared Apps Common EFF workflow.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Attribute group definition | Context usage Item; Internal Name; Behavior Single Row or Multiple Row | Stop before preparing a group definition | Provide the missing group detail | A new or changed attribute group is requested | |
| Attribute definition | Attribute name and a Value Set decision when the attribute uses a value set | Stop before preparing the affected attribute | Provide the missing attribute detail; the shared EFF workflow handles creation or reuse of the Value Set | A new or changed attribute is requested | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Context usage | Reject a group definition unless its context usage is Item | An attribute group is supplied | |
| Internal Name comma prohibition | Reject an Internal Name that contains a comma | An Internal Name is supplied | |
| Behavior | Reject a behavior other than Single Row or Multiple Row | Attribute group behavior is supplied | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IAG.VALIDATE_INPUT | step | 10 | validate_input | valid->IAG.READY;invalid->RETURN_ISSUES | none | stop | A Manage Item Attribute Groups and Attributes request is supplied |

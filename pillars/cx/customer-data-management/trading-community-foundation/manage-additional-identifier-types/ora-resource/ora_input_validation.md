# Input Validation

Source: Oracle Fusion Cloud Sales, Manage Identifier Types — https://docs.oracle.com/en/cloud/saas/sales/oacdm/manage-identifier-types.html#Create-Additional-Identifier-Types

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Create identifier type | Party Type, short name, Additional Identifier descriptive name, and unique-name selection | Stop before preview | Provide every required field from the Manage Additional Identifier Types page | Create |  |
| Edit identifier type | Exact existing identifier type, Additional Identifier descriptive name or Description | Stop before preview | Provide the target identifier type and at least one editable field | Edit |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Party Type | Require the party type that can use the additional identifier type | Create |  |
| Short name | Require a short name used by the application to reference the identifier type and require it to be unique | Create |  |
| Additional Identifier | Require a descriptive name | Create |  |
| Description | Permit an optional description | Create or edit |  |
| Unique-name selection | Require an explicit selection that determines whether multiple entries of the identifier type can be added to a party | Create |  |

## FSM Import Contract

Before an import preview, require one unchanged ZIP with a valid ZIP signature,
exactly one `ASM_SETUP_CSV_METADATA.xml` member, and exactly one
`ObjectShortName` value of `HZ_MANAGE_ADDITIONAL_IDENTIFIER_TYPES`. Bind the
absolute ZIP path, SHA-256, target environment, `executionRoute=data-loader`,
and the task-local native FSM adapter to the approval envelope. Reject generic
Data Loader upload and initiation routes.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AIT.VALIDATE_INPUT | step | 1 | validate_input | valid->AIT.DESIGN_REVIEW;invalid->AIT.RETURN_ISSUES | none | stop | Before a create or edit preview. |

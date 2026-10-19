# Design Enforcement

Source: Oracle Fusion Cloud Sales, Manage Identifier Types — https://docs.oracle.com/en/cloud/saas/sales/oacdm/manage-identifier-types.html#Create-Additional-Identifier-Types

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Select party type | Identify the organization or person party type that can use the new additional identifier type. |
| 2 | Validate short name | Confirm the application reference short name is unique. |
| 3 | Confirm multiplicity | Explicitly decide whether multiple entries of this identifier type may be added to a party. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Create | Error |  | Party Type is absent | Select the party type that can use the additional identifier type | Yes |
| Create | Error |  | Short name is absent or not unique | Provide a unique short name used by the application to reference the identifier type | Yes |
| Create | Error |  | Additional Identifier descriptive name is absent | Provide a descriptive name | Yes |
| Create | Error |  | Unique-name selection is absent | Specify whether multiple entries of this identifier type can be added to a party | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| AIT.DESIGN_REVIEW | decision | 2 | design_enforcement | pass->AIT.EXECUTION_GATE;fail->AIT.RETURN_ISSUES | AIT.VALIDATE_INPUT | stop | Before a create or edit preview. |

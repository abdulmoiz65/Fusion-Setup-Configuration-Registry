# Manage Resource Role Descriptive Flexfields Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Plan | Identify the business-object attribute need and validation design before changing the flexfield |
| 2 | Configure | Define the required global, context, or context-sensitive segment properties |
| 3 | Test | Deploy the descriptive-flexfield change to a sandbox and test it |
| 4 | Publish | Publish only the tested sandbox change through the existing Apps Common DFF route |
| 5 | Integrate | Complete required downstream technology-stack integration for the configured attributes |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any DFF configuration | Blocker |  | The request does not identify the user-defined attribute need and validation approach | Plan the DFF configuration and validation before defining segments | Yes |
| Defining a global segment | Blocker |  | Identity information, initial default value, or display properties are incomplete | Supply the complete global-segment definition | Yes |
| Defining a context | Blocker |  | Context code, name, description, or its context-sensitive segment definition is incomplete | Supply a complete context definition | Yes |
| Deploying a descriptive-flexfield change | Blocker |  | No sandbox deployment and test evidence is available before publication | Deploy to a sandbox, test, then publish | Yes |
| Retiring a context | Blocker |  | The request deletes an existing context | End-date the associated context value instead of deleting the context | Yes |
| Enabling Business Intelligence | Warning |  | No BI label has been selected for a segment intended for BI use | Select the appropriate BI label before enabling BI | Yes |
| Changes across usages | Warning |  | The requester has not assessed other usages of the same flexfield definition | Review all affected entities or application tables before configuration | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRRDFF.DESIGN_GUARD | decision | 3 | design_enforcement | passed->MRRDFF.DONE;blocked->MRRDFF.BLOCKED | MRRDFF.VALIDATE_INPUT, MRRDFF.APPLY_DEFAULTS | stop | Every validated DFF request |

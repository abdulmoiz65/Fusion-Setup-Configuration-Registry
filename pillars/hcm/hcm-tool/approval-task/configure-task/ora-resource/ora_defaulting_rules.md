# Defaulting Rules

## Source Material

- [Approval Management Configuration Options for Oracle Fusion Human Capital Management](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/approval-management-configuration-options-for-oracle-fusion.html)

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Ad hoc insertion of approvers | True | The task retains the HCM family default. | Yes |  |
| Allow delegate | True | The task retains the HCM family default. | Yes |  |
| Allow push back | True | The task retains the HCM family default. | Yes |  |
| Allow reassign | True | The task retains the HCM family default. | Yes |  |
| Allow request information | True | The task retains the HCM family default. | Yes |  |
| Allow self-approval | False | The task retains the HCM family default. | Yes |  |
| Allow withdraw | True | The task retains the HCM family default. | Yes |  |
| Period before task expires | None | The task retains the HCM family default. | Yes |  |
| Period before task escalates | None | The task retains the HCM family default. | Yes |  |
| Repeated approver frequency | Once per approval | The task retains the HCM family default. | Yes |  |
| Re-evaluate approver list | True | The task retains the HCM family default. | Yes |  |
| Rejection outcome | Stop all | The task retains the HCM family default. | Yes |  |
| commitNeededFlag | true | The request does not explicitly provide commitNeededFlag for writeTaskConfiguration. | Yes |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TASK_CONFIG.APPLY_DOCUMENTED_DEFAULTS | step | 5 | apply_default | reviewed->TASK_CONFIG.ENFORCE_DESIGN;defaults_uncertain->TASK_CONFIG.MISSING_INPUT | TASK_CONFIG.READ_CONFIGURATION | stop | The exact approval process and current configuration were read |

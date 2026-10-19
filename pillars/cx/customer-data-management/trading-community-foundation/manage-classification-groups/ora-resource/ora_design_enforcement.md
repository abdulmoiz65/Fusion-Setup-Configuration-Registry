# Design Enforcement

Do not apply task-specific business-design gates to an unchanged Manage
Classification Groups FSM package. Package import does not by itself prove that
the target's active industry classification setting is changing.

Official sources:

- [Define Auxiliary Dimensions](https://docs.oracle.com/en/cloud/saas/sales/fastr/define-auxiliary-dimensions.html)
- [Overview of Account and Contact Setup](https://docs.oracle.com/en/cloud/saas/sales/fadsi/overview-of-account-and-contact-setup.html)

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve package intent | Validate and submit the package as one immutable task artifact without interpreting individual group or category rows as a separate design request |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| An unchanged FSM package is imported | None | | None beyond objective task and package validation | Do not request category-existence, territory-impact, account-impact, or offering-context acknowledgement | Not applicable |
| The user separately asks to change the active classification used by territories or accounts | Outside this import gate | | Do not infer this separate change from package contents | Route that explicit request to its owning setup workflow | Not applicable |

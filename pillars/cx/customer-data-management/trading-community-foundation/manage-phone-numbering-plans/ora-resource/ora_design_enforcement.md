# Design Enforcement

Do not apply task-specific business-design gates to an unchanged Manage Phone
Numbering Plans FSM package. Package import does not by itself prove that a
separate telephony-design change is being requested.

Official sources:

- [Telephone Numbering Plan overview](https://docs.oracle.com/en/cloud/saas/sales/oacdm/telephone-numbering-plan.html)
- [Manage Phone Numbering Plans procedure](https://docs.oracle.com/en/cloud/saas/sales/oacdm/update-telephone-numbering-plans.html)

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Preserve package intent | Validate and submit the package as one immutable task artifact without interpreting individual country, area-code, prefix, or format rows as a separate design request |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| An unchanged FSM package is imported | None | | None beyond objective task and package validation | Do not request country, area-code, mobile-prefix, number-format, downstream-impact, or offering-context acknowledgement | Not applicable |
| The user separately asks to redesign telephone-number formats or validation behavior | Outside this import gate | | Do not infer this separate change from package contents | Route that explicit request to its owning setup workflow | Not applicable |
